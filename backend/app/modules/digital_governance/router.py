from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.modules.digital_governance.schemas import (
    ScenarioListItem, CaseScenario, ScenarioSessionStartRequest,
    ScenarioSessionResponse, ScenarioAnswerRequest, ScenarioAnswerResponse,
    ScenarioSummary
)
from app.modules.digital_governance.services.scenario_service import (
    ScenarioRepository, ScenarioSessionManager
)

router = APIRouter(prefix="/digital-governance", tags=["digital-governance"])

# ── Scenario-Based Tabletop Questions Endpoints ──────────────────────────────

@router.get("/scenarios", response_model=List[ScenarioListItem])
def list_scenarios():
    """Returns official repository of Digital Governance incident response tabletop scenarios."""
    return ScenarioRepository.list_scenarios()

@router.get("/scenarios/{scenario_id}", response_model=CaseScenario)
def get_scenario_detail(scenario_id: str):
    """Retrieves full case scenario briefing and question tree."""
    scenario = ScenarioRepository.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.post("/scenarios/session/start", response_model=ScenarioSessionResponse)
def start_scenario_session(req: Optional[ScenarioSessionStartRequest] = None):
    """Initializes an interactive civil-service incident response tabletop simulation session."""
    scenario_id = req.scenario_id if req else None
    try:
        return ScenarioSessionManager.start_session(scenario_id=scenario_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/scenarios/session/{session_id}/answer", response_model=ScenarioAnswerResponse)
def submit_scenario_decision(session_id: str, req: ScenarioAnswerRequest):
    """
    Submits an operational decision for the active scenario checkpoint.
    Returns immediate consequence summary, statutory rationale, updated compliance score, and next branch.
    """
    try:
        return ScenarioSessionManager.submit_answer(session_id=session_id, option_id=req.option_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.get("/scenarios/session/{session_id}/summary", response_model=ScenarioSummary)
def get_scenario_session_summary(session_id: str):
    """Retrieves final executive debrief report and decision audit trail for a completed session."""
    summary = ScenarioSessionManager.get_session_summary(session_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Session summary not found or session still active")
    return summary
