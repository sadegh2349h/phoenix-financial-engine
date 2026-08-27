from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .monitoring import Monitor
from .scheduled_execution import ScheduledExecution
from .memory import MemoryStore
from .agent_learning import AgentLearningContext


@dataclass(frozen=True)
class RuntimeCycle:
    status: str
    runs: list[dict[str, Any]]
    health: dict[str, Any]
    learning_contexts: list[dict[str, Any]]


class PhoenixRuntime:
    """Runs due tasks, records health, and exposes durable experience to agents."""

    def __init__(self, execution: ScheduledExecution, monitor: Monitor,
                 memory: MemoryStore | None = None) -> None:
        self.execution = execution
        self.monitor = monitor
        self.memory = memory or MemoryStore()

    def tick(self) -> RuntimeCycle:
        runs = self.execution.run_due()
        contexts: list[dict[str, Any]] = []
        for run in runs:
            self.monitor.record(run.name, run.status, {"result": run.result})
            self.memory.put(f"runtime:{run.name}", {
                "type": "runtime_event", "task": run.name,
                "status": run.status, "result": run.result,
            })
            contexts.append(AgentLearningContext(self.memory).build(run.name).__dict__)
        health = self.monitor.health()
        status = "healthy" if health["status"] == "healthy" else "degraded"
        return RuntimeCycle(status, [r.__dict__ for r in runs], health, contexts)
