from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agent_performance import AgentPerformanceTracker
from .agents import AgentManifest, AgentRegistry


@dataclass(frozen=True)
class RoutingDecision:
    selected: list[str]
    candidates: list[str]
    rationale: str


class SmartRouter:
    """Ranks capable agents using capability fit and measured historical quality."""

    def __init__(self, registry: AgentRegistry, performance: AgentPerformanceTracker) -> None:
        self.registry = registry
        self.performance = performance

    def select(self, capability: str, limit: int = 3) -> RoutingDecision:
        candidates = self.registry.find_by_capability(capability)
        report = {item.agent: item.average_score for item in self.performance.report()}
        ranked = sorted(candidates, key=lambda m: (-report.get(m.name, 0.5), m.name))
        selected = [m.name for m in ranked[:max(1, limit)]]
        return RoutingDecision(selected, [m.name for m in ranked],
                               "capability fit + historical outcome quality")
