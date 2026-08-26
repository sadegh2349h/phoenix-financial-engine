from phoenix_core.decision_engine import DecisionEngine


def test_decision_engine_is_conservative_for_high_risk():
    decision = DecisionEngine().evaluate(
        agent_results=[{"status": "completed", "requires_human_review": True}],
        risk_level="high",
    )
    assert decision.status == "ready"
    assert decision.requires_human_approval is True
    assert decision.confidence == 1.0


def test_decision_engine_rejects_empty_evidence():
    decision = DecisionEngine().evaluate(agent_results=[])
    assert decision.status == "insufficient_data"
    assert decision.requires_human_approval is True
