import sys
import os
import argparse
from tabulate import tabulate
from colorama import init, Fore, Style
import pandas as pd

# Add the current directory to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import config, data, strategy

def parse_args():
    parser = argparse.ArgumentParser(
        description="Swing Trading Scanner for IDX stocks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                    # Show only crossover setups from default watchlist
  python -m src.main --list lq45        # Show ALL stocks from LQ45 watchlist
  python -m src.main --list idx_liquid  # Show ALL stocks from liquid IDX watchlist
  python -m src.main BBCA BBRI ANTM     # Show specific tickers
        """
    )
    parser.add_argument('tickers', nargs='*', help='Specific tickers to scan')
    parser.add_argument('--list', '-l', dest='watchlist', 
                        help='Watchlist name (default, lq45, idx_liquid) - shows ALL stocks from list')
    parser.add_argument('--show-lists', action='store_true',
                        help='Show available watchlists')
    return parser.parse_args()

def show_available_lists():
    print(f"{Style.BRIGHT}Available Watchlists:{Style.RESET_ALL}")
    for f in os.listdir(config.WATCHLISTS_DIR):
        if f.endswith('.txt'):
            name = f[:-4]
            filepath = os.path.join(config.WATCHLISTS_DIR, f)
            count = len(config.load_watchlist(name))
            print(f"  {name:15} ({count} stocks)")

def main():
    init(autoreset=True)
    args = parse_args()
    
    if args.show_lists:
        show_available_lists()
        return
    
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
