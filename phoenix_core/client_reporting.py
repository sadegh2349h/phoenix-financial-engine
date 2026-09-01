"""Customer-facing reporting layer for the PHOENIX intelligence pipeline."""
from __future__ import annotations

from typing import Any


def build_client_report(*, profile: Any, analysis: dict[str, Any], actions: list[dict[str, Any]], measurement: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a concise evidence-first report without making decisions for the client."""
    health = analysis.get("business_health", {})
    return {
        "client_id": profile.client_id,
        "business_name": profile.business_name,
        "status": "analysis_complete" if measurement is None else "measurement_complete",
        "executive_summary": {"goal": profile.business_goal, "primary_bottleneck": health.get("weakest_metric")},
        "data_used": sorted(profile.baseline.keys()),
        "baseline": dict(profile.baseline),
        "evidence": {k: v for k, v in analysis.items() if k != "client_id"},
        "opportunities": actions,
        "measurement": measurement,
        "decision_owner": "human",
        "next_step": "human_approval" if actions else "collect_more_evidence",
    }
