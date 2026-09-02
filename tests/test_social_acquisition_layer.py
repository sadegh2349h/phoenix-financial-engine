from phoenix_core.social_acquisition_layer import (
    acquire_social_profile,
    analyze_social_url,
    validate_social_url,
)
from phoenix_core.social_intelligence import SocialProfileInput


def test_validate_social_url():
    assert validate_social_url(" https://www.instagram.com/example/ ") == "https://www.instagram.com/example"


def test_no_adapter_uses_explicit_fallback():
    result = acquire_social_profile("https://www.instagram.com/example")
    assert result.status == "fallback_required"
    assert result.profile is None
    assert result.confidence == 0.0


def test_user_supplied_data_flows_into_intelligence():
    profile = SocialProfileInput(
        url="https://www.instagram.com/example",
        username="example",
        bio="Example business",
        followers=1000,
        content_samples=({"views": 100, "likes": 10},),
    )
    result = analyze_social_url(profile.url, user_supplied=profile)
    assert result["acquisition"]["status"] == "acquired"
    assert result["intelligence"]["engine"] == "PHOENIX Social Intelligence Engine"
    assert result["intelligence"]["analysis"]["content"]["measurable_sample_count"] == 1
