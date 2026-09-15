import json
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.models.models import (
    User, UserProfile, Competency, UserCompetencyScore, StatEngineMastery,
    BehaviouralSessionResult, GapAnalysis, CompetencyProfile,
)
from app.agents.competency.gap_agent import run_gap_analysis


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)
    try:
        yield db
    finally:
        db.close()


def _make_user(db, designation="Section Officer"):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.add(UserProfile(user_id=user.id, designation=designation))
    db.commit()
    return user


def test_gap_analysis_creates_one_row_per_domain(db_session):
    user = _make_user(db_session)
    result = run_gap_analysis(db_session, user.id)
    assert len(result["gaps"]) == 4
    domains = {g.domain.code for g in result["gaps"]}
    assert domains == {"statistical", "technical", "digital_governance", "behavioural"}


def test_gap_analysis_uses_target_level_from_designation(db_session):
    user = _make_user(db_session, designation="Section Officer")  # middle tier -> 3.0
    result = run_gap_analysis(db_session, user.id)
    for gap in result["gaps"]:
        assert gap.target_level == 3.0


def test_gap_analysis_merges_self_declared_score(db_session):
    user = _make_user(db_session)
    python_comp = db_session.query(Competency).filter_by(code="technical_python").first()
    db_session.add(UserCompetencyScore(user_id=user.id, competency_id=python_comp.id, level=3.5, evidence_source="self_declared"))
    db_session.commit()

    result = run_gap_analysis(db_session, user.id)
    technical_gap = next(g for g in result["gaps"] if g.domain.code == "technical")
    assert technical_gap.current_level > 0  # the 3.5 self-declared score contributes to the domain average


def test_gap_analysis_resolves_stat_engine_evidence(db_session):
    user = _make_user(db_session)
    db_session.add(StatEngineMastery(
        user_id=str(user.id), skill_id="price.price_relative",
        mastery_json=json.dumps({"score": 80.0, "level": "advanced"}),
    ))
    db_session.commit()

    result = run_gap_analysis(db_session, user.id)
    statistical_gap = next(g for g in result["gaps"] if g.domain.code == "statistical")
    # 80.0 / 20.0 = 4.0 on the 0-5 scale, should dominate the statistical domain average
    assert statistical_gap.current_level > 0


def test_gap_analysis_resolves_behavioural_evidence_via_alias(db_session):
    user = _make_user(db_session)
    db_session.add(BehaviouralSessionResult(
        session_id="cf_sess_test", session_type="carryforward", user_id=user.id,
        score=82.0, result_json=json.dumps({"competency_scores": {"Ethical Judgement": 82.0}}),
    ))
    db_session.commit()

    result = run_gap_analysis(db_session, user.id)
    behavioural_gap = next(g for g in result["gaps"] if g.domain.code == "behavioural")
    assert behavioural_gap.current_level > 0  # "Ethical Judgement" must resolve via the alias to behavioural_ethics


def test_gap_analysis_skips_unmapped_evidence_without_crashing(db_session):
    user = _make_user(db_session)
    db_session.add(StatEngineMastery(
        user_id=str(user.id), skill_id="some.totally.unmapped.skill",
        mastery_json=json.dumps({"score": 50.0}),
    ))
    db_session.commit()
    result = run_gap_analysis(db_session, user.id)  # must not raise
    assert len(result["gaps"]) == 4


def test_gap_analysis_upserts_competency_profile(db_session):
    user = _make_user(db_session)
    run_gap_analysis(db_session, user.id)
    run_gap_analysis(db_session, user.id)  # run twice
    profiles = db_session.query(CompetencyProfile).filter_by(user_id=user.id).all()
    assert len(profiles) == 1  # upsert, not a new row each run


def test_gap_analysis_writes_new_gap_analyses_row_each_run(db_session):
    user = _make_user(db_session)
    run_gap_analysis(db_session, user.id)
    run_gap_analysis(db_session, user.id)
    rows = db_session.query(GapAnalysis).filter_by(user_id=user.id).all()
    assert len(rows) == 8  # 4 domains x 2 runs, gap_analyses is a history table, not upserted
