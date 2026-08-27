from phoenix_core.memory import MemoryStore
from phoenix_core.monitoring import Monitor
from phoenix_core.runtime import PhoenixRuntime
from phoenix_core.scheduler import Scheduler
from phoenix_core.scheduled_execution import ScheduledExecution


def test_runtime_persists_event_and_builds_learning_context(tmp_path):
    memory = MemoryStore(tmp_path / "memory.json")
    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("growth", 60, lambda: {"ok": True})
    runtime = PhoenixRuntime(execution, Monitor(), memory)
    cycle = runtime.tick()
    assert cycle.status == "healthy"
    assert cycle.learning_contexts[0]["objective"] == "growth"
    assert MemoryStore(tmp_path / "memory.json").get("runtime:growth")["status"] == "completed"
