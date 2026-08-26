from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .data_access import DataAccessLayer
from .monitoring import Monitor


@dataclass(frozen=True)
class DataSnapshot:
    query: str
    sources: dict[str, Any]
    complete: bool


class DataPipeline:
    """Normalizes data acquisition into an auditable PHOENIX snapshot."""

    def __init__(self, access: DataAccessLayer, monitor: Monitor | None = None) -> None:
        self.access = access
        self.monitor = monitor or Monitor()

    def collect(self, query: str) -> DataSnapshot:
        if not query.strip():
            raise ValueError("query must not be empty")
        self.monitor.record("data.collect.start", "success", query=query)
        try:
            sources = self.access.query(query)
            complete = bool(sources) and all("data" in item for item in sources.values())
            snapshot = DataSnapshot(query=query, sources=sources, complete=complete)
            self.monitor.record("data.collect.complete", "success", complete=complete, source_count=len(sources))
            return snapshot
        except Exception as exc:
            self.monitor.record("data.collect.complete", "error", error=type(exc).__name__)
            raise
