from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, Recommendation
from app.agents.recommendation.agent import generate_recommendations
from .schemas import RecommendationSchema

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/generate", response_model=list[RecommendationSchema])
def generate_user_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    recs = generate_recommendations(db, current_user.id)
    return [_serialize(r) for r in recs]


@router.get("", response_model=list[RecommendationSchema])
def list_user_recommendations(
    status_filter: Optional[str] = Query(default=None, alias="status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    query = db.query(Recommendation).filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    return [_serialize(r) for r in query.order_by(Recommendation.generated_at.desc()).all()]


def _serialize(r: Recommendation) -> RecommendationSchema:
    return RecommendationSchema(
        id=r.id, course_id=r.course_id,
        course_title=r.course.title if r.course else None,
        reason=r.reason, score=r.score, status=r.status,
        generated_at=r.generated_at.isoformat() if r.generated_at else "",
    )
