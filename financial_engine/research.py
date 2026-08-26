from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class ResearchSummary:
    direction: str
    confidence: float
    aligned_timeframes: int
    total_timeframes: int
    notes: List[str]


def aggregate(assessments: Iterable[object]) -> ResearchSummary:
    rows = list(assessments)
    if not rows:
        return ResearchSummary("neutral", 0.0, 0, 0, ["No assessments available"])
    longs = sum(getattr(x, "direction", "neutral") == "long" for x in rows)
    shorts = sum(getattr(x, "direction", "neutral") == "short" for x in rows)
    direction = "long" if longs > shorts else "short" if shorts > longs else "neutral"
    confidence = sum(float(getattr(x, "confidence", 0)) for x in rows) / len(rows)
    aligned = max(longs, shorts)
    return ResearchSummary(direction, round(confidence, 2), aligned, len(rows), [f"{aligned}/{len(rows)} timeframes align"])
