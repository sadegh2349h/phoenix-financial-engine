from financial_engine.financial_intelligence import Evidence, Scenario, decide


def test_low_quality_data_cannot_produce_trade():
    decision = decide(
        Evidence(90, 90, 90, 90, 90, 50),
        [Scenario("bull", 0.9, 10.0, "break below support")],
        risk_reward=2.0,
    )
    assert decision.action == "NO_TRADE"


def test_high_quality_multi_factor_setup_can_be_candidate():
    decision = decide(
        Evidence(90, 80, 75, 80, 90, 95),
        [Scenario("bull", 0.8, 8.0, "loss of structure")],
        risk_reward=2.2,
    )
    assert decision.action == "TRADE_CANDIDATE"
    assert decision.confidence == 0.76
