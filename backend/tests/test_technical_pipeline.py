import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.models import TechnicalGeneratedLab
from app.modules.technical_courses.schemas import (
    TranscriptIngestRequest, ObjectiveExtractionRequest,
    DecisionRequest, TemplateMatchRequest, LabGenerationRequest,
    SolutionGenerationRequest, LearningObjectiveSchema, TestCaseSchema,
    GeneratedLabSchema
)
from app.modules.technical_courses.services.transcript_service import TranscriptService
from app.modules.technical_courses.services.decision_service import DecisionService
from app.modules.technical_courses.services.objective_extractor import ObjectiveExtractor
from app.modules.technical_courses.services.template_service import TemplateService
from app.modules.technical_courses.services.lab_generator import LabGenerator
from app.modules.technical_courses.services.solution_generator import SolutionGenerator
from app.modules.technical_courses.services.sandbox_service import SandboxService


# In-memory SQLite DB fixture for testing
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


# ============================================================================
# 1. TRANSCRIPT PROCESSING TESTS
# ============================================================================

def test_clean_transcript_subtitles_and_noise():
    raw = """WEBVTT
00:00:01.000 --> 00:00:04.500
[Music]
In this module, we will learn how to build REST APIs using FastAPI.

00:00:05.000 --> 00:00:08.000
12
We will define Pydantic schemas and handle error validation cleanly.
"""
    cleaned = TranscriptService.clean_transcript(raw)
    assert "WEBVTT" not in cleaned
    assert "00:00:01.000" not in cleaned
    assert "[Music]" not in cleaned
    assert "FastAPI" in cleaned
    assert "Pydantic" in cleaned


def test_transcript_chunking_and_metadata():
    text = "Sentence one. Sentence two. Sentence three. Sentence four. " * 50
    chunks = TranscriptService.chunk_transcript(text, chunk_size_chars=200, overlap_chars=30)
    assert len(chunks) > 1
    assert all(c.token_count > 0 for c in chunks)
    assert chunks[0].chunk_index == 0


def test_transcript_empty_input():
    cleaned = TranscriptService.clean_transcript("")
    assert cleaned == ""
    chunks = TranscriptService.chunk_transcript("")
    assert len(chunks) == 0


# ============================================================================
# 2. LEARNING OBJECTIVE EXTRACTION TESTS
# ============================================================================

def test_extract_objectives_fastapi(db_session):
    transcript = "In this lecture we explore FastAPI route handlers, Pydantic request models, and error responses."
    req = ObjectiveExtractionRequest(transcript_text=transcript)
    res = ObjectiveExtractor.extract_objectives(req, db=db_session)
    assert len(res.objectives) > 0
    obj = res.objectives[0]
    assert obj.skill == "FastAPI"
    assert obj.assessment_mode == "lab"
    assert obj.action in ["implement", "build", "develop", "create"]


def test_extract_objectives_empty(db_session):
    req = ObjectiveExtractionRequest(transcript_text="")
    res = ObjectiveExtractor.extract_objectives(req, db=db_session)
    assert len(res.objectives) == 0


# ============================================================================
# 3. QUIZ VS LAB DECISION ENGINE TESTS
# ============================================================================

def test_decision_engine_hands_on_lab():
    req = DecisionRequest(
        objective="Implement a FastAPI endpoint to filter citizen application records",
        skill="FastAPI",
        action="implement"
    )
    res = DecisionService.evaluate(req)
    assert res.assessment_mode == "lab"
    assert res.confidence >= 0.7
    assert res.recommended_lab_type == "implementation"


def test_decision_engine_conceptual_quiz():
    req = DecisionRequest(
        objective="Explain the theoretical foundations and history of consumer price indices",
        skill="Economic Statistics",
        action="explain"
    )
    res = DecisionService.evaluate(req)
    assert res.assessment_mode == "quiz"
    assert res.recommended_lab_type is None


def test_decision_engine_debugging_lab():
    req = DecisionRequest(
        objective="Debug and fix division by zero exceptions in data aggregation routines",
        skill="Python Debugging",
        action="debug"
    )
    res = DecisionService.evaluate(req)
    assert res.assessment_mode == "lab"
    assert res.recommended_lab_type == "debugging"


# ============================================================================
# 4. TEMPLATE MATCHING TESTS
# ============================================================================

def test_template_matching_exact():
    req = TemplateMatchRequest(
        objective="Implement a REST endpoint using FastAPI",
        skill="FastAPI",
        language="python"
    )
    res = TemplateService.match_template(req)
    assert res.matched is True
    assert res.template is not None
    assert "fastapi" in res.template.id


def test_template_matching_pandas():
    req = TemplateMatchRequest(
        objective="Clean and transform survey records using Pandas",
        skill="Pandas",
        language="python"
    )
    res = TemplateService.match_template(req)
    assert res.matched is True
    assert "pandas" in res.template.id


def test_template_matching_fallback():
    req = TemplateMatchRequest(
        objective="Perform complex custom algorithmic computation",
        skill="Algorithms",
        language="python"
    )
    res = TemplateService.match_template(req)
    assert res.matched is True
    assert res.template is not None


# ============================================================================
# 5. LAB GENERATION TESTS
# ============================================================================

def test_lab_generation_from_template(db_session):
    obj = LearningObjectiveSchema(
        objective="Implement REST API endpoints with request validation and structured error handling using FastAPI",
        skill="FastAPI",
        difficulty="intermediate",
        action="implement",
        assessment_mode="lab"
    )
    req = LabGenerationRequest(
        objective=obj,
        template_id="python-fastapi-crud-001",
        persist=True
    )
    res = LabGenerator.generate_lab(req, db=db_session)
    assert res.lab_id is not None
    assert res.template_id == "python-fastapi-crud-001"
    assert len(res.lab.test_cases) >= 2
    assert "process_api_request" in res.lab.starter_code
    assert len(res.lab.constraints) > 0


# ============================================================================
# 6. SOLUTION GENERATION TESTS
# ============================================================================

def test_solution_generation_untrusted_flag(db_session):
    obj = LearningObjectiveSchema(
        objective="Implement REST API endpoints",
        skill="FastAPI",
        action="implement"
    )
    lab_res = LabGenerator.generate_lab(
        LabGenerationRequest(objective=obj, template_id="python-fastapi-crud-001", persist=True),
        db=db_session
    )
    
    sol_res = SolutionGenerator.generate_solution(
        SolutionGenerationRequest(lab_id=lab_res.lab_id, persist=True),
        db=db_session
    )
    assert sol_res.solution_id is not None
    assert "def process_api_request" in sol_res.reference_code
    assert sol_res.is_trusted is False  # Must be untrusted until validated


# ============================================================================
# 7. SANDBOX VALIDATION TESTS
# ============================================================================

def test_sandbox_validation_passing_code():
    code = """
def process_api_request(items, query_id=None):
    if query_id is not None and query_id < 0:
        raise ValueError("Invalid query_id")
    if query_id is not None:
        filtered = [item for item in items if item.get("id") == query_id]
    else:
        filtered = list(items)
    return {
        "status": "success",
        "data": filtered,
        "count": len(filtered)
    }
"""
    test_cases = [
        TestCaseSchema(
            name="test_get_all",
            test_code="res = process_api_request([{'id': 1}, {'id': 2}]); assert res['count'] == 2"
        ),
        TestCaseSchema(
            name="test_filter",
            test_code="res = process_api_request([{'id': 1}, {'id': 2}], query_id=1); assert res['count'] == 1"
        )
    ]
    res = SandboxService.validate_code(code, test_cases)
    assert res.is_valid is True
    assert res.passed_tests_count == 2
    assert res.exit_code == 0
    assert len(res.test_results) == 2
    assert all(tr.passed for tr in res.test_results)


def test_sandbox_validation_failing_assertion():
    code = """
def process_api_request(items, query_id=None):
    return {"status": "failure", "data": [], "count": 0}
"""
    test_cases = [
        TestCaseSchema(
            name="test_get_all",
            test_code="res = process_api_request([{'id': 1}]); assert res['status'] == 'success'"
        )
    ]
    res = SandboxService.validate_code(code, test_cases)
    assert res.is_valid is False
    assert res.passed_tests_count == 0
    assert "AssertionFailed" in str(res.test_results[0].error)


def test_sandbox_validation_syntax_error():
    bad_code = "def broken_code(:\n  pass"
    test_cases = [TestCaseSchema(name="test_syntax", test_code="assert True")]
    res = SandboxService.validate_code(bad_code, test_cases)
    assert res.is_valid is False
    assert res.error_message is not None


def test_sandbox_validation_timeout_handling():
    infinite_loop_code = """
import time
while True:
    time.sleep(0.1)
"""
    test_cases = [TestCaseSchema(name="test_timeout", test_code="assert True")]
    res = SandboxService.validate_code(infinite_loop_code, test_cases, timeout_seconds=1)
    assert res.is_valid is False
    assert res.exit_code == -1
    assert "ExecutionTimedOut" in (res.error_message or "")


# ============================================================================
# 8. API ENDPOINT & END-TO-END INTEGRATION TESTS
# ============================================================================

def test_api_process_transcript(client):
    payload = {
        "title": "FastAPI Masterclass",
        "raw_text": "In this video we build FastAPI endpoints and test Pydantic serialization models."
    }
    resp = client.post("/api/technical-courses/process", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "FastAPI Masterclass"
    assert data["chunk_count"] >= 1


def test_api_extract_objectives(client):
    payload = {
        "transcript_text": "We will learn to implement REST APIs with FastAPI and validate schemas with Pydantic."
    }
    resp = client.post("/api/technical-courses/objectives", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["objectives"]) > 0


def test_api_decide_mode(client):
    payload = {
        "objective": "Build a data ingestion pipeline in Python",
        "skill": "Python",
        "action": "build"
    }
    resp = client.post("/api/technical-courses/decide-mode", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["assessment_mode"] == "lab"


def test_api_list_templates(client):
    resp = client.get("/api/technical-courses/templates")
    assert resp.status_code == 200
    templates = resp.json()
    assert len(templates) >= 3


def test_api_full_pipeline_end_to_end(client):
    payload = {
        "title": "Public Data Processing with Pandas",
        "transcript_text": "In this tutorial we will clean and transform tabular survey datasets using Pandas dataframe operations and aggregate statistics."
    }
    resp = client.post("/api/technical-courses/pipeline/run-full", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["objectives_count"] >= 1
    assert data["labs_generated_count"] >= 1
    assert data["validated_labs_count"] >= 1
    
    first_lab = data["labs"][0]
    lab_id = first_lab["lab_id"]
    assert first_lab["status"] == "validated"
    assert first_lab["is_valid"] is True

    # Test GET lab details
    get_resp = client.get(f"/api/technical-courses/labs/{lab_id}")
    assert get_resp.status_code == 200
    lab_details = get_resp.json()
    assert lab_details["status"] == "validated"
    assert lab_details["solution"] is not None
    assert lab_details["latest_validation"]["is_valid"] is True
