"""Adapter boundary for Langfuse observability."""
from __future__ import annotations


def status() -> dict[str, object]:
    try:
        __import__("langfuse")
        installed = True
    except ImportError:
        installed = False
    return {"provider": "Langfuse", "installed": installed, "role": "observability"}


def trace_event(*, name: str, metadata: dict[str, object] | None = None) -> dict[str, object]:
    if not name.strip():
        raise ValueError("name is required")
    return {"name": name, "metadata": metadata or {}}
