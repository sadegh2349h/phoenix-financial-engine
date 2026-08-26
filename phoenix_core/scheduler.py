from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass(frozen=True)
class ScheduledTask:
    name: str
    interval_seconds: int
    handler: Callable[[], Any]
    enabled: bool = True
    last_run: str | None = None


class Scheduler:
    """Small deterministic scheduler contract for 24/7 orchestration.

    It is intentionally transport-agnostic: a cloud scheduler, worker, or cron
    can call `due_tasks()` and `run()` without coupling the PHOENIX core to a
    particular hosting provider.
    """

    def __init__(self) -> None:
        self._tasks: dict[str, ScheduledTask] = {}

    def register(self, task: ScheduledTask) -> None:
        if task.interval_seconds < 1:
            raise ValueError("interval_seconds must be positive")
        if task.name in self._tasks:
            raise ValueError(f"scheduled task already registered: {task.name}")
        self._tasks[task.name] = task

    def due_tasks(self, now: datetime | None = None) -> list[str]:
        now = now or datetime.now(timezone.utc)
        due: list[str] = []
        for task in self._tasks.values():
            if not task.enabled:
                continue
            if task.last_run is None:
                due.append(task.name)
                continue
            elapsed = (now - datetime.fromisoformat(task.last_run)).total_seconds()
            if elapsed >= task.interval_seconds:
                due.append(task.name)
        return due

    def run(self, name: str) -> Any:
        task = self._tasks.get(name)
        if task is None or not task.enabled:
            raise ValueError(f"scheduled task unavailable: {name}")
        result = task.handler()
        self._tasks[name] = ScheduledTask(task.name, task.interval_seconds, task.handler, task.enabled,
                                          datetime.now(timezone.utc).isoformat())
        return result
