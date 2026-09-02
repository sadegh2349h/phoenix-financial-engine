from phoenix_core.specialist_router import enrich_client_package, route_specialists, specialist_registry


def test_registry_contains_required_core_specialists():
    registry = specialist_registry()
    assert {"psyche", "ops", "brand", "closer"}.issubset(set(registry))


def test_routing_is_evidence_based_and_requires_human_approval():
    routed = route_specialists(problem="مشتری به قیمت بالا اعتراض دارد و فروش بسته می‌شود")
    assert routed
    assert routed[0]["key"] == "closer"
    assert routed[0]["human_approval_required"] is True


def test_ops_routes_for_repetitive_bottleneck():
    routed = route_specialists(problem="فرآیند تکراری و گلوگاه داریم و باید اتوماسیون شود")
    assert routed[0]["key"] == "ops"


def test_enrichment_preserves_package_and_adds_routing():
    package = {"status": "analyzed", "analysis": {"business_health": "bottleneck"}}
    enriched = enrich_client_package(package, problem="جایگاه برند و مزیت رقابتی نامشخص است")
    assert enriched["status"] == "analyzed"
    assert enriched["specialist_routing"][0]["key"] == "brand"
    assert enriched["specialist_decision_owner"] == "human"
