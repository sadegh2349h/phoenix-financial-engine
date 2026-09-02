"""PHOENIX coordination layer for specialists, social intelligence and capabilities."""
from __future__ import annotations

from typing import Any

from .capability_registry import capability_registry
from .growth_specialist import build_growth_plan
from .social_intelligence import SocialProfileInput, build_social_intelligence_package
from .specialist_router import route_specialists


def build_execution_plan(
    *,
    problem: str,
    analysis: dict[str, Any] | None = None,
    max_specialists: int = 2,
    social_profile: SocialProfileInput | None = None,
) -> dict[str, Any]:
    """Create a deterministic coordination plan; execution remains governed.

    Social intelligence is optional and evidence-first. When supplied, its
    findings become an input to routing and business diagnosis without claiming
    unavailable Instagram metrics.
    """
    social_package = build_social_intelligence_package(social_profile) if social_profile else None
    routing_analysis = dict(analysis or {})
    if social_package:
        routing_analysis["social_intelligence"] = social_package["business_diagnosis"]

    specialists = route_specialists(problem=problem, analysis=routing_analysis, max_specialists=max_specialists)
    active_modules = [
        {"module": "Phoenix Orchestrator", "role": "هماهنگی، ترتیب اجرا و کنترل حاکمیت"},
        *[
            {"module": item["specialist"], "role": item["reason"]}
            for item in specialists
        ],
    ]
    if social_package:
        active_modules.insert(1, {"module": "PHOENIX Social Intelligence Engine", "role": "جمع‌آوری شواهد مجاز، تحلیل پیج و تبدیل آن به تشخیص کسب‌وکار"})

    plan: dict[str, Any] = {
        "problem": problem,
        "active_modules": active_modules,
        "specialists": specialists,
        "capabilities": capability_registry(),
        "sequence": ("observe", "remember", "route", "analyze", "deliberate", "human_approve", "execute", "monitor", "learn", "audit"),
        "decision_owner": "human",
        "telegram_notifications": False,
    }
    if social_package:
        plan["social_intelligence"] = social_package
    if any(item["key"] == "growth" for item in specialists):
        channel = str((analysis or {}).get("acquisition_channel", "digital channels"))
        goal = str((analysis or {}).get("business_goal", problem))
        plan["growth_plan"] = build_growth_plan(goal=goal, acquisition_channel=channel)
    return plan
