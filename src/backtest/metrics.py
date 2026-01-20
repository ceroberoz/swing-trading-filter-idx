import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class PerformanceMetrics:
    """
    Calculate and analyze performance metrics for backtesting results
    Focus on Win Rate, Profit Factor, and other swing trading specific metrics
    """
    
    def __init__(self):
        self.metrics_cache = {}
        
    def calculate_basic_metrics(self, trades: pd.DataFrame) -> Dict:
        """
        Calculate basic performance metrics
        
        Args:
            trades: DataFrame of trades with PnL, duration, etc.
            
        Returns:
            Dictionary of basic metrics
        """
        if trades.empty:
            return self._empty_metrics()
            
        # Win Rate
        winning_trades = trades[trades['realized_pnl'] > 0]
        losing_trades = trades[trades['realized_pnl'] < 0]
        win_rate = len(winning_trades) / len(trades) * 100
        
        # Profit Factor
        gross_wins = winning_trades['realized_pnl'].sum()
        gross_losses = abs(losing_trades['realized_pnl'].sum())
        profit_factor = gross_wins / gross_losses if gross_losses > 0 else float('inf')
        
        # Average Trade Metrics
        avg_win = winning_trades['realized_pnl'].mean() if not winning_trades.empty else 0
        avg_loss = losing_trades['realized_pnl'].mean() if not losing_trades.empty else 0
        avg_trade = trades['realized_pnl'].mean()
        
        # Trade Duration
        if 'duration_days' in trades.columns:
            avg_duration = trades['duration_days'].mean()
            avg_winning_duration = winning_trades['duration_days'].mean() if not winning_trades.empty else 0
            avg_losing_duration = losing_trades['duration_days'].mean() if not losing_trades.empty else 0
        else:
            avg_duration = avg_winning_duration = avg_losing_duration = 0
        
        # Risk Metrics
        total_pnl = trades['realized_pnl'].sum()
        std_dev = trades['realized_pnl'].std()
        sharpe_ratio = (avg_trade / std_dev) * np.sqrt(252) if std_dev > 0 else 0
        
        return {
            'total_trades': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_trade': avg_trade,
            'total_pnl': total_pnl,
            'avg_duration_days': avg_duration,
            'avg_winning_duration_days': avg_winning_duration,
            'avg_losing_duration_days': avg_losing_duration,
            'sharpe_ratio': sharpe_ratio,
            'std_deviation': std_dev
        }
        
    def calculate_advanced_metrics(self, 
                                 trades: pd.DataFrame,
                                 equity_curve: pd.DataFrame,
                                 initial_capital: float) -> Dict:
        """
        Calculate advanced performance metrics
        
        Args:
            trades: DataFrame of trades
            equity_curve: DataFrame of equity over time
            initial_capital: Starting capital
            
        Returns:
            Dictionary of advanced metrics
        """
        basic_metrics = self.calculate_basic_metrics(trades)
        
        # Drawdown Analysis
        if not equity_curve.empty and 'Equity' in equity_curve.columns:
            drawdown_metrics = self._calculate_drawdown_metrics(equity_curve)
        else:
            drawdown_metrics = {
                'max_drawdown': 0,
                'max_drawdown_duration': 0,
                'avg_drawdown': 0,
                'drawdown_recovery_factor': 0
            }
        
        # Return Metrics
        final_equity = equity_curve['equity'].iloc[-1] if not equity_curve.empty else initial_capital
        total_return = ((final_equity - initial_capital) / initial_capital) * 100
        
        # Monthly Returns
        if not equity_curve.empty:
            monthly_returns = self._calculate_monthly_returns(equity_curve)
        else:
            monthly_returns = {
                'avg_monthly_return': 0,
                'best_month': 0,
                'worst_month': 0,
                'positive_months': 0,
                'total_months': 0
            }
        
        # Trade Distribution Analysis
        trade_distribution = self._analyze_trade_distribution(trades)
        
        # Expectancy
        expectancy = self._calculate_expectancy(trades)
        
        # Risk of Ruin
        risk_of_ruin = self._calculate_risk_of_ruin(trades, initial_capital)
        
        return {
            **basic_metrics,
            **drawdown_metrics,
            'total_return': total_return,
            'final_equity': final_equity,
            **monthly_returns,
            **trade_distribution,
            'expectancy': expectancy,
            'risk_of_ruin': risk_of_ruin
        }
        
    def calculate_swing_trading_metrics(self, trades: pd.DataFrame) -> Dict:
        """
        Calculate swing trading specific metrics
        
        Args:
            trades: DataFrame of trades
            
        Returns:
            Dictionary of swing trading specific metrics
        """
        if trades.empty:
            return {}
            
        # Holding Period Analysis
        if 'Duration' in trades.columns:
            holding_periods = trades['Duration'].describe()
            
            # Target holding period achievement (3-10 days)
            target_trades = trades[(trades['duration_days'] >= 3) & (trades['duration_days'] <= 10)]
            target_achievement = len(target_trades) / len(trades) * 100
            
            # Quick trades (< 3 days) performance
            quick_trades = trades[trades['Duration'] < 3]
            quick_win_rate = (len(quick_trades[quick_trades['PnL'] > 0]) / len(quick_trades) * 100) if not quick_trades.empty else 0
            
            # Long trades (> 10 days) performance
            long_trades = trades[trades['Duration'] > 10]
            long_win_rate = (len(long_trades[long_trades['PnL'] > 0]) / len(long_trades) * 100) if not long_trades.empty else 0
        else:
            holding_periods = {}
            target_achievement = quick_win_rate = long_win_rate = 0
        
            # Weekend Gap Analysis (if we have timestamp data)
            if 'entry_time' in trades.columns and 'exit_time' in trades.columns:
                # Calculate weekend gaps (placeholder for now)
                trades['weekend_gap_days'] = 0  # Would need actual implementation
        weekend_gap_analysis = self._analyze_weekend_gaps(trades)
        
        # Volume and Liquidity Analysis
        volume_analysis = self._analyze_volume_patterns(trades)
        
        return {
            'holding_period_stats': holding_periods,
            'target_holding_achievement': target_achievement,
            'quick_trades_win_rate': quick_win_rate,
            'long_trades_win_rate': long_win_rate,
            **weekend_gap_analysis,
            **volume_analysis
        }
        
    def _calculate_drawdown_metrics(self, equity_curve: pd.DataFrame) -> Dict:
        """Calculate drawdown related metrics"""
        equity = equity_curve['Equity']
        peak = equity.expanding().max()
        drawdown = ((peak - equity) / peak) * 100
        
        max_drawdown = drawdown.max()
        
        # Calculate drawdown durations
        in_drawdown = drawdown > 0
        drawdown_periods = in_drawdown.astype(int).groupby((~in_drawdown).cumsum()).cumsum()
        max_drawdown_duration = drawdown_periods.max()
        
        # Average drawdown
        avg_drawdown = drawdown[in_drawdown].mean() if in_drawdown.any() else 0
        
        # Recovery factor
        recovery_factor = equity_curve['Equity'].iloc[-1] / max_drawdown if max_drawdown > 0 else 0
        
        return {
            'max_drawdown': max_drawdown,
            'max_drawdown_duration': max_drawdown_duration,
            'avg_drawdown': avg_drawdown,
            'drawdown_recovery_factor': recovery_factor
        }
        
    def _calculate_monthly_returns(self, equity_curve: pd.DataFrame) -> Dict:
        """Calculate monthly return statistics"""
        if equity_curve.empty:
            return {'avg_monthly_return': 0, 'best_month': 0, 'worst_month': 0}
        
        monthly_returns = equity_curve['equity'].resample('M').last().pct_change().dropna()
        
        return {
            'avg_monthly_return': monthly_returns.mean() * 100,
            'best_month': monthly_returns.max() * 100,
            'worst_month': monthly_returns.min() * 100
        }
        
    def _analyze_trade_distribution(self, trades: pd.DataFrame) -> Dict:
        """Analyze trade P&L distribution"""
        if trades.empty:
            return {}
            
        pnl = trades['realized_pnl']
        
        # Percentiles
        percentiles = {
            'p10': pnl.quantile(0.1),
            'p25': pnl.quantile(0.25),
            'p50': pnl.quantile(0.5),
            'p75': pnl.quantile(0.75),
            'p90': pnl.quantile(0.9)
        }
        
        # Outlier analysis
        q1 = pnl.quantile(0.25)
        q3 = pnl.quantile(0.75)
        iqr = q3 - q1
        outliers = pnl[(pnl < (q1 - 1.5 * iqr)) | (pnl > (q3 + 1.5 * iqr))]
        
        return {
            'pnl_percentiles': percentiles,
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(trades) * 100,
            'largest_win': pnl.max(),
            'largest_loss': pnl.min(),
            'skewness': pnl.skew(),
            'kurtosis': pnl.kurtosis()
        }
        
    def _calculate_expectancy(self, trades: pd.DataFrame) -> float:
        """Calculate expectancy per trade"""
        if trades.empty:
            return 0
            
        winning_trades = trades[trades['PnL'] > 0]
        losing_trades = trades[trades['PnL'] < 0]
        
        if len(winning_trades) == 0 or len(losing_trades) == 0:
            return 0
            
        avg_win = winning_trades['realized_pnl'].mean()
        avg_loss = abs(losing_trades['realized_pnl'].mean())
        win_rate = len(winning_trades) / len(trades)
        
        expectancy = (avg_win * win_rate) - (avg_loss * (1 - win_rate))
        return expectancy
        
    def _calculate_risk_of_ruin(self, trades: pd.DataFrame, initial_capital: float) -> float:
        """Calculate risk of ruin probability"""
        if trades.empty or len(trades) < 10:
            return 0
            
        # Simple risk of ruin calculation
        winning_trades = trades[trades['PnL'] > 0]
        losing_trades = trades[trades['PnL'] < 0]
        
        if len(losing_trades) == 0:
            return 0
            
        win_rate = len(winning_trades) / len(trades)
        avg_loss = abs(losing_trades['PnL'].mean())
        
        # Risk of losing 50% of capital
        max_acceptable_loss = initial_capital * 0.5
        trades_to_ruin = max_acceptable_loss / avg_loss
        
        # Probability formula
        if win_rate <= 0.5:
            risk_of_ruin = ((1 - win_rate) / win_rate) ** trades_to_ruin
        else:
            risk_of_ruin = 0
            
        return min(risk_of_ruin, 1.0)  # Cap at 100%
        
    def _analyze_weekend_gaps(self, trades: pd.DataFrame) -> Dict:
        """Analyze weekend gap effects (placeholder for now)"""
        # This would require intraday data or more detailed timestamps
        return {
            'weekend_gap_analysis': 'Requires intraday data',
            'avg_weekend_gap': 0,
            'gap_win_rate_impact': 0
        }
        
    def _analyze_volume_patterns(self, trades: pd.DataFrame) -> Dict:
        """Analyze volume patterns in trades (placeholder for now)"""
        # This would require volume data in trades
        return {
            'volume_analysis': 'Requires volume data in trades',
            'avg_entry_volume_ratio': 0,
            'volume_success_correlation': 0
        }
        
    def _empty_metrics(self) -> Dict:
        """Return empty metrics dictionary"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'profit_factor': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'avg_trade': 0,
            'total_pnl': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
            'total_return': 0
        }