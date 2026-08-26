from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class AgentManifest:
    name: str
    version: str
    capabilities: tuple[str, ...]
    risk_level: str = "low"


class AgentRegistry:
    """Dynamic registry for specialist agents without coupling them to the core."""

    def __init__(self) -> None:
        self._agents: Dict[str, tuple[AgentManifest, Callable[..., Any]]] = {}

    def register(self, manifest: AgentManifest, handler: Callable[..., Any]) -> None:
        self._agents[manifest.name] = (manifest, handler)

    def get(self, name: str) -> tuple[AgentManifest, Callable[..., Any]]:
        return self._agents[name]

    def list(self) -> list[AgentManifest]:
        return [manifest for manifest, _ in self._agents.values()]

    def run(self, name: str, **kwargs: Any) -> Any:
        manifest, handler = self.get(name)
        return handler(**kwargs)
