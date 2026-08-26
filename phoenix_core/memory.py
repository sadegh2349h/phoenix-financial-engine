from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional


class MemoryStore:
    """Provider-agnostic operational memory for PHOENIX context and decisions."""

    def __init__(self) -> None:
        self._items: Dict[str, Dict[str, Any]] = {}

    def put(self, key: str, value: Dict[str, Any]) -> None:
        if not key.strip():
            raise ValueError("memory key cannot be empty")
        record = dict(value)
        record.setdefault("stored_at", datetime.now(timezone.utc).isoformat())
        self._items[key] = record

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._items.get(key)
        return dict(value) if value is not None else None

    def search(self, term: str) -> Iterable[Dict[str, Any]]:
        q = term.lower()
        return [dict(value) for key, value in self._items.items() if q in key.lower() or q in str(value).lower()]

    def all(self) -> Iterable[Dict[str, Any]]:
        return [dict(value) for value in self._items.values()]

    def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def context_for(self, objective: str, limit: int = 10) -> list[Dict[str, Any]]:
        return list(self.search(objective))[:limit]
