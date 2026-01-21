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
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ticker = line.upper()
                if not ticker.endswith(".JK"):
                    ticker = f"{ticker}.JK"
                tickers.append(ticker)
    return tickers


# Legacy: Keep TICKERS for backward compatibility
TICKERS = load_watchlist(DEFAULT_WATCHLIST)

# Timeframe for data fetching
TIMEFRAME = "1d"  # Daily candles
HISTORY_PERIOD = "2y"  # Need enough data for weekly EMA50 (55+ weeks)

# Strategy Parameters (optimized for 3-10 day IDX swings)
FAST_EMA = 13  # Faster than 20 for earlier trend capture
SLOW_EMA = 34  # Paired with 13 for reduced lag
RSI_PERIOD = 14
RSI_OVERBOUGHT = 75  # IDX trends stay overbought longer
RSI_OVERSOLD = 35  # More realistic for volatile market

# MACD Parameters
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ATR Parameters (Dynamic SL - wider for IDX volatility)
ATR_PERIOD = 14
ATR_MULTIPLIER = 1.5  # SL = Close - (ATR * 1.5), tighter stops for smaller losses

# Volume Parameters
VOL_AVG_PERIOD = 20
VOLUME_STRICT_FILTER = True  # Requires Volume > Vol_Avg
VOL_RATIO_MIN = 1.2  # Minimum volume ratio for quality signals

# Market Cap Filter (skip small-cap "gorengan")
# NOTE: Disabled by default - fetching info for 100+ tickers causes API issues
# Enable only for small watchlists (< 20 stocks)
ENABLE_MCAP_FILTER = False
MIN_MARKET_CAP = 5e12  # 5 Trillion IDR minimum (expands to quality mid-caps)
# Reference: Large Cap > 50T, Mid Cap 10-50T, Small Cap < 10T

# Market Cap Tiering (optional - for tiered filtering rules)
MARKET_CAP_TIERS = {
    "large_cap": 50e12,  # > 50T IDR (most liquid, blue chips)
    "mid_cap": 10e12,  # 10-50T IDR
    "small_cap": 5e12,  # 5-10T IDR (quality mid-caps, some gorengan)
}
ENABLE_TIERED_FILTER = False  # Set True to apply different rules per tier

# Sector Filters (optional - prefer/avoid specific IDX sectors)
SECTOR_FILTER = {
    "BANKING": {"preferred": True, "min_market_cap": 20e12},
    "INFRASTRUCTURE": {"preferred": True, "min_market_cap": 15e12},
    "CONSUMER": {"preferred": True, "min_market_cap": 10e12},
    "TELECOMMUNICATION": {"preferred": True, "min_market_cap": 15e12},
    "MINING": {"preferred": False, "min_market_cap": 50e12},  # Too volatile
    "CONSTRUCTION": {"preferred": False, "min_market_cap": 30e12},  # Cyclical
}
ENABLE_SECTOR_FILTER = False  # Set True to activate sector filtering

# Volatility Filter (optional - avoid excessively volatile stocks)
ATR_PCT_MAX = 0.05  # Max 5% daily volatility (avoid manipulated/news-driven)
ENABLE_VOLATILITY_FILTER = False  # Set True to activate

# Dividend Yield Filter (optional - prefer dividend-paying stocks)
MIN_DIVIDEND_YIELD = 0.02  # Minimum 2% dividend yield
ENABLE_DIVIDEND_FILTER = False  # Set True to activate

# Risk Management (realistic for weekly swings after fees/spreads)
TARGET_PROFIT_MIN = 0.03  # Minimum 3% profit target
TARGET_PROFIT_MAX = (
    0.10  # Maximum 10% profit target (more realistic for 3-10 day swings)
)
TARGET_PROFIT_PCT = 0.06  # Default 6% target for better R:R
STOP_LOSS_PCT = 0.03  # 3% fallback (tighter stop loss)

# ---- Multi-timeframe (faster for swing horizon) ----
ENABLE_MTF = True
WEEKLY_FAST_EMA = 10  # Faster weekly EMA for 3-10 day trades
WEEKLY_SLOW_EMA = 30  # Paired with 10 for swing alignment
MTF_REQUIRED_FOR_BUY = True  # if True: block daily BUY when weekly not aligned

# ---- Market breadth / regime (smoother, less flip-flops) ----
ENABLE_MARKET_FILTER = True
MARKET_TICKER = "^JKSE"
MARKET_TIMEFRAME = "1d"
MARKET_HISTORY_PERIOD = "2y"  # More history for stable EMA100
MARKET_FAST_EMA = 13
MARKET_SLOW_EMA = 50  # Faster response to market regime changes
MARKET_FILTER_MODE = "TAG"  # Don't hard-block, use scoring instead

# ---- Backtesting Configuration ----
BACKTEST_START_DATE = "2022-01-01"
BACKTEST_END_DATE = "2024-12-31"
INITIAL_CAPITAL = 100000000  # 100M IDR

# Risk Management
RISK_PER_TRADE = 0.01  # 1% risk per trade
MAX_POSITION_EXPOSURE = 0.20  # 20% max exposure per position
MAX_CONCURRENT_POSITIONS = 5  # Max number of open positions
MAX_TOTAL_EXPOSURE = 0.60  # 60% max total portfolio exposure (keeps 40% dry powder)
MAX_VOLUME_PARTICIPATION = 0.05  # Max 5% of daily volume

# Cost Structure
COMMISSION_RATE = 0.0015  # 0.15% commission per trade (typical for IDX brokers)
SLIPPAGE_RATE = 0.002  # 0.2% average slippage

# Rate Limiting for Yahoo Finance API
ENABLE_RATE_LIMITER = True
REQUEST_DELAY_MIN = 2.0  # Minimum delay between requests (seconds)
REQUEST_DELAY_MAX = 4.0  # Maximum delay between requests (seconds)
MAX_RETRIES = 2  # Maximum retry attempts (reduced to fail faster)
RETRY_BACKOFF_BASE = 3  # Exponential backoff multiplier (3^n seconds)
MAX_CONSECUTIVE_429 = 2  # Stop after N consecutive 429 errors
BATCH_SIZE = 5  # Smaller batches to avoid DNS thread exhaustion
BATCH_DELAY = 3.0  # Delay between batch requests (seconds)

# User-Agent rotation for Yahoo Finance requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]
