import pytest

from phoenix_core.instagram_profile_analyzer import (
    analyze_instagram_profile,
    build_instagram_audit_plan,
    validate_instagram_url,
)


def test_profile_url_is_normalized():
    assert validate_instagram_url("https://www.instagram.com/example/?x=1") == "https://www.instagram.com/example/"


def test_post_url_is_rejected():
    with pytest.raises(ValueError):
        validate_instagram_url("https://www.instagram.com/p/ABC123/")


def test_audit_plan_covers_full_social_scope():
    plan = build_instagram_audit_plan("https://instagram.com/example")
    assert "content_strategy" in plan["analysis_order"]
    assert "conversion" in plan["analysis_order"]
    assert plan["minimum_deep_audit"]["recent_content"] == 10
    assert plan["minimum_deep_audit"]["competitors"] == 3


def test_analyzer_is_evidence_first():
    result = analyze_instagram_profile(
        url="https://instagram.com/example",
        username="example",
        bio="Business profile",
        followers=10000,
        posts=100,
        content_samples=({"views": 1000, "saves": 20, "shares": 10},),
    )
    assert result["no_claims_without_evidence"] is True
    assert result["coverage"]["content_metrics"] == 1.0
    assert result["human_review_required"] is True
    assert len(result["dimensions"]) == 14


def test_analyzer_marks_missing_insights_and_competitors():
    result = analyze_instagram_profile(url="https://instagram.com/example")
    assert "native Insights unavailable" in result["gaps"]
    assert "competitor sample unavailable" in result["gaps"]
    assert result["coverage"]["overall"] < 0.5
