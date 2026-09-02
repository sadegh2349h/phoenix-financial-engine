from phoenix_core.social_acquisition_layer import acquire_social_profile


def test_acquisition_requires_authorized_source_or_fallback():
    result = acquire_social_profile("https://www.instagram.com/example")
    assert result.status == "fallback_required"
    assert result.source == "none"
    assert result.profile is None
