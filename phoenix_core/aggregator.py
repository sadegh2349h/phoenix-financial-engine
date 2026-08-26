from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .data_access import DataAccessLayer


@dataclass(frozen=True)
class SourceResult:
    source: str
    data: Any
    available: bool
    error: str | None = None


class MultiSourceAggregator:
    """Collects independent sources without allowing one failure to hide others."""

    def __init__(self, access: DataAccessLayer) -> None:
        self.access = access

    def collect(self, query: str) -> list[SourceResult]:
        results: list[SourceResult] = []
        for name, payload in self.access.query(query).items():
            results.append(SourceResult(
                source=name,
                data=payload.get("data"),
                available=payload.get("data") is not None,
            ))
        return results

    @staticmethod
    def summary(results: list[SourceResult]) -> dict[str, Any]:
        available = [r.source for r in results if r.available]
        return {
            "source_count": len(results),
            "available_sources": available,
            "coverage": round(len(available) / len(results), 4) if results else 0.0,
        }
