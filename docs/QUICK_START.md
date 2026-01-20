# Quick Start Guide - Updated Rate Limiter

## What Changed?

Your scanner was getting rate-limited by Yahoo Finance because it was making requests too quickly. I've fixed this by:

1. **Slowing down requests:** 1.5-3 seconds between requests (was 200-500ms)
2. **Chunking batch requests:** Fetching 10 tickers at a time instead of all 130 at once
3. **Adding delays between batches:** 5 seconds between each batch of 10 stocks
4. **Better error detection:** Stops faster when rate limits are hit

---

## Expected Scan Times

| Watchlist | Stocks | Without Market Cap Filter | With Market Cap Filter |
|-----------|--------|---------------------------|------------------------|
| Manual (5 stocks) | 5 | ~30 seconds | ~45 seconds |
| LQ45 | 47 | ~2.5 minutes | ~5 minutes |
| IDX Liquid | 130 | ~4 minutes | ~10 minutes |

**Recommendation:** Disable market cap filter for faster scans (see below).

---

## Fastest Setup for Daily Scans

### Option 1: Disable Market Cap Filter (RECOMMENDED)

Since you're scanning the same stocks daily, you don't need to fetch market cap info every time.

**Edit `src/config.py`:**
```python
# Change this line from True to False
ENABLE_MCAP_FILTER = False
```

**Result:** Scans complete 2-3x faster!

### Option 2: Use Smaller Watchlists

Create custom watchlists with your favorite stocks:

**Create `watchlists/my_picks.txt`:**
```
BBCA.JK
BBRI.JK
TLKM.JK
ASII.JK
UNVR.JK
GOTO.JK
ANTM.JK
INCO.JK
PTBA.JK
ITMG.JK
```

**Run:**
```bash
python -m src.main --list my_picks
```

---

## Common Commands

### Daily Scanning
```bash
# Fast scan - specific stocks (30 sec)
python -m src.main BBCA BBRI TLKM

# Medium scan - LQ45 blue chips (~2.5 min)
python -m src.main --list lq45

# Full scan - all liquid stocks (~4 min)
python -m src.main --list idx_liquid
```

### Backtesting
```bash
# Quick backtest - 3 stocks
python -m src.main --backtest BBCA BBRI TLKM

# Full backtest - LQ45 (takes 30-45 min)
python -m src.main --backtest --list lq45

# Backtest with charts
python -m src.main --backtest --detailed --charts BBCA BBRI
```

---

## What You'll See (New Output)

### Step 1: Fetching Historical Data
```
Step 1/3: Fetching historical data...
Fetching data for 130 tickers in 13 batches...
Batch 1/13: Fetching 10 tickers...
Batch 2/13: Fetching 10 tickers...
...
Successfully fetched 128/130 tickers
```

### Step 2: Fetching Stock Info (if ENABLE_MCAP_FILTER = True)
```
Step 2/3: Fetching stock info for market cap filter...
Fetching info 1/130: BBCA.JK...
Fetching info 2/130: BBRI.JK...
...
Successfully fetched info for 125/130 tickers
```

### Step 3: Analysis
```
Step 3/3: Analyzing tickers...
Analyzing 45/130: TLKM.JK...
Analysis complete!
```

---

## Troubleshooting

### Still Getting Rate Limited?

**Increase delays in `src/config.py`:**
```python
REQUEST_DELAY_MIN = 2.0    # Increase from 1.5
REQUEST_DELAY_MAX = 4.0    # Increase from 3.0
BATCH_SIZE = 5             # Decrease from 10
BATCH_DELAY = 10.0         # Increase from 5.0
```

### Too Slow?

**If scans work fine but are too slow:**
```python
REQUEST_DELAY_MIN = 1.0    # Decrease (risky!)
REQUEST_DELAY_MAX = 2.0    # Decrease (risky!)
BATCH_SIZE = 15            # Increase
BATCH_DELAY = 3.0          # Decrease
```

**⚠️ Warning:** Going too fast may trigger rate limits again!

### "Circuit breaker" Error

```
Circuit breaker: 2 consecutive 429 errors. Stopping.
```

**What to do:**
1. Wait 30-60 minutes before trying again
2. Increase the delays (see "Still Getting Rate Limited?" above)
3. Use smaller watchlists or disable MCAP filter

---

## Best Practices

### 1. Morning Routine (9:30 AM WIB)
```bash
# After market opens and stabilizes
python -m src.main --list lq45 > results_$(date +%Y%m%d).txt

# Review the results file
cat results_$(date +%Y%m%d).txt
```

### 2. Save Scan Results
```bash
# Linux/Mac
python -m src.main --list lq45 | tee scan_results.txt

# Windows
python -m src.main --list lq45 > scan_results.txt
```

### 3. Watchlist Rotation (Advanced)
Don't scan 130 stocks daily. Rotate by sector:

**Monday:** Banking
```bash
python -m src.main BBCA BBRI BMRI BBNI BBTN
```

**Tuesday:** Infrastructure
```bash
python -m src.main TLKM PGAS JSMR PTPP WIKA
```

**Wednesday:** Consumer
```bash
python -m src.main UNVR ICBP INDF KLBF GGRM
```

**Thursday:** Mining/Commodities
```bash
python -m src.main ANTM INCO PTBA ITMG ADRO
```

**Friday:** Tech/Others
```bash
python -m src.main GOTO EMTK BUKA MEDC CPIN
```

---

## Configuration Reference

### Key Settings in `src/config.py`

```python
# Rate Limiting (NEW VALUES)
ENABLE_RATE_LIMITER = True
REQUEST_DELAY_MIN = 1.5      # Min delay between requests (seconds)
REQUEST_DELAY_MAX = 3.0      # Max delay between requests (seconds)
BATCH_SIZE = 10              # Tickers per batch
BATCH_DELAY = 5.0            # Delay between batches (seconds)
MAX_CONSECUTIVE_429 = 2      # Stop after N rate limit errors

# Speed vs Safety Trade-off
ENABLE_MCAP_FILTER = False   # Set False for 2-3x faster scans
```

### Speed Comparison

| Setting | Scan Time (130 stocks) | Risk |
|---------|------------------------|------|
| Conservative (DELAY=2-4s, BATCH=5) | ~15 min | Very Safe ✅ |
| **Default (DELAY=1.5-3s, BATCH=10)** | **~10 min** | **Safe ✅** |
| Moderate (DELAY=1-2s, BATCH=15) | ~6 min | Moderate ⚠️ |
| Aggressive (DELAY=0.5-1s, BATCH=20) | ~3 min | Risky ❌ |

---

## Testing Your Setup

### Test 1: Verify Fixes Work
```bash
# Small test - should complete without errors
python -m src.main BBCA BBRI TLKM ASII UNVR
```

**Expected:** Completes in ~30 seconds, no 429 errors

### Test 2: Medium Load
```bash
# 47 stocks - should complete in ~2.5 min
python -m src.main --list lq45
```

**Watch for:** "Successfully fetched X/47 tickers" message

### Test 3: Full Load
```bash
# 130 stocks - monitor carefully
python -m src.main --list idx_liquid
```

**Watch for:** 
- ✅ "Batch 1/13", "Batch 2/13", etc.
- ✅ "Successfully fetched X/130 tickers"
- ❌ "429 errors" or "Circuit breaker"

---

## Emergency Actions

### If You Get IP Banned
1. **Wait:** 1-2 hours minimum
2. **Check:** Visit https://finance.yahoo.com in browser
3. **Restart router:** Get new IP address (if possible)
4. **Use VPN:** As last resort
5. **Increase delays:** Make settings more conservative

### If Scans Take Too Long
1. **Disable MCAP filter:** `ENABLE_MCAP_FILTER = False`
2. **Use smaller watchlists:** 20-30 stocks max
3. **Pre-filter stocks:** Create curated watchlists
4. **Run during off-peak:** 7-9 AM or 9-11 PM WIB

---

## Additional Resources

- **Full documentation:** See `RATE_LIMIT_FIXES.md`
- **Strategy guide:** See `README.md`
- **Issue tracker:** Report problems on GitHub

---

## Summary

✅ **Rate limiter is now fixed**  
✅ **Default settings are safe for most users**  
✅ **Scans will be slower but reliable**  
✅ **Disable MCAP filter for 2-3x speed boost**  
✅ **Use smaller watchlists for fastest results**  

**Happy Trading! 📈**

Remember: Slower scans = No rate limits = Consistent results