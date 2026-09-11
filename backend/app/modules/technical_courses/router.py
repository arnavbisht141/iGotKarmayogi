import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import (
    User, TechnicalTranscript, TechnicalLearningObjective, TechnicalLabTemplate,
    TechnicalGeneratedLab, TechnicalLabSolution, TechnicalLabValidationResult
)
from app.modules.technical_courses.schemas import (
    TranscriptIngestRequest, TranscriptProcessResponse,
    ObjectiveExtractionRequest, ObjectiveExtractionResponse,
    DecisionRequest, DecisionResponse,
    LabTemplateSchema, TemplateMatchRequest, TemplateMatchResponse,
    LabGenerationRequest, LabGenerationResponse,
    SolutionGenerationRequest, SolutionGenerationResponse,
    LabValidationResponse, FullPipelineRequest, FullPipelineResponse,
    GeneratedLabSchema, TestCaseSchema, ValidationResultSchema, TestResultItem
)
from app.modules.technical_courses.services.transcript_service import TranscriptService
from app.modules.technical_courses.services.objective_extractor import ObjectiveExtractor
from app.modules.technical_courses.services.decision_service import DecisionService
from app.modules.technical_courses.services.template_service import TemplateService
from app.modules.technical_courses.services.lab_generator import LabGenerator
from app.modules.technical_courses.services.solution_generator import SolutionGenerator
from app.modules.technical_courses.services.sandbox_service import SandboxService
from app.modules.technical_courses.services.pipeline_orchestrator import TechnicalPipelineOrchestrator


router = APIRouter(prefix="/technical-courses", tags=["technical-courses"])


# 1. Transcript Ingestion & Processing
@router.post("/process", response_model=TranscriptProcessResponse)
def process_transcript(
    req: TranscriptIngestRequest,
    db: Session = Depends(get_db)
):
    """
    Ingests, cleans, normalizes, and chunks a technical-course transcript.
    """
    try:
        return TranscriptService.process_and_persist(req, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process transcript: {str(e)}")


# 2. Learning Objective Extraction
@router.post("/objectives", response_model=ObjectiveExtractionResponse)
def extract_learning_objectives(
    req: ObjectiveExtractionRequest,
    db: Session = Depends(get_db)
):
    """
    Extracts structured, measurable learning objectives from technical course text.
    """
    try:
        return ObjectiveExtractor.extract_objectives(req, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract objectives: {str(e)}")


# 3. Quiz vs Lab Decision Layer
@router.post("/decide-mode", response_model=DecisionResponse)
def decide_assessment_mode(req: DecisionRequest):
    """
    Determines whether a learning objective is best suited for a Hands-on Lab or a Quiz.
    """
    return DecisionService.evaluate(req)


# 4. Lab Templates Catalog
@router.get("/templates", response_model=List[LabTemplateSchema])
def list_lab_templates(db: Session = Depends(get_db)):
    """
    Retrieves human-created lab templates defining structural constraints and test harnesses.
    """
    return TemplateService.get_all_templates(db=db)


# 5. Template Matching
@router.post("/match-template", response_model=TemplateMatchResponse)
def match_template_for_objective(
    req: TemplateMatchRequest,
    db: Session = Depends(get_db)
):
    """
    Matches a learning objective to the most suitable human-created lab template.
    """
    return TemplateService.match_template(req, db=db)


# 6. Lab Generation (Template Filling)
@router.post("/labs/generate", response_model=LabGenerationResponse)
def generate_lab_from_template(
    req: LabGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generates a concrete lab by filling a human-created template using structured LLM synthesis.
    """
    try:
        return LabGenerator.generate_lab(req, db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lab generation failed: {str(e)}")


# 7. Reference Solution Generation
@router.post("/labs/{lab_id}/solution", response_model=SolutionGenerationResponse)
def generate_solution_for_lab(
    lab_id: int,
    db: Session = Depends(get_db)
):
    """
    Generates candidate reference solution code for a generated lab.
    Note: Code is marked untrusted until sandbox validation passes.
    """
    try:
        return SolutionGenerator.generate_solution(
            SolutionGenerationRequest(lab_id=lab_id, persist=True),
            db=db
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Solution generation failed: {str(e)}")


# 8. Sandbox Validation
@router.post("/labs/{lab_id}/validate", response_model=LabValidationResponse)
def validate_lab_in_sandbox(
    lab_id: int,
    db: Session = Depends(get_db)
):
    """
    Validates a generated lab by executing its reference solution and test harness
    in an isolated Docker sandbox (or isolated subprocess testing fallback).
    """
    try:
        return SandboxService.validate_lab(lab_id=lab_id, db=db)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sandbox validation failed: {str(e)}")


# 9. Get Generated Lab Details
@router.get("/labs/{lab_id}")
def get_lab_details(
    lab_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves full details of a generated lab, including its solution, test cases, and validation history.
    """
    lab = db.query(TechnicalGeneratedLab).filter(TechnicalGeneratedLab.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")

    solution = db.query(TechnicalLabSolution).filter(TechnicalLabSolution.lab_id == lab.id).first()
    val_records = db.query(TechnicalLabValidationResult).filter(
        TechnicalLabValidationResult.lab_id == lab.id
    ).order_by(TechnicalLabValidationResult.validated_at.desc()).all()

    test_cases_raw = json.loads(lab.test_cases_json) if lab.test_cases_json else []
    constraints_raw = json.loads(lab.constraints_json) if lab.constraints_json else []

    validation_history = []
    for vr in val_records:
        test_summary = json.loads(vr.test_summary_json) if vr.test_summary_json else []
        validation_history.append({
            "id": vr.id,
            "is_valid": vr.is_valid,
            "sandbox_type": vr.sandbox_type,
            "exit_code": vr.exit_code,
            "execution_time_ms": vr.execution_time_ms,
            "stdout": vr.stdout,
            "stderr": vr.stderr,
            "test_summary": test_summary,
            "error_message": vr.error_message,
            "validated_at": vr.validated_at.isoformat() if vr.validated_at else None
        })

    return {
        "id": lab.id,
        "template_id": lab.template_id,
        "title": lab.title,
        "objective": lab.objective,
        "language": lab.language,
        "difficulty": lab.difficulty,
        "status": lab.status,
        "instructions": lab.instructions,
        "starter_code": lab.starter_code,
        "constraints": constraints_raw,
        "test_cases": test_cases_raw,
        "expected_behavior": lab.expected_behavior,
        "solution": {
            "id": solution.id,
            "reference_code": solution.reference_code,
            "explanation": solution.explanation
        } if solution else None,
        "latest_validation": validation_history[0] if validation_history else None,
        "validation_history": validation_history,
        "created_at": lab.created_at.isoformat() if lab.created_at else None
    }


# 10. End-to-End Pipeline Orchestration
@router.post("/pipeline/run-full", response_model=FullPipelineResponse)
def run_full_technical_pipeline(
    req: FullPipelineRequest,
    db: Session = Depends(get_db)
):
    """
    Convenience endpoint executing the entire technical course pipeline end-to-end:
    Transcript -> Objectives -> Decision -> Template Match -> Lab Gen -> Solution Gen -> Sandbox Validation.
    """
    try:
        return TechnicalPipelineOrchestrator.run_pipeline(req, db=db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")
