import yfinance as yf
import pandas as pd
from . import config

def fetch_data(ticker, period=None, interval=None, start_date=None, end_date=None):
    """
    Fetches historical data for a given ticker from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
        period: Data period (e.g., '2y', '1y')
        interval: Data interval (e.g., '1d', '1h')
        start_date: Start date for custom date range (YYYY-MM-DD)
        end_date: End date for custom date range (YYYY-MM-DD)
    """
    try:
        # Use custom date range if provided, otherwise use period
        if start_date and end_date:
            df = yf.download(ticker, start=start_date, end=end_date, 
                           interval=interval or config.TIMEFRAME, progress=False)
        else:
            period = period or config.HISTORY_PERIOD
            interval = interval or config.TIMEFRAME
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            
        if df.empty:
            return None
        
        # Handle MultiIndex columns from yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
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
