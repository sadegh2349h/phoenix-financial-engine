from phoenix_core.oss_evaluation_report import (
    acceptance_threshold,
    pilot_evaluations,
    recommended_evaluations,
)


def test_acceptance_threshold_is_80():
    assert acceptance_threshold() == 80


def test_recommendations_meet_threshold():
    assert recommended_evaluations()
    assert all(item.score >= acceptance_threshold() for item in recommended_evaluations())


def test_pilots_are_below_threshold():
    assert pilot_evaluations()
    assert all(item.score < acceptance_threshold() for item in pilot_evaluations())
