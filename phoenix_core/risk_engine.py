from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_LEVELS = {"low": 0, "medium": 1, "high": 2, "critical": 3}


@dataclass(frozen=True)
class RiskAssessment:
    level: str
    score: float
    reasons: tuple[str, ...]
    blocked: bool


class RiskEngine:
    """Deterministic safety gate for PHOENIX decisions and actions."""

    def assess(self, *, decision: Any, requested_action: str | None = None,
               minimum_level: str = "high") -> RiskAssessment:
        reasons: list[str] = []
        level = "low"
        if requested_action:
            level = "medium"
            reasons.append("external action requested")
        if getattr(decision, "requires_human_approval", False):
            level = "high"
            reasons.append("human approval required by decision")
        confidence = float(getattr(decision, "confidence", 0.0))
        if confidence < 0.5:
            level = max(level, "high", key=lambda x: _LEVELS[x])
            reasons.append("low decision confidence")
        blocked = _LEVELS[level] >= _LEVELS.get(minimum_level, 2)
        return RiskAssessment(level, round(1.0 - confidence, 4), tuple(reasons) or ("no elevated risk detected",), blocked)
