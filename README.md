# Swing Trading Filter (IDX)

Find profitable stock trading opportunities in the Indonesia Stock Exchange (IDX).

## What It Does

- **Scans stocks** for buy/sell opportunities based on price trends
- **Shows key price levels** (support/resistance) for entry/exit
- **Gives clear recommendations** - BUY ALL, HOLD, SELL, etc.
- **Tests strategies** on historical data (backtesting)
- **Filters out risky stocks** automatically

## Installation

```bash
git clone https://github.com/ceroberoz/swing-trading-filter-idx.git
cd swing-trading-filter-idx
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Daily Scanning

```bash
# Scan specific stocks
python -m src.main BBCA BBRI TLKM

# Scan LQ45 blue chips (~2.5 min)
python -m src.main --list lq45

# See all watchlists
python -m src.main --show-lists
```

### Backtesting

```bash
# Test strategy on historical data
python -m src.main --backtest BBCA BBRI

# Full backtest with charts
python -m src.main --backtest --detailed --charts
```

## Understanding the Output

```
╒══════════╤════════════════════╤═════════╤═══════════╤═══════╤═══════════╤════════╤════════════╕
│ Ticker   │ Signal             │   Price │ S/R       │   RSI │ W.Trend   │ MCap   │ Strategy   │
╞══════════╪════════════════════╪═════════╪═══════════╪═══════╪═══════════╪════════╪════════════╡
│ BBCA.JK  │ BUY (STRONG)       │    8500 │ 8300/8700 │  55.2 │ UP        │ 992.1T │ BUY ALL    │
│ ANTM.JK  │ DOWNTREND          │    2100 │ 2000/2200 │  42.5 │ DOWN      │ 97.3T  │ SELL ALL   │
╘══════════╧════════════════════╧═════════╧═══════════╧═══════╧═══════════╧════════╧════════════╛
```

| Column | Meaning |
|--------|---------|
| **Signal** | BUY (STRONG/WEAK), UPTREND, DOWNTREND, WAIT |
| **Price** | Current price (IDR) |
| **S/R** | Support/Resistance levels |
| **RSI** | Momentum (0-100): <35 oversold, >75 overbought |
| **W.Trend** | Weekly trend (UP/DOWN) |
| **MCap** | Market cap in trillions IDR |
| **Strategy** | Action: BUY ALL, HOLD, SELL ALL, etc. |

## Configuration

Edit `src/config.py` to customize:

| Setting | Default | What It Does |
|---------|---------|--------------|
| `MIN_MARKET_CAP` | 5T IDR | Filter out small stocks |
| `FAST_EMA / SLOW_EMA` | 13/34 | Trend detection speed |
| `TARGET_PROFIT_PCT` | 6% | Your profit goal |
| `STOP_LOSS_PCT` | 3% | Maximum loss per trade |
| `MAX_TOTAL_EXPOSURE` | 60% | Max money invested at once |

### Optional Filters (disabled by default)

Set to `True` in `src/config.py` to enable:

- `ENABLE_SECTOR_FILTER` - Prefer banking/infrastructure, avoid mining
- `ENABLE_VOLATILITY_FILTER` - Skip stocks with >5% daily moves
- `ENABLE_DIVIDEND_FILTER` - Focus on 2%+ dividend stocks

## Project Structure

```
swing-trading-filter-idx/
├── src/                # Python source code
├── watchlists/         # Stock lists (lq45.txt, idx_liquid.txt)
├── output/             # Generated scan results and charts
├── docs/               # Documentation
├── scripts/            # Utility scripts
└── README.md           # This file
```

## Troubleshooting

**Rate limited?** Use smaller watchlists or disable `ENABLE_MCAP_FILTER` in config.

**Missing module?** Run `pip install -r requirements.txt`

**Wrong ticker?** IDX stocks need `.JK` suffix (e.g., `BBCA.JK`)

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more help.

## Glossary

- **EMA** - Exponential Moving Average (trend line)
- **RSI** - Relative Strength Index (overbought/oversold indicator)
- **ATR** - Average True Range (daily price movement)
- **Golden Cross** - Short-term EMA crosses above long-term EMA (buy signal)
- **DYOR** - Do Your Own Research

## Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY.** This is NOT financial advice. Past performance does NOT guarantee future results. Only invest money you can afford to lose.

## License

MIT License - Free to use and modify.

---

**Happy Trading! 📈**
