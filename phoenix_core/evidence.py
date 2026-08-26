from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .source_intelligence import SourceAssessment, SourceIntelligence


@dataclass(frozen=True)
class EvidenceBundle:
    assessments: list[SourceAssessment]
    confidence: float
    warnings: list[str]


class EvidenceEngine:
    """Turns multi-source quality scores into an explicit evidence confidence."""

    def __init__(self, source_intelligence: SourceIntelligence | None = None) -> None:
        self.source_intelligence = source_intelligence or SourceIntelligence()

    def evaluate(self, sources: dict[str, dict[str, Any]]) -> EvidenceBundle:
        assessments = [
            self.source_intelligence.assess(name, payload)
            for name, payload in sources.items()
        ]
        total_weight = sum(item.weight for item in assessments)
        confidence = round(total_weight / len(assessments), 4) if assessments else 0.0
        warnings: list[str] = []
        if not assessments:
            warnings.append("no evidence sources available")
        elif confidence < 0.4:
            warnings.append("evidence confidence is low")
        return EvidenceBundle(
            assessments=self.source_intelligence.rank(assessments),
            confidence=confidence,
            warnings=warnings,
        )
