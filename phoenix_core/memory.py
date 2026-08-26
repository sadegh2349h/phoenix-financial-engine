from __future__ import annotations

import re
from typing import Any, Dict, Iterable, Optional


class MemoryStore:
    """Provider-agnostic operational memory for PHOENIX context and decisions."""

    def __init__(self) -> None:
        self._items: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _tokens(value: str) -> set[str]:
        return set(re.findall(r"[\w]+", value.lower().replace("-", " ")))

    def put(self, key: str, value: Dict[str, Any]) -> None:
        if not key.strip():
            raise ValueError("memory key cannot be empty")
        self._items[key] = dict(value)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._items.get(key)
        return dict(value) if value is not None else None

    def search(self, term: str) -> Iterable[Dict[str, Any]]:
        query_tokens = self._tokens(term)
        results = []
        for key, value in self._items.items():
            key_tokens = self._tokens(key)
            value_tokens = self._tokens(str(value))
            if query_tokens & (key_tokens | value_tokens):
                results.append(dict(value))
        return results

    def all(self) -> Iterable[Dict[str, Any]]:
        return [dict(value) for value in self._items.values()]

    def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def context_for(self, objective: str, limit: int = 10) -> list[Dict[str, Any]]:
        return list(self.search(objective))[:limit]
