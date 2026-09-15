import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, GapAnalysis, Recommendation, Course
from app.core.seed_competencies import seed_competency_taxonomy
from app.models.models import CompetencyDomain


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


def test_gap_analysis_row(db_session):
    seed_competency_taxonomy(db_session)
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    db_session.add(user)
    db_session.commit()
    domain = db_session.query(CompetencyDomain).filter_by(code="technical").first()

    gap = GapAnalysis(user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=1.5, gap=2.5)
    db_session.add(gap)
    db_session.commit()

    fetched = db_session.query(GapAnalysis).filter_by(user_id=user.id).first()
    assert fetched.gap == 2.5
    assert fetched.domain.code == "technical"


def test_recommendation_defaults_to_pending(db_session):
    user = User(email="c@d.gov.in", password_hash="x", full_name="C")
    course = Course(title="Intro to GIS", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()

    rec = Recommendation(user_id=user.id, course_id=course.id, reason="Closes GIS gap", score=0.87)
    db_session.add(rec)
    db_session.commit()

    fetched = db_session.query(Recommendation).filter_by(user_id=user.id).first()
    assert fetched.status == "pending"
    assert fetched.course.title == "Intro to GIS"


def test_recommendation_without_course(db_session):
    user = User(email="e@f.gov.in", password_hash="x", full_name="E")
    db_session.add(user)
    db_session.commit()
    rec = Recommendation(user_id=user.id, course_id=None, reason="General upskilling", score=0.5)
    db_session.add(rec)
    db_session.commit()
    assert db_session.query(Recommendation).filter_by(user_id=user.id).first().course_id is None
