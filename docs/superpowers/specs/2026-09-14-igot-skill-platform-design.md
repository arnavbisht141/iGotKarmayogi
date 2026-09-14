# AI-Enabled Skill Intelligence & Learning Platform — Design

Branch: `final-shoot` (off `cgp/statistical`)
Date: 2026-09-14

## 1. Problem & Scope

Build an AI-enabled learning platform for India's Official Statistical System that:
- builds a competency profile per official from designation/department/role/education/experience/prior training,
- assesses that profile against competency frameworks across 4 domains (Statistical, Technical, Digital Governance, Behavioural/Managerial),
- identifies skill gaps and recommends personalized learning paths from an iGOT Karmayogi course catalogue (mocked adapter for now),
- generates MCQs/quizzes from uploaded learning materials (PDF/PPT/video transcript) via LLM, with instant grading and explanations,
- exposes learner and admin analytics dashboards,
- is secure, RBAC-gated, and cloud-ready (Postgres/Supabase).

Current repo state (see audit): FastAPI modular monolith with a real but siloed schema per domain (technical pipeline and cyber/digital-governance persisted; statistical_engine and behavioural sessions in-memory only), a single trivial LangGraph node for chat, an empty `ai-service/`, and a Next.js frontend with 26 pages but hand-rolled (non-shadcn) components and a 5-line admin stub.

## 2. Decisions Locked In

- **iGOT integration**: mocked adapter behind a clean interface (`IgotClient`), backed by our own `courses` table now; swappable for the real API later without touching callers.
- **Data store**: consolidate on Supabase Postgres. Drop SQLite. Existing 26-table SQLAlchemy schema is kept and extended (not rewritten) — it's already well-normalized and `UserProfile` already captures designation/department/job_role/education/work_experience/prior_training, which is most of the competency-profile input surface the problem statement asks for.
- **LLM stack**: keep LangChain + LangGraph, Groq (primary, `llama-3.3-70b-versatile`) -> OpenAI -> Gemini fallback chain, already wired in `backend/app/core/config.py`. Real keys are present in root `.env`.
- **Orchestration**: LangGraph supervisor graph coordinating specialist agents (competency-gap agent, recommendation agent, MCQ-generation agent, tutor/chat agent) instead of today's single-node graph.
- **Frontend**: migrate to real shadcn/ui (Radix primitives + CVA), sourcing polished component patterns from 21st.dev via Playwright MCP (fetch component code/prompts, adapt to our design system) rather than hand-rolling. Add per-competency-domain pages, learner + admin dashboards, and LMS features comparable to Coursera/popular LMS: video lessons via YouTube embed, course player with progress tracking, module/lesson structure (already modeled), certificates of completion, ratings/reviews on courses, instructor/source attribution, wishlist/saved courses, search & filter, gamification (streaks — already partially modeled via `current_streak_days`). Explicitly out of scope: payments, live cohorts/proctoring, social forums — no fit for a government upskilling tool and not asked for.
- **Branding**: define a distinct visual identity (not generic Tailwind/shadcn defaults) during the frontend phase — covered under `frontend-design` skill guidance when we get there.
- **OSS reuse**: where a phase's problem has a well-known open-source pattern (e.g. LangGraph supervisor patterns, PDF/PPT parsing libraries, YouTube embed components), prefer adapting a known-good library/pattern over inventing one from scratch.

## 3. Phased Build Plan

Each phase gets its own brainstorm-approval -> plan -> implementation -> review cycle. This spec covers Phase 1 in full detail; later phases are scoped at a summary level and will be re-brainstormed in detail when reached (requirements may shift once Phase 1 ships).

### Phase 1 — Data layer: unified competency schema + Postgres migration

**Goal**: one source of truth in Supabase Postgres, with cross-domain competency data structured so gap-analysis and recommendation (Phase 2) have something real to read and write.

**Schema additions** (new Supabase migration, additive to existing 17+10 tables):

- `competency_domains` — the 4 top-level domains (statistical, technical, digital_governance, behavioural), seeded.
- `competencies` — individual competencies within a domain (e.g. "Survey Design", "Python", "Data Privacy", "Leadership"), FK to `competency_domains`, replaces/extends the existing generic `skills` table's role by giving it domain grouping and a proficiency-level rubric (1-5).
- `competency_profiles` — one row per user, aggregates a computed overall readiness score per domain (4 float columns) plus `last_computed_at`; derived/cache table, recomputed by the gap-analysis agent, not hand-edited.
- `user_competency_scores` — per-user, per-competency current level (0-5), evidence source (`self_declared`, `assessment`, `inferred`), and `updated_at`. Supersedes/feeds from `user_skills` for the 4-domain model; existing `user_skills` stays for backward-compat with technical pipeline, bridged via a `competency_id` nullable FK rather than dropped.
- `gap_analyses` — one row per (user, domain) run: target level, current level, gap size, generated_at. History table, not just latest snapshot, so admin analytics can show trend.
- `recommendations` — one row per (user, course_or_lab, reason, score, generated_at, status: `pending`/`enrolled`/`dismissed`), output of the recommendation agent.
- Persist statistical_engine's in-memory state: `stat_engine_attempts`, `stat_engine_mastery` — mirror what `memory_repositories.py` currently holds so it survives restarts. Exact columns pulled from `backend/app/statistical_engine/memory_repositories.py` at implementation time.
- Persist behavioural sessions similarly: `behavioural_sessions`, `behavioural_interview_results` — mirrors `CarryforwardSessionManager`/`InterviewSessionManager` state.

**Migration mechanics**: `DATABASE_URL` in `.env` moves from `sqlite:///./karmayogi.db` to the Supabase Postgres URI (already present as `SUPABASE_URL`/service key — need the Postgres connection string too, added to `.env`). `Base.metadata.create_all` continues to work against Postgres; a proper Supabase SQL migration file is added under `supabase/migrations/` mirroring the ORM changes, per existing project convention (see `20260914000001_technical_course_pipeline.sql` as the pattern to follow — ORM models are the source of truth, migration file documents/applies the same DDL to Supabase directly since seeding currently happens via SQLAlchemy at FastAPI startup, not via the migration files).

**Out of scope for Phase 1**: no changes to routers/endpoints, no LLM work — pure schema + persistence-wiring for the two in-memory subsystems, executed as a mechanical port of existing in-memory repo logic to SQLAlchemy repos with the same interface, so Phase 1 is a safe, isolated, testable change.

**Testing**: existing `backend/tests/stats_engine` and `test_behavioural_cgp.py` must keep passing against the new Postgres-backed repos (swap fixtures, not test logic). New tests for the competency tables: create profile, record score, run one gap analysis, assert `gap_analyses` row shape.

### Phase 2 — Competency engine, gap analysis, mock iGOT adapter, recommendation agent

- `CompetencyGapAgent` (LangGraph node/graph): reads `user_competency_scores` + a seeded competency framework (target levels per job_role), writes `gap_analyses` + updates `competency_profiles`.
- `IgotClient` interface + `MockIgotClient` implementation: `list_courses(domain, competency_ids)`, `get_enrollment_status(user, course)`, `sync_completion(user, course)` — backed by our own `courses`/`enrollments` tables today.
- `RecommendationAgent`: given gaps + course catalogue (via `IgotClient`) + learning history, ranks and writes `recommendations`. Uses semantic search (embeddings over course descriptions) + rule-based filtering (job role, department priority) — LLM used for ranking rationale/explanation text, not for the retrieval itself.
- New endpoints: `GET /api/v1/competency/profile`, `GET /api/v1/competency/gaps`, `GET /api/v1/recommendations`.

### Phase 3 — MCQ/Quiz generation from uploaded materials

- Ingest pipeline: accept PDF/PPTX/video-transcript upload, extract text (reuse pattern from `technical_courses` transcript pipeline where applicable), chunk, embed.
- `QuizGenerationAgent` (LangGraph): chunk -> generate candidate MCQs with distractors + explanations -> self-check pass (agent critiques its own questions for ambiguity/correctness) -> persist to `questions`/`assessments` tables (already exist) tagged with source-material provenance.
- Instant evaluation: reuse existing `assessment_attempts` grading path, extend to surface per-question explanation on submit.
- New endpoints: `POST /api/v1/quiz/generate` (upload + params), `GET /api/v1/quiz/{id}`.

### Phase 4 — Agent orchestration

- Replace the single-node LangGraph in `backend/app/agents/router.py` with a supervisor graph routing between: chat/tutor node (existing canned+LLM logic), CompetencyGapAgent, RecommendationAgent, QuizGenerationAgent — shared LLM client factory (the existing Groq->OpenAI->Gemini fallback), shared conversation memory.
- Decide at this point whether agent code moves into the still-empty `ai-service/` (per ADR 0001's stated intent) or stays in `backend/app/agents` — revisit ADR 0001/0002 with fresh eyes once real agent count/complexity is known.

### Phase 5 — Frontend

- Real shadcn/ui migration (Radix + CVA), sourcing component patterns from 21st.dev community via Playwright MCP.
- Per-competency-domain pages for all 4 domains with real data (profile, gap, recommendations) replacing/extending current `/statistical`, `/behavioural`, `/digital-governance` pages and adding a `/technical` equivalent.
- Learner dashboard: competency levels, gaps, recommended paths, learning hours, progress (extend existing `/home`, `/progress`).
- Admin dashboard: build out the 5-line stub into workforce competency distribution, training effectiveness, predictive gap trends (backed by `gap_analyses` history).
- Quiz-from-upload UI: upload flow, generated-quiz review/edit (trainer), take-quiz flow with instant feedback.
- LMS feature pass: YouTube embed for video lessons, course player polish, certificates, ratings, search/filter.
- Branding pass per `frontend-design` skill.

## 4. Risks / Open Questions Deferred to Later Phases

- Whether `ai-service/` gets populated (Phase 4 decision) — not blocking Phase 1-3.
- Exact competency-framework target levels per job role (who defines "expected Python level for a Deputy Director") — needs either a seed dataset the user provides, or a reasonable default framework we draft and flag for review at Phase 2 kickoff.
- Real Postgres connection string for Supabase — need it added to `.env` before Phase 1 implementation runs migrations (SUPABASE_URL/keys present are REST API keys, not the Postgres URI).
