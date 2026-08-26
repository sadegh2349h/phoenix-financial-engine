from phoenix_core.monitoring import Monitor


def test_monitor_records_events_and_reports_health():
    monitor = Monitor()
    monitor.record("agent.execute", "success", agent="financial_analyst")
    monitor.record("decision.gate", "failed", reason="low confidence")
    assert monitor.health() == {"status": "degraded", "events": 2, "failures": 1}
    assert monitor.recent(1)[0].event == "decision.gate"
