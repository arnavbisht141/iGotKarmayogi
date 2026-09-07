from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import (
    User, UserProfile, Enrollment, UserSkill, AssessmentAttempt
)
from .schemas import UpdateProfileRequest


router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/")
def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Completed courses for Certificates
    completed_enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current_user.id, Enrollment.status == "completed")
        .all()
    )

    certificates = []
    for enr in completed_enrollments:
        # Get passing attempt if any
        attempt = (
            db.query(AssessmentAttempt)
            .join(Enrollment, Enrollment.course_id == enr.course_id)
            .filter(AssessmentAttempt.user_id == current_user.id, AssessmentAttempt.passed == True)
            .order_by(AssessmentAttempt.score_percent.desc())
            .first()
        )
        certificates.append({
            "certificate_id": f"KARM-CERT-{enr.course.id}-{current_user.id:04d}",
            "course_id": enr.course.id,
            "course_title": enr.course.title,
            "organization": enr.course.organization,
            "instructor": enr.course.instructor,
            "recipient_name": current_user.full_name,
            "issued_date": enr.completed_at.strftime("%B %d, %Y") if enr.completed_at else "Recently Completed",
            "score_percent": attempt.score_percent if attempt else 100.0,
            "verification_status": "Verified Official Credential",
            "duration_hours": enr.course.duration_hours
        })

    # Acquired skills
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    skills_data = [
        {
            "id": us.skill.id,
            "name": us.skill.name,
            "category": us.skill.category,
            "acquired_date": us.acquired_at.strftime("%B %Y"),
            "source_course": us.source_course.title if us.source_course else "Training Assessment"
        }
        for us in user_skills if us.skill
    ]

    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "profile": {
            "phone": profile.phone or "",
            "bio": profile.bio or "",
            "education": profile.education or "",
            "work_experience_years": profile.work_experience_years or 0,
            "prior_training": profile.prior_training or "",
            "designation": profile.designation or "",
            "department": profile.department or "",
            "job_role": profile.job_role or "",
            "current_assignment": profile.current_assignment or "",
            "areas_of_interest": profile.areas_of_interest.split(",") if profile.areas_of_interest else [],
            "language_pref": profile.language_pref or "en",
            "appearance_pref": profile.appearance_pref or "light",
            "daily_goal_minutes": profile.daily_goal_minutes or 30,
            "current_streak_days": profile.current_streak_days or 1,
            "onboarding_completed": profile.onboarding_completed
        },
        "certificates": certificates,
        "skills": skills_data
    }

@router.put("/")
def update_user_profile(
    req: UpdateProfileRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    if req.full_name is not None:
        current_user.full_name = req.full_name
    if req.phone is not None:
        profile.phone = req.phone
    if req.bio is not None:
        profile.bio = req.bio
    if req.education is not None:
        profile.education = req.education
    if req.work_experience_years is not None:
        profile.work_experience_years = req.work_experience_years
    if req.prior_training is not None:
        profile.prior_training = req.prior_training
    if req.designation is not None:
        profile.designation = req.designation
    if req.department is not None:
        profile.department = req.department
    if req.job_role is not None:
        profile.job_role = req.job_role
    if req.current_assignment is not None:
        profile.current_assignment = req.current_assignment
    if req.areas_of_interest is not None:
        profile.areas_of_interest = ",".join(req.areas_of_interest)
    if req.language_pref is not None:
        profile.language_pref = req.language_pref
    if req.appearance_pref is not None:
        profile.appearance_pref = req.appearance_pref
    if req.daily_goal_minutes is not None:
        profile.daily_goal_minutes = req.daily_goal_minutes

    db.commit()
    return {
        "success": True,
        "message": "Official profile updated successfully."
    }
