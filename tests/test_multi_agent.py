from phoenix_core.agents import build_default_registry
from phoenix_core.multi_agent import MultiAgentCoordinator


def test_multi_agent_synthesis_requires_review_for_financial_risk():
    result = MultiAgentCoordinator(build_default_registry()).analyze(
        task="market review",
        capabilities=["market_analysis", "risk_analysis"],
        risk_level="high",
    )
    assert result["status"] == "ready"
    assert "financial_analyst" in result["agents"]
    assert result["decision"].requires_human_approval is True


def test_multi_agent_deduplicates_specialists():
    result = MultiAgentCoordinator(build_default_registry()).analyze(
        task="strategy review",
        capabilities=["market_analysis", "financial_research", "risk_analysis"],
    )
    assert len(result["agents"]) == len(set(result["agents"]))
