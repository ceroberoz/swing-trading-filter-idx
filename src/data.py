import yfinance as yf
import pandas as pd
from . import config

def fetch_data(ticker, period=None, interval=None):
    """
    Fetches historical data for a given ticker from Yahoo Finance.
    """
    try:
        period = period or config.HISTORY_PERIOD
        interval = interval or config.TIMEFRAME
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_latest_price(df):
    """
    Returns the latest close price.
    """
    if df is not None and not df.empty:
        return df['Close'].iloc[-1]
    return None

def get_stock_info(ticker):
    """
    Fetch stock fundamental info (market cap, sector, etc.) from Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'market_cap': info.get('marketCap'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'pe_ratio': info.get('trailingPE'),
            'pbv': info.get('priceToBook'),
            'dividend_yield': info.get('dividendYield'),
        }
    except Exception as e:
        return None

def format_market_cap(mcap):
    """
    Format market cap to human readable (e.g., 10.5T, 500B)
    """
    if mcap is None:
        return "-"
    if mcap >= 1e12:
        return f"{mcap/1e12:.1f}T"
    elif mcap >= 1e9:
        return f"{mcap/1e9:.0f}B"
    else:
        return f"{mcap/1e6:.0f}M"
