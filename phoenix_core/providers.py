from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable


class DataProvider(ABC):
    """Stable boundary between PHOENIX and external data sources."""

    name: str = "unknown"

    @abstractmethod
    def fetch(self, query: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError


class InMemoryProvider(DataProvider):
    name = "memory"

    def __init__(self, rows: Iterable[Dict[str, Any]] = ()) -> None:
        self.rows = list(rows)

    def fetch(self, query: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        return list(self.rows)
