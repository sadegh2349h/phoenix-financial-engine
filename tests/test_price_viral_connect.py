from phoenix_core.connect_specialist import outreach_dm, partnership_plan
from phoenix_core.price_specialist import design_pricing
from phoenix_core.specialist_router import route_specialists
from phoenix_core.viral_specialist import engineer_reel


def test_price_has_three_tiers_and_behavioral_frameworks():
    model = design_pricing("coaching", "measurable transformation")
    assert [tier.role for tier in model.tiers] == ["tripwire", "best_value", "anchor"]
    assert "Anchoring" in model.pricing_mechanisms
    assert "Decoy Effect" in model.pricing_mechanisms
    assert len(model.objection_reframe) == 3


def test_viral_script_has_required_structure():
    script = engineer_reel("consistency is not the real growth lever", "personal branding")
    assert script.hook_0_3s
    assert script.value_story_3_15s
    assert script.twist_15_30s
    assert script.cta
    assert script.shareable_identity


def test_connect_builds_partnership_system():
    plan = partnership_plan("premium coaches", "wellness services")
    assert len(plan.partner_categories) == 5
    assert len(plan.campaign_formats) == 4
    assert len(plan.relationship_steps) >= 5
    assert outreach_dm("wellness providers", "premium coaches")


def test_router_routes_new_specialists_from_persian_problem():
    result = route_specialists(problem="قیمت گذاری، ریلز وایرال و همکاری با برندهای مکمل")
    keys = {item["key"] for item in result}
    assert keys & {"price", "viral", "connect"}
    assert all(item["human_approval_required"] for item in result)
