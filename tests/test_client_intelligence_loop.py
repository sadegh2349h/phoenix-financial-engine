from phoenix_core.action_engine import approval_gate, recommend_actions
from phoenix_core.client_intelligence_engine import ClientProfile, build_client_intelligence_package
from phoenix_core.customer_intelligence import SocialMetrics
from phoenix_core.measurement import record_measurement


def profile():
    return ClientProfile(
        client_id="client-loop", business_name="Loop Business",
        business_goal="increase leads", ideal_customer="local buyers",
        data_authorized=True, baseline={"conversion_rate": 0.10, "revenue_growth": 0.05},
    )


def test_full_client_package_is_evidence_first():
    result = build_client_intelligence_package(
        profile=profile(), social=SocialMetrics(reach=1000, views=700, saves=10),
        business={"revenue_growth": .05, "conversion_rate": .10, "retention_rate": .60, "margin": .30},
        objective="build trust with case study",
        actual={"conversion_rate": .12, "revenue_growth": .08},
        targets={"conversion_rate": .12},
    )
    assert result["status"] == "measurement_complete"
    assert result["decision_owner"] == "human"
    assert result["report"]["executive_summary"]["primary_bottleneck"] == "revenue_growth"
    assert result["measurement"]["targets"]["conversion_rate"]["met"] is True


def test_recommendations_require_human_approval():
    actions = recommend_actions({"business_health": {"weakest_metric": "margin"}})
    gate = approval_gate(actions)
    assert gate["status"] == "awaiting_human_approval"
    assert gate["approved"] is False


def test_measurement_compares_baseline_to_actual():
    result = record_measurement(baseline={"kpi": 100}, actual={"kpi": 120})
    assert result["changes"]["kpi"] == .2
