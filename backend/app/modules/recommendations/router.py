import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, Recommendation, Enrollment
from app.agents.recommendation.agent import generate_recommendations, get_llm_client
from app.agents.recommendation.indexer import get_real_pinecone_index
from .schemas import RecommendationSchema

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

RECOMMENDATION_STATUSES = {"pending", "enrolled", "dismissed"}


class RecommendationStatusUpdate(BaseModel):
    status: str


@router.patch("/{recommendation_id}", response_model=RecommendationSchema)
def update_recommendation_status(
    recommendation_id: int,
    req: RecommendationStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if req.status not in RECOMMENDATION_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {sorted(RECOMMENDATION_STATUSES)}")
    rec = db.query(Recommendation).filter_by(id=recommendation_id, user_id=current_user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    rec.status = req.status
    if req.status == "enrolled" and rec.course_id:
        if not db.query(Enrollment).filter_by(user_id=current_user.id, course_id=rec.course_id).first():
            db.add(Enrollment(user_id=current_user.id, course_id=rec.course_id, status="in_progress"))
    db.commit()
    db.refresh(rec)
    return _serialize(rec)


def _safe_pinecone_index():
    try:
        return get_real_pinecone_index()
    except Exception as e:
        logger.warning("Pinecone index unavailable, falling back to structured-only recommendations: %s", e)
        return None


def _safe_llm_client():
    try:
        return get_llm_client()
    except Exception as e:
        logger.warning("LLM client unavailable, falling back to templated rationale: %s", e)
        return None


@router.post("/generate", response_model=list[RecommendationSchema])
def generate_user_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    recs = generate_recommendations(
        db, current_user.id,
        pinecone_index=_safe_pinecone_index(),
        llm_client=_safe_llm_client(),
    )
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
