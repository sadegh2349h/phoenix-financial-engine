"""PHOENIX Instagram public acquisition layer.

Evidence-first acquisition with ordered fallbacks. No authentication bypass,
credential harvesting, challenge solving, or private-data access is performed.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class AcquisitionResult:
    source: str
    status: str
    profile_url: str
    data: dict[str, Any]
    evidence: tuple[dict[str, Any], ...] = ()
    error: str | None = None


PUBLIC_SOURCES = ("public_http", "public_browser", "authorized_provider", "user_supplied")


def _http_profile(url: str, timeout: int = 12) -> AcquisitionResult:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return AcquisitionResult(
                source="public_http",
                status="success",
                profile_url=url,
                data={"html": body, "content_type": response.headers.get("Content-Type")},
                evidence=({"source": "public_http", "field": "html", "confidence": 0.9},),
            )
    except Exception as exc:  # network/provider failures are expected fallback conditions
        return AcquisitionResult("public_http", "failed", url, {}, error=str(exc))


def acquire_instagram_profile(
    url: str,
    *,
    authorized_provider: Callable[[str], AcquisitionResult] | None = None,
    public_browser: Callable[[str], AcquisitionResult] | None = None,
) -> dict[str, Any]:
    """Acquire public/authorized evidence using deterministic fallbacks.

    The function never treats an unavailable source as evidence and never
    fabricates profile/content metrics.
    """
    attempts: list[AcquisitionResult] = []

    if authorized_provider is not None:
        result = authorized_provider(url)
        attempts.append(result)
        if result.status == "success":
            return {"status": "success", "selected_source": result.source,
                    "data": result.data, "evidence": list(result.evidence),
                    "attempts": [asdict(x) for x in attempts]}

    result = _http_profile(url)
    attempts.append(result)
    if result.status == "success":
        return {"status": "success", "selected_source": result.source,
                "data": result.data, "evidence": list(result.evidence),
                "attempts": [asdict(x) for x in attempts]}

    if public_browser is not None:
        result = public_browser(url)
        attempts.append(result)
        if result.status == "success":
            return {"status": "success", "selected_source": result.source,
                    "data": result.data, "evidence": list(result.evidence),
                    "attempts": [asdict(x) for x in attempts]}

    return {"status": "unavailable", "selected_source": None, "data": {},
            "evidence": [], "attempts": [asdict(x) for x in attempts],
            "next_action": "connect an authorized provider or public browser adapter"}
