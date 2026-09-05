from phoenix_core.instagram_acquisition import acquire_instagram_profile


def test_acquisition_fails_closed_without_fabricating_data():
    result = acquire_instagram_profile("https://www.instagram.com/example/")
    assert result["status"] in {"success", "unavailable"}
    if result["status"] == "unavailable":
        assert result["data"] == {}
        assert result["evidence"] == []


def test_authorized_provider_is_preferred():
    def provider(url):
        from phoenix_core.instagram_acquisition import AcquisitionResult
        return AcquisitionResult(
            source="authorized_provider",
            status="success",
            profile_url=url,
            data={"username": "example", "followers": 123},
            evidence=({"source": "authorized_provider", "field": "followers", "confidence": 1.0},),
        )

    result = acquire_instagram_profile("https://www.instagram.com/example/", authorized_provider=provider)
    assert result["selected_source"] == "authorized_provider"
    assert result["data"]["followers"] == 123
