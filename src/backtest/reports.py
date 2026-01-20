import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from colorama import Fore, Style

from .metrics import PerformanceMetrics


class BacktestReport:
    """
    Generate comprehensive backtesting reports with visualizations
    """
    
    def __init__(self, metrics_calculator: PerformanceMetrics = None):
        """
        Initialize report generator
        
        Args:
            metrics_calculator: PerformanceMetrics instance
        """
        self.metrics = metrics_calculator or PerformanceMetrics()
        
    def generate_summary_report(self, backtest_results: Dict) -> str:
        """
        Generate comprehensive summary report
        
        Args:
            backtest_results: Results from BacktestEngine
            
        Returns:
            Formatted report string
        """
        if 'error' in backtest_results:
            return f"{Fore.RED}Error: {backtest_results['error']}{Style.RESET_ALL}"
            
        # Extract key metrics
        period = backtest_results.get('period', 'Unknown')
        initial_capital = backtest_results.get('initial_capital', 0)
        total_trades = backtest_results.get('total_trades', 0)
        avg_return = backtest_results.get('avg_return', 0)
        avg_win_rate = backtest_results.get('avg_win_rate', 0)
        avg_profit_factor = backtest_results.get('avg_profit_factor', 0)
        max_drawdown = backtest_results.get('max_drawdown', 0)
        avg_sharpe = backtest_results.get('avg_sharpe_ratio', 0)
        successful_tickers = backtest_results.get('successful_tickers', 0)
        total_tickers = backtest_results.get('total_tickers', 0)
        
        # Format report
        report = f"""
{Style.BRIGHT}{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                    SWING TRADING BACKTEST REPORT                          ║
╚════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Style.BRIGHT}Test Period:{Style.RESET_ALL}        {period}
{Style.BRIGHT}Initial Capital:{Style.RESET_ALL}    {self._format_currency(initial_capital)}
{Style.BRIGHT}Total Tickers:{Style.RESET_ALL}       {total_tickers} ({successful_tickers} profitable)

{Style.BRIGHT}{Fore.GREEN}PERFORMANCE METRICS:{Style.RESET_ALL}
├─ Total Trades:           {total_trades}
├─ Average Return:          {avg_return:.2f}%
├─ Win Rate:                {avg_win_rate:.1f}%
├─ Profit Factor:           {avg_profit_factor:.2f}
├─ Max Drawdown:            {max_drawdown:.2f}%
└─ Sharpe Ratio:            {avg_sharpe:.2f}

{Style.BRIGHT}{Fore.YELLOW}STRATEGY ASSESSMENT:{Style.RESET_ALL}
"""
        
        # Strategy assessment
        assessment = self._assess_strategy_performance(avg_win_rate, avg_profit_factor, max_drawdown)
        report += f"├─ Overall Rating:          {assessment['rating']}\n"
        report += f"├─ Strengths:               {', '.join(assessment['strengths'])}\n"
        report += f"└─ Areas for Improvement:    {', '.join(assessment['weaknesses'])}\n"
        
        # Individual ticker results
        ticker_results = backtest_results.get('ticker_results', {})
        if ticker_results:
            report += f"\n{Style.BRIGHT}{Fore.BLUE}TOP PERFORMERS:{Style.RESET_ALL}\n"
            top_performers = sorted(ticker_results.items(), 
                                  key=lambda x: x[1].get('win_rate', 0), 
                                  reverse=True)[:5]
            
            for ticker, result in top_performers:
                win_rate = result.get('win_rate', 0)
                profit_factor = result.get('profit_factor', 0)
                trades = result.get('total_trades', 0)
                report += f"├─ {ticker:<10} Win Rate: {win_rate:.1f}%, PF: {profit_factor:.2f}, Trades: {trades}\n"
        
        report += f"\n{Style.BRIGHT}{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════════╗\n"
        report += f"║                           END OF REPORT                                 ║\n"
        report += f"╚════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n"
        
        return report
        
    def generate_detailed_ticker_report(self, ticker: str, ticker_result: Dict) -> str:
        """
        Generate detailed report for a single ticker
        
        Args:
            ticker: Stock ticker
            ticker_result: Individual ticker backtest result
            
        Returns:
            Formatted detailed report
        """
        stats = ticker_result.get('stats', {})
        trades = ticker_result.get('trades', pd.DataFrame())
        
        if trades.empty:
            return f"{Fore.RED}No trades found for {ticker}{Style.RESET_ALL}"
            
        # Calculate detailed metrics
        detailed_metrics = self.metrics.calculate_advanced_metrics(trades, 
                                                                   ticker_result.get('equity_curve', pd.DataFrame()),
                                                                   ticker_result.get('final_equity', 0))
        
        swing_metrics = self.metrics.calculate_swing_trading_metrics(trades)
        
        report = f"""
{Style.BRIGHT}{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                    DETAILED ANALYSIS: {ticker:<10}                          ║
╚════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Style.BRIGHT}TRADE STATISTICS:{Style.RESET_ALL}
├─ Total Trades:           {detailed_metrics.get('total_trades', 0)}
├─ Winning Trades:         {detailed_metrics.get('winning_trades', 0)}
├─ Losing Trades:           {detailed_metrics.get('losing_trades', 0)}
├─ Win Rate:                {detailed_metrics.get('win_rate', 0):.1f}%
├─ Profit Factor:           {detailed_metrics.get('profit_factor', 0):.2f}
├─ Average Win:             {self._format_currency(detailed_metrics.get('avg_win', 0))}
├─ Average Loss:            {self._format_currency(detailed_metrics.get('avg_loss', 0))}
└─ Expectancy:              {self._format_currency(detailed_metrics.get('expectancy', 0))}

{Style.BRIGHT}RISK METRICS:{Style.RESET_ALL}
├─ Total Return:            {detailed_metrics.get('total_return', 0):.2f}%
├─ Max Drawdown:            {detailed_metrics.get('max_drawdown', 0):.2f}%
├─ Sharpe Ratio:            {detailed_metrics.get('sharpe_ratio', 0):.2f}
└─ Risk of Ruin:            {detailed_metrics.get('risk_of_ruin', 0):.2f}%

{Style.BRIGHT}SWING TRADING METRICS:{Style.RESET_ALL}
"""
        
        if swing_metrics:
            holding_stats = swing_metrics.get('holding_period_stats', {})
            report += f"├─ Avg Holding Period:      {holding_stats.get('mean', 0):.1f} days\n"
            report += f"├─ Target Achievement:      {swing_metrics.get('target_holding_achievement', 0):.1f}%\n"
            report += f"├─ Quick Trades Win Rate:  {swing_metrics.get('quick_trades_win_rate', 0):.1f}%\n"
            report += f"└─ Long Trades Win Rate:   {swing_metrics.get('long_trades_win_rate', 0):.1f}%\n"
        
        # Recent trades
        if not trades.empty:
            report += f"\n{Style.BRIGHT}{Fore.YELLOW}RECENT TRADES (Last 10):{Style.RESET_ALL}\n"
            recent_trades = trades.tail(10)[['EntryTime', 'ExitTime', 'EntryPrice', 'ExitPrice', 'PnL', 'PnL%']]
            report += self._format_trades_table(recent_trades)
        
        return report
        
    def generate_trade_log(self, trades: pd.DataFrame) -> str:
        """
        Generate detailed trade log
        
        Args:
            trades: DataFrame of trades
            
        Returns:
            Formatted trade log
        """
        if trades.empty:
            return f"{Fore.YELLOW}No trades to display{Style.RESET_ALL}"
            
        # Format trades for display
        display_trades = trades.copy()
        display_trades['EntryTime'] = pd.to_datetime(display_trades['EntryTime']).dt.strftime('%Y-%m-%d')
        display_trades['ExitTime'] = pd.to_datetime(display_trades['ExitTime']).dt.strftime('%Y-%m-%d')
        display_trades['PnL'] = display_trades['PnL'].apply(lambda x: f"{Fore.GREEN if x > 0 else Fore.RED}{self._format_currency(x)}{Style.RESET_ALL}")
        display_trades['PnL%'] = display_trades['PnL%'].apply(lambda x: f"{Fore.GREEN if x > 0 else Fore.RED}{x:.2f}%{Style.RESET_ALL}")
        
        headers = ['Entry', 'Exit', 'Entry Price', 'Exit Price', 'P&L', 'P&L%']
        table_data = display_trades[['EntryTime', 'ExitTime', 'EntryPrice', 'ExitPrice', 'PnL', 'PnL%']].values.tolist()
        
        return tabulate(table_data, headers=headers, tablefmt="fancy_grid")
        
    def create_performance_charts(self, backtest_results: Dict, save_path: str = None):
        """
        Create performance visualization charts
        
        Args:
            backtest_results: Results from BacktestEngine
            save_path: Path to save charts (optional)
        """
        try:
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Swing Trading Strategy Performance Analysis', fontsize=16, fontweight='bold')
            
            # Chart 1: Win Rate Distribution
            ticker_results = backtest_results.get('ticker_results', {})
            if ticker_results:
                win_rates = [result.get('win_rate', 0) for result in ticker_results.values()]
                axes[0, 0].hist(win_rates, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                axes[0, 0].axvline(np.mean(win_rates), color='red', linestyle='--', label=f'Mean: {np.mean(win_rates):.1f}%')
                axes[0, 0].set_title('Win Rate Distribution Across Tickers')
                axes[0, 0].set_xlabel('Win Rate (%)')
                axes[0, 0].set_ylabel('Number of Tickers')
                axes[0, 0].legend()
                axes[0, 0].grid(True, alpha=0.3)
            
            # Chart 2: Profit Factor vs Win Rate Scatter
            if ticker_results:
                win_rates = []
                profit_factors = []
                tickers = []
                
                for ticker, result in ticker_results.items():
                    wr = result.get('win_rate', 0)
                    pf = result.get('profit_factor', 0)
                    if pf != float('inf') and pf < 10:  # Filter extreme values
                        win_rates.append(wr)
                        profit_factors.append(pf)
                        tickers.append(ticker)
                
                scatter = axes[0, 1].scatter(win_rates, profit_factors, alpha=0.6, s=50)
                axes[0, 1].set_title('Profit Factor vs Win Rate')
                axes[0, 1].set_xlabel('Win Rate (%)')
                axes[0, 1].set_ylabel('Profit Factor')
                axes[0, 1].grid(True, alpha=0.3)
                
                # Add trend line
                if len(win_rates) > 1:
                    z = np.polyfit(win_rates, profit_factors, 1)
                    p = np.poly1d(z)
                    axes[0, 1].plot(win_rates, p(win_rates), "r--", alpha=0.8)
            
            # Chart 3: Trade Count Distribution
            if ticker_results:
                trade_counts = [result.get('total_trades', 0) for result in ticker_results.values()]
                axes[1, 0].hist(trade_counts, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
                axes[1, 0].axvline(np.mean(trade_counts), color='red', linestyle='--', label=f'Mean: {np.mean(trade_counts):.1f}')
                axes[1, 0].set_title('Number of Trades per Ticker')
                axes[1, 0].set_xlabel('Number of Trades')
                axes[1, 0].set_ylabel('Number of Tickers')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
            
            # Chart 4: Performance Summary Table
            axes[1, 1].axis('off')
            
            # Create summary text
            summary_text = f"""
PERFORMANCE SUMMARY:
═══════════════════════════════════
Total Tickers:    {backtest_results.get('total_tickers', 0)}
Successful:       {backtest_results.get('successful_tickers', 0)}
Avg Win Rate:     {backtest_results.get('avg_win_rate', 0):.1f}%
Avg Profit Factor: {backtest_results.get('avg_profit_factor', 0):.2f}
Max Drawdown:     {backtest_results.get('max_drawdown', 0):.2f}%
Avg Sharpe Ratio: {backtest_results.get('avg_sharpe_ratio', 0):.2f}

STRATEGY ASSESSMENT:
═══════════════════════════════════
"""
            
            assessment = self._assess_strategy_performance(
                backtest_results.get('avg_win_rate', 0),
                backtest_results.get('avg_profit_factor', 0),
                backtest_results.get('max_drawdown', 0)
            )
            
            summary_text += f"Rating: {assessment['rating']}\n"
            summary_text += f"Strengths: {', '.join(assessment['strengths'])}\n"
            summary_text += f"Weaknesses: {', '.join(assessment['weaknesses'])}"
            
            axes[1, 1].text(0.1, 0.9, summary_text, transform=axes[1, 1].transAxes,
                          fontsize=11, verticalalignment='top', fontfamily='monospace')
            
            plt.tight_layout()
            
            # Save or show
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Charts saved to {save_path}")
            else:
                plt.show()
                
        except Exception as e:
            print(f"Error creating charts: {e}")
            
    def _assess_strategy_performance(self, win_rate: float, profit_factor: float, max_drawdown: float) -> Dict:
        """Assess overall strategy performance"""
        rating = "UNKNOWN"
        strengths = []
        weaknesses = []
        
        # Win Rate Assessment
        if win_rate >= 55:
            strengths.append("High Win Rate")
            rating_points = 3
        elif win_rate >= 45:
            strengths.append("Good Win Rate")
            rating_points = 2
        elif win_rate >= 35:
            weaknesses.append("Moderate Win Rate")
            rating_points = 1
        else:
            weaknesses.append("Low Win Rate")
            rating_points = 0
        
        # Profit Factor Assessment
        if profit_factor >= 2.0:
            strengths.append("Excellent Profit Factor")
            rating_points += 3
        elif profit_factor >= 1.5:
            strengths.append("Good Profit Factor")
            rating_points += 2
        elif profit_factor >= 1.2:
            weaknesses.append("Moderate Profit Factor")
            rating_points += 1
        else:
            weaknesses.append("Poor Profit Factor")
            rating_points += 0
        
        # Drawdown Assessment
        if max_drawdown <= 10:
            strengths.append("Low Drawdown")
            rating_points += 2
        elif max_drawdown <= 20:
            weaknesses.append("Moderate Drawdown")
            rating_points += 1
        else:
            weaknesses.append("High Drawdown")
            rating_points += 0
        
        # Overall Rating
        total_points = rating_points
        if total_points >= 7:
            rating = "EXCELLENT"
        elif total_points >= 5:
            rating = "GOOD"
        elif total_points >= 3:
            rating = "FAIR"
        else:
            rating = "POOR"
        
        return {
            'rating': rating,
            'strengths': strengths if strengths else ["None identified"],
            'weaknesses': weaknesses if weaknesses else ["None identified"]
        }
        
    def _format_currency(self, amount: float) -> str:
        """Format currency amount"""
        if abs(amount) >= 1e9:
            return f"{amount/1e9:.1f}B IDR"
        elif abs(amount) >= 1e6:
            return f"{amount/1e6:.1f}M IDR"
        elif abs(amount) >= 1e3:
            return f"{amount/1e3:.0f}K IDR"
        else:
            return f"{amount:.0f} IDR"
            
    def _format_trades_table(self, trades: pd.DataFrame) -> str:
        """Format trades table for display"""
        if trades.empty:
            return "No trades to display"
            
        # Convert to list of lists for tabulate
        table_data = []
        for _, trade in trades.iterrows():
            row = [
                trade.get('EntryTime', ''),
                trade.get('ExitTime', ''),
                f"{trade.get('EntryPrice', 0):.0f}",
                f"{trade.get('ExitPrice', 0):.0f}",
                f"{Fore.GREEN if trade.get('PnL', 0) > 0 else Fore.RED}{self._format_currency(trade.get('PnL', 0))}{Style.RESET_ALL}",
                f"{Fore.GREEN if trade.get('PnL%', 0) > 0 else Fore.RED}{trade.get('PnL%', 0):.2f}%{Style.RESET_ALL}"
            ]
            table_data.append(row)
        
        headers = ['Entry', 'Exit', 'Entry Price', 'Exit Price', 'P&L', 'P&L%']
        return tabulate(table_data, headers=headers, tablefmt="fancy_grid")