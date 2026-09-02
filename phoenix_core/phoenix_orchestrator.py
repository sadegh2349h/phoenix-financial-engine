"""PHOENIX coordination layer for specialists and external capabilities."""
from __future__ import annotations

from typing import Any

from .capability_registry import capability_registry
from .specialist_router import route_specialists


def build_execution_plan(*, problem: str, analysis: dict[str, Any] | None = None, max_specialists: int = 2) -> dict[str, Any]:
    """Create a deterministic coordination plan; execution remains governed."""
    specialists = route_specialists(problem=problem, analysis=analysis, max_specialists=max_specialists)
    return {
        "problem": problem,
        "specialists": specialists,
        "capabilities": capability_registry(),
        "sequence": ("observe", "remember", "route", "analyze", "deliberate", "human_approve", "execute", "monitor", "learn", "audit"),
        "decision_owner": "human",
        "telegram_notifications": False,
    }
