import json
import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import (
    User, Course, Module, Lesson, Enrollment, Progress
)
from .schemas import ActivityAnswerRequest


router = APIRouter(prefix="/learning", tags=["learning"])

@router.get("/course/{course_id}/player")
def get_course_player(
    course_id: int,
    lesson_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Ensure user is enrolled
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course.id
    ).first()

    if not enrollment:
        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=course.id,
            status="in_progress",
            progress_percent=0.0
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

    # Flatten all lessons for navigation
    all_lessons = []
    modules_tree = []
    completed_lesson_ids = set()

    # Get completed lessons
    progress_records = db.query(Progress).filter(Progress.enrollment_id == enrollment.id).all()
    for p in progress_records:
        if p.completed:
            completed_lesson_ids.add(p.lesson_id)

    for m in course.modules:
        m_lessons = []
        for l in m.lessons:
            is_completed = l.id in completed_lesson_ids
            lesson_meta = {
                "id": l.id,
                "module_id": m.id,
                "title": l.title,
                "content_type": l.content_type,
                "duration_minutes": l.duration_minutes,
                "completed": is_completed,
                "order": l.order
            }
            m_lessons.append(lesson_meta)
            all_lessons.append(lesson_meta)
        
        m_completed = sum(1 for ml in m_lessons if ml["completed"])
        modules_tree.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "order": m.order,
            "lessons": m_lessons,
            "completed_lessons": m_completed,
            "total_lessons": len(m_lessons)
        })

    # Determine target lesson
    target_lesson = None
    if lesson_id:
        target_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    elif enrollment.last_lesson_id:
        target_lesson = db.query(Lesson).filter(Lesson.id == enrollment.last_lesson_id).first()
    
    if not target_lesson and all_lessons:
        target_lesson = db.query(Lesson).filter(Lesson.id == all_lessons[0]["id"]).first()

    if not target_lesson:
        raise HTTPException(status_code=404, detail="No lesson content available in this course")

    # Update last viewed lesson
    enrollment.last_lesson_id = target_lesson.id
    db.commit()

    # Determine prev and next lessons
    prev_lesson_id = None
    next_lesson_id = None
    for idx, l in enumerate(all_lessons):
        if l["id"] == target_lesson.id:
            if idx > 0:
                prev_lesson_id = all_lessons[idx - 1]["id"]
            if idx < len(all_lessons) - 1:
                next_lesson_id = all_lessons[idx + 1]["id"]
            break

    # Parse activity options
    activity_options = []
    if target_lesson.activity_options_json:
        try:
            activity_options = json.loads(target_lesson.activity_options_json)
        except Exception:
            activity_options = []

    # Check if target lesson activity is completed
    target_progress = db.query(Progress).filter(
        Progress.enrollment_id == enrollment.id,
        Progress.lesson_id == target_lesson.id
    ).first()

    total_lessons_count = len(all_lessons)
    overall_progress_pct = round((len(completed_lesson_ids) / max(total_lessons_count, 1)) * 100, 1)

    return {
        "course": {
            "id": course.id,
            "title": course.title,
            "organization": course.organization,
            "progress_percent": overall_progress_pct,
            "assessment_id": course.assessment.id if course.assessment else None
        },
        "modules_tree": modules_tree,
        "current_lesson": {
            "id": target_lesson.id,
            "module_id": target_lesson.module_id,
            "module_title": target_lesson.module.title if target_lesson.module else "",
            "title": target_lesson.title,
            "content_type": target_lesson.content_type,
            "duration_minutes": target_lesson.duration_minutes,
            "content": target_lesson.content,
            "video_url": target_lesson.video_url,
            "completed": target_lesson.id in completed_lesson_ids,
            "activity": {
                "question": target_lesson.activity_question,
                "options": activity_options,
                "has_activity": bool(target_lesson.activity_question),
                "is_completed": target_progress.activity_completed if target_progress else False
            } if target_lesson.activity_question else None,
            "prev_lesson_id": prev_lesson_id,
            "next_lesson_id": next_lesson_id,
            "is_last_lesson": next_lesson_id is None
        }
    }

@router.post("/lesson/{lesson_id}/complete")
def mark_lesson_complete(
    lesson_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    course_id = lesson.module.course_id
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id, status="in_progress")
        db.add(enrollment)
        db.flush()

    progress = db.query(Progress).filter(
        Progress.enrollment_id == enrollment.id,
        Progress.lesson_id == lesson.id
    ).first()

    if not progress:
        progress = Progress(
            enrollment_id=enrollment.id,
            module_id=lesson.module_id,
            lesson_id=lesson.id,
            completed=True
        )
        db.add(progress)
    else:
        progress.completed = True
        progress.updated_at = datetime.datetime.utcnow()

    # Recalculate course percentage
    all_course_lessons = (
        db.query(Lesson)
        .join(Module, Lesson.module_id == Module.id)
        .filter(Module.course_id == course_id)
        .count()
    )
    all_completed = (
        db.query(Progress)
        .filter(Progress.enrollment_id == enrollment.id, Progress.completed == True)
        .count()
    )

    pct = min(100.0, round((all_completed / max(all_course_lessons, 1)) * 100, 1))
    enrollment.progress_percent = pct
    db.commit()

    return {
        "success": True,
        "lesson_id": lesson.id,
        "progress_percent": pct,
        "is_course_finished": pct >= 100.0
    }

@router.post("/lesson/{lesson_id}/activity")
def check_activity_answer(
    lesson_id: int,
    req: ActivityAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson or not lesson.activity_question:
        raise HTTPException(status_code=404, detail="Activity not found for this lesson")

    is_correct = (req.selected_option == lesson.activity_correct_option)

    # Record activity completion if correct
    if is_correct:
        course_id = lesson.module.course_id
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id
        ).first()
        if enrollment:
            prog = db.query(Progress).filter(
                Progress.enrollment_id == enrollment.id,
                Progress.lesson_id == lesson.id
            ).first()
            if prog:
                prog.activity_completed = True
                db.commit()

    return {
        "is_correct": is_correct,
        "correct_option_index": lesson.activity_correct_option,
        "explanation": lesson.activity_explanation or "Correct concept understanding verified."
    }
