# Algorithmic Trading System (XT Futures Bot)

A modular, event-driven algorithmic trading system designed for automated futures trading on XT Exchange.  
The system integrates TradingView Pine Script signals, a backend execution engine, and real-time notification delivery.

---

## Overview

This project is a fully automated trading pipeline that:

- Receives trading signals from Pine Script (TradingView webhook)
- Processes and normalizes signals in a handler layer
- Executes futures trades on XT Exchange via API
- Manages open positions, leverage, take-profit orders, and risk exposure
- Sends real-time notifications to Telegram or external webhook services

The architecture is designed for **scalability, modularity, and production-level reliability**.

---

## System Architecture


Pine Script (TradingView)
↓
Webhook / Signal Handler
↓
Execution Engine (XT Futures API)
↓
Order Management (Position, TP, SL, Leverage)
↓
Notification Service (Telegram / Webhook)


---

## Project Structure


algorithmic-trading-system/
│
├── execution_engine/
│ └── xt_futures_executor.py # Core XT Futures API wrapper & order execution
│
├── notification/
│ └── telegram_notifier.py # Sends trading alerts and system notifications
│
├── pine_script/
│ └── strategy.pine # TradingView strategy & signal generator
│
├── signal_handler.py # Webhook entry point (Pipedream / serverless)
├── config.py # API keys and system configuration
├── utils.py # Helper functions
└── main.py # Optional entry point for local execution


---

## Key Features

### Trading Engine
- Market order execution (long/short)
- Position closing automation
- Leverage adjustment per symbol
- Take-profit order management (multi-target support)

### Market Data Access
- Order book (depth)
- Mark price and ticker data
- Funding rate and contract information
- K-line (candlestick) historical data

### Risk & Position Management
- Auto position closing before new entry
- Contract size normalization
- Position-side aware execution (LONG / SHORT)

### Notification System
- Telegram webhook integration
- Structured trade alerts
- Signal broadcasting to external systems

---

## Execution Flow

1. Pine Script generates trading signal
2. Signal is sent via webhook to `signal_handler`
3. Handler parses:
   - entry direction
   - targets (TP1, TP2)
   - stop loss
   - position size
4. Execution engine:
   - closes existing positions
   - sets leverage
   - opens new trade
   - places take-profit orders
5. Notification service sends update to users

---

## Development Timeline

This trading execution system was developed through an extended research and development cycle from 2022 to 2024, focusing on algorithmic trading automation, futures market execution logic, and API-based order management.

The system went through multiple iterations during this period, including:
- experimental signal execution workflows
- position management logic design
- leverage and risk handling strategies
- integration with futures exchange APIs

The final production-ready version was stabilized and published in 2026 after structural refinements and codebase consolidation.

---

## Example Signal Payload

```json
{
  "symbol": "BTC-USDT",
  "entry": "LONG",
  "entry2": "BUY",
  "target1": 45000,
  "target3": 47000,
  "stop": 43000,
  "valu": 100,
  "valexi1": 60,
  "valexi2": 40
}
Tech Stack
Python 3.x
Requests (HTTP client)
HMAC SHA256 authentication
XT Futures API
TradingView Pine Script
Pipedream (serverless webhook processing)
Security Notes
API keys must be stored in environment variables (.env)
Never commit secrets to version control
Use IP restrictions if supported by exchange
Limitations
No advanced portfolio optimization yet
No machine learning decision layer (rule-based execution only)
Dependent on external webhook reliability (TradingView / Pipedream)
Roadmap
 Add risk management module (max daily loss / drawdown control)
 Introduce strategy engine abstraction layer
 Add backtesting environment
 Add multi-exchange support (Binance, Bybit)
 Add database logging (PostgreSQL / Redis)
 Add dashboard for live monitoring
Disclaimer

This project is for educational and experimental purposes in algorithmic trading.
Use in live markets involves financial risk.

Author

Built as an automated trading infrastructure for futures market execution and signal-based trading systems.
