from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from .schemas import (
    GovernmentDocument,
    CaseScenario,
    CarryforwardQuestion,
    CarryforwardSessionStartRequest,
    CarryforwardAnswerRequest,
    CarryforwardAnswerResponse,
    CarryforwardSessionSummary,
    CaseGenerationRequest,
    InterviewStartRequest,
    InterviewTurnRequest,
    InterviewTurnResponse,
    InterviewEndRequest,
    InterviewAnalysisResponse
)
from .services.corpus import get_all_documents, get_document_by_id
from .services.carryforward_generator import (
    get_all_cases,
    get_case_by_id,
    generate_case_from_document
)
from .services.carryforward_session import CarryforwardSessionManager
from .services.interview_service import InterviewSessionManager

router = APIRouter(prefix="/behavioural", tags=["behavioural_cgp"])

# --- Corpus & Government Documents Endpoints ---

@router.get("/corpus", response_model=List[GovernmentDocument])
def list_government_documents():
    """Returns official repository of government notices, statutory forms, and proceedings."""
    return get_all_documents()

@router.get("/corpus/{doc_id}", response_model=GovernmentDocument)
def get_government_document(doc_id: str):
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Government document not found")
    return doc

# --- Carryforward Cases & Generator Endpoints ---

@router.get("/cases", response_model=List[CaseScenario])
def list_case_scenarios():
    """Returns all pre-seeded and active case scenarios."""
    return get_all_cases()

@router.get("/cases/{case_id}", response_model=CaseScenario)
def get_case_scenario(case_id: str):
    case = get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case scenario not found")
    return case

@router.post("/cases/generate", response_model=CaseScenario)
def generate_custom_case(req: CaseGenerationRequest):
    """
    Ingests raw government notice or form text and dynamically generates an authentic
    carryforward branching case scenario.
    """
    if not req.raw_text or len(req.raw_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Document text must contain at least 50 characters")
    case = generate_case_from_document(req)
    return case

# --- Interactive Carryforward Session Runner Endpoints ---

@router.post("/session/start")
def start_carryforward_session(req: Optional[CarryforwardSessionStartRequest] = None):
    """
    Initializes an interactive assessment session for carryforward case MCQs.
    """
    case_id = req.case_id if req else None
    session = CarryforwardSessionManager.create_session(case_id=case_id)
    
    current_q = session.current_question
    case = session.current_case
    
    return {
        "session_id": session.session_id,
        "case_id": case.id if case else None,
        "case_title": case.title if case else None,
        "document_title": case.document_title if case else None,
        "document_type": case.document_type if case else None,
        "initial_context": case.initial_context if case else None,
        "current_question": current_q
    }

@router.get("/session/{session_id}/current")
def get_current_session_question(session_id: str):
    session = CarryforwardSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session.session_id,
        "case_id": session.current_case.id if session.current_case else None,
        "case_title": session.current_case.title if session.current_case else None,
        "session_completed": session.session_completed,
        "total_steps": session.total_steps,
        "optimal_steps": session.optimal_steps,
        "current_question": session.current_question
    }

@router.post("/session/{session_id}/submit", response_model=CarryforwardAnswerResponse)
def submit_carryforward_answer(session_id: str, req: CarryforwardAnswerRequest):
    """
    Submits an answer to the current MCQ. If the answer introduces procedural complications
    or regulatory notice consequences, branches into a carryforward follow-up MCQ.
    If answered satisfactorily, concludes the scenario and advances to subsequent cases.
    """
    session = CarryforwardSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        res = session.submit_answer(
            question_id=req.question_id,
            selected_option_id=req.selected_option_id
        )
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/session/{session_id}/summary", response_model=CarryforwardSessionSummary)
def get_carryforward_session_summary(session_id: str):
    session = CarryforwardSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.get_summary()

# --- AI Live Feed Interview Endpoints ---

@router.post("/interview/start")
def start_live_interview(req: InterviewStartRequest):
    """
    Initiates a live AI oral competency interview related to the specified course.
    """
    session = InterviewSessionManager.start_interview(req)
    first_q = session.transcript[0].content
    return {
        "session_id": session.session_id,
        "course_id": session.course_id,
        "course_title": session.course_info["title"],
        "officer_name": session.officer_name,
        "target_duration_minutes": session.target_duration_minutes,
        "initial_ai_question": first_q,
        "current_phase": "Phase 1: Foundational Subject Matter & Conceptual Rigor",
        "primary_competency": "Course Knowledge"
    }

@router.post("/interview/turn", response_model=InterviewTurnResponse)
def submit_interview_turn(req: InterviewTurnRequest):
    """
    Submits the officer's verbal/text answer. The AI evaluates both course knowledge
    and the 6 behavioral competencies, generating an adaptive follow-up question.
    """
    session = InterviewSessionManager.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    turn_res = session.process_turn(
        officer_text=req.officer_response,
        elapsed_seconds=req.elapsed_seconds
    )
    return turn_res

@router.post("/interview/end", response_model=InterviewAnalysisResponse)
def conclude_interview_by_body(req: InterviewEndRequest):
    """Concludes the interview when session_id is supplied in the request body."""
    return conclude_and_analyze_interview(req.session_id)


@router.post("/interview/{session_id}/end", response_model=InterviewAnalysisResponse)
def conclude_and_analyze_interview(session_id: str):
    """
    Concludes the 25-35 min interview and generates the comprehensive diagnostic scorecard
    evaluating Course Knowledge + 6 Behavioral Competencies.
    """
    session = InterviewSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    analysis = session.generate_analysis()
    return analysis
