from typing import Callable, Dict
from .contracts import Decision, Event, Task
from .memory import MemoryStore
from .registry import ModuleRegistry


class PhoenixKernel:
    """Minimal orchestration kernel connecting tasks, modules, memory and decisions."""

    def __init__(self, memory: MemoryStore, registry: ModuleRegistry) -> None:
        self.memory = memory
        self.registry = registry
        self.handlers: Dict[str, Callable[[Task], Decision]] = {}

    def register_handler(self, capability: str, handler: Callable[[Task], Decision]) -> None:
        self.handlers[capability] = handler

    def dispatch(self, task: Task, capability: str) -> Decision:
        handler = self.handlers[capability]
        decision = handler(task)
        self.memory.put(decision.decision_id, {
            "type": "decision",
            "decision": decision,
        })
        self.memory.put(
            f"event:{decision.decision_id}",
            {"type": "event", "event": Event("decision.created", "phoenix.kernel", {"decision_id": decision.decision_id})},
        )
        return decision
