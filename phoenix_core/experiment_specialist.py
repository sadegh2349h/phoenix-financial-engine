"""PHOENIX Experiment specialist: hypothesis-driven growth optimization."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentPlan:
    hypothesis: str
    variant_a: str
    variant_b: str
    primary_kpi: str
    guardrail_kpis: tuple[str, ...]
    decision_rule: str
    learning: str


def design_experiment(*, hypothesis: str, variant_a: str, variant_b: str, primary_kpi: str) -> ExperimentPlan:
    values = (hypothesis, variant_a, variant_b, primary_kpi)
    if any(not value or not value.strip() for value in values):
        raise ValueError("hypothesis, variants and primary_kpi are required")
    return ExperimentPlan(
        hypothesis=hypothesis,
        variant_a=variant_a,
        variant_b=variant_b,
        primary_kpi=primary_kpi,
        guardrail_kpis=("conversion_rate", "retention_rate", "customer_satisfaction"),
        decision_rule="Choose the variant with stronger primary KPI only when guardrails remain acceptable; human approves rollout.",
        learning="Record result, evidence and decision for the next experiment.",
    )

FRAMEWORKS = ("A/B Testing", "Growth Experimentation", "Hypothesis-Driven Optimization", "Measurement Loop")
