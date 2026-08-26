from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .agent_orchestration import AgentResult, AgentTeam


@dataclass(frozen=True)
class SpecialistProfile:
    name: str
    domain: str
    priority: int = 100


class SpecialistAgentTeam(AgentTeam):
    """Extensible registry for PHOENIX domain specialists."""

    def __init__(self) -> None:
        super().__init__()
        self._profiles: dict[str, SpecialistProfile] = {}

    def register_specialist(self, profile: SpecialistProfile, handler: Callable[[dict[str, Any]], dict[str, Any]]) -> None:
        self.register(profile.name, handler)
        self._profiles[profile.name] = profile

    def run_by_domain(self, task: dict[str, Any], domains: set[str] | None = None) -> list[AgentResult]:
        selected: list[AgentResult] = []
        for name, handler in self._agents.items():
            profile = self._profiles[name]
            if domains and profile.domain not in domains:
                continue
            try:
                output = handler(dict(task))
                selected.append(AgentResult(name, "completed", output, float(output.get("confidence", 0.0))))
            except Exception as exc:
                selected.append(AgentResult(name, "failed", {"error": type(exc).__name__}, 0.0))
        return sorted(selected, key=lambda result: self._profiles[result.agent].priority)
