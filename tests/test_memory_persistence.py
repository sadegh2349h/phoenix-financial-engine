from phoenix_core.memory import MemoryStore


def test_memory_survives_a_new_store_instance(tmp_path):
    path = tmp_path / "memory.json"
    first = MemoryStore(path)
    first.put("growth-plan", {"previous": "positive"})
    second = MemoryStore(path)
    assert second.get("growth-plan") == {"previous": "positive"}
