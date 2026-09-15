import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import BehaviouralSessionResult
from app.modules.behavioural_cgp.services.result_store import save_behavioural_result


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


def test_save_and_read_carryforward_result(db_session):
    save_behavioural_result(
        db_session,
        session_id="cf_sess_abc123",
        session_type="carryforward",
        user_id=None,
        case_or_course_id="case_mospi_nqaf_audit",
        score=82.5,
        result_payload={"procedural_compliance_score": 82.5, "competency_scores": {"Leadership": 78.0}},
    )
    row = db_session.query(BehaviouralSessionResult).filter_by(session_id="cf_sess_abc123").first()
    assert row is not None
    assert row.session_type == "carryforward"
    assert row.score == 82.5
    assert row.user_id is None


def test_save_result_with_user_id(db_session):
    save_behavioural_result(
        db_session,
        session_id="int_sess_xyz789",
        session_type="interview",
        user_id=7,
        case_or_course_id="12",
        score=64.0,
        result_payload={"overall_score": 64.0},
    )
    row = db_session.query(BehaviouralSessionResult).filter_by(session_id="int_sess_xyz789").first()
    assert row.user_id == 7
    assert row.session_type == "interview"


def test_save_is_upsert_on_session_id(db_session):
    save_behavioural_result(db_session, session_id="s1", session_type="carryforward", user_id=None, case_or_course_id="c1", score=50.0, result_payload={})
    save_behavioural_result(db_session, session_id="s1", session_type="carryforward", user_id=None, case_or_course_id="c1", score=90.0, result_payload={})
    rows = db_session.query(BehaviouralSessionResult).filter_by(session_id="s1").all()
    assert len(rows) == 1
    assert rows[0].score == 90.0
