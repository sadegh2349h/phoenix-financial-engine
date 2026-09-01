"""PHOENIX client-intelligence onboarding and decision-support pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .action_engine import recommend_actions
from .client_reporting import build_client_report
from .customer_intelligence import business_health, content_score, funnel_stage, lead_score, segment_customer
from .measurement import record_measurement


@dataclass(frozen=True)
class ClientProfile:
    client_id: str
    business_name: str
    business_goal: str
    ideal_customer: str
    services: tuple[str, ...] = ()
    channels: tuple[str, ...] = ()
    data_authorized: bool = False
    baseline: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IntelligenceResult:
    client_id: str
    readiness: str
    missing_inputs: tuple[str, ...]
    capabilities: tuple[str, ...]
    next_actions: tuple[str, ...]
    evidence: dict[str, Any]


def assess_readiness(profile: ClientProfile) -> tuple[str, tuple[str, ...]]:
    missing: list[str] = []
    if not profile.client_id.strip(): missing.append("client_id")
    if not profile.business_name.strip(): missing.append("business_name")
    if not profile.business_goal.strip(): missing.append("business_goal")
    if not profile.ideal_customer.strip(): missing.append("ideal_customer")
    if not profile.data_authorized: missing.append("data_authorization")
    return ("ready" if not missing else "needs_setup", tuple(missing))


def build_client_baseline(profile: ClientProfile) -> IntelligenceResult:
    readiness, missing = assess_readiness(profile)
    if readiness != "ready":
        return IntelligenceResult(profile.client_id, readiness, missing, (), ("complete_client_intake", "confirm_data_authorization"), {})
    capabilities = ("social_performance", "content_funnel_intelligence", "lead_scoring", "customer_segmentation", "business_health", "action_recommendation", "measurement_loop", "client_reporting")
    actions = ("capture_baseline_kpis", "identify_primary_bottleneck", "map_content_to_funnel", "create_first_measurable_action", "schedule_result_review")
    return IntelligenceResult(profile.client_id, "ready", (), capabilities, actions, dict(profile.baseline))


def run_authorized_analysis(*, profile: ClientProfile, social: Any | None = None,
                            business: dict[str, float] | None = None,
                            lead: dict[str, float] | None = None,
                            customer: dict[str, float] | None = None,
                            objective: str | None = None) -> dict[str, Any]:
    """Run analysis only after intake and data authorization."""
    readiness, missing = assess_readiness(profile)
    if readiness != "ready": raise ValueError(f"Client is not ready: {', '.join(missing)}")
    result: dict[str, Any] = {"client_id": profile.client_id, "status": "analyzed"}
    if social is not None: result["content_score"] = content_score(social)
    if business is not None: result["business_health"] = business_health(**business)
    if lead is not None: result["lead_score"] = lead_score(**lead)
    if customer is not None: result["customer_segment"] = segment_customer(**customer)
    if objective is not None: result["funnel_stage"] = funnel_stage(objective=objective)
    return result


def build_client_intelligence_package(*, profile: ClientProfile, social: Any | None = None,
                                      business: dict[str, float] | None = None,
                                      lead: dict[str, float] | None = None,
                                      customer: dict[str, float] | None = None,
                                      objective: str | None = None,
                                      actual: dict[str, float] | None = None,
                                      targets: dict[str, float] | None = None) -> dict[str, Any]:
    """Run the full client loop: analysis -> actions -> report -> measurement."""
    baseline = build_client_baseline(profile)
    if baseline.readiness != "ready":
        return {"status": "needs_setup", "onboarding": baseline}
    analysis = run_authorized_analysis(profile=profile, social=social, business=business, lead=lead, customer=customer, objective=objective)
    actions = recommend_actions(analysis)
    measurement = None
    if actual is not None:
        measurement = record_measurement(baseline={k: float(v) for k, v in profile.baseline.items() if isinstance(v, (int, float))}, actual=actual, targets=targets)
    report = build_client_report(profile=profile, analysis=analysis, actions=actions, measurement=measurement)
    return {"status": report["status"], "onboarding": baseline, "analysis": analysis, "actions": actions, "report": report, "measurement": measurement, "decision_owner": "human"}
