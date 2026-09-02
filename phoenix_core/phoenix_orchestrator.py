"""PHOENIX coordination layer for specialists, social acquisition and intelligence."""
from __future__ import annotations

from typing import Any, Callable

from .capability_registry import capability_registry
from .growth_specialist import build_growth_plan
from .social_acquisition import AcquisitionRequest, build_social_acquisition_package
from .social_acquisition_layer import analyze_social_url
from .social_intelligence import SocialProfileInput, build_social_intelligence_package
from .specialist_router import route_specialists


def build_execution_plan(
    *,
    problem: str,
    analysis: dict[str, Any] | None = None,
    max_specialists: int = 2,
    social_profile: SocialProfileInput | None = None,
    social_url: str | None = None,
    social_adapter: Callable[[str], SocialProfileInput] | None = None,
) -> dict[str, Any]:
    """Create a deterministic coordination plan; execution remains human-governed."""
    social_package = build_social_intelligence_package(social_profile) if social_profile else None
    acquisition_package = build_social_acquisition_package(AcquisitionRequest(social_url)) if social_url else None
    live_social_analysis = analyze_social_url(social_url, adapter=social_adapter) if social_url else None

    routing_analysis = dict(analysis or {})
    if social_package:
        routing_analysis["social_intelligence"] = social_package["business_diagnosis"]
    if live_social_analysis and live_social_analysis.get("intelligence"):
        routing_analysis["social_intelligence"] = live_social_analysis["intelligence"]["business_diagnosis"]

    specialists = route_specialists(problem=problem, analysis=routing_analysis, max_specialists=max_specialists)
    active_modules = [
        {"module": "Phoenix Orchestrator", "role": "هماهنگی، ترتیب اجرا و کنترل حاکمیت"},
        *[{"module": item["specialist"], "role": item["reason"]} for item in specialists],
    ]
    if acquisition_package:
        active_modules.insert(1, {"module": "PHOENIX Social Acquisition Layer", "role": "دریافت و تعیین مسیر شواهد مجاز"})
    if live_social_analysis:
        active_modules.insert(1, {"module": "PHOENIX Social URL Analyzer", "role": "اتصال URL به دریافت شواهد و موتور تحلیل"})
    if social_package or (live_social_analysis and live_social_analysis.get("intelligence")):
        active_modules.insert(1, {"module": "PHOENIX Social Intelligence Engine", "role": "تحلیل شواهد اجتماعی و تبدیل آن به تشخیص کسب‌وکار"})

    plan: dict[str, Any] = {
        "problem": problem,
        "active_modules": active_modules,
        "specialists": specialists,
        "capabilities": capability_registry(),
        "sequence": ("observe", "acquire", "normalize", "remember", "route", "analyze", "deliberate", "human_approve", "execute", "monitor", "learn", "audit"),
        "decision_owner": "human",
        "telegram_notifications": False,
    }
    if acquisition_package:
        plan["social_acquisition"] = acquisition_package
    if live_social_analysis:
        plan["social_url_analysis"] = live_social_analysis
    if social_package:
        plan["social_intelligence"] = social_package
    if any(item["key"] == "growth" for item in specialists):
        channel = str((analysis or {}).get("acquisition_channel", "digital channels"))
        goal = str((analysis or {}).get("business_goal", problem))
        plan["growth_plan"] = build_growth_plan(goal=goal, acquisition_channel=channel)
    return plan
