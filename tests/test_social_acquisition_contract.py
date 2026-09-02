from phoenix_core.social_acquisition_contract import analyze_social_url


def test_public_contract_is_importable():
    result = analyze_social_url("https://www.instagram.com/example")
    assert result["human_decision_required"] is True
    assert result["acquisition"]["status"] == "fallback_required"
