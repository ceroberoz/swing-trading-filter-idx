# Swing Trading Filter (IDX)

A beginner-friendly tool to find profitable stock trading opportunities in the Indonesia Stock Exchange (IDX).

## What is Swing Trading?

Swing trading means holding stocks for **3-10 days** to capture short-term price movements. Unlike day trading (buying and selling within hours) or long-term investing (holding for years), swing trading aims for quick 5-10% profits within a week.

## What This Tool Does

✅ **Scans stocks** for buy/sell opportunities based on price trends  
✅ **Shows key price levels** where you should enter or exit  
✅ **Gives clear recommendations** - BUY ALL, HOLD, SELL, etc.  
✅ **Tests strategies** on historical data to see what works  
✅ **Filters out risky stocks** - skips very small or illiquid stocks automatically  

## Installation

```bash
# 1. Download the project
git clone https://github.com/ceroberoz/swing-trading-filter-idx.git
cd swing-trading-filter-idx

# 2. Create isolated environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt
```

## Basic Usage

### Daily Stock Scanning

```bash
# Find stocks with buy signals today
python -m src.main

# Scan specific stocks (e.g., Bank BCA, Bank BRI, Antam)
python -m src.main BBCA BBRI ANTM

# Use a pre-made watchlist
python -m src.main --list lq45           # Blue chip stocks
python -m src.main --list idx_liquid     # 100+ liquid stocks

# See all available watchlists
python -m src.main --show-lists
```

### Testing Your Strategy (Backtesting)

```bash
# Test strategy on 2022-2024 data
python -m src.main --backtest

# Test specific stocks
python -m src.main --backtest BBCA BBRI ANTM

# Test with custom date range
python -m src.main --backtest --start-date 2023-01-01 --end-date 2023-12-31

# Get detailed results with charts
python -m src.main --backtest --detailed --charts
```

## Understanding the Output

```
╒══════════╤════════════════════╤═════════╤═══════════╤═══════╤═══════════╤════════╤════════════╕
│ Ticker   │ Signal             │   Price │ S/R       │   RSI │ W.Trend   │ MCap   │ Strategy   │
╞══════════╪════════════════════╪═════════╪═══════════╪═══════╪═══════════╪════════╪════════════╡
│ BBCA.JK  │ BUY (STRONG)       │    8500 │ 8300/8700 │  55.2 │ UP        │ 992.1T │ BUY ALL    │
│ BBRI.JK  │ UPTREND (No Cross) │    4200 │ 4050/4350 │  62.1 │ UP        │ 585.0T │ HOLD       │
│ ANTM.JK  │ DOWNTREND          │    2100 │ 2000/2200 │  42.5 │ DOWN      │ 97.3T  │ SELL ALL   │
╘══════════╧════════════════════╧═════════╧═══════════╧═══════╧═══════════╧════════╧════════════╛
```

### Column Explanations

| Column | What It Means |
|--------|---------------|
| **Ticker** | Stock code (e.g., BBCA.JK = Bank BCA) |
| **Signal** | Trading signal based on trend analysis |
| **Price** | Current stock price (in IDR) |
| **S/R** | Support/Resistance - key price levels to watch |
| **RSI** | Momentum indicator (0-100): <30 = oversold, >70 = overbought |
| **W.Trend** | Weekly trend direction (UP or DOWN) |
| **MCap** | Market capitalization - company size (in trillions IDR) |
| **Strategy** | Recommended action based on all factors |

### Signal Types

- **BUY (STRONG)** - Strong uptrend starting, good entry point
- **BUY (WEAK)** - Uptrend but weaker confirmation, be cautious
- **UPTREND (No Cross)** - Already rising but no new signal today
- **DOWNTREND** - Price falling, avoid or exit positions
- **WAIT** - No clear direction, stay on sidelines

### Strategy Recommendations

- **BUY ALL** - All indicators positive, use full position size
- **BUY PARTIAL** - Mixed signals, use 50% position size
- **HOLD** - Keep existing position, no action needed
- **SELL PARTIAL** - Take some profits, reduce exposure
- **SELL ALL** - Exit completely, preserve capital

## Customizing Watchlists

Edit text files in the `watchlists/` folder:

- **default.txt** - Your personal stock picks
- **lq45.txt** - Indonesia's 45 most liquid stocks
- **idx_liquid.txt** - 100+ actively traded stocks

Simply add stock tickers (e.g., BBCA.JK, TLKM.JK) one per line.

## Adjusting Settings

Edit `src/config.py` to customize:

- **MIN_MARKET_CAP** - Minimum company size (default: 10 trillion IDR)
- **EMA_SHORT / EMA_LONG** - Moving average periods for trend detection
- **RSI_PERIOD** - Momentum calculation period
- **PROFIT_TARGET_PCT** - Your profit goal (default: 5-10%)
- **STOP_LOSS_PCT** - Maximum acceptable loss (default: 2-5%)

## Key Features Explained

### 🔍 What the Tool Analyzes

1. **Trend Detection** - Uses moving averages (13/34 periods) to identify when prices start rising or falling
2. **Momentum** - RSI indicator shows if stock is overbought (too expensive) or oversold (potential bargain)
3. **Volume** - Requires 1.2x average trading volume to ensure signal quality
4. **Weekly Trend** - Checks longer timeframe to confirm direction
5. **Market Condition** - Monitors Jakarta Composite Index for overall market health
6. **Support/Resistance** - Identifies price levels where stock typically bounces or stalls

### 📊 Backtesting Features

- **Win Rate** - Percentage of profitable trades
- **Profit Factor** - Total profit divided by total loss (>1.5 is good)
- **Sharpe Ratio** - Risk-adjusted returns (>1.0 is acceptable)
- **Max Drawdown** - Worst peak-to-valley loss
- **Average Trade Duration** - Typical holding period

### 🛡️ Risk Management

- **Position Sizing** - Automatically calculates how much to invest per trade (1% account risk)
- **Stop Loss** - Uses ATR (Average True Range) - 2x the stock's typical daily movement
- **Take Profit** - Targets 3-12% gains based on market conditions
- **Market Cap Filter** - Skips stocks below 10 trillion IDR to avoid high-risk penny stocks

## Glossary

- **EMA** (Exponential Moving Average) - Trend line that gives more weight to recent prices
- **RSI** (Relative Strength Index) - Measures if stock is overbought or oversold (0-100 scale)
- **ATR** (Average True Range) - Measures how much a stock typically moves per day
- **Pivot Points** - Price levels calculated from previous day's high/low/close
- **Golden Cross** - When short-term average crosses above long-term average (bullish signal)
- **MCap** (Market Capitalization) - Total company value (stock price × shares outstanding)
- **DYOR** (Do Your Own Research) - Always verify before making decisions

## Example Workflow

1. **Morning Scan** (9:00 AM) - Run `python -m src.main` to find opportunities
2. **Review Signals** - Check stocks with BUY (STRONG) signal
3. **Verify Charts** - Look at price near support level, RSI not overbought
4. **Check Weekly Trend** - Confirm W.Trend shows "UP"
5. **Place Order** - Enter at market open or at support level
6. **Set Stop Loss** - Place below support level shown in S/R column
7. **Monitor Daily** - Re-run tool to check if signal changes
8. **Exit** - Sell when profit target hit or stop loss triggered

## ⚠️ IMPORTANT DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY.**

- ❌ This is **NOT financial advice**
- ❌ Past performance does **NOT guarantee future results**
- ❌ The creators are **NOT responsible** for any trading losses
- ✅ Always do your own research (DYOR)
- ✅ Only invest money you can afford to lose
- ✅ Consider consulting a licensed financial advisor
- ✅ Understand that all trading involves risk

**Use at your own risk. You are solely responsible for your investment decisions.**

## Troubleshooting

### "No module named 'yfinance'"
Run `pip install -r requirements.txt` to install dependencies.

### "No data found for ticker"
Stock ticker may be incorrect. IDX stocks need `.JK` suffix (e.g., BBCA.JK not BBCA).

### "Empty watchlist"
Make sure watchlist file exists in `watchlists/` folder and contains valid tickers.

### Charts not showing
Install matplotlib: `pip install matplotlib seaborn`

## Data Source

All market data comes from [Yahoo Finance](https://finance.yahoo.com) via the `yfinance` Python library. Data is free but may have delays or occasional gaps.

## Contributing

Found a bug? Have a feature request? Open an issue or submit a pull request on GitHub.

## Credits

Built with assistance from AI coding tools:
- **Amp** (ampcode.com) - AI coding agent
- **Google Gemini** - AI assistant
- **OpenCode** (opencode.ai) - AI development platform

## License

MIT License - Free to use, modify, and distribute with attribution.

---

**Happy Trading! 📈 Remember: The best trade is the one you don't take when conditions aren't right.**
