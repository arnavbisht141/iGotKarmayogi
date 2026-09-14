import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import EvidenceCompetencyMapping, Competency
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping


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
    try:
        yield db
    finally:
        db.close()


def _seed(db):
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)


def test_new_behavioural_competencies_seeded(db_session):
    _seed(db_session)
    codes = {c.code for c in db_session.query(Competency).filter_by(domain_id=db_session.query(Competency).filter_by(code="behavioural_leadership").first().domain_id)}
    assert "behavioural_situational_awareness" in codes
    assert "behavioural_accountability" in codes


def test_stat_engine_skill_mappings_resolve_to_price_statistics(db_session):
    _seed(db_session)
    price_comp = db_session.query(Competency).filter_by(code="statistical_price_statistics").first()
    for skill_id in [
        "price.price_relative", "price.cpi.weighted_price_relatives", "price.fisher_index",
        "price.inflation_rate", "price.laspeyres_index", "price.real_vs_nominal",
    ]:
        row = db_session.query(EvidenceCompetencyMapping).filter_by(
            source_system="stat_engine_skill", source_key=skill_id
        ).first()
        assert row is not None, f"missing mapping for {skill_id}"
        assert row.competency_id == price_comp.id


def test_stat_engine_competency_mapping(db_session):
    _seed(db_session)
    price_comp = db_session.query(Competency).filter_by(code="statistical_price_statistics").first()
    row = db_session.query(EvidenceCompetencyMapping).filter_by(
        source_system="stat_engine_competency", source_key="price_statistics"
    ).first()
    assert row.competency_id == price_comp.id


def test_behavioural_competency_mappings_including_aliases(db_session):
    _seed(db_session)
    ethics_comp = db_session.query(Competency).filter_by(code="behavioural_ethics").first()
    situational_comp = db_session.query(Competency).filter_by(code="behavioural_situational_awareness").first()

    ethics_row = db_session.query(EvidenceCompetencyMapping).filter_by(
        source_system="behavioural_competency", source_key="Ethics"
    ).first()
    assert ethics_row.competency_id == ethics_comp.id

    alias_row = db_session.query(EvidenceCompetencyMapping).filter_by(
        source_system="behavioural_competency", source_key="Ethical Judgement"
    ).first()
    assert alias_row.competency_id == ethics_comp.id, "Ethical Judgement (carryforward) must alias to behavioural_ethics"

    situational_row = db_session.query(EvidenceCompetencyMapping).filter_by(
        source_system="behavioural_competency", source_key="Situational Awareness"
    ).first()
    assert situational_row.competency_id == situational_comp.id


def test_course_knowledge_has_no_mapping(db_session):
    _seed(db_session)
    row = db_session.query(EvidenceCompetencyMapping).filter_by(
        source_system="behavioural_competency", source_key="Course Knowledge"
    ).first()
    assert row is None, "Course Knowledge is not a taxonomy competency, must stay unmapped"


def test_seed_evidence_mapping_is_idempotent(db_session):
    _seed(db_session)
    seed_evidence_mapping(db_session)
    count = db_session.query(EvidenceCompetencyMapping).count()
    seed_evidence_mapping(db_session)
    assert db_session.query(EvidenceCompetencyMapping).count() == count
