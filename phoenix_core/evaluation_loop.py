from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .memory import MemoryStore


@dataclass(frozen=True)
class Evaluation:
    decision_id: str
    outcome: str
    score: float
    lesson: str


class SelfEvaluationLoop:
    """Records observed outcomes and feeds measurable lessons back into memory."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory

    def evaluate(self, decision_id: str, outcome: str, score: float, lesson: str = "") -> Evaluation:
        if not decision_id.strip():
            raise ValueError("decision_id cannot be empty")
        if not 0.0 <= score <= 1.0:
            raise ValueError("score must be between 0 and 1")
        evaluation = Evaluation(decision_id, outcome, score, lesson)
        self.memory.put(f"evaluation:{decision_id}", {
            "type": "evaluation",
            "decision_id": decision_id,
            "outcome": outcome,
            "score": score,
            "lesson": lesson,
        })
        return evaluation

    def performance(self) -> dict[str, Any]:
        evaluations = [item for item in self.memory.all() if item.get("type") == "evaluation"]
        if not evaluations:
            return {"count": 0, "average_score": 0.0}
        return {
            "count": len(evaluations),
            "average_score": round(sum(float(x["score"]) for x in evaluations) / len(evaluations), 4),
        }
