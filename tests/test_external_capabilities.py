from phoenix_core.external_capabilities import CAPABILITIES, capability_status


def test_external_capability_registry_is_non_empty():
    assert CAPABILITIES
    assert {cap.priority for cap in CAPABILITIES} >= {"P0", "P1"}


def test_capability_status_is_machine_readable():
    status = capability_status()
    assert len(status) == len(CAPABILITIES)
    assert all({"name", "project", "package", "priority", "installed"} <= set(item) for item in status)
