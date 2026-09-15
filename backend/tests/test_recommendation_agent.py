import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, UserProfile, Course, CompetencyDomain, GapAnalysis, Recommendation
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.agents.recommendation.agent import generate_recommendations


@pytest.fixture(autouse=True)
def fake_embeddings(monkeypatch):
    fake = MagicMock()
    fake.embed_query.return_value = [0.1] * 768
    monkeypatch.setattr("app.agents.recommendation.agent.get_embedding_client", lambda: fake)


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


def test_recommends_matching_course_with_real_seed_data_casing(db_session):
    # real seed_data.py stores category as Title Case with spaces ("Digital Governance"),
    # not the snake_case domain code ("digital_governance") the gap analysis uses.
    user = _setup_user_with_gap(db_session, domain_code="digital_governance", gap=2.0)
    course = Course(title="Cyber Hygiene", overview="x", instructor="x", organization="MoSPI", category="Digital Governance", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "This course closes your cybersecurity gap."

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)

    assert len(recs) == 1
    assert recs[0].course_id == course.id


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


def test_closed_gap_in_latest_row_is_not_shadowed_by_older_open_row(db_session):
    # gap_analyses is a history table: an older row with gap>0 for a domain must not
    # cause a recommendation once a newer row for that same domain has gap==0 (closed).
    import datetime
    user = User(email="g@h.gov.in", password_hash="x", full_name="G")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    domain = db_session.query(CompetencyDomain).filter_by(code="technical").first()
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical")
    db_session.add(course)
    db_session.commit()

    old_gap = GapAnalysis(
        user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=2.0, gap=2.0,
        generated_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
    )
    new_gap = GapAnalysis(
        user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=4.0, gap=0.0,
        generated_at=datetime.datetime.utcnow(),
    )
    db_session.add_all([old_gap, new_gap])
    db_session.commit()

    recs = generate_recommendations(db_session, user.id, pinecone_index=MagicMock(), llm_client=MagicMock())
    assert recs == []


def test_regenerating_recommendations_does_not_duplicate_pending_rows(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)
    generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)

    persisted = db_session.query(Recommendation).filter_by(user_id=user.id).all()
    assert len(persisted) == 1


def test_regenerating_recommendations_preserves_non_pending_rows(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    acted_on = Recommendation(user_id=user.id, course_id=course.id, reason="old", score=0.5, status="enrolled")
    db_session.add(acted_on)
    db_session.commit()
    db_session.refresh(acted_on)

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)

    persisted = db_session.query(Recommendation).filter_by(user_id=user.id).all()
    statuses = sorted(r.status for r in persisted)
    assert statuses == ["enrolled", "pending"]
    assert db_session.query(Recommendation).filter_by(id=acted_on.id).first() is not None


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
