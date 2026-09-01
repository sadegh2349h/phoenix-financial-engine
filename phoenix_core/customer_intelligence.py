"""Customer, marketing and social-media intelligence primitives for PHOENIX.

These are provider-agnostic building blocks: they do not scrape Instagram or
make psychological diagnoses. They operate on data supplied by authorized
connectors and return explainable scores for human review.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SocialMetrics:
    reach: int = 0
    views: int = 0
    saves: int = 0
    shares: int = 0
    comments: int = 0
    profile_visits: int = 0
    follows: int = 0
    dms: int = 0

    def retention_proxy(self) -> float:
        return min(1.0, self.views / max(self.reach, 1))

    def save_rate(self) -> float:
        return self.saves / max(self.reach, 1)

    def share_rate(self) -> float:
        return self.shares / max(self.reach, 1)

    def conversion_rate(self) -> float:
        return (self.follows + self.dms) / max(self.profile_visits, 1)


def content_score(metrics: SocialMetrics) -> dict[str, float]:
    """Prioritize retention/saves while keeping conversion visible."""
    return {
        "retention": round(metrics.retention_proxy(), 4),
        "save_rate": round(metrics.save_rate(), 4),
        "share_rate": round(metrics.share_rate(), 4),
        "conversion_rate": round(metrics.conversion_rate(), 4),
    }


def funnel_stage(*, objective: str, promotional: bool = False) -> str:
    text = objective.lower()
    if promotional or any(k in text for k in ("buy", "book", "purchase", "lead", "dm")):
        return "conversion"
    if any(k in text for k in ("compare", "evaluate", "trust", "case study", "proof")):
        return "consideration"
    return "awareness"


def lead_score(*, intent: float, fit: float, engagement: float, recency: float) -> float:
    """Explainable 0-100 lead score; weights are intentionally transparent."""
    values = [max(0.0, min(1.0, x)) for x in (intent, fit, engagement, recency)]
    score = 100 * (0.40 * values[0] + 0.30 * values[1] + 0.20 * values[2] + 0.10 * values[3])
    return round(score, 2)


def segment_customer(*, recency_days: int, frequency: int, monetary: float) -> str:
    """Simple RFM-style segmentation suitable for service businesses."""
    if recency_days <= 30 and frequency >= 3 and monetary > 0:
        return "loyal"
    if recency_days <= 60 and frequency >= 1:
        return "active"
    if recency_days > 120 and frequency > 0:
        return "at_risk"
    if frequency == 0:
        return "prospect"
    return "developing"


def business_health(*, revenue_growth: float, conversion_rate: float,
                    retention_rate: float, margin: float) -> dict[str, Any]:
    """Compact operating-health snapshot for PHOENIX client diagnostics."""
    metrics = {
        "revenue_growth": revenue_growth,
        "conversion_rate": conversion_rate,
        "retention_rate": retention_rate,
        "margin": margin,
    }
    return {
        "metrics": metrics,
        "weakest_metric": min(metrics, key=metrics.get),
        "priority": "fix_bottleneck",
    }
