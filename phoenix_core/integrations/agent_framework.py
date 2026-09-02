"""Adapter boundary for Microsoft Agent Framework orchestration."""
from __future__ import annotations


def status() -> dict[str, object]:
    try:
        __import__("agent_framework")
        installed = True
    except ImportError:
        installed = False
    return {"provider": "Microsoft Agent Framework", "installed": installed, "role": "orchestration", "human_approval": True}


def build_workflow_plan(tasks: list[str]) -> dict[str, object]:
    if not tasks:
        raise ValueError("tasks are required")
    return {"tasks": tuple(tasks), "mode": "specialist_workflow", "approval_boundary": "human"}
