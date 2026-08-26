from phoenix_core.intelligence import IntelligenceLayer, IntelligenceRequest


def test_default_intelligence_provider_is_safe():
    layer = IntelligenceLayer()
    response = layer.analyze(IntelligenceRequest("test objective", {}, "financial_analyst"))

    assert response.status == "ready"
    assert response.provider == "rule-based"
    assert response.requires_human_review is True
    assert response.confidence == 0.0
