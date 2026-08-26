from __future__ import annotations

import json

from phoenix_core.monitoring import Monitor
from phoenix_core.runtime import PhoenixRuntime
from phoenix_core.scheduler import Scheduler
from phoenix_core.scheduled_execution import ScheduledExecution


def main() -> None:
    scheduler = Scheduler()
    execution = ScheduledExecution(scheduler)
    execution.register("runtime-heartbeat", 300, lambda: {"ok": True})
    monitor = Monitor()
    cycle = PhoenixRuntime(execution, monitor).tick()
    print(json.dumps({"status": cycle.status, "health": cycle.health, "runs": cycle.runs}, default=str))
    if cycle.status != "healthy":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
