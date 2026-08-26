from dataclasses import asdict
from typing import List
from .contracts import Event


class AuditLog:
    """Append-oriented in-process audit log; durable backends can implement the same contract later."""

    def __init__(self) -> None:
        self._events: List[Event] = []

    def append(self, event: Event) -> None:
        self._events.append(event)

    def recent(self, limit: int = 100) -> List[dict]:
        return [asdict(e) for e in self._events[-limit:]]
