"""PHOENIX Social Acquisition Layer.

Multi-route acquisition for publicly exposed social evidence. Routes fail
closed: no login, credential bypass, challenge solving, or private-data access.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable
from urllib.parse import urlparse

from .browser_social_provider import fetch_public_social_profile_browser
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
        {"route": "public_http", "priority": 3, "authorization": "public_only", "enabled": True},
        {"route": "public_browser", "priority": 4, "authorization": "public_only", "enabled": True},
        {"route": "user_supplied", "priority": 5, "authorization": "user_supplied", "enabled": True},
        {"route": "visual_capture", "priority": 6, "authorization": "user_supplied", "enabled": True},
    )


def acquire_social_profile(
    url: str,
    *,
    adapter: Callable[[str], SocialProfileInput] | None = None,
    user_supplied: SocialProfileInput | None = None,
) -> AcquisitionResult:
    normalized = validate_social_url(url)
    if adapter is not None:
        return AcquisitionResult("acquired", "authorized_adapter", adapter(normalized), confidence=1.0)
    if user_supplied is not None:
        return AcquisitionResult("acquired", "user_supplied", user_supplied, confidence=1.0)

    errors: list[str] = []
    try:
        profile = fetch_public_social_profile(normalized)
        if profile is not None:
            return AcquisitionResult("acquired", "public_http", profile, confidence=0.75)
    except Exception as exc:
        errors.append(f"public_http: {exc}")

    try:
        profile = fetch_public_social_profile_browser(normalized)
        if profile is not None:
            return AcquisitionResult("acquired", "public_browser", profile, confidence=0.70)
    except Exception as exc:
        errors.append(f"public_browser: {exc}")

    return AcquisitionResult(
        "fallback_required", "public_gateway", None,
        "; ".join(errors) or "No public profile evidence was available.", 0.0,
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
    payload["intelligence"] = (
        build_social_intelligence_package(result.profile) if result.profile is not None else None
    )
    return payload
