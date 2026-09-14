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
