from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, UserProfile

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

class OnboardingStep1Request(BaseModel):
    # Profile Setup (intro acknowledgement)
    pass

class OnboardingStep2Request(BaseModel):
    # Personal Info
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

class OnboardingStep3Request(BaseModel):
    # Education / Workex / Previous Training
    education: str
    work_experience_years: int
    prior_training: Optional[str] = None

class OnboardingStep4Request(BaseModel):
    # Designation / Department / Job Role
    designation: str
    department: str
    job_role: str

class OnboardingStep5Request(BaseModel):
    # Current Assignment / Areas of Interest
    current_assignment: Optional[str] = None
    areas_of_interest: List[str]

class FullOnboardingSubmission(BaseModel):
    phone: Optional[str] = None
    bio: Optional[str] = None
    education: str
    work_experience_years: int = 0
    prior_training: Optional[str] = None
    designation: str
    department: str
    job_role: str
    current_assignment: Optional[str] = None
    areas_of_interest: List[str] = []
    language_pref: Optional[str] = "en"
    appearance_pref: Optional[str] = "light"

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
