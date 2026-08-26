from phoenix_core.alerting import AlertEngine


def test_alert_dispatches_to_registered_channel():
    delivered = []
    engine = AlertEngine()
    engine.register_channel("test", lambda alert: delivered.append(alert.title))
    alert = engine.build(severity="critical", title="PHOENIX", message="action required")
    assert engine.dispatch(alert) == {"test": "sent"}
    assert delivered == ["PHOENIX"]


def test_unavailable_channel_is_reported():
    engine = AlertEngine()
    alert = engine.build(severity="warning", title="x", message="y")
    assert engine.dispatch(alert, ["push"]) == {"push": "unavailable"}
