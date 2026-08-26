from phoenix_core.decision_engine import Decision
from phoenix_core.risk_engine import RiskEngine


def test_high_risk_decision_is_blocked_until_review():
    decision = Decision("ready", "review_recommendation", 0.9, ("test",), True)
    assessment = RiskEngine().assess(decision=decision)
    assert assessment.level == "high"
    assert assessment.blocked is True


def test_low_confidence_is_elevated():
    decision = Decision("ready", "review_recommendation", 0.2, ("weak evidence",), False)
    assessment = RiskEngine().assess(decision=decision)
    assert assessment.level == "high"
    assert assessment.blocked is True
