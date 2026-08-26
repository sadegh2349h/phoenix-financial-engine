from phoenix_core.alerting import AlertEngine
from phoenix_core.monitoring import Monitor
from phoenix_core.monitoring_alert_bridge import MonitoringAlertBridge


def test_monitoring_event_reaches_registered_alert_channel():
    monitor = Monitor()
    alerts = AlertEngine()
    received = []
    alerts.register_channel("test", lambda alert: received.append(alert))
    MonitoringAlertBridge(monitor, alerts)
    monitor.record("scheduler", "failed", {"task": "market-watch"})
    assert len(received) == 1
    assert received[0].severity == "warning"
    assert received[0].metadata["task"] == "market-watch"
