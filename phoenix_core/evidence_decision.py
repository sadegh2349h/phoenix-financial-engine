from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .aggregator import SourceResult
from .memory import MemoryStore
from .source_intelligence import SourceIntelligence


@dataclass(frozen=True)
class DecisionRecord:
    objective: str
    decision: str
    confidence: float
    evidence: list[dict[str, Any]]


class EvidenceDecisionEngine:
    """Turns multi-source evidence into an auditable decision record."""

    def __init__(self, memory: MemoryStore, source_intelligence: SourceIntelligence | None = None) -> None:
        self.memory = memory
        self.source_intelligence = source_intelligence or SourceIntelligence()

    def decide(self, objective: str, results: list[SourceResult]) -> DecisionRecord:
        evidence = [
            {"source": item.source, "available": item.available, "data": item.data}
            for item in results
        ]
        available = [item for item in results if item.available]
        confidence = round(len(available) / len(results), 4) if results else 0.0
        decision = "proceed" if confidence >= 0.5 else "insufficient_evidence"
        record = DecisionRecord(objective, decision, confidence, evidence)
        self.memory.put(f"decision:{objective}", {
            "decision": decision,
            "confidence": confidence,
            "evidence": evidence,
        })
        return record
