from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Connector:
    name: str
    capability: str
    handler: Callable[[dict[str, Any]], Any]
    enabled: bool = True


class ConnectorRegistry:
    """Controlled adapter registry for external apps, APIs, and AI services."""

    def __init__(self) -> None:
        self._connectors: dict[str, Connector] = {}

    def register(self, connector: Connector) -> None:
        if connector.name in self._connectors:
            raise ValueError(f"connector already registered: {connector.name}")
        self._connectors[connector.name] = connector

    def available(self, capability: str | None = None) -> list[str]:
        return [c.name for c in self._connectors.values()
                if c.enabled and (capability is None or c.capability == capability)]

    def invoke(self, name: str, payload: dict[str, Any]) -> Any:
        connector = self._connectors.get(name)
        if connector is None or not connector.enabled:
            raise ValueError(f"connector unavailable: {name}")
        return connector.handler(dict(payload))
