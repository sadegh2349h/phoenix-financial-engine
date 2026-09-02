"""Phoenix Growth: evidence-first acquisition and growth specialist.

The module is provider-agnostic: it creates measurable growth experiments,
connects them to the funnel, and keeps rollout decisions human-approved.
"""
from __future__ import annotations

from dataclasses import dataclass


FUNNEL_STAGES = ("awareness", "consideration", "conversion")


@dataclass(frozen=True)
class GrowthExperiment:
    hypothesis: str
    execution_plan: tuple[str, ...]
    metric_to_track: tuple[str, ...]
    potential_risk: str
    funnel_stage: str = "awareness"
    primary_kpi: str = "qualified_leads"
    human_approval_required: bool = True


def growth_experiments(goal: str, acquisition_channel: str) -> tuple[GrowthExperiment, ...]:
    """Return three low-cost, measurable experiments for a supplied goal/channel."""
    if not goal.strip() or not acquisition_channel.strip():
        raise ValueError("goal and acquisition_channel are required")
    return (
        GrowthExperiment(
            f"A highly shareable, opinionated asset will attract qualified people to {goal}.",
            ("Create a strong contrarian hook", f"Distribute through {acquisition_channel}", "Measure qualified traffic and repeat the strongest angle"),
            ("reach", "shares", "profile visits", "qualified leads"),
            "Polarization may reduce trust or attract low-fit traffic.",
            "awareness",
            "shares",
        ),
        GrowthExperiment(
            "A participatory challenge can create an acquisition-to-referral loop.",
            ("Define a 3-7 day micro-challenge", "Give participants a visible identity or badge", "Invite each participant to nominate one relevant person", "Showcase selected results"),
            ("challenge joins", "completion rate", "referral rate", "new qualified followers"),
            "Low-quality participation can dilute the brand or create moderation load.",
            "consideration",
            "referral rate",
        ),
        GrowthExperiment(
            "A free diagnostic or scorecard can turn attention into a qualified conversation.",
            ("Build a 3-5 question diagnostic", "Return a useful result plus one next action", "Make the result shareable", "Offer an optional next-step conversation"),
            ("completion rate", "shares", "profile visits", "conversation conversion"),
            "An overly broad diagnostic can create curiosity without commercial intent.",
            "conversion",
            "conversation conversion",
        ),
    )


def build_growth_plan(*, goal: str, acquisition_channel: str) -> dict[str, object]:
    """Build a compact Growth plan for orchestration and measurement."""
    experiments = growth_experiments(goal, acquisition_channel)
    return {
        "specialist": "Phoenix Growth",
        "goal": goal,
        "acquisition_channel": acquisition_channel,
        "funnel_stages": FUNNEL_STAGES,
        "experiments": experiments,
        "decision_owner": "human",
        "measurement_priority": ("retention", "saves", "shares", "qualified_leads", "conversion"),
    }


FRAMEWORKS = ("AARRR", "Hook Model", "Growth Loops", "Hypothesis-Driven Experimentation")
PLATFORMS = ("Instagram", "website", "CRM", "community")
