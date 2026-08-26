from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class AgentManifest:
    name: str
    version: str
    capabilities: tuple[str, ...]
    risk_level: str = "low"
    description: str = ""
    human_approval_required: bool = False


class AgentRegistry:
    """Registry for specialist agents without coupling them to the core."""

    def __init__(self) -> None:
        self._agents: Dict[str, tuple[AgentManifest, Callable[..., Any]]] = {}

    def register(self, manifest: AgentManifest, handler: Callable[..., Any]) -> None:
        if not manifest.name.strip():
            raise ValueError("agent name cannot be empty")
        if manifest.name in self._agents:
            raise ValueError(f"agent already registered: {manifest.name}")
        self._agents[manifest.name] = (manifest, handler)

    def get(self, name: str) -> tuple[AgentManifest, Callable[..., Any]]:
        return self._agents[name]

    def find_by_capability(self, capability: str) -> list[AgentManifest]:
        return [m for m, _ in self._agents.values() if capability in m.capabilities]

    def list(self) -> list[AgentManifest]:
        return sorted((m for m, _ in self._agents.values()), key=lambda m: m.name)

    def run(self, name: str, **kwargs: Any) -> Any:
        manifest, handler = self.get(name)
        return handler(**kwargs)


def build_default_registry() -> AgentRegistry:
    """Build PHOENIX's initial specialist-agent registry.

    These are orchestration-ready specialist contracts. They intentionally do
    not call external LLMs or perform autonomous side effects. Production AI
    providers can be attached to the handlers later without changing the
    registry contract.
    """
    from .specialist_agents import SPECIALIST_AGENTS

    registry = AgentRegistry()
    for manifest, handler in SPECIALIST_AGENTS:
        registry.register(manifest, handler)
    return registry
