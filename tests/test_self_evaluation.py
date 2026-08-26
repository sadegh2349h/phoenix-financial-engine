from phoenix_core.memory import MemoryStore
from phoenix_core.self_evaluation import SelfEvaluator


def test_self_evaluation_persists_outcome_and_performance():
    memory = MemoryStore()
    evaluator = SelfEvaluator(memory)
    evaluator.evaluate("btc-1", actual="up", expected="up")
    evaluator.evaluate("btc-2", actual="down", expected="up")
    assert memory.get("evaluation:btc-1")["outcome"] == "correct"
    assert evaluator.performance() == {"count": 2.0, "accuracy": 0.5}
