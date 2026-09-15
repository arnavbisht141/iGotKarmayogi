import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import CompetencyDomain, Competency
from app.core.seed_competencies import seed_competency_taxonomy


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


def test_seed_creates_four_domains(db_session):
    seed_competency_taxonomy(db_session)
    domains = db_session.query(CompetencyDomain).all()
    assert len(domains) == 4
    codes = {d.code for d in domains}
    assert codes == {"statistical", "technical", "digital_governance", "behavioural"}


def test_seed_is_idempotent(db_session):
    seed_competency_taxonomy(db_session)
    seed_competency_taxonomy(db_session)
    assert db_session.query(CompetencyDomain).count() == 4


def test_competencies_link_to_domains(db_session):
    seed_competency_taxonomy(db_session)
    python_comp = db_session.query(Competency).filter_by(code="technical_python").first()
    assert python_comp is not None
    assert python_comp.domain.code == "technical"
    assert python_comp.max_level == 5


def test_new_competencies_backfill_on_already_seeded_domain(db_session):
    # Simulates a DB that ran an earlier version of the seed (pre-Phase-2): the
    # behavioural domain and only its original 6 competencies already exist. Re-running
    # the (fixed) seed must add the 2 new Phase 2 competencies without skipping the
    # whole domain, and must not duplicate the pre-existing 6.
    original_behavioural = [
        ("behavioural_leadership", "Leadership"),
        ("behavioural_communication", "Communication"),
        ("behavioural_project_management", "Project Management"),
        ("behavioural_ethics", "Ethics"),
        ("behavioural_decision_making", "Decision Making"),
        ("behavioural_change_management", "Change Management"),
    ]
    domain = CompetencyDomain(code="behavioural", name="Behavioural & Managerial", description="pre-existing")
    db_session.add(domain)
    db_session.flush()
    for code, name in original_behavioural:
        db_session.add(Competency(domain_id=domain.id, code=code, name=name, max_level=5))
    db_session.commit()

    seed_competency_taxonomy(db_session)

    codes = {c.code for c in db_session.query(Competency).filter_by(domain_id=domain.id).all()}
    assert "behavioural_situational_awareness" in codes
    assert "behavioural_accountability" in codes
    assert len(codes) == 8  # 6 original + 2 new, no duplicates
    assert db_session.query(CompetencyDomain).filter_by(code="behavioural").count() == 1
