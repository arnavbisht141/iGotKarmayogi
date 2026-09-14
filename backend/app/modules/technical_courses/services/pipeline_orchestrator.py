import time
import json
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.modules.technical_courses.schemas import (
    FullPipelineRequest, FullPipelineResponse, TranscriptIngestRequest,
    ObjectiveExtractionRequest, TemplateMatchRequest, LabGenerationRequest,
    SolutionGenerationRequest, LearningObjectiveSchema
)
from app.modules.technical_courses.services.transcript_service import TranscriptService
from app.modules.technical_courses.services.objective_extractor import ObjectiveExtractor
from app.modules.technical_courses.services.decision_service import DecisionService
from app.modules.technical_courses.services.template_service import TemplateService
from app.modules.technical_courses.services.lab_generator import LabGenerator
from app.modules.technical_courses.services.solution_generator import SolutionGenerator
from app.modules.technical_courses.services.sandbox_service import SandboxService


class TechnicalPipelineOrchestrator:
    """
    Coordinates the full end-to-end Technical Course Content Generation Pipeline:
    Transcript -> Objectives -> Decision (Lab vs Quiz) -> Template Matching -> 
    Lab Generation -> Solution Generation -> Sandbox Validation -> Validated Lab.
    """

    @classmethod
    def run_pipeline(
        cls,
        req: FullPipelineRequest,
        db: Session
    ) -> FullPipelineResponse:
        t0 = time.perf_counter()
        timing_breakdown: Dict[str, float] = {}

        # 1. Transcript Ingestion & Cleaning
        t_start = time.perf_counter()
        transcript_res = TranscriptService.process_and_persist(
            TranscriptIngestRequest(
                title=req.title,
                raw_text=req.transcript_text,
                course_id=req.course_id
            ),
            db=db
        )
        timing_breakdown["transcript_processing_ms"] = round((time.perf_counter() - t_start) * 1000, 2)

        # 2. Structured Learning Objective Extraction
        t_start = time.perf_counter()
        objectives_res = ObjectiveExtractor.extract_objectives(
            ObjectiveExtractionRequest(
                transcript_text=transcript_res.chunks[0].text if transcript_res.chunks else req.transcript_text,
                transcript_id=transcript_res.id,
                course_id=req.course_id
            ),
            db=db
        )
        timing_breakdown["objective_extraction_ms"] = round((time.perf_counter() - t_start) * 1000, 2)

        objectives = objectives_res.objectives
        generated_labs_list: List[Dict[str, Any]] = []
        validated_count = 0

        # Process each lab-suitable objective
        for obj in objectives:
            if obj.assessment_mode == "lab":
                # 3. Template Matching
                t_start = time.perf_counter()
                match_res = TemplateService.match_template(
                    TemplateMatchRequest(
                        objective=obj.objective,
                        skill=obj.skill,
                        difficulty=req.target_difficulty or obj.difficulty,
                        language=req.preferred_language
                    ),
                    db=db
                )
                matched_template = match_res.template
                template_id = matched_template.id if matched_template else "python-fastapi-crud-001"

                # 4. Lab Generation (Filling Template)
                lab_res = LabGenerator.generate_lab(
                    LabGenerationRequest(
                        objective=obj,
                        template_id=template_id,
                        persist=True
                    ),
                    db=db
                )
                lab_id = lab_res.lab_id

                # 5. Solution Generation
                sol_res = SolutionGenerator.generate_solution(
                    SolutionGenerationRequest(
                        lab_id=lab_id,
                        lab_schema=lab_res.lab,
                        persist=True
                    ),
                    db=db
                )

                # 6. Sandbox Validation
                val_res = SandboxService.validate_lab(
                    lab_id=lab_id,
                    db=db
                )

                if val_res.is_valid:
                    validated_count += 1

                generated_labs_list.append({
                    "lab_id": lab_id,
                    "template_id": template_id,
                    "title": lab_res.lab.title,
                    "objective": lab_res.lab.objective,
                    "status": val_res.status,
                    "is_valid": val_res.is_valid,
                    "sandbox_type": val_res.validation_details.sandbox_type,
                    "passed_tests": f"{val_res.validation_details.passed_tests_count}/{val_res.validation_details.total_tests_count}",
                    "execution_time_ms": val_res.validation_details.execution_time_ms,
                    "instructions_preview": lab_res.lab.instructions[:200] + "..." if len(lab_res.lab.instructions) > 200 else lab_res.lab.instructions
                })

        total_elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
        timing_breakdown["total_pipeline_ms"] = total_elapsed_ms

        return FullPipelineResponse(
            success=True,
            transcript_id=transcript_res.id,
            objectives_count=len(objectives),
            objectives=objectives,
            labs_generated_count=len(generated_labs_list),
            validated_labs_count=validated_count,
            labs=generated_labs_list,
            execution_summary={
                "timings": timing_breakdown,
                "status": "completed",
                "deployable": validated_count > 0
            }
        )
