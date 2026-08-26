# PHOENIX Financial Engine

## Live public data
The first production-oriented adapter uses Binance's public market-data API. No API key is required for public market-data endpoints, and no trading/account permissions are requested.

Official endpoint family: `https://data-api.binance.vision`

## Current capabilities
- Spot ticker retrieval
- OHLCV kline retrieval
- Data-quality-aware analytics
- EMA20 / EMA50
- RSI14
- ATR14
- Volume ratio
- Structured market score
- Baseline auditable backtest with fee assumption and drawdown

## Next modules
1. Multi-timeframe confirmation
2. Market-structure engine
3. Volatility/regime classification
4. Cross-asset relationships
5. Fundamental and macro context
6. Sentiment and on-chain providers
7. Risk engine and position sizing
8. Walk-forward and out-of-sample testing
9. Alert engine
10. Telegram delivery

All provider integrations remain replaceable. No trading execution is enabled by this module.
