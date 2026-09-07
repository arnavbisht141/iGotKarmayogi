"""Request and response contracts for the onboarding module."""

from typing import List, Optional
from pydantic import BaseModel

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
