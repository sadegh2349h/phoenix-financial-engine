from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .agent_orchestration import AgentResult, AgentTeam
from .agents import AgentManifest


# Stable public list for compatibility and discovery.
default_agent_names = [
    "strategy", "marketing", "brand", "financial_analyst", "sports",
    "meditation", "future", "systemization", "research",
]


def _contract_handler(**kwargs: Any) -> dict[str, Any]:
    """Safe default handler: returns a specialist contract, no external side effects."""
    return {"status": "ready", "confidence": 0.5, "context_keys": sorted(kwargs)}


def _financial_handler(**kwargs: Any) -> dict[str, Any]:
    """Financial specialist contract; analysis is never an autonomous action."""
    return {
        "status": "ready",
        "confidence": 0.5,
        "autonomous_action": False,
        "governance": "human approval required for financial actions",
        "context_keys": sorted(kwargs),
    }


SPECIALIST_AGENTS = [
    (AgentManifest("strategy", "1.0", ("growth_strategy", "strategy", "planning")), _contract_handler),
    (AgentManifest("marketing", "1.0", ("marketing", "growth", "customer_acquisition", "market_analysis")), _contract_handler),
    (AgentManifest("brand", "1.0", ("branding", "brand_strategy")), _contract_handler),
    (AgentManifest("financial_analyst", "1.0", ("finance", "financial_analysis", "financial_research", "market_analysis"), risk_level="high", human_approval_required=True), _financial_handler),
    (AgentManifest("sports", "1.0", ("sports", "performance")), _contract_handler),
    (AgentManifest("meditation", "1.0", ("meditation", "mindfulness")), _contract_handler),
    (AgentManifest("future", "1.0", ("future", "foresight")), _contract_handler),
    (AgentManifest("systemization", "1.0", ("systemization", "operations")), _contract_handler),
    (AgentManifest("research", "1.0", ("research", "analysis")), _contract_handler),
]


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
