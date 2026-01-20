import pandas as pd
import numpy as np
from . import config

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def calculate_rsi(series, period=14):
    """
    Calculate RSI using Wilder's Smoothing Method.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # Wilder's smoothing
    for i in range(period, len(series)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period
        
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(series, fast)
    ema_slow = calculate_ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_atr(df, period=14):
    """
    Calculate Average True Range (ATR).
    """
    high = df['High']
    low = df['Low']
    close = df['Close'].shift(1)
    
    tr1 = high - low
    tr2 = (high - close).abs()
    tr3 = (low - close).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_pivot_points(df):
    """
    Calculate Classic Pivot Points using previous day's OHLC.
    Returns: pivot, support1, support2, resistance1, resistance2
    """
    if len(df) < 2:
        return None
    
    prev = df.iloc[-2]
    high = float(prev['High'])
    low = float(prev['Low'])
    close = float(prev['Close'])
    
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    r2 = pivot + (high - low)
    s1 = (2 * pivot) - high
    s2 = pivot - (high - low)
    
    return {
        'pivot': pivot,
        'r1': r1,
        'r2': r2,
        's1': s1,
        's2': s2
    }

def find_swing_levels(df, lookback=20):
    """
    Find recent swing highs and lows as support/resistance levels.
    """
    if len(df) < lookback:
        return None
    
    recent = df.tail(lookback)
    
    swing_high = float(recent['High'].max())
    swing_low = float(recent['Low'].min())
    
    high_idx = recent['High'].idxmax()
    low_idx = recent['Low'].idxmin()
    
    return {
        'swing_high': swing_high,
        'swing_low': swing_low,
        'high_date': high_idx,
        'low_date': low_idx
    }

def analyze_support_resistance(current_price, pivot_data, swing_data):
    """
    Analyze price position relative to support/resistance levels.
    Returns recommendation based on S/R levels.
    """
    if not pivot_data or not swing_data:
        return {'sr_signal': 'NEUTRAL', 'nearest_support': 0, 'nearest_resistance': 0, 'sr_score': 0}
    
    supports = [pivot_data['s1'], pivot_data['s2'], swing_data['swing_low']]
    resistances = [pivot_data['r1'], pivot_data['r2'], swing_data['swing_high']]
    
    supports_below = [s for s in supports if s < current_price]
    resistances_above = [r for r in resistances if r > current_price]
    
    nearest_support = max(supports_below) if supports_below else min(supports)
    nearest_resistance = min(resistances_above) if resistances_above else max(resistances)
    
    support_distance_pct = ((current_price - nearest_support) / current_price) * 100
    resistance_distance_pct = ((nearest_resistance - current_price) / current_price) * 100
    
    sr_score = 0
    
    if support_distance_pct < 2:
        sr_score += 2
        sr_signal = 'NEAR SUPPORT'
    elif support_distance_pct < 5:
        sr_score += 1
        sr_signal = 'ABOVE SUPPORT'
    elif resistance_distance_pct < 2:
        sr_score -= 2
        sr_signal = 'NEAR RESISTANCE'
    elif resistance_distance_pct < 5:
        sr_score -= 1
        sr_signal = 'BELOW RESISTANCE'
    else:
        sr_signal = 'NEUTRAL'
    
    risk_reward = resistance_distance_pct / support_distance_pct if support_distance_pct > 0 else 0
    if risk_reward > 2:
        sr_score += 1
    elif risk_reward < 0.5:
        sr_score -= 1
    
    return {
        'sr_signal': sr_signal,
        'nearest_support': nearest_support,
        'nearest_resistance': nearest_resistance,
        'support_distance_pct': support_distance_pct,
        'resistance_distance_pct': resistance_distance_pct,
        'risk_reward': risk_reward,
        'sr_score': sr_score
    }

def to_weekly(df_daily):
    """
    Resample daily OHLCV to weekly candles.
    """
    df = df_daily.copy()
    df.index = pd.to_datetime(df.index)
    
    weekly = df.resample("W-FRI").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    })
    return weekly.dropna(subset=["Close"])

def analyze_weekly_trend(df_weekly):
    """
    Analyze weekly trend alignment using EMAs.
    """
    if df_weekly is None or len(df_weekly) < config.WEEKLY_SLOW_EMA + 5:
        return {"weekly_trend": "UNKNOWN", "weekly_aligned": True}
    
    close = df_weekly["Close"]
    ema_fast = calculate_ema(close, config.WEEKLY_FAST_EMA)
    ema_slow = calculate_ema(close, config.WEEKLY_SLOW_EMA)
    
    aligned = bool(ema_fast.iloc[-1] > ema_slow.iloc[-1])
    trend = "UP" if aligned else "DOWN"
    return {"weekly_trend": trend, "weekly_aligned": aligned}

def analyze_market_regime(df_market):
    """
    Analyze overall market health using ^JKSE EMAs.
    """
    if df_market is None or len(df_market) < config.MARKET_SLOW_EMA + 5:
        return {"market_regime": "UNKNOWN", "risk_on": True}
    
    if isinstance(df_market.columns, pd.MultiIndex):
        df_market.columns = df_market.columns.get_level_values(0)
    
    close = df_market["Close"]
    ema_fast = calculate_ema(close, config.MARKET_FAST_EMA)
    ema_slow = calculate_ema(close, config.MARKET_SLOW_EMA)
    
    risk_on = bool(ema_fast.iloc[-1] > ema_slow.iloc[-1])
    regime = "RISK_ON" if risk_on else "RISK_OFF"
    return {"market_regime": regime, "risk_on": risk_on}

def get_investment_strategy(analysis, weekly_ctx, market_ctx):
    """
    Determine investment strategy based on multiple factors.
    Returns: BUY ALL, BUY PARTIAL, HOLD, SELL PARTIAL, SELL ALL
    """
    signal = analysis.get("signal", "")
    final_signal = analysis.get("final_signal", signal)
    rsi = analysis.get("rsi", 50)
    vol_ratio = analysis.get("vol_ratio", 1.0)
    weekly_aligned = weekly_ctx.get("weekly_aligned", True)
    risk_on = (market_ctx or {}).get("risk_on", True)
    price_vs_ema = analysis.get("price_vs_ema_pct", 0)
    sr_score = analysis.get("sr_score", 0)
    
    score = 0
    
    if "BUY" in final_signal and "WAIT" not in final_signal:
        score += 3
        if "STRONG" in final_signal:
            score += 2
        elif "WEAK" in final_signal:
            score -= 1
    elif "UPTREND" in signal:
        score += 1
    elif "DOWNTREND" in signal:
        score -= 2
    elif "WAIT" in final_signal:
        score += 0
    
    if weekly_aligned:
        score += 1
    else:
        score -= 1
    
    if risk_on:
        score += 1
    else:
        score -= 1
    
    if rsi < 30:
        score += 2
    elif rsi < 40:
        score += 1
    elif rsi > 80:
        score -= 2
    elif rsi > 70:
        score -= 1
    
    if vol_ratio > 1.5:
        score += 1
    elif vol_ratio < 0.5:
        score -= 1
    
    if price_vs_ema < -5:
        score += 1
    elif price_vs_ema > 10:
        score -= 1
    
    score += sr_score
    
    if score >= 5:
        return "BUY ALL"
    elif score >= 3:
        return "BUY PARTIAL"
    elif score >= 0:
        return "HOLD"
    elif score >= -2:
        return "SELL PARTIAL"
    else:
        return "SELL ALL"

def combine_signals(base_analysis, weekly_ctx, market_ctx):
    """
    Combine daily signal with weekly trend and market regime context.
    """
    weekly_ok = weekly_ctx.get("weekly_aligned", True)
    risk_on = (market_ctx or {}).get("risk_on", True)
    
    original_signal = base_analysis["signal"]
    final_signal = original_signal
    context_reasons = []
    score = 0
    
    if original_signal == "BUY":
        score += 2
        
        if weekly_ok:
            score += 1
        else:
            context_reasons.append("Weekly misaligned")
            
        if risk_on:
            score += 1
        else:
            context_reasons.append("Market risk-off")
        
        if config.ENABLE_MTF and config.MTF_REQUIRED_FOR_BUY and not weekly_ok:
            final_signal = "WAIT (Weekly misaligned)"
        elif config.ENABLE_MARKET_FILTER and config.MARKET_FILTER_MODE == "BLOCK" and not risk_on:
            final_signal = "WAIT (Market risk-off)"
        else:
            if weekly_ok and risk_on:
                final_signal = "BUY (STRONG)"
            elif weekly_ok and not risk_on:
                final_signal = "BUY (WEAK-MKT)"
            elif not weekly_ok and risk_on:
                final_signal = "BUY (WEAK-W)"
            else:
                final_signal = "BUY (WEAK)"
    
    base_analysis.update({
        "final_signal": final_signal,
        "score": score,
        "weekly_trend": weekly_ctx.get("weekly_trend"),
        "market_regime": (market_ctx or {}).get("market_regime"),
        "context_reasons": context_reasons,
    })
    
    strategy = get_investment_strategy(base_analysis, weekly_ctx, market_ctx)
    base_analysis["strategy"] = strategy
    
    return base_analysis

def analyze_ticker(df, market_ctx=None):
    """
    Applies the swing trading strategy to the dataframe.
    """
    if df is None or len(df) < max(config.SLOW_EMA, config.MACD_SLOW + config.MACD_SIGNAL, config.ATR_PERIOD):
        return None

    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # Handle yfinance multi-index if necessary
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Convert all columns to numeric and handle potential NaNs
    for col in ['Close', 'Open', 'High', 'Low', 'Volume']:
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=['Close'])
    close = df['Close']
    volume = df['Volume']
    
    # Calculate Indicators
    df.loc[:, 'EMA_Fast'] = calculate_ema(close, config.FAST_EMA)
    df.loc[:, 'EMA_Slow'] = calculate_ema(close, config.SLOW_EMA)
    df.loc[:, 'RSI'] = calculate_rsi(close, config.RSI_PERIOD)
    df.loc[:, 'ATR'] = calculate_atr(df, config.ATR_PERIOD)
    
    macd_line, signal_line, hist = calculate_macd(close, config.MACD_FAST, config.MACD_SLOW, config.MACD_SIGNAL)
    df.loc[:, 'MACD'] = macd_line
    df.loc[:, 'MACD_Signal'] = signal_line
    df.loc[:, 'MACD_Hist'] = hist
    
    df.loc[:, 'Vol_Avg'] = volume.rolling(window=config.VOL_AVG_PERIOD).mean()

    if len(df) < 2:
        return None

    # Get latest values
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Primary Signal: Golden Cross (EMA20 crosses above EMA50)
    crossover_today = (last_row['EMA_Fast'] > last_row['EMA_Slow']) and (prev_row['EMA_Fast'] <= prev_row['EMA_Slow'])
    
    current_price = float(last_row['Close'])
    atr_value = float(last_row['ATR'])
    
    stop_loss = 0.0
    take_profit_min = 0.0
    take_profit_max = 0.0
    is_setup = False
    
    # Target SL/TP calculation (used for BUY setups and UPTREND reference)
    def get_risk_levels(price, atr):
        sl = price - (atr * config.ATR_MULTIPLIER)
        # Sanity check for SL
        if sl > price:
            sl = price * (1 - config.STOP_LOSS_PCT)
        tp_min = price * (1 + config.TARGET_PROFIT_MIN)
        tp_max = price * (1 + config.TARGET_PROFIT_MAX)
        return sl, tp_min, tp_max

    if crossover_today:
        is_setup = True
        reasons = []
        is_buy = True
        
        # Filter 1: RSI not overbought
        if last_row['RSI'] > config.RSI_OVERBOUGHT:
            is_buy = False
            reasons.append("Overbought RSI")
        elif last_row['RSI'] < 40: # Momentum check
            is_buy = False
            reasons.append("Weak RSI")

        # Filter 2: MACD Confirmation
        if last_row['MACD'] < last_row['MACD_Signal']:
            is_buy = False
            reasons.append("Bearish MACD")
            
        # Filter 3: Volume Confirmation
        vol_ratio = last_row['Volume'] / last_row['Vol_Avg'] if last_row['Vol_Avg'] > 0 else 0
        if config.VOLUME_STRICT_FILTER:
            if vol_ratio < config.VOL_RATIO_MIN:
                is_buy = False
                reasons.append(f"Low Vol ({vol_ratio:.1f}x)")

        signal = "BUY" if is_buy else f"WAIT ({', '.join(reasons)})"
        stop_loss, take_profit_min, take_profit_max = get_risk_levels(current_price, atr_value)
        
    else:
        # No crossover today
        if last_row['EMA_Fast'] > last_row['EMA_Slow']:
            signal = "UPTREND (No Cross)"
            # Reference SL/TP for UPTREND
            stop_loss, take_profit_min, take_profit_max = get_risk_levels(current_price, atr_value)
        else:
            signal = "DOWNTREND"
            stop_loss, take_profit_min, take_profit_max = 0.0, 0.0, 0.0
            
    ema_slow_value = float(last_row['EMA_Slow'])
    price_vs_ema_pct = ((current_price - ema_slow_value) / ema_slow_value) * 100 if ema_slow_value > 0 else 0
    
    pivot_data = calculate_pivot_points(df)
    swing_data = find_swing_levels(df, lookback=20)
    sr_analysis = analyze_support_resistance(current_price, pivot_data, swing_data)
    
    base_analysis = {
        "signal": signal,
        "is_setup": is_setup,
        "current_price": current_price,
        "ideal_entry": current_price,
        "target_profit_range": f"{config.TARGET_PROFIT_MIN*100:.0f}-{config.TARGET_PROFIT_MAX*100:.0f}%",
        "rsi": last_row['RSI'],
        "macd_hist": last_row['MACD_Hist'],
        "vol_ratio": last_row['Volume'] / last_row['Vol_Avg'] if last_row['Vol_Avg'] > 0 else 0,
        "stop_loss": stop_loss,
        "take_profit_min": take_profit_min,
        "take_profit_max": take_profit_max,
        "price_vs_ema_pct": price_vs_ema_pct,
        "sr_signal": sr_analysis['sr_signal'],
        "nearest_support": sr_analysis['nearest_support'],
        "nearest_resistance": sr_analysis['nearest_resistance'],
        "sr_score": sr_analysis['sr_score']
    }
    
    if config.ENABLE_MTF or config.ENABLE_MARKET_FILTER:
        weekly_df = to_weekly(df)
        weekly_ctx = analyze_weekly_trend(weekly_df)
        base_analysis = combine_signals(base_analysis, weekly_ctx, market_ctx)
    else:
        base_analysis["final_signal"] = signal
        base_analysis["weekly_trend"] = None
        base_analysis["market_regime"] = None
        base_analysis["score"] = 0
        base_analysis["context_reasons"] = []
        weekly_ctx = {"weekly_aligned": True, "weekly_trend": None}
        base_analysis["strategy"] = get_investment_strategy(base_analysis, weekly_ctx, market_ctx)
    
    return base_analysis
