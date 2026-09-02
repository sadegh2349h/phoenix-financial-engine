"""PHOENIX evidence acquisition contract for social profiles."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
from urllib.parse import urlparse

SOURCES = ("official_api", "public_data", "user_supplied", "visual_input", "authorized_insights")

@dataclass(frozen=True)
class AcquisitionRequest:
    url: str
    requested_sources: tuple[str, ...] = SOURCES

@dataclass(frozen=True)
class AcquisitionEvidence:
    source: str
    field: str
    value: Any
    confidence: float = 1.0

def validate_url(url: str) -> dict[str, str]:
    if not url or not url.strip():
        raise ValueError("url is required")
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url must be an absolute http(s) URL")
    return {"scheme": parsed.scheme.lower(), "host": parsed.netloc.lower().split(":", 1)[0], "path": parsed.path.rstrip("/"), "url": url.strip()}

def build_acquisition_plan(request: AcquisitionRequest) -> dict[str, Any]:
    normalized = validate_url(request.url)
    sources = tuple(dict.fromkeys(request.requested_sources))
    unknown = tuple(s for s in sources if s not in SOURCES)
    if unknown:
        raise ValueError(f"unsupported source(s): {', '.join(unknown)}")
    priority = {name: index + 1 for index, name in enumerate(sources)}
    routes = [{"source": name, "priority": priority[name], "status": "adapter_required" if name in {"official_api", "public_data"} else "ready"} for name in sources]
    return {"url": normalized["url"], "normalized": normalized, "routes": routes, "human_review_required": True, "evidence_first": True, "no_private_access": True, "no_credential_bypass": True}

def normalize_evidence(items: list[AcquisitionEvidence]) -> dict[str, Any]:
    for item in items:
        if item.source not in SOURCES:
            raise ValueError(f"unsupported evidence source: {item.source}")
    fields = {item.field for item in items}
    return {"evidence": [asdict(item) for item in items], "field_coverage": len(fields), "ready_for_social_intelligence": bool(items), "confidence": min(1.0, 0.2 + 0.1 * len(fields)) if items else 0.0}

def build_social_acquisition_package(request: AcquisitionRequest) -> dict[str, Any]:
    return {"engine": "PHOENIX Social Acquisition Layer", "version": "1.0", "plan": build_acquisition_plan(request), "handoff": "acquisition -> evidence_normalizer -> social_intelligence -> business_diagnosis", "human_decision_required": True}
