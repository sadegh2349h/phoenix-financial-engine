import json
import sqlite3
from pathlib import Path
from typing import Any, Optional


class SQLiteMemoryStore:
    """Durable local store with explicit retention; no automatic 24-hour deletion."""

    def __init__(self, path: str = "data/phoenix_memory.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT NOT NULL, created_at TEXT NOT NULL)")
            db.commit()

    def put(self, key: str, value: Any, created_at: str) -> None:
        with self._connect() as db:
            db.execute("INSERT OR REPLACE INTO memory(key,value,created_at) VALUES(?,?,?)", (key, json.dumps(value, default=str), created_at))
            db.commit()

    def get(self, key: str) -> Optional[Any]:
        with self._connect() as db:
            row = db.execute("SELECT value FROM memory WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def purge_before(self, iso_timestamp: str) -> int:
        """Explicit operator-invoked purge; never scheduled implicitly."""
        with self._connect() as db:
            cur = db.execute("DELETE FROM memory WHERE created_at < ?", (iso_timestamp,))
            db.commit()
            return cur.rowcount
