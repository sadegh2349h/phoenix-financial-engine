"""Phoenix Growth: growth-hacking and viral marketing specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GrowthExperiment:
    hypothesis: str
    execution_plan: tuple[str, ...]
    metric_to_track: tuple[str, ...]
    potential_risk: str


def growth_experiments(goal: str, acquisition_channel: str) -> tuple[GrowthExperiment, ...]:
    """Return three low-cost, measurable experiments for the Iranian market."""
    if not goal.strip() or not acquisition_channel.strip():
        raise ValueError("goal and acquisition_channel are required")
    return (
        GrowthExperiment(
            f"A highly shareable, opinionated asset will attract qualified people to {goal}.",
            ("Create a strong controversial/contrarian hook", "Remix it with 2-3 relevant creators or communities", "Publish on Instagram and route interested users to a Telegram continuation"),
            ("shares", "profile visits", "qualified leads", "activation rate"),
            "Polarization may reduce trust or attract low-fit traffic.",
        ),
        GrowthExperiment(
            "A participatory challenge can create an acquisition-to-referral loop.",
            ("Define a 3-7 day micro-challenge", "Give participants a visible identity/badge", "Ask each participant to nominate one relevant person", "Showcase selected results"),
            ("challenge joins", "completion rate", "referral rate", "new qualified followers"),
            "Low-quality participation can dilute the brand or create moderation load.",
        ),
        GrowthExperiment(
            "A free diagnostic/scorecard creates activation and a reason to share results.",
            ("Build a 3-5 question diagnostic", "Return a useful result plus one next action", "Use a shareable result card", "Offer an optional Telegram follow-up"),
            ("completion rate", "shares", "Telegram joins", "conversion to conversation"),
            "An overly broad diagnostic can generate curiosity without commercial intent.",
        ),
    )


FRAMEWORKS = ("AARRR", "Hook Model")
PLATFORMS = ("Instagram", "Telegram")
