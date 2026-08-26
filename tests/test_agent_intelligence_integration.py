from phoenix_core.agent_orchestrator import AgentOrchestrator, AgentTask


def test_low_risk_task_reaches_intelligence_layer():
    result = AgentOrchestrator().execute(
        AgentTask("create a growth plan", "growth_strategy", {})
    )
    assert result["status"] == "completed"
    assert result["executed"] is True
    assert result["intelligence"].provider == "rule-based"


def test_financial_task_stays_human_governed():
    result = AgentOrchestrator().execute(
        AgentTask("analyze financial market", "financial_research", {})
    )
    assert result["status"] == "approval_required"
    assert result["executed"] is False
