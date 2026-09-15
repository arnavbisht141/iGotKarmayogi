import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.main import app
from app.models.models import Course, Enrollment, Recommendation, StatEngineMastery, User


@pytest.fixture(name="env")
def fixture_env():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    learner = User(email="learner@example.gov.in", password_hash="x", full_name="Learner", role="learner")
    admin = User(email="admin@example.gov.in", password_hash="x", full_name="Admin", role="admin")
    db.add_all([learner, admin])
    db.commit()
    headers = lambda u: {"Authorization": f"Bearer {create_access_token({'sub': str(u.id)})}"}
    with TestClient(app) as client:
        yield client, db, learner, headers(learner), headers(admin)
    app.dependency_overrides.clear()
    db.close()


def test_domain_detail_reflects_evidence_and_courses(env):
    client, db, learner, learner_headers, _ = env
    db.add(StatEngineMastery(user_id=str(learner.id), skill_id="price.price_relative", mastery_json=json.dumps({"score": 60.0})))
    db.add(Course(title="Price Statistics 101", overview="x", instructor="x", organization="MoSPI", category="Price Statistics"))
    db.add(Course(title="Leadership", overview="x", instructor="x", organization="ISTM", category="Public Administration"))
    db.commit()

    client.post("/api/competency/analyze", headers=learner_headers)
    detail = client.get("/api/competency/domains/statistical", headers=learner_headers).json()

    price = next(c for c in detail["competencies"] if c["code"] == "statistical_price_statistics")
    assert price["level"] == 3.0 and price["evidence_source"] == "assessment"
    assert [c["title"] for c in detail["courses"]] == ["Price Statistics 101"]
    assert detail["gap"] is not None


def test_unknown_domain_is_404(env):
    client, _, _, learner_headers, _ = env
    assert client.get("/api/competency/domains/astrology", headers=learner_headers).status_code == 404


def test_enrolling_from_recommendation_creates_enrollment(env):
    client, db, learner, learner_headers, _ = env
    course = Course(title="Sampling", overview="x", instructor="x", organization="MoSPI", category="Sample Surveys")
    db.add(course)
    db.commit()
    rec = Recommendation(user_id=learner.id, course_id=course.id, reason="closes gap", score=0.9)
    db.add(rec)
    db.commit()

    resp = client.patch(f"/api/recommendations/{rec.id}", headers=learner_headers, json={"status": "enrolled"})
    assert resp.status_code == 200 and resp.json()["status"] == "enrolled"
    assert db.query(Enrollment).filter_by(user_id=learner.id, course_id=course.id).count() == 1
    assert client.patch(f"/api/recommendations/{rec.id}", headers=learner_headers, json={"status": "bogus"}).status_code == 400


def test_admin_analytics_requires_admin_and_reports_distribution(env):
    client, _, _, learner_headers, admin_headers = env
    client.post("/api/competency/analyze", headers=learner_headers)
    assert client.get("/api/admin/competency-analytics", headers=learner_headers).status_code == 403

    data = client.get("/api/admin/competency-analytics", headers=admin_headers).json()
    assert data["profiled_learners"] == 1
    assert len(data["gap_distribution"]) == 4
    assert sum(d["major_gap"] + d["minor_gap"] + d["on_target"] for d in data["gap_distribution"]) == 4
    assert data["gap_trend"] and len(data["projections"]) == 4
