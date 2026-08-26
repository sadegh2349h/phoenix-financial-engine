from phoenix_core.agent_deliberation import AgentDeliberator


def test_agents_review_previous_proposals_and_reach_decision():
    d = AgentDeliberator()
    d.register("strategy", lambda ctx: {"view": "hold", "confidence": 0.8})
    d.register("risk", lambda ctx: {"risk": "medium", "confidence": 0.6})
    result = d.deliberate({"objective": "btc"}, rounds=2)
    assert result.rounds == 2
    assert result.decision["status"] == "decided"
    assert result.decision["confidence"] == 0.7


def test_empty_team_is_explicit():
    result = AgentDeliberator().deliberate({"objective": "x"})
    assert result.decision["status"] == "no_agents"
