from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Evidence:
    technical: float
    fundamental: float
    sentiment: float
    flow: float
    regime: float
    data_quality: float

    @property
    def composite(self) -> float:
        # Fundamental/sentiment/flow are deliberately explicit inputs. Missing
        # evidence is not silently treated as positive evidence.
        weights = (0.25, 0.20, 0.15, 0.15, 0.15, 0.10)
        values = (self.technical, self.fundamental, self.sentiment, self.flow, self.regime, self.data_quality)
        return round(sum(w * max(0.0, min(100.0, v)) for w, v in zip(weights, values)), 2)


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: float
    expected_return_pct: float
    invalidation: str


@dataclass(frozen=True)
class FinancialDecision:
    action: str
    confidence: float
    evidence_score: float
    scenarios: tuple[Scenario, ...]
    risk_reward: float | None
    rationale: tuple[str, ...]


def decide(
    evidence: Evidence,
    scenarios: list[Scenario],
    *,
    risk_reward: float | None = None,
    minimum_confidence: float = 0.65,
) -> FinancialDecision:
    scenarios = sorted(scenarios, key=lambda s: s.probability, reverse=True)
    best = scenarios[0] if scenarios else None
    confidence = (best.probability if best else 0.0) * (evidence.data_quality / 100.0)
    reasons: list[str] = []
    if evidence.data_quality < 70:
        reasons.append("insufficient_data_quality")
    if best is None:
        reasons.append("no_valid_scenario")
    if risk_reward is not None and risk_reward < 1.5:
        reasons.append("unfavorable_risk_reward")
    if confidence < minimum_confidence:
        reasons.append("insufficient_confidence")
    if reasons:
        action = "NO_TRADE"
    elif best.expected_return_pct > 0:
        action = "TRADE_CANDIDATE"
    else:
        action = "WAIT"
    return FinancialDecision(
        action=action,
        confidence=round(confidence, 4),
        evidence_score=evidence.composite,
        scenarios=tuple(scenarios),
        risk_reward=risk_reward,
        rationale=tuple(reasons) if reasons else ("multi_factor_confirmation",),
    )


def report(decision: FinancialDecision) -> dict[str, Any]:
    return {
        "action": decision.action,
        "confidence": decision.confidence,
        "evidence_score": decision.evidence_score,
        "risk_reward": decision.risk_reward,
        "rationale": list(decision.rationale),
        "scenarios": [
            {
                "name": s.name,
                "probability": s.probability,
                "expected_return_pct": s.expected_return_pct,
                "invalidation": s.invalidation,
            }
            for s in decision.scenarios
        ],
    }
