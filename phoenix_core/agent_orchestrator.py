from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .agents import AgentRegistry, build_default_registry
from .data_access import DataAccessLayer
from .intelligence import IntelligenceLayer, IntelligenceRequest
from .memory import MemoryStore


@dataclass(frozen=True)
class AgentTask:
    objective: str
    capability: str
    context: dict[str, Any]
    requires_approval: bool = False


class AgentOrchestrator:
    """Governed routing: data -> memory -> specialist -> intelligence -> review."""

    def __init__(self, registry: AgentRegistry | None = None,
                 intelligence: IntelligenceLayer | None = None,
                 data_access: DataAccessLayer | None = None,
                 memory: MemoryStore | None = None) -> None:
        self.registry = registry or build_default_registry()
        self.intelligence = intelligence or IntelligenceLayer()
        self.data_access = data_access or DataAccessLayer()
        self.memory = memory or MemoryStore()

    def plan(self, task: AgentTask) -> dict[str, Any]:
        candidates = self.registry.find_by_capability(task.capability)
        if not candidates:
            return {"status": "no_agent", "objective": task.objective, "capability": task.capability}
        selected = candidates[0]
        return {"status": "planned", "agent": selected.name, "version": selected.version,
                "objective": task.objective, "capability": task.capability,
                "human_approval_required": task.requires_approval or selected.human_approval_required}

    def execute(self, task: AgentTask) -> dict[str, Any]:
        plan = self.plan(task)
        if plan["status"] != "planned":
            return plan
        if plan["human_approval_required"]:
            return {**plan, "status": "approval_required", "executed": False}
        data = self.data_access.query(task.objective)
        memory_context = self.memory.context_for(task.objective)
        request = IntelligenceRequest(task.objective,
                                      {**task.context, "data": data, "memory": memory_context},
                                      plan["agent"])
        response = self.intelligence.analyze(request)
        result = {**plan, "status": "completed", "executed": True,
                  "data": data, "memory": memory_context, "intelligence": response}
        self.memory.put(f"decision:{task.objective}", {"agent": plan["agent"], "answer": response.answer,
                                                         "confidence": response.confidence})
        return result
