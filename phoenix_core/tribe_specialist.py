"""Phoenix Tribe: community architecture and engagement specialist."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class CommunitySystem:
    onboarding_ritual: tuple[str, ...]
    weekly_engagement_loop: tuple[str, ...]
    recognition_system: tuple[str, ...]
    exclusive_benefits: tuple[str, ...]


def design_community(core_identity: str) -> CommunitySystem:
    """Design a shared-identity community system, not a generic group chat."""
    if not core_identity.strip():
        raise ValueError("core_identity is required")
    return CommunitySystem(
        onboarding_ritual=(f"Declare the shared identity: {core_identity}", "Introduce one personal commitment", "Complete a first contribution"),
        weekly_engagement_loop=("weekly ritual", "member challenge", "peer contribution", "reflection/result post"),
        recognition_system=("contribution badges", "member spotlight", "peer nominations", "milestone recognition"),
        exclusive_benefits=("private sessions", "early access", "member-only resources", "collaboration opportunities"),
    )


FRAMEWORKS = ("Community Canvas", "Gamification Mechanics", "Social Identity Theory")
