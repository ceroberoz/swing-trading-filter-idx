# Quick Start

Get up and running in 5 minutes.

## Setup

```bash
# Clone and enter project
git clone https://github.com/ceroberoz/swing-trading-filter-idx.git
cd swing-trading-filter-idx

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Daily Scanning

```bash
# Scan specific stocks
python -m src.main BBCA BBRI TLKM

# Scan LQ45 blue chips
python -m src.main --list lq45

# Scan all liquid stocks
python -m src.main --list idx_liquid

# See available watchlists
python -m src.main --show-lists
```

## Backtesting

```bash
# Basic backtest
python -m src.main --backtest BBCA BBRI

# Backtest with charts
python -m src.main --backtest --detailed --charts

# Custom date range
python -m src.main --backtest --start-date 2023-01-01 --end-date 2023-12-31
```

## Save Results

```bash
# Save scan to file
python -m src.main --list lq45 > output/scans/scan_$(date +%Y%m%d).txt

# Save backtest to file  
python -m src.main --backtest --list lq45 > output/backtests/backtest_$(date +%Y%m%d).txt
```

## Next Steps

- **Configure settings:** Edit `src/config.py` for stop-loss, profit targets, etc.
- **Create watchlists:** Add stocks to `watchlists/default.txt`
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
