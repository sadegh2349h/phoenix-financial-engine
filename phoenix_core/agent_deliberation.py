from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Deliberation:
    rounds: int
    proposals: dict[str, dict[str, Any]]
    decision: dict[str, Any]


class AgentDeliberator:
    """Coordinates proposals, cross-review, and a final evidence-aware decision."""

    def __init__(self) -> None:
        self._agents: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(self, name: str, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        if name in self._agents:
            raise ValueError(f"agent already registered: {name}")
        self._agents[name] = handler

    def deliberate(self, task: dict[str, Any], rounds: int = 2) -> Deliberation:
        if not self._agents:
            return Deliberation(0, {}, {"status": "no_agents"})
        if rounds < 1:
            raise ValueError("rounds must be positive")
        proposals: dict[str, dict[str, Any]] = {}
        for current_round in range(1, rounds + 1):
            context = {**task, "round": current_round, "proposals": proposals}
            for name, handler in self._agents.items():
                proposals[name] = dict(handler(dict(context)))
        scores = [float(p.get("confidence", 0.0)) for p in proposals.values()]
        confidence = round(sum(scores) / len(scores), 4) if scores else 0.0
        decision = {
            "status": "decided" if confidence >= 0.5 else "needs_review",
            "confidence": confidence,
            "proposals": proposals,
        }
        return Deliberation(rounds, proposals, decision)
