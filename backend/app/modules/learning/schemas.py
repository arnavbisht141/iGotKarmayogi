"""Request and response contracts for the learning module."""

from pydantic import BaseModel

class ActivityAnswerRequest(BaseModel):
    selected_option: int
