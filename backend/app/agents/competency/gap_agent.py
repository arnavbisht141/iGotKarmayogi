import json
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.models import (
    User, UserProfile, CompetencyDomain, Competency, UserCompetencyScore,
    EvidenceCompetencyMapping, StatEngineMastery, BehaviouralSessionResult,
    GapAnalysis, CompetencyProfile,
)
from app.agents.competency.target_levels import resolve_target_level

DOMAIN_PROFILE_COLUMN = {
    "statistical": "statistical_score",
    "technical": "technical_score",
    "digital_governance": "digital_governance_score",
    "behavioural": "behavioural_score",
}


def _resolve_mapping(db: Session, source_system: str, source_key: str) -> Optional[int]:
    row = db.query(EvidenceCompetencyMapping).filter_by(
        source_system=source_system, source_key=source_key
    ).first()
    return row.competency_id if row else None


def collect_current_levels(db: Session, user_id: int) -> Dict[int, float]:
    """Returns {competency_id: level (0-5)}, merging self-declared scores with
    resolved evidence via max() so evidence never lowers an already-recorded level."""
    levels: Dict[int, float] = {}

    for row in db.query(UserCompetencyScore).filter_by(user_id=user_id).all():
        levels[row.competency_id] = max(levels.get(row.competency_id, 0.0), row.level)

    for row in db.query(StatEngineMastery).filter_by(user_id=str(user_id)).all():
        competency_id = _resolve_mapping(db, "stat_engine_skill", row.skill_id)
        if competency_id is None:
            continue
        mastery = json.loads(row.mastery_json)
        score = mastery.get("score", 0.0)  # 0-100 scale
        level = min(5.0, score / 20.0)
        levels[competency_id] = max(levels.get(competency_id, 0.0), level)

    for row in db.query(BehaviouralSessionResult).filter_by(user_id=user_id).all():
        result = json.loads(row.result_json)
        comp_scores = result.get("competency_scores", {})  # {"Leadership": 78.0, ...}
        for name, score in comp_scores.items():
            competency_id = _resolve_mapping(db, "behavioural_competency", name)
            if competency_id is None:
                continue  # e.g. "Course Knowledge", intentionally unmapped
            level = min(5.0, float(score) / 20.0)
            levels[competency_id] = max(levels.get(competency_id, 0.0), level)

    return levels


def run_gap_analysis(db: Session, user_id: int) -> dict:
    user = db.query(User).filter_by(id=user_id).first()
    profile_row: Optional[UserProfile] = user.profile if user else None
    target_level = resolve_target_level(
        profile_row.designation if profile_row else None,
        profile_row.job_role if profile_row else None,
    )

    current_levels = collect_current_levels(db, user_id)

    domains = db.query(CompetencyDomain).all()
    gaps: List[GapAnalysis] = []
    domain_scores: Dict[str, float] = {}

    for domain in domains:
        competency_ids = [c.id for c in db.query(Competency).filter_by(domain_id=domain.id).all()]
        levels_in_domain = [current_levels[cid] for cid in competency_ids if cid in current_levels]
        current_level = sum(levels_in_domain) / len(levels_in_domain) if levels_in_domain else 0.0

        gap_row = GapAnalysis(
            user_id=user_id, domain_id=domain.id,
            target_level=target_level, current_level=current_level,
            gap=max(0.0, target_level - current_level),
        )
        db.add(gap_row)
        gaps.append(gap_row)
        domain_scores[domain.code] = round((current_level / 5.0) * 100.0, 1)  # 0-100 scale, matches CompetencyProfile's float columns

    db.commit()
    for gap in gaps:
        db.refresh(gap)  # populate gap.domain relationship for callers

    profile = db.query(CompetencyProfile).filter_by(user_id=user_id).first()
    if not profile:
        profile = CompetencyProfile(user_id=user_id)
        db.add(profile)
    for domain_code, column_name in DOMAIN_PROFILE_COLUMN.items():
        setattr(profile, column_name, domain_scores.get(domain_code, 0.0))
    db.commit()
    db.refresh(profile)

    return {"profile": profile, "gaps": gaps}
