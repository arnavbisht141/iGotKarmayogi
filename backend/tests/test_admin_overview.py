import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.models.models import Assessment, AssessmentAttempt, Course, Enrollment, Question, User, UserProfile


@pytest.fixture(name="client")
def fixture_client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    admin = User(email="admin@example.gov.in", password_hash="x", full_name="Admin", role="admin")
    learner = User(email="learner@example.gov.in", password_hash="x", full_name="Learner")
    cpi = Course(title="CPI", overview="x", instructor="x", organization="MoSPI")
    nss = Course(title="NSS", overview="x", instructor="x", organization="MoSPI")
    db.add_all([admin, learner, cpi, nss])
    db.commit()

    db.add(UserProfile(user_id=learner.id, designation="Statistical Officer", department="NSO", onboarding_completed=True))
    assessment = Assessment(course_id=cpi.id, title="CPI exam")
    db.add(assessment)
    db.commit()

    q1 = Question(assessment_id=assessment.id, text="Q1", options_json="[]", correct_option_index=0, order=1)
    q2 = Question(assessment_id=assessment.id, text="Q2", options_json="[]", correct_option_index=1, order=2)
    db.add_all([q1, q2])
    db.commit()

    db.add_all([
        Enrollment(user_id=learner.id, course_id=cpi.id, status="completed"),
        Enrollment(user_id=learner.id, course_id=nss.id, status="in_progress"),
        AssessmentAttempt(user_id=learner.id, assessment_id=assessment.id, score_percent=100, passed=True,
                          answers_json=json.dumps({str(q1.id): 0, str(q2.id): 1})),
        AssessmentAttempt(user_id=learner.id, assessment_id=assessment.id, score_percent=50, passed=False,
                          answers_json=json.dumps({str(q1.id): 2, str(q2.id): 1})),
    ])
    db.commit()

    headers = {"Authorization": f"Bearer {create_access_token({'sub': str(admin.id)})}"}
    with TestClient(app) as test_client:
        yield test_client, headers, learner.id, cpi.id, q1.id, q2.id
    app.dependency_overrides.clear()
    db.close()


def test_admin_overview_aggregates(client):
    test_client, headers, learner_id, cpi_id, q1_id, q2_id = client
    data = test_client.get("/api/admin/overview", headers=headers).json()

    summary = data["summary"]
    assert (summary["total_users"], summary["total_courses"], summary["total_enrollments"]) == (2, 2, 2)
    assert summary["completion_rate_percent"] == 50.0
    assert summary["total_assessment_attempts"] == 2 and summary["overall_pass_rate_percent"] == 50.0

    learner = next(u for u in data["users"] if u["id"] == learner_id)
    assert learner["designation"] == "Statistical Officer" and learner["department"] == "NSO"
    assert learner["enrolled_courses_count"] == 2 and learner["completed_courses_count"] == 1
    assert {c["title"] for c in learner["courses"]} == {"CPI", "NSS"}

    admin = next(u for u in data["users"] if u["id"] != learner_id)
    assert admin["designation"] == "Not onboarded" and admin["courses"] == []

    cpi = next(c for c in data["course_analytics"] if c["id"] == cpi_id)
    assert cpi["enrolled_count"] == 1 and cpi["completion_rate_percent"] == 100.0 and cpi["assessment_pass_rate"] == 50.0

    by_question = {q["question_id"]: q for q in data["struggling_questions"]}
    assert by_question[q1_id]["accuracy_percent"] == 50.0 and by_question[q1_id]["assessment_title"] == "CPI exam"
    assert by_question[q2_id]["accuracy_percent"] == 100.0
    assert data["struggling_questions"][0]["question_id"] == q1_id  # sorted by accuracy ascending
