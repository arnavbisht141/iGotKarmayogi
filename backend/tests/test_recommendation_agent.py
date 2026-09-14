import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, UserProfile, Course, CompetencyDomain, GapAnalysis, Recommendation
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.agents.recommendation.agent import generate_recommendations


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
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)
    try:
        yield db
    finally:
        db.close()


def _setup_user_with_gap(db, domain_code="technical", gap=2.0):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db.add(user)
    db.commit()
    db.refresh(user)
    domain = db.query(CompetencyDomain).filter_by(code=domain_code).first()
    db.add(GapAnalysis(user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=4.0 - gap, gap=gap))
    db.commit()
    return user


def test_no_recommendations_when_no_gaps(db_session):
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    recs = generate_recommendations(db_session, user.id, pinecone_index=MagicMock(), llm_client=MagicMock())
    assert recs == []


def test_recommends_matching_course_for_domain_gap(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "This course closes your Python gap."

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)

    assert len(recs) == 1
    assert recs[0].course_id == course.id
    assert recs[0].status == "pending"
    persisted = db_session.query(Recommendation).filter_by(user_id=user.id).all()
    assert len(persisted) == 1


def test_excludes_already_completed_courses(db_session):
    from app.models.models import Enrollment
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="completed"))
    db_session.commit()

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)
    assert recs == []


def test_falls_back_to_structured_filter_when_pinecone_unavailable(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.side_effect = Exception("network error")
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)
    # falls back to the structured-filter candidate list (still just the one technical course), doesn't raise
    assert len(recs) == 1
    assert recs[0].course_id == course.id
