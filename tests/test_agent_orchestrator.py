from phoenix_core.agent_orchestrator import AgentOrchestrator, AgentTask


def test_routes_capability_to_agent():
    orchestrator = AgentOrchestrator()
    plan = orchestrator.plan(AgentTask("analyze market", "market_analysis", {}))
    assert plan["status"] == "planned"
    assert plan["agent"] in {"financial_analyst", "marketing"}


def test_high_risk_agent_requires_approval():
    orchestrator = AgentOrchestrator()
    result = orchestrator.execute(AgentTask("research financial market", "financial_research", {}))
    assert result["status"] == "approval_required"
    assert result["executed"] is False


def test_unknown_capability_is_safe():
    orchestrator = AgentOrchestrator()
    result = orchestrator.plan(AgentTask("unknown", "does_not_exist", {}))
    assert result["status"] == "no_agent"
