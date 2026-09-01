"""Phoenix Story: narrative strategy for transformation-led brands."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class StoryArc:
    hook_status_quo: str
    inciting_pain: str
    struggle_journey: str
    breakthrough_solution: str
    new_identity: str


def craft_story(client_before: str, struggle: str, breakthrough: str, new_identity: str) -> StoryArc:
    if not all(x.strip() for x in (client_before, struggle, breakthrough, new_identity)):
        raise ValueError("all story inputs are required")
    return StoryArc(
        client_before,
        struggle,
        "Show the human journey, tension, doubts, attempts and turning point.",
        breakthrough,
        new_identity,
    )

FRAMEWORKS = ("Hero's Journey", "StoryBrand", "Three-Act Structure")
ROLE = "client as hero; Phoenix as guide"
