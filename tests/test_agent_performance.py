from phoenix_core.agent_performance import AgentPerformanceTracker
from phoenix_core.memory import MemoryStore


def test_performance_is_tracked_per_agent():
    tracker = AgentPerformanceTracker(MemoryStore())
    tracker.record("strategy", "d1", 1.0, "correct")
    tracker.record("strategy", "d2", 0.5, "partial")
    tracker.record("risk", "d1", 0.8, "useful")
    report = tracker.report()
    assert report[0].agent == "risk"
    assert report[0].average_score == 0.8
    assert report[1].agent == "strategy"
    assert report[1].average_score == 0.75
