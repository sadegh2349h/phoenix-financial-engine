"""PHOENIX Opportunity Engine.

Converts signals from markets, customers, competitors and social channels into
ranked, evidence-backed opportunities. It recommends; humans decide.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class OpportunitySignal:
    source: str
    title: str
    evidence: str
    impact: float = 0.0
    confidence: float = 0.0
    urgency: float = 0.0
    effort: float = 0.0

@dataclass(frozen=True)
class Opportunity:
    title: str
    source: str
    score: float
    evidence: str
    action: str
    human_approval_required: bool = True

class OpportunityEngine:
    def __init__(self, approval_required: bool = True) -> None:
        self.approval_required = approval_required

    def detect(self, signals: Iterable[OpportunitySignal]) -> list[Opportunity]:
        results = []
        for s in signals:
            score = round(max(0.0, min(1.0, (s.impact * .35 + s.confidence * .30 + s.urgency * .20 + (1-s.effort) * .15))), 4)
            action = "prioritize_and_test" if score >= .70 else "investigate" if score >= .45 else "monitor"
            results.append(Opportunity(s.title, s.source, score, s.evidence, action, self.approval_required))
        return sorted(results, key=lambda x: x.score, reverse=True)

    def run(self, signals: Iterable[OpportunitySignal]) -> dict[str, object]:
        opportunities = self.detect(signals)
        return {"engine": "Opportunity Engine", "opportunities": [o.__dict__ for o in opportunities], "decision_owner": "human"}
