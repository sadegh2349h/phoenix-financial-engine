"""KPI measurement loop for PHOENIX client engagements."""
from __future__ import annotations

from typing import Any


def record_measurement(*, baseline: dict[str, float], actual: dict[str, float], targets: dict[str, float] | None = None) -> dict[str, Any]:
    """Compare actual KPIs with baseline and optional targets."""
    keys = sorted(set(baseline) | set(actual))
    changes: dict[str, float | None] = {}
    for key in keys:
        before = baseline.get(key)
        after = actual.get(key)
        changes[key] = None if before in (None, 0) or after is None else round((after - before) / abs(before), 4)
    target_results = {}
    for key, target in (targets or {}).items():
        value = actual.get(key)
        target_results[key] = {"target": target, "actual": value, "met": value is not None and value >= target}
    return {"status": "measurement_complete", "baseline": dict(baseline), "actual": dict(actual), "changes": changes, "targets": target_results}


def next_measurement_status(*, action_active: bool, measurement_due: bool) -> str:
    if action_active and measurement_due:
        return "measurement_due"
    if action_active:
        return "action_active"
    return "ready_for_next_action"
