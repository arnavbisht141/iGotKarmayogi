import io
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.models.models import User
from app.agents.quiz.extract import extract_text
from app.agents.quiz.generator import generate_quiz_questions

SOURCE = (
    "The Consumer Price Index measures the change in prices paid by consumers for a basket of goods and services. "
    "In India the base year for the all-India CPI is 2012, and the index is compiled by the National Statistics Office. "
    "The Laspeyres formula uses base period quantities as weights when aggregating price relatives across items. "
    "Inflation is commonly measured as the year-on-year percentage change in the Consumer Price Index. "
    "Sampling design determines how markets and outlets are selected for monthly price collection across states. "
    "Data quality frameworks require documented metadata, timeliness, accuracy and coherence for official statistics."
)


class FakeLLM:
    def invoke(self, prompt):
        reply = MagicMock()
        reply.content = """```json
[{"question": "What is the base year of the all-India CPI?", "options": ["2012", "2010", "2004", "2015"], "correct_index": 0, "explanation": "The source states the base year is 2012.", "concept": "CPI base year"},
 {"question": "Which weights does the Laspeyres formula use?", "options": ["Base period quantities", "Current quantities", "Equal weights", "Geometric weights"], "correct_index": 0, "explanation": "Laspeyres uses base period quantities.", "concept": "Laspeyres index"},
 {"question": "Broken question", "options": ["only one"], "correct_index": 0}]
```"""
        return reply


def test_extract_vtt_strips_cues():
    vtt = b"WEBVTT\n\n1\n00:00:01.000 --> 00:00:04.000\nPrice indices track inflation.\n\n2\n00:00:04.500 --> 00:00:06.000\n<b>Base year</b> matters.\n"
    assert extract_text("lecture.vtt", vtt) == "Price indices track inflation. Base year matters."


def test_extract_rejects_unsupported_type():
    with pytest.raises(ValueError):
        extract_text("clip.mp4", b"binary")


def test_llm_questions_are_validated_and_shuffled_consistently():
    questions, generator = generate_quiz_questions(SOURCE, num_questions=2, llm_client=FakeLLM())
    assert generator == "llm"
    assert len(questions) == 2  # the malformed third item is dropped
    base_year = next(q for q in questions if "base year" in q["question"])
    assert base_year["options"][base_year["correct_index"]] == "2012"


def test_fallback_generation_without_llm():
    class BrokenLLM:
        def invoke(self, prompt):
            raise RuntimeError("provider down")

    questions, generator = generate_quiz_questions(SOURCE, num_questions=3, llm_client=BrokenLLM())
    assert generator == "fallback"
    assert len(questions) == 3
    for q in questions:
        assert len(q["options"]) == 4 and 0 <= q["correct_index"] < 4


@pytest.fixture(name="client")
def fixture_client(monkeypatch):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def override_get_db():
        yield db

    monkeypatch.setattr("app.agents.recommendation.agent.get_llm_client", lambda: FakeLLM())
    app.dependency_overrides[get_db] = override_get_db
    user = User(email="trainer@example.gov.in", password_hash="x", full_name="Trainer")
    db.add(user)
    db.commit()
    db.refresh(user)
    headers = {"Authorization": f"Bearer {create_access_token({'sub': str(user.id)})}"}
    with TestClient(app) as test_client:
        yield test_client, headers
    app.dependency_overrides.clear()
    db.close()


def test_generate_take_and_score_quiz(client):
    test_client, headers = client
    resp = test_client.post(
        "/api/quiz/generate",
        headers=headers,
        data={"num_questions": "2", "difficulty": "intermediate", "title": "CPI basics"},
        files={"file": ("notes.txt", io.BytesIO(SOURCE.encode()), "text/plain")},
    )
    assert resp.status_code == 200, resp.text
    quiz = resp.json()
    assert quiz["question_count"] == 2 and quiz["can_manage"] is True

    answers = {str(q["id"]): q["correct_index"] for q in quiz["questions"]}
    answers[str(quiz["questions"][0]["id"])] = (quiz["questions"][0]["correct_index"] + 1) % 4

    result = test_client.post(f"/api/quiz/{quiz['id']}/submit", headers=headers, json={"answers": answers}).json()
    assert result["correct_count"] == 1 and result["score_percent"] == 50.0
    assert result["concepts_to_review"] == [quiz["questions"][0]["concept"]]

    listing = test_client.get("/api/quiz", headers=headers).json()
    assert listing[0]["best_score"] == 50.0


def test_generate_rejects_too_little_text(client):
    test_client, headers = client
    resp = test_client.post("/api/quiz/generate", headers=headers, data={"text": "too short"})
    assert resp.status_code == 422
