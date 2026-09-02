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

## Operational reporting rule — Active Modules
Every PHOENIX operational task must explicitly declare the **active modules** in its report/output before presenting the result.

For each active module, the report must state its **role in the current task**, not merely list its name. This makes responsibility, reasoning ownership and output provenance visible.

Minimum reporting contract:
- **Active modules:** module names selected for the task.
- **Role:** what each active module contributes.
- **Primary diagnosis/output:** the consolidated result.
- **Decision owner:** human unless an explicitly governed contract states otherwise.

Example: for an Instagram page analysis, PHOENIX may activate Phoenix SMM for social/content performance, Phoenix Intelligence for market/competitor signals, Phoenix Psyche for audience behavior hypotheses, Phoenix Growth for growth opportunities, Phoenix Experiment for test design, and Phoenix Brand for positioning. Only modules actually selected by routing/analysis should be reported as active.

The orchestrator exposes this contract through `build_execution_plan()` using the `active_modules` field.

## Phoenix Growth
**Phoenix Growth** is the acquisition and growth specialist. Its current implementation is `phoenix_core/growth_specialist.py` and its role is to turn a business goal into measurable, low-cost growth experiments.

Core contract:
- Funnel stages: **Awareness (آگاهی) → Consideration (بررسی) → Conversion (تبدیل)**.
- Three experiment types: shareable acquisition asset, participatory referral loop, and diagnostic-to-conversation activation.
- Primary measurement priority: retention, saves, shares, qualified leads and conversion.
- Frameworks: AARRR, Hook Model, Growth Loops and hypothesis-driven experimentation.
- Every experiment declares hypothesis, execution plan, KPI, risk and human approval requirement.
- No Telegram dependency; the module is channel-agnostic and can use Instagram, website, CRM or community data.

Phoenix Growth is routed by `specialist_router.py` and, when selected, is injected into `phoenix_orchestrator.build_execution_plan()` as a measurable growth plan.

## Evidence-ranked open-source intelligence
PHOENIX maintains an evidence-ranked registry of high-signal open-source projects at `phoenix_core/oss_intelligence.py` and `docs/PHOENIX_EXTERNAL_CODE_REGISTRY.md`.

The current five selected architecture references are:
1. **obra/superpowers** — disciplined skills, planning, TDD, review and verification → PHOENIX skill governance and quality gates.
2. **langchain-ai/langchain** — composable models, tools, data and provider integrations → PHOENIX integration fabric.
3. **TauricResearch/TradingAgents** — specialist financial analysis, debate, risk and decision logging → Financial Engine research council and shadow evaluation.
4. **vllm-project/vllm** — high-throughput, memory-efficient inference → optional self-hosted inference tier.
5. **FoundationAgents/MetaGPT** — role-based multi-agent collaboration and SOP-driven workflows → specialist collaboration and governed handoffs.

These are **reference architectures, not wholesale dependencies**. PHOENIX adopts patterns selectively after security, license, compatibility, performance and regression review. Human approval remains mandatory for consequential actions.

## External capability layer
Five optional provider adapters are registered without hard-coupling the core:
- **Microsoft Agent Framework** — multi-agent orchestration, workflows, checkpoints and approval boundaries.
- **Mem0** — durable user/session/agent memory.
- **GrowthBook** — experimentation, feature flags and statistical evaluation.
- **Langfuse** — traces, evaluations, latency and cost observability.
- **PydanticAI** — typed agent contracts and structured outputs.

The adapter boundary allows PHOENIX to operate without these optional dependencies while making each provider replaceable and testable. Providers must pass security, license, dependency and compatibility review before production activation.

## Coordination contract
`phoenix_core.phoenix_orchestrator.build_execution_plan()` connects specialist routing with the capability registry and emits a governed lifecycle: observe → remember → route → analyze → deliberate → human approval → execute → monitor → learn → audit. It also emits `active_modules`, identifying the modules participating in the current task and their roles. When Growth is routed, the plan also contains `growth_plan` with funnel stages, experiments and measurement priorities.

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
