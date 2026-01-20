import sys
import os
import argparse
from tabulate import tabulate
from colorama import init, Fore, Style
import pandas as pd

# Add the current directory to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import config, data, strategy
from src.backtest import BacktestEngine, BacktestReport

def parse_args():
    parser = argparse.ArgumentParser(
        description="Swing Trading Scanner for IDX stocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Live Scanning
  python -m src.main                    # Show only crossover setups from default watchlist
  python -m src.main --list lq45        # Show ALL stocks from LQ45 watchlist
  python -m src.main --list idx_liquid  # Show ALL stocks from liquid IDX watchlist
  python -m src.main BBCA BBRI ANTM     # Show specific tickers
  
  # Backtesting
  python -m src.main --backtest                               # Backtest default watchlist (2022-2024)
  python -m src.main --backtest --list lq45                   # Backtest LQ45 stocks
  python -m src.main --backtest BBCA BBRI ANTM               # Backtest specific tickers
  python -m src.main --backtest --start-date 2022-01-01 --end-date 2023-12-31
  python -m src.main --backtest --detailed --charts           # Full analysis with charts
        """
    )
    parser.add_argument('tickers', nargs='*', help='Specific tickers to scan')
    parser.add_argument('--list', '-l', dest='watchlist', 
                        help='Watchlist name (default, lq45, idx_liquid) - shows ALL stocks from list')
    parser.add_argument('--show-lists', action='store_true',
                        help='Show available watchlists')
    
    # Backtesting arguments
    parser.add_argument('--backtest', action='store_true',
                        help='Run backtesting instead of live scan')
    parser.add_argument('--start-date', dest='start_date',
                        help='Backtest start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', dest='end_date',
                        help='Backtest end date (YYYY-MM-DD)')
    parser.add_argument('--detailed', action='store_true',
                        help='Show detailed backtest report for each ticker')
    parser.add_argument('--charts', action='store_true',
                        help='Generate performance charts')
    
    return parser.parse_args()

def show_available_lists():
    print(f"{Style.BRIGHT}Available Watchlists:{Style.RESET_ALL}")
    for f in os.listdir(config.WATCHLISTS_DIR):
        if f.endswith('.txt'):
            name = f[:-4]
            filepath = os.path.join(config.WATCHLISTS_DIR, f)
            count = len(config.load_watchlist(name))
            print(f"  {name:15} ({count} stocks)")

def run_backtest(args):
    """Run backtesting engine"""
    print(f"{Style.BRIGHT}{Fore.CYAN}Starting Swing Trading Backtesting...{Style.RESET_ALL}")
    
    # Determine tickers to backtest
    if args.tickers:
        tickers_to_test = [t if t.endswith(".JK") else f"{t.upper()}.JK" for t in args.tickers]
        test_mode = "Manual Selection"
    elif args.watchlist:
        tickers_to_test = config.load_watchlist(args.watchlist)
        test_mode = f"Watchlist: {args.watchlist}"
    else:
        tickers_to_test = config.load_watchlist("idx_liquid")  # Default to liquid stocks
        test_mode = "Watchlist: idx_liquid (default)"
    
    print(f"Mode: {test_mode}")
    print(f"Tickers: {len(tickers_to_test)}")
    
    # Initialize backtest engine
    engine = BacktestEngine(
        start_date=args.start_date or config.BACKTEST_START_DATE,
        end_date=args.end_date or config.BACKTEST_END_DATE,
        initial_cash=config.INITIAL_CAPITAL,
        commission=config.COMMISSION_RATE
    )
    
    print(f"Period: {engine.start_date} to {engine.end_date}")
    print(f"Initial Capital: {engine.initial_cash:,} IDR")
    print(f"Commission: {engine.commission*100:.1f}% per trade")
    print(f"Risk per Trade: {config.RISK_PER_TRADE*100:.1f}%")
    print("-" * 60)
    
    # Run backtest
    print("Running backtest...")
    results = engine.run_backtest(tickers_to_test)
    
    if 'error' in results:
        print(f"{Fore.RED}Backtest failed: {results['error']}{Style.RESET_ALL}")
        return
    
    # Generate report
    report_generator = BacktestReport()
    
    if args.detailed:
        # Show detailed reports for each ticker
        for ticker, ticker_result in results.get('ticker_results', {}).items():
            print(report_generator.generate_detailed_ticker_report(ticker, ticker_result))
            print("-" * 60)
    else:
        # Show summary report
        print(report_generator.generate_summary_report(results))
    
    # Generate charts if requested
    if args.charts:
        print(f"\n{Fore.CYAN}Generating performance charts...{Style.RESET_ALL}")
        chart_path = "backtest_performance.png"
        report_generator.create_performance_charts(results, save_path=chart_path)
    
    return results

def main():
    init(autoreset=True)
    args = parse_args()
    
    if args.show_lists:
        show_available_lists()
        return
    
    # Check if backtest mode
    if args.backtest:
        run_backtest(args)
        return
    
    # Original scanning logic
    if args.tickers:
        tickers_to_scan = [t if t.endswith(".JK") else f"{t.upper()}.JK" for t in args.tickers]
        scan_mode = "Manual Selection"
    elif args.watchlist:
        tickers_to_scan = config.load_watchlist(args.watchlist)
        scan_mode = f"Watchlist: {args.watchlist}"
    else:
        tickers_to_scan = config.TICKERS
        scan_mode = f"Watchlist: {config.DEFAULT_WATCHLIST}"
        # Fallback to idx_liquid if default is empty
        if not tickers_to_scan:
            tickers_to_scan = config.load_watchlist("idx_liquid")
            scan_mode = "Watchlist: idx_liquid (fallback)"

    print(f"{Style.BRIGHT}{Fore.CYAN}Starting Swing Trading Scanner (IDX)...{Style.RESET_ALL}")
    print(f"Mode: {scan_mode}")
    print(f"Strategy: EMA{config.FAST_EMA} / EMA{config.SLOW_EMA} Crossover")
    print(f"Target Profit: {config.TARGET_PROFIT_MIN*100:.0f}-{config.TARGET_PROFIT_MAX*100:.0f}% | Stop Loss: Dynamic (ATR {config.ATR_MULTIPLIER}x)")
    
    market_ctx = {"market_regime": "UNKNOWN", "risk_on": True}
    if config.ENABLE_MARKET_FILTER:
        print(f"Fetching market data ({config.MARKET_TICKER})...", end="\r")
        market_df = data.fetch_data(
            config.MARKET_TICKER, 
            period=config.MARKET_HISTORY_PERIOD, 
            interval=config.MARKET_TIMEFRAME
        )
        if market_df is not None:
            market_ctx = strategy.analyze_market_regime(market_df)
        print(" " * 40, end="\r")
    
    print(f"Market Regime: {market_ctx['market_regime']} | MTF: {'ON' if config.ENABLE_MTF else 'OFF'}")
    print("-" * 60)

    results = []
    skipped_mcap = 0

    for ticker in tickers_to_scan:
        print(f"Scanning {ticker}...", end="\r")
        
        # Market cap filter
        if config.ENABLE_MCAP_FILTER:
            stock_info = data.get_stock_info(ticker)
            mcap = stock_info.get('market_cap') if stock_info else None
            if mcap is not None and mcap < config.MIN_MARKET_CAP:
                skipped_mcap += 1
                continue
        else:
            stock_info = None
            mcap = None
        
        df = data.fetch_data(ticker)
        if df is not None:
            analysis = strategy.analyze_ticker(df, market_ctx=market_ctx)
            if analysis:
                # Show all if --list or specific tickers, otherwise only setups
                show_all = args.watchlist or args.tickers
                if analysis['is_setup'] or show_all:
                    weekly_trend = analysis.get('weekly_trend', '-') or '-'
                    final_signal = analysis.get('final_signal', analysis['signal'])
                    
                    inv_strategy = analysis.get('strategy', 'HOLD')
                    support = analysis.get('nearest_support', 0)
                    resistance = analysis.get('nearest_resistance', 0)
                    sr_display = f"{support:.0f}/{resistance:.0f}" if support > 0 else "-"
                    mcap_display = data.format_market_cap(mcap) if mcap else "-"
                    
                    results.append([
                        ticker,
                        final_signal,
                        f"{analysis['ideal_entry']:.0f}",
                        sr_display,
                        f"{analysis['rsi']:.1f}",
                        weekly_trend,
                        mcap_display,
                        inv_strategy
                    ])

    print(" " * 30, end="\r") # Clear the scanning line
    
    if results:
        headers = ["Ticker", "Signal", "Price", "S/R", "RSI", "W.Trend", "MCap", "Strategy"]
        print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
        skip_msg = f" (Skipped {skipped_mcap} small-cap)" if skipped_mcap > 0 else ""
        print(f"\n{Fore.GREEN}Scan Complete. Found {len(results)} setups.{skip_msg}{Style.RESET_ALL}")
    else:
        skip_msg = f" (Skipped {skipped_mcap} small-cap)" if skipped_mcap > 0 else ""
        print(f"\n{Fore.YELLOW}No setups found matching the criteria today.{skip_msg}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
