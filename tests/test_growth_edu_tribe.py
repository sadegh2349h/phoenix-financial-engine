from phoenix_core.growth_specialist import growth_experiments
from phoenix_core.edu_specialist import design_course
from phoenix_core.tribe_specialist import design_community
from phoenix_core.specialist_router import route_specialists


def test_growth_returns_three_experiments():
    assert len(growth_experiments("audience acquisition", "Instagram")) == 3


def test_edu_starts_with_quick_win():
    assert "Quick Win" in design_course("coaching", "experts", "a measurable result")[0].title


def test_tribe_has_four_system_layers():
    community = design_community("people committed to transformation")
    assert community.onboarding_ritual and community.weekly_engagement_loop
    assert community.recognition_system and community.exclusive_benefits


def test_router_selects_top_two_relevant_specialists():
    result = route_specialists(problem="رشد و جذب مخاطب و طراحی دوره و جامعه")
    keys = {item["key"] for item in result}
    assert {"growth", "edu"}.issubset(keys)
    assert len(result) <= 2
