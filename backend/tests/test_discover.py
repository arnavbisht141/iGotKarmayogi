import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.models.models import Assessment, Course, Module, SearchHistory, User


@pytest.fixture(name="client")
def fixture_client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    with_modules = Course(title="CPI", overview="x", instructor="x", organization="MoSPI", category="Price Statistics", enrolled_count=900)
    bare = Course(title="Leadership", overview="x", instructor="x", organization="ISTM", category="Leadership", enrolled_count=100)
    db.add_all([user, with_modules, bare])
    db.commit()
    db.add_all([
        Module(course_id=with_modules.id, title="M1", order=1),
        Module(course_id=with_modules.id, title="M2", order=2),
        Assessment(course_id=with_modules.id, title="CPI exam"),
    ])
    now = datetime.datetime.utcnow()
    for minutes_ago, text in [(50, "sampling"), (40, "cpi"), (30, "sampling"), (20, "gdp"), (10, "cpi")]:
        db.add(SearchHistory(user_id=user.id, query=text, searched_at=now - datetime.timedelta(minutes=minutes_ago)))
    db.commit()

    headers = {"Authorization": f"Bearer {create_access_token({'sub': str(user.id)})}"}
    with TestClient(app) as test_client:
        yield test_client, headers, with_modules.id, bare.id
    app.dependency_overrides.clear()
    db.close()


def test_signed_in_discover_returns_distinct_recent_searches_newest_first(client):
    test_client, headers, _, _ = client
    data = test_client.get("/api/discover/courses?sort=popular", headers=headers).json()
    assert data["user_recent_searches"] == ["cpi", "gdp", "sampling"]


def test_discover_reports_module_counts_and_assessments(client):
    test_client, headers, with_modules_id, bare_id = client
    courses = {c["id"]: c for c in test_client.get("/api/discover/courses", headers=headers).json()["courses"]}
    assert courses[with_modules_id]["modules_count"] == 2 and courses[with_modules_id]["has_assessment"] is True
    assert courses[bare_id]["modules_count"] == 0 and courses[bare_id]["has_assessment"] is False
