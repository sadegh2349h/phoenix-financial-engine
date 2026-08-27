from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .agent_performance import AgentPerformanceTracker
from .agents import AgentManifest, AgentRegistry


@dataclass(frozen=True)
class AgentSelection:
    agent: str
    capability: str
    score: float
    reason: str


class IntelligentAgentSelector:
    """Ranks capable specialists using historical performance, with a neutral prior."""

    def __init__(self, registry: AgentRegistry, performance: AgentPerformanceTracker) -> None:
        self.registry = registry
        self.performance = performance

    def select(self, capability: str, limit: int = 3) -> list[AgentSelection]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        candidates = self.registry.find_by_capability(capability)
        report = {item.agent: item.average_score for item in self.performance.report()}
        ranked = []
        for manifest in candidates:
            score = report.get(manifest.name, 0.5)
            reason = "historical performance" if manifest.name in report else "neutral prior"
            ranked.append(AgentSelection(manifest.name, capability, score, reason))
        return sorted(ranked, key=lambda item: (-item.score, item.agent))[:limit]
