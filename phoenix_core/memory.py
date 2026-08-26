from __future__ import annotations

from typing import Any, Dict, Iterable, Optional


class MemoryStore:
    """Provider-agnostic memory boundary for PHOENIX context and decisions."""

    def __init__(self) -> None:
        self._items: Dict[str, Dict[str, Any]] = {}

    def put(self, key: str, value: Dict[str, Any]) -> None:
        if not key.strip():
            raise ValueError("memory key cannot be empty")
        self._items[key] = dict(value)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._items.get(key)
        return dict(value) if value is not None else None

    def search(self, term: str) -> Iterable[Dict[str, Any]]:
        q = term.lower()
        return [value for key, value in self._items.items() if q in key.lower() or q in str(value).lower()]

    def all(self) -> Iterable[Dict[str, Any]]:
        return list(self._items.values())

    def delete(self, key: str) -> None:
        self._items.pop(key, None)
