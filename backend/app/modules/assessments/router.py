import json
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import (
    User, Course, Assessment, Question, AssessmentAttempt, Enrollment, UserSkill, CourseSkill
)
from .schemas import SubmitAssessmentRequest


router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.get("/{assessment_id}")
def get_assessment_for_test(
    assessment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    course = assessment.course
    questions_data = []
    for q in assessment.questions:
        try:
            options = json.loads(q.options_json)
        except Exception:
            options = []
        questions_data.append({
            "id": q.id,
            "text": q.text,
            "options": options,
            "order": q.order
        })

    # Check previous attempts
    attempts = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.assessment_id == assessment.id
        )
        .order_by(AssessmentAttempt.submitted_at.desc())
        .all()
    )

    last_attempt = None
    if attempts:
        last_attempt = {
            "id": attempts[0].id,
            "score_percent": attempts[0].score_percent,
            "passed": attempts[0].passed,
            "submitted_at": attempts[0].submitted_at.strftime("%d %b %Y, %I:%M %p")
        }

    return {
        "id": assessment.id,
        "course_id": course.id,
        "course_title": course.title,
        "organization": course.organization,
        "title": assessment.title,
        "description": assessment.description,
        "time_limit_minutes": assessment.time_limit_minutes,
        "pass_threshold_percent": assessment.pass_threshold_percent,
        "total_questions": len(questions_data),
        "questions": questions_data,
        "last_attempt": last_attempt,
        "total_attempts_count": len(attempts)
    }

@router.post("/{assessment_id}/submit")
def submit_assessment(
    assessment_id: int,
    req: SubmitAssessmentRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    total_questions = len(assessment.questions)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="No questions configured for this assessment")

    correct_count = 0
    breakdown = []

    for q in assessment.questions:
        selected_option = req.answers.get(str(q.id))
        is_correct = (selected_option == q.correct_option_index)
        if is_correct:
            correct_count += 1
        
        try:
            opts = json.loads(q.options_json)
        except Exception:
            opts = []

        breakdown.append({
            "question_id": q.id,
            "question_text": q.text,
            "options": opts,
            "selected_option": selected_option,
            "correct_option": q.correct_option_index,
            "is_correct": is_correct,
            "explanation": q.explanation
        })

    score_percent = round((correct_count / total_questions) * 100, 1)
    passed = score_percent >= assessment.pass_threshold_percent

    # Save Attempt
    attempt = AssessmentAttempt(
        user_id=current_user.id,
        assessment_id=assessment.id,
        score_percent=score_percent,
        passed=passed,
        answers_json=json.dumps(req.answers)
    )
    db.add(attempt)

    # If passed, mark course enrollment as completed & award user skills!
    if passed:
        enr = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == assessment.course_id
        ).first()
        if enr:
            enr.status = "completed"
            enr.progress_percent = 100.0
            enr.completed_at = datetime.datetime.utcnow()

        # Award course skills to user
        course_skills = db.query(CourseSkill).filter(CourseSkill.course_id == assessment.course_id).all()
        for cs in course_skills:
            existing_skill = db.query(UserSkill).filter(
                UserSkill.user_id == current_user.id,
                UserSkill.skill_id == cs.skill_id
            ).first()
            if not existing_skill:
                us = UserSkill(
                    user_id=current_user.id,
                    skill_id=cs.skill_id,
                    source_course_id=assessment.course_id
                )
                db.add(us)

    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "score_percent": score_percent,
        "pass_threshold_percent": assessment.pass_threshold_percent,
        "passed": passed,
        "correct_answers": correct_count,
        "total_questions": total_questions,
        "course_id": assessment.course_id,
        "course_title": assessment.course.title,
        "organization": assessment.course.organization,
        "recipient_name": current_user.full_name,
        "breakdown": breakdown
    }
