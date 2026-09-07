"""Request and response contracts for the profile module."""

from typing import List, Optional
from pydantic import BaseModel

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    education: Optional[str] = None
    work_experience_years: Optional[int] = None
    prior_training: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    job_role: Optional[str] = None
    current_assignment: Optional[str] = None
    areas_of_interest: Optional[List[str]] = None
    language_pref: Optional[str] = None
    appearance_pref: Optional[str] = None
    daily_goal_minutes: Optional[int] = None
