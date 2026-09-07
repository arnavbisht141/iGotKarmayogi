"""Request and response contracts for the admin module."""

from pydantic import BaseModel

class CourseAssignmentRequest(BaseModel):
    user_id: int
    course_id: int

class CreateCourseRequest(BaseModel):
    title: str
    overview: str
    instructor: str
    organization: str
    duration_hours: float
    difficulty: str = "intermediate"
    category: str = "General"
    source: str = "internal"
