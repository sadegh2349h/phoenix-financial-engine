# PHOENIX External Code Intelligence Registry

## Purpose

This registry records high-value open-source projects and implementation patterns that can materially improve PHOENIX. External code is **not copied blindly into the core**. Each candidate is evaluated for architectural fit, license, maintenance status, security, dependency cost, and testability before adoption.

## 2026 high-signal GitHub research

The following five projects were selected as the strongest combination of community adoption, technical relevance and architectural value for PHOENIX. GitHub stars are treated as a popularity signal, not as proof of correctness or quality.

| Rank | Project | Primary strength | PHOENIX decision |
|---|---|---|---|
| 1 | `obra/superpowers` | skill-driven, evidence-first development workflow, TDD, planning, review and verification | **Adopt patterns** for PHOENIX engineering skills and quality gates; do not vendor the project |
| 2 | `langchain-ai/langchain` | interoperable LLM/agent components, integrations, model portability and rapid composition | **Selective architecture adoption** for tool/data/model composition; keep PHOENIX orchestration as the governing layer |
| 3 | `TauricResearch/TradingAgents` | specialized financial agents, analyst/researcher debate, risk/portfolio roles, persistence and checkpointing | **Selective adoption** for Financial Engine research/debate patterns; never bypass PHOENIX human approval |
| 4 | `vllm-project/vllm` | high-throughput, memory-efficient LLM inference and OpenAI-compatible serving | **Infrastructure option** for future self-hosted/local model serving and cost/latency optimization |
| 5 | `FoundationAgents/MetaGPT` | role-based multi-agent collaboration, SOP-driven teams and structured deliverables | **Architecture pattern** for specialist collaboration; do not replace PHOENIX router/orchestrator |

## PHOENIX capability mapping

### Superpowers → PHOENIX Skill Governance
Absorb: mandatory planning, test-first implementation, systematic debugging, code review and verification-before-completion. This strengthens execution quality and prevents PHOENIX from declaring success without evidence.

Target: specialist skill contracts, engineering workflow, quality gates and future client-delivery playbooks.

### LangChain → PHOENIX Integration Fabric
Absorb: modular components, provider interoperability and tool/data integration patterns. Use only where they improve the existing provider-agnostic boundary.

Target: Data, Tools, model gateway, retrieval and future external-service adapters.

### TradingAgents → PHOENIX Financial Council
Absorb: specialist analyst roles, bullish/bearish research debate, risk management, portfolio-level synthesis, decision logging and checkpoint/recovery patterns.

Target: Financial Engine research and shadow evaluation. External code must never autonomously trade or override human approval.

### vLLM → PHOENIX Inference Infrastructure
Absorb: efficient model serving, continuous batching, caching, quantization and OpenAI-compatible serving where operationally justified.

Target: optional self-hosted inference tier for high-volume or privacy-sensitive workloads. Adoption is conditional on hardware, model quality, security and total-cost testing.

### MetaGPT → PHOENIX Specialist Organization
Absorb: role-based decomposition, SOP-driven collaboration and structured handoffs between specialists.

Target: Orchestrator + Specialist Router + multi-stage client problem solving. PHOENIX remains the governance layer and human decision owner.

## Combined PHOENIX target architecture

Observe → Normalize → Remember → Route → Specialist Collaboration → Evidence/De\-bate → Decision Gate → Human Approval → Execute → Monitor → Learn → Audit

Supporting capabilities:
- Superpowers patterns for disciplined work and verification.
- LangChain-style composition for tools, models and integrations.
- MetaGPT-style role/SOP collaboration for specialist teams.
- TradingAgents-style domain councils for financial research.
- vLLM as an optional execution/inference tier.

## Adoption rules

1. **Patterns before dependencies:** prefer extracting proven design patterns before adding a hard dependency.
2. **No wholesale copying:** external repositories are references/adapters, not replacements for the PHOENIX core.
3. **Human governance remains mandatory:** external agents cannot make irreversible client or financial decisions autonomously.
4. **Evidence before activation:** every dependency must pass compatibility, security, licensing, performance and regression tests.
5. **Rollback required:** every production integration must have a native PHOENIX fallback path.

## Current baseline retained

Existing PHOENIX adapters remain valid: Microsoft Agent Framework, Mem0, GrowthBook, Langfuse and PydanticAI, plus the broader optional capability registry. This research **adds an evidence-ranked architecture layer**; it does not invalidate existing adapters.

## Research provenance

Primary project sources reviewed: official GitHub repositories/READMEs for Superpowers, LangChain, TradingAgents, vLLM and MetaGPT. Star counts are time-sensitive and should be refreshed before procurement or production dependency decisions.
