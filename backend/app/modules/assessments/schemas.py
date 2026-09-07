"""Request and response contracts for the assessments module."""

from typing import Dict
from pydantic import BaseModel

class SubmitAssessmentRequest(BaseModel):
    # Mapping of question_id (str or int) to chosen option index (int)
    answers: Dict[str, int]
