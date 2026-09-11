import pytest
from app.statistical_engine.questions.generator import question_generator
from app.statistical_engine.schemas.questions import QuestionType, QuestionDifficulty

def test_question_generation_reproducibility():
    """Verify that identical seeds produce the exact same question instance and parameters."""
    seed = 42891
    q1, r1 = question_generator.generate_question(
        skill_id="price.price_relative",
        seed=seed
    )
    q2, r2 = question_generator.generate_question(
        skill_id="price.price_relative",
        seed=seed
    )

    assert q1.question_id == q2.question_id
    assert q1.prompt == q2.prompt
    assert q1.data == q2.data
    assert r1.correct_answer == r2.correct_answer

def test_mcq_options_are_distinct():
    """Verify that for MCQ templates, all generated options are mutually distinct and non-empty."""
    q, r = question_generator.generate_question(
        skill_id="price.cpi.weighted_price_relatives",
        question_type=QuestionType.MCQ,
        seed=101
    )

    assert q.options is not None
    assert len(q.options) >= 3
    texts = [o.text for o in q.options]
    assert len(texts) == len(set(texts))
    assert r.correct_option_id in [o.id for o in q.options]

def test_numeric_question_tolerance():
    """Verify numeric question answer generation has valid tolerance and answer is withheld from client."""
    q, r = question_generator.generate_question(
        skill_id="price.inflation_rate",
        question_type=QuestionType.NUMERIC,
        seed=555
    )

    assert q.type == QuestionType.NUMERIC
    assert r.tolerance > 0
    # Crucial security guarantee: client question does NOT have correct answer field
    assert not hasattr(q, "correct_answer")

def test_fisher_question_advanced():
    """Verify Fisher Ideal Index template generation at advanced level."""
    q, r = question_generator.generate_question(
        skill_id="price.fisher_index",
        difficulty=QuestionDifficulty.ADVANCED,
        seed=999
    )
    assert q.skill_id == "price.fisher_index"
    assert q.difficulty == QuestionDifficulty.ADVANCED
    assert float(r.correct_answer) > 0
