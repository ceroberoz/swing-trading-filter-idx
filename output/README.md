# Output Directory

This directory contains all generated outputs from the Swing Trading Scanner.

## Structure

```
output/
├── scans/          # Daily scan results
├── backtests/      # Backtest reports and analysis
└── charts/         # Generated charts and visualizations
```

## Subdirectories

### 📊 `scans/`
Daily and on-demand scan results.

**Example Usage:**
```bash
# Save scan results
python -m src.main --list lq45 > output/scans/scan_$(date +%Y%m%d).txt

# Review results
cat output/scans/scan_20240115.txt
```

### 📈 `backtests/`
Backtesting results and performance reports.

**Example Usage:**
```bash
# Save backtest results
python -m src.main --backtest --list lq45 > output/backtests/backtest_lq45_$(date +%Y%m%d).txt

# Detailed backtest with charts
python -m src.main --backtest --detailed --charts --list lq45
```

### 📉 `charts/`
Performance charts and visualizations.

**Generated Charts:**
- `backtest_performance.png` - Equity curve and drawdown
- `monthly_returns.png` - Monthly return heatmap
- `win_rate_comparison.png` - Win rate across tickers

## File Naming Conventions

Use consistent naming for easy organization:

| File Type | Pattern | Example |
|-----------|---------|---------|
| Daily Scan | `scan_YYYYMMDD.txt` | `scan_20240115.txt` |
| Watchlist Scan | `{list}_scan_YYYYMMDD.txt` | `lq45_scan_20240115.txt` |
| Backtest | `backtest_{list}_YYYYMMDD.txt` | `backtest_lq45_20240115.txt` |
| Chart | `{chart_type}_YYYYMMDD.png` | `equity_curve_20240115.png` |

## Maintenance

### Clean Old Files
Keep your output directory manageable by cleaning old files:

```bash
# Delete files older than 30 days
find output/scans/ -name "*.txt" -mtime +30 -delete
find output/backtests/ -name "*.txt" -mtime +30 -delete
find output/charts/ -name "*.png" -mtime +30 -delete
```

### Archive Important Results
```bash
# Create archive directory
mkdir -p output/archive/2024Q1/

# Move important results
mv output/backtests/backtest_summary_*.txt output/archive/2024Q1/
```

## Git Ignore

**All files in this directory are ignored by git** (except `.gitkeep` and `README.md`).

This prevents committing large data files or personal trading results to version control.

## Best Practices

1. **Use Dates** - Always include date in filename (YYYYMMDD format)
2. **Be Descriptive** - Include watchlist or stock names in filename
3. **Clean Regularly** - Delete files older than 30-90 days
4. **Backup Important Results** - Archive significant backtest results
5. **Organize by Quarter/Month** - Create subdirectories for long-term organization

## Quick Commands

```bash
# Today's scan
TODAY=$(date +%Y%m%d)
python -m src.main --list lq45 > output/scans/lq45_scan_${TODAY}.txt

# Weekly backtest (with charts)
python -m src.main --backtest --charts --list lq45 > output/backtests/weekly_backtest_${TODAY}.txt

# View latest scan
ls -lt output/scans/ | head -n 5
cat output/scans/$(ls -t output/scans/*.txt | head -n 1)

# View latest backtest
cat output/backtests/$(ls -t output/backtests/*.txt | head -n 1)
```

## Disk Space

Monitor disk usage to prevent filling up:

```bash
# Check output directory size
du -sh output/

# Check each subdirectory
du -sh output/*/

# Find largest files
find output/ -type f -exec du -h {} + | sort -rh | head -n 10
```

## Notes

- Output files are **local only** and not synchronized with git
- Safe to delete entire directory - will be regenerated as needed
- Consider compressing old files: `gzip output/scans/scan_2024*.txt`
- Chart files can be large (PNG format) - clean regularly

---

**Happy Trading! 📊**