"""PHOENIX Instagram profile analysis contract.

Builds a comprehensive, evidence-first diagnosis from public or authorized
Instagram evidence. Acquisition is intentionally separated from analysis so
PHOENIX can use public HTTP/browser, authorized providers, or user-supplied
captures without bypassing authentication or platform controls.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlparse


DIMENSIONS = (
    "identity_and_positioning",
    "profile_conversion",
    "audience_and_offer",
    "content_strategy",
    "content_quality",
    "hook_and_copy",
    "funnel_and_cta",
    "engagement",
    "growth",
    "visual_brand",
    "consistency",
    "competitors",
    "conversion",
    "risks_and_compliance",
)


@dataclass(frozen=True)
class InstagramEvidence:
    source: str
    field: str
    value: Any
    confidence: float = 1.0


def validate_instagram_url(url: str) -> str:
    parsed = urlparse((url or "").strip())
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {
        "instagram.com", "www.instagram.com"
    }:
        raise ValueError("url must be an Instagram profile URL")
    path = parsed.path.strip("/")
    if not path or path.startswith(("p/", "reel/", "tv/", "explore/")):
        raise ValueError("url must point to a profile, not a post or explore page")
    return f"https://www.instagram.com/{path.split('/')[0]}/"


def _coverage(profile: dict[str, Any]) -> float:
    available = 0
    total = 0
    for key in ("username", "bio", "followers", "following", "posts", "engagement_rate"):
        total += 1
        if profile.get(key) is not None:
            available += 1
    samples = profile.get("content_samples", ())
    total += 1
    if samples:
        available += 1
    competitors = profile.get("competitor_samples", ())
    total += 1
    if competitors:
        available += 1
    insights = profile.get("insights")
    total += 1
    if insights:
        available += 1
    return round(available / total, 4)


def analyze_instagram_profile(
    *,
    url: str,
    username: str | None = None,
    bio: str | None = None,
    followers: int | None = None,
    following: int | None = None,
    posts: int | None = None,
    engagement_rate: float | None = None,
    insights: dict[str, Any] | None = None,
    content_samples: tuple[dict[str, Any], ...] = (),
    competitor_samples: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Return a full diagnostic contract without inventing unavailable data."""
    normalized = validate_instagram_url(url)
    profile = {
        "username": username,
        "bio": bio,
        "followers": followers,
        "following": following,
        "posts": posts,
        "engagement_rate": engagement_rate,
        "content_samples": content_samples,
        "competitor_samples": competitor_samples,
        "insights": insights or {},
    }
    coverage = _coverage(profile)
    evidence: list[InstagramEvidence] = []
    for key, value in profile.items():
        if key not in {"content_samples", "competitor_samples", "insights"} and value is not None:
            evidence.append(InstagramEvidence("public_or_authorized", key, value))
    for key, value in (insights or {}).items():
        evidence.append(InstagramEvidence("authorized_insights", key, value))

    sample_metrics = {"views", "reach", "likes", "comments", "saves", "shares"}
    measurable_posts = sum(1 for item in content_samples if sample_metrics.intersection(item))
    content_coverage = round(measurable_posts / len(content_samples), 4) if content_samples else 0.0

    strengths: list[str] = []
    gaps: list[str] = []
    if bio:
        strengths.append("profile messaging evidence available")
    else:
        gaps.append("bio/positioning unavailable")
    if content_samples:
        strengths.append("content sample available")
    else:
        gaps.append("recent content sample unavailable")
    if insights:
        strengths.append("authorized performance insights available")
    else:
        gaps.append("native Insights unavailable")
    if competitor_samples:
        strengths.append("competitor evidence available")
    else:
        gaps.append("competitor sample unavailable")

    dimensions = {dimension: {"status": "requires_analysis", "evidence": []} for dimension in DIMENSIONS}
    dimensions["identity_and_positioning"]["evidence"] = ["bio", "username"]
    dimensions["profile_conversion"]["evidence"] = ["bio", "profile_visits", "link_clicks"]
    dimensions["audience_and_offer"]["evidence"] = ["audience", "offer", "insights"]
    dimensions["content_strategy"]["evidence"] = ["content_samples", "content_pillars"]
    dimensions["content_quality"]["evidence"] = ["views", "reach", "saves", "shares", "comments"]
    dimensions["hook_and_copy"]["evidence"] = ["captions", "first_frame", "first_seconds"]
    dimensions["funnel_and_cta"]["evidence"] = ["cta", "funnel_stage", "profile_actions"]
    dimensions["engagement"]["evidence"] = ["likes", "comments", "saves", "shares", "engagement_rate"]
    dimensions["growth"]["evidence"] = ["followers", "reach", "non_follower_reach", "trend"]
    dimensions["visual_brand"]["evidence"] = ["media", "palette", "typography", "composition"]
    dimensions["consistency"]["evidence"] = ["dates", "posting_frequency", "format_mix"]
    dimensions["competitors"]["evidence"] = ["competitor_samples"]
    dimensions["conversion"]["evidence"] = ["profile_actions", "leads", "sales"]
    dimensions["risks_and_compliance"]["evidence"] = ["claims", "copyright", "disclosures"]

    return {
        "engine": "PHOENIX Instagram Profile Analyzer",
        "version": "1.0",
        "url": normalized,
        "scope": "profile + content + funnel + performance + brand + competitors + conversion + risk",
        "profile": {k: v for k, v in profile.items() if k not in {"content_samples", "competitor_samples", "insights"}},
        "coverage": {
            "overall": coverage,
            "content_metrics": content_coverage,
            "content_sample_count": len(content_samples),
            "competitor_sample_count": len(competitor_samples),
        },
        "dimensions": dimensions,
        "evidence": [asdict(item) for item in evidence],
        "strengths": strengths,
        "gaps": gaps,
        "required_for_deep_audit": (
            "public profile + recent posts/reels + captions + visible metrics; "
            "authorized Insights when available; competitor sample for benchmarking"
        ),
        "no_claims_without_evidence": True,
        "human_review_required": True,
        "source_policy": "public, authorized, or user-supplied evidence only",
    }


def build_instagram_audit_plan(url: str) -> dict[str, Any]:
    """Create the acquisition/analysis checklist for a supplied profile URL."""
    normalized = validate_instagram_url(url)
    return {
        "url": normalized,
        "acquisition_order": ("official_api", "authorized_provider", "public_http", "public_browser", "user_supplied", "visual_capture"),
        "analysis_order": DIMENSIONS,
        "minimum_deep_audit": {
            "profile": True,
            "recent_content": 10,
            "reels": True,
            "stories": "when supplied/authorized",
            "insights": "when authorized",
            "competitors": 3,
        },
        "human_review_required": True,
    }
