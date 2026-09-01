"""PHOENIX Opportunity specialist: evidence-based opportunity discovery."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Opportunity:
    signal: str
    opportunity: str
    evidence: tuple[str, ...]
    value_hypothesis: str
    recommended_action: str
    risk: str
    human_approval_required: bool = True


def discover_opportunity(*, signal: str, opportunity: str, evidence: list[str], value_hypothesis: str, recommended_action: str, risk: str) -> Opportunity:
    if any(not value or not value.strip() for value in (signal, opportunity, value_hypothesis, recommended_action, risk)):
        raise ValueError("all opportunity fields are required")
    if not evidence:
        raise ValueError("evidence is required")
    return Opportunity(signal, opportunity, tuple(evidence), value_hypothesis, recommended_action, risk)

FRAMEWORKS = ("Opportunity Detection", "Pattern Recognition", "Anomaly Detection", "Evidence-Based Prioritization")
