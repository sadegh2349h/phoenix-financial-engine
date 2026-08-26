# PHOENIX Continuation Manifest

This repository is the persistent engineering source of truth for PHOENIX.

## Current state
- Mother core exists under `phoenix_core/`.
- Durable SQLite storage abstraction exists.
- Data-provider abstraction exists.
- Public market-data adapter exists under `phoenix_core/market_data.py`.
- Financial analysis exists under `financial_engine/`.
- Baseline EMA20/EMA50 backtest exists under `financial_engine/backtest.py`.
- Multi-timeframe aggregation exists under `financial_engine/research.py`.
- Scheduled market monitoring exists under `.github/workflows/phoenix-market-monitor.yml`.
- Telegram credentials are expected only through GitHub Actions secrets; never commit credentials.

## Branch map
- `development`: integration branch.
- `feature/phoenix-mother-core`: mother-core development.
- `feature/financial-engine`: financial-engine development.
- `feature/alerting`: monitoring/alerting development.

## Non-negotiable architecture rules
1. Never introduce a fixed 24-hour purge.
2. Raw data, derived data, decisions and audit records remain separable.
3. External providers are adapters and must be replaceable.
4. Modules must be independently enableable and versionable.
5. Critical actions require governance/human approval unless explicitly changed by policy.
6. Never represent confidence as certainty.
7. Backtests must include costs and disclose assumptions.
8. Do not commit API keys, bot tokens or private credentials.
9. Prefer additive migrations and backward-compatible contracts over destructive rewrites.
10. PHOENIX is decision support; autonomous financial order execution is disabled by design.

## Next engineering priorities
1. Merge mother-core and financial branches through review.
2. Add real historical data ingestion with pagination and rate-limit handling.
3. Add dataset versioning and reproducible snapshots.
4. Expand backtests: walk-forward, out-of-sample, benchmark comparison, slippage/fees, regime analysis.
5. Add multi-factor signal engine and risk engine.
6. Add Telegram alert formatting, deduplication and cooldowns.
7. Add monitoring health checks and failure alerts.
8. Add CI tests and security checks.
9. Build additional PHOENIX engines only after core contracts stabilize.
