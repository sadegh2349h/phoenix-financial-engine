"""PHOENIX coordination layer for specialists and external capabilities."""
from __future__ import annotations

from typing import Any

from .capability_registry import capability_registry
from .growth_specialist import build_growth_plan
from .specialist_router import route_specialists


def build_execution_plan(*, problem: str, analysis: dict[str, Any] | None = None, max_specialists: int = 2) -> dict[str, Any]:
    """Create a deterministic coordination plan; execution remains governed."""
    specialists = route_specialists(problem=problem, analysis=analysis, max_specialists=max_specialists)
    plan: dict[str, Any] = {
        "problem": problem,
        "specialists": specialists,
        "capabilities": capability_registry(),
        "sequence": ("observe", "remember", "route", "analyze", "deliberate", "human_approve", "execute", "monitor", "learn", "audit"),
        "decision_owner": "human",
        "telegram_notifications": False,
    }
    if any(item["key"] == "growth" for item in specialists):
        channel = str((analysis or {}).get("acquisition_channel", "digital channels"))
        goal = str((analysis or {}).get("business_goal", problem))
        plan["growth_plan"] = build_growth_plan(goal=goal, acquisition_channel=channel)
    return plan
