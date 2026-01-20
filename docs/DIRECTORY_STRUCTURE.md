# Directory Structure

This document describes the organization of the Swing Trading Filter (IDX) project.

## Overview

```
swing-trading-filter-idx/
├── src/                    # Source code
├── docs/                   # Documentation
├── watchlists/             # Stock watchlists
├── output/                 # Generated outputs
├── logs/                   # Application logs
├── scripts/                # Utility scripts
├── cache/                  # Cached data (yfinance)
├── venv/                   # Virtual environment (ignored by git)
└── tests/                  # Unit tests (future)
```

## Detailed Structure

### 📁 Root Directory

```
swing-trading-filter-idx/
├── README.md              # Main project documentation
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── .git/                 # Git repository (hidden)
```

### 📂 `src/` - Source Code

Main application code organized by functionality.

```
src/
├── __init__.py           # Package initializer
├── main.py               # Entry point - CLI interface
├── config.py             # Configuration settings
├── data.py               # Data fetching (Yahoo Finance API)
├── strategy.py           # Trading strategy logic
├── rate_limiter.py       # API rate limiting
└── backtest/             # Backtesting engine
    ├── __init__.py       # Backtest package initializer
    ├── engine.py         # Main backtesting engine
    ├── portfolio.py      # Portfolio management
    ├── metrics.py        # Performance metrics
    └── reports.py        # Report generation
```

**Key Files:**
- **main.py**: Command-line interface, orchestrates scanning and backtesting
- **config.py**: All configuration parameters (EMAs, RSI, rate limits, etc.)
- **data.py**: Fetches historical data and stock info from Yahoo Finance
- **strategy.py**: Implements EMA crossover strategy and technical analysis
- **rate_limiter.py**: Prevents Yahoo Finance API rate limiting
- **backtest/**: Complete backtesting framework with portfolio tracking

### 📚 `docs/` - Documentation

All documentation files are organized here.

```
docs/
├── DIRECTORY_STRUCTURE.md    # This file
├── QUICK_START.md           # Quick start guide for users
├── RATE_LIMIT_FIXES.md      # Rate limit implementation details
├── BACKTESTING_SUMMARY.md   # Backtesting guide
├── GEMINI.md                # Project objectives and strategy
└── API_REFERENCE.md         # Code API documentation (future)
```

**Purpose:**
- Keeps documentation separate from code
- Easy to navigate and maintain
- Can be built into static site (e.g., MkDocs)

### 📊 `watchlists/` - Stock Watchlists

Pre-configured stock lists for scanning.

```
watchlists/
├── default.txt              # Your personal picks (2 stocks)
├── lq45.txt                # LQ45 blue chip stocks (47 stocks)
├── idx_liquid.txt          # IDX liquid stocks (130 stocks)
└── custom_*.txt            # Your custom watchlists
```

**Format:**
```
# Comments start with #
BBCA.JK
BBRI.JK
TLKM.JK
# One ticker per line
```

**Usage:**
```bash
python -m src.main --list lq45           # Scan LQ45
python -m src.main --list custom_banking # Scan custom list
```

### 📁 `output/` - Generated Outputs

All generated files from scans, backtests, and analysis.

```
output/
├── scans/                   # Daily scan results
│   ├── .gitkeep            # Directory placeholder with README
│   ├── scan_20240115.txt   # Daily scan output
│   └── lq45_scan_*.txt     # Watchlist-specific scans
│
├── backtests/              # Backtest results
│   ├── .gitkeep            # Directory placeholder with README
│   ├── backtest_lq45_*.txt # Backtest reports
│   ├── detailed_*.txt      # Detailed trade logs
│   └── summary_*.json      # JSON format results
│
└── charts/                 # Generated charts
    ├── .gitkeep            # Directory placeholder with README
    ├── backtest_performance.png
    ├── equity_curve_*.png
    └── monthly_returns_*.png
```

**Notes:**
- All files in `output/` are ignored by git (except `.gitkeep` files)
- Organize by date: `YYYYMMDD` format
- Clean old files periodically (keep last 30-90 days)

### 📝 `logs/` - Application Logs

Runtime logs for debugging and monitoring.

```
logs/
├── .gitkeep                # Directory placeholder with README
├── scanner.log             # Daily scanner logs
├── backtest.log            # Backtesting logs
├── error.log               # Error traces
├── api_calls.log           # API request/response logs
└── rate_limiter.log        # Rate limiting events
```

**Log Rotation:**
- Keep last 30 days
- Rotate daily or weekly
- Archive old logs: `logs/archive/2024/`

**All log files are ignored by git.**

### 🔧 `scripts/` - Utility Scripts

Helper scripts for automation and maintenance.

```
scripts/
├── run_scanner.sh          # Shell script to run daily scans
├── todo.txt                # Development TODO list
├── update_watchlists.py    # Update watchlist data (future)
├── cleanup_old_files.sh    # Clean old output files (future)
└── setup_cron.sh           # Setup cron jobs (future)
```

**Usage:**
```bash
# Run daily scan
./scripts/run_scanner.sh

# Make executable
chmod +x scripts/*.sh
```

### 💾 `cache/` - Cached Data

YFinance timezone and cookie cache.

```
cache/
├── tkr-tz.db              # Ticker timezone database
├── tkr-tz.db-shm          # Shared memory file
├── tkr-tz.db-wal          # Write-ahead log
├── cookies.db             # Session cookies
└── *.db-*                 # Other cache files
```

**Notes:**
- Automatically created by `yfinance` library
- Safe to delete if corrupted (will regenerate)
- All cache files are ignored by git
- Improves performance by caching timezone data

### 🧪 `tests/` - Unit Tests (Future)

Unit tests and integration tests.

```
tests/
├── __init__.py
├── test_data.py           # Test data fetching
├── test_strategy.py       # Test strategy logic
├── test_backtest.py       # Test backtesting engine
├── test_rate_limiter.py   # Test rate limiter
└── fixtures/              # Test data fixtures
    └── sample_data.csv
```

**Run Tests:**
```bash
pytest tests/
pytest tests/test_strategy.py -v
```

### 🔒 Ignored by Git

The following directories/files are ignored by `.gitignore`:

**System & Environment:**
- `venv/`, `.venv/`, `env/` - Virtual environments
- `__pycache__/`, `*.pyc` - Python bytecode
- `.DS_Store`, `Thumbs.db` - OS files

**AI Tools:**
- `.agents/` - Amp agent files
- `.opencode/` - OpenCode files
- `.cursor/`, `.copilot/` - AI assistant files
- `.continue/`, `.aider/` - AI coding tools

**Generated Files:**
- `output/` - All output files
- `logs/` - All log files
- `cache/` - All cache files
- `*.png`, `*.csv`, `*.json` - Generated data files

**Secrets:**
- `.env`, `.env.local` - Environment variables
- `*.pem`, `*.key` - Certificates and keys
- `secrets.json`, `credentials.json` - API keys

## File Naming Conventions

### Scan Results
```
scan_YYYYMMDD.txt              # Generic daily scan
lq45_scan_YYYYMMDD.txt         # LQ45 watchlist scan
banking_scan_YYYYMMDD.txt      # Sector-specific scan
```

### Backtest Results
```
backtest_lq45_YYYYMMDD.txt           # Backtest report
backtest_detailed_YYYYMMDD.txt       # Detailed trades
backtest_summary_2024Q1.json         # Quarterly summary
```

### Charts
```
backtest_performance_YYYYMMDD.png    # Performance chart
equity_curve_YYYYMMDD.png            # Equity curve
monthly_returns_YYYYMMDD.png         # Monthly returns
```

### Logs
```
scanner_YYYYMMDD.log           # Daily scanner log
error_YYYYMMDD.log             # Daily error log
```

## Best Practices

### 1. Keep It Organized
- Save scan results to `output/scans/` with dates
- Archive backtests in `output/backtests/`
- Check logs in `logs/` when troubleshooting

### 2. Clean Up Regularly
```bash
# Delete scans older than 30 days
find output/scans/ -name "*.txt" -mtime +30 -delete

# Delete logs older than 30 days
find logs/ -name "*.log" -mtime +30 -delete

# Clean cache if corrupted
rm -rf cache/*.db*
```

### 3. Backup Important Data
```bash
# Backup watchlists
cp -r watchlists/ watchlists_backup/

# Backup important backtest results
cp output/backtests/backtest_summary_2024.txt ~/backups/
```

### 4. Version Control
- Commit code changes in `src/`
- Commit watchlist changes in `watchlists/`
- Commit documentation changes in `docs/`
- **Do NOT commit**: `output/`, `logs/`, `cache/`, `.env`

### 5. Documentation
- Update `docs/` when adding features
- Keep `README.md` up to date
- Document configuration changes in `docs/`

## Quick Reference

| Task | Command |
|------|---------|
| Run scan | `python -m src.main --list lq45` |
| Save scan | `python -m src.main --list lq45 > output/scans/scan_$(date +%Y%m%d).txt` |
| Run backtest | `python -m src.main --backtest --list lq45` |
| Save backtest | `python -m src.main --backtest > output/backtests/backtest_$(date +%Y%m%d).txt` |
| View logs | `tail -f logs/scanner.log` |
| Clean cache | `rm -rf cache/*.db*` |

## Migration from Old Structure

If you have files in the old structure, move them:

```bash
# Move documentation
mv *.md docs/  # except README.md and LICENSE

# Move scripts
mv *.sh scripts/
mv todo.txt scripts/

# Create output directories
mkdir -p output/{scans,backtests,charts}
mkdir -p logs

# Move old results
mv scan_*.txt output/scans/
mv backtest_*.txt output/backtests/
mv *.png output/charts/
```

## Summary

✅ **Organized structure** - Easy to navigate and maintain  
✅ **Separation of concerns** - Code, docs, data, outputs are separate  
✅ **Git-friendly** - Ignores generated files and secrets  
✅ **Scalable** - Room for growth (tests, more docs, more scripts)  
✅ **AI-tool compatible** - Ignores AI assistant artifacts  

**Next Steps:**
1. Review the structure and create any missing directories
2. Move files to appropriate locations
3. Update your scripts to use new paths
4. Add more watchlists in `watchlists/`
5. Write unit tests in `tests/` (future)

---

**Last Updated:** January 2024  
**Maintained By:** Project Contributors