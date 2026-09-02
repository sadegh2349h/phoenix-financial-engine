from phoenix_core.growth_specialist import build_growth_plan, growth_experiments
from phoenix_core.phoenix_orchestrator import build_execution_plan


def test_growth_returns_three_funnel_mapped_experiments():
    experiments = growth_experiments("qualified leads", "Instagram")
    assert len(experiments) == 3
    assert tuple(item.funnel_stage for item in experiments) == ("awareness", "consideration", "conversion")
    assert all(item.human_approval_required for item in experiments)


def test_growth_plan_is_measurable_and_human_governed():
    plan = build_growth_plan(goal="qualified leads", acquisition_channel="Instagram")
    assert plan["specialist"] == "Phoenix Growth"
    assert "shares" in plan["measurement_priority"]
    assert plan["decision_owner"] == "human"


def test_orchestrator_includes_growth_plan_when_growth_is_routed():
    plan = build_execution_plan(
        problem="افزایش جذب مشتری از اینستاگرام",
        analysis={"business_goal": "qualified leads", "acquisition_channel": "Instagram"},
    )
    assert any(item["key"] == "growth" for item in plan["specialists"])
    assert plan["growth_plan"]["specialist"] == "Phoenix Growth"
    assert plan["decision_owner"] == "human"
