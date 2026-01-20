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

## 🔧 Recent Updates & Optimizations (January 2026)

The configuration has been optimized for the Indonesian market:

### Better Risk Management
- **Tighter Stop Losses** - Now 1.5x ATR instead of 2x, meaning smaller losses when trades go wrong
- **Realistic Profit Targets** - 3-10% range instead of 3-12%, more achievable for short-term swings
- **Conservative Exposure** - Maximum 60% invested (instead of 80%), keeps 40% cash ready for opportunities

### Faster Market Response
- **Market Regime Detection** - Updated to 13/50 EMA (from 20/100) for quicker bull/bear market signals
- This helps you avoid buying when the overall market is turning negative

### Broader Stock Universe
- **Lower Market Cap Filter** - Now includes stocks above 5 trillion IDR (was 10T)
- More quality mid-cap stocks added without including risky "gorengan"

### Accurate Cost Modeling
- **Commission Rate** - Updated to 0.15% (typical for IDX brokers like BCA Sekuritas, Mandiri Sekuritas)
- Better backtesting results that reflect real trading costs

### New Optional Filters (Disabled by Default)
You can now activate advanced filters in `src/config.py`:
- **Sector Filter** - Prefer banking/infrastructure, avoid mining/construction
- **Volatility Filter** - Skip stocks with >5% daily moves (avoid manipulated stocks)
- **Dividend Filter** - Focus on stocks paying 2%+ dividends (stable companies)
- **Market Cap Tiering** - Apply stricter rules to smaller companies

These features are designed to give you more control while keeping the default settings beginner-friendly and conservative.  

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
| **RSI** | Momentum indicator (0-100): <35 = oversold, >75 = overbought |
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

- **MIN_MARKET_CAP** - Minimum company size (default: 5 trillion IDR)
  - Filters out very small/risky stocks while including quality mid-caps
  - Lower value = more stocks to scan, higher = safer but fewer opportunities

- **FAST_EMA / SLOW_EMA** - Moving average periods for trend detection (default: 13/34)
  - Controls how quickly signals appear
  - Smaller numbers = more signals (faster), larger = fewer signals (more reliable)

- **RSI_PERIOD** - Momentum calculation period (default: 14)
  - RSI_OVERBOUGHT (default: 75) - Avoid buying when stock is too expensive
  - RSI_OVERSOLD (default: 35) - Find bargains when stock is undervalued

- **TARGET_PROFIT_PCT** - Your profit goal (default: 6%)
  - TARGET_PROFIT_MIN (default: 3%) - Minimum acceptable gain
  - TARGET_PROFIT_MAX (default: 10%) - Maximum realistic gain for 3-10 day swings
  - Smaller values = more frequent exits, larger = hold longer for bigger gains

- **STOP_LOSS_PCT** - Maximum acceptable loss (default: 3%)
  - ATR_MULTIPLIER (default: 1.5) - Dynamic stop loss based on volatility
  - Smaller value = cut losses faster (safer), larger = give more room (risky)

- **MARKET_FAST_EMA / MARKET_SLOW_EMA** - Market health detection (default: 13/50)
  - Monitors Jakarta Composite Index (^JKSE) trend
  - Helps avoid buying during bear markets
  - Faster periods (13/50) = respond quicker to market changes

- **RISK_PER_TRADE** - How much to risk per trade (default: 1%)
  - 1% means you only lose 1% of your account if stop loss is hit
  - Conservative traders: 0.5%, Aggressive traders: 2%

- **MAX_TOTAL_EXPOSURE** - Maximum money invested at once (default: 60%)
  - 60% means keeping 40% cash available for new opportunities
  - Lower = more conservative (safer), Higher = more aggressive (riskier)

### Advanced Optional Filters

These features are turned **OFF by default**. Edit `src/config.py` and set them to `True` to activate:

- **ENABLE_SECTOR_FILTER** - Prefer/avoid specific industries
  - Preferred: Banking, Infrastructure, Consumer, Telecom (stable, good trends)
  - Avoided: Mining, Construction (too volatile or cyclical)
  - Good for: Focusing on sectors you know or trust

- **ENABLE_VOLATILITY_FILTER** - Avoid excessive price swings
  - Max 5% daily movement allowed
  - Filters out manipulated or news-driven stocks
  - Good for: Avoiding unexpected sharp drops

- **ENABLE_DIVIDEND_FILTER** - Focus on income stocks
  - Minimum 2% dividend yield required
  - Targets stable, dividend-paying companies
  - Good for: Long-term wealth building with regular income

- **ENABLE_TIERED_FILTER** - Different rules for company sizes
  - Large cap (>50T): Most liquid, blue chip stocks
  - Mid cap (10-50T): Balanced liquidity and growth
  - Small cap (5-10T): More volatile but higher growth potential
  - Good for: Applying stricter rules to riskier stocks

## Key Features Explained

### 🔍 What the Tool Analyzes

1. **Trend Detection** - Uses moving averages (13/34 periods) to identify when prices start rising or falling
2. **Momentum** - RSI indicator shows if stock is overbought (too expensive, >75) or oversold (potential bargain, <35)
3. **Volume** - Requires 1.2x average trading volume to ensure signal quality
4. **Weekly Trend** - Checks longer timeframe (weekly EMA10/30) to confirm direction
5. **Market Condition** - Monitors Jakarta Composite Index (13/50 EMA) for overall market health
6. **Support/Resistance** - Identifies price levels where stock typically bounces or stalls

### 📊 Backtesting Features

- **Win Rate** - Percentage of profitable trades
- **Profit Factor** - Total profit divided by total loss (>1.5 is good)
- **Sharpe Ratio** - Risk-adjusted returns (>1.0 is acceptable)
- **Max Drawdown** - Worst peak-to-valley loss
- **Average Trade Duration** - Typical holding period

### 🛡️ Risk Management

- **Position Sizing** - Automatically calculates how much to invest per trade (1% account risk)
- **Stop Loss** - Uses ATR (Average True Range) - 1.5x the stock's typical daily movement
- **Take Profit** - Targets 3-10% gains based on market conditions
- **Market Cap Filter** - Skips stocks below 5 trillion IDR to avoid high-risk penny stocks (includes quality mid-caps)

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
