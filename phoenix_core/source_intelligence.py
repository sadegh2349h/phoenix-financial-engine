from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class SourceAssessment:
    source: str
    reliability: float
    freshness: float
    completeness: float
    weight: float


class SourceIntelligence:
    """Scores source quality so downstream analysis can weight evidence explicitly."""

    def assess(self, source: str, payload: dict[str, Any]) -> SourceAssessment:
        data = payload.get("data")
        completeness = 1.0 if data is not None else 0.0
        reliability = float(payload.get("reliability", 0.5))
        freshness = float(payload.get("freshness", 0.5))
        reliability = min(1.0, max(0.0, reliability))
        freshness = min(1.0, max(0.0, freshness))
        weight = round(reliability * freshness * completeness, 4)
        return SourceAssessment(source, reliability, freshness, completeness, weight)

    @staticmethod
    def rank(assessments: list[SourceAssessment]) -> list[SourceAssessment]:
        return sorted(assessments, key=lambda item: item.weight, reverse=True)
