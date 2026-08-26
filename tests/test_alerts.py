from phoenix_core.alerts import AlertEngine


def test_high_risk_alert_is_generated():
    engine = AlertEngine()
    engine.add_rule(AlertEngine.high_risk_rule)
    alerts = engine.evaluate({"risk_level": "high", "asset": "BTC"})
    assert len(alerts) == 1
    assert alerts[0].level == "high"


def test_low_risk_does_not_alert():
    engine = AlertEngine()
    engine.add_rule(AlertEngine.high_risk_rule)
    assert engine.evaluate({"risk_level": "low"}) == []
