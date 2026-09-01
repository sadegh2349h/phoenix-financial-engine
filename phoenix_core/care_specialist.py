"""Phoenix Care: customer success and retention specialist."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class CareJourney:
    welcome_sequence: tuple[str, ...]
    check_in_milestones: tuple[str, ...]
    loyalty_reward_system: tuple[str, ...]
    churn_points: tuple[str, ...]
    referral_moment: str


def design_customer_journey(service: str) -> CareJourney:
    if not service.strip():
        raise ValueError("service is required")
    return CareJourney(
        ("warm welcome", "clear next step", "expectation setting", "first quick win"),
        ("Day 1", "Day 7", "Day 30", "Day 60", "Day 90"),
        ("milestone recognition", "surprise and delight", "loyalty benefits", "referral rewards"),
        ("unclear onboarding", "slow early result", "communication gap", "plateau", "expectation mismatch"),
        "Ask for testimonial/referral immediately after a documented peak outcome or delight moment.",
    )

FRAMEWORKS = ("First 90 Days", "Peak-End Rule", "Surprise and Delight")
