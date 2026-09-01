"""Phoenix Connect: strategic partnerships and business-development specialist."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartnershipPlan:
    partner_categories: tuple[str, ...]
    campaign_formats: tuple[str, ...]
    relationship_steps: tuple[str, ...]
    revenue_model: str


def partnership_plan(ideal_client: str, loved_non_competing_services: str) -> PartnershipPlan:
    """Create a value-first partnership system around the same ideal client."""
    if not ideal_client.strip() or not loved_non_competing_services.strip():
        raise ValueError("ideal_client and loved_non_competing_services are required")
    return PartnershipPlan(
        partner_categories=("complementary premium brands", "wellness/beauty providers", "education/coaching ecosystems", "professional communities", "technology/tools already used by the client"),
        campaign_formats=("co-hosted webinar", "bundle offer", "guest takeover", "exclusive community event"),
        relationship_steps=("research fit", "lead with partner value", "propose a small pilot", "measure qualified audience and revenue", "formalize repeatable joint venture", "review revenue share and expand"),
        revenue_model="Use a transparent revenue-share or reciprocal-value agreement tied to attributable qualified leads/sales; define attribution and settlement before launch.",
    )


def outreach_dm(partner_category: str, ideal_client: str) -> str:
    """Return a concise value-first outreach draft for a partner category."""
    if not partner_category.strip() or not ideal_client.strip():
        raise ValueError("partner_category and ideal_client are required")
    return (f"سلام؛ فکر می‌کنم مخاطب مشترکی داریم: {ideal_client}. "
            f"به‌جای تبلیغ متقابل ساده، یک همکاری کوچک و قابل‌اندازه‌گیری در حوزه {partner_category} پیشنهاد می‌کنم "
            "که برای هر دو طرف ارزش واقعی بسازد. اگر موافق باشید، یک پایلوت کوتاه با KPI مشخص طراحی کنیم و فقط در صورت نتیجه، آن را توسعه بدهیم.")


FRAMEWORKS = ("Value-First Outreach", "Joint Venture Structuring")
