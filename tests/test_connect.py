import pytest

from phoenix_core.connect import Connector, ConnectorRegistry


def test_connector_registry_invokes_enabled_adapter():
    registry = ConnectorRegistry()
    registry.register(Connector("image-generator", "image", lambda payload: {"ok": True, **payload}))
    assert registry.available("image") == ["image-generator"]
    assert registry.invoke("image-generator", {"prompt": "phoenix"})["ok"] is True


def test_duplicate_connector_is_rejected():
    registry = ConnectorRegistry()
    registry.register(Connector("x", "test", lambda _: None))
    with pytest.raises(ValueError):
        registry.register(Connector("x", "test", lambda _: None))
