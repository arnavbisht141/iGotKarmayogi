from typing import Optional
from pydantic import BaseModel


class RecommendationSchema(BaseModel):
    id: int
    course_id: Optional[int]
    course_title: Optional[str] = None
    reason: str
    score: float
    status: str
    generated_at: str

    class Config:
        from_attributes = True
