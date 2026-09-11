import pytest
from app.statistical_engine.competency.mastery import mastery_evaluator
from app.statistical_engine.questions.branching import branching_engine

def test_mastery_increment_on_success():
    # Initial state None -> first success
    m1 = mastery_evaluator.update_mastery(
        current_mastery=None,
        skill_id="price.price_relative",
        correct=True
    )
    assert m1.score == 10.0
    assert m1.attempts_count == 1
    assert m1.correct_count == 1
    assert m1.remediation_recommended is False

    # Second success
    m2 = mastery_evaluator.update_mastery(
        current_mastery=m1.model_dump(),
        skill_id="price.price_relative",
        correct=True
    )
    assert m2.score == 20.0
    assert m2.attempts_count == 2
    assert m2.correct_count == 2

def test_mastery_decrement_on_failure():
    # Current score 30 -> failure decreases score
    initial = {"score": 30.0, "attempts_count": 3, "correct_count": 3, "consecutive_errors": 0}
    m = mastery_evaluator.update_mastery(
        current_mastery=initial,
        skill_id="price.price_relative",
        correct=False
    )
    assert m.score == 25.0
    assert m.attempts_count == 4

def test_branching_consecutive_errors_remediation():
    # 2 consecutive errors on CPI weighted relatives routes to prerequisite price.price_relative
    action = branching_engine.evaluate(
        skill_id="price.cpi.weighted_price_relatives",
        correct=False,
        misconception_id=None,
        consecutive_errors=2,
        mastery_score=40.0
    )
    assert action.type == "remediation"
    assert action.target_skill_id == "price.price_relative"

def test_branching_targeted_misconception():
    # Inverted ratio error triggers specific remediation notice
    action = branching_engine.evaluate(
        skill_id="price.price_relative",
        correct=False,
        misconception_id="err.price.inverted_ratio",
        consecutive_errors=1,
        mastery_score=50.0
    )
    assert action.type == "remediation"
    assert "numerator" in action.message.lower()

def test_branching_mastery_advancement():
    # Correct answer with 85% mastery advances to next skill
    action = branching_engine.evaluate(
        skill_id="price.price_relative",
        correct=True,
        misconception_id=None,
        consecutive_errors=0,
        mastery_score=85.0
    )
    assert action.type == "question"
    assert action.target_skill_id == "price.weights"
