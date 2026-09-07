import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin
from app.models.models import (
    User, Course, Module, Lesson, Enrollment, Assessment, Question, AssessmentAttempt
)
from .schemas import CourseAssignmentRequest, CreateCourseRequest


router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/overview")
def get_admin_overview(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_enrollments = db.query(Enrollment).count()
    completed_enrollments = db.query(Enrollment).filter(Enrollment.status == "completed").count()
    total_attempts = db.query(AssessmentAttempt).count()
    passed_attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.passed == True).count()

    # User List with their courses and progress
    users = db.query(User).all()
    user_list = []
    for u in users:
        enrs = db.query(Enrollment).filter(Enrollment.user_id == u.id).all()
        user_list.append({
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "designation": u.profile.designation if u.profile else "Not onboarded",
            "department": u.profile.department if u.profile else "N/A",
            "onboarding_completed": u.profile.onboarding_completed if u.profile else False,
            "enrolled_courses_count": len(enrs),
            "completed_courses_count": sum(1 for e in enrs if e.status == "completed"),
            "courses": [
                {
                    "course_id": e.course.id,
                    "title": e.course.title,
                    "status": e.status,
                    "progress_percent": e.progress_percent
                }
                for e in enrs if e.course
            ]
        })

    # Course Analytics
    courses = db.query(Course).all()
    course_analytics = []
    for c in courses:
        enr_count = db.query(Enrollment).filter(Enrollment.course_id == c.id).count()
        comp_count = db.query(Enrollment).filter(Enrollment.course_id == c.id, Enrollment.status == "completed").count()
        
        # Assessment pass rate
        ass_pass_rate = 0.0
        if c.assessment:
            attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.assessment_id == c.assessment.id).all()
            if attempts:
                passed = sum(1 for a in attempts if a.passed)
                ass_pass_rate = round((passed / len(attempts)) * 100, 1)

        course_analytics.append({
            "id": c.id,
            "title": c.title,
            "organization": c.organization,
            "enrolled_count": enr_count,
            "completed_count": comp_count,
            "completion_rate_percent": round((comp_count / max(enr_count, 1)) * 100, 1),
            "assessment_pass_rate": ass_pass_rate,
            "source": c.source
        })

    # Question Difficulty Analysis (identifying where learners struggle)
    questions = db.query(Question).all()
    question_stats = []
    for q in questions:
        attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.assessment_id == q.assessment_id).all()
        if attempts:
            total = len(attempts)
            correct = 0
            for a in attempts:
                try:
                    ans_map = json.loads(a.answers_json)
                    if ans_map.get(str(q.id)) == q.correct_option_index:
                        correct += 1
                except Exception:
                    pass
            accuracy = round((correct / max(total, 1)) * 100, 1)
            question_stats.append({
                "question_id": q.id,
                "assessment_title": q.assessment.title,
                "question_text": q.text[:80] + ("..." if len(q.text) > 80 else ""),
                "accuracy_percent": accuracy,
                "difficulty_tag": "High Error Rate" if accuracy < 50 else ("Moderate" if accuracy < 80 else "Well Understood")
            })

    return {
        "summary": {
            "total_users": total_users,
            "total_courses": total_courses,
            "total_enrollments": total_enrollments,
            "completed_enrollments": completed_enrollments,
            "completion_rate_percent": round((completed_enrollments / max(total_enrollments, 1)) * 100, 1),
            "total_assessment_attempts": total_attempts,
            "overall_pass_rate_percent": round((passed_attempts / max(total_attempts, 1)) * 100, 1)
        },
        "users": user_list,
        "course_analytics": course_analytics,
        "struggling_questions": sorted(question_stats, key=lambda x: x["accuracy_percent"])
    }

@router.post("/assign-course")
def assign_course_to_user(
    req: CourseAssignmentRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == req.user_id).first()
    course = db.query(Course).filter(Course.id == req.course_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(Enrollment).filter(
        Enrollment.user_id == user.id,
        Enrollment.course_id == course.id
    ).first()

    if existing:
        return {
            "success": True,
            "message": f"Official {user.full_name} is already enrolled in {course.title} (Status: {existing.status})."
        }

    enr = Enrollment(
        user_id=user.id,
        course_id=course.id,
        status="in_progress",
        progress_percent=0.0
    )
    course.enrolled_count += 1
    db.add(enr)
    db.commit()

    return {
        "success": True,
        "message": f"Course '{course.title}' officially assigned to {user.full_name} ({user.email})."
    }

@router.post("/courses")
def create_course(
    req: CreateCourseRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    course = Course(
        title=req.title,
        overview=req.overview,
        instructor=req.instructor,
        organization=req.organization,
        duration_hours=req.duration_hours,
        difficulty=req.difficulty,
        category=req.category,
        source=req.source,
        is_new=True
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    return {
        "success": True,
        "message": "Course created successfully",
        "course_id": course.id
    }
