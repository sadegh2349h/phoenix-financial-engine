from __future__ import annotations

from typing import Any, Protocol


class DataSource(Protocol):
    name: str

    def read(self, query: str) -> dict[str, Any]: ...


class InMemoryDataSource:
    name = "memory"

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = data or {}

    def read(self, query: str) -> dict[str, Any]:
        value = self.data.get(query)
        return {"source": self.name, "query": query, "data": value}


class DataAccessLayer:
    """Provider-agnostic gateway between PHOENIX agents and external data."""

    def __init__(self, sources: list[DataSource] | None = None) -> None:
        self.sources = sources or [InMemoryDataSource()]

    def query(self, query: str) -> dict[str, Any]:
        return {source.name: source.read(query) for source in self.sources}
