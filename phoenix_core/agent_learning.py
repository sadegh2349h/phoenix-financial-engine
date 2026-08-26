from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .memory import MemoryStore


@dataclass(frozen=True)
class LearningContext:
    objective: str
    memories: list[dict[str, Any]]
    average_score: float


class AgentLearningContext:
    """Builds bounded learning context from prior decisions and evaluations."""

    def __init__(self, memory: MemoryStore, limit: int = 10) -> None:
        self.memory = memory
        self.limit = limit

    def build(self, objective: str) -> LearningContext:
        if not objective.strip():
            raise ValueError("objective cannot be empty")
        memories = self.memory.context_for(objective, self.limit)
        evaluations = [
            item for item in self.memory.all()
            if item.get("type") == "evaluation"
        ]
        average = round(
            sum(float(item.get("score", 0.0)) for item in evaluations) / len(evaluations), 4
        ) if evaluations else 0.0
        return LearningContext(objective, memories, average)
