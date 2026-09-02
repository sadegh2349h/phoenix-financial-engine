from phoenix_core.social_intelligence import SocialProfileInput, build_social_business_diagnosis, build_social_intelligence_package
from phoenix_core.phoenix_orchestrator import build_execution_plan


def test_social_engine_is_evidence_first():
    package = build_social_intelligence_package(SocialProfileInput(url="https://instagram.com/example"))
    assert package["no_claims_without_evidence"] is True
    assert package["analysis"]["fallback_required"] is True
    assert package["business_diagnosis"]["decision_owner"] == "human"


def test_social_engine_uses_authorized_insights_and_content():
    data = SocialProfileInput(
        url="https://instagram.com/example",
        username="example",
        bio="Specialist clinic | Book an appointment",
        followers=10000,
        posts=120,
        insights={"reach": 5000, "profile_visits": 250},
        content_samples=({"views": 1000, "saves": 20, "shares": 10}, {"reach": 800, "likes": 50}),
    )
    package = build_social_intelligence_package(data)
    assert package["analysis"]["content"]["data_coverage"] == 1.0
    assert package["analysis"]["confidence"]["overall"] == 1.0
    assert package["business_diagnosis"]["next_data_priority"].startswith("expand sample")


def test_orchestrator_reports_social_module_when_used():
    plan = build_execution_plan(
        problem="تحلیل پیج اینستاگرام و پیدا کردن گلوگاه جذب مشتری",
        social_profile=SocialProfileInput(url="https://instagram.com/example", bio="clinic"),
    )
    modules = [item["module"] for item in plan["active_modules"]]
    assert "PHOENIX Social Intelligence Engine" in modules
    assert "social_intelligence" in plan
    assert plan["decision_owner"] == "human"


def test_diagnosis_does_not_invent_a_primary_bottleneck():
    diagnosis = build_social_business_diagnosis(
        {
            "profile": {"bio": "x", "engagement_rate": 0.03},
            "content": {"data_coverage": 1.0},
            "confidence": {"overall": 0.75},
        }
    )
    assert diagnosis["primary_bottleneck"] == "insufficient evidence for a primary bottleneck"
