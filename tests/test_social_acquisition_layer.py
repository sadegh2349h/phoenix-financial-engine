from phoenix_core import social_acquisition_layer as gateway
from phoenix_core.social_intelligence import SocialProfileInput


def test_validate_social_url():
    assert gateway.validate_social_url(" https://www.instagram.com/example/ ") == "https://www.instagram.com/example"


def test_no_public_evidence_returns_gateway_fallback(monkeypatch):
    monkeypatch.setattr(gateway, "fetch_public_social_profile", lambda url: None)
    monkeypatch.setattr(
        gateway,
        "fetch_public_social_profile_browser",
        lambda url: None,
    )
    result = gateway.acquire_social_profile("https://www.instagram.com/example")
    assert result.status == "fallback_required"
    assert result.source == "public_gateway"
    assert result.profile is None


def test_browser_route_is_used_after_http_failure(monkeypatch):
    profile = SocialProfileInput(
        url="https://www.instagram.com/example",
        username="example",
        bio="Example business",
        followers=1000,
    )
    def fail_http(url):
        raise RuntimeError("HTTP blocked")
    monkeypatch.setattr(gateway, "fetch_public_social_profile", fail_http)
    monkeypatch.setattr(
        gateway,
        "fetch_public_social_profile_browser",
        lambda url: profile,
    )
    result = gateway.acquire_social_profile(profile.url)
    assert result.status == "acquired"
    assert result.source == "public_browser"
    assert result.profile == profile


def test_user_supplied_data_flows_into_intelligence():
    profile = SocialProfileInput(
        url="https://www.instagram.com/example",
        username="example",
        bio="Example business",
        followers=1000,
        content_samples=({"views": 100, "likes": 10},),
    )
    result = gateway.analyze_social_url(profile.url, user_supplied=profile)
    assert result["acquisition"]["status"] == "acquired"
    assert result["intelligence"]["engine"] == "PHOENIX Social Intelligence Engine"
    assert result["intelligence"]["analysis"]["content"]["measurable_sample_count"] == 1
