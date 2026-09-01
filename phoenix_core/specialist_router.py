"""PHOENIX specialist registry and evidence-based routing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Specialist:
    key: str
    name: str
    domain: str
    primary_signals: tuple[str, ...]
    deliverables: tuple[str, ...]


SPECIALISTS: tuple[Specialist, ...] = (
    Specialist("psyche", "Phoenix Psyche", "consumer psychology and behavioral economics",
               ("ideal_customer", "hidden_objection", "purchase_fear", "identity_shift", "messaging"),
               ("psychographic_hypotheses", "core_desire", "hidden_objection", "psychological_trigger", "messaging_angle")),
    Specialist("ops", "Phoenix Ops", "operations and systems thinking",
               ("repetitive_task", "bottleneck", "workflow", "automation", "delegation", "sop"),
               ("process_map", "bottleneck", "automation", "delegation", "sop", "success_metrics")),
    Specialist("brand", "Phoenix Brand", "positioning and premium brand strategy",
               ("competitors", "positioning", "misconception", "unfair_advantage", "uvp", "brand_voice"),
               ("positioning_statement", "brand_voice", "visual_identity_direction", "content_pillars")),
    Specialist("closer", "Phoenix Closer", "high-ticket sales and negotiation",
               ("objection", "price_resistance", "closing", "negotiation", "value_alignment", "pricing"),
               ("objection_scripts", "value_reframe", "low_pressure_next_step", "tiered_pricing")),
)

_PERSIAN_ALIASES: dict[str, tuple[str, ...]] = {
    "psyche": ("مشتری ایده آل", "مخاطب", "ترس", "اعتراض پنهان", "خواسته", "هویت", "پیام"),
    "ops": ("تکراری", "گلوگاه", "فرآیند", "فرایند", "اتوماسیون", "واگذاری", "دستورالعمل"),
    "brand": ("رقیب", "رقبا", "جایگاه برند", "جایگاه", "تصویر برند", "مزیت رقابتی", "پیام برند"),
    "closer": ("اعتراض", "قیمت", "فروش", "بستن فروش", "مذاکره", "ارزش", "قیمت گذاری"),
}


def specialist_registry() -> dict[str, dict[str, Any]]:
    return {s.key: {"name": s.name, "domain": s.domain, "primary_signals": s.primary_signals,
                    "deliverables": s.deliverables} for s in SPECIALISTS}


def route_specialists(*, problem: str, analysis: dict[str, Any] | None = None,
                      max_specialists: int = 2) -> list[dict[str, Any]]:
    """Rank specialists from problem/evidence; recommendation remains human-approved."""
    if not problem or not problem.strip():
        raise ValueError("problem is required")
    if max_specialists < 1:
        raise ValueError("max_specialists must be >= 1")
    haystack = f"{problem} {' '.join(str(v) for v in (analysis or {}).values())}".lower()
    ranked: list[tuple[int, Specialist, list[str]]] = []
    for specialist in SPECIALISTS:
        signals = tuple(specialist.primary_signals) + _PERSIAN_ALIASES[specialist.key]
        matched = [signal for signal in signals if signal.replace("_", " ") in haystack or signal in haystack]
        if matched:
            ranked.append((len(matched), specialist, matched))
    ranked.sort(key=lambda item: (-item[0], item[1].key))
    return [{"specialist": s.name, "key": s.key, "score": score,
             "matched_signals": tuple(matches), "reason": f"matched {len(matches)} evidence signal(s)",
             "human_approval_required": True} for score, s, matches in ranked[:max_specialists]]


def enrich_client_package(package: dict[str, Any], *, problem: str,
                          max_specialists: int = 2) -> dict[str, Any]:
    enriched = dict(package)
    enriched["specialist_routing"] = route_specialists(problem=problem, analysis=package.get("analysis", {}),
                                                        max_specialists=max_specialists)
    enriched["specialist_decision_owner"] = "human"
    return enriched
