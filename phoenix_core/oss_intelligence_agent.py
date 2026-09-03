"""PHOENIX OSS Intelligence Agent.

Provider-agnostic agent for discovering, evaluating and ranking open-source
capabilities before PHOENIX adopts them. It never installs dependencies,
executes third-party code, or approves adoption by itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .oss_intelligence import OSSPattern, adoption_score, oss_pattern_registry


@dataclass(frozen=True)
class OSSDiscoverySignal:
    name: str
    source: str
    capability: str
    evidence: str = ""
    maturity: float = 0.0
    relevance: float = 0.0


@dataclass(frozen=True)
class OSSEvaluation:
    name: str
    source: str
    score: float
    decision: str
    evidence: str
    human_approval_required: bool = True


@dataclass
class PhoenixOSSIntelligenceAgent:
    """Evidence-first OSS scout for PHOENIX."""

    name: str = "Phoenix OSS Intelligence Agent"
    approval_required: bool = True
    audit_log: list[dict[str, object]] = field(default_factory=list)

    def discover_candidates(self, signals: Iterable[OSSDiscoverySignal]) -> list[OSSDiscoverySignal]:
        candidates = sorted(
            signals,
            key=lambda s: (s.relevance, s.maturity),
            reverse=True,
        )
        self.audit_log.append({"action": "discover", "count": len(candidates)})
        return candidates

    def evaluate_candidate(
        self,
        signal: OSSDiscoverySignal,
        *,
        fit: float,
        security: float,
        maintenance: float,
        integration_cost: float,
        license_ok: bool = True,
    ) -> OSSEvaluation:
        result = adoption_score(
            fit=fit,
            security=security,
            maintenance=maintenance,
            integration_cost=integration_cost,
            license_ok=license_ok,
        )
        evaluation = OSSEvaluation(
            name=signal.name,
            source=signal.source,
            score=float(result["score"]),
            decision=str(result["decision"]),
            evidence=signal.evidence,
            human_approval_required=self.approval_required,
        )
        self.audit_log.append({"action": "evaluate", "name": signal.name, "score": evaluation.score})
        return evaluation

    def rank_candidates(self, evaluations: Iterable[OSSEvaluation]) -> list[OSSEvaluation]:
        ranked = sorted(evaluations, key=lambda item: item.score, reverse=True)
        self.audit_log.append({"action": "rank", "count": len(ranked)})
        return ranked

    def build_adoption_recommendation(self, evaluation: OSSEvaluation) -> dict[str, object]:
        return {
            "candidate": evaluation.name,
            "source": evaluation.source,
            "score": evaluation.score,
            "recommendation": evaluation.decision,
            "evidence": evaluation.evidence,
            "next_step": "human_review_and_approval",
            "auto_install": False,
            "execute_third_party_code": False,
        }

    def run(self, signals: Iterable[OSSDiscoverySignal]) -> dict[str, object]:
        discovered = self.discover_candidates(signals)
        evaluations = [
            self.evaluate_candidate(
                signal,
                fit=signal.relevance,
                security=signal.maturity,
                maintenance=signal.maturity,
                integration_cost=1.0 - signal.relevance,
            )
            for signal in discovered
        ]
        ranked = self.rank_candidates(evaluations)
        return {
            "agent": self.name,
            "candidates": [self.build_adoption_recommendation(item) for item in ranked],
            "approval_required": self.approval_required,
            "audit_events": len(self.audit_log),
        }


def default_oss_signals() -> list[OSSDiscoverySignal]:
    """Turn PHOENIX's curated OSS registry into agent discovery signals."""
    return [
        OSSDiscoverySignal(
            name=item["project"],
            source="curated_registry",
            capability=item["capability"],
            evidence=item["phoenix_target"],
            maturity=0.8,
            relevance=0.9,
        )
        for item in oss_pattern_registry()
    ]
