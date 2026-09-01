"""Phoenix Price: value-based pricing and behavioral-economics specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriceTier:
    name: str
    price: float
    value_proposition: str
    transformation_metrics: tuple[str, ...]
    role: str


@dataclass(frozen=True)
class PricingModel:
    tiers: tuple[PriceTier, ...]
    pricing_mechanisms: tuple[str, ...]
    objection_reframe: tuple[str, ...]


def design_pricing(core_service: str, transformation: str, currency: str = "IRR") -> PricingModel:
    """Create a three-tier value-based model; price is supplied as an input benchmark, not invented."""
    if not core_service.strip() or not transformation.strip():
        raise ValueError("core_service and transformation are required")
    return PricingModel(
        tiers=(
            PriceTier("Entry-Level (Tripwire)", 0, f"Low-friction entry into {transformation}.", ("baseline KPI", "first measurable win"), "tripwire"),
            PriceTier("Core Offer (Best Value)", 0, f"Primary transformation: {transformation} with guided implementation.", ("target KPI", "implementation rate", "outcome delta"), "best_value"),
            PriceTier("Premium VIP (High-Ticket)", 0, f"High-touch path to accelerate and deepen {transformation}.", ("target KPI", "time-to-result", "ROI / outcome value"), "anchor"),
        ),
        pricing_mechanisms=("Value-Based Pricing", "Tiered Packaging", "Anchoring", "Decoy Effect", "Price Framing", "Subscription Models"),
        objection_reframe=("Compare investment with the value of the desired outcome, not hours.", "Tie price to measurable transformation and avoided cost.", "Frame the purchase as an investment in identity, capability, and results."),
    )


FRAMEWORKS = ("Value-Based Pricing", "Anchoring", "Decoy Effect", "Price Framing")
