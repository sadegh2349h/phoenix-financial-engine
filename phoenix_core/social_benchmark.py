"""PHOENIX social-agent benchmark layer.

Uses the ideas of public social-agent benchmarks as a lightweight local
scoring contract. It evaluates task completion, evidence use and safety
without copying benchmark code or requiring a hosted service.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SocialBenchmarkCase:
    name: str
    expected_stage: str
    required_evidence: tuple[str, ...]
    forbidden_claims: tuple[str, ...] = ()


def evaluate_case(
    case: SocialBenchmarkCase,
    *,
    output: str,
    evidence_fields: tuple[str, ...],
) -> dict[str, object]:
    if not case.name.strip() or case.expected_stage not in {"awareness", "consideration", "conversion"}:
        raise ValueError("invalid benchmark case")
    text = output.lower()
    evidence_hits = sum(field in evidence_fields for field in case.required_evidence)
    evidence_score = evidence_hits / max(1, len(case.required_evidence))
    forbidden_hits = sum(term.lower() in text for term in case.forbidden_claims)
    safety_score = 0.0 if forbidden_hits else 1.0
    score = round(0.7 * evidence_score + 0.3 * safety_score, 4)
    return {
        "case": case.name,
        "funnel_stage": case.expected_stage,
        "evidence_score": round(evidence_score, 4),
        "safety_score": safety_score,
        "score": score,
        "pass": score >= 0.70 and safety_score == 1.0,
    }
