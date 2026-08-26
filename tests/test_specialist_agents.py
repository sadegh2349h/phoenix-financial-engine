from phoenix_core.agents import build_default_registry
from phoenix_core.specialist_agents import default_agent_names


def test_default_specialist_agents_are_registered():
    registry = build_default_registry()
    names = tuple(agent.name for agent in registry.list())

    assert set(names) == set(default_agent_names())
    assert len(names) == 9


def test_capability_lookup_returns_specialists():
    registry = build_default_registry()
    matches = registry.find_by_capability("market_analysis")

    assert {agent.name for agent in matches} == {"marketing", "financial_analyst"}


def test_financial_agent_is_governed():
    registry = build_default_registry()
    result = registry.run("financial_analyst", task="research")

    assert result["status"] == "ready"
    assert result["autonomous_action"] is False
    assert "human approval" in result["governance"]
