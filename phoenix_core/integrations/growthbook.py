"""Adapter boundary for GrowthBook experimentation."""
from __future__ import annotations


def status() -> dict[str, object]:
    try:
        __import__("growthbook")
        installed = True
    except ImportError:
        installed = False
    return {"provider": "GrowthBook", "installed": installed, "role": "experimentation"}


def experiment_assignment(*, experiment: str, variants: tuple[str, ...]) -> dict[str, object]:
    if not experiment.strip() or not variants:
        raise ValueError("experiment and variants are required")
    return {"experiment": experiment, "variants": variants}
