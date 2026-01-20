# Configuration for the Swing Trading Filter
import os

# Watchlist Configuration
# Available lists: default, lq45, idx_liquid (or custom .txt file path)
DEFAULT_WATCHLIST = "default"
WATCHLISTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "watchlists")

def load_watchlist(name_or_path=None):
    """
    Load tickers from a watchlist file.
    Accepts: list name (e.g., 'lq45') or full path to .txt file
    """
    name_or_path = name_or_path or DEFAULT_WATCHLIST
    
    if os.path.isfile(name_or_path):
        filepath = name_or_path
    else:
        filepath = os.path.join(WATCHLISTS_DIR, f"{name_or_path}.txt")
    
    if not os.path.exists(filepath):
        print(f"Warning: Watchlist '{name_or_path}' not found. Using empty list.")
        return []
    
    tickers = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                ticker = line.upper()
                if not ticker.endswith('.JK'):
                    ticker = f"{ticker}.JK"
                tickers.append(ticker)
    return tickers

# Legacy: Keep TICKERS for backward compatibility
TICKERS = load_watchlist(DEFAULT_WATCHLIST)

# Timeframe for data fetching
TIMEFRAME = "1d"  # Daily candles
HISTORY_PERIOD = "2y" # Need enough data for weekly EMA50 (55+ weeks)

# Strategy Parameters (optimized for 3-10 day IDX swings)
FAST_EMA = 13          # Faster than 20 for earlier trend capture
SLOW_EMA = 34          # Paired with 13 for reduced lag
RSI_PERIOD = 14
RSI_OVERBOUGHT = 75    # IDX trends stay overbought longer
RSI_OVERSOLD = 35      # More realistic for volatile market

# MACD Parameters
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ATR Parameters (Dynamic SL - wider for IDX volatility)
ATR_PERIOD = 14
ATR_MULTIPLIER = 2.0   # SL = Close - (ATR * 2.0), wider for gaps/volatility

# Volume Parameters
VOL_AVG_PERIOD = 20
VOLUME_STRICT_FILTER = True    # Requires Volume > Vol_Avg
VOL_RATIO_MIN = 1.2            # Minimum volume ratio for quality signals

# Market Cap Filter (skip small-cap "gorengan")
ENABLE_MCAP_FILTER = True
MIN_MARKET_CAP = 10e12         # 10 Trillion IDR minimum (adjust as needed)
# Reference: Large Cap > 50T, Mid Cap 10-50T, Small Cap < 10T

# Risk Management (realistic for weekly swings after fees/spreads)
TARGET_PROFIT_MIN = 0.03  # Minimum 3% profit target
TARGET_PROFIT_MAX = 0.12  # Maximum 12% profit target
TARGET_PROFIT_PCT = 0.06  # Default 6% target for better R:R
STOP_LOSS_PCT = 0.04      # 4% fallback (breathing room for pullbacks)

# ---- Multi-timeframe (faster for swing horizon) ----
ENABLE_MTF = True
WEEKLY_FAST_EMA = 10   # Faster weekly EMA for 3-10 day trades
WEEKLY_SLOW_EMA = 30   # Paired with 10 for swing alignment
MTF_REQUIRED_FOR_BUY = True   # if True: block daily BUY when weekly not aligned

# ---- Market breadth / regime (smoother, less flip-flops) ----
ENABLE_MARKET_FILTER = True
MARKET_TICKER = "^JKSE"
MARKET_TIMEFRAME = "1d"
MARKET_HISTORY_PERIOD = "2y"   # More history for stable EMA100
MARKET_FAST_EMA = 20
MARKET_SLOW_EMA = 100          # Smoother regime, reduces whipsaws
MARKET_FILTER_MODE = "TAG"     # Don't hard-block, use scoring instead

# ---- Backtesting Configuration ----
BACKTEST_START_DATE = "2022-01-01"
BACKTEST_END_DATE = "2024-12-31"
INITIAL_CAPITAL = 100000000  # 100M IDR

# Risk Management
RISK_PER_TRADE = 0.01        # 1% risk per trade
MAX_POSITION_EXPOSURE = 0.20  # 20% max exposure per position
MAX_CONCURRENT_POSITIONS = 5 # Max number of open positions
MAX_TOTAL_EXPOSURE = 0.80    # 80% max total portfolio exposure
MAX_VOLUME_PARTICIPATION = 0.05  # Max 5% of daily volume

# Cost Structure
COMMISSION_RATE = 0.002      # 0.2% commission per trade
SLIPPAGE_RATE = 0.002        # 0.2% average slippage
