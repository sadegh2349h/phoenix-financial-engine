"""Adapter boundary for PydanticAI typed agent contracts."""
from __future__ import annotations


def status() -> dict[str, object]:
    try:
        __import__("pydantic_ai")
        installed = True
    except ImportError:
        installed = False
    return {"provider": "PydanticAI", "installed": installed, "role": "typed_agents"}


def validate_agent_output(output: object, expected_type: type) -> object:
    if not isinstance(output, expected_type):
        raise TypeError(f"expected {expected_type.__name__}")
    return output
