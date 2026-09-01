from phoenix_core.customer_intelligence import (
    SocialMetrics,
    business_health,
    content_score,
    funnel_stage,
    lead_score,
    segment_customer,
)


def test_social_metrics_prioritize_saves_and_retention():
    result = content_score(SocialMetrics(reach=1000, views=1800, saves=120, shares=60, profile_visits=100, follows=12, dms=8))
    assert result["save_rate"] == 0.12
    assert result["retention"] == 1.0
    assert result["conversion_rate"] == 0.2


def test_funnel_stage_is_objective_driven():
    assert funnel_stage(objective="educate audience") == "awareness"
    assert funnel_stage(objective="compare alternatives and build trust") == "consideration"
    assert funnel_stage(objective="generate leads", promotional=True) == "conversion"


def test_lead_score_is_bounded_and_explainable():
    assert lead_score(intent=1, fit=1, engagement=1, recency=1) == 100
    assert lead_score(intent=0, fit=0, engagement=0, recency=0) == 0


def test_customer_segments():
    assert segment_customer(recency_days=10, frequency=5, monetary=100) == "loyal"
    assert segment_customer(recency_days=150, frequency=2, monetary=100) == "at_risk"
    assert segment_customer(recency_days=1, frequency=0, monetary=0) == "prospect"


def test_business_health_finds_bottleneck():
    result = business_health(revenue_growth=.2, conversion_rate=.05, retention_rate=.7, margin=.3)
    assert result["weakest_metric"] == "conversion_rate"
