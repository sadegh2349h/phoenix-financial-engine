import pytest

from phoenix_core.client_intelligence_engine import ClientProfile, assess_readiness, build_client_baseline, run_authorized_analysis
from phoenix_core.customer_intelligence import SocialMetrics


def ready_profile() -> ClientProfile:
    return ClientProfile(
        client_id="client-1",
        business_name="Demo Business",
        business_goal="increase qualified leads",
        ideal_customer="local service customers",
        services=("service",),
        channels=("instagram",),
        data_authorized=True,
    )


def test_onboarding_blocks_analysis_without_authorization():
    profile = ready_profile()
    profile = ClientProfile(**{**profile.__dict__, "data_authorized": False})
    status, missing = assess_readiness(profile)
    assert status == "needs_setup"
    assert "data_authorization" in missing
    with pytest.raises(ValueError):
        run_authorized_analysis(profile=profile)


def test_ready_client_gets_repeatable_capability_plan():
    result = build_client_baseline(ready_profile())
    assert result.readiness == "ready"
    assert "content_funnel_intelligence" in result.capabilities
    assert "measurement_loop" in result.capabilities
    assert result.next_actions[0] == "capture_baseline_kpis"


def test_authorized_analysis_combines_core_modules():
    result = run_authorized_analysis(
        profile=ready_profile(),
        social=SocialMetrics(reach=1000, views=1200, saves=100, shares=40),
        objective="build trust with case study",
        lead={"intent": .8, "fit": .9, "engagement": .5, "recency": 1},
    )
    assert result["status"] == "analyzed"
    assert result["funnel_stage"] == "consideration"
    assert result["lead_score"] == 81
    assert result["content_score"]["save_rate"] == .1
