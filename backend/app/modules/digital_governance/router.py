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


# ── Cybersecurity Sandbox & CTF Pipeline Endpoints ───────────────────────────

from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.digital_governance.schemas import (
    SandboxChallengeSummary,
    SandboxGenerateRequest,
    SandboxGenerateResponse,
    SandboxStartRequest,
    SandboxSessionResponse,
    SandboxFlagSubmitRequest,
    SandboxFlagSubmitResponse,
    SandboxHintUnlockRequest,
    SandboxHintUnlockResponse,
    UserCompetencyRadar,
    TopicGenerateRequest,
)
from app.modules.digital_governance.services.sandbox_manager import sandbox_manager
from app.modules.digital_governance.services.supabase_service import supabase_knowledge_service


@router.get("/sandbox/challenges", response_model=List[SandboxChallengeSummary])
def list_sandbox_challenges(db: Session = Depends(get_db)):
    """Lists available static and dynamically generated CTF challenges from the database."""
    return sandbox_manager.list_challenges(db=db)


@router.get("/sandbox/knowledge-base")
def get_digital_governance_knowledge_base():
    """
    Retrieves the 5 Digital Governance pillars, scraped Wikipedia articles, and video curricula
    from the live Supabase instance (strictly read-only GET).
    """
    return supabase_knowledge_service.get_full_knowledge_base()


@router.post("/sandbox/generate-from-topic", response_model=SandboxGenerateResponse)
async def generate_sandbox_from_topic(req: TopicGenerateRequest, db: Session = Depends(get_db)):
    """
    Fetches the scraped Wikipedia article for the selected topic from Supabase,
    runs the Multi-LLM procedural challenge compiler, and persists the challenge to the database.
    """
    kb = supabase_knowledge_service.get_full_knowledge_base()
    matched_item = next((item for item in kb if req.topic_name.lower() in item["topic_name"].lower()), None)
    if not matched_item:
        raise HTTPException(status_code=404, detail=f"Topic '{req.topic_name}' not found in Digital Governance knowledge base")

    text_to_use = matched_item.get("full_text") or matched_item.get("body_snippet") or req.topic_name
    try:
        res = await sandbox_manager.generate_from_transcript(
            transcript_text=text_to_use,
            student_id=req.student_id or "nodal_officer_01",
            db=db,
        )
        return SandboxGenerateResponse(
            challenge_id=res["challenge_id"],
            title=res["title"],
            category=res["category"],
            difficulty=res["difficulty"],
            points=res["points"],
            objectives=res["objectives"],
            scenario_md=res["scenario_md"],
            extracted_meta=res["extracted_meta"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Topic generation failed: {str(e)}")


@router.post("/sandbox/generate", response_model=SandboxGenerateResponse)
async def generate_sandbox_from_transcript(req: SandboxGenerateRequest, db: Session = Depends(get_db)):
    """
    Ingests video/lecture transcripts, extracts learning objectives and tags via Multi-LLM,
    matches challenge templates, fills slots, and returns a compiled challenge package saved to the DB.
    """
    try:
        res = await sandbox_manager.generate_from_transcript(
            transcript_text=req.transcript_text,
            student_id=req.student_id or "nodal_officer_01",
            db=db,
        )
        return SandboxGenerateResponse(
            challenge_id=res["challenge_id"],
            title=res["title"],
            category=res["category"],
            difficulty=res["difficulty"],
            points=res["points"],
            objectives=res["objectives"],
            scenario_md=res["scenario_md"],
            extracted_meta=res["extracted_meta"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.post("/sandbox/session/start", response_model=SandboxSessionResponse)
async def start_sandbox_session(req: SandboxStartRequest, db: Session = Depends(get_db)):
    """Spawns an isolated Marimo instance from DB telemetry and starts the interactive challenge timer."""
    try:
        return await sandbox_manager.start_session(
            challenge_id=req.challenge_id,
            duration_minutes=req.duration_minutes or 45,
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start sandbox session: {str(e)}")


@router.get("/sandbox/session/{session_id}", response_model=SandboxSessionResponse)
def get_sandbox_session_status(session_id: str, db: Session = Depends(get_db)):
    """Checks session status, remaining TTL seconds, and unlocked hints."""
    sess = sandbox_manager.get_session(session_id, db=db)
    if not sess:
        raise HTTPException(status_code=404, detail="Sandbox session not found")
    return sess


@router.post("/sandbox/session/{session_id}/stop")
async def stop_sandbox_session(session_id: str, db: Session = Depends(get_db)):
    """Stops the active Marimo instance and marks session as terminated."""
    ok = await sandbox_manager.stop_session(session_id, db=db)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Sandbox session stopped successfully", "session_id": session_id}


@router.post("/sandbox/session/submit-flag", response_model=SandboxFlagSubmitResponse)
def submit_sandbox_flag(req: SandboxFlagSubmitRequest, db: Session = Depends(get_db)):
    """Validates the officer's submitted FLAG{...}, applies hint deductions, and records competency points in DB."""
    return sandbox_manager.submit_flag(
        session_id=req.session_id,
        flag_attempt=req.flag,
        db=db,
        challenge_id=req.challenge_id,
    )


@router.post("/sandbox/session/unlock-hint", response_model=SandboxHintUnlockResponse)
def unlock_sandbox_hint(req: SandboxHintUnlockRequest, db: Session = Depends(get_db)):
    """Unlocks a tiered hint for the challenge and records the point penalty in DB."""
    return sandbox_manager.unlock_hint(
        session_id=req.session_id,
        hint_id=req.hint_id,
        db=db,
        challenge_id=req.challenge_id,
    )


@router.get("/sandbox/competencies", response_model=UserCompetencyRadar)
def get_user_cyber_competencies(db: Session = Depends(get_db)):
    """Returns officer's competency matrix across the 5 digital governance cyber defense pillars."""
    return sandbox_manager.get_competencies(db=db)


