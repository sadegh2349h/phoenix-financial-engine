# PHOENIX External Code Intelligence Registry

## Purpose

This registry records high-value open-source projects and implementation patterns that can materially improve PHOENIX. External code is **not copied blindly into the core**. Each candidate is evaluated for architectural fit, license, maintenance status, security, dependency cost, and testability before adoption.

## Current PHOENIX baseline

The repository already contains core capabilities for agent orchestration, smart routing, memory, data access, evaluation loops, monitoring, risk control, multi-agent coordination, market intelligence, scheduled execution, Telegram alerting, and CI/runtime workflows.

## Priority adoption matrix

| Priority | Project | Capability to absorb | PHOENIX target | Adoption mode |
|---|---|---|---|---|
| P0 | Microsoft Agent Framework | Durable multi-agent workflows, sequential/concurrent/handoff/group patterns, checkpointing, human-in-loop, OpenTelemetry | `phoenix_core/orchestrator.py`, `execution_loop.py`, `monitoring.py` | Architecture pattern + optional adapter |
| P0 | PydanticAI | Typed agents, structured outputs, dependency injection, agent specs, evals | agent contracts, specialist agents, decision outputs | Optional adapter + native validation |
| P0 | LiteLLM | Provider abstraction, routing, retry/fallback, load balancing, spend tracking | `llm_provider.py`, `smart_routing.py`, cost governance | Optional provider gateway |
| P0 | LangGraph | Stateful/durable workflows, persistence, human-in-loop, state transitions | long-running execution and recovery | Pattern/optional adapter; do not duplicate current orchestration blindly |
| P1 | Mem0 | Layered memory, semantic retrieval, deduplication/conflict resolution, scoped memories | `memory.py`, data-memory layer | Optional memory provider |
| P1 | Langfuse | LLM tracing, latency/token/cost tracking, prompt/eval observability | `observability.py`, `monitoring.py`, evaluation loop | Optional telemetry backend |
| P1 | OpenLLMetry/OpenTelemetry | Standardized LLM traces and provider/vector DB instrumentation | runtime observability | Native OTel instrumentation |
| P1 | Evidently | Evaluation suites, data/LLM quality metrics, drift detection, live monitoring | self-evaluation, performance diagnostics, market/data quality | Optional evaluation/monitoring module |

## Why these are valuable

### 1. Microsoft Agent Framework — P0
Adds production workflow patterns that map directly to PHOENIX's goal-oriented execution model: sequential, concurrent, handoff and group collaboration, plus checkpointing, streaming and human approval. It is actively maintained and MIT licensed.

### 2. PydanticAI — P0
Strengthens the contract boundary between agents and the core. Typed inputs/outputs and declarative agent specifications reduce runtime ambiguity and make specialist-agent behavior easier to validate.

### 3. LiteLLM — P0
Creates a model-provider abstraction with retry/fallback, routing and cost tracking. This is strategically important because PHOENIX should not become dependent on one model/provider.

### 4. LangGraph — P0
Useful as a reference for durable state machines and resumable long-running agent workflows. PHOENIX already has orchestration and runtime code, so the correct approach is selective adoption rather than replacing the existing core.

### 5. Mem0 — P1
Provides a mature memory lifecycle model: conversation/session/user or agent memory, semantic retrieval, deduplication and conflict handling. PHOENIX's current JSON/token memory is functional but comparatively simple.

### 6. Langfuse — P1
Provides the missing operational visibility around model calls: traces, latency, token usage, cost, retrieval/tool steps, prompts and evaluations.

### 7. OpenLLMetry/OpenTelemetry — P1
Gives PHOENIX vendor-neutral telemetry so observability can survive changes in LLM providers and backends.

### 8. Evidently — P1
Adds systematic quality monitoring: data drift, evaluation metrics, regression detection and production monitoring. This aligns strongly with PHOENIX's requirement to learn from measurable outcomes rather than intuition.

## Safety / maintenance decisions

- Microsoft AutoGen is **not** selected as a new dependency because its upstream repository is now in maintenance mode and directs new projects toward Microsoft Agent Framework.
- No external repository is vendored wholesale into PHOENIX.
- Optional integrations must fail closed and leave the native PHOENIX path operational when the external package is absent.
- Every adopted integration requires tests and a rollback path.
- Financial decision logic remains under PHOENIX governance and human-approval rules; external agent frameworks must not override those controls.

## Implementation sequence

1. Typed contracts and quality gates.
2. Model gateway with fallback/cost governance.
3. Durable workflow/checkpoint layer.
4. Tiered semantic memory provider.
5. Unified OpenTelemetry tracing.
6. Evaluation/drift monitoring.
7. Dashboard and operational reporting.
