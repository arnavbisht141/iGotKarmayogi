import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, Course, Enrollment, Skill, CourseSkill
from app.agents.igot.client import MockIgotClient


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


def test_list_courses_filters_by_category(db_session):
    db_session.add_all([
        Course(title="Intro to GIS", overview="x", instructor="x", organization="MoSPI", category="technical"),
        Course(title="Leadership 101", overview="x", instructor="x", organization="ISTM", category="behavioural"),
    ])
    db_session.commit()

    client = MockIgotClient(db_session)
    technical_courses = client.list_courses(domain="technical")
    assert len(technical_courses) == 1
    assert technical_courses[0].title == "Intro to GIS"


def test_get_enrollment_status_none_when_not_enrolled(db_session):
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    course = Course(title="X", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()

    client = MockIgotClient(db_session)
    assert client.get_enrollment_status(user.id, course.id) is None


def test_get_enrollment_status_reflects_enrollment(db_session):
    user = User(email="c@d.gov.in", password_hash="x", full_name="C")
    course = Course(title="Y", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="in_progress"))
    db_session.commit()

    client = MockIgotClient(db_session)
    assert client.get_enrollment_status(user.id, course.id) == "in_progress"


def test_sync_completion_marks_enrollment_completed(db_session):
    user = User(email="e@f.gov.in", password_hash="x", full_name="E")
    course = Course(title="Z", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="in_progress"))
    db_session.commit()

    client = MockIgotClient(db_session)
    client.sync_completion(user.id, course.id)

    assert client.get_enrollment_status(user.id, course.id) == "completed"
