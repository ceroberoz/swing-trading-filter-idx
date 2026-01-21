# Output Directory

Generated files from scans and backtests. Not tracked by git.

## Structure

```
output/
├── scans/      # Daily scan results (.txt)
├── backtests/  # Backtest reports (.txt)
└── charts/     # Performance charts (.png)
```

## Usage

```bash
# Save scan
python -m src.main --list lq45 > output/scans/scan_$(date +%Y%m%d).txt

# Save backtest
python -m src.main --backtest > output/backtests/backtest_$(date +%Y%m%d).txt
```

## Cleanup

```bash
# Delete files older than 30 days
find output/ -type f -mtime +30 -delete
```
