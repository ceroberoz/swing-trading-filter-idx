# Project Context: Swing Trading Filter (IDX)

## Current Status (2026-01-21)
We are in the process of upgrading the trading strategy to "Phase 1: Better Entry/Exit".

### Completed Features
1.  **Momentum & Trend Slopes:**
    -   Modified `src/strategy.py` to calculate slopes for MACD, RSI, and EMA Spread.
    -   Investment scoring now rewards positive momentum (rising MACD/RSI) and penalizes fading momentum.
2.  **Candlestick Pattern Recognition:**
    -   Created `src/patterns.py` to detect Doji, Hammer, Shooting Star, Bullish/Bearish Engulfing.
    -   Integrated into `src/strategy.py`:
        -   Bullish patterns add +1 to score.
        -   Bearish patterns subtract -1 (or -2 for strong reversals).

### Pending Tasks (Phase 1)
1.  **Trailing Stop Loss:**
    -   Logic: Implement a trailing stop that moves up as the price moves up, locking in profits.
    -   Target File: `src/backtest/engine.py` (execution) and `src/strategy.py` (calculation).
    -   *Status*: Not started.

### Architecture Notes
-   **Strategy Engine**: `src/strategy.py` is the core. It returns a dictionary `base_analysis`.
-   **Scoring**: `get_investment_strategy` converts signals + indicators + patterns into a final decision (BUY ALL, BUY PARTIAL, HOLD, SELL).
-   **Configuration**: `src/config.py` holds all constants (EMA periods, RSI thresholds).

### How to Continue
-   Next agent should start by implementing the **Trailing Stop Loss**.
-   Check `src/strategy.py` for `calculate_atr` which is currently used for static stops.
