from phoenix_core.scheduler import ScheduledTask, Scheduler


def test_new_task_is_due_and_runs():
    calls: list[str] = []
    scheduler = Scheduler()
    scheduler.register(ScheduledTask("market-watch", 300, lambda: calls.append("run")))
    assert scheduler.due_tasks() == ["market-watch"]
    scheduler.run("market-watch")
    assert calls == ["run"]
    assert scheduler.due_tasks() == []


def test_duplicate_or_invalid_schedule_is_rejected():
    scheduler = Scheduler()
    try:
        scheduler.register(ScheduledTask("bad", 0, lambda: None))
        assert False
    except ValueError:
        pass
