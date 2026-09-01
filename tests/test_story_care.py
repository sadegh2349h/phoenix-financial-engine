from phoenix_core.story_specialist import craft_story
from phoenix_core.care_specialist import design_customer_journey
from phoenix_core.specialist_router import route_specialists


def test_story_has_five_part_transformation_arc():
    story = craft_story("before", "pain", "breakthrough", "new identity")
    assert story.hook_status_quo == "before"
    assert story.inciting_pain == "pain"
    assert story.breakthrough_solution == "breakthrough"
    assert story.new_identity == "new identity"


def test_care_has_first_90_days_system():
    journey = design_customer_journey("premium coaching")
    assert len(journey.check_in_milestones) == 5
    assert journey.referral_moment
    assert journey.churn_points


def test_router_routes_story_and_care():
    result = route_specialists(problem="داستان تحول مشتری و رضایت و ماندگاری مشتری")
    keys = {item["key"] for item in result}
    assert keys & {"story", "care"}
    assert all(item["human_approval_required"] for item in result)
