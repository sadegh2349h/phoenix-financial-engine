from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agents import AgentRegistry, build_default_registry
from .intelligence import IntelligenceLayer, IntelligenceRequest


@dataclass(frozen=True)
class AgentTask:
    objective: str
    capability: str
    context: dict[str, Any]
    requires_approval: bool = False


class AgentOrchestrator:
    """Governed routing and intelligence layer for PHOENIX specialist agents."""

    def __init__(self, registry: AgentRegistry | None = None, intelligence: IntelligenceLayer | None = None) -> None:
        self.registry = registry or build_default_registry()
        self.intelligence = intelligence or IntelligenceLayer()

    def plan(self, task: AgentTask) -> dict[str, Any]:
        candidates = self.registry.find_by_capability(task.capability)
        if not candidates:
            return {"status": "no_agent", "objective": task.objective, "capability": task.capability}
        selected = candidates[0]
        return {
            "status": "planned",
            "agent": selected.name,
            "version": selected.version,
            "objective": task.objective,
            "capability": task.capability,
            "human_approval_required": task.requires_approval or selected.human_approval_required,
        }

    def execute(self, task: AgentTask) -> dict[str, Any]:
        plan = self.plan(task)
        if plan["status"] != "planned":
            return plan
        if plan["human_approval_required"]:
            return {**plan, "status": "approval_required", "executed": False}
        response = self.intelligence.analyze(
            IntelligenceRequest(task.objective, task.context, plan["agent"])
        )
        return {**plan, "status": "completed", "executed": True, "intelligence": response}
