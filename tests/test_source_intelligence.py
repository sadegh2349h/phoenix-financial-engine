from phoenix_core.source_intelligence import SourceIntelligence


def test_source_quality_is_weighted_and_ranked():
    engine = SourceIntelligence()
    weak = engine.assess("weak", {"data": {"x": 1}, "reliability": 0.4, "freshness": 0.5})
    strong = engine.assess("strong", {"data": {"x": 2}, "reliability": 0.9, "freshness": 1.0})
    ranked = engine.rank([weak, strong])
    assert ranked[0].source == "strong"
    assert ranked[0].weight > ranked[1].weight
