from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Alert:
    level: str
    title: str
    message: str
    data: dict[str, Any]


class AlertEngine:
    """Policy-driven alert generation; delivery is delegated to connectors."""

    def __init__(self) -> None:
        self._rules: list[Callable[[dict[str, Any]], Alert | None]] = []

    def add_rule(self, rule: Callable[[dict[str, Any]], Alert | None]) -> None:
        self._rules.append(rule)

    def evaluate(self, event: dict[str, Any]) -> list[Alert]:
        alerts: list[Alert] = []
        for rule in self._rules:
            alert = rule(dict(event))
            if alert is not None:
                alerts.append(alert)
        return alerts

    @staticmethod
    def high_risk_rule(event: dict[str, Any]) -> Alert | None:
        if event.get("risk_level") in {"high", "critical"}:
            return Alert(event["risk_level"], "PHOENIX Risk Alert", "High-risk condition detected.", dict(event))
        return None
