from phoenix_core.api import PhoenixService


def test_service_health_is_exposed():
    service = PhoenixService()
    health = service.health()
    assert health["service"] == "phoenix"
    assert health["status"] == "healthy"


def test_service_analysis_boundary():
    result = PhoenixService().analyze("growth plan", "growth_strategy")
    assert result["status"] in {"completed", "approval_required"}
