import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from .. import config


class Portfolio:
    """
    Portfolio management system for backtesting
    Handles position sizing, risk management, and exposure limits
    """
    
    def __init__(self, initial_cash: float = 100000000):
        """
        Initialize portfolio
        
        Args:
            initial_cash: Starting capital in IDR
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}  # {ticker: position_data}
        self.equity = initial_cash
        self.peak_equity = initial_cash
        self.drawdown = 0
        self.max_drawdown = 0
        
        # Trading statistics
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0
        self.commission_paid = 0
        
        # Position tracking
        self.trade_log = []
        self.equity_curve = []
        
    def calculate_position_size(self, 
                               ticker: str,
                               entry_price: float,
                               stop_loss: float,
                               volatility: float = None) -> float:
        """
        Calculate optimal position size based on risk management rules
        
        Args:
            ticker: Stock ticker
            entry_price: Entry price
            stop_loss: Stop loss price
            volatility: ATR or other volatility measure
            
        Returns:
            Position size in shares
        """
        # Risk per trade (1% of equity by default)
        risk_amount = self.equity * config.RISK_PER_TRADE
        
        # Calculate stop distance
        stop_distance = entry_price - stop_loss
        if stop_distance <= 0:
            return 0
            
        # Base position size from risk
        position_value = risk_amount / stop_distance * entry_price
        
        # Apply maximum exposure limits
        max_position_value = self.equity * config.MAX_POSITION_EXPOSURE
        position_value = min(position_value, max_position_value)
        
        # Apply liquidity constraints (max 5% of daily volume)
        if volatility:
            max_liquidity_value = volatility * config.MAX_VOLUME_PARTICIPATION * entry_price
            position_value = min(position_value, max_liquidity_value)
        
        # Calculate number of shares
        shares = position_value / entry_price
        
        # Round to nearest lot (IDX lot size = 100 shares)
        shares = int(shares / 100) * 100
        
        # Ensure we have enough cash
        required_cash = shares * entry_price * (1 + config.COMMISSION_RATE)
        if required_cash > self.cash:
            shares = int(self.cash / (entry_price * (1 + config.COMMISSION_RATE)) / 100) * 100
            
        return shares
        
    def can_open_position(self, ticker: str, position_value: float) -> bool:
        """
        Check if we can open a new position based on portfolio constraints
        
        Args:
            ticker: Stock ticker
            position_value: Value of proposed position
            
        Returns:
            True if position can be opened
        """
        # Check cash availability
        required_cash = position_value * (1 + config.COMMISSION_RATE)
        if required_cash > self.cash:
            return False
            
        # Check maximum concurrent positions
        if len(self.positions) >= config.MAX_CONCURRENT_POSITIONS:
            return False
            
        # Check if we already have position in this ticker
        if ticker in self.positions:
            return False
            
        # Check total exposure
        total_exposure = sum(pos['value'] for pos in self.positions.values())
        if total_exposure + position_value > self.equity * config.MAX_TOTAL_EXPOSURE:
            return False
            
        return True
        
    def open_position(self, 
                     ticker: str,
                     shares: int,
                     entry_price: float,
                     stop_loss: float,
                     take_profit: float = None,
                     entry_time = None) -> Dict:
        """
        Open a new position
        
        Args:
            ticker: Stock ticker
            shares: Number of shares
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            entry_time: Entry timestamp
            
        Returns:
            Position data dictionary
        """
        position_value = shares * entry_price
        commission = position_value * config.COMMISSION_RATE
        
        # Update cash
        self.cash -= (position_value + commission)
        self.commission_paid += commission
        
        # Create position record
        position = {
            'ticker': ticker,
            'shares': shares,
            'entry_price': entry_price,
            'entry_value': position_value,
            'entry_time': entry_time or datetime.now(),
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'commission': commission,
            'current_price': entry_price,
            'unrealized_pnl': 0,
            'realized_pnl': 0,
            'duration_days': 0
        }
        
        # Add to positions
        self.positions[ticker] = position
        
        # Record trade
        self.total_trades += 1
        self.trade_log.append({
            'action': 'BUY',
            'ticker': ticker,
            'shares': shares,
            'price': entry_price,
            'value': position_value,
            'commission': commission,
            'time': entry_time or datetime.now(),
            'cash_before': self.cash + position_value + commission,
            'cash_after': self.cash
        })
        
        return position
        
    def close_position(self, 
                       ticker: str,
                       exit_price: float,
                       exit_time = None,
                       exit_reason: str = 'MANUAL') -> Optional[Dict]:
        """
        Close an existing position
        
        Args:
            ticker: Stock ticker
            exit_price: Exit price
            exit_time: Exit timestamp
            exit_reason: Reason for exit (SL, TP, SIGNAL, MANUAL)
            
        Returns:
            Closed position data or None if position not found
        """
        if ticker not in self.positions:
            return None
            
        position = self.positions[ticker]
        shares = position['shares']
        entry_value = position['entry_value']
        
        # Calculate exit values
        exit_value = shares * exit_price
        commission = exit_value * config.COMMISSION_RATE
        net_exit_value = exit_value - commission
        
        # Calculate P&L
        gross_pnl = exit_value - entry_value
        net_pnl = gross_pnl - position['commission'] - commission
        pnl_pct = (net_pnl / entry_value) * 100
        
        # Update cash
        self.cash += net_exit_value
        self.commission_paid += commission
        
        # Update statistics
        self.total_pnl += net_pnl
        if net_pnl > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
            
        # Update position record
        position['exit_price'] = exit_price
        position['exit_value'] = exit_value
        position['exit_time'] = exit_time or datetime.now()
        position['exit_reason'] = exit_reason
        position['realized_pnl'] = net_pnl
        position['duration_days'] = (position['exit_time'] - position['entry_time']).days
        
        # Record trade
        self.trade_log.append({
            'action': 'SELL',
            'ticker': ticker,
            'shares': shares,
            'price': exit_price,
            'value': exit_value,
            'commission': commission,
            'pnl': net_pnl,
            'pnl_pct': pnl_pct,
            'reason': exit_reason,
            'time': exit_time or datetime.now(),
            'cash_before': self.cash - net_exit_value,
            'cash_after': self.cash
        })
        
        # Remove from positions
        del self.positions[ticker]
        
        return position
        
    def update_positions(self, current_prices: Dict[str, float], current_time = None):
        """
        Update all positions with current prices and calculate unrealized P&L
        
        Args:
            current_prices: Dictionary of current prices by ticker
            current_time: Current timestamp
        """
        total_unrealized_pnl = 0
        
        for ticker, position in self.positions.items():
            if ticker in current_prices:
                old_price = position['current_price']
                new_price = current_prices[ticker]
                position['current_price'] = new_price
                
                # Calculate unrealized P&L
                unrealized_pnl = (new_price - position['entry_price']) * position['shares']
                position['unrealized_pnl'] = unrealized_pnl
                total_unrealized_pnl += unrealized_pnl
                
                # Check for stop loss or take profit
                if new_price <= position['stop_loss']:
                    self.close_position(ticker, new_price, current_time, 'STOP_LOSS')
                elif position['take_profit'] and new_price >= position['take_profit']:
                    self.close_position(ticker, new_price, current_time, 'TAKE_PROFIT')
        
        # Update equity
        self.equity = self.cash + sum(pos['entry_value'] + pos['unrealized_pnl'] for pos in self.positions.values())
        
        # Update drawdown tracking
        if self.equity > self.peak_equity:
            self.peak_equity = self.equity
            self.drawdown = 0
        else:
            self.drawdown = (self.peak_equity - self.equity) / self.peak_equity * 100
            self.max_drawdown = max(self.max_drawdown, self.drawdown)
            
        # Record equity curve
        self.equity_curve.append({
            'time': current_time or datetime.now(),
            'equity': self.equity,
            'cash': self.cash,
            'positions': len(self.positions),
            'drawdown': self.drawdown
        })
        
    def get_portfolio_summary(self) -> Dict:
        """Get comprehensive portfolio summary"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        avg_win = 0
        avg_loss = 0
        
        # Calculate average win/loss from trade log
        sells = [trade for trade in self.trade_log if trade['action'] == 'SELL']
        if sells:
            wins = [trade['pnl'] for trade in sells if trade['pnl'] > 0]
            losses = [trade['pnl'] for trade in sells if trade['pnl'] < 0]
            avg_win = np.mean(wins) if wins else 0
            avg_loss = np.mean(losses) if losses else 0
        
        profit_factor = abs(avg_win * self.winning_trades / (avg_loss * self.losing_trades)) if avg_loss != 0 and self.losing_trades > 0 else 0
        
        return {
            'initial_cash': self.initial_cash,
            'current_equity': self.equity,
            'total_return': ((self.equity - self.initial_cash) / self.initial_cash) * 100,
            'cash': self.cash,
            'positions_count': len(self.positions),
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'total_pnl': self.total_pnl,
            'commission_paid': self.commission_paid,
            'max_drawdown': self.max_drawdown,
            'current_drawdown': self.drawdown,
            'positions': list(self.positions.values())
        }