from phoenix_core.evidence import EvidenceEngine


def test_evidence_engine_produces_confidence_and_warnings():
    result = EvidenceEngine().evaluate({
        "primary": {"data": {"price": 100}, "reliability": 0.9, "freshness": 1.0},
        "secondary": {"data": None, "reliability": 0.2, "freshness": 0.2},
    })
    assert 0 <= result.confidence <= 1
    assert result.assessments[0].source == "primary"


def test_no_sources_is_explicitly_low_confidence():
    result = EvidenceEngine().evaluate({})
    assert result.confidence == 0
    assert result.warnings
