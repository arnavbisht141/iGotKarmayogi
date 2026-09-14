# Phase 2: Competency Engine, Gap Analysis, Mock iGOT Adapter, Recommendation Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Phase 1 competency data layer actually compute something: a cross-domain gap analysis per user, and ranked, explained course recommendations, via LangGraph-style agents and a mock iGOT adapter.

**Architecture:** Five additive backend changes. (1) A bridge table mapping the free-text skill/competency identifiers used by the statistical engine and behavioural sessions to real `competencies` rows. (2) A `CompetencyGapAgent` that merges self-declared scores with that resolved evidence, compares against a simple designation-tier default framework, and writes `gap_analyses`/`competency_profiles`. (3) A `MockIgotClient` wrapping the existing `courses`/`enrollments` tables behind the interface the real iGOT API will eventually fill. (4) A Pinecone-backed course indexer (Gemini embeddings). (5) A `RecommendationAgent` doing structured-filter-then-vector-rerank-then-LLM-rationale, writing `recommendations`.

**Tech Stack:** FastAPI, SQLAlchemy 2.0, LangGraph/LangChain (existing Groq→OpenAI→Gemini fallback), `langchain-google-genai` (`GoogleGenerativeAIEmbeddings`, `text-embedding-004`), Pinecone (`pinecone` package, serverless index), pytest.

**Spec:** `docs/superpowers/specs/2026-09-15-phase2-competency-engine-design.md`

## Global Constraints

- New tables use `Text` columns with a `_json` suffix for structured data (never native `JSON`/`JSONB`), matching Phase 1's convention.
- New SQLAlchemy models go in `backend/app/models/models.py`, the single source of truth for schema.
- New backend modules follow the existing `backend/app/modules/<name>/{__init__.py, schemas.py, router.py}` layout (see `backend/app/modules/profile/` as the reference), `APIRouter(prefix="/<name>", tags=[...])`, mounted once in `backend/app/main.py` with `prefix=settings.API_V1_STR` (not the triple-mount pattern some older modules use).
- New agent code goes under `backend/app/agents/<name>/`, matching the existing `backend/app/agents/` package.
- Every new endpoint in this phase requires `Depends(get_current_active_user)` (the strict dependency that raises 401 if unauthenticated) except the admin reindex endpoint, which uses `Depends(require_admin)` — both already exist in `backend/app/core/security.py`. There is no anonymous case in this phase, unlike Phase 1's behavioural sessions.
- Every new table gets a matching Supabase migration file under `supabase/migrations/`, following the style of `supabase/migrations/20260914000003_competency_intelligence_layer.sql`.
- Do not touch the frontend, `ai-service/`, or any Phase 1 file outside what's explicitly listed per task.

---

### Task 1: Evidence-to-competency mapping table and seed data

**Files:**
- Modify: `backend/app/models/models.py` (append)
- Modify: `backend/app/core/seed_competencies.py` (extend `COMPETENCIES["behavioural"]`, add a new seed function)
- Modify: `backend/app/main.py` (wire the new seed call)
- Create: `supabase/migrations/20260915000001_phase2_evidence_mapping.sql`
- Test: `backend/tests/test_evidence_mapping.py`

**Interfaces:**
- Produces: `EvidenceCompetencyMapping` (`__tablename__ = "evidence_competency_mapping"`: `id`, `source_system`, `source_key`, `competency_id`, unique on `(source_system, source_key)`), `seed_evidence_mapping(db: Session) -> None` in `backend/app/core/seed_competencies.py`. Task 2's `CompetencyGapAgent` queries this table by `(source_system, source_key)` to resolve evidence rows.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_evidence_mapping.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_evidence_mapping.py -v`
Expected: FAIL with `ImportError: cannot import name 'EvidenceCompetencyMapping'`

- [ ] **Step 3: Add the model**

Append to `backend/app/models/models.py`:

```python
class EvidenceCompetencyMapping(Base):
    __tablename__ = "evidence_competency_mapping"
    __table_args__ = (
        UniqueConstraint("source_system", "source_key", name="uq_evidence_mapping_source"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_system = Column(String(50), nullable=False)  # stat_engine_skill, stat_engine_competency, behavioural_competency
    source_key = Column(String(255), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False)

    competency = relationship("Competency")
```

- [ ] **Step 4: Extend the behavioural competency seed list and add the mapping seed function**

In `backend/app/core/seed_competencies.py`, add two rows to `COMPETENCIES["behavioural"]` (after the existing 6):

```python
    "behavioural": [
        ("behavioural_leadership", "Leadership"),
        ("behavioural_communication", "Communication"),
        ("behavioural_project_management", "Project Management"),
        ("behavioural_ethics", "Ethics"),
        ("behavioural_decision_making", "Decision Making"),
        ("behavioural_change_management", "Change Management"),
        ("behavioural_situational_awareness", "Situational Awareness"),
        ("behavioural_accountability", "Accountability"),
    ],
```

Then append this function and import to the same file:

```python
from app.models.models import CompetencyDomain, Competency, EvidenceCompetencyMapping

STAT_ENGINE_SKILL_TO_COMPETENCY_CODE = {
    "price.price_relative": "statistical_price_statistics",
    "price.cpi.weighted_price_relatives": "statistical_price_statistics",
    "price.fisher_index": "statistical_price_statistics",
    "price.inflation_rate": "statistical_price_statistics",
    "price.laspeyres_index": "statistical_price_statistics",
    "price.real_vs_nominal": "statistical_price_statistics",
}

STAT_ENGINE_COMPETENCY_TO_COMPETENCY_CODE = {
    "price_statistics": "statistical_price_statistics",
}

BEHAVIOURAL_NAME_TO_COMPETENCY_CODE = {
    "Leadership": "behavioural_leadership",
    "Communication": "behavioural_communication",
    "Project Management": "behavioural_project_management",
    "Ethics": "behavioural_ethics",
    "Decision Making": "behavioural_decision_making",
    "Change Management": "behavioural_change_management",
    "Ethical Judgement": "behavioural_ethics",  # carryforward's name for the same dimension interview calls "Ethics"
    "Situational Awareness": "behavioural_situational_awareness",
    "Accountability": "behavioural_accountability",
    # "Course Knowledge" is intentionally absent: it's interview-specific, not a taxonomy competency.
}


def seed_evidence_mapping(db: Session) -> None:
    """Seeds evidence_competency_mapping rows bridging stat_engine/behavioural string
    identifiers to real competencies.id rows. Idempotent. Requires seed_competency_taxonomy
    to have already run (reads Competency rows by code)."""
    def _upsert(source_system: str, source_key: str, competency_code: str) -> None:
        existing = db.query(EvidenceCompetencyMapping).filter_by(
            source_system=source_system, source_key=source_key
        ).first()
        if existing:
            return
        competency = db.query(Competency).filter_by(code=competency_code).first()
        if not competency:
            return  # taxonomy not seeded yet or code typo; skip rather than crash startup
        db.add(EvidenceCompetencyMapping(
            source_system=source_system, source_key=source_key, competency_id=competency.id
        ))

    for skill_id, code in STAT_ENGINE_SKILL_TO_COMPETENCY_CODE.items():
        _upsert("stat_engine_skill", skill_id, code)
    for comp_id, code in STAT_ENGINE_COMPETENCY_TO_COMPETENCY_CODE.items():
        _upsert("stat_engine_competency", comp_id, code)
    for name, code in BEHAVIOURAL_NAME_TO_COMPETENCY_CODE.items():
        _upsert("behavioural_competency", name, code)

    db.commit()
```

(The `EvidenceCompetencyMapping` import goes at the top of the file alongside the existing `CompetencyDomain, Competency` import — merge into one import line rather than duplicating it.)

- [ ] **Step 5: Wire the new seed call into startup**

In `backend/app/main.py`, immediately after the existing `seed_competency_taxonomy(db)` call, add:

```python
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
# ... in the same startup block:
seed_evidence_mapping(db)
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd backend && python -m pytest tests/test_evidence_mapping.py -v`
Expected: 6 passed

- [ ] **Step 7: Write the Supabase migration**

Create `supabase/migrations/20260915000001_phase2_evidence_mapping.sql`, following the style of `supabase/migrations/20260914000003_competency_intelligence_layer.sql`:

```sql
-- Migration: 20260915000001_phase2_evidence_mapping.sql
-- Description: Bridges free-text skill/competency identifiers from the statistical
-- engine and behavioural sessions to the competency taxonomy (Phase 2).

CREATE TABLE IF NOT EXISTS public.evidence_competency_mapping (
    id SERIAL PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    source_key VARCHAR(255) NOT NULL,
    competency_id INTEGER NOT NULL REFERENCES public.competencies(id) ON DELETE CASCADE,
    CONSTRAINT uq_evidence_mapping_source UNIQUE (source_system, source_key)
);

CREATE INDEX IF NOT EXISTS idx_evidence_mapping_competency_id ON public.evidence_competency_mapping(competency_id);
```

(The two new `behavioural_situational_awareness`/`behavioural_accountability` rows and all `evidence_competency_mapping` data rows are seeded by Python at startup, per the existing project convention that `Base.metadata.create_all` + Python seed functions are the actual source of runtime data — this migration only creates the table shape, matching how `competency_domains`/`competencies` rows are seeded in `20260914000003_competency_intelligence_layer.sql`'s sibling migration too.)

- [ ] **Step 8: Run full backend suite for regressions**

Run: `cd backend && python -m pytest tests/ -v --ignore=tests/test_technical_pipeline.py -k "not test_dynamic_case_generation_from_notice and not test_live_interview_session_and_analysis and not test_nqaf_carryforward_and_generated_case_session and not test_generate_course_anchored_case and not test_api_live_interview_flow and not test_live_interview_with_dynamic_database_course"`
Expected: all pass (the `-k` exclusions are the documented pre-existing live-LLM-call hangs from Phase 1's ledger, unrelated to this task)

- [ ] **Step 9: Commit**

```bash
git add backend/app/models/models.py backend/app/core/seed_competencies.py backend/app/main.py supabase/migrations/20260915000001_phase2_evidence_mapping.sql backend/tests/test_evidence_mapping.py
git commit -m "feat: add evidence-to-competency mapping table and seed data"
```

---

### Task 2: Target-level defaults, CompetencyGapAgent, competency endpoints

**Files:**
- Create: `backend/app/agents/competency/__init__.py`
- Create: `backend/app/agents/competency/target_levels.py`
- Create: `backend/app/agents/competency/gap_agent.py`
- Create: `backend/app/modules/competency/__init__.py`
- Create: `backend/app/modules/competency/schemas.py`
- Create: `backend/app/modules/competency/router.py`
- Modify: `backend/app/main.py` (mount the new router)
- Test: `backend/tests/test_target_levels.py`, `backend/tests/test_gap_agent.py`, `backend/tests/test_competency_endpoints.py`

**Interfaces:**
- Consumes: `EvidenceCompetencyMapping` (Task 1), `CompetencyProfile`, `UserCompetencyScore`, `GapAnalysis`, `CompetencyDomain`, `Competency`, `StatEngineMastery`, `BehaviouralSessionResult` (all Phase 1).
- Produces: `resolve_target_level(designation: Optional[str], job_role: Optional[str]) -> float` in `target_levels.py`. `run_gap_analysis(db: Session, user_id: int) -> dict` in `gap_agent.py` — returns `{"profile": CompetencyProfile, "gaps": List[GapAnalysis]}`, the object Task 5's `RecommendationAgent` reads via a fresh `db.query(GapAnalysis)` (not via this return value directly, since it runs in a separate request).

- [ ] **Step 1: Write the failing test for target levels**

```python
# backend/tests/test_target_levels.py
from app.agents.competency.target_levels import resolve_target_level


def test_senior_designation_gets_highest_tier():
    assert resolve_target_level("Joint Director", "Statistical Officer") == 4.0
    assert resolve_target_level("Deputy Secretary", None) == 4.0


def test_middle_designation_gets_middle_tier():
    assert resolve_target_level("Section Officer", None) == 3.0


def test_junior_designation_gets_junior_tier():
    assert resolve_target_level("Junior Statistical Officer", None) == 2.0


def test_unknown_designation_gets_default_tier():
    assert resolve_target_level(None, None) == 2.5
    assert resolve_target_level("Some Unrecognized Title", None) == 2.5


def test_case_insensitive_matching():
    assert resolve_target_level("director", None) == 4.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_target_levels.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement target_levels.py**

```python
# backend/app/agents/competency/target_levels.py
"""
Default designation-tier -> target competency level framework.

This is a DRAFTED DEFAULT, not a validated competency framework. It exists so
gap analysis has something to compare against on day one. It applies the same
target level across all 4 domains for a given tier (no per-domain weighting
yet), keyed by simple keyword matching on the officer's designation/job_role
free text. Replace with a real, validated per-role-per-domain dataset when
one is available; callers only need resolve_target_level() to keep working
with the same signature.
"""
from typing import Optional

TARGET_LEVEL_BY_TIER = {
    "senior": 4.0,
    "middle": 3.0,
    "junior": 2.0,
    "default": 2.5,
}

SENIOR_KEYWORDS = ["director", "secretary", "commissioner", "chief", "head of department"]
MIDDLE_KEYWORDS = ["officer in charge", "section officer", "deputy director", "under secretary", "superintendent"]
JUNIOR_KEYWORDS = ["junior", "assistant", "trainee", "probationer"]


def resolve_target_level(designation: Optional[str], job_role: Optional[str]) -> float:
    text = " ".join(filter(None, [designation, job_role])).lower()
    if not text.strip():
        return TARGET_LEVEL_BY_TIER["default"]

    if any(k in text for k in JUNIOR_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["junior"]
    if any(k in text for k in MIDDLE_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["middle"]
    if any(k in text for k in SENIOR_KEYWORDS):
        return TARGET_LEVEL_BY_TIER["senior"]
    return TARGET_LEVEL_BY_TIER["default"]
```

Note: "Deputy Director" contains both "deputy director" (middle keyword) and would also match if "director" were checked first — check JUNIOR, then MIDDLE, then SENIOR in that order (as written above) so multi-word MIDDLE phrases like "deputy director" win over the bare SENIOR keyword "director" they happen to contain. The test `test_senior_designation_gets_highest_tier` uses "Joint Director" and "Deputy Secretary", neither of which contains a MIDDLE keyword, so both correctly fall through to SENIOR.

- [ ] **Step 4: Run target_levels test**

Run: `cd backend && python -m pytest tests/test_target_levels.py -v`
Expected: 5 passed

- [ ] **Step 5: Write the failing test for the gap agent**

```python
# backend/tests/test_gap_agent.py
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
```

- [ ] **Step 6: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_gap_agent.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 7: Implement the gap agent**

```python
# backend/app/agents/competency/gap_agent.py
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


def _collect_current_levels(db: Session, user_id: int) -> Dict[int, float]:
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

    current_levels = _collect_current_levels(db, user_id)

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
```

- [ ] **Step 8: Run gap agent tests**

Run: `cd backend && python -m pytest tests/test_gap_agent.py -v`
Expected: 8 passed

- [ ] **Step 9: Write the competency module (schemas + router)**

```python
# backend/app/modules/competency/schemas.py
from typing import List, Optional
from pydantic import BaseModel


class DomainGapSchema(BaseModel):
    domain_code: str
    domain_name: str
    target_level: float
    current_level: float
    gap: float
    generated_at: str

    class Config:
        from_attributes = True


class CompetencyProfileSchema(BaseModel):
    statistical_score: float
    technical_score: float
    digital_governance_score: float
    behavioural_score: float
    last_computed_at: Optional[str] = None
    is_default_framework: bool = True

    class Config:
        from_attributes = True


class GapAnalysisResponse(BaseModel):
    profile: CompetencyProfileSchema
    gaps: List[DomainGapSchema]
```

```python
# backend/app/modules/competency/router.py
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
```

```python
# backend/app/modules/competency/__init__.py
```
(empty file, matches the existing modules' convention)

- [ ] **Step 10: Mount the router**

In `backend/app/main.py`, add:

```python
from app.modules.competency.router import router as competency_router
# ... alongside the other single-mount routers:
app.include_router(competency_router, prefix=settings.API_V1_STR)
```

- [ ] **Step 11: Write endpoint tests**

```python
# backend/tests/test_competency_endpoints.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.models.models import User


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
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)
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


@pytest.fixture(name="auth_headers")
def fixture_auth_headers(db_session):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}, user.id


def test_gaps_returns_404_before_analyze(client, auth_headers):
    headers, _ = auth_headers
    resp = client.get("/api/v1/competency/gaps", headers=headers)
    assert resp.status_code == 404


def test_analyze_then_profile_and_gaps(client, auth_headers):
    headers, _ = auth_headers
    analyze_resp = client.post("/api/v1/competency/analyze", headers=headers)
    assert analyze_resp.status_code == 200
    assert len(analyze_resp.json()["gaps"]) == 4

    profile_resp = client.get("/api/v1/competency/profile", headers=headers)
    assert profile_resp.status_code == 200

    gaps_resp = client.get("/api/v1/competency/gaps", headers=headers)
    assert gaps_resp.status_code == 200
    assert len(gaps_resp.json()) == 4


def test_endpoints_require_auth(client):
    resp = client.get("/api/v1/competency/profile")
    assert resp.status_code == 401
```

- [ ] **Step 12: Run tests**

Run: `cd backend && python -m pytest tests/test_competency_endpoints.py -v`
Expected: 3 passed

- [ ] **Step 13: Run full backend suite for regressions**

Run: `cd backend && python -m pytest tests/ -v --ignore=tests/test_technical_pipeline.py -k "not test_dynamic_case_generation_from_notice and not test_live_interview_session_and_analysis and not test_nqaf_carryforward_and_generated_case_session and not test_generate_course_anchored_case and not test_api_live_interview_flow and not test_live_interview_with_dynamic_database_course"`
Expected: all pass

- [ ] **Step 14: Commit**

```bash
git add backend/app/agents/competency backend/app/modules/competency backend/app/main.py backend/tests/test_target_levels.py backend/tests/test_gap_agent.py backend/tests/test_competency_endpoints.py
git commit -m "feat: add CompetencyGapAgent, target-level defaults, and competency endpoints"
```

---

### Task 3: MockIgotClient

**Files:**
- Create: `backend/app/agents/igot/__init__.py`
- Create: `backend/app/agents/igot/client.py`
- Test: `backend/tests/test_igot_client.py`

**Interfaces:**
- Produces: `IgotClient` (ABC: `list_courses`, `get_enrollment_status`, `sync_completion`), `MockIgotClient(db: Session)` implementing it against `Course`/`Enrollment`. Task 5's `RecommendationAgent` calls `MockIgotClient(db).get_enrollment_status(user_id, course_id)` to exclude completed courses.

- [ ] **Step 1: Write the failing test**

```python
# backend/tests/test_igot_client.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, Course, Enrollment, Skill, CourseSkill
from app.agents.igot.client import MockIgotClient


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


def test_list_courses_filters_by_category(db_session):
    db_session.add_all([
        Course(title="Intro to GIS", overview="x", instructor="x", organization="MoSPI", category="technical"),
        Course(title="Leadership 101", overview="x", instructor="x", organization="ISTM", category="behavioural"),
    ])
    db_session.commit()

    client = MockIgotClient(db_session)
    technical_courses = client.list_courses(domain="technical")
    assert len(technical_courses) == 1
    assert technical_courses[0].title == "Intro to GIS"


def test_get_enrollment_status_none_when_not_enrolled(db_session):
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    course = Course(title="X", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()

    client = MockIgotClient(db_session)
    assert client.get_enrollment_status(user.id, course.id) is None


def test_get_enrollment_status_reflects_enrollment(db_session):
    user = User(email="c@d.gov.in", password_hash="x", full_name="C")
    course = Course(title="Y", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="in_progress"))
    db_session.commit()

    client = MockIgotClient(db_session)
    assert client.get_enrollment_status(user.id, course.id) == "in_progress"


def test_sync_completion_marks_enrollment_completed(db_session):
    user = User(email="e@f.gov.in", password_hash="x", full_name="E")
    course = Course(title="Z", overview="x", instructor="x", organization="MoSPI")
    db_session.add_all([user, course])
    db_session.commit()
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="in_progress"))
    db_session.commit()

    client = MockIgotClient(db_session)
    client.sync_completion(user.id, course.id)

    assert client.get_enrollment_status(user.id, course.id) == "completed"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_igot_client.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement the client**

```python
# backend/app/agents/igot/client.py
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
```

- [ ] **Step 4: Run tests**

Run: `cd backend && python -m pytest tests/test_igot_client.py -v`
Expected: 4 passed

- [ ] **Step 5: Run full backend suite for regressions**

Run: `cd backend && python -m pytest tests/ -v --ignore=tests/test_technical_pipeline.py -k "not test_dynamic_case_generation_from_notice and not test_live_interview_session_and_analysis and not test_nqaf_carryforward_and_generated_case_session and not test_generate_course_anchored_case and not test_api_live_interview_flow and not test_live_interview_with_dynamic_database_course"`
Expected: all pass

- [ ] **Step 6: Commit**

```bash
git add backend/app/agents/igot backend/tests/test_igot_client.py
git commit -m "feat: add MockIgotClient backed by the existing courses and enrollments tables"
```

---

### Task 4: Pinecone course indexer and admin reindex endpoint

**Files:**
- Modify: `backend/requirements.txt` (add `pinecone`)
- Modify: `backend/app/core/config.py` (add `PINECONE_API_KEY`, `PINECONE_INDEX_NAME` settings)
- Create: `backend/app/agents/recommendation/__init__.py`
- Create: `backend/app/agents/recommendation/embeddings.py`
- Create: `backend/app/agents/recommendation/indexer.py`
- Modify: `backend/app/modules/admin/router.py` (add the reindex endpoint)
- Test: `backend/tests/test_course_indexer.py`

**Interfaces:**
- Produces: `get_embedding_client() -> GoogleGenerativeAIEmbeddings` in `embeddings.py` (one shared factory so Task 5 reuses the same client rather than constructing its own). `index_course(db: Session, course_id: int, pinecone_index=None) -> None` in `indexer.py` — `pinecone_index` is an injectable parameter (defaults to the real Pinecone index if not passed) so tests can pass a fake.

- [ ] **Step 1: Add the dependency and settings**

In `backend/requirements.txt`, add a line: `pinecone>=5.0.0`

In `backend/app/core/config.py`, inside the `Settings` class, add (near the other API-key settings):

```python
    # Pinecone vector DB for the recommendation engine's semantic search
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "igot-competency-recommendations")
```

- [ ] **Step 2: Write the embedding client factory**

```python
# backend/app/agents/recommendation/embeddings.py
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIMENSION = 768


def get_embedding_client() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=settings.GOOGLE_API_KEY)


def build_course_embedding_text(course) -> str:
    skill_names = [cs.skill.name for cs in course.course_skills] if course.course_skills else []
    parts = [course.title, course.overview, course.organization, course.category] + skill_names
    return " | ".join(p for p in parts if p)
```

- [ ] **Step 3: Write the failing test for the indexer**

```python
# backend/tests/test_course_indexer.py
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import Course
from app.agents.recommendation.indexer import index_course


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


def test_index_course_upserts_to_pinecone_with_correct_id_and_metadata(db_session, monkeypatch):
    course = Course(title="Intro to Python", overview="Learn Python basics", instructor="x", organization="ISTM", category="technical", difficulty="beginner")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_index = MagicMock()
    fake_embedding_client = MagicMock()
    fake_embedding_client.embed_query.return_value = [0.1] * 768
    monkeypatch.setattr("app.agents.recommendation.indexer.get_embedding_client", lambda: fake_embedding_client)

    index_course(db_session, course.id, pinecone_index=fake_index)

    fake_index.upsert.assert_called_once()
    call_kwargs = fake_index.upsert.call_args
    vectors = call_kwargs.kwargs.get("vectors") or call_kwargs.args[0]
    assert vectors[0][0] == f"course-{course.id}"
    assert vectors[0][1] == [0.1] * 768
    metadata = vectors[0][2]
    assert metadata["course_id"] == course.id
    assert metadata["category"] == "technical"
    assert metadata["title"] == "Intro to Python"


def test_index_course_raises_for_missing_course(db_session):
    with pytest.raises(ValueError):
        index_course(db_session, 99999, pinecone_index=MagicMock())
```

- [ ] **Step 4: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_course_indexer.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 5: Implement the indexer**

```python
# backend/app/agents/recommendation/indexer.py
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Course
from app.agents.recommendation.embeddings import get_embedding_client, build_course_embedding_text

_pinecone_index = None  # lazily constructed real Pinecone index, module-level cache


def _get_real_pinecone_index():
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        _pinecone_index = pc.Index(settings.PINECONE_INDEX_NAME)
    return _pinecone_index


def index_course(db: Session, course_id: int, pinecone_index=None) -> None:
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise ValueError(f"Course {course_id} not found")

    index = pinecone_index if pinecone_index is not None else _get_real_pinecone_index()
    embedding_client = get_embedding_client()
    text = build_course_embedding_text(course)
    vector = embedding_client.embed_query(text)

    index.upsert(vectors=[(
        f"course-{course.id}",
        vector,
        {"course_id": course.id, "category": course.category or "", "difficulty": course.difficulty or "", "title": course.title},
    )])
```

- [ ] **Step 6: Run indexer tests**

Run: `cd backend && python -m pytest tests/test_course_indexer.py -v`
Expected: 2 passed

- [ ] **Step 7: Add the admin reindex endpoint**

Read `backend/app/modules/admin/router.py` first to match its existing import style and endpoint patterns exactly (it already imports `require_admin`). Add:

```python
from app.agents.recommendation.indexer import index_course

@router.post("/courses/{course_id}/reindex")
def reindex_course(
    course_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    try:
        index_course(db, course_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return {"status": "indexed", "course_id": course_id}
```

(Match whatever `User`/`HTTPException`/`status` import names are already used in that file; do not introduce duplicate imports.)

- [ ] **Step 8: Run full backend suite for regressions**

Run: `cd backend && python -m pytest tests/ -v --ignore=tests/test_technical_pipeline.py -k "not test_dynamic_case_generation_from_notice and not test_live_interview_session_and_analysis and not test_nqaf_carryforward_and_generated_case_session and not test_generate_course_anchored_case and not test_api_live_interview_flow and not test_live_interview_with_dynamic_database_course"`
Expected: all pass

- [ ] **Step 9: Commit**

```bash
git add backend/requirements.txt backend/app/core/config.py backend/app/agents/recommendation/__init__.py backend/app/agents/recommendation/embeddings.py backend/app/agents/recommendation/indexer.py backend/app/modules/admin/router.py backend/tests/test_course_indexer.py
git commit -m "feat: add Pinecone course indexer and admin reindex endpoint"
```

---

### Task 5: RecommendationAgent and recommendations endpoints

**Files:**
- Create: `backend/app/agents/recommendation/agent.py`
- Create: `backend/app/modules/recommendations/__init__.py`
- Create: `backend/app/modules/recommendations/schemas.py`
- Create: `backend/app/modules/recommendations/router.py`
- Modify: `backend/app/main.py` (mount the new router)
- Test: `backend/tests/test_recommendation_agent.py`, `backend/tests/test_recommendation_endpoints.py`

**Interfaces:**
- Consumes: `GapAnalysis`, `Course`, `CourseSkill`, `Skill` (existing), `MockIgotClient` (Task 3), `get_embedding_client` (Task 4).
- Produces: `generate_recommendations(db: Session, user_id: int, pinecone_index=None, llm_client=None) -> List[Recommendation]` in `agent.py` — `pinecone_index` and `llm_client` are injectable (same pattern as Task 4's `index_course`) so tests never hit real external services.

- [ ] **Step 1: Write the failing test for the recommendation agent**

```python
# backend/tests/test_recommendation_agent.py
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import User, UserProfile, Course, CompetencyDomain, GapAnalysis, Recommendation
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.agents.recommendation.agent import generate_recommendations


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


def _setup_user_with_gap(db, domain_code="technical", gap=2.0):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db.add(user)
    db.commit()
    db.refresh(user)
    domain = db.query(CompetencyDomain).filter_by(code=domain_code).first()
    db.add(GapAnalysis(user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=4.0 - gap, gap=gap))
    db.commit()
    return user


def test_no_recommendations_when_no_gaps(db_session):
    user = User(email="a@b.gov.in", password_hash="x", full_name="A")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    recs = generate_recommendations(db_session, user.id, pinecone_index=MagicMock(), llm_client=MagicMock())
    assert recs == []


def test_recommends_matching_course_for_domain_gap(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "This course closes your Python gap."

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)

    assert len(recs) == 1
    assert recs[0].course_id == course.id
    assert recs[0].status == "pending"
    persisted = db_session.query(Recommendation).filter_by(user_id=user.id).all()
    assert len(persisted) == 1


def test_excludes_already_completed_courses(db_session):
    from app.models.models import Enrollment
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    db_session.add(Enrollment(user_id=user.id, course_id=course.id, status="completed"))
    db_session.commit()

    fake_pinecone = MagicMock()
    fake_pinecone.query.return_value = {"matches": [{"id": f"course-{course.id}", "score": 0.9, "metadata": {"course_id": course.id}}]}
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)
    assert recs == []


def test_falls_back_to_structured_filter_when_pinecone_unavailable(db_session):
    user = _setup_user_with_gap(db_session, domain_code="technical", gap=2.0)
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical", difficulty="intermediate")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_pinecone = MagicMock()
    fake_pinecone.query.side_effect = Exception("network error")
    fake_llm = MagicMock()
    fake_llm.invoke.return_value.content = "rationale"

    recs = generate_recommendations(db_session, user.id, pinecone_index=fake_pinecone, llm_client=fake_llm)
    # falls back to the structured-filter candidate list (still just the one technical course), doesn't raise
    assert len(recs) == 1
    assert recs[0].course_id == course.id
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd backend && python -m pytest tests/test_recommendation_agent.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement the recommendation agent**

```python
# backend/app/agents/recommendation/agent.py
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import GapAnalysis, Course, Recommendation
from app.agents.igot.client import MockIgotClient
from app.agents.recommendation.embeddings import get_embedding_client

logger = logging.getLogger(__name__)

MAX_RECOMMENDATIONS = 5


def _structured_candidates(db: Session, domain_code: str) -> List[Course]:
    return db.query(Course).filter(Course.category == domain_code).all()


def _vector_rerank(pinecone_index, gap_description: str, candidate_ids: List[int]) -> List[int]:
    """Returns candidate_ids re-ordered by semantic similarity to gap_description.
    Falls back to the original order (unchanged) if Pinecone errors."""
    if not candidate_ids:
        return []
    try:
        embedding_client = get_embedding_client()
        query_vector = embedding_client.embed_query(gap_description)
        result = pinecone_index.query(vector=query_vector, top_k=10, include_metadata=True)
        matched_ids_in_order = [
            m["metadata"]["course_id"] for m in result.get("matches", [])
            if m.get("metadata", {}).get("course_id") in candidate_ids
        ]
        remaining = [cid for cid in candidate_ids if cid not in matched_ids_in_order]
        return matched_ids_in_order + remaining
    except Exception as e:
        logger.warning("Pinecone vector rerank failed, falling back to structured order: %s", e)
        return candidate_ids


def _write_rationale(llm_client, gap_description: str, courses: List[Course]) -> dict:
    """Returns {course_id: rationale_text}. Falls back to a templated rationale
    per course if the LLM call fails."""
    try:
        course_list_text = "\n".join(f"- {c.title} ({c.category}, {c.difficulty}): {c.overview}" for c in courses)
        prompt = (
            f"An official has this skill gap: {gap_description}\n\n"
            f"Candidate courses:\n{course_list_text}\n\n"
            "For each course, write one short paragraph explaining why it helps close this gap. "
            "Format as 'Course Title: rationale text', one per line."
        )
        response = llm_client.invoke(prompt)
        text = response.content
        rationales = {}
        for line in text.split("\n"):
            if ":" not in line:
                continue
            title_part, rationale_part = line.split(":", 1)
            match = next((c for c in courses if c.title.strip() == title_part.strip()), None)
            if match:
                rationales[match.id] = rationale_part.strip()
        for c in courses:
            rationales.setdefault(c.id, f"Recommended to help close your {gap_description} gap.")
        return rationales
    except Exception as e:
        logger.warning("LLM rationale generation failed, using templated fallback: %s", e)
        return {c.id: f"Recommended to help close your {gap_description} gap." for c in courses}


def generate_recommendations(
    db: Session, user_id: int, pinecone_index=None, llm_client=None
) -> List[Recommendation]:
    igot_client = MockIgotClient(db)
    gaps = db.query(GapAnalysis).filter(GapAnalysis.user_id == user_id, GapAnalysis.gap > 0).order_by(GapAnalysis.generated_at.desc()).all()

    seen_domains = set()
    recommendations: List[Recommendation] = []

    for gap in gaps:
        if gap.domain.code in seen_domains:
            continue  # only the most recent gap row per domain
        seen_domains.add(gap.domain.code)

        candidates = _structured_candidates(db, gap.domain.code)
        candidates = [c for c in candidates if igot_client.get_enrollment_status(user_id, c.id) != "completed"]
        if not candidates:
            continue

        gap_description = f"progress from level {gap.current_level:.1f} to {gap.target_level:.1f} in {gap.domain.name}"

        candidate_ids = [c.id for c in candidates]
        if pinecone_index is not None:
            candidate_ids = _vector_rerank(pinecone_index, gap_description, candidate_ids)

        ranked_courses = [c for cid in candidate_ids for c in candidates if c.id == cid][:MAX_RECOMMENDATIONS]
        if not ranked_courses:
            continue

        rationales = _write_rationale(llm_client, gap_description, ranked_courses) if llm_client is not None else {
            c.id: f"Recommended to help close your {gap_description} gap." for c in ranked_courses
        }

        for rank, course in enumerate(ranked_courses):
            rec = Recommendation(
                user_id=user_id, course_id=course.id,
                reason=rationales.get(course.id, ""),
                score=round(1.0 - (rank * 0.1), 2),
            )
            db.add(rec)
            recommendations.append(rec)

    db.commit()
    for rec in recommendations:
        db.refresh(rec)
    return recommendations
```

- [ ] **Step 4: Run agent tests**

Run: `cd backend && python -m pytest tests/test_recommendation_agent.py -v`
Expected: 4 passed

- [ ] **Step 5: Write the recommendations module (schemas + router)**

```python
# backend/app/modules/recommendations/schemas.py
from typing import Optional
from pydantic import BaseModel


class RecommendationSchema(BaseModel):
    id: int
    course_id: Optional[int]
    course_title: Optional[str] = None
    reason: str
    score: float
    status: str
    generated_at: str

    class Config:
        from_attributes = True
```

```python
# backend/app/modules/recommendations/router.py
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
```

```python
# backend/app/modules/recommendations/__init__.py
```
(empty file)

- [ ] **Step 6: Mount the router**

In `backend/app/main.py`, add:

```python
from app.modules.recommendations.router import router as recommendations_router
# ... alongside the competency_router mount:
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
```

- [ ] **Step 7: Write endpoint tests**

```python
# backend/tests/test_recommendation_endpoints.py
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app
from app.core.seed_competencies import seed_competency_taxonomy, seed_evidence_mapping
from app.models.models import User, Course, CompetencyDomain, GapAnalysis


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
    seed_competency_taxonomy(db)
    seed_evidence_mapping(db)
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


def test_generate_and_list_recommendations(client, db_session, monkeypatch):
    user = User(email="officer@example.gov.in", password_hash="x", full_name="Officer")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    domain = db_session.query(CompetencyDomain).filter_by(code="technical").first()
    db_session.add(GapAnalysis(user_id=user.id, domain_id=domain.id, target_level=4.0, current_level=2.0, gap=2.0))
    course = Course(title="Intro to Python", overview="x", instructor="x", organization="ISTM", category="technical")
    db_session.add(course)
    db_session.commit()

    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    generate_resp = client.post("/api/v1/recommendations/generate", headers=headers)
    assert generate_resp.status_code == 200
    assert len(generate_resp.json()) == 1

    list_resp = client.get("/api/v1/recommendations", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["status"] == "pending"


def test_recommendations_require_auth(client):
    resp = client.get("/api/v1/recommendations")
    assert resp.status_code == 401
```

- [ ] **Step 8: Run tests**

Run: `cd backend && python -m pytest tests/test_recommendation_endpoints.py -v`
Expected: 2 passed

Note: `generate_recommendations` is called here with no `pinecone_index`/`llm_client` args (both default to `None` in the router, since Task 5's `generate_recommendations` signature defaults both to `None`) — verify the agent code handles `pinecone_index=None` by skipping the vector-rerank step entirely (falls through to the structured-filter order) rather than erroring, since this endpoint test has no real Pinecone/LLM credentials available. If the Step 3 implementation doesn't already handle `pinecone_index=None` gracefully, fix it now: `_vector_rerank` should only be called when `pinecone_index is not None` (already written that way above), and `_write_rationale` needs `llm_client is not None` checked the same way (already handled in the `generate_recommendations` body above).

- [ ] **Step 9: Run full backend suite for regressions**

Run: `cd backend && python -m pytest tests/ -v --ignore=tests/test_technical_pipeline.py -k "not test_dynamic_case_generation_from_notice and not test_live_interview_session_and_analysis and not test_nqaf_carryforward_and_generated_case_session and not test_generate_course_anchored_case and not test_api_live_interview_flow and not test_live_interview_with_dynamic_database_course"`
Expected: all pass

- [ ] **Step 10: Commit**

```bash
git add backend/app/agents/recommendation/agent.py backend/app/modules/recommendations backend/app/main.py backend/tests/test_recommendation_agent.py backend/tests/test_recommendation_endpoints.py
git commit -m "feat: add RecommendationAgent (hybrid structured filter plus vector rerank) and recommendations endpoints"
```

---

## Phase 2 Definition of Done

- All 5 tasks committed, full backend test suite green (SQLite, with the documented live-LLM exclusions).
- `POST /api/v1/competency/analyze` produces a real, evidence-informed gap analysis for a seeded user (manually verify: register a user, complete a statistical-engine question, run analyze, confirm the statistical domain score reflects it).
- `POST /api/v1/recommendations/generate` produces recommendations with real LLM-written rationale when `GROQ_API_KEY`/`GOOGLE_API_KEY` and `PINECONE_API_KEY` are set, and degrades gracefully (structured-filter-only, templated rationale) when they're not.
- Ready for Phase 3 (MCQ/quiz generation from uploaded materials) to be brainstormed next.
