import numpy as np
import pandas as pd

def _is_doji(row, threshold=0.1):
    """
    Detect Doji: Body is very small relative to the total range.
    Indecision candle.
    """
    body = abs(row["Close"] - row["Open"])
    rng = row["High"] - row["Low"]
    # Avoid division by zero if range is 0 (flat line)
    return rng > 0 and body <= (rng * threshold)

def _is_hammer(row, body_factor=0.3, wick_factor=2.0):
    """
    Detect Hammer: Small body, long lower wick, small/no upper wick.
    Bullish reversal signal (usually found at bottom of downtrend).
    """
    body = abs(row["Close"] - row["Open"])
    rng = row["High"] - row["Low"]
    lower_wick = min(row["Close"], row["Open"]) - row["Low"]
    upper_wick = row["High"] - max(row["Close"], row["Open"])
    
    if rng == 0:
        return False
        
    return (
        body <= (rng * body_factor) and
        lower_wick >= (body * wick_factor) and
        upper_wick <= body  # Upper wick should be small (length <= body is a reasonable heuristic)
    )

def _is_shooting_star(row, body_factor=0.3, wick_factor=2.0):
    """
    Detect Shooting Star: Small body, long upper wick, small/no lower wick.
    Bearish reversal signal (usually found at top of uptrend).
    """
    body = abs(row["Close"] - row["Open"])
    rng = row["High"] - row["Low"]
    lower_wick = min(row["Close"], row["Open"]) - row["Low"]
    upper_wick = row["High"] - max(row["Close"], row["Open"])
    
    if rng == 0:
        return False
        
    return (
        body <= (rng * body_factor) and
        upper_wick >= (body * wick_factor) and
        lower_wick <= body  # Lower wick should be small
    )

def _is_bullish_engulfing(curr, prev):
    """
    Detect Bullish Engulfing: 
    - Previous candle is RED (Close < Open)
    - Current candle is GREEN (Close > Open)
    - Current body engulfs previous body
    """
    # Check colors
    prev_is_red = prev["Close"] < prev["Open"]
    curr_is_green = curr["Close"] > curr["Open"]
    
    if not (prev_is_red and curr_is_green):
        return False
        
    # Check engulfing (Current Body covers Previous Body)
    # Since Prev is Red: Top is Open, Bottom is Close
    # Since Curr is Green: Top is Close, Bottom is Open
    return (
        curr["Open"] <= prev["Close"] and 
        curr["Close"] >= prev["Open"]
    )

def _is_bearish_engulfing(curr, prev):
    """
    Detect Bearish Engulfing:
    - Previous candle is GREEN (Close > Open)
    - Current candle is RED (Close < Open)
    - Current body engulfs previous body
    """
    # Check colors
    prev_is_green = prev["Close"] > prev["Open"]
    curr_is_red = curr["Close"] < curr["Open"]
    
    if not (prev_is_green and curr_is_red):
        return False
        
    # Check engulfing (Current Body covers Previous Body)
    # Since Prev is Green: Top is Close, Bottom is Open
    # Since Curr is Red: Top is Open, Bottom is Close
    return (
        curr["Open"] >= prev["Close"] and
        curr["Close"] <= prev["Open"]
    )

def detect_patterns(df):
    """
    Detect candlestick patterns for the latest candle in the DataFrame.
    
    Args:
        df: DataFrame with Open, High, Low, Close
        
    Returns:
        Dictionary with boolean flags and list of pattern names for the last row.
        Example: {'is_doji': True, 'patterns': ['Doji']}
    """
    if df is None or len(df) < 2:
        return {
            "patterns": [],
            "is_doji": False,
            "is_hammer": False,
            "is_shooting_star": False,
            "is_bullish_engulfing": False,
            "is_bearish_engulfing": False
        }
        
    # Get last two rows
    curr = df.iloc[-1]
    prev = df.iloc[-2]
    
    patterns = []
    
    # 1. Doji
    is_doji = _is_doji(curr)
    if is_doji:
        patterns.append("Doji")
        
    # 2. Hammer
    is_hammer = _is_hammer(curr)
    if is_hammer:
        patterns.append("Hammer")
        
    # 3. Shooting Star
    is_shooting_star = _is_shooting_star(curr)
    if is_shooting_star:
        patterns.append("Shooting Star")
        
    # 4. Bullish Engulfing
    is_bull_eng = _is_bullish_engulfing(curr, prev)
    if is_bull_eng:
        patterns.append("Bullish Engulfing")
        
    # 5. Bearish Engulfing
    is_bear_eng = _is_bearish_engulfing(curr, prev)
    if is_bear_eng:
        patterns.append("Bearish Engulfing")
        
    return {
        "patterns": patterns,
        "is_doji": is_doji,
        "is_hammer": is_hammer,
        "is_shooting_star": is_shooting_star,
        "is_bullish_engulfing": is_bull_eng,
        "is_bearish_engulfing": is_bear_eng
    }
