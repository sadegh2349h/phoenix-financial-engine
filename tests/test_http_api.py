from fastapi.testclient import TestClient

from phoenix_core.http_api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "phoenix"


def test_analysis_requires_key_when_configured(monkeypatch):
    monkeypatch.setenv("PHOENIX_API_KEY", "secret")
    response = client.post("/v1/analyze", json={"objective": "growth plan", "capability": "growth_strategy"})
    assert response.status_code == 401
    response = client.post("/v1/analyze", headers={"X-API-Key": "secret"}, json={"objective": "growth plan", "capability": "growth_strategy"})
    assert response.status_code == 200
