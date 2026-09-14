"""
iGOT Karmayogi API adapter interface. MockIgotClient is backed entirely by
this project's own courses/enrollments tables. Swap in a real HTTP-backed
implementation later without touching any caller, they only depend on the
IgotClient interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import Course, Enrollment


class IgotClient(ABC):
    @abstractmethod
    def list_courses(self, domain: Optional[str] = None, competency_ids: Optional[List[int]] = None) -> List[Course]:
        ...

    @abstractmethod
    def get_enrollment_status(self, user_id: int, course_id: int) -> Optional[str]:
        ...

    @abstractmethod
    def sync_completion(self, user_id: int, course_id: int) -> None:
        ...


class MockIgotClient(IgotClient):
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self, domain: Optional[str] = None, competency_ids: Optional[List[int]] = None) -> List[Course]:
        # competency_ids is part of the IgotClient interface for a future real API that can
        # filter server-side by competency; the existing Skill/CourseSkill tables have no
        # competency_id link (only UserSkill got that bridge in Phase 1), so there's nothing
        # to join on yet. Task 5's RecommendationAgent does its own domain-based structured
        # filter directly against Course.category, so this parameter is accepted for interface
        # completeness but intentionally not filtered on here.
        query = self.db.query(Course)
        if domain:
            query = query.filter(Course.category == domain)
        return query.all()

    def get_enrollment_status(self, user_id: int, course_id: int) -> Optional[str]:
        enrollment = self.db.query(Enrollment).filter_by(user_id=user_id, course_id=course_id).first()
        return enrollment.status if enrollment else None

    def sync_completion(self, user_id: int, course_id: int) -> None:
        enrollment = self.db.query(Enrollment).filter_by(user_id=user_id, course_id=course_id).first()
        if enrollment:
            enrollment.status = "completed"
            self.db.commit()
