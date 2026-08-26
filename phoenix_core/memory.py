from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


class MemoryStore:
    """Provider-agnostic operational memory with optional durable JSON persistence."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else None
        self._items: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if self._path and self._path.exists():
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("memory file must contain an object")
            self._items = {str(k): dict(v) for k, v in data.items() if isinstance(v, dict)}

    def _save(self) -> None:
        if not self._path:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temp = self._path.with_suffix(self._path.suffix + ".tmp")
        temp.write_text(json.dumps(self._items, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        temp.replace(self._path)

    @staticmethod
    def _tokens(value: str) -> set[str]:
        return set(re.findall(r"[\w]+", value.lower().replace("-", " ")))

    def put(self, key: str, value: Dict[str, Any]) -> None:
        if not key.strip():
            raise ValueError("memory key cannot be empty")
        self._items[key] = dict(value)
        self._save()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        value = self._items.get(key)
        return dict(value) if value is not None else None

    def search(self, term: str) -> Iterable[Dict[str, Any]]:
        query_tokens = self._tokens(term)
        return [dict(value) for key, value in self._items.items()
                if query_tokens & (self._tokens(key) | self._tokens(str(value)))]

    def all(self) -> Iterable[Dict[str, Any]]:
        return [dict(value) for value in self._items.values()]

    def delete(self, key: str) -> None:
        self._items.pop(key, None)
        self._save()

    def context_for(self, objective: str, limit: int = 10) -> list[Dict[str, Any]]:
        return list(self.search(objective))[:limit]
