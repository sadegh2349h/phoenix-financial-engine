"""PHOENIX coordination layer for specialists and external capabilities."""
from __future__ import annotations

from typing import Any

from .capability_registry import capability_registry
from .growth_specialist import build_growth_plan
from .specialist_router import route_specialists


def build_execution_plan(*, problem: str, analysis: dict[str, Any] | None = None, max_specialists: int = 2) -> dict[str, Any]:
    """Create a deterministic coordination plan; execution remains governed.

    Every operational plan explicitly reports which PHOENIX modules are active
    and what role each active module has in the task.
    """
    specialists = route_specialists(problem=problem, analysis=analysis, max_specialists=max_specialists)
    active_modules = [
        {"module": "Phoenix Orchestrator", "role": "هماهنگی، ترتیب اجرا و کنترل حاکمیت"},
        *[
            {"module": item["specialist"], "role": item["reason"]}
            for item in specialists
        ],
    ]
    plan: dict[str, Any] = {
        "problem": problem,
        "active_modules": active_modules,
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
