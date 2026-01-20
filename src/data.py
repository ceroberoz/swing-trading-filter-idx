import time
import warnings

import pandas as pd
import yfinance as yf

from . import config
from .rate_limiter import get_rate_limiter, retry_with_backoff

warnings.filterwarnings("ignore", category=FutureWarning, module="yfinance")

# Use local cache directory to avoid SQLite corruption issues
yf.set_tz_cache_location("./cache")

rate_limiter = get_rate_limiter()


@retry_with_backoff()
def fetch_data(ticker, period=None, interval=None, start_date=None, end_date=None):
    """
    Fetch historical OHLCV data for a single ticker.

    Args:
        ticker: Stock ticker symbol (e.g., 'BBCA.JK')
        period: Time period (e.g., '1mo', '1y', '2y')
        interval: Data interval (e.g., '1d', '1wk')
        start_date: Start date for historical data (YYYY-MM-DD)
        end_date: End date for historical data (YYYY-MM-DD)

    Returns:
        DataFrame with OHLCV data or None if failed
    """
    rate_limiter.wait()

    try:
        if start_date and end_date:
            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=interval or config.TIMEFRAME,
                progress=False,
                auto_adjust=True,
            )
        else:
            period = period or config.HISTORY_PERIOD
            interval = interval or config.TIMEFRAME
            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True,
            )

        if df.empty:
            return None

        # Handle multi-index columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        raise


def fetch_data_batch(
    tickers, period=None, interval=None, start_date=None, end_date=None
):
    """
    Fetch historical data for multiple tickers with proper rate limiting.
    Uses chunking to avoid overwhelming Yahoo Finance API.

    Args:
        tickers: List of stock ticker symbols
        period: Time period (e.g., '1mo', '1y', '2y')
        interval: Data interval (e.g., '1d', '1wk')
        start_date: Start date for historical data (YYYY-MM-DD)
        end_date: End date for historical data (YYYY-MM-DD)

    Returns:
        Dictionary mapping ticker -> DataFrame with OHLCV data
    """
    if not tickers:
        return {}

    results = {}
    batch_size = config.BATCH_SIZE
    total_batches = (len(tickers) + batch_size - 1) // batch_size

    print(f"Fetching data for {len(tickers)} tickers in {total_batches} batches...")

    # Process tickers in chunks
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i : i + batch_size]
        batch_num = (i // batch_size) + 1

        print(
            f"Batch {batch_num}/{total_batches}: Fetching {len(batch)} tickers...",
            end="\r",
        )

        try:
            # Fetch batch with rate limiting
            batch_result = _fetch_batch_chunk(
                batch, period, interval, start_date, end_date
            )
            results.update(batch_result)

            # Extra delay between batches (except for last batch)
            if i + batch_size < len(tickers):
                time.sleep(config.BATCH_DELAY)

        except Exception as e:
            print(f"\nError fetching batch {batch_num}: {e}")
            # Fall back to individual fetching for this batch
            print(f"Falling back to individual fetching for batch {batch_num}...")
            for ticker in batch:
                try:
                    df = fetch_data(ticker, period, interval, start_date, end_date)
                    if df is not None and not df.empty:
                        results[ticker] = df
                except Exception as ticker_error:
                    print(f"Failed to fetch {ticker}: {ticker_error}")
                    continue

    print(f"\nSuccessfully fetched {len(results)}/{len(tickers)} tickers")
    return results


@retry_with_backoff()
def _fetch_batch_chunk(
    tickers, period=None, interval=None, start_date=None, end_date=None
):
    """
    Internal function to fetch a chunk of tickers.

    Args:
        tickers: List of tickers (should be <= BATCH_SIZE)
        period: Time period
        interval: Data interval
        start_date: Start date
        end_date: End date

    Returns:
        Dictionary mapping ticker -> DataFrame
    """
    rate_limiter.wait()

    try:
        # Download data for multiple tickers at once
        if start_date and end_date:
            df = yf.download(
                tickers,
                start=start_date,
                end=end_date,
                interval=interval or config.TIMEFRAME,
                progress=False,
                auto_adjust=True,
                group_by="ticker",
            )
        else:
            period = period or config.HISTORY_PERIOD
            interval = interval or config.TIMEFRAME
            df = yf.download(
                tickers,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True,
                group_by="ticker",
            )

        if df.empty:
            return {}

        # Parse multi-ticker results
        results = {}

        if len(tickers) == 1:
            # Single ticker - no multi-index
            ticker = tickers[0]
            if not df.empty:
                results[ticker] = df
        else:
            # Multiple tickers - split by ticker
            for ticker in tickers:
                try:
                    ticker_df = (
                        df[ticker]
                        if ticker in df.columns.get_level_values(0)
                        else pd.DataFrame()
                    )
                    if not ticker_df.empty:
                        # Drop NaN rows
                        ticker_df = ticker_df.dropna(subset=["Close"])
                        if not ticker_df.empty:
                            results[ticker] = ticker_df
                except (KeyError, AttributeError):
                    # Ticker not found in results
                    continue

        return results

    except Exception as e:
        print(f"Error in batch fetch: {e}")
        raise


@retry_with_backoff()
def get_stock_info(ticker):
    """
    Fetch fundamental info for a single ticker.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with stock info or None if failed
    """
    rate_limiter.wait()

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "pe_ratio": info.get("trailingPE"),
            "pbv": info.get("priceToBook"),
            "dividend_yield": info.get("dividendYield"),
        }
    except Exception as e:
        print(f"Error fetching info for {ticker}: {e}")
        raise


def fetch_stock_info_batch(tickers):
    """
    Fetch stock info for multiple tickers with proper rate limiting.
    Fetches each ticker individually with delays to avoid rate limits.

    Args:
        tickers: List of stock ticker symbols

    Returns:
        Dictionary mapping ticker -> stock info dict
    """
    if not tickers:
        return {}

    results = {}
    total = len(tickers)

    print(f"Fetching stock info for {total} tickers...")

    for idx, ticker in enumerate(tickers, 1):
        print(f"Fetching info {idx}/{total}: {ticker}...", end="\r")

        try:
            info = get_stock_info(ticker)
            results[ticker] = info
        except Exception as e:
            print(f"\nFailed to fetch info for {ticker}: {e}")
            results[ticker] = None
            continue

    print(
        f"\nSuccessfully fetched info for {len([r for r in results.values() if r])}/{total} tickers"
    )
    return results


def get_latest_price(df):
    """
    Returns the latest close price from a DataFrame.

    Args:
        df: DataFrame with OHLCV data

    Returns:
        Latest close price or None
    """
    if df is not None and not df.empty:
        return df["Close"].iloc[-1]
    return None


def format_market_cap(mcap):
    """
    Format market cap to human readable format.

    Args:
        mcap: Market cap value in IDR

    Returns:
        Formatted string (e.g., '10.5T', '500B', '50M')
    """
    if mcap is None:
        return "-"
    if mcap >= 1e12:
        return f"{mcap / 1e12:.1f}T"
    elif mcap >= 1e9:
        return f"{mcap / 1e9:.0f}B"
    else:
        return f"{mcap / 1e6:.0f}M"
