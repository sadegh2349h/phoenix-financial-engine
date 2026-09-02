"""PHOENIX Social Acquisition Layer.

Acquires only publicly exposed profile evidence. No login, credential bypass,
or private Insights access is attempted. Rich metrics still require an
authorized provider or user-supplied evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable
from urllib.parse import urlparse

from .public_social_provider import fetch_public_social_profile
from .social_intelligence import SocialProfileInput, build_social_intelligence_package


@dataclass(frozen=True)
class AcquisitionResult:
    status: str
    source: str
    profile: SocialProfileInput | None = None
    message: str = ""
    confidence: float = 0.0


def validate_social_url(url: str) -> str:
    if not url or not url.strip():
        raise ValueError("url is required")
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url must be an absolute HTTP(S) URL")
    return url.strip().rstrip("/")


def acquisition_routes() -> tuple[dict[str, Any], ...]:
    return (
        {"route": "official_api", "priority": 1, "authorization": "required", "enabled": False},
        {"route": "authorized_provider", "priority": 2, "authorization": "required", "enabled": False},
        {"route": "public_evidence", "priority": 3, "authorization": "public_only", "enabled": True},
        {"route": "user_supplied", "priority": 4, "authorization": "user_supplied", "enabled": True},
        {"route": "visual_capture", "priority": 5, "authorization": "user_supplied", "enabled": True},
    )


def acquire_social_profile(
    url: str,
    *,
    adapter: Callable[[str], SocialProfileInput] | None = None,
    user_supplied: SocialProfileInput | None = None,
) -> AcquisitionResult:
    normalized = validate_social_url(url)
    if adapter is not None:
        profile = adapter(normalized)
        return AcquisitionResult("acquired", "authorized_adapter", profile, confidence=1.0)
    if user_supplied is not None:
        return AcquisitionResult("acquired", "user_supplied", user_supplied, confidence=1.0)
    try:
        profile = fetch_public_social_profile(normalized)
    except Exception as exc:
        return AcquisitionResult("fallback_required", "public_evidence", None, str(exc), 0.0)
    if profile is not None:
        return AcquisitionResult("acquired", "public_evidence", profile, confidence=0.75)
    return AcquisitionResult(
        "fallback_required", "public_evidence", None,
        "Public profile evidence was not available from the target response.", 0.0,
    )


def analyze_social_url(
    url: str,
    *,
    adapter: Callable[[str], SocialProfileInput] | None = None,
    user_supplied: SocialProfileInput | None = None,
) -> dict[str, Any]:
    result = acquire_social_profile(url, adapter=adapter, user_supplied=user_supplied)
    payload: dict[str, Any] = {
        "acquisition": asdict(result),
        "routes": acquisition_routes(),
        "human_decision_required": True,
    }
    if result.profile is not None:
        payload["intelligence"] = build_social_intelligence_package(result.profile)
    else:
        payload["intelligence"] = None
    return payload
