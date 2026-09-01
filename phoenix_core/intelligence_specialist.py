"""PHOENIX Intelligence specialist: market, competitor and signal intelligence."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntelligenceBrief:
    question: str
    signals: tuple[str, ...]
    patterns: tuple[str, ...]
    implications: tuple[str, ...]
    recommended_next_step: str
    confidence: float
    human_approval_required: bool = True


def synthesize_intelligence(*, question: str, signals: list[str], patterns: list[str], implications: list[str], recommended_next_step: str, confidence: float) -> IntelligenceBrief:
    if not question or not question.strip():
        raise ValueError("question is required")
    if not signals:
        raise ValueError("signals are required")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return IntelligenceBrief(question, tuple(signals), tuple(patterns), tuple(implications), recommended_next_step, confidence)

FRAMEWORKS = ("Market Intelligence", "Competitive Intelligence", "Signal Analysis", "Scenario Thinking")
