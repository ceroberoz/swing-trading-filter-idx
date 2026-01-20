# Swing Trading Filter (IDX)

A CLI stock screener for Indonesia Stock Exchange (IDX) that helps identify swing trading opportunities.

## What It Does

- Scans IDX stocks for potential **buy/sell setups**
- Shows **support/resistance levels** for entry planning
- Provides **investment strategy recommendations** (BUY ALL, HOLD, SELL, etc.)
- Filters out small-cap "gorengan" stocks automatically

## Quick Start

```bash
# Install
git clone https://github.com/yourusername/swing-trading-filter-idx.git
cd swing-trading-filter-idx
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python -m src.main
```

## Usage

```bash
# Show crossover setups only (default)
python -m src.main

# Show ALL stocks from a watchlist
python -m src.main --list lq45
python -m src.main --list idx_liquid

# Scan specific stocks
python -m src.main BBCA BBRI ANTM

# List available watchlists
python -m src.main --show-lists
```

## Output

```
╒══════════╤════════════════════╤═════════╤═══════════╤═══════╤═══════════╤════════╤════════════╕
│ Ticker   │ Signal             │   Price │ S/R       │   RSI │ W.Trend   │ MCap   │ Strategy   │
╞══════════╪════════════════════╪═════════╪═══════════╪═══════╪═══════════╪════════╪════════════╡
│ BBCA.JK  │ BUY (STRONG)       │    8500 │ 8300/8700 │  55.2 │ UP        │ 992.1T │ BUY ALL    │
│ BBRI.JK  │ UPTREND (No Cross) │    4200 │ 4050/4350 │  62.1 │ UP        │ 585.0T │ HOLD       │
│ ANTM.JK  │ DOWNTREND          │    2100 │ 2000/2200 │  42.5 │ DOWN      │ 97.3T  │ SELL ALL   │
╘══════════╧════════════════════╧═════════╧═══════════╧═══════╧═══════════╧════════╧════════════╛
```

| Column | Meaning |
|--------|---------|
| **Signal** | BUY, UPTREND, DOWNTREND, or WAIT |
| **S/R** | Support / Resistance levels |
| **W.Trend** | Weekly trend (UP/DOWN) |
| **MCap** | Market capitalization |
| **Strategy** | BUY ALL, BUY PARTIAL, HOLD, SELL PARTIAL, SELL ALL |

## Watchlists

Edit files in `watchlists/` folder:
- `default.txt` - Your personal watchlist
- `lq45.txt` - LQ45 index stocks
- `idx_liquid.txt` - 100+ liquid IDX stocks

## Configuration

Edit `src/config.py` to customize:
- EMA periods, RSI thresholds
- Minimum market cap filter
- Profit targets and stop-loss

## ⚠️ DISCLAIMER

**FOR EDUCATIONAL PURPOSES ONLY.**

- This is NOT financial advice
- Always do your own research (DYOR)
- Never invest money you cannot afford to lose
- The authors are NOT responsible for any financial losses

## Credits

Built with assistance from:
- [Amp](https://ampcode.com) - AI coding agent
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) - Google Gemini AI

Data source: [Yahoo Finance](https://finance.yahoo.com)

## License

MIT License
