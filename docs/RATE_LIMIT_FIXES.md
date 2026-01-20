# Rate Limit Fixes - Yahoo Finance API

## Summary of Changes

This document outlines the rate limit issues found and fixes applied to prevent Yahoo Finance API rate limiting.

---

## 🔴 Issues Found

### 1. **Insufficient Request Delays**
- **Old:** 200-500ms between requests
- **Problem:** Yahoo Finance allows ~2000 requests/hour (~1.8s per request). With 130+ stocks, you were making 5+ requests/second
- **Fix:** Increased to 1.5-3 seconds between requests

### 2. **Batch Fetching Without Proper Chunking**
- **Old:** `fetch_data_batch()` called Yahoo Finance with all 130 tickers at once
- **Problem:** Single API call with 130 tickers still heavily loads Yahoo's servers and triggers rate limits
- **Fix:** Implemented chunking - fetch 10 tickers at a time with 5-second delays between batches

### 3. **Stock Info Loop Without Rate Limiting**
- **Old:** `fetch_stock_info_batch()` looped through all tickers with only one `rate_limiter.wait()` at the start
- **Problem:** 130 rapid API calls to fetch `.info` for each ticker
- **Fix:** Each ticker now calls `get_stock_info()` which applies rate limiting per request

### 4. **Circuit Breaker Too Lenient**
- **Old:** Allowed 3 consecutive 429 errors before stopping
- **Problem:** By then, your IP may already be rate-limited for hours
- **Fix:** Reduced to 2 consecutive failures for faster detection

---

## ✅ Changes Applied

### Configuration Changes (`src/config.py`)

```python
# Old values
REQUEST_DELAY_MIN = 0.2       # 200ms
REQUEST_DELAY_MAX = 0.5       # 500ms
MAX_CONSECUTIVE_429 = 3

# New values
REQUEST_DELAY_MIN = 1.5       # 1.5 seconds - Yahoo Finance safe
REQUEST_DELAY_MAX = 3.0       # 3.0 seconds - adds randomness
MAX_CONSECUTIVE_429 = 2       # Fail faster to prevent IP ban
BATCH_SIZE = 10               # NEW: Max tickers per batch
BATCH_DELAY = 5.0             # NEW: Extra delay between batches
```

### Data Fetching Refactor (`src/data.py`)

#### Before:
```python
@retry_with_backoff()
def fetch_data_batch(tickers, ...):
    rate_limiter.wait()  # ❌ Only one wait
    df = yf.download(tickers, ...)  # ❌ All 130 at once
    return df
```

#### After:
```python
def fetch_data_batch(tickers, ...):
    results = {}
    batch_size = config.BATCH_SIZE  # 10 tickers
    
    # Process in chunks
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        
        # Fetch batch with rate limiting
        batch_result = _fetch_batch_chunk(batch, ...)
        results.update(batch_result)
        
        # Wait between batches
        if i + batch_size < len(tickers):
            time.sleep(config.BATCH_DELAY)  # 5 seconds
    
    return results

@retry_with_backoff()
def _fetch_batch_chunk(tickers, ...):
    rate_limiter.wait()  # ✅ Rate limited per chunk
    df = yf.download(tickers, ..., group_by='ticker')
    return parse_results(df)
```

#### Stock Info Fetching:
```python
def fetch_stock_info_batch(tickers):
    results = {}
    for ticker in tickers:
        # Each call is rate limited individually
        info = get_stock_info(ticker)  # ✅ Has @retry_with_backoff and rate_limiter.wait()
        results[ticker] = info
    return results
```

### Better Progress Reporting (`src/main.py`)

- Added step-by-step progress indicators
- Shows batch progress: "Batch 1/13: Fetching 10 tickers..."
- Shows analysis progress: "Analyzing 45/130: BBCA.JK..."

---

## 📊 Expected Performance

### Before (130 tickers):
- **Batch fetch:** 1 request × 130 tickers = RATE LIMITED ⚠️
- **Info fetch:** 130 rapid requests = RATE LIMITED ⚠️
- **Total time:** ~30 seconds (before getting blocked)

### After (130 tickers):
- **Batch fetch:** 13 batches × 10 tickers = 13 API calls with 5s delays
- **Info fetch (if enabled):** 130 requests with 1.5-3s delays each
- **Total time:** 
  - Data fetching: ~65 seconds (13 batches × 5s)
  - Info fetching: ~325 seconds if ENABLE_MCAP_FILTER=True (130 × 2.5s avg)
  - Analysis: ~5 seconds
  - **Grand total: ~70 seconds without info, ~395 seconds (~6.5 min) with info**

---

## 🚀 Recommendations

### 1. **Disable Market Cap Filter for Daily Scans**
Since you're scanning the same watchlist daily, fetch stock info once and cache it:

```python
# In src/config.py
ENABLE_MCAP_FILTER = False  # Disable for faster scans
```

**Alternative:** Create pre-filtered watchlists that only include stocks above your market cap threshold.

### 2. **Cache Stock Info**
Create a cache file for stock fundamentals (market cap, sector, etc.) that updates weekly:

```bash
# Run once per week
python -m src.main --update-cache

# Daily scans use cached data
python -m src.main
```

### 3. **Use Smaller Watchlists**
Instead of scanning all 130 idx_liquid stocks daily:

```bash
# Scan only LQ45 (47 stocks) - finishes in ~2.5 minutes
python -m src.main --list lq45

# Or create custom watchlist with your favorite 20-30 stocks
python -m src.main --list my_favorites
```

### 4. **Adjust Batch Size Based on Experience**
If you still get rate limited:

```python
# In src/config.py - be more conservative
BATCH_SIZE = 5           # Smaller batches
BATCH_DELAY = 10.0       # Longer delays
REQUEST_DELAY_MIN = 2.0  # Slower individual requests
REQUEST_DELAY_MAX = 4.0
```

If it works smoothly:

```python
# In src/config.py - slightly faster
BATCH_SIZE = 15          # Larger batches
BATCH_DELAY = 3.0        # Shorter delays
```

### 5. **Schedule Scans During Off-Peak Hours**
Yahoo Finance API has less traffic during:
- Asian morning hours (7-9 AM WIB)
- US evening hours (9 PM - midnight WIB)

### 6. **Alternative Data Sources (Future)**
Consider these alternatives if Yahoo Finance continues to be problematic:
- **Alpha Vantage** - Free tier: 500 requests/day
- **IEX Cloud** - Free tier: 50,000 messages/month
- **Finnhub** - Free tier: 60 API calls/minute
- **IDX Direct** - Official Indonesia Stock Exchange data

---

## 🧪 Testing the Fixes

### Test 1: Small Watchlist (No Rate Limits Expected)
```bash
# Should complete in ~30 seconds
python -m src.main BBCA BBRI TLKM ASII UNVR
```

### Test 2: Medium Watchlist (47 stocks)
```bash
# Should complete in ~2.5 minutes (without info fetch)
python -m src.main --list lq45
```

### Test 3: Large Watchlist (130 stocks) - With Info
```bash
# Should complete in ~6.5 minutes
# Watch for any 429 errors
python -m src.main --list idx_liquid
```

### Test 4: Backtest (Sequential Fetching)
```bash
# This will take longer due to historical data fetching
python -m src.main --backtest BBCA BBRI TLKM
```

---

## 🔍 Monitoring for Rate Limits

Watch the console output for these signs:

### ✅ Good Signs:
```
Fetching data for 130 tickers in 13 batches...
Batch 1/13: Fetching 10 tickers...
Batch 2/13: Fetching 10 tickers...
Successfully fetched 128/130 tickers
```

### ⚠️ Warning Signs:
```
Attempt 1/4 failed: Too Many Requests. Retrying in 5s...
Attempt 2/4 failed: Too Many Requests. Retrying in 25s...
```
**Action:** If you see this, the delays are working but you may need to increase them.

### 🔴 Critical Signs:
```
Circuit breaker: 2 consecutive 429 errors. Stopping.
Too many 429 errors (2). Wait and try again later.
```
**Action:** Stop and wait 30-60 minutes. Increase `REQUEST_DELAY_MIN/MAX` and decrease `BATCH_SIZE`.

---

## 📝 Additional Notes

1. **Duplicate Function Removed:** Removed duplicate `get_stock_info()` function in `data.py`

2. **Better Error Handling:** Each batch now falls back to individual fetching if batch fails

3. **Multi-Index Parsing:** Fixed DataFrame parsing for multi-ticker downloads using `group_by='ticker'`

4. **Progress Tracking:** Added detailed progress output so you can see what's happening

5. **Clean Code:** Applied PEP 8 formatting and added comprehensive docstrings

---

## 🎯 Quick Start After Fixes

```bash
# 1. Fastest scan - specific stocks (30 sec)
python -m src.main BBCA BBRI TLKM ASII

# 2. Fast scan - LQ45 without market cap filter (2.5 min)
# First, disable MCAP filter in src/config.py:
# ENABLE_MCAP_FILTER = False
python -m src.main --list lq45

# 3. Full scan - all liquid stocks (6.5 min with MCAP filter)
python -m src.main --list idx_liquid
```

---

## 💡 Pro Tips

1. **Run once in the morning** - Market opens at 9:00 AM WIB, scan at 9:30 AM after volatility settles

2. **Cache your results** - Save scan results to a file for reference:
   ```bash
   python -m src.main --list lq45 > scan_results_$(date +%Y%m%d).txt
   ```

3. **Use watchlist rotation** - Don't scan the same large list repeatedly:
   - Monday: Banking sector
   - Tuesday: Infrastructure
   - Wednesday: Consumer goods
   - Thursday: Tech & Telecom
   - Friday: Mixed/Opportunities

4. **Backtest on weekends** - Historical data fetching is slower, do it when you have time

---

## ✅ Verification Checklist

- [x] Increased `REQUEST_DELAY_MIN/MAX` to Yahoo Finance safe values (1.5-3s)
- [x] Implemented batch chunking (10 tickers per batch)
- [x] Added `BATCH_DELAY` between chunks (5s)
- [x] Fixed `fetch_stock_info_batch()` to rate limit per ticker
- [x] Reduced `MAX_CONSECUTIVE_429` to fail faster (2)
- [x] Improved progress reporting in `main.py`
- [x] Added proper error handling and fallback mechanisms
- [x] Documented all changes and recommendations
- [x] Provided testing procedures and monitoring guidelines

---

**Status:** ✅ READY FOR TESTING

Test with small watchlists first, then gradually increase to verify the fixes work for your use case.