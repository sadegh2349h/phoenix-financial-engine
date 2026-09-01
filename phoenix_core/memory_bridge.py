"""Small provider-agnostic bridge for PHOENIX learning records."""
from __future__ import annotations

from typing import Any


def create_learning_record(*, client_id: str, action: dict[str, Any], measurement: dict[str, Any], approved: bool) -> dict[str, Any]:
    """Create a safe, serializable learning record for an external/native memory layer."""
    return {
        "client_id": client_id,
        "type": "client_learning",
        "approved": bool(approved),
        "action": dict(action),
        "measurement": dict(measurement),
    }


def memory_write_payload(record: dict[str, Any]) -> dict[str, Any]:
    """Normalize a learning record for a future memory provider adapter."""
    return {"namespace": f"client:{record['client_id']}", "record": dict(record)}
