from __future__ import annotations

from typing import Any

from .alerting import AlertEngine
from .monitoring import Monitor, MonitorEvent


class MonitoringAlertBridge:
    """Bridges health events to PHOENIX notification channels."""

    def __init__(self, monitor: Monitor, alerts: AlertEngine) -> None:
        self.monitor = monitor
        self.alerts = alerts
        self.monitor.add_alert(self._on_event)

    def _on_event(self, event: MonitorEvent) -> None:
        severity = "critical" if event.status == "critical" else "warning"
        alert = self.alerts.build(
            severity=severity,
            title=f"PHOENIX: {event.name}",
            message=f"System event status: {event.status}",
            metadata={"timestamp": event.timestamp, **event.details},
        )
        self.alerts.dispatch(alert)

    def health(self) -> dict[str, Any]:
        return self.monitor.health()
