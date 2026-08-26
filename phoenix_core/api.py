from __future__ import annotations

from typing import Any

from .agents import build_default_registry
from .agent_orchestrator import AgentOrchestrator, AgentTask
from .decision_engine import DecisionEngine
from .monitoring import Monitor
from .risk_engine import RiskEngine


class PhoenixService:
    """Application-facing service boundary; transport/framework agnostic."""

    def __init__(self) -> None:
        self.monitor = Monitor()
        self.orchestrator = AgentOrchestrator(registry=build_default_registry())
        self.risk = RiskEngine()
        self.decisions = DecisionEngine()

    def health(self) -> dict[str, Any]:
        return {"service": "phoenix", "status": self.monitor.health()["status"], "monitor": self.monitor.health()}

    def analyze(self, objective: str, capability: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        self.monitor.record("analysis.start", "success", objective=objective, capability=capability)
        try:
            result = self.orchestrator.execute(AgentTask(objective, capability, context or {}))
            self.monitor.record("analysis.complete", "success", status=result.get("status"))
            return result
        except Exception as exc:
            self.monitor.record("analysis.complete", "error", error=type(exc).__name__)
            raise
