# PHOENIX data, memory and agent layer

## Durable memory
SQLite is the first durable local backend. The interface is intentionally small so PostgreSQL, object storage or another backend can be introduced without changing consumers.

Retention is explicit. There is no hard-coded 24-hour deletion policy. Raw market data, derived features, signals, decisions and outcomes should use separate logical datasets as the system grows.

## Data layer
External providers implement the DataProvider contract. Normalization creates a provider-independent OHLCV representation. Provider failures and malformed records must reduce data-quality confidence rather than silently become valid observations.

## Agent layer
Agents are registered by manifest and capability. The core invokes capabilities through a registry, allowing specialist agents to be added, disabled or replaced independently.

## Governance
Sensitive capabilities remain behind central policy gates. Financial execution is not automatically authorized by analytical confidence.

## Next implementation sequence
1. Provider adapters and historical ingestion.
2. Dataset metadata and data-quality validation.
3. Durable event and decision storage.
4. Agent lifecycle and health checks.
5. Financial Engine integration.
6. Scheduled monitoring and Telegram notification adapter.
7. Evaluation, backtesting and resilience tests.
