"""Adapter boundary for Mem0 durable memory."""
from __future__ import annotations


def status() -> dict[str, object]:
    try:
        __import__("mem0")
        installed = True
    except ImportError:
        installed = False
    return {"provider": "Mem0", "installed": installed, "role": "memory"}


def memory_record(*, scope: str, key: str, value: str) -> dict[str, str]:
    if not all((scope.strip(), key.strip(), value.strip())):
        raise ValueError("scope, key and value are required")
    return {"scope": scope, "key": key, "value": value}
