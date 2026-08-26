from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .scheduler import Scheduler, ScheduledTask


@dataclass(frozen=True)
class ScheduledRun:
    name: str
    status: str
    result: Any


class ScheduledExecution:
    """Connects the scheduler to safe, observable task execution."""

    def __init__(self, scheduler: Scheduler) -> None:
        self.scheduler = scheduler

    def register(self, name: str, interval_seconds: int, handler: Callable[[], Any]) -> None:
        self.scheduler.register(ScheduledTask(name, interval_seconds, handler))

    def run_due(self) -> list[ScheduledRun]:
        runs: list[ScheduledRun] = []
        for name in self.scheduler.due_tasks():
            try:
                result = self.scheduler.run(name)
                runs.append(ScheduledRun(name, "completed", result))
            except Exception as exc:
                runs.append(ScheduledRun(name, "failed", {"error": type(exc).__name__}))
        return runs
