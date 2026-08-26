from phoenix_core.scheduler import Scheduler
from phoenix_core.scheduled_execution import ScheduledExecution


def test_due_tasks_are_executed_and_observable():
    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("health", 60, lambda: {"ok": True})
    runs = execution.run_due()
    assert runs[0].name == "health"
    assert runs[0].status == "completed"
    assert runs[0].result == {"ok": True}


def test_failed_task_is_reported_without_stopping_other_tasks():
    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("bad", 60, lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    execution.register("good", 60, lambda: "ok")
    runs = execution.run_due()
    assert [r.status for r in runs] == ["failed", "completed"]
