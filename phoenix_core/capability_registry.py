"""PHOENIX external capability registry.

Integrations are optional adapters: the core remains provider-agnostic and
safe when third-party packages/services are unavailable.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    key: str
    provider: str
    purpose: str
    adapter: str
    enabled: bool = True
    optional_dependency: bool = True


CAPABILITIES = (
    Capability("orchestration", "Microsoft Agent Framework", "multi-agent workflows, checkpoints and human approval", "phoenix_core.integrations.agent_framework"),
    Capability("memory", "Mem0", "durable user/session/agent memory", "phoenix_core.integrations.mem0"),
    Capability("experimentation", "GrowthBook", "experiments, feature flags and statistical evaluation", "phoenix_core.integrations.growthbook"),
    Capability("observability", "Langfuse", "traces, evaluations, latency and cost visibility", "phoenix_core.integrations.langfuse"),
    Capability("typed_agents", "PydanticAI", "typed agent contracts and structured outputs", "phoenix_core.integrations.pydantic_ai"),
    Capability("oss_intelligence", "PHOENIX local layer", "evidence-ranked discovery and adoption scoring for open-source capabilities", "phoenix_core.oss_intelligence", optional_dependency=False),
    Capability("social_benchmark", "PHOENIX local layer", "evidence, funnel-stage and safety evaluation for social intelligence", "phoenix_core.social_benchmark", optional_dependency=False),
    Capability("agent_quality", "PHOENIX local layer", "goal, evidence, safety and observability production gates", "phoenix_core.agent_quality_gate", optional_dependency=False),
)


def capability_registry() -> dict[str, dict[str, object]]:
    return {item.key: item.__dict__.copy() for item in CAPABILITIES}
