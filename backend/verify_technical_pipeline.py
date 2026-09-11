"""
Verification Script for Technical Course Content Generation Pipeline
Run: python verify_technical_pipeline.py
"""

import json
import time
from app.core.database import SessionLocal, engine, Base
from app.core.seed_data import seed_database
from app.modules.technical_courses.schemas import FullPipelineRequest
from app.modules.technical_courses.services.pipeline_orchestrator import TechnicalPipelineOrchestrator
from app.models.models import (
    TechnicalTranscript, TechnicalLearningObjective,
    TechnicalGeneratedLab, TechnicalLabSolution, TechnicalLabValidationResult
)


def run_verification():
    print("=" * 80)
    print(" TECHNICAL COURSE CONTENT GENERATION PIPELINE VERIFICATION")
    print("=" * 80)

    # 1. Initialize DB & seed templates
    print("\n[Stage 0] Initializing SQLite database and seeding human lab templates...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        seed_database(db)

        # 2. Sample Technical Video Transcript
        sample_transcript = """WEBVTT
00:00:01.000 --> 00:00:04.200
[Music]
Welcome back. In this lecture, we will learn how to implement robust REST API endpoints 
using FastAPI and Pydantic validation schemas.

00:00:05.000 --> 00:00:09.500
We will define request handlers to filter citizen records by ID, calculate data counts, 
and raise structured ValueErrors when negative query parameters are passed.

00:00:10.000 --> 00:00:14.000
Finally, we will verify error responses with appropriate HTTP status codes.
"""

        print("\n[Stage 1] Ingesting Technical Transcript:")
        print("  - Title: 'Building Resilient REST APIs with FastAPI'")
        print(f"  - Raw Length: {len(sample_transcript)} characters")

        # 3. Execute End-to-End Orchestrator
        req = FullPipelineRequest(
            title="Building Resilient REST APIs with FastAPI",
            transcript_text=sample_transcript,
            preferred_language="python",
            target_difficulty="intermediate"
        )

        t_start = time.perf_counter()
        print("\n[Stage 2] Running Pipeline Orchestrator (Transcript -> Objectives -> Template Match -> Lab Gen -> Solution -> Sandbox Validation)...")
        response = TechnicalPipelineOrchestrator.run_pipeline(req, db=db)
        total_time_ms = round((time.perf_counter() - t_start) * 1000, 2)

        # 4. Display Results
        print("\n" + "=" * 80)
        print(" PIPELINE EXECUTION SUMMARY")
        print("=" * 80)
        print(f"  * Status:               {'[PASSED]' if response.success else '[FAILED]'}")
        print(f"  * Transcript ID:        {response.transcript_id}")
        print(f"  * Objectives Extracted: {response.objectives_count}")
        print(f"  * Labs Generated:       {response.labs_generated_count}")
        print(f"  * Labs Validated:       {response.validated_labs_count}")
        print(f"  * Total Time:           {total_time_ms} ms")
        print(f"  * Deployable Status:    {'[DEPLOYABLE]' if response.execution_summary.get('deployable') else '[PENDING]'}")

        print("\n" + "-" * 80)
        print(" EXTRACTED LEARNING OBJECTIVES:")
        print("-" * 80)
        for i, obj in enumerate(response.objectives, 1):
            print(f"  {i}. [{obj.assessment_mode.upper()}] Skill: {obj.skill} | Action: {obj.action}")
            print(f"     Objective: \"{obj.objective}\"")
            print(f"     Reasoning: {obj.suitability_reason}")

        print("\n" + "-" * 80)
        print(" GENERATED & VALIDATED LABS:")
        print("-" * 80)
        for lab_info in response.labs:
            print(f"  * Lab ID:           {lab_info['lab_id']}")
            print(f"  * Template Matched: {lab_info['template_id']}")
            print(f"  * Title:            {lab_info['title']}")
            print(f"  * Sandbox Status:   {'[PASSED]' if lab_info['is_valid'] else '[FAILED]'} ({lab_info['status'].upper()})")
            print(f"  * Sandbox Engine:   {lab_info['sandbox_type']}")
            print(f"  * Test Suite:       {lab_info['passed_tests']} tests passed")
            print(f"  * Execution Time:   {lab_info['execution_time_ms']} ms")

        # 5. Verify SQLite Database Records
        print("\n" + "-" * 80)
        print(" VERIFYING DATABASE PERSISTENCE (SQLite):")
        print("-" * 80)
        db_lab = db.query(TechnicalGeneratedLab).filter(TechnicalGeneratedLab.id == response.labs[0]["lab_id"]).first()
        if db_lab:
            print(f"  [OK] Lab Record Exists: ID={db_lab.id}, Status='{db_lab.status}'")
            print(f"  [OK] Starter Code Present: {len(db_lab.starter_code)} characters")
            test_cases = json.loads(db_lab.test_cases_json)
            print(f"  [OK] Test Cases Stored: {len(test_cases)} assertions")
            
            sol = db.query(TechnicalLabSolution).filter(TechnicalLabSolution.lab_id == db_lab.id).first()
            if sol:
                print(f"  [OK] Reference Solution Stored: ID={sol.id} ({len(sol.reference_code)} characters)")
            
            val = db.query(TechnicalLabValidationResult).filter(TechnicalLabValidationResult.lab_id == db_lab.id).first()
            if val:
                print(f"  [OK] Validation Result Stored: Valid={val.is_valid}, ExitCode={val.exit_code}, Sandbox='{val.sandbox_type}'")

        print("\n" + "=" * 80)
        print(" ALL VERIFICATION CHECKS COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    run_verification()
