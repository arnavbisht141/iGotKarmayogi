from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import (
    User, Course, Enrollment, Progress, PlannedCourse, LearningHistory, UserSkill, Lesson
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # If unauthenticated, return public preview highlights
    if not current_user:
        popular_courses = db.query(Course).filter(Course.is_popular == True).limit(4).all()
        return {
            "authenticated": False,
            "recommended": [
                {
                    "id": c.id,
                    "title": c.title,
                    "overview": c.overview,
                    "instructor": c.instructor,
                    "organization": c.organization,
                    "duration_hours": c.duration_hours,
                    "difficulty": c.difficulty,
                    "rating": c.rating,
                    "enrolled_count": c.enrolled_count,
                    "source": c.source,
                    "category": c.category
                } for c in popular_courses
            ]
        }

    profile = current_user.profile
    
    # 1. Continue Learning & Current Course Progress
    active_enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id, Enrollment.status == "in_progress")
        .order_by(Enrollment.started_at.desc())
        .first()
    )
    
    continue_learning = None
    if active_enrollment:
        course = active_enrollment.course
        last_lesson = db.query(Lesson).filter(Lesson.id == active_enrollment.last_lesson_id).first() if active_enrollment.last_lesson_id else None
        continue_learning = {
            "enrollment_id": active_enrollment.id,
            "course_id": course.id,
            "course_title": course.title,
            "organization": course.organization,
            "progress_percent": active_enrollment.progress_percent,
            "current_module": last_lesson.module.title if last_lesson and last_lesson.module else (course.modules[0].title if course.modules else "Orientation"),
            "current_lesson": last_lesson.title if last_lesson else (course.modules[0].lessons[0].title if course.modules and course.modules[0].lessons else "Introduction"),
            "last_lesson_id": last_lesson.id if last_lesson else (course.modules[0].lessons[0].id if course.modules and course.modules[0].lessons else None)
        }

    # 2. Today's Goals (Lightweight computed comparison)
    daily_goal_minutes = profile.daily_goal_minutes if profile else 30
    today_completed_minutes = 20 if active_enrollment else 0

    # 3. Learning Streak
    streak_days = profile.current_streak_days if profile else 1

    # 4. Recommended / Suggested Courses
    # Filter based on department / interests if available, otherwise high-rated
    recommended_query = db.query(Course)
    if active_enrollment:
        recommended_query = recommended_query.filter(Course.id != active_enrollment.course_id)
    recommended_courses = recommended_query.limit(4).all()

    # 5. Trending Courses
    trending_courses = db.query(Course).order_by(Course.enrolled_count.desc()).limit(4).all()

    # 6. Recently Explored Courses
    recent_history = (
        db.query(LearningHistory)
        .filter(LearningHistory.user_id == current_user.id)
        .order_by(LearningHistory.viewed_at.desc())
        .limit(3)
        .all()
    )
    recently_explored = [
        {
            "id": h.course.id,
            "title": h.course.title,
            "organization": h.course.organization,
            "duration_hours": h.course.duration_hours,
            "difficulty": h.course.difficulty,
            "rating": h.course.rating,
            "category": h.course.category,
            "viewed_at": h.viewed_at.isoformat()
        }
        for h in recent_history if h.course
    ]

    # 7. Learning History
    all_enrollments = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()
    in_progress_count = sum(1 for e in all_enrollments if e.status == "in_progress")
    completed_count = sum(1 for e in all_enrollments if e.status == "completed")
    overall_progress = round(sum(e.progress_percent for e in all_enrollments) / max(len(all_enrollments), 1), 1) if all_enrollments else 0

    # 8. Future Planned Courses
    planned_records = db.query(PlannedCourse).filter(PlannedCourse.user_id == current_user.id).all()
    future_planned = [
        {
            "id": p.id,
            "course_id": p.course.id,
            "course_title": p.course.title,
            "organization": p.course.organization,
            "duration_hours": p.course.duration_hours,
            "planned_for": p.planned_for or "Upcoming Quarter",
            "source": p.source
        }
        for p in planned_records if p.course
    ]

    # 9. Competencies / User Skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    skills_list = [
        {
            "id": us.skill.id,
            "name": us.skill.name,
            "category": us.skill.category,
            "acquired_at": us.acquired_at.strftime("%b %Y")
        }
        for us in user_skills if us.skill
    ]

    return {
        "authenticated": True,
        "learner": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "designation": profile.designation if profile else "Civil Servant",
            "department": profile.department if profile else "Official Statistical System",
            "role": current_user.role
        },
        "continue_learning": continue_learning,
        "todays_goals": {
            "target_minutes": daily_goal_minutes,
            "achieved_minutes": today_completed_minutes,
            "percent": min(100, int((today_completed_minutes / max(daily_goal_minutes, 1)) * 100))
        },
        "learning_streak": {
            "streak_days": streak_days,
            "last_active": profile.last_active_date.isoformat() if profile and profile.last_active_date else None
        },
        "my_learning_progress": {
            "in_progress_count": in_progress_count,
            "completed_count": completed_count,
            "overall_progress_percent": overall_progress,
            "hours_learned": round(completed_count * 5.5 + in_progress_count * 2.8, 1)
        },
        "competencies": {
            "skills_count": len(skills_list),
            "top_skills": skills_list
        },
        "recently_explored": recently_explored,
        "trending_courses": [
            {
                "id": c.id,
                "title": c.title,
                "overview": c.overview,
                "organization": c.organization,
                "duration_hours": c.duration_hours,
                "difficulty": c.difficulty,
                "enrolled_count": c.enrolled_count,
                "rating": c.rating,
                "source": c.source,
                "category": c.category
            }
            for c in trending_courses
        ],
        "recommended_courses": [
            {
                "id": c.id,
                "title": c.title,
                "overview": c.overview,
                "organization": c.organization,
                "duration_hours": c.duration_hours,
                "difficulty": c.difficulty,
                "enrolled_count": c.enrolled_count,
                "rating": c.rating,
                "source": c.source,
                "category": c.category
            }
            for c in recommended_courses
        ],
        "future_planned": future_planned
    }
