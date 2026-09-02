"""Optional external capability registry for PHOENIX.

Third-party frameworks remain optional. PHOENIX discovers them without eagerly
importing vendor packages, keeping the native core portable and testable.
"""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from typing import Iterable


@dataclass(frozen=True)
class ExternalCapability:
    name: str
    project: str
    package: str
    priority: str
    purpose: str
    optional: bool = True


CAPABILITIES: tuple[ExternalCapability, ...] = (
    ExternalCapability("durable_workflows", "Microsoft Agent Framework / LangGraph", "agent_framework", "P0", "durable, stateful and human-governed agent workflows"),
    ExternalCapability("typed_agents", "PydanticAI", "pydantic_ai", "P0", "typed agent contracts and structured outputs"),
    ExternalCapability("model_gateway", "LiteLLM", "litellm", "P0", "provider routing, retry/fallback and spend governance"),
    ExternalCapability("semantic_memory", "Mem0", "mem0", "P1", "scoped semantic memory and memory lifecycle management"),
    ExternalCapability("llm_observability", "Langfuse", "langfuse", "P1", "traces, latency, token/cost and evaluation telemetry"),
    ExternalCapability("experimentation", "GrowthBook", "growthbook", "P0", "experimentation, feature flags and statistical evaluation"),
    ExternalCapability("otel_instrumentation", "OpenLLMetry/OpenTelemetry", "opentelemetry", "P1", "vendor-neutral distributed telemetry"),
    ExternalCapability("quality_monitoring", "Evidently", "evidently", "P1", "quality evaluation, drift detection and production monitoring"),
)


def available_capabilities(capabilities: Iterable[ExternalCapability] = CAPABILITIES) -> list[ExternalCapability]:
    return [cap for cap in capabilities if importlib.util.find_spec(cap.package) is not None]


def capability_status() -> list[dict[str, object]]:
    installed = {cap.name for cap in available_capabilities()}
    return [{
        "name": cap.name, "project": cap.project, "package": cap.package,
        "priority": cap.priority, "optional": cap.optional,
        "installed": cap.name in installed, "purpose": cap.purpose,
    } for cap in CAPABILITIES]
