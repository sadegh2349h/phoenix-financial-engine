from __future__ import annotations

from phoenix_core.alerting import AlertEngine
from phoenix_core.decision_engine import DecisionEngine
from phoenix_core.monitoring import Monitor
from phoenix_core.monitoring_alert_bridge import MonitoringAlertBridge
from phoenix_core.memory import MemoryStore
from phoenix_core.runtime import PhoenixRuntime
from phoenix_core.scheduler import Scheduler
from phoenix_core.scheduled_execution import ScheduledExecution
from phoenix_core.agent_orchestrator import AgentOrchestrator, AgentTask


def test_phoenix_operational_chain_is_governed_and_observable(tmp_path):
    """Exercise the core operational path without external side effects."""
    monitor = Monitor()
    alerts = AlertEngine()
    received = []
    alerts.register_channel("smoke", lambda alert: received.append(alert))
    bridge = MonitoringAlertBridge(monitor, alerts)

    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("heartbeat", 60, lambda: {"ok": True})
    memory = MemoryStore(tmp_path / "memory.json")
    runtime = PhoenixRuntime(execution, monitor, memory)

    cycle = runtime.tick()

    assert cycle.status == "healthy"
    assert cycle.runs[0]["name"] == "heartbeat"
    assert cycle.runs[0]["result"] == {"ok": True}
    assert cycle.health["status"] == "healthy"
    assert memory.context_for("heartbeat")
    assert bridge.health()["status"] == "healthy"

    monitor.record("operational.smoke", "failed", {"task": "synthetic-check"})
    assert len(received) == 1
    assert received[0].severity == "warning"
    assert received[0].metadata["task"] == "synthetic-check"

    governed = AgentOrchestrator().execute(
        AgentTask("research financial market", "financial_research", {})
    )
    assert governed["status"] == "approval_required"
    assert governed["executed"] is False

    decision = DecisionEngine().evaluate(
        agent_results=[{"status": "completed", "requires_human_review": True}],
        risk_level="high",
    )
    assert decision.status == "ready"
    assert decision.requires_human_approval is True
    assert decision.confidence == 1.0
