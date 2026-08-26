from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    event: str
    status: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Monitor:
    """In-process operational telemetry and immutable-style audit records."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: str, status: str, **details: Any) -> AuditEvent:
        item = AuditEvent(event=event, status=status, details=dict(details))
        self._events.append(item)
        return item

    def recent(self, limit: int = 50) -> list[AuditEvent]:
        if limit < 1:
            raise ValueError("limit must be positive")
        return list(self._events[-limit:])

    def health(self) -> dict[str, Any]:
        failed = sum(1 for e in self._events if e.status in {"error", "failed"})
        return {"status": "degraded" if failed else "healthy", "events": len(self._events), "failures": failed}
