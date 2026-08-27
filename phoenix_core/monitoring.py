from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass(frozen=True)
class AuditEvent:
    event: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


MonitorEvent = AuditEvent


class Monitor:
    """In-process operational telemetry with alert hooks and audit records."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._alerts: list[Callable[[AuditEvent], Any]] = []

    def add_alert(self, handler: Callable[[AuditEvent], Any]) -> None:
        self._alerts.append(handler)

    def record(self, event: str, status: str, details: dict[str, Any] | None = None, **extra: Any) -> AuditEvent:
        """Record an event and notify alert hooks for failure states."""
        payload = dict(details or {})
        payload.update(extra)
        item = AuditEvent(event=event, status=status, details=payload)
        self._events.append(item)
        if status in {"error", "failed", "critical"}:
            for alert in self._alerts:
                try:
                    alert(item)
                except Exception:
                    pass
        return item

    def recent(self, limit: int = 50) -> list[AuditEvent]:
        if limit < 1:
            raise ValueError("limit must be positive")
        return list(self._events[-limit:])

    def health(self) -> dict[str, Any]:
        failed = sum(1 for e in self._events if e.status in {"error", "failed"})
        critical = sum(1 for e in self._events if e.status == "critical")
        return {
            "status": "critical" if critical else ("degraded" if failed else "healthy"),
            "events": len(self._events),
            "failures": failed,
        }
