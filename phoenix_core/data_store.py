import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class SQLiteStore:
    """Durable local store with explicit retention; never purges by default."""

    def __init__(self, path: str = "data/phoenix.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records (key TEXT PRIMARY KEY, value TEXT NOT NULL, created_at TEXT NOT NULL)")
            db.commit()

    def put(self, key: str, value: Dict[str, Any], created_at: str) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT OR REPLACE INTO records(key,value,created_at) VALUES(?,?,?)", (key, json.dumps(value, default=str), created_at))
            db.commit()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT value FROM records WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def list_recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute("SELECT key,value,created_at FROM records ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [{"key": k, "value": json.loads(v), "created_at": t} for k, v, t in rows]
