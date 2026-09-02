from phoenix_core.social_acquisition import AcquisitionEvidence, AcquisitionRequest, build_acquisition_plan, normalize_evidence


def test_acquisition_plan_is_evidence_first():
    plan = build_acquisition_plan(AcquisitionRequest("https://www.instagram.com/example/"))
    assert plan["human_review_required"] is True
    assert plan["evidence_first"] is True
    assert plan["no_private_access"] is True
    assert plan["routes"][0]["source"] == "official_api"


def test_evidence_normalization():
    result = normalize_evidence([AcquisitionEvidence("user_supplied", "followers", 1200)])
    assert result["field_coverage"] == 1
    assert result["ready_for_social_intelligence"] is True


def test_invalid_url_rejected():
    try:
        build_acquisition_plan(AcquisitionRequest("not-a-url"))
    except ValueError:
        return
    raise AssertionError("invalid URL must be rejected")
