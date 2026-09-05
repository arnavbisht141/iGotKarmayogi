import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.models.models import (
    User, Course, Module, Lesson, Enrollment, LearningHistory, CourseSkill
)

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/{course_id}")
def get_course_details(
    course_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Record viewed in learning history if logged in
    if current_user:
        lh = db.query(LearningHistory).filter(
            LearningHistory.user_id == current_user.id,
            LearningHistory.course_id == course.id
        ).first()
        if not lh:
            lh = LearningHistory(user_id=current_user.id, course_id=course.id)
            db.add(lh)
        else:
            lh.viewed_at = datetime.datetime.utcnow()
        db.commit()

    # Calculate content type counts
    video_count = 0
    reading_count = 0
    lab_count = 0
    modules_data = []

    for m in course.modules:
        lessons_data = []
        for l in m.lessons:
            if l.content_type == "video":
                video_count += 1
            elif l.content_type == "lab":
                lab_count += 1
            else:
                reading_count += 1
            
            lessons_data.append({
                "id": l.id,
                "title": l.title,
                "content_type": l.content_type,
                "duration_minutes": l.duration_minutes,
                "has_activity": l.activity_question is not None,
                "order": l.order
            })

        modules_data.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "order": m.order,
            "lessons_count": len(m.lessons),
            "lessons": lessons_data
        })

    # Skills gained
    skills = [cs.skill.name for cs in course.course_skills if cs.skill]

    # Check enrollment status
    enrollment_data = None
    if current_user:
        enr = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course.id
        ).first()
        if enr:
            enrollment_data = {
                "enrollment_id": enr.id,
                "status": enr.status,
                "progress_percent": enr.progress_percent,
                "last_lesson_id": enr.last_lesson_id or (course.modules[0].lessons[0].id if course.modules and course.modules[0].lessons else None)
            }

    return {
        "id": course.id,
        "title": course.title,
        "overview": course.overview,
        "instructor": course.instructor,
        "organization": course.organization,
        "duration_hours": course.duration_hours,
        "difficulty": course.difficulty,
        "source": course.source,
        "category": course.category,
        "rating": course.rating,
        "enrolled_count": course.enrolled_count,
        "counts": {
            "videos": video_count,
            "readings": reading_count,
            "labs": lab_count,
            "assessments": 1 if course.assessment else 0,
            "modules": len(course.modules)
        },
        "skills_gained": skills,
        "modules": modules_data,
        "assessment_id": course.assessment.id if course.assessment else None,
        "enrollment": enrollment_data
    }

@router.post("/{course_id}/enroll")
def enroll_in_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enr = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course.id
    ).first()

    first_lesson_id = None
    if course.modules and course.modules[0].lessons:
        first_lesson_id = course.modules[0].lessons[0].id

    if not enr:
        enr = Enrollment(
            user_id=current_user.id,
            course_id=course.id,
            status="in_progress",
            progress_percent=0.0,
            last_lesson_id=first_lesson_id
        )
        course.enrolled_count += 1
        db.add(enr)
        db.commit()
        db.refresh(enr)

    return {
        "success": True,
        "message": f"Enrolled successfully in {course.title}",
        "enrollment_id": enr.id,
        "status": enr.status,
        "first_lesson_id": enr.last_lesson_id or first_lesson_id
    }
