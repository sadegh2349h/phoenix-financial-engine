"""Phoenix Viral: short-form content and algorithmic retention specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViralScript:
    hook_0_3s: str
    value_story_3_15s: str
    twist_15_30s: str
    cta: str
    shareable_identity: str
    visual_editing: tuple[str, ...]


def engineer_reel(controversial_belief: str, niche: str) -> ViralScript:
    """Build a retention/share-oriented Reel structure without relying on generic trends."""
    if not controversial_belief.strip() or not niche.strip():
        raise ValueError("controversial_belief and niche are required")
    return ViralScript(
        hook_0_3s=f"VISUAL: pattern interrupt. AUDIO: decisive opening. Claim: {controversial_belief}",
        value_story_3_15s=f"Show the specific pain in {niche}, then prove the claim with one concrete example or contrast.",
        twist_15_30s="Reveal the counter-intuitive mechanism and one action the viewer can apply immediately.",
        cta="Save this for later and share it with the person who needs to hear it.",
        shareable_identity="Make sharing signal identity: 'I am the kind of person who knows/does this.'",
        visual_editing=("fast pattern interrupt in the first frame", "tight cuts around completed ideas", "on-screen keywords", "visual change at the insight/twist", "remove dead air"),
    )


FRAMEWORKS = ("Pattern Interrupt", "Controversial Truth", "Relatable Pain Point", "Shareable Identity")
PLATFORMS = ("Instagram Reels", "Short-form video")
