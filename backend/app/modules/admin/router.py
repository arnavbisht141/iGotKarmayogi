import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin
from app.models.models import (
    User, Course, Module, Lesson, Enrollment, Assessment, Question, AssessmentAttempt,
    CompetencyDomain, CompetencyProfile, GapAnalysis, Recommendation, GeneratedQuiz, QuizAttempt,
)
from .schemas import CourseAssignmentRequest, CreateCourseRequest
from app.agents.recommendation.indexer import index_course


router = APIRouter(prefix="/admin", tags=["admin"])

DOMAIN_PROFILE_COLUMN = {
    "statistical": "statistical_score",
    "technical": "technical_score",
    "digital_governance": "digital_governance_score",
    "behavioural": "behavioural_score",
}


@router.get("/competency-analytics")
def get_competency_analytics(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    domains = db.query(CompetencyDomain).order_by(CompetencyDomain.id).all()
    profiles = db.query(CompetencyProfile).all()

    average_scores = []
    for d in domains:
        column = DOMAIN_PROFILE_COLUMN.get(d.code)
        values = [getattr(p, column) or 0.0 for p in profiles] if column else []
        average_scores.append({
            "domain_code": d.code, "domain_name": d.name,
            "average_score": round(sum(values) / len(values), 1) if values else 0.0,
        })

    latest_gap = {}
    for row in db.query(GapAnalysis).order_by(GapAnalysis.generated_at.desc()).all():
        latest_gap.setdefault((row.user_id, row.domain_id), row)
    gap_distribution = []
    for d in domains:
        rows = [r for (_, domain_id), r in latest_gap.items() if domain_id == d.id]
        gap_distribution.append({
            "domain_code": d.code, "domain_name": d.name,
            "on_target": sum(1 for r in rows if r.gap <= 0),
            "minor_gap": sum(1 for r in rows if 0 < r.gap <= 1),
            "major_gap": sum(1 for r in rows if r.gap > 1),
        })

    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    by_day = {}
    for row in db.query(GapAnalysis).filter(GapAnalysis.generated_at >= cutoff).all():
        by_day.setdefault(row.generated_at.date().isoformat(), {}).setdefault(row.domain.code, []).append(row.gap)
    gap_trend = [
        {"date": day, **{code: round(sum(v) / len(v), 2) for code, v in gaps.items()}}
        for day, gaps in sorted(by_day.items())
    ]

    # ponytail: half-over-half linear extrapolation, swap for a real forecasting model once there is months of history
    projections = []
    for d in domains:
        series = [point[d.code] for point in gap_trend if d.code in point]
        current = series[-1] if series else None
        projected = current
        if len(series) >= 2:
            mid = len(series) // 2
            first = sum(series[:mid]) / mid
            second = sum(series[mid:]) / (len(series) - mid)
            projected = max(0.0, round(second + (second - first), 2))
        projections.append({"domain_code": d.code, "domain_name": d.name, "current_gap": current, "projected_gap_30d": projected})

    quiz_attempts = db.query(QuizAttempt).all()
    assessment_attempts = db.query(AssessmentAttempt).all()
    enrollments = db.query(Enrollment).all()
    training_effectiveness = {
        "quizzes_generated": db.query(GeneratedQuiz).count(),
        "quiz_attempts": len(quiz_attempts),
        "average_quiz_score": round(sum(a.score_percent for a in quiz_attempts) / len(quiz_attempts), 1) if quiz_attempts else None,
        "assessment_attempts": len(assessment_attempts),
        "assessment_pass_rate": round(100.0 * sum(1 for a in assessment_attempts if a.passed) / len(assessment_attempts), 1) if assessment_attempts else None,
        "enrollments_completed": sum(1 for e in enrollments if e.status == "completed"),
        "enrollments_in_progress": sum(1 for e in enrollments if e.status != "completed"),
    }

    demand = (
        db.query(Recommendation.course_id, func.count(Recommendation.id))
        .filter(Recommendation.course_id.isnot(None))
        .group_by(Recommendation.course_id)
        .order_by(func.count(Recommendation.id).desc())
        .limit(5)
        .all()
    )
    titles = {c.id: c.title for c in db.query(Course).filter(Course.id.in_([cid for cid, _ in demand])).all()} if demand else {}

    return {
        "profiled_learners": len(profiles),
        "average_scores": average_scores,
        "gap_distribution": gap_distribution,
        "gap_trend": gap_trend,
        "projections": projections,
        "training_effectiveness": training_effectiveness,
        "top_recommended_courses": [{"course_id": cid, "title": titles.get(cid, ""), "recommended_to": count} for cid, count in demand],
    }

@router.get("/overview")
def get_admin_overview(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    from collections import defaultdict
    from app.models.models import UserProfile

    # Load each table once and group in Python: per-row queries cost a network round trip each on hosted Postgres.
    users = db.query(User).all()
    courses = db.query(Course).all()
    enrollments = db.query(Enrollment).all()
    all_attempts = db.query(AssessmentAttempt).all()
    questions = db.query(Question).all()
    profiles = {p.user_id: p for p in db.query(UserProfile).all()}
    assessment_by_course = {a.course_id: a for a in db.query(Assessment).all()}
    assessment_titles = {a.id: a.title for a in assessment_by_course.values()}
    course_by_id = {c.id: c for c in courses}

    enrollments_by_user = defaultdict(list)
    enrollments_by_course = defaultdict(list)
    for e in enrollments:
        enrollments_by_user[e.user_id].append(e)
        enrollments_by_course[e.course_id].append(e)
    attempts_by_assessment = defaultdict(list)
    for a in all_attempts:
        attempts_by_assessment[a.assessment_id].append(a)

    total_users = len(users)
    total_courses = len(courses)
    total_enrollments = len(enrollments)
    completed_enrollments = sum(1 for e in enrollments if e.status == "completed")
    total_attempts = len(all_attempts)
    passed_attempts = sum(1 for a in all_attempts if a.passed)

    # User List with their courses and progress
    user_list = []
    for u in users:
        enrs = enrollments_by_user[u.id]
        profile = profiles.get(u.id)
        user_list.append({
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "designation": profile.designation if profile else "Not onboarded",
            "department": profile.department if profile else "N/A",
            "onboarding_completed": profile.onboarding_completed if profile else False,
            "enrolled_courses_count": len(enrs),
            "completed_courses_count": sum(1 for e in enrs if e.status == "completed"),
            "courses": [
                {
                    "course_id": e.course_id,
                    "title": course_by_id[e.course_id].title,
                    "status": e.status,
                    "progress_percent": e.progress_percent
                }
                for e in enrs if e.course_id in course_by_id
            ]
        })

    # Course Analytics
    course_analytics = []
    for c in courses:
        course_enrollments = enrollments_by_course[c.id]
        enr_count = len(course_enrollments)
        comp_count = sum(1 for e in course_enrollments if e.status == "completed")

        # Assessment pass rate
        ass_pass_rate = 0.0
        assessment = assessment_by_course.get(c.id)
        if assessment:
            attempts = attempts_by_assessment[assessment.id]
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
    question_stats = []
    for q in questions:
        attempts = attempts_by_assessment[q.assessment_id]
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
                "assessment_title": assessment_titles.get(q.assessment_id, ""),
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

@router.post("/courses/{course_id}/reindex")
def reindex_course(
    course_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    try:
        index_course(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail="Vector index service unavailable") from e

    return {
        "success": True,
        "status": "indexed",
        "course_id": course_id
    }
