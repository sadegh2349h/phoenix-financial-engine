from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .memory import MemoryStore


@dataclass(frozen=True)
class Evaluation:
    decision_key: str
    outcome: str
    score: float
    lesson: str


class SelfEvaluator:
    """Records outcomes and converts them into reusable operational lessons."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory

    def evaluate(self, decision_key: str, actual: Any, expected: Any) -> Evaluation:
        if not decision_key.strip():
            raise ValueError("decision_key cannot be empty")
        correct = actual == expected
        outcome = "correct" if correct else "incorrect"
        score = 1.0 if correct else 0.0
        lesson = "reinforce evidence pattern" if correct else "review evidence and decision assumptions"
        evaluation = Evaluation(decision_key, outcome, score, lesson)
        self.memory.put(f"evaluation:{decision_key}", {
            "outcome": outcome,
            "score": score,
            "lesson": lesson,
            "actual": actual,
            "expected": expected,
        })
        return evaluation

    def performance(self, prefix: str = "evaluation:") -> dict[str, float]:
        records = [item for key, item in self.memory._items.items() if key.startswith(prefix)]
        if not records:
            return {"count": 0.0, "accuracy": 0.0}
        return {
            "count": float(len(records)),
            "accuracy": round(sum(item.get("score", 0.0) for item in records) / len(records), 4),
        }
