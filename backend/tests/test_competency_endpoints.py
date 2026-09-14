import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.models.models import User


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="client")
def fixture_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def fixture_auth_headers(db_session):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}, user.id


def test_gaps_returns_404_before_analyze(client, auth_headers):
    headers, _ = auth_headers
    resp = client.get("/api/competency/gaps", headers=headers)
    assert resp.status_code == 404


def test_analyze_then_profile_and_gaps(client, auth_headers):
    headers, _ = auth_headers
    analyze_resp = client.post("/api/competency/analyze", headers=headers)
    assert analyze_resp.status_code == 200
    assert len(analyze_resp.json()["gaps"]) == 4

    profile_resp = client.get("/api/competency/profile", headers=headers)
    assert profile_resp.status_code == 200

    gaps_resp = client.get("/api/competency/gaps", headers=headers)
    assert gaps_resp.status_code == 200
    assert len(gaps_resp.json()) == 4


def test_endpoints_require_auth(client):
    resp = client.get("/api/competency/profile")
    assert resp.status_code == 401
