import pytest

from phoenix_core.evaluation_loop import SelfEvaluationLoop
from phoenix_core.memory import MemoryStore


def test_evaluation_is_persisted_and_performance_is_aggregated():
    memory = MemoryStore()
    loop = SelfEvaluationLoop(memory)
    loop.evaluate("d1", "correct", 1.0, "signal matched outcome")
    loop.evaluate("d2", "wrong", 0.0, "signal failed")
    assert loop.performance() == {"count": 2, "average_score": 0.5}
    assert memory.get("evaluation:d1")["lesson"] == "signal matched outcome"


def test_evaluation_score_is_bounded():
    loop = SelfEvaluationLoop(MemoryStore())
    with pytest.raises(ValueError):
        loop.evaluate("d1", "invalid", 1.1)
