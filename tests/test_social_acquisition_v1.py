from phoenix_core import social_acquisition_layer as gateway


def test_acquisition_requires_public_gateway_fallback(monkeypatch):
    monkeypatch.setattr(gateway, "fetch_public_social_profile", lambda url: None)
    monkeypatch.setattr(gateway, "fetch_public_social_profile_browser", lambda url: None)
    result = gateway.acquire_social_profile("https://www.instagram.com/example")
    assert result.status == "fallback_required"
    assert result.source == "public_gateway"
    assert result.profile is None
