from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Alert:
    severity: str
    title: str
    message: str
    metadata: dict[str, Any]


class AlertEngine:
    """Routes actionable events to registered notification channels."""

    def __init__(self) -> None:
        self._channels: dict[str, Callable[[Alert], Any]] = {}

    def register_channel(self, name: str, handler: Callable[[Alert], Any]) -> None:
        if name in self._channels:
            raise ValueError(f"channel already registered: {name}")
        self._channels[name] = handler

    def build(self, *, severity: str, title: str, message: str, metadata: dict[str, Any] | None = None) -> Alert:
        if severity not in {"info", "warning", "critical"}:
            raise ValueError("invalid severity")
        return Alert(severity, title, message, dict(metadata or {}))

    def dispatch(self, alert: Alert, channels: list[str] | None = None) -> dict[str, str]:
        targets = channels or list(self._channels)
        result: dict[str, str] = {}
        for name in targets:
            handler = self._channels.get(name)
            if handler is None:
                result[name] = "unavailable"
                continue
            try:
                handler(alert)
                result[name] = "sent"
            except Exception:
                result[name] = "failed"
        return result
