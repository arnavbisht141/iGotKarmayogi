from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, CompetencyProfile, GapAnalysis
from app.agents.competency.gap_agent import run_gap_analysis
from .schemas import GapAnalysisResponse, CompetencyProfileSchema, DomainGapSchema

router = APIRouter(prefix="/competency", tags=["competency"])


def _serialize_gap(gap: GapAnalysis) -> DomainGapSchema:
    return DomainGapSchema(
        domain_code=gap.domain.code,
        domain_name=gap.domain.name,
        target_level=gap.target_level,
        current_level=gap.current_level,
        gap=gap.gap,
        generated_at=gap.generated_at.isoformat() if gap.generated_at else "",
    )


@router.post("/analyze", response_model=GapAnalysisResponse)
def analyze_competency(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    result = run_gap_analysis(db, current_user.id)
    return GapAnalysisResponse(
        profile=CompetencyProfileSchema(
            statistical_score=result["profile"].statistical_score,
            technical_score=result["profile"].technical_score,
            digital_governance_score=result["profile"].digital_governance_score,
            behavioural_score=result["profile"].behavioural_score,
            last_computed_at=result["profile"].last_computed_at.isoformat() if result["profile"].last_computed_at else None,
        ),
        gaps=[_serialize_gap(g) for g in result["gaps"]],
    )


@router.get("/profile", response_model=CompetencyProfileSchema)
def get_competency_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    profile = db.query(CompetencyProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No competency profile yet. Call POST /competency/analyze first.")
    return CompetencyProfileSchema(
        statistical_score=profile.statistical_score,
        technical_score=profile.technical_score,
        digital_governance_score=profile.digital_governance_score,
        behavioural_score=profile.behavioural_score,
        last_computed_at=profile.last_computed_at.isoformat() if profile.last_computed_at else None,
    )


@router.get("/gaps", response_model=list[DomainGapSchema])
def get_competency_gaps(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # latest gap_analyses row per domain for this user
    all_rows = db.query(GapAnalysis).filter_by(user_id=current_user.id).order_by(GapAnalysis.generated_at.desc()).all()
    latest_by_domain = {}
    for row in all_rows:
        if row.domain_id not in latest_by_domain:
            latest_by_domain[row.domain_id] = row
    if not latest_by_domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No gap analysis yet. Call POST /competency/analyze first.")
    return [_serialize_gap(g) for g in latest_by_domain.values()]
