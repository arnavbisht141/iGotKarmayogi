from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, UserProfile
from .schemas import OnboardingStep1Request, OnboardingStep2Request, OnboardingStep3Request, OnboardingStep4Request, OnboardingStep5Request, FullOnboardingSubmission

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

@router.get("/status")
def get_onboarding_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id, onboarding_completed=False)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "onboarding_completed": profile.onboarding_completed,
        "profile": {
            "phone": profile.phone,
            "bio": profile.bio,
            "education": profile.education,
            "work_experience_years": profile.work_experience_years,
            "prior_training": profile.prior_training,
            "designation": profile.designation,
            "department": profile.department,
            "job_role": profile.job_role,
            "current_assignment": profile.current_assignment,
            "areas_of_interest": profile.areas_of_interest.split(",") if profile.areas_of_interest else [],
            "language_pref": profile.language_pref,
            "appearance_pref": profile.appearance_pref
        }
    }

@router.post("/save")
def save_full_onboarding(
    req: FullOnboardingSubmission,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    profile.phone = req.phone
    profile.bio = req.bio
    profile.education = req.education
    profile.work_experience_years = req.work_experience_years
    profile.prior_training = req.prior_training
    profile.designation = req.designation
    profile.department = req.department
    profile.job_role = req.job_role
    profile.current_assignment = req.current_assignment
    profile.areas_of_interest = ",".join(req.areas_of_interest)
    profile.language_pref = req.language_pref or "en"
    profile.appearance_pref = req.appearance_pref or "light"
    profile.onboarding_completed = True

    db.commit()
    return {
        "success": True,
        "message": "Onboarding profile saved successfully. Routing to dashboard.",
        "onboarding_completed": True
    }
