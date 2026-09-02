# PHOENIX Mother Ecosystem

## Mission
PHOENIX is a modular intelligence and execution ecosystem designed to coordinate specialized engines, durable memory, external data, monitoring and human-approved actions.

## Core operating loop
Observe → Normalize → Remember → Analyze → Deliberate → Decide → Approve when required → Execute → Monitor → Learn → Audit.

## Architectural layers
1. **Data** — web, APIs, files, market feeds and future providers.
2. **Memory** — durable facts, historical observations, decisions, outcomes and lessons.
3. **Intelligence** — specialist agents and engines.
4. **Orchestration** — task routing, dependencies, priorities and lifecycle management.
5. **Decision** — evidence aggregation, confidence, uncertainty and risk gates.
6. **Execution** — controlled actions through approved integrations.
7. **Monitoring** — scheduled and event-driven observation.
8. **Audit** — immutable-style event records, provenance and decision traceability.
9. **Security** — least privilege, secret isolation and explicit approval boundaries.
10. **Interface** — ChatGPT, dashboards, Telegram and future channels.

## Specialist layer
PHOENIX currently maintains 15 specialist domains: Psyche, Ops, Brand, Closer, Growth, Edu, Tribe, Price, Viral, Connect, Story, Care, Experiment, Opportunity and Intelligence. Routing is evidence-based and recommendations remain human-approved.

## External capability layer
Five optional provider adapters are registered without hard-coupling the core:
- **Microsoft Agent Framework** — multi-agent orchestration, workflows, checkpoints and approval boundaries.
- **Mem0** — durable user/session/agent memory.
- **GrowthBook** — experimentation, feature flags and statistical evaluation.
- **Langfuse** — traces, evaluations, latency and cost observability.
- **PydanticAI** — typed agent contracts and structured outputs.

The adapter boundary allows PHOENIX to operate without these optional dependencies while making each provider replaceable and testable. Providers must pass security, license, dependency and compatibility review before production activation.

## Coordination contract
`phoenix_core.phoenix_orchestrator.build_execution_plan()` connects specialist routing with the capability registry and emits a governed lifecycle: observe → remember → route → analyze → deliberate → human approval → execute → monitor → learn → audit.

## Modularity
Each engine is a plugin-like module with a manifest, capabilities and version. The core must not contain business-specific assumptions. Modules can be enabled, disabled, upgraded or replaced independently.

## Financial engine contract
Financial Engine is a specialist module. It consumes normalized market/context data and returns structured research, signals, risk metrics and backtest results. It does not bypass PHOENIX governance or autonomously execute trades.

## Memory policy
No fixed 24-hour purge. Retention is explicit and configurable by dataset. Historical market data should be durable and reproducible.

## Data provenance
Every important output should retain source, timestamp, transformation, confidence/data-quality indicators and relevant assumptions.

## Reliability
- Fail closed when critical data is missing.
- Separate raw data from derived data.
- Separate research from action.
- Never convert confidence into certainty.
- Preserve backward-compatible contracts where practical.
- Prefer additive migrations over destructive rewrites.

## Communications
Telegram reporting/notifications are currently disabled by operational preference. Re-enable only with explicit human approval.

## Evolution roadmap
Phase 1: mother kernel and contracts.
Phase 2: durable storage and data-provider abstraction.
Phase 3: specialist-agent registry and governance.
Phase 4: Financial Engine.
Phase 5: monitoring and alerting.
Phase 6: external capability adapters and coordinated specialist orchestration.
Phase 7: dashboards, APIs, evaluation, resilience, security hardening and public-facing PHOENIX platform.
