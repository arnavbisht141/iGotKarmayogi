# Phase 2: Competency Engine, Gap Analysis, Mock iGOT Adapter, Recommendation Agent — Design

Branch: `final-shoot`
Date: 2026-09-15
Builds on: `docs/superpowers/specs/2026-09-14-igot-skill-platform-design.md` (master design), Phase 1 (unified competency data layer, complete).

## 1. Goal

Turn the data layer Phase 1 built into something that actually computes: a per-user cross-domain competency profile, gaps against expected levels, and ranked course recommendations that explain themselves. Phase 1 gave the schema something real to read and write; Phase 2 is the first thing that reads and writes it.

## 2. Decisions Locked In

- **Target competency levels**: no new DB table. A small Python lookup (designation-tier x domain) in a new `backend/app/agents/competency/target_levels.py`, keyed off `UserProfile.designation`/`job_role` text via keyword matching (Director/Deputy/Assistant/Officer tiers, matching common Indian government designation patterns). Explicitly a starting default, not a real framework — flagged in the module docstring and in the API response (`is_default_framework: true`) so nobody mistakes it for authoritative. Swappable for a real dataset later without touching callers.
- **Evidence-to-competency mapping**: new table `evidence_competency_mapping` (source_system, source_key, competency_id) bridges the free-text skill/competency identifiers used by `stat_engine_mastery`/`stat_engine_attempts` (e.g. `"price.price_relative"`, `"price_statistics"`) and `behavioural_session_results` (e.g. `"Leadership"`, `"Ethical Judgement"`) to real `competencies.id` rows. Seeded with the well-known keys discoverable in the statistical engine's question templates and the behavioural competency-name sets used by both `carryforward_session.py` and `interview_service.py`. Two behavioural dimensions (`Situational Awareness`, `Accountability`) have no existing taxonomy match — Phase 2 adds them as two new rows to `competencies` (domain `behavioural`), additive to Phase 1's seed. Any evidence key with no mapping is skipped (logged, not fatal) rather than blocking a gap-analysis run — this table is meant to grow incrementally, not be exhaustive on day one.
- **Mock iGOT adapter**: `IgotClient` ABC + `MockIgotClient` backed entirely by the existing `courses`/`enrollments` tables. No network calls, no external service.
- **Recommendation approach**: hybrid RAG. Structured filter first (domain match, difficulty vs. target level) narrows candidates in Postgres, Pinecone vector search re-ranks by semantic similarity between a generated gap description and course embeddings, then an LLM call (existing Groq→OpenAI→Gemini fallback) writes the human-readable rationale for the top results. Embeddings via `GoogleGenerativeAIEmbeddings` (`langchain-google-genai`, already a dependency, `text-embedding-004`, 768-dim) since `GOOGLE_API_KEY` is already configured — no new embedding provider needed.
- **Vector store**: Pinecone (serverless, cosine metric, 768-dim), one index (`PINECONE_INDEX_NAME`, key already in `.env`). New dependency: `pinecone-client` added to `backend/requirements.txt`.
- **Auth**: all new endpoints require an authenticated user (`Depends(get_current_active_user)`, the strict existing dependency, not the optional one Phase 1's behavioural fix introduced for anonymous practice sessions) — competency profile, gaps, and recommendations are inherently personal, there's no anonymous case here.
- **Gap analysis and recommendation generation are explicit actions, not implicit side effects of a GET.** A `POST /competency/analyze` computes and persists a fresh `gap_analyses` snapshot + updates `competency_profiles`; `GET /competency/gaps` just reads the latest. Same split for recommendations (`POST /recommendations/generate` vs `GET /recommendations`). This matches the existing `technical_courses` module's explicit-pipeline-step pattern and keeps read endpoints cheap and side-effect-free.
- **Course indexing into Pinecone is a separate, explicit step** (`POST /admin/courses/{id}/reindex`), not automatic on every course write — keeps the write path to `courses` simple and avoids surprise embedding-API calls on unrelated course edits. Bulk reindexing (all courses) is a one-off management script, not a dedicated endpoint — YAGNI, an admin runs it once after seeding/importing courses.

## 3. Schema Additions (Phase 2 migration, additive)

- `evidence_competency_mapping`: `id`, `source_system` (`stat_engine_skill` | `stat_engine_competency` | `behavioural_competency`), `source_key` (string, e.g. `"price.price_relative"`), `competency_id` (FK → `competencies.id`), unique on `(source_system, source_key)`.
- Two new `competencies` rows (via seed, not a migration DDL change): `behavioural_situational_awareness`, `behavioural_accountability`, domain `behavioural`.
- No other new tables. `gap_analyses`, `recommendations`, `competency_profiles`, `user_competency_scores` (all from Phase 1) are the write targets.

## 4. Components

### 4.1 `CompetencyGapAgent` (`backend/app/agents/competency/gap_agent.py`)

LangGraph graph, single flow (no branching needed yet — this is an ETL-shaped task, not a conversational one, so a plain function pipeline wrapped in one LangGraph node is enough; no multi-agent conversation here):

1. Load the user's `UserProfile` (designation/job_role) → resolve target levels via `target_levels.py`.
2. Load `user_competency_scores` (Phase 1, self-declared/assessment-sourced).
3. Load raw evidence: `stat_engine_mastery` rows for the user, `behavioural_session_results` rows for the user (both keyed by string user_id/int user_id respectively — note `stat_engine_mastery.user_id` is `VARCHAR`, cast/compare as string).
4. Resolve each evidence row's skill/competency string through `evidence_competency_mapping` → `competency_id`; skip unmapped rows (log at debug level).
5. Merge: for each `competency_id` touched by either `user_competency_scores` or resolved evidence, compute a current level (evidence-sourced mastery scores and behavioural scores are 0-100 or 0-1 scales depending on source — normalize all to the same 0-5 scale `user_competency_scores.level` uses before merging; take the max of self-declared and evidence-derived where both exist, evidence should not lower a level below what's already recorded).
6. For each of the 4 domains, aggregate a domain-level score (mean of that domain's competency levels, 0-5 scale, projected to 0-100 for `competency_profiles`'s existing float columns) and compare to the target level for that domain → write one `gap_analyses` row per domain (target_level, current_level, gap).
7. Upsert `competency_profiles` (the 4 domain scores + `last_computed_at`).

### 4.2 `IgotClient` (`backend/app/agents/igot/client.py`)

```python
class IgotClient(ABC):
    def list_courses(self, domain: Optional[str] = None, competency_ids: Optional[List[int]] = None) -> List[Course]: ...
    def get_enrollment_status(self, user_id: int, course_id: int) -> Optional[str]: ...  # None | "in_progress" | "completed"
    def sync_completion(self, user_id: int, course_id: int) -> None: ...  # marks Enrollment.status = "completed"

class MockIgotClient(IgotClient):
    def __init__(self, db: Session): ...
    # implemented entirely against the existing Course/Enrollment tables
```

### 4.3 `RecommendationAgent` (`backend/app/agents/recommendation/agent.py`)

1. Read the user's latest `gap_analyses` (one per domain).
2. For each domain with `gap > 0`, build a natural-language gap description ("Officer needs to progress from level {current} to {target} in {domain}, particularly in {top competencies by gap}").
3. Structured filter: query `courses` joined through `course_skills`/the domain's competencies for candidates roughly matching the domain and a difficulty tier consistent with the gap size (small gap → beginner/intermediate, large gap → intermediate/advanced) — this is the Postgres-side narrowing, cheap and exact.
4. Semantic re-rank: embed the gap description, query Pinecone (top-k=10, metadata-filtered by the same domain/category where the metadata supports it) for the closest course vectors, intersect with the structured candidate set.
5. Drop courses already `completed` per `MockIgotClient.get_enrollment_status`.
6. Take the top 3-5 by combined score (structured-match tier + vector similarity), call the LLM once per user (not once per course) with all finalist courses + the gap descriptions, asking for a one-paragraph rationale per course tied to the specific gap.
7. Write one `Recommendation` row per finalist course (reason = the LLM-written rationale, score = the combined ranking score, status defaults to `pending`).

### 4.4 Course indexing (`backend/app/agents/recommendation/indexer.py`)

`index_course(db: Session, course_id: int) -> None`: builds embedding text from `title + overview + organization + category + joined skill names`, embeds via `GoogleGenerativeAIEmbeddings`, upserts to Pinecone with `id=f"course-{course_id}"` and metadata `{course_id, category, difficulty, title}`.

## 5. New Endpoints (all under existing `/api/v1` prefix pattern, all require `Depends(get_current_active_user)`)

- `POST /competency/analyze` — runs `CompetencyGapAgent` for the current user, returns the fresh `gap_analyses` + `competency_profiles` snapshot.
- `GET /competency/profile` — returns the current user's `competency_profiles` row (404 if `analyze` never run).
- `GET /competency/gaps` — returns the current user's latest `gap_analyses` row per domain.
- `POST /recommendations/generate` — runs `RecommendationAgent` for the current user.
- `GET /recommendations` — returns the current user's `recommendations` (filterable by `status`).
- `POST /admin/courses/{id}/reindex` — admin-only (existing role check pattern), runs `index_course`.

## 6. Error Handling

- Missing/unmappable evidence rows: skipped, logged, never fatal to a gap-analysis run.
- Pinecone unavailable (network/API error): `RecommendationAgent` falls back to the structured-filter-only candidate list (no semantic re-rank), still returns recommendations rather than failing the whole request — logged as degraded, not silent.
- LLM unavailable: existing Groq→OpenAI→Gemini fallback chain already handles this; if all three fail, recommendation rows are still written with a templated (non-LLM) rationale string rather than blocking the whole flow.

## 7. Testing

- `evidence_competency_mapping` seed + resolution: unit tests with in-memory SQLite (Pinecone/LLM calls mocked or skipped entirely — this layer doesn't need either).
- `CompetencyGapAgent`: unit tests against in-memory SQLite fixtures covering the normalize-and-merge logic (self-declared vs. evidence-derived, unmapped-evidence skip).
- `MockIgotClient`: unit tests against in-memory SQLite, no mocking needed (it's a real implementation, not a stub).
- `RecommendationAgent`: the Pinecone/embedding/LLM calls are the one place this phase needs to mock external services in tests — structure the agent so the vector-search step and the LLM-rationale step are separately injectable/mockable functions, test the merge/ranking/fallback logic with fakes, and leave one manual/integration-only smoke test (not part of the default `pytest` run) that hits real Pinecone+Gemini to confirm end-to-end wiring.

## 8. Out of Scope for Phase 2

- Real iGOT API integration (still mocked, per the master design's locked-in decision).
- A real, externally-validated target-level framework (still the drafted default).
- Automatic/scheduled re-analysis (gap analysis and recommendations are user/admin-triggered actions only, for now).
- Frontend for any of this (Phase 5).
