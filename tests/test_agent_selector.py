from phoenix_core.agent_performance import AgentPerformanceTracker
from phoenix_core.agent_selector import IntelligentAgentSelector
from phoenix_core.agents import AgentManifest, AgentRegistry
from phoenix_core.memory import MemoryStore


def test_selector_prefers_agent_with_better_history():
    memory = MemoryStore()
    registry = AgentRegistry()
    registry.register(AgentManifest("a", "1", ("growth",)), lambda **_: None)
    registry.register(AgentManifest("b", "1", ("growth",)), lambda **_: None)
    performance = AgentPerformanceTracker(memory)
    performance.record("a", "d1", 0.7, "ok")
    performance.record("b", "d2", 0.9, "ok")
    selected = IntelligentAgentSelector(registry, performance).select("growth", 2)
    assert [item.agent for item in selected] == ["b", "a"]
