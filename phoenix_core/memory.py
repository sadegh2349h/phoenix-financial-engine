from typing import Any, Dict, Iterable, Optional


class MemoryStore:
    """Durable-memory interface; persistence is intentionally provider-agnostic."""

    def __init__(self) -> None:
        self._items: Dict[str, Dict[str, Any]] = {}

    def put(self, key: str, value: Dict[str, Any]) -> None:
        self._items[key] = value

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._items.get(key)

    def all(self) -> Iterable[Dict[str, Any]]:
        return self._items.values()

    def delete(self, key: str) -> None:
        self._items.pop(key, None)
