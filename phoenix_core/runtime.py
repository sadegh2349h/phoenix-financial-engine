from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .monitoring import Monitor
from .scheduled_execution import ScheduledExecution


@dataclass(frozen=True)
class RuntimeCycle:
    status: str
    runs: list[dict[str, Any]]
    health: dict[str, Any]


class PhoenixRuntime:
    """Runs due PHOENIX tasks and records runtime health without hiding failures."""

    def __init__(self, execution: ScheduledExecution, monitor: Monitor) -> None:
        self.execution = execution
        self.monitor = monitor

    def tick(self) -> RuntimeCycle:
        runs = self.execution.run_due()
        for run in runs:
            self.monitor.record(run.name, run.status, {"result": run.result})
        health = self.monitor.health()
        status = "healthy" if health["status"] == "healthy" else "degraded"
        return RuntimeCycle(status, [r.__dict__ for r in runs], health)
