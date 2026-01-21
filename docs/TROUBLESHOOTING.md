# Troubleshooting

Common issues and how to fix them.

## Rate Limiting (Yahoo Finance)

### Symptoms
```
Attempt 1/4 failed: Too Many Requests. Retrying in 5s...
Circuit breaker: 2 consecutive 429 errors. Stopping.
```

### Solutions

**Quick fix - use smaller watchlists:**
```bash
python -m src.main BBCA BBRI TLKM  # 5 stocks = ~30 seconds
python -m src.main --list lq45     # 47 stocks = ~2.5 minutes
```

**Disable market cap filter** in `src/config.py`:
```python
ENABLE_MCAP_FILTER = False  # 2-3x faster scans
```

**If still rate limited**, edit `src/config.py`:
```python
REQUEST_DELAY_MIN = 2.0    # Increase from 1.5
REQUEST_DELAY_MAX = 4.0    # Increase from 3.0
BATCH_SIZE = 5             # Decrease from 10
```

**If you get IP banned:**
1. Wait 1-2 hours
2. Visit https://finance.yahoo.com in browser to verify access
3. Consider using a VPN

## Common Errors

### "No module named 'yfinance'"
```bash
pip install -r requirements.txt
```

### "No data found for ticker"
Stock ticker may be incorrect. IDX stocks need `.JK` suffix:
```
BBCA.JK   ✓ correct
BBCA      ✗ wrong
```

### "Empty watchlist"
Make sure watchlist file exists and contains valid tickers:
```bash
cat watchlists/lq45.txt
```

### Charts not showing
```bash
pip install matplotlib seaborn
```

## Expected Scan Times

| Watchlist | Stocks | Time |
|-----------|--------|------|
| Manual (5 stocks) | 5 | ~30 seconds |
| LQ45 | 47 | ~2.5 minutes |
| IDX Liquid | 130 | ~10 minutes |

## Where to Find Output

| Type | Location |
|------|----------|
| Scan results | `output/scans/` |
| Backtest reports | `output/backtests/` |
| Charts | `output/charts/` |
| Logs | `logs/` |

## Getting Help

Open an issue on GitHub with:
1. What command you ran
2. The full error message
3. Your Python version (`python --version`)
