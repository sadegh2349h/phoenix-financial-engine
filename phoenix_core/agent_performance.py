from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .memory import MemoryStore


@dataclass(frozen=True)
class AgentPerformance:
    agent: str
    count: int
    average_score: float


class AgentPerformanceTracker:
    """Tracks outcome quality per specialist agent for measurable improvement."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory

    def record(self, agent: str, decision_id: str, score: float, outcome: str) -> None:
        if not agent.strip() or not decision_id.strip():
            raise ValueError("agent and decision_id are required")
        if not 0.0 <= score <= 1.0:
            raise ValueError("score must be between 0 and 1")
        self.memory.put(f"agent-evaluation:{agent}:{decision_id}", {
            "type": "agent_evaluation",
            "agent": agent,
            "decision_id": decision_id,
            "score": score,
            "outcome": outcome,
        })

    def report(self) -> list[AgentPerformance]:
        grouped: dict[str, list[float]] = {}
        for item in self.memory.all():
            if item.get("type") == "agent_evaluation":
                grouped.setdefault(str(item["agent"]), []).append(float(item["score"]))
        return [
            AgentPerformance(agent, len(scores), round(sum(scores) / len(scores), 4))
            for agent, scores in sorted(grouped.items())
        ]
