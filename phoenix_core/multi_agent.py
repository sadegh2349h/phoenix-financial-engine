from __future__ import annotations

from typing import Any

from .agents import AgentRegistry
from .decision_engine import Decision, DecisionEngine


class MultiAgentCoordinator:
    """Runs compatible specialists, then delegates synthesis to DecisionEngine."""

    def __init__(self, registry: AgentRegistry, decision_engine: DecisionEngine | None = None) -> None:
        self.registry = registry
        self.decision_engine = decision_engine or DecisionEngine()

    def analyze(self, *, task: str, capabilities: list[str], context: dict[str, Any] | None = None,
                risk_level: str = "low") -> dict[str, Any]:
        context = context or {}
        selected: list[str] = []
        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        for capability in capabilities:
            for manifest in self.registry.find_by_capability(capability):
                if manifest.name in seen:
                    continue
                seen.add(manifest.name)
                selected.append(manifest.name)
                result = self.registry.run(manifest.name, task=task, context=context)
                result = dict(result)
                result["agent"] = manifest.name
                result["risk_level"] = manifest.risk_level
                result["requires_human_review"] = manifest.human_approval_required
                results.append(result)
        decision: Decision = self.decision_engine.evaluate(agent_results=results, risk_level=risk_level)
        return {
            "status": decision.status,
            "agents": selected,
            "agent_results": results,
            "decision": decision,
        }
