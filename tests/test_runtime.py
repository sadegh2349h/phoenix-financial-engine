from phoenix_core.monitoring import Monitor
from phoenix_core.runtime import PhoenixRuntime
from phoenix_core.scheduler import Scheduler
from phoenix_core.scheduled_execution import ScheduledExecution


def test_runtime_executes_due_work_and_records_health():
    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("health", 60, lambda: {"ok": True})
    monitor = Monitor()
    runtime = PhoenixRuntime(execution, monitor)
    cycle = runtime.tick()
    assert cycle.status == "healthy"
    assert cycle.runs[0]["status"] == "completed"
    assert cycle.health["events"] == 1
