# Project: Swing Trading Filter (IDX)

## Objective
Develop a swing trading screener for the Indonesia Stock Market (IDX) to identify stocks with a high probability of yielding 5-10% profit on a weekly basis.

## Data Sources
*   **Primary:** Yahoo Finance (via `yfinance`).
*   **Secondary:** Google Finance or other credible sources if needed.

## Trading Strategy
### Core Logic
*   **Trend Identification:** Focus on EMA20 crossing above EMA50 (Golden Cross) as the primary signal.
*   **Optimization:** Evaluate supplementary indicators (RSI, MACD, Volume) to filter out false positives and improve win rate.

### Risk Management
*   **Take Profit (TP):** 5% - 10% (aligned with weekly targets).
*   **Stop Loss (SL):** 2% - 5% (to preserve capital).

## Technical Stack
*   Python (Pandas, yfinance, TA-Lib/pandas-ta).
*   CLI interface for execution.
