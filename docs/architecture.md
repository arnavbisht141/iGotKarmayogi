# System Architecture & Engineering Standards

> **Document Type:** System Architecture & Agent Knowledge Base  
> **Phase:** Phase 0 Implementation (Smart India Hackathon SIH '26)  
> **Target Audience:** AI Coding Agents, Software Engineers, Evaluators  

---

## 1. System Architecture Diagram

```
                                  ┌─────────────────────────────────────────┐
                                  │           Browser Client                │
                                  │      (Civil Servant / Evaluator)        │
                                  └────────────────────┬────────────────────┘
                                                       │
                                  HTTP (Port 3000)     │
                                                       ▼
                      ┌─────────────────────────────────────────────────────────────────┐
                      │                   FRONTEND CONTAINER (Next.js 16)               │
                      │ ─────────────────────────────────────────────────────────────── │
                      │ • Next.js 16 (App Router)        • TypeScript & ESLint          │
                      │ • Tailwind CSS v4                • Lucide React Icons           │
                      │ • shadcn/ui Component Primitives • Canvas Confetti Milestones   │
                      │ • Standalone Runner (~150MB)     • Custom i18n Context (EN/HI)  │
                      └────────────────────────┬────────────────────────────────────────┘
                                               │
                               REST Calls via  │ NEXT_PUBLIC_API_URL (Port 8000)
                                               ▼
                      ┌─────────────────────────────────────────────────────────────────┐
                      │                    BACKEND CONTAINER (FastAPI)                  │
                      │ ─────────────────────────────────────────────────────────────── │
                      │ • FastAPI (Python 3.12)          • Pydantic v2 Validation       │
                      │ • SQLAlchemy 2.0 ORM             • Custom PBKDF2-HMAC Auth      │
                      │ • Uvicorn ASGI Server            • Automated DB Directory Init  │
                      └───────────────┬─────────────────────────────────┬───────────────┘
                                      │                                 │
           Stateful AI Invocations    │                                 │ Direct Queries
                                      ▼                                 ▼
         ┌──────────────────────────────────────────────┐    ┌──────────────────────────┐
         │         AI AGENT (LangGraph + LangChain)     │    │  PERSISTENT SQLITE STORE │
         │ ──────────────────────────────────────────── │    │ ──────────────────────── │
         │ • StateGraph Compiled Workflow               │    │ • karmayogi.db           │
         │ • Google Gemini / OpenAI Support             │    │ • /app/data volume mount │
         │ • Built-in MoSPI Domain Knowledge Engine     │    │ • 17 Normalized Tables   │
         └──────────────────────────────────────────────┘    └──────────────────────────┘
```

---

## 2. Responsibilities & Boundaries

| Boundary | Owns | Must NOT Own |
|---|---|---|
| **Frontend** | Presentation, UI rendering, calls to LMS API | Business records, direct external AI provider keys |
| **LMS Backend** | Authorization, LMS business rules, data mutations, AI context shaping | Direct browser exposure of AI provider keys |
| **Future AI Service** | Orchestration, prompts, provider selection, response generation | LMS persistence, certificate decisions, user authorization |
| **Model Providers** | Generated text | Platform truth, authoritative certification decisions |

*Reference ADRs:*
- [`adr/0001-modular-monolith-and-ai-boundary.md`](adr/0001-modular-monolith-and-ai-boundary.md)
- [`adr/0002-backend-owns-lms-data.md`](adr/0002-backend-owns-lms-data.md)

---

## 3. Database Schema & Domain Models

All models are centralized in `backend/app/models/models.py`:

| Model Name | Table Name | Purpose & Relationships |
|---|---|---|
| `User` | `users` | Core credentials, email, password hash, role (`admin` or `learner`), active status. |
| `UserProfile` | `user_profiles` | Department, designation, cadre, phone, state, onboarding status, preferences. |
| `Department` | `departments` | Government departments/ministries (MoSPI, DoPT, ISTM, Finance). |
| `Course` | `courses` | Course catalog, descriptions, thumbnails, level, duration, provider (MoSPI vs ISTM). |
| `Module` | `modules` | Syllabus sections within a course, ordered by sequence number. |
| `Lesson` | `lessons` | Atomic units: video URLs, markdown reading material, practice concept checks. |
| `Skill` | `skills` | Competency taxonomy (e.g., *Survey Sampling*, *National Accounts*, *Inflation Analysis*). |
| `CourseSkill` | `course_skills` | Association linking courses to the specific competencies they instill. |
| `UserSkill` | `user_skills` | Association tracking a learner's acquired competency level. |
| `Enrollment` | `enrollments` | Tracks learner enrollment, overall completion percentage, status, and dates. |
| `Progress` | `progress` | Granular per-lesson completion records with timestamps. |
| `Assessment` | `assessments` | Graded exams linked to courses or modules (passing standard: 70%). |
| `Question` | `questions` | MCQs with options, correct answer index, explanation, and difficulty rating. |
| `AssessmentAttempt` | `assessment_attempts` | Full history of quiz submissions, score percentage, passed flag, and answers. |
| `PlannedCourse` | `planned_courses` | Future target courses marked by civil servants on their dashboard. |
| `LearningHistory` | `learning_history` | Historical log of learning sessions, time spent, and streak calculations. |
| `SearchHistory` | `search_history` | Recent searches recorded for discovery suggestions and trending analytics. |

---

## 4. Mandatory Operational Guidelines for AI Coding Agents

When continuing work on this codebase, all AI agents **MUST adhere to the following rules**:

### Rule 1: Respect the Navy Blue & Sober Yellow Institutional Design System
- Follow the official Government of India palette: Official Navy Primary (`#1E3A8A` / `#172554`), Sober Yellow (`#EAB308` / `#CA8A04`), clean neutral background (`#F8FAFC`), and crisp slate typography (`#0F172A` / `#334155` / `#64748B`). Never use legacy muted rose (`#965C66` / `#EEE8E9`).
- Strict prohibition of decorative emojis (`🔥`, `✨`, `★`) and artificial rectangular colored pill boxes above headings. Use clean Lucide SVG icons and official typography.
- Ensure 100% full bilingual (Hindi/English) compatibility across all user-facing pages using `useI18n()` and `frontend/src/lib/i18n/index.tsx`.
- Preserve aspect ratios on all institutional graphics (`object-contain`).


### Rule 2: Keep the Next.js Standalone Build Functional
- Ensure any client component using `useSearchParams()` is wrapped inside a `<Suspense>` boundary (required by Next.js Turbopack).
- Keep `output: "standalone"` in `next.config.ts`.
- Do not import server-only packages into client components.

### Rule 3: Maintain Backend Security Standards
- Do NOT re-introduce `passlib[bcrypt]` due to known upstream Python 3.12 compatibility bugs. Always use the NIST-standard PBKDF2 implementation in `backend/app/core/security.py`.
- Ensure new endpoints have clear Pydantic schemas and are registered under `app.include_router(..., prefix=settings.API_V1_STR)`.

### Rule 4: Zero External Dependency Lock for AI
- When expanding AI agent capabilities in `backend/app/agents/`, **always maintain fallback execution**. The system must never crash if `GOOGLE_API_KEY` or `OPENAI_API_KEY` is omitted.

### Rule 5: Preserve Seed Data Reproducibility
- Any new model added to `models.py` must have corresponding seed data in `backend/app/core/seed_data.py` so that executing `docker compose down -v && docker compose up --build` produces a fully populated, demonstratable system.

---

## 5. Roadmap: Phase 0 Boundaries vs. Phase 1+

| Feature Area | Phase 0 (Current Implementation) | Phase 1 & 2 (Planned Future Scope) |
|---|---|---|
| **LMS User Flow** | Complete Miro user flow implemented with real courses, lessons, and practice checks. | Adaptive course generation dynamically re-sequencing modules based on real-time quiz performance. |
| **Assessments** | 70% passing threshold MCQ engine, instant grading, full explanations, verifiable certificates. | Automated question generation from PDF course notes, AI-proctored webcam exam validation. |
| **AI Assistant** | Context-aware statistical copilot via LangGraph with multi-provider and local fallback support. | Multi-agent autonomous workflow: Personal Tutor Agent + Evaluation Agent + Cadre Alignment Agent. |
| **Admin Analytics** | Officer completion overview, course assignment modal, question difficulty/failure analytics. | Cross-ministry predictive competency gap analysis and automated training budget allocation. |
| **Authentication** | JWT with PBKDF2 hashing, demo quick logins, role protection (`admin` vs `learner`). | Parichay / Jan Parichay single sign-on (SSO) integration with official Government of India NIC gateway. |
