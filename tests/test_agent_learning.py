from phoenix_core.agent_learning import AgentLearningContext
from phoenix_core.memory import MemoryStore


def test_learning_context_uses_prior_memory_and_evaluations():
    memory = MemoryStore()
    memory.put("growth-plan", {"previous": "positive"})
    memory.put("evaluation:d1", {"type": "evaluation", "score": 0.8})
    memory.put("evaluation:d2", {"type": "evaluation", "score": 0.6})
    context = AgentLearningContext(memory).build("growth plan")
    assert context.memories == [{"previous": "positive"}]
    assert context.average_score == 0.7
