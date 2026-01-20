import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from .. import config, data, strategy
from .portfolio import Portfolio
from .metrics import PerformanceMetrics


class BacktestEngine:
    """
    Main backtesting engine that orchestrates the backtesting process
    """
    
    def __init__(self, 
                 start_date: str = "2022-01-01",
                 end_date: str = "2024-12-31",
                 initial_cash: float = 100000000,
                 commission: float = 0.002):
        """
        Initialize backtesting engine
        
        Args:
            start_date: Backtest start date (YYYY-MM-DD)
            end_date: Backtest end date (YYYY-MM-DD)
            initial_cash: Starting capital in IDR
            commission: Commission rate per trade
        """
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.commission = commission
        
        # Initialize portfolio and metrics
        self.portfolio = Portfolio(initial_cash)
        self.metrics = PerformanceMetrics()
        
    def run_backtest(self, tickers: List[str], **strategy_params) -> Dict:
        """
        Run backtest on given tickers
        
        Args:
            tickers: List of stock tickers to test
            **strategy_params: Override strategy parameters
            
        Returns:
            Dictionary with backtest results
        """
        results = []
        
        for ticker in tickers:
            print(f"Backtesting {ticker}...", end="\r")
            
            # Fetch historical data
            df = data.fetch_data(ticker, 
                               period=None, 
                               interval="1d",
                               start_date=self.start_date,
                               end_date=self.end_date)
            
            if df is None or df.empty:
                print(f"No data available for {ticker}")
                continue
                
            # Run individual backtest
            result = self._run_single_backtest(ticker, df, **strategy_params)
            if result:
                results.append(result)
                
        print(" " * 50, end="\r")  # Clear line
        
        # Aggregate results
        if results:
            return self._aggregate_results(results)
        else:
            return {"error": "No valid backtest results"}
            
    def _run_single_backtest(self, ticker: str, df: pd.DataFrame, **strategy_params) -> Optional[Dict]:
        """Run backtest for a single ticker using custom implementation"""
        try:
            # Initialize portfolio for this ticker
            portfolio = Portfolio(self.initial_cash)
            
            # List to store completed trades
            completed_trades = []
            equity_curve = []
            
            # Iterate through each day
            for i in range(len(df)):
                current_date = pd.to_datetime(df.index[i])
                current_data = df.iloc[:i+1]  # Data up to current date
                
                if len(current_data) < max(config.SLOW_EMA, config.ATR_PERIOD, config.RSI_PERIOD):
                    # Not enough data for analysis
                    continue
                
                # Run strategy analysis on current data
                analysis = strategy.analyze_ticker(current_data)
                if not analysis:
                    continue
                
                current_price = analysis['current_price']
                
                # Check for entry signals
                if analysis['is_setup'] and not portfolio.positions:
                    # Apply additional filters
                    if self._validate_entry_signal(analysis):
                        # Calculate position size
                        position_value = self.initial_cash * config.RISK_PER_TRADE * 10  # Risk 1%, 10:1 RR
                        shares = int(position_value / current_price / 100) * 100  # Round to lots
                        
                        # Check if we can afford this position
                        cost = shares * current_price * (1 + config.COMMISSION_RATE)
                        if cost <= portfolio.cash:
                            # Open position
                            position = portfolio.open_position(
                                ticker=ticker,
                                shares=shares,
                                entry_price=current_price,
                                stop_loss=analysis['stop_loss'],
                                take_profit=analysis['take_profit_min'],
                                entry_time=current_date.to_pydatetime() if hasattr(current_date, 'to_pydatetime') else current_date
                            )
                
                # Check exit conditions for existing positions
                if ticker in portfolio.positions:
                    position = portfolio.positions[ticker]
                    
                    # Check if stop loss or take profit hit
                    should_exit = False
                    exit_reason = 'MANUAL'
                    
                    if current_price <= position['stop_loss']:
                        should_exit = True
                        exit_reason = 'STOP_LOSS'
                    elif current_price >= position['take_profit']:
                        should_exit = True
                        exit_reason = 'TAKE_PROFIT'
                    
                    if should_exit:
                        # Close position
                        closed_position = portfolio.close_position(
                            ticker=ticker,
                            exit_price=current_price,
                            exit_time=current_date.to_pydatetime() if hasattr(current_date, 'to_pydatetime') else current_date,
                            exit_reason=exit_reason
                        )
                        if closed_position:
                            completed_trades.append(closed_position)
                
                # Update portfolio
                current_prices = {ticker: current_price}
                portfolio.update_positions(current_prices, current_date.to_pydatetime() if hasattr(current_date, 'to_pydatetime') else current_date)
                equity_curve.append({
                    'date': current_date,
                    'equity': portfolio.equity
                })
            
            # Convert trades to DataFrame
            if completed_trades:
                trades_df = pd.DataFrame(completed_trades)
            else:
                trades_df = pd.DataFrame()
            
            # Convert equity curve to DataFrame
            equity_df = pd.DataFrame(equity_curve)
            if not equity_df.empty:
                equity_df.set_index('date', inplace=True)
            
            # Calculate metrics
            win_rate = self._calculate_win_rate(completed_trades)
            profit_factor = self._calculate_profit_factor_trades(completed_trades)
            
            return {
                'ticker': ticker,
                'stats': {},  # Empty for now
                'trades': trades_df,
                'equity_curve': equity_df,
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_trades': len(completed_trades),
                'final_equity': portfolio.equity,
                'total_return': ((portfolio.equity - self.initial_cash) / self.initial_cash) * 100,
                'max_drawdown': portfolio.max_drawdown,
                'sharpe_ratio': self._calculate_sharpe_ratio(equity_df),
                'avg_trade_duration': self._calculate_avg_duration(completed_trades)
            }
            
        except Exception as e:
            print(f"Error backtesting {ticker}: {e}")
            return None
    
    def _validate_entry_signal(self, analysis: Dict) -> bool:
        """Validate entry signal using additional filters"""
        # RSI filter
        rsi = analysis.get('rsi', 50)
        if rsi > config.RSI_OVERBOUGHT or rsi < 40:
            return False
            
        # Volume filter
        vol_ratio = analysis.get('vol_ratio', 1.0)
        if vol_ratio < config.VOL_RATIO_MIN:
            return False
            
        return True
    
    def _calculate_win_rate(self, trades: List[Dict]) -> float:
        """Calculate win rate from trades list"""
        if not trades:
            return 0.0
        winning_trades = len([t for t in trades if t.get('realized_pnl', 0) > 0])
        return (winning_trades / len(trades)) * 100
    
    def _calculate_profit_factor_trades(self, trades: List[Dict]) -> float:
        """Calculate profit factor from trades list"""
        if not trades:
            return 0.0
            
        gross_wins = sum(t.get('realized_pnl', 0) for t in trades if t.get('realized_pnl', 0) > 0)
        gross_losses = abs(sum(t.get('realized_pnl', 0) for t in trades if t.get('realized_pnl', 0) < 0))
        
        if gross_losses == 0:
            return float('inf') if gross_wins > 0 else 0
            
        return gross_wins / gross_losses
    
    def _calculate_sharpe_ratio(self, equity_df: pd.DataFrame) -> float:
        """Calculate Sharpe ratio from equity curve"""
        if equity_df.empty or len(equity_df) < 2:
            return 0.0
            
        returns = equity_df['equity'].pct_change().dropna()
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
            
        # Annualized Sharpe ratio (assuming 252 trading days)
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
        return sharpe
    
    def _calculate_avg_duration(self, trades: List[Dict]) -> float:
        """Calculate average trade duration in days"""
        if not trades:
            return 0.0
            
        durations = [t.get('duration_days', 0) for t in trades]
        return np.mean(durations) if durations else 0.0
            
    def _calculate_profit_factor(self, trades: pd.DataFrame) -> float:
        """Calculate profit factor from trades"""
        if len(trades) == 0:
            return 0
            
        gross_wins = trades[trades['PnL'] > 0]['PnL'].sum()
        gross_losses = abs(trades[trades['PnL'] < 0]['PnL'].sum())
        
        if gross_losses == 0:
            return float('inf') if gross_wins > 0 else 0
            
        return gross_wins / gross_losses
        
    def _aggregate_results(self, results: List[Dict]) -> Dict:
        """Aggregate results from multiple tickers"""
        # Portfolio-level metrics
        total_trades = sum(r['total_trades'] for r in results)
        total_return = np.mean([r['total_return'] for r in results])
        avg_win_rate = np.mean([r['win_rate'] for r in results])
        avg_profit_factor = np.mean([r['profit_factor'] for r in results if r['profit_factor'] != float('inf')])
        max_drawdown = max(r['max_drawdown'] for r in results)
        avg_sharpe = np.mean([r['sharpe_ratio'] for r in results if r['sharpe_ratio'] is not None])
        
        # Individual ticker results
        ticker_results = {r['ticker']: r for r in results}
        
        return {
            'period': f"{self.start_date} to {self.end_date}",
            'initial_capital': self.initial_cash,
            'total_trades': total_trades,
            'avg_return': total_return,
            'avg_win_rate': avg_win_rate,
            'avg_profit_factor': avg_profit_factor,
            'max_drawdown': max_drawdown,
            'avg_sharpe_ratio': avg_sharpe,
            'ticker_results': ticker_results,
            'successful_tickers': len([r for r in results if r['win_rate'] > 0.4]),
            'total_tickers': len(results)
        }