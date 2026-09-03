"""PHOENIX prediction and scenario engine.

Builds transparent scenarios from weighted signals; it does not claim certainty.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class ForecastSignal:
    name: str
    direction: float
    strength: float
    evidence: str

@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    outlook: float
    evidence: tuple[str, ...]

class PredictionScenarioEngine:
    def build(self, signals: Iterable[ForecastSignal]) -> list[Scenario]:
        items = list(signals)
        if not items:
            return []
        raw = sum(max(0.0, min(1.0, s.strength)) for s in items) or 1.0
        outlook = sum(s.direction * s.strength for s in items) / raw
        positive = max(0.0, min(1.0, .5 + outlook * .5))
        negative = 1.0 - positive
        evidence = tuple(s.evidence for s in items if s.evidence)
        return [
            Scenario("upside", round(positive, 4), round(outlook, 4), evidence),
            Scenario("downside", round(negative, 4), round(-outlook, 4), evidence),
        ]

    def run(self, signals: Iterable[ForecastSignal]) -> dict[str, object]:
        scenarios = self.build(signals)
        return {"engine": "Prediction & Scenario Engine", "scenarios": [s.__dict__ for s in scenarios], "certainty": "not_guaranteed", "decision_owner": "human"}
