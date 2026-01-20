# Project Organization Guide

This guide explains how to keep your Swing Trading Filter (IDX) project organized and maintainable.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Directory Structure](#directory-structure)
3. [File Organization](#file-organization)
4. [Git Workflow](#git-workflow)
5. [Maintenance Tasks](#maintenance-tasks)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### After Fresh Clone/Setup

```bash
# 1. Navigate to project
cd swing-trading-filter-idx

# 2. Verify directory structure exists
ls -la

# Expected directories:
# - src/          (source code)
# - docs/         (documentation)
# - watchlists/   (stock lists)
# - output/       (generated files)
# - logs/         (application logs)
# - scripts/      (utility scripts)
# - cache/        (yfinance cache)

# 3. If any directories are missing, create them:
mkdir -p output/{scans,backtests,charts} logs scripts
```

### Daily Workflow

```bash
# Morning: Run scan and save results
TODAY=$(date +%Y%m%d)
python -m src.main --list lq45 > output/scans/lq45_scan_${TODAY}.txt

# Review results
cat output/scans/lq45_scan_${TODAY}.txt

# Weekly: Clean old files (optional)
./scripts/cleanup.sh
```

---

## Directory Structure

### Complete Tree

```
swing-trading-filter-idx/
│
├── src/                        # 📦 Source Code
│   ├── __init__.py
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration
│   ├── data.py                # Data fetching
│   ├── strategy.py            # Trading strategy
│   ├── rate_limiter.py        # API rate limiting
│   └── backtest/              # Backtesting engine
│       ├── __init__.py
│       ├── engine.py
│       ├── portfolio.py
│       ├── metrics.py
│       └── reports.py
│
├── docs/                       # 📚 Documentation
│   ├── DIRECTORY_STRUCTURE.md
│   ├── ORGANIZATION_GUIDE.md  # This file
│   ├── QUICK_START.md
│   ├── RATE_LIMIT_FIXES.md
│   ├── BACKTESTING_SUMMARY.md
│   └── GEMINI.md
│
├── watchlists/                 # 📊 Stock Lists
│   ├── default.txt            # Personal picks
│   ├── lq45.txt               # LQ45 blue chips
│   ├── idx_liquid.txt         # Liquid stocks
│   └── custom_*.txt           # Your custom lists
│
├── output/                     # 📁 Generated Files (not in git)
│   ├── README.md
│   ├── scans/                 # Daily scan results
│   │   └── .gitkeep
│   ├── backtests/             # Backtest reports
│   │   └── .gitkeep
│   └── charts/                # Generated charts
│       └── .gitkeep
│
├── logs/                       # 📝 Application Logs (not in git)
│   └── .gitkeep
│
├── scripts/                    # 🔧 Utility Scripts
│   ├── run_scanner.sh         # Daily scan automation
│   ├── cleanup.sh             # Maintenance script
│   └── todo.txt               # Development TODO
│
├── cache/                      # 💾 YFinance Cache (not in git)
│   ├── tkr-tz.db
│   └── cookies.db
│
├── venv/                       # 🐍 Virtual Environment (not in git)
│
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
└── .gitignore                 # Git ignore rules
```

### What Goes Where?

| Content Type | Directory | Tracked by Git? | Example |
|--------------|-----------|-----------------|---------|
| Python code | `src/` | ✅ Yes | `strategy.py` |
| Documentation | `docs/` | ✅ Yes | `QUICK_START.md` |
| Stock lists | `watchlists/` | ✅ Yes | `lq45.txt` |
| Scan results | `output/scans/` | ❌ No | `scan_20240115.txt` |
| Backtest reports | `output/backtests/` | ❌ No | `backtest_lq45.txt` |
| Charts | `output/charts/` | ❌ No | `equity_curve.png` |
| Logs | `logs/` | ❌ No | `scanner.log` |
| Scripts | `scripts/` | ✅ Yes | `cleanup.sh` |
| Cache | `cache/` | ❌ No | `tkr-tz.db` |

---

## File Organization

### Naming Conventions

#### Scan Results
```
# Pattern: {watchlist}_scan_{YYYYMMDD}.txt
lq45_scan_20240115.txt
banking_scan_20240115.txt
custom_scan_20240115.txt

# Special cases
morning_scan_20240115.txt       # Morning scan
afternoon_scan_20240115.txt     # Afternoon update
```

#### Backtest Results
```
# Pattern: backtest_{watchlist}_{YYYYMMDD}.txt
backtest_lq45_20240115.txt
backtest_BBCA_20240115.txt

# Detailed reports
backtest_detailed_20240115.txt
backtest_summary_2024Q1.txt
```

#### Charts
```
# Pattern: {chart_type}_{YYYYMMDD}.png
backtest_performance_20240115.png
equity_curve_20240115.png
monthly_returns_20240115.png
```

#### Logs
```
# Pattern: {component}_{YYYYMMDD}.log
scanner_20240115.log
backtest_20240115.log
error_20240115.log
```

### File Organization Tips

1. **Always use dates** - Makes sorting and archiving easy
2. **Be descriptive** - Include watchlist name or purpose
3. **Use consistent patterns** - Easier to write scripts
4. **Separate by type** - Keep scans, backtests, and charts in their own directories

---

## Git Workflow

### What to Commit

✅ **DO commit:**
- Source code changes (`src/`)
- Documentation updates (`docs/`, `README.md`)
- New watchlists (`watchlists/`)
- Utility scripts (`scripts/`)
- Configuration changes (`src/config.py`)
- Requirements updates (`requirements.txt`)

❌ **DON'T commit:**
- Output files (`output/`)
- Log files (`logs/`)
- Cache files (`cache/`)
- Virtual environment (`venv/`)
- Personal API keys (`.env`)
- IDE settings (`.vscode/`, `.idea/`)
- AI tool files (`.agents/`, `.cursor/`)

### Typical Workflow

```bash
# 1. Check what changed
git status

# 2. Stage changes
git add src/strategy.py          # Specific files
git add docs/                    # Entire directory
git add watchlists/my_picks.txt  # New watchlist

# 3. Commit with meaningful message
git commit -m "Optimize EMA crossover strategy for IDX volatility"

# 4. Push to remote
git push origin main
```

### Good Commit Messages

```bash
# ✅ Good
git commit -m "Add support/resistance analysis to strategy"
git commit -m "Fix rate limiter batch chunking issue"
git commit -m "Update LQ45 watchlist for 2024"
git commit -m "Add comprehensive cleanup script"

# ❌ Bad
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### Branches (Optional)

```bash
# Create feature branch
git checkout -b feature/add-macd-filter

# Work on feature
git add src/strategy.py
git commit -m "Add MACD histogram filter"

# Merge back to main
git checkout main
git merge feature/add-macd-filter

# Delete feature branch
git branch -d feature/add-macd-filter
```

---

## Maintenance Tasks

### Daily

```bash
# Run scan and save results
TODAY=$(date +%Y%m%d)
python -m src.main --list lq45 > output/scans/lq45_scan_${TODAY}.txt

# Check for errors in logs (if logging enabled)
tail -f logs/scanner.log
```

### Weekly

```bash
# Clean old files (>30 days)
./scripts/cleanup.sh

# Or manually:
find output/scans/ -name "*.txt" -mtime +30 -delete
find logs/ -name "*.log" -mtime +30 -delete

# Archive important backtest results
mkdir -p output/archive/$(date +%Y)Q$(( ($(date +%-m)-1)/3 + 1 ))
cp output/backtests/*summary* output/archive/$(date +%Y)Q$(( ($(date +%-m)-1)/3 + 1 ))/
```

### Monthly

```bash
# Full cleanup
./scripts/cleanup.sh  # Option 7: Clean all

# Update watchlists if needed
vim watchlists/lq45.txt

# Commit changes
git add watchlists/
git commit -m "Update watchlists for $(date +%B)"
git push
```

### Quarterly

```bash
# Run comprehensive backtest
python -m src.main --backtest --detailed --charts --list idx_liquid > \
  output/backtests/quarterly_backtest_$(date +%Y)Q$(( ($(date +%-m)-1)/3 + 1 )).txt

# Archive quarter results
QUARTER=$(date +%Y)Q$(( ($(date +%-m)-1)/3 + 1 ))
mkdir -p output/archive/$QUARTER
cp output/backtests/*summary* output/archive/$QUARTER/
cp output/charts/*performance* output/archive/$QUARTER/

# Review and document performance
echo "Q1 2024 Performance Summary" > output/archive/$QUARTER/README.md
```

---

## Best Practices

### 1. Use Version Control Effectively

```bash
# Commit often with clear messages
git commit -m "Fix: Rate limiter timeout handling"

# Use .gitignore properly (already configured)
# Never commit secrets or generated files

# Create tags for releases
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

### 2. Keep Documentation Updated

```bash
# When adding features, update docs
vim docs/QUICK_START.md

# Update README for major changes
vim README.md

# Document configuration changes
vim docs/RATE_LIMIT_FIXES.md
```

### 3. Organize Output Files

```bash
# Use consistent naming
TODAY=$(date +%Y%m%d)
WATCHLIST="lq45"

# Save with proper names
python -m src.main --list $WATCHLIST > \
  output/scans/${WATCHLIST}_scan_${TODAY}.txt

# Archive monthly
mkdir -p output/archive/$(date +%Y%m)
mv output/scans/*$(date +%Y%m)*.txt output/archive/$(date +%Y%m)/
```

### 4. Clean Regularly

```bash
# Set up weekly cleanup (cron job)
# Edit crontab: crontab -e
# Add line:
0 2 * * 0 cd /path/to/swing-trading-filter-idx && ./scripts/cleanup.sh

# Or run manually
./scripts/cleanup.sh
```

### 5. Backup Important Data

```bash
# Backup watchlists
cp -r watchlists/ ~/backups/watchlists_$(date +%Y%m%d)/

# Backup important backtest results
cp output/backtests/*summary* ~/backups/

# Backup entire project (excluding venv)
tar -czf ~/backups/swing-trading-$(date +%Y%m%d).tar.gz \
  --exclude=venv --exclude=cache --exclude=output \
  swing-trading-filter-idx/
```

### 6. Monitor Disk Space

```bash
# Check sizes
du -sh output/
du -sh logs/
du -sh cache/

# Find large files
find output/ -type f -size +10M

# Clean if needed
./scripts/cleanup.sh  # Option 9: Show disk usage
```

---

## Troubleshooting

### "Directory not found" errors

```bash
# Create missing directories
mkdir -p output/{scans,backtests,charts}
mkdir -p logs
mkdir -p scripts

# Verify structure
ls -la
```

### Git tracking unwanted files

```bash
# Remove from git but keep local
git rm --cached output/scans/*.txt
git rm --cached logs/*.log

# Verify .gitignore is working
git status  # Should not show output/ or logs/
```

### Disk space issues

```bash
# Check usage
du -sh output/ logs/ cache/

# Clean old files
find output/ -type f -mtime +30 -delete
find logs/ -type f -mtime +30 -delete

# Clean cache
rm -rf cache/*.db*  # Will regenerate on next run
```

### Lost scan results

```bash
# Check output directory
ls -lt output/scans/ | head -n 10

# Check if accidentally deleted
# Restore from backup if available
cp ~/backups/output/scans/*.txt output/scans/
```

### Merge conflicts

```bash
# If you have conflicts in config or code
git status  # See conflicted files

# Edit files to resolve conflicts
vim src/config.py  # Remove conflict markers

# Mark as resolved
git add src/config.py
git commit -m "Resolve config merge conflict"
```

---

## Quick Reference

### Common Commands

```bash
# Daily scan with save
python -m src.main --list lq45 > output/scans/scan_$(date +%Y%m%d).txt

# Weekly cleanup
./scripts/cleanup.sh

# Check disk usage
du -sh output/ logs/ cache/

# Git commit workflow
git add .
git commit -m "Description of changes"
git push

# Find recent scans
ls -lt output/scans/ | head -n 5

# Archive old files
mkdir -p output/archive/$(date +%Y%m)
mv output/scans/*old* output/archive/$(date +%Y%m)/
```

### Directory Quick Access

```bash
# Jump to directories
cd src/              # Source code
cd docs/             # Documentation
cd output/scans/     # Scan results
cd watchlists/       # Stock lists
cd scripts/          # Utility scripts

# View structure
tree -L 2 -I 'venv|__pycache__'  # If tree is installed
# Or:
find . -maxdepth 2 -type d | grep -v venv | sort
```

### File Patterns

```bash
# Find all scans from January 2024
find output/scans/ -name "*202401*.txt"

# Find all backtest summaries
find output/backtests/ -name "*summary*.txt"

# Find large files (>1MB)
find output/ -type f -size +1M

# Count files by directory
find output/scans/ -type f | wc -l
find output/backtests/ -type f | wc -l
```

---

## Summary Checklist

### Setup (One-time)
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Verify directory structure
- [ ] Configure watchlists

### Daily
- [ ] Run morning scan
- [ ] Save results to `output/scans/`
- [ ] Review signals and setups

### Weekly
- [ ] Run cleanup script
- [ ] Archive important results
- [ ] Commit code changes

### Monthly
- [ ] Full cleanup of old files
- [ ] Update watchlists if needed
- [ ] Review monthly performance

### Quarterly
- [ ] Comprehensive backtest
- [ ] Archive quarter results
- [ ] Document strategy performance
- [ ] Backup important data

---

## Additional Resources

- **Main Documentation**: `README.md`
- **Directory Structure**: `docs/DIRECTORY_STRUCTURE.md`
- **Quick Start**: `docs/QUICK_START.md`
- **Rate Limiting**: `docs/RATE_LIMIT_FIXES.md`
- **Backtesting**: `docs/BACKTESTING_SUMMARY.md`

---

**Last Updated:** January 2024  
**Maintained By:** Project Contributors

Keep your project organized and your trading systematic! 📊