"""PHOENIX Social Intelligence Engine.

Provider-agnostic social-profile intelligence with explicit fallbacks.
The engine never claims unavailable metrics; it records source and confidence.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class SocialEvidence:
    source: str
    field: str
    value: Any
    confidence: float = 1.0


@dataclass(frozen=True)
class SocialProfileInput:
    url: str
    username: str | None = None
    bio: str | None = None
    followers: int | None = None
    following: int | None = None
    posts: int | None = None
    engagement_rate: float | None = None
    insights: dict[str, Any] | None = None
    content_samples: tuple[dict[str, Any], ...] = ()
    competitor_samples: tuple[dict[str, Any], ...] = ()


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def analyze_profile(data: SocialProfileInput) -> dict[str, Any]:
    """Build an evidence-backed diagnosis from whatever authorized data exists."""
    if not data.url or not data.url.strip():
        raise ValueError("url is required")

    evidence: list[SocialEvidence] = []
    if data.bio is not None:
        evidence.append(SocialEvidence("user_or_provider", "bio", data.bio))
    for field in ("followers", "following", "posts", "engagement_rate"):
        value = getattr(data, field)
        if value is not None:
            evidence.append(SocialEvidence("user_or_provider", field, value))
    if data.insights:
        for key, value in data.insights.items():
            evidence.append(SocialEvidence("authorized_insights", key, value, 1.0))

    content_count = len(data.content_samples)
    measurable_content = sum(
        1 for item in data.content_samples
        if any(k in item for k in ("views", "reach", "likes", "saves", "shares", "comments"))
    )
    content_data_coverage = _clamp(measurable_content / content_count) if content_count else 0.0

    profile_score = None
    if data.bio is not None:
        profile_score = _clamp((min(len(data.bio), 150) / 150) * 0.5 + (0.5 if data.username else 0.0))

    return {
        "url": data.url,
        "profile": {
            "username": data.username,
            "bio": data.bio,
            "followers": data.followers,
            "following": data.following,
            "posts": data.posts,
            "engagement_rate": data.engagement_rate,
            "profile_completeness_proxy": profile_score,
        },
        "content": {
            "sample_count": content_count,
            "measurable_sample_count": measurable_content,
            "data_coverage": content_data_coverage,
        },
        "competitors": {
            "sample_count": len(data.competitor_samples),
        },
        "evidence": [asdict(item) for item in evidence],
        "confidence": {
            "overall": _clamp(0.25 + 0.25 * bool(data.bio) + 0.25 * bool(data.content_samples) + 0.25 * bool(data.insights)),
            "rule": "confidence reflects supplied/authorized evidence coverage, not model certainty",
        },
        "fallback_required": not bool(data.insights or data.content_samples),
        "human_review_required": True,
    }


def build_social_business_diagnosis(analysis: dict[str, Any]) -> dict[str, Any]:
    """Translate social evidence into business-oriented bottleneck hypotheses."""
    profile = analysis["profile"]
    content = analysis["content"]
    hypotheses: list[dict[str, Any]] = []

    if profile.get("bio") is None:
        hypotheses.append({"bottleneck": "profile messaging visibility", "reason": "bio evidence unavailable", "confidence": 0.35})
    if content["data_coverage"] < 0.5:
        hypotheses.append({"bottleneck": "content performance visibility", "reason": "insufficient measurable content sample", "confidence": 0.5})
    if profile.get("engagement_rate") is not None and profile["engagement_rate"] < 0.01:
        hypotheses.append({"bottleneck": "engagement", "reason": "reported engagement rate below 1%", "confidence": 0.85})

    return {
        "primary_bottleneck": hypotheses[0]["bottleneck"] if hypotheses else "insufficient evidence for a primary bottleneck",
        "hypotheses": hypotheses,
        "evidence_coverage": content["data_coverage"],
        "confidence": analysis["confidence"]["overall"],
        "next_data_priority": (
            "authorized Insights + 10-20 recent posts/reels + 3 competitors"
            if analysis["fallback_required"]
            else "expand sample and validate hypotheses against business outcomes"
        ),
        "decision_owner": "human",
    }


def build_social_intelligence_package(data: SocialProfileInput) -> dict[str, Any]:
    analysis = analyze_profile(data)
    diagnosis = build_social_business_diagnosis(analysis)
    return {
        "engine": "PHOENIX Social Intelligence Engine",
        "version": "1.0",
        "analysis": analysis,
        "business_diagnosis": diagnosis,
        "source_policy": "provider-agnostic; authorized/public/user-supplied evidence only",
        "no_claims_without_evidence": True,
        "human_decision_required": True,
    }
