from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class AgentResult:
    agent: str
    status: str
    output: dict[str, Any]
    confidence: float = 0.0


class AgentTeam:
    """Runs independent specialist agents and returns an auditable team result."""

    def __init__(self) -> None:
        self._agents: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(self, name: str, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        if name in self._agents:
            raise ValueError(f"agent already registered: {name}")
        self._agents[name] = handler

    def run(self, task: dict[str, Any]) -> list[AgentResult]:
        results: list[AgentResult] = []
        for name, handler in self._agents.items():
            try:
                output = handler(dict(task))
                results.append(AgentResult(name, "completed", output, float(output.get("confidence", 0.0))))
            except Exception as exc:
                results.append(AgentResult(name, "failed", {"error": type(exc).__name__}, 0.0))
        return results

    @staticmethod
    def consensus(results: list[AgentResult]) -> dict[str, Any]:
        completed = [r for r in results if r.status == "completed"]
        confidence = round(sum(r.confidence for r in completed) / len(completed), 4) if completed else 0.0
        return {
            "status": "completed" if completed else "failed",
            "agents": [r.agent for r in completed],
            "confidence": confidence,
            "outputs": {r.agent: r.output for r in completed},
        }
