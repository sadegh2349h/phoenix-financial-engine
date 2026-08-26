from typing import Dict, Iterable
from .contracts import ModuleManifest


class ModuleRegistry:
    """Runtime registry allowing modules to be added, disabled, or replaced independently."""

    def __init__(self) -> None:
        self._modules: Dict[str, ModuleManifest] = {}

    def register(self, manifest: ModuleManifest) -> None:
        self._modules[manifest.name] = manifest

    def enable(self, name: str) -> None:
        m = self._modules[name]
        self._modules[name] = ModuleManifest(m.name, m.version, m.capabilities, True)

    def disable(self, name: str) -> None:
        m = self._modules[name]
        self._modules[name] = ModuleManifest(m.name, m.version, m.capabilities, False)

    def active(self) -> Iterable[ModuleManifest]:
        return (m for m in self._modules.values() if m.enabled)

    def get(self, name: str) -> ModuleManifest:
        return self._modules[name]
