import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

from app.core.database import Base
from app.models.models import User, CompetencyProfile, UserCompetencyScore
from app.core.seed_competencies import seed_competency_taxonomy
from app.models.models import Competency


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


def _make_user(db):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Test Officer")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_competency_profile(db_session):
    user = _make_user(db_session)
    profile = CompetencyProfile(user_id=user.id, statistical_score=42.0)
    db_session.add(profile)
    db_session.commit()
    fetched = db_session.query(CompetencyProfile).filter_by(user_id=user.id).first()
    assert fetched.statistical_score == 42.0
    assert fetched.technical_score == 0.0  # default


def test_one_profile_per_user(db_session):
    user = _make_user(db_session)
    db_session.add(CompetencyProfile(user_id=user.id))
    db_session.commit()
    db_session.add(CompetencyProfile(user_id=user.id))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_user_competency_score_unique_per_competency(db_session):
    seed_competency_taxonomy(db_session)
    user = _make_user(db_session)
    comp = db_session.query(Competency).filter_by(code="technical_python").first()
    db_session.add(UserCompetencyScore(user_id=user.id, competency_id=comp.id, level=3.0, evidence_source="assessment"))
    db_session.commit()
    db_session.add(UserCompetencyScore(user_id=user.id, competency_id=comp.id, level=4.0, evidence_source="assessment"))
    with pytest.raises(IntegrityError):
        db_session.commit()
