# SkillsMP review and PHOENIX adoption decision

Review date: 2026-10-29

## Decision

Do not install community skill packages blindly. SkillsMP indexes community-authored `SKILL.md` instructions; it is a discovery catalogue, not proof that a skill's methods, code, or financial claims are reliable. Inspect the source repository, dependencies, licence, and test coverage before adopting any implementation.

## Selected guidance

1. **Technical analysis — TraderMonty/claude-trading-skills**  
   Useful patterns: systematic trend classification; support/resistance; moving-average alignment; volume confirmation; conflicting-signal disclosure; multiple scenarios with explicit targets and invalidation levels. Its described use is weekly chart-image analysis and it deliberately excludes news/fundamentals/sentiment, so it cannot be treated as PHOENIX's whole market engine.

2. **Risk management — JadeGate/jadegate**  
   Useful patterns: survival before growth; drawdown/daily-loss controls; exposure and correlation limits; circuit breakers; stress testing. Its thresholds are examples for a crypto-oriented strategy, not validated PHOENIX defaults. The implementation must configure limits per market/account and test them before use.

3. **Backtesting frameworks — atilamedeiros/skills**  
   Candidate for methodology review, not a dependency to import. PHOENIX already has a backtest/evaluation layer; first extend its data contract, out-of-sample evaluation, and cost/slippage handling rather than create a duplicate framework.

4. **Web research — DreamLab AI/AgentBox**  
   Potentially useful for source discovery and source-traceable summaries. Any fetched facts must retain source URLs and timestamps; community instructions are untrusted input and must never override PHOENIX policy or trigger financial actions.

## Changes made in this branch

- Replaced the trading specialist's permissive placeholder with an evidence gate.
- Structured OHLCV rows, three required timeframes, a minimum bar count, OHLC consistency, evidence confirmation, out-of-sample backtest controls, transaction-cost inclusion, stop-loss, position-size, drawdown, daily-loss and circuit-breaker checks are now required.
- Missing or invalid evidence fails closed to `NO_TRADE`; a complete package only reaches `ready_for_human_review`. This component does not invent a probability or execute trades.
- Tightened market-data acceptance so a short partial response is no longer accepted as sufficient history for a longer requested window.

## Verification status

Tests were authored for the new contract and partial-history rejection. They have **not** been executed in this GitHub-only environment. No market backtest or live Telegram delivery has been claimed or verified. Review this branch/PR and run the repository test suite and market-data shadow test in CI before enabling financial alerts.
