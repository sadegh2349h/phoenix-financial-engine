# PHOENIX Financial Performance Failure Audit

## Current diagnosis

The current production backtest is not yet a multi-factor financial intelligence engine. The live shadow evaluation ultimately delegates to `ema_cross_backtest`, which uses only daily close prices, EMA20/EMA50, and fixed fee/slippage assumptions. The signal is a binary long/flat rule and is shifted by one bar to avoid same-candle look-ahead.

## Primary causes of weak performance

### 1. Strategy architecture is the dominant weakness
The engine is effectively an EMA20/EMA50 trend-following strategy. That is too narrow for a system expected to analyze market regimes, momentum, volatility, liquidity, sentiment, macro/fundamental context, and risk. A single trend rule will predictably struggle in sideways and regime-changing markets.

### 2. Analysis layer is not actually driving the backtest
The repository does not currently expose a connected multi-factor analysis pipeline in the shadow evaluation path. The evaluation function calls the EMA crossover backtest directly. Therefore adding indicators conceptually does not improve results unless their outputs affect entry, exit, sizing, and trade selection.

### 3. The sample is far too small for confidence claims
The previous 365-day result used only 5 completed trades. A 20% win rate from five trades is not a reliable estimate of the true probability of success. The 30-day result used one trade, so the reported 100% is statistically meaningless.

### 4. Regime awareness is missing
The current rule does not explicitly distinguish trending, ranging, high-volatility, low-volatility, or transition regimes. This is a major design gap. Professional backtesting should examine performance across regimes rather than only aggregate one-number results. CFA's current backtesting guidance explicitly emphasizes rolling-window testing, scenario analysis, simulation, sensitivity analysis, and structural breaks.

### 5. The objective is too weak
The engine optimizes a basic long/flat return stream rather than selecting high-quality opportunities with calibrated expected return, risk, and probability. A professional system should be allowed to return NO TRADE when evidence is weak.

### 6. Data breadth is insufficient
The current backtest contract requires only timestamp and close. It therefore cannot incorporate volume, volatility structure, market breadth, order-flow/liquidity proxies, derivatives positioning, sentiment, macro variables, or fundamentals.

## Evidence from the current implementation

`financial_engine/evaluation.py` calls `ema_cross_backtest` directly. `financial_engine/backtest.py` computes EMA20/EMA50 and a shifted binary signal. This means the current performance result is primarily a test of one technical strategy, not a test of the full PHOENIX financial-analysis concept.

## Required redesign before the next serious performance test

1. Build a regime classifier.
2. Build a feature layer: trend, momentum, volatility, volume, structure/liquidity proxies, sentiment, derivatives and macro/fundamental inputs where available.
3. Build a signal ensemble instead of a single indicator rule.
4. Add position sizing and risk-aware exits.
5. Permit NO TRADE.
6. Use rolling walk-forward evaluation with strict train/validation/test separation.
7. Add transaction costs and slippage consistently.
8. Require a minimum number of completed trades before reporting probability estimates.
9. Report confidence intervals and uncertainty instead of unsupported win-rate claims.
10. Compare against buy-and-hold and simple robust baselines.
11. Stress-test across market regimes.
12. Freeze the final test set before tuning to prevent backtest overfitting.

## Bottom line

The weak result is **not primarily evidence that individual indicators are bad**. The strongest evidence from the code is that PHOENIX's current financial engine is too narrow: the actual tested strategy is an EMA crossover with limited data features. The first major fix should therefore be the **analysis/strategy architecture and evaluation methodology**, followed by data expansion and only then indicator selection/tuning.
