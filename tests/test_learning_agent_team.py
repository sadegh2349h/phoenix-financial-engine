from phoenix_core.agent_learning import AgentLearningContext
from phoenix_core.learning_agent_team import LearningAgentTeam
from phoenix_core.memory import MemoryStore
from phoenix_core.specialist_agents import SpecialistAgentTeam, SpecialistProfile


def test_specialists_receive_shared_learning_context():
    memory = MemoryStore()
    memory.put("growth-plan", {"previous": "positive"})
    team = SpecialistAgentTeam()
    team.register_specialist(
        SpecialistProfile("strategy", "growth", 1),
        lambda task: {"seen": task["memory"], "confidence": 0.9},
    )
    result = LearningAgentTeam(team, AgentLearningContext(memory)).run(
        "growth plan", {"goal": "expand"}
    )
    assert result.memories == [{"previous": "positive"}]
    assert result.agents[0]["result"]["seen"] == [{"previous": "positive"}]
