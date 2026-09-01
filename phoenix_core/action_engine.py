"""Deterministic, explainable action recommendations for PHOENIX clients."""
from __future__ import annotations

from typing import Any


def recommend_actions(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    """Return prioritized actions from measured bottlenecks; humans approve execution."""
    actions: list[dict[str, Any]] = []
    health = analysis.get("business_health", {})
    weakest = health.get("weakest_metric")
    mapping = {
        "conversion_rate": ("improve_conversion", "بهینه‌سازی مسیر تبدیل و دعوت به اقدام", "conversion_rate"),
        "retention_rate": ("improve_retention", "تقویت نگهداشت و بازگشت مشتری", "retention_rate"),
        "revenue_growth": ("improve_revenue", "تمرکز روی پیشنهاد و کانال‌های درآمدی مؤثر", "revenue_growth"),
        "margin": ("improve_margin", "بررسی قیمت‌گذاری، هزینه و ترکیب خدمات", "margin"),
    }
    if weakest in mapping:
        code, title, kpi = mapping[weakest]
        actions.append({"code": code, "title": title, "kpi": kpi, "priority": 1})

    content = analysis.get("content_score", {})
    if content.get("save_rate", 1.0) < 0.02:
        actions.append({"code": "increase_saves", "title": "تولید محتوای ذخیره‌پذیر", "kpi": "save_rate", "priority": 2})
    if content.get("retention", 1.0) < 0.50:
        actions.append({"code": "improve_retention", "title": "تقویت شروع و ریتم محتوا برای افزایش ماندگاری", "kpi": "retention", "priority": 2})
    return actions


def approval_gate(actions: list[dict[str, Any]]) -> dict[str, Any]:
    """Place recommendations behind an explicit human decision."""
    return {"status": "awaiting_human_approval", "actions": actions, "approved": False}
