import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.statistical_engine.repositories.sql_repositories import (
    SQLQuestionRepository,
    SQLAttemptRepository,
    SQLLearnerRepository,
)
from app.statistical_engine.questions.generator import QuestionInternalRecord
from app.statistical_engine.schemas.questions import QuestionType, QuestionDifficulty


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def _make_record():
    return QuestionInternalRecord(
        question_id="q-test-1",
        template_id="tmpl-1",
        skill_id="price_statistics_cpi",
        competency_id="price_statistics",
        question_type=QuestionType.MCQ,
        difficulty=QuestionDifficulty.BASIC,
        prompt="What is the CPI base year?",
        parameters={"base_year": 2012},
        correct_answer="A",
        tolerance=0.0,
        options_map={"A": (2012, None), "B": (2010, "wrong_base_year")},
        correct_option_id="A",
        explanation="Base year is 2012=100.",
        unit="index",
        chart=None,
        seed=42,
    )


def test_question_repo_round_trip(db_session):
    repo = SQLQuestionRepository(db_session)
    record = _make_record()
    repo.save_instance(record)

    fetched = repo.get_instance("q-test-1")
    assert fetched is not None
    assert fetched.prompt == "What is the CPI base year?"
    assert fetched.options_map["A"] == (2012, None)
    assert fetched.options_map["B"] == (2010, "wrong_base_year")
    assert fetched.question_type == QuestionType.MCQ
    assert fetched.difficulty == QuestionDifficulty.BASIC
    assert fetched.parameters == {"base_year": 2012}


def test_question_repo_missing_returns_none(db_session):
    repo = SQLQuestionRepository(db_session)
    assert repo.get_instance("does-not-exist") is None


def test_attempt_repo_filters_by_skill(db_session):
    repo = SQLAttemptRepository(db_session)
    repo.record_attempt({"attempt_id": "att-1", "user_id": "u1", "question_id": "q1", "skill_id": "skill_a", "submitted_answer": "A", "is_correct": True, "score": 1.0, "misconception_id": None, "time_taken_seconds": 12, "timestamp": "2026-01-01T00:00:00"})
    repo.record_attempt({"attempt_id": "att-2", "user_id": "u1", "question_id": "q2", "skill_id": "skill_b", "submitted_answer": "B", "is_correct": False, "score": 0.0, "misconception_id": "m1", "time_taken_seconds": 8, "timestamp": "2026-01-01T00:01:00"})

    all_attempts = repo.get_user_attempts("u1")
    assert len(all_attempts) == 2
    skill_a_only = repo.get_user_attempts("u1", skill_id="skill_a")
    assert len(skill_a_only) == 1
    assert skill_a_only[0]["is_correct"] is True


def test_learner_repo_upsert_mastery(db_session):
    repo = SQLLearnerRepository(db_session)
    repo.update_user_skill_mastery("u1", "skill_a", {"score": 0.4, "attempts": 1})
    repo.update_user_skill_mastery("u1", "skill_a", {"score": 0.6, "attempts": 2})

    mastery = repo.get_user_mastery("u1")
    assert mastery["skill_a"]["score"] == 0.6
    assert mastery["skill_a"]["attempts"] == 2
