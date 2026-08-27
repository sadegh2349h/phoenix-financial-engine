# PHOENIX Financial Intelligence — Learning & Validation Specification

## Mission
PHOENIX must evolve from a market-reporting script into a decision-support engine that can identify opportunities, quantify uncertainty, explain the evidence, and explicitly abstain when evidence is insufficient.

A market report alone is not a successful outcome. Every actionable analysis must produce: **directional thesis, setup, entry zone, invalidation, targets, expected-return range, probability estimate, risk/reward, confidence, evidence, and reasons not to trade**.

## Knowledge domains

1. Macroeconomics: inflation, rates, liquidity, credit, employment, growth, central-bank policy and transmission.
2. Fundamental analysis: valuation, earnings/cash-flow drivers, supply/demand, token/network fundamentals where applicable.
3. Technical analysis: price action, market structure, trend, support/resistance, volume, volatility, momentum, multi-timeframe analysis.
4. Market microstructure: liquidity, spreads, depth, order flow, market impact, execution quality.
5. Derivatives: futures, funding, open interest, basis, options, implied volatility, liquidation dynamics.
6. Sentiment and behavioral finance: positioning, fear/greed, crowding, FOMO/panic and behavioral biases.
7. Cross-asset relationships: dollar, rates, commodities, equities, crypto correlations and regime changes.
8. Risk management: position sizing, stop distance, drawdown, VaR/scenario analysis, concentration and correlation risk.
9. Strategy research: trend following, momentum, mean reversion, breakout, pullback, volatility and regime-dependent strategies.
10. Execution and evaluation: fees, slippage, benchmark selection, attribution, walk-forward testing and out-of-sample validation.

These domains follow professional investment-analysis principles covering risk management, portfolio construction, behavioral finance, market efficiency, execution and market microstructure. Sources: CFA Institute CBOK and 2026 curriculum readings; Investor.gov; Federal Reserve; BIS.

## Analysis pipeline

`Data → Data Quality → Regime → Macro/Fundamental → Technical → Microstructure/Derivatives → Sentiment → Candidate Setups → Risk Model → Probability Model → Decision Gate → Explanation → Outcome Tracking → Learning`

### Data rules
- Every feature must have a timestamp and source.
- No look-ahead leakage.
- Missing/stale/conflicting data must reduce confidence or cause abstention.
- Historical data used for indicators must be available before the prediction timestamp.
- Live analysis must separate information known at decision time from later information.

### Opportunity detection
PHOENIX must scan for setups rather than force a trade. Candidate setups are ranked using independent evidence:

- market regime compatibility
- structural confirmation
- momentum/volume confirmation
- liquidity/execution quality
- macro/fundamental alignment
- derivatives/positioning confirmation
- sentiment confirmation
- risk/reward

A single indicator must never be sufficient for an actionable signal.

### Probability and expected return
PHOENIX must **not invent a precise probability** from subjective confidence. Probabilities must be calibrated from historical, out-of-sample outcomes for the same setup/regime class.

Each opportunity should expose:
- `p_success`
- `expected_return_pct`
- `expected_loss_pct`
- `risk_reward`
- `confidence_score`
- `sample_size`
- `calibration_status`

If calibration or sample size is inadequate, the result must be `NO_TRADE` or `INSUFFICIENT_EVIDENCE`, not a fabricated high-confidence prediction.

### Decision states
- `STRONG_LONG`
- `LONG`
- `WAIT_LONG`
- `NEUTRAL`
- `WAIT_SHORT`
- `SHORT`
- `STRONG_SHORT`
- `NO_TRADE`
- `INSUFFICIENT_EVIDENCE`

## Validation protocol

No strategy is accepted because a single backtest is profitable.

Required progression:

1. Unit and integration tests.
2. Historical backtest with realistic fees and slippage.
3. Multiple market regimes.
4. Walk-forward validation.
5. Strict out-of-sample test.
6. Blind/forward paper test.
7. Stress tests for volatility, liquidity and data gaps.
8. Stability test across assets and timeframes.
9. Probability calibration test.
10. Only then: limited live decision-support use with human approval.

## Performance gates

A strategy is rejected if any of the following is unacceptable:
- profit factor ≤ 1
- persistent negative excess return versus an appropriate benchmark
- excessive drawdown relative to expected return
- unstable performance across regimes
- poor probability calibration
- too few independent observations
- material sensitivity to small parameter changes
- evidence of look-ahead bias or data leakage

Accuracy alone is not the objective. PHOENIX must optimize for **risk-adjusted, benchmark-relative, repeatable performance**.

## Human governance

PHOENIX is a decision-support system. It must never replace the founder's final financial decision. High-risk opportunities, weak evidence, conflicting signals, and abnormal market conditions must trigger human review or abstention.

## Learning loop

For every historical or forward signal, store:
- information available at decision time
- feature values
- thesis and regime
- predicted probability/range
- entry/invalidation/targets
- actual outcome
- slippage/fees
- error category

The engine should periodically evaluate which features and setup classes add predictive value and remove features that fail out-of-sample validation.

## Success criterion

The next version is not considered successful merely because CI is green. It is successful only when PHOENIX demonstrates, on unseen data, that its opportunity selection and probability estimates are materially better than the previous baseline while controlling drawdown and execution costs.
