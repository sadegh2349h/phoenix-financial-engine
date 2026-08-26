from phoenix_core.agent_orchestrator import AgentOrchestrator, AgentTask
from phoenix_core.memory import MemoryStore


def test_memory_is_available_to_intelligence_and_persisted():
    memory = MemoryStore()
    memory.put("growth-plan", {"previous": "positive"})
    result = AgentOrchestrator(memory=memory).execute(
        AgentTask("growth plan", "growth_strategy", {})
    )
    assert result["status"] == "completed"
    assert result["memory"] == [{"previous": "positive"}]
    assert memory.get("decision:growth plan") is not None
