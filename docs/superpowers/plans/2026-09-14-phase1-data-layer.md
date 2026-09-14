# Phase 1: Unified Competency Data Layer — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the platform one real, persistent, cross-domain competency data model in Postgres — replacing the two in-memory subsystems (statistical engine, behavioural sessions) that currently lose all state on restart, and adding the taxonomy/profile/gap/recommendation tables Phase 2's gap-analysis and recommendation agents will read and write.

**Architecture:** Extend the existing SQLAlchemy schema in `backend/app/models/models.py` (do not rewrite it) with new tables for competency taxonomy, per-user competency scores, gap-analysis history, and recommendations. Port the statistical engine's in-memory repositories (`backend/app/statistical_engine/repositories/memory_repositories.py`) to SQLAlchemy-backed equivalents that take an injected `db: Session`, matching the pattern already used by `backend/app/modules/technical_courses`. Persist behavioural session results (carryforward case summaries, interview analyses) to a new table on session completion, attributed to a user via a new optional `user_id` field threaded through the existing session-start requests. Finish by adding a Supabase SQL migration mirroring all the new DDL and cutting `DATABASE_URL` over from SQLite to Postgres.

**Tech Stack:** FastAPI, SQLAlchemy 2.0, Postgres (Supabase), pytest, existing `sqlite:///:memory:` + `StaticPool` test-fixture pattern from `backend/tests/test_technical_pipeline.py`.

**Spec:** `docs/superpowers/specs/2026-09-14-igot-skill-platform-design.md` (Section 3, "Phase 1 — Data layer")

## Global Constraints

- New tables use `Text` columns with a `_json` suffix for structured/JSON data (never native `JSON`/`JSONB` column types) — matches the existing convention (`options_json`, `metadata_json`, `chunks_json`) so the schema stays testable against SQLite in-memory as well as Postgres.
- New SQLAlchemy models go in `backend/app/models/models.py` alongside the existing 26 classes — this file is the single source of truth for schema, per existing project convention; do not create a second models file.
- Every new/changed table gets a matching `CREATE TABLE IF NOT EXISTS` block in a new Supabase migration file under `supabase/migrations/`, following the exact style of `supabase/migrations/20260914000001_technical_course_pipeline.sql`.
- No changes to existing table columns or existing endpoint response shapes — only additive columns/tables, except where a task explicitly says otherwise (Task 4 and Task 5 each make one small, justified signature change to thread through a DB session / user_id — noted in that task).
- Do not touch `ai-service/`, the frontend, or LangGraph/agent code in this phase — that's Phase 2+.

---

### Task 1: Competency taxonomy tables (`competency_domains`, `competencies`)

**Files:**
- Modify: `backend/app/models/models.py` (append at end of file)
- Create: `backend/app/core/seed_competencies.py`
- Modify: `backend/app/main.py` (call the new seed function alongside existing `seed_database()`)
- Test: `backend/tests/test_competency_taxonomy.py`

**Interfaces:**
- Produces: `CompetencyDomain` (`__tablename__ = "competency_domains"`, columns `id`, `code`, `name`, `description`), `Competency` (`__tablename__ = "competencies"`, columns `id`, `domain_id`, `code`, `name`, `description`, `max_level`). Later tasks FK against `competencies.id` and `competency_domains.id`.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_competency_taxonomy.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_competency_taxonomy.py -v`
Expected: FAIL with `ImportError: cannot import name 'CompetencyDomain'` (models don't exist yet)

- [ ] **Step 3: Add the models**

Append to `backend/app/models/models.py`:

```python
class CompetencyDomain(Base):
    __tablename__ = "competency_domains"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)  # statistical, technical, digital_governance, behavioural
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    competencies = relationship("Competency", back_populates="domain", cascade="all, delete-orphan")


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("competency_domains.id", ondelete="CASCADE"), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    max_level = Column(Integer, default=5)

    domain = relationship("CompetencyDomain", back_populates="competencies")
```

- [ ] **Step 4: Write the seed function**

```python
# backend/app/core/seed_competencies.py
from sqlalchemy.orm import Session
from app.models.models import CompetencyDomain, Competency

DOMAINS = [
    ("statistical", "Statistical Competencies", "Survey design, sampling, national accounts, and official statistics methodology."),
    ("technical", "Technical Competencies", "Programming, data tooling, cloud, and AI/ML skills."),
    ("digital_governance", "Digital Governance", "Cybersecurity, data privacy, and government digital infrastructure."),
    ("behavioural", "Behavioural & Managerial", "Leadership, communication, ethics, and decision making."),
]

COMPETENCIES = {
    "statistical": [
        ("statistical_survey_design", "Survey Design"),
        ("statistical_sampling", "Sampling"),
        ("statistical_national_accounts", "National Accounts"),
        ("statistical_price_statistics", "Price Statistics"),
        ("statistical_labour_statistics", "Labour Statistics"),
        ("statistical_agricultural_statistics", "Agricultural Statistics"),
        ("statistical_industrial_statistics", "Industrial Statistics"),
        ("statistical_sdg_indicators", "SDG Indicators"),
        ("statistical_metadata_standards", "Metadata Standards"),
        ("statistical_data_quality", "Data Quality Frameworks"),
    ],
    "technical": [
        ("technical_python", "Python"),
        ("technical_r", "R"),
        ("technical_sql", "SQL"),
        ("technical_stata", "Stata"),
        ("technical_spss", "SPSS"),
        ("technical_sas", "SAS"),
        ("technical_gis", "GIS"),
        ("technical_data_visualization", "Data Visualization"),
        ("technical_ai_ml", "AI/ML"),
        ("technical_cloud_computing", "Cloud Computing"),
        ("technical_apis", "APIs"),
        ("technical_open_data", "Open Data"),
    ],
    "digital_governance": [
        ("digital_governance_cybersecurity", "Cybersecurity"),
        ("digital_governance_data_privacy", "Data Privacy"),
        ("digital_governance_digital_signatures", "Digital Signatures"),
        ("digital_governance_gov_cloud", "Government Cloud"),
        ("digital_governance_dpi", "Digital Public Infrastructure"),
    ],
    "behavioural": [
        ("behavioural_leadership", "Leadership"),
        ("behavioural_communication", "Communication"),
        ("behavioural_project_management", "Project Management"),
        ("behavioural_ethics", "Ethics"),
        ("behavioural_decision_making", "Decision Making"),
        ("behavioural_change_management", "Change Management"),
    ],
}


def seed_competency_taxonomy(db: Session) -> None:
    """Seeds the 4 competency domains and their competencies. Idempotent."""
    for code, name, description in DOMAINS:
        existing = db.query(CompetencyDomain).filter_by(code=code).first()
        if existing:
            continue
        domain = CompetencyDomain(code=code, name=name, description=description)
        db.add(domain)
        db.flush()  # get domain.id without committing
        for comp_code, comp_name in COMPETENCIES[code]:
            db.add(Competency(domain_id=domain.id, code=comp_code, name=comp_name, max_level=5))
    db.commit()
```

- [ ] **Step 5: Wire the seed call into startup**

In `backend/app/main.py`, find the existing `seed_database()` call (used to seed the core LMS data on startup) and add the new seed call immediately after it, using the same `db` session pattern already in that file:

```python
from app.core.seed_competencies import seed_competency_taxonomy
# ... inside the same startup block that already calls seed_database(db):
seed_competency_taxonomy(db)
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/test_competency_taxonomy.py -v`
Expected: 3 passed

- [ ] **Step 7: Run full existing suite to check for regressions**

Run: `cd backend && python -m pytest -v`
Expected: all previously-passing tests still pass (new tables are additive, no existing table touched)

- [ ] **Step 8: Commit**

```bash
git add backend/app/models/models.py backend/app/core/seed_competencies.py backend/app/main.py backend/tests/test_competency_taxonomy.py
git commit -m "feat: add competency taxonomy tables (domains + competencies)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 2: Competency profile & per-competency score tables

**Files:**
- Modify: `backend/app/models/models.py` (append)
- Test: `backend/tests/test_competency_profile.py`

**Interfaces:**
- Consumes: `Competency`, `CompetencyDomain` from Task 1.
- Produces: `CompetencyProfile` (`__tablename__ = "competency_profiles"`: `id`, `user_id` unique FK, `statistical_score`, `technical_score`, `digital_governance_score`, `behavioural_score`, `last_computed_at`), `UserCompetencyScore` (`__tablename__ = "user_competency_scores"`: `id`, `user_id`, `competency_id`, `level` float 0-5, `evidence_source` string, `updated_at`, unique on `(user_id, competency_id)`). Phase 2's gap-analysis agent reads/writes both.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_competency_profile.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

from app.core.database import Base
from app.models.models import User, CompetencyProfile, UserCompetencyScore
from app.core.seed_competencies import seed_competency_taxonomy
from app.models.models import Competency


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


def _make_user(db):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Test Officer")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_competency_profile(db_session):
    user = _make_user(db_session)
    profile = CompetencyProfile(user_id=user.id, statistical_score=42.0)
    db_session.add(profile)
    db_session.commit()
    fetched = db_session.query(CompetencyProfile).filter_by(user_id=user.id).first()
    assert fetched.statistical_score == 42.0
    assert fetched.technical_score == 0.0  # default


def test_one_profile_per_user(db_session):
    user = _make_user(db_session)
    db_session.add(CompetencyProfile(user_id=user.id))
    db_session.commit()
    db_session.add(CompetencyProfile(user_id=user.id))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_user_competency_score_unique_per_competency(db_session):
    seed_competency_taxonomy(db_session)
    user = _make_user(db_session)
    comp = db_session.query(Competency).filter_by(code="technical_python").first()
    db_session.add(UserCompetencyScore(user_id=user.id, competency_id=comp.id, level=3.0, evidence_source="assessment"))
    db_session.commit()
    db_session.add(UserCompetencyScore(user_id=user.id, competency_id=comp.id, level=4.0, evidence_source="assessment"))
    with pytest.raises(IntegrityError):
        db_session.commit()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_competency_profile.py -v`
Expected: FAIL with `ImportError: cannot import name 'CompetencyProfile'`

- [ ] **Step 3: Add the models**

Append to `backend/app/models/models.py`:

```python
class CompetencyProfile(Base):
    __tablename__ = "competency_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    statistical_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    digital_governance_score = Column(Float, default=0.0)
    behavioural_score = Column(Float, default=0.0)
    last_computed_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User")


class UserCompetencyScore(Base):
    __tablename__ = "user_competency_scores"
    __table_args__ = (
        UniqueConstraint("user_id", "competency_id", name="uq_user_competency"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False)
    level = Column(Float, default=0.0)  # 0-5
    evidence_source = Column(String(50), default="self_declared")  # self_declared, assessment, inferred
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User")
    competency = relationship("Competency")
```

Add `UniqueConstraint` to the SQLAlchemy import line at the top of the file (currently `from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey`):

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, UniqueConstraint
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/test_competency_profile.py -v`
Expected: 3 passed

- [ ] **Step 5: Run full suite for regressions**

Run: `cd backend && python -m pytest -v`
Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/models/models.py backend/tests/test_competency_profile.py
git commit -m "feat: add competency_profiles and user_competency_scores tables

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 3: Gap-analysis history & recommendation tables

**Files:**
- Modify: `backend/app/models/models.py` (append)
- Test: `backend/tests/test_gap_and_recommendations.py`

**Interfaces:**
- Consumes: `CompetencyDomain` (Task 1), `Course` (existing model).
- Produces: `GapAnalysis` (`__tablename__ = "gap_analyses"`: `id`, `user_id`, `domain_id`, `target_level`, `current_level`, `gap`, `generated_at`), `Recommendation` (`__tablename__ = "recommendations"`: `id`, `user_id`, `course_id` nullable, `reason`, `score`, `status` default `"pending"`, `generated_at`). Phase 2's `CompetencyGapAgent` writes `GapAnalysis` rows; `RecommendationAgent` writes `Recommendation` rows.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_gap_and_recommendations.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, GapAnalysis, Recommendation, Course
from app.core.seed_competencies import seed_competency_taxonomy
from app.models.models import CompetencyDomain


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


def test_gap_analysis_row(db_session):
    seed_competency_taxonomy(db_session)
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    db_session.add(user)
    db_session.commit()
    domain = db_session.query(CompetencyDomain).filter_by(code="technical").first()

    gap = GapAnalysis(user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=1.5, gap=2.5)
    db_session.add(gap)
    db_session.commit()

    fetched = db_session.query(GapAnalysis).filter_by(user_id=user.id).first()
    assert fetched.gap == 2.5
    assert fetched.domain.code == "technical"


def test_recommendation_defaults_to_pending(db_session):
    user = User(email="c@d.gov.in", password_hash="x", full_name="C")
    course = Course(title="Intro to GIS", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()

    rec = Recommendation(user_id=user.id, course_id=course.id, reason="Closes GIS gap", score=0.87)
    db_session.add(rec)
    db_session.commit()

    fetched = db_session.query(Recommendation).filter_by(user_id=user.id).first()
    assert fetched.status == "pending"
    assert fetched.course.title == "Intro to GIS"


def test_recommendation_without_course(db_session):
    user = User(email="e@f.gov.in", password_hash="x", full_name="E")
    db_session.add(user)
    db_session.commit()
    rec = Recommendation(user_id=user.id, course_id=None, reason="General upskilling", score=0.5)
    db_session.add(rec)
    db_session.commit()
    assert db_session.query(Recommendation).filter_by(user_id=user.id).first().course_id is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_gap_and_recommendations.py -v`
Expected: FAIL with `ImportError: cannot import name 'GapAnalysis'`

- [ ] **Step 3: Add the models**

Append to `backend/app/models/models.py`:

```python
class GapAnalysis(Base):
    __tablename__ = "gap_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    domain_id = Column(Integer, ForeignKey("competency_domains.id", ondelete="CASCADE"), nullable=False)
    target_level = Column(Float, nullable=False)
    current_level = Column(Float, nullable=False)
    gap = Column(Float, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    domain = relationship("CompetencyDomain")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    reason = Column(Text, nullable=False)
    score = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # pending, enrolled, dismissed
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    course = relationship("Course")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/test_gap_and_recommendations.py -v`
Expected: 3 passed

- [ ] **Step 5: Run full suite for regressions**

Run: `cd backend && python -m pytest -v`
Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/models/models.py backend/tests/test_gap_and_recommendations.py
git commit -m "feat: add gap_analyses and recommendations tables

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 4: Persist the statistical engine (questions, attempts, mastery)

This is the biggest task in the phase: it replaces the three in-memory repositories with SQLAlchemy-backed ones, which means threading a `db: Session` through `AssessmentService` and the two router files that call it. This matches the pattern `backend/app/modules/technical_courses` already uses (`db: Session = Depends(get_db)` on each endpoint), so after this task the whole backend is consistent.

**Files:**
- Modify: `backend/app/models/models.py` (append 3 tables)
- Create: `backend/app/statistical_engine/repositories/sql_repositories.py`
- Modify: `backend/app/statistical_engine/questions/generator.py:20-53` (add `to_dict`/`from_dict` to `QuestionInternalRecord`)
- Modify: `backend/app/statistical_engine/services/assessment_service.py` (accept `db: Session` in every public method; drop the module-level repo imports)
- Modify: `backend/app/statistical_engine/api/router.py` (add `db: Session = Depends(get_db)` to each endpoint that calls `assessment_service` or `learner_repo`, pass `db` through)
- Delete: nothing — `backend/app/statistical_engine/repositories/memory_repositories.py` keeps its ABCs (still useful as the interface contract, and the in-memory classes stay as a documented fallback/test double) but its module-level singletons (`question_repo`, `attempt_repo`, `learner_repo`) are no longer imported anywhere after this task.
- Test: `backend/tests/stats_engine/test_sql_repositories.py`
- Modify: `backend/tests/stats_engine/test_api_endpoints.py` and `backend/tests/stats_engine/test_branching_and_mastery.py` (add the `db_session` fixture + override, same pattern as `test_technical_pipeline.py`)

**Interfaces:**
- Consumes: `QuestionInternalRecord` from `backend/app/statistical_engine/questions/generator.py:20`.
- Produces: `SQLQuestionRepository(db)`, `SQLAttemptRepository(db)`, `SQLLearnerRepository(db)` — each implements the same method signatures as `BaseQuestionRepository`/`BaseAttemptRepository`/`BaseLearnerRepository` in `memory_repositories.py`, but takes `db: Session` in `__init__`. `AssessmentService` methods now take `db: Session` as their first parameter after `self`.

- [ ] **Step 1: Write the failing repository test**

```python
# backend/tests/stats_engine/test_sql_repositories.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.statistical_engine.repositories.sql_repositories import (
    SQLQuestionRepository,
    SQLAttemptRepository,
    SQLLearnerRepository,
)
from app.statistical_engine.questions.generator import QuestionInternalRecord
from app.statistical_engine.schemas.questions import QuestionType, QuestionDifficulty


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


def _make_record():
    return QuestionInternalRecord(
        question_id="q-test-1",
        template_id="tmpl-1",
        skill_id="price_statistics_cpi",
        competency_id="price_statistics",
        question_type=QuestionType.MCQ,
        difficulty=QuestionDifficulty.BASIC,
        prompt="What is the CPI base year?",
        parameters={"base_year": 2012},
        correct_answer="A",
        tolerance=0.0,
        options_map={"A": (2012, None), "B": (2010, "wrong_base_year")},
        correct_option_id="A",
        explanation="Base year is 2012=100.",
        unit="index",
        chart=None,
        seed=42,
    )


def test_question_repo_round_trip(db_session):
    repo = SQLQuestionRepository(db_session)
    record = _make_record()
    repo.save_instance(record)

    fetched = repo.get_instance("q-test-1")
    assert fetched is not None
    assert fetched.prompt == "What is the CPI base year?"
    assert fetched.options_map["A"] == (2012, None)
    assert fetched.options_map["B"] == (2010, "wrong_base_year")
    assert fetched.question_type == QuestionType.MCQ
    assert fetched.difficulty == QuestionDifficulty.BASIC
    assert fetched.parameters == {"base_year": 2012}


def test_question_repo_missing_returns_none(db_session):
    repo = SQLQuestionRepository(db_session)
    assert repo.get_instance("does-not-exist") is None


def test_attempt_repo_filters_by_skill(db_session):
    repo = SQLAttemptRepository(db_session)
    repo.record_attempt({"attempt_id": "att-1", "user_id": "u1", "question_id": "q1", "skill_id": "skill_a", "submitted_answer": "A", "is_correct": True, "score": 1.0, "misconception_id": None, "time_taken_seconds": 12, "timestamp": "2026-01-01T00:00:00"})
    repo.record_attempt({"attempt_id": "att-2", "user_id": "u1", "question_id": "q2", "skill_id": "skill_b", "submitted_answer": "B", "is_correct": False, "score": 0.0, "misconception_id": "m1", "time_taken_seconds": 8, "timestamp": "2026-01-01T00:01:00"})

    all_attempts = repo.get_user_attempts("u1")
    assert len(all_attempts) == 2
    skill_a_only = repo.get_user_attempts("u1", skill_id="skill_a")
    assert len(skill_a_only) == 1
    assert skill_a_only[0]["is_correct"] is True


def test_learner_repo_upsert_mastery(db_session):
    repo = SQLLearnerRepository(db_session)
    repo.update_user_skill_mastery("u1", "skill_a", {"score": 0.4, "attempts": 1})
    repo.update_user_skill_mastery("u1", "skill_a", {"score": 0.6, "attempts": 2})

    mastery = repo.get_user_mastery("u1")
    assert mastery["skill_a"]["score"] == 0.6
    assert mastery["skill_a"]["attempts"] == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/stats_engine/test_sql_repositories.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.statistical_engine.repositories.sql_repositories'`

- [ ] **Step 3: Add the three new tables**

Append to `backend/app/models/models.py`:

```python
class StatEngineQuestion(Base):
    __tablename__ = "stat_engine_questions"

    question_id = Column(String(100), primary_key=True)
    template_id = Column(String(100), nullable=False)
    skill_id = Column(String(100), nullable=False, index=True)
    competency_id = Column(String(100), nullable=False)
    question_type = Column(String(50), nullable=False)
    difficulty = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    parameters_json = Column(Text, nullable=False)
    correct_answer_json = Column(Text, nullable=False)
    tolerance = Column(Float, default=0.0)
    options_map_json = Column(Text, nullable=False)
    correct_option_id = Column(String(50), nullable=True)
    explanation = Column(Text, nullable=True)
    unit = Column(String(100), nullable=True)
    chart_json = Column(Text, nullable=True)
    seed = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class StatEngineAttempt(Base):
    __tablename__ = "stat_engine_attempts"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(String(100), nullable=False, index=True)
    question_id = Column(String(100), nullable=False)
    skill_id = Column(String(100), nullable=False, index=True)
    submitted_answer = Column(String(255), nullable=True)
    is_correct = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    misconception_id = Column(String(100), nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class StatEngineMastery(Base):
    __tablename__ = "stat_engine_mastery"
    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_stat_mastery_user_skill"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    skill_id = Column(String(100), nullable=False)
    mastery_json = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
```

- [ ] **Step 4: Add `to_dict`/`from_dict` to `QuestionInternalRecord`**

In `backend/app/statistical_engine/questions/generator.py`, add these two methods to the `QuestionInternalRecord` class (after `__init__`, which ends at line 53):

```python
    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "template_id": self.template_id,
            "skill_id": self.skill_id,
            "competency_id": self.competency_id,
            "question_type": self.question_type.value,
            "difficulty": self.difficulty.value,
            "prompt": self.prompt,
            "parameters": self.parameters,
            "correct_answer": self.correct_answer,
            "tolerance": self.tolerance,
            "options_map": {k: list(v) for k, v in self.options_map.items()},
            "correct_option_id": self.correct_option_id,
            "explanation": self.explanation,
            "unit": self.unit,
            "chart": self.chart.model_dump() if self.chart is not None else None,
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestionInternalRecord":
        from app.statistical_engine.schemas.charts import ChartSpec
        return cls(
            question_id=data["question_id"],
            template_id=data["template_id"],
            skill_id=data["skill_id"],
            competency_id=data["competency_id"],
            question_type=QuestionType(data["question_type"]),
            difficulty=QuestionDifficulty(data["difficulty"]),
            prompt=data["prompt"],
            parameters=data["parameters"],
            correct_answer=data["correct_answer"],
            tolerance=data["tolerance"],
            options_map={k: tuple(v) for k, v in data["options_map"].items()},
            correct_option_id=data.get("correct_option_id"),
            explanation=data.get("explanation", ""),
            unit=data.get("unit", ""),
            chart=ChartSpec(**data["chart"]) if data.get("chart") else None,
            seed=data.get("seed"),
        )
```

- [ ] **Step 5: Write the SQL repositories**

```python
# backend/app/statistical_engine/repositories/sql_repositories.py
import json
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.models import StatEngineQuestion, StatEngineAttempt, StatEngineMastery
from app.statistical_engine.questions.generator import QuestionInternalRecord
from app.statistical_engine.repositories.memory_repositories import (
    BaseQuestionRepository,
    BaseAttemptRepository,
    BaseLearnerRepository,
)


class SQLQuestionRepository(BaseQuestionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_instance(self, record: QuestionInternalRecord) -> None:
        data = record.to_dict()
        row = StatEngineQuestion(
            question_id=data["question_id"],
            template_id=data["template_id"],
            skill_id=data["skill_id"],
            competency_id=data["competency_id"],
            question_type=data["question_type"],
            difficulty=data["difficulty"],
            prompt=data["prompt"],
            parameters_json=json.dumps(data["parameters"]),
            correct_answer_json=json.dumps(data["correct_answer"]),
            tolerance=data["tolerance"],
            options_map_json=json.dumps(data["options_map"]),
            correct_option_id=data["correct_option_id"],
            explanation=data["explanation"],
            unit=data["unit"],
            chart_json=json.dumps(data["chart"]) if data["chart"] is not None else None,
            seed=data["seed"],
        )
        self.db.merge(row)
        self.db.commit()

    def get_instance(self, question_id: str) -> Optional[QuestionInternalRecord]:
        row = self.db.query(StatEngineQuestion).filter_by(question_id=question_id).first()
        if not row:
            return None
        return QuestionInternalRecord.from_dict({
            "question_id": row.question_id,
            "template_id": row.template_id,
            "skill_id": row.skill_id,
            "competency_id": row.competency_id,
            "question_type": row.question_type,
            "difficulty": row.difficulty,
            "prompt": row.prompt,
            "parameters": json.loads(row.parameters_json),
            "correct_answer": json.loads(row.correct_answer_json),
            "tolerance": row.tolerance,
            "options_map": json.loads(row.options_map_json),
            "correct_option_id": row.correct_option_id,
            "explanation": row.explanation,
            "unit": row.unit,
            "chart": json.loads(row.chart_json) if row.chart_json else None,
            "seed": row.seed,
        })


class SQLAttemptRepository(BaseAttemptRepository):
    def __init__(self, db: Session):
        self.db = db

    def record_attempt(self, attempt_data: Dict[str, Any]) -> None:
        row = StatEngineAttempt(
            attempt_id=attempt_data["attempt_id"],
            user_id=str(attempt_data["user_id"]),
            question_id=attempt_data["question_id"],
            skill_id=attempt_data["skill_id"],
            submitted_answer=str(attempt_data.get("submitted_answer", "")),
            is_correct=bool(attempt_data.get("is_correct", False)),
            score=float(attempt_data.get("score", 0.0)),
            misconception_id=attempt_data.get("misconception_id"),
            time_taken_seconds=attempt_data.get("time_taken_seconds"),
        )
        self.db.add(row)
        self.db.commit()

    def get_user_attempts(self, user_id: str, skill_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.db.query(StatEngineAttempt).filter_by(user_id=str(user_id))
        if skill_id is not None:
            query = query.filter_by(skill_id=skill_id)
        rows = query.order_by(StatEngineAttempt.created_at.asc()).all()
        return [
            {
                "attempt_id": r.attempt_id,
                "user_id": r.user_id,
                "question_id": r.question_id,
                "skill_id": r.skill_id,
                "submitted_answer": r.submitted_answer,
                "is_correct": r.is_correct,
                "score": r.score,
                "misconception_id": r.misconception_id,
                "time_taken_seconds": r.time_taken_seconds,
                "timestamp": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]


class SQLLearnerRepository(BaseLearnerRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_mastery(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        rows = self.db.query(StatEngineMastery).filter_by(user_id=str(user_id)).all()
        return {r.skill_id: json.loads(r.mastery_json) for r in rows}

    def update_user_skill_mastery(self, user_id: str, skill_id: str, mastery_data: Dict[str, Any]) -> None:
        row = self.db.query(StatEngineMastery).filter_by(user_id=str(user_id), skill_id=skill_id).first()
        if row:
            row.mastery_json = json.dumps(mastery_data)
        else:
            row = StatEngineMastery(user_id=str(user_id), skill_id=skill_id, mastery_json=json.dumps(mastery_data))
            self.db.add(row)
        self.db.commit()
```

- [ ] **Step 6: Run the repository tests**

Run: `cd backend && python -m pytest tests/stats_engine/test_sql_repositories.py -v`
Expected: 4 passed

- [ ] **Step 7: Thread `db: Session` through `AssessmentService`**

In `backend/app/statistical_engine/services/assessment_service.py`, replace the module-level repo import (lines 11-15) with:

```python
from sqlalchemy.orm import Session
from app.statistical_engine.repositories.sql_repositories import (
    SQLQuestionRepository,
    SQLAttemptRepository,
    SQLLearnerRepository,
)
```

Then update every public method of `AssessmentService` to accept `db: Session` as its first parameter (after `self`) and build the three repos from it at the top of the method body, e.g.:

```python
    def generate_question(
        self,
        db: Session,
        skill_id: str,
        difficulty: Optional[QuestionDifficulty] = None,
        question_type: Optional[QuestionType] = None,
        seed: Optional[int] = None
    ) -> QuestionInstance:
        question_repo = SQLQuestionRepository(db)
        client_instance, internal_record = question_generator.generate_question(
            skill_id=skill_id,
            difficulty=difficulty,
            question_type=question_type,
            seed=seed
        )
        question_repo.save_instance(internal_record)
        return client_instance
```

Apply the same pattern (add `db: Session` param, construct `SQLQuestionRepository(db)` / `SQLAttemptRepository(db)` / `SQLLearnerRepository(db)` locally instead of using the removed module-level `question_repo`/`attempt_repo`/`learner_repo` names) to `get_next_question` and `submit_answer`.

- [ ] **Step 8: Update the router to inject `db` and pass it through**

In `backend/app/statistical_engine/api/router.py`:
- Add `from sqlalchemy.orm import Session` and `from app.core.database import get_db` to the imports.
- Replace `from app.statistical_engine.repositories.memory_repositories import learner_repo` with `from app.statistical_engine.repositories.sql_repositories import SQLLearnerRepository`.
- Add `db: Session = Depends(get_db)` as a parameter to every endpoint function that currently calls `assessment_service.*` or `learner_repo.*`, and pass `db` through (e.g. `assessment_service.generate_question(db, skill_id=..., ...)`); replace `learner_repo.get_user_mastery(user_id)` at line 162 with `SQLLearnerRepository(db).get_user_mastery(user_id)`.

- [ ] **Step 9: Update existing stats_engine tests to use the DB fixture**

In both `backend/tests/stats_engine/test_api_endpoints.py` and `backend/tests/stats_engine/test_branching_and_mastery.py`, add these two fixtures (matching `backend/tests/test_technical_pipeline.py:1-54` exactly) and replace the module-level `client = TestClient(app)` with the `client` fixture in every test function's parameters:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(name="client")
def fixture_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

Every test function that currently calls `client.get(...)` / `client.post(...)` on the module-level `client` must add `client` as a parameter (pytest injects the fixture) instead of relying on the module-level instance — e.g. `def test_generate_question(client):` instead of `def test_generate_question():`.

- [ ] **Step 10: Run the full statistical engine test suite**

Run: `cd backend && python -m pytest tests/stats_engine -v`
Expected: all pass

- [ ] **Step 11: Run full backend suite for regressions**

Run: `cd backend && python -m pytest -v`
Expected: all pass

- [ ] **Step 12: Commit**

```bash
git add backend/app/models/models.py backend/app/statistical_engine backend/tests/stats_engine
git commit -m "feat: persist statistical engine questions/attempts/mastery to Postgres

Replaces the in-memory repositories with SQLAlchemy-backed ones so
adaptive assessment state survives a restart. Threads db: Session
through AssessmentService and the stats-engine router, matching the
pattern already used by the technical_courses module.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 5: Persist behavioural session results (carryforward + interview)

Session *play state* (the in-progress case walkthrough or interview turn-by-turn) stays in memory in `CarryforwardSessionManager`/`InterviewSessionManager` — that's normal, ephemeral UI state, fine to lose on restart, same as any in-progress quiz. What needs to persist is the *final result* (competency scores, decision trail, compliance score) once a session completes, so Phase 2's gap-analysis agent has behavioural evidence to read. Today sessions aren't attributed to a user at all, so this task also adds an optional `user_id` to the two session-start requests.

**Files:**
- Modify: `backend/app/models/models.py` (append 1 table)
- Modify: `backend/app/modules/behavioural_cgp/schemas.py:80-83` (`CarryforwardSessionStartRequest`), `:147-150` (`InterviewStartRequest`) — add `user_id: Optional[int] = None`
- Modify: `backend/app/modules/behavioural_cgp/services/carryforward_session.py` — store `user_id` on `CarryforwardSession`, add a persistence call in `get_summary()`'s caller
- Modify: `backend/app/modules/behavioural_cgp/services/interview_service.py` — same, for the interview session's final analysis
- Create: `backend/app/modules/behavioural_cgp/services/result_store.py`
- Modify: `backend/app/modules/behavioural_cgp/router.py` — thread `req.user_id` into `CarryforwardSessionManager.create_session` (`start_carryforward_session` already has no `db` param and needs none); add `db: Session = Depends(get_db)` to `get_carryforward_session_summary`, `conclude_interview_by_body`, and `conclude_and_analyze_interview` (`start_live_interview` already has `db`); call the new result-store function when a session completes
- Test: `backend/tests/test_behavioural_persistence.py`

**Interfaces:**
- Produces: `BehaviouralSessionResult` (`__tablename__ = "behavioural_session_results"`: `id`, `session_id` unique, `session_type` [`carryforward`/`interview`], `user_id` nullable FK, `case_or_course_id`, `score` float, `result_json` (full summary payload), `completed_at`). `save_behavioural_result(db, *, session_id, session_type, user_id, case_or_course_id, score, result_payload)` in the new `result_store.py` — the single write path both session types call on completion.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_behavioural_persistence.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import BehaviouralSessionResult
from app.modules.behavioural_cgp.services.result_store import save_behavioural_result


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


def test_save_and_read_carryforward_result(db_session):
    save_behavioural_result(
        db_session,
        session_id="cf_sess_abc123",
        session_type="carryforward",
        user_id=None,
        case_or_course_id="case_mospi_nqaf_audit",
        score=82.5,
        result_payload={"procedural_compliance_score": 82.5, "competency_scores": {"Leadership": 78.0}},
    )
    row = db_session.query(BehaviouralSessionResult).filter_by(session_id="cf_sess_abc123").first()
    assert row is not None
    assert row.session_type == "carryforward"
    assert row.score == 82.5
    assert row.user_id is None


def test_save_result_with_user_id(db_session):
    save_behavioural_result(
        db_session,
        session_id="int_sess_xyz789",
        session_type="interview",
        user_id=7,
        case_or_course_id="12",
        score=64.0,
        result_payload={"overall_score": 64.0},
    )
    row = db_session.query(BehaviouralSessionResult).filter_by(session_id="int_sess_xyz789").first()
    assert row.user_id == 7
    assert row.session_type == "interview"


def test_save_is_upsert_on_session_id(db_session):
    save_behavioural_result(db_session, session_id="s1", session_type="carryforward", user_id=None, case_or_course_id="c1", score=50.0, result_payload={})
    save_behavioural_result(db_session, session_id="s1", session_type="carryforward", user_id=None, case_or_course_id="c1", score=90.0, result_payload={})
    rows = db_session.query(BehaviouralSessionResult).filter_by(session_id="s1").all()
    assert len(rows) == 1
    assert rows[0].score == 90.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_behavioural_persistence.py -v`
Expected: FAIL with `ImportError: cannot import name 'BehaviouralSessionResult'`

- [ ] **Step 3: Add the model**

Append to `backend/app/models/models.py`:

```python
class BehaviouralSessionResult(Base):
    __tablename__ = "behavioural_session_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    session_type = Column(String(20), nullable=False)  # carryforward, interview
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    case_or_course_id = Column(String(100), nullable=True)
    score = Column(Float, default=0.0)
    result_json = Column(Text, nullable=False)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User")
```

- [ ] **Step 4: Write the result store**

```python
# backend/app/modules/behavioural_cgp/services/result_store.py
import json
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.models import BehaviouralSessionResult


def save_behavioural_result(
    db: Session,
    *,
    session_id: str,
    session_type: str,
    user_id: Optional[int],
    case_or_course_id: Optional[str],
    score: float,
    result_payload: Dict[str, Any],
) -> None:
    row = db.query(BehaviouralSessionResult).filter_by(session_id=session_id).first()
    if row:
        row.score = score
        row.result_json = json.dumps(result_payload)
        row.user_id = user_id
        row.case_or_course_id = case_or_course_id
    else:
        row = BehaviouralSessionResult(
            session_id=session_id,
            session_type=session_type,
            user_id=user_id,
            case_or_course_id=case_or_course_id,
            score=score,
            result_json=json.dumps(result_payload),
        )
        db.add(row)
    db.commit()
```

- [ ] **Step 5: Run the result-store tests**

Run: `cd backend && python -m pytest tests/test_behavioural_persistence.py -v`
Expected: 3 passed

- [ ] **Step 6: Add `user_id` to the two start-request schemas**

In `backend/app/modules/behavioural_cgp/schemas.py`, change:

```python
class CarryforwardSessionStartRequest(BaseModel):
    case_id: Optional[str] = None
    custom_document_id: Optional[str] = None
```

to:

```python
class CarryforwardSessionStartRequest(BaseModel):
    case_id: Optional[str] = None
    custom_document_id: Optional[str] = None
    user_id: Optional[int] = None
```

and change:

```python
class InterviewStartRequest(BaseModel):
    course_id: int
    officer_name: Optional[str] = "Officer"
    target_duration_minutes: int = Field(default=30, ge=25, le=35)
```

to:

```python
class InterviewStartRequest(BaseModel):
    course_id: int
    officer_name: Optional[str] = "Officer"
    target_duration_minutes: int = Field(default=30, ge=25, le=35)
    user_id: Optional[int] = None
```

- [ ] **Step 7: Store `user_id` on the session objects**

In `backend/app/modules/behavioural_cgp/services/carryforward_session.py`:
- Add `user_id: Optional[int] = None` parameter to `CarryforwardSession.__init__` (line 14) and store it as `self.user_id = user_id`.
- Add `user_id: Optional[int] = None` parameter to `CarryforwardSessionManager.create_session` (line 230) and pass it through to the `CarryforwardSession(...)` constructor call (line 245): `session = CarryforwardSession(session_id=session_id, case_scenarios=scenarios, user_id=user_id)`.

In `backend/app/modules/behavioural_cgp/services/interview_service.py`:
- Add `user_id: Optional[int] = None` parameter to `LiveInterviewSession.__init__` (line 102-109) and store it as `self.user_id = user_id`.
- In `InterviewSessionManager.start_interview` (line 596), the classmethod already takes the whole `req: InterviewStartRequest` object (not individual fields) — pass `user_id=req.user_id` into the `LiveInterviewSession(...)` constructor call at the end of that method (line ~633).

- [ ] **Step 8: Wire persistence + `user_id` into the router**

In `backend/app/modules/behavioural_cgp/router.py`:
- Add `from sqlalchemy.orm import Session`, `from app.core.database import get_db`, `from .services.result_store import save_behavioural_result` to the imports (note: `Session`/`get_db` may already be imported — check before duplicating).
- `start_carryforward_session` (line 127): change `session = CarryforwardSessionManager.create_session(case_id=case_id)` to `session = CarryforwardSessionManager.create_session(case_id=case_id, user_id=req.user_id if req else None)`.
- `get_carryforward_session_summary` (line 184): add `db: Session = Depends(get_db)` as a parameter; after the existing `summary = session.get_summary()` line, call:

```python
    save_behavioural_result(
        db,
        session_id=session.session_id,
        session_type="carryforward",
        user_id=session.user_id,
        case_or_course_id=summary.case_id,
        score=summary.procedural_compliance_score,
        result_payload=summary.model_dump(),
    )
```

before returning `summary`.
- `start_live_interview` (line 193, already has `db: Session = Depends(get_db)` and already calls `InterviewSessionManager.start_interview(req, db=db)`): no change needed here — `user_id` now flows through automatically via `req.user_id` from Step 7.
- `conclude_interview_by_body` (line 237): currently `def conclude_interview_by_body(req: InterviewEndRequest): return conclude_and_analyze_interview(req.session_id)`. Change to accept `db: Session = Depends(get_db)` and pass it through: `def conclude_interview_by_body(req: InterviewEndRequest, db: Session = Depends(get_db)): return conclude_and_analyze_interview(req.session_id, db)`.
- `conclude_and_analyze_interview` (line 243): add `db: Session = Depends(get_db)` as a parameter; after the existing `analysis = session.generate_analysis()` line, call:

```python
    save_behavioural_result(
        db,
        session_id=session.session_id,
        session_type="interview",
        user_id=session.user_id,
        case_or_course_id=str(session.course_id),
        score=analysis.overall_score_percent,
        result_payload=analysis.model_dump(),
    )
```

before returning `analysis`. (`InterviewAnalysisResponse.overall_score_percent` is the exact field name defined in `backend/app/modules/behavioural_cgp/schemas.py:229`.)

- [ ] **Step 9: Run behavioural tests**

Run: `cd backend && python -m pytest tests/test_behavioural_cgp.py tests/test_behavioural_persistence.py -v`
Expected: all pass

- [ ] **Step 10: Run full backend suite for regressions**

Run: `cd backend && python -m pytest -v`
Expected: all pass

- [ ] **Step 11: Commit**

```bash
git add backend/app/models/models.py backend/app/modules/behavioural_cgp backend/tests/test_behavioural_persistence.py
git commit -m "feat: persist behavioural session results with optional user attribution

Carryforward case and live-interview sessions now write their final
scored result to the DB on completion, and accept an optional user_id
so results can later feed the cross-domain gap-analysis agent.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 6: Supabase migration file + cut over to Postgres

**Files:**
- Create: `supabase/migrations/20260914000003_competency_intelligence_layer.sql`
- Modify: `.env` (you provide the real `DATABASE_URL` value; this task documents where it goes)
- Test: full existing backend suite, run twice (once against SQLite as a final regression check, once against the real Supabase Postgres instance)

- [ ] **Step 1: Write the migration file**

Create `supabase/migrations/20260914000003_competency_intelligence_layer.sql`, following the exact style of `supabase/migrations/20260914000001_technical_course_pipeline.sql` (header comment, `CREATE TABLE IF NOT EXISTS public.<table>`, `CREATE INDEX IF NOT EXISTS` after each table). It must contain one `CREATE TABLE` block per table added in Tasks 1-5 (`competency_domains`, `competencies`, `competency_profiles`, `user_competency_scores`, `gap_analyses`, `recommendations`, `stat_engine_questions`, `stat_engine_attempts`, `stat_engine_mastery`, `behavioural_session_results`), with column types and constraints matching the SQLAlchemy models exactly (`Integer`→`SERIAL`/`INTEGER`, `String(n)`→`VARCHAR(n)`, `Text`→`TEXT`, `Float`→`FLOAT`, `Boolean`→`BOOLEAN`, `DateTime`→`TIMESTAMPTZ`), plus indexes matching every `index=True` / `ForeignKey` column and the two `UniqueConstraint`s from Tasks 2 and 4.

- [ ] **Step 2: Get the real Postgres connection string**

Ask the user (if not already supplied) for the Supabase Postgres connection string from the dashboard: Project Settings → Database → Connection string → URI, "Transaction" pooler mode, for project ref `tdcrpjlpvkqjptvsndnp`. Update `DATABASE_URL` in `.env` to that value (format: `postgresql+psycopg2://postgres.<project-ref>:<db-password>@aws-0-<region>.pooler.supabase.com:6543/postgres`).

- [ ] **Step 3: Apply the migration to Supabase**

Run: `cd /Users/amankumar/Desktop/sih && supabase db push` (if the Supabase CLI is linked to the project) — or, if not linked, run the SQL file's contents directly against the Postgres connection string via `psql "$DATABASE_URL" -f supabase/migrations/20260914000003_competency_intelligence_layer.sql`.

Expected: all `CREATE TABLE`/`CREATE INDEX` statements succeed (they're `IF NOT EXISTS`, safe to re-run).

- [ ] **Step 4: Start the backend against Postgres and confirm startup seeding works**

Run: `cd backend && python run.py` (or the project's existing dev-server command — check `backend/README.md` for the exact one) and confirm in the logs that `Base.metadata.create_all`, `seed_database`, and `seed_competency_taxonomy` all run without error against the Postgres connection.

- [ ] **Step 5: Run the full backend test suite against Postgres**

Run: `cd backend && DATABASE_URL="$(grep ^DATABASE_URL ../.env | cut -d= -f2-)" python -m pytest -v`

Expected: all tests pass. (The unit tests added in Tasks 1-5 use their own isolated in-memory SQLite fixture regardless of `DATABASE_URL`, so this run is primarily verifying the app-level `TestClient(app)` tests in `test_behavioural_cgp.py` and the stats-engine API tests that don't override `get_db` still work end-to-end against real Postgres.)

- [ ] **Step 6: Commit**

```bash
git add supabase/migrations/20260914000003_competency_intelligence_layer.sql
git commit -m "feat: add Supabase migration for the competency intelligence layer, cut over to Postgres

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

(`.env` is gitignored — do not commit it; the `DATABASE_URL` change lives only in the local environment.)

---

## Phase 1 Definition of Done

- All 6 tasks committed, full backend test suite green against both the in-memory SQLite test fixtures and real Supabase Postgres.
- Statistical engine and behavioural session results survive a backend restart (manually verify: generate a question, restart `python run.py`, confirm `GET /api/v1/stats-engine/...` for that question ID still resolves).
- `docs/superpowers/specs/2026-09-14-igot-skill-platform-design.md` Phase 2 can now be brainstormed against a real, queryable `user_competency_scores` / `gap_analyses` / `recommendations` schema.
