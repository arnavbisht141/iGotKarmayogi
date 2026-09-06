# 🏛️ iGOT Karmayogi (MoSPI) — Master Project Context & Architectural Progress Guide

> **Document Type:** Project Context, Architectural Blueprint & Agent Knowledge Base  
> **Location:** `docs/PROJECT_CONTEXT_AND_PROGRESS.md`  
> **Phase:** Phase 0 Implementation (Smart India Hackathon SIH '26)  
> **Target Audience:** AI Coding Agents, Software Engineers, UI/UX Designers, Evaluators

---

## 📌 Table of Contents
1. [Executive Summary & Hackathon Context](#1-executive-summary--hackathon-context)
2. [Technology Stack & System Architecture](#2-technology-stack--system-architecture)
3. [Database Schema & Domain Models](#3-database-schema--domain-models)
4. [Pre-Seeded Accounts & Test Personas](#4-pre-seeded-accounts--test-personas)
5. [Miro User Flow Realization & Route Inventory](#5-miro-user-flow-realization--route-inventory)
6. [UI/UX Design System: The Muted Rose Standard](#6-uiux-design-system-the-muted-rose-standard)
7. [AI Copilot Architecture (LangGraph + LangChain)](#7-ai-copilot-architecture-langgraph--langchain)
8. [Dockerization & DevOps Lifecycle](#8-dockerization--devops-lifecycle)
9. [Recent Changes & Branch Synchronization](#9-recent-changes--branch-synchronization)
10. [Rules & Operational Guidelines for Future AI Agents](#10-rules--operational-guidelines-for-future-ai-agents)
11. [Roadmap: Phase 0 Boundaries vs. Phase 1+](#11-roadmap-phase-0-boundaries-vs-phase-1)

---

## 1. Executive Summary & Hackathon Context

### Problem Statement
Under Mission Karmayogi, civil servants require accredited competency-driven capacity building. However, existing public-service platforms often lack personalized learning pathways, structured micro-assessment checkpoints, verifiable competency tracking, and an intuitive, dignifying civil-service user experience.

For the **Ministry of Statistics and Programme Implementation (MoSPI)** in **Smart India Hackathon (SIH '26)**, this platform serves as the **Phase 0 implementation** of an AI-enabled skill intelligence and learning management system (LMS). It focuses on:
- Official statistical methodologies (NSS surveys, CPI inflation compilation, UN-NQAF data quality standards, PFMS financial architecture, and Python for policy analysis).
- High-fidelity execution of the validated **Miro LMS User Flow**.
- Clean, institutional, non-flashy design (strictly civil-service dignified, avoiding excessive "neon AI" visuals).
- Production-grade multi-stage containerization with live-development hot-reloading.

---

## 2. Technology Stack & System Architecture

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

### Detailed Tech Stack
| Component | Technology | Version | Key Decisions & Rationale |
|---|---|---|---|
| **Frontend Framework** | Next.js (App Router) | `16.3.4` | React 19, standalone output mode for lightweight production containers. |
| **Language** | TypeScript | `5.x` | Strict type safety across all API interactions and state objects. |
| **Styling** | Tailwind CSS | `4.x` | Modern utility classes, custom muted rose theme tokens, responsive layouts. |
| **Components** | shadcn/ui inspired primitives | Custom | Accessible Dialogs, Badges, Cards, Inputs, Progress Bars. |
| **Icons & Effects** | Lucide React + Canvas Confetti | `^1.41.0`, `^1.9.4` | Clean iconography + celebratory feedback upon passing assessments. |
| **Backend Framework** | FastAPI | `>=0.115.0` | Async Python 3.12 API, automatic OpenAPI/Swagger documentation at `/docs`. |
| **ORM & Database** | SQLAlchemy + SQLite | `>=2.0.30` | Declarative models, thread-safe session handling, volume-persisted SQLite. |
| **Security / Auth** | Python `hashlib` (PBKDF2-HMAC-SHA256) | Standard Lib | Replaced broken `passlib[bcrypt]` compatibility with robust NIST PBKDF2. |
| **Validation** | Pydantic + `email-validator` | `>=2.8.0`, `>=2.2.0` | Strict request/response parsing and government domain email checking. |
| **AI Orchestration** | LangGraph + LangChain Core | `>=0.2.0` | StateGraph node compilation, multi-provider model routing, local fallback. |
| **Container Engine** | Docker & Docker Compose | Desktop 29.6+ | Dual compose profiles (Production standalone vs Development volume-mount). |

---

## 3. Database Schema & Domain Models

All models are defined in [backend/app/models/models.py](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/backend/app/models/models.py):

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

## 4. Pre-Seeded Accounts & Test Personas

The database is automatically seeded on startup via [backend/app/core/seed_data.py](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/backend/app/core/seed_data.py):

| Role | Email | Password | Pre-Configured State & Key Demonstration Flow |
|---|---|---|---|
| **Administrator** | `admin@karmayogi.gov.in` | `Admin@123` | Has full access to `/admin` console. Can inspect officer completion rates across cadres, assign courses, create curriculum, and view question failure-rate analytics. |
| **Senior Statistical Officer** | `rajesh.kumar@mospi.gov.in` | `Learner@123` | Fully onboarded officer. Has active 66% progress in *National Sample Survey Methodologies*, a 6-day learning streak, today's goals, and acquired competency badges. |
| **New Civil Servant** | `priya.sharma@mospi.gov.in` | `Learner@123` | Brand new officer. `is_onboarded = False`. Logging in immediately redirects into the **5-step Onboarding Wizard**. |

> [!TIP]
> The login screen at `/login` provides **1-click demo login buttons** for instant persona switching during live evaluation.

---

## 5. Miro User Flow Realization & Route Inventory

```
ENTRY (/) ──▶ AUTH (/login, /register) ──▶ ONBOARD (/onboarding, 5 steps) ──▶ HOME (/home)
                                                                                  │
   ┌──────────────────────────────────────────────────────────────────────────────┘
   ▼                                             ▼
Discover (/discover) ────▶ Course Detail ────▶ Learn (/learn/[courseId]) ──▶ Assess (/assess/[id])
                            (/courses/[id])      (Split Player + Practice)       (MCQ 70% standard)
                                                                                  │
                                                                                  ▼
                                                            Certificates & Analytics (/my-learning)
```

### Route-by-Route Breakdown
1. **Landing Page (`frontend/src/app/page.tsx` - `/`)**:
   - Institutional Ministry top ribbon and scrolling announcement marquee.
   - Two-column hero with verified civil service headline and auto-rotating image carousel (`/karmayogi.jpg`, `/government-meeting.jpg`, `/ai-daksh.jpg`) preserving 100% natural aspect ratios.
   - Left-aligned live statistical metrics: `40,000+` Officers Enrolled, `100%` Accredited Curricula, `UN-NQAF` Standardized, `Verifiable` Digital Credentials.
   - Explore Course preview cards, "How it Works" guide, and dual CTAs.
2. **Authentication (`/(auth)/login`, `/(auth)/register`, `/(auth)/forgot-password`)**:
   - Official government email checking, secure JWT session issuance, role-based redirection.
   - 1-click credentials for instant review.
3. **Onboarding Wizard (`frontend/src/app/onboarding/page.tsx` - `/onboarding`)**:
   - 5-step wizard per Miro flow:
     - Step 1: Profile Setup
     - Step 2: Personal Information (Service Cadre, Batch)
     - Step 3: Education & Prior Experience
     - Step 4: Designation & Department Assignment
     - Step 5: Technical Interests & Skill Focus
   - Progress bar, step validation, and persistent state transition into the Home dashboard.
4. **Home Dashboard (`frontend/src/app/(dashboard)/home/page.tsx` - `/home`)**:
   - Implements **all 10 confirmed Phase 0 widgets**:
     1. Continue Learning (primary resume card with progress bar)
     2. Today's Learning Goals (interactive completion checklist)
     3. Learning Streak Counter (consecutive active days indicator)
     4. Recommended Courses (cadre-tailored statistical suggestions)
     5. Current Course Progress breakdown
     6. Recently Explored modules
     7. Official Learning History log
     8. Trending MoSPI Courses
     9. Future Planned Courses
     10. Competencies & Skills radar summary
5. **Discover Catalog (`frontend/src/app/discover/page.tsx` - `/discover`)**:
   - Instant search input with trending keyword tags (*NSS Survey*, *CPI Inflation*, *PFMS*, *Sampling*).
   - Category filters (*Popular*, *New*, *Foundational*, *Advanced*).
   - Provider segmentation: MoSPI Internal vs. External Partners (ISTM/DoPT).
   - Dynamic query string handling wrapped safely in React `<Suspense>` boundaries.
6. **Course Details (`frontend/src/app/courses/[courseId]/page.tsx`)**:
   - Comprehensive syllabus breakdown with collapsible accordion modules.
   - Metrics summary: duration, video count, reading materials, lab count, assessments.
   - Dynamic button logic: *Start Course* / *Resume Course* / *Completed*.
7. **Coursera-Style Learning Player (`frontend/src/app/learn/[courseId]/page.tsx`)**:
   - Split-screen layout: collapsible syllabus curriculum tree on the left, primary content on the right.
   - Supports video lecture players and markdown official technical reading.
   - **Interactive Concept Practice Activity**: embedded mini-quiz validating understanding *before* advancing, providing immediate regulatory feedback.
8. **Assessment Engine (`frontend/src/app/assess/[assessmentId]/page.tsx`)**:
   - Formal test environment: timed session, instructions, 70% passing standard.
   - Single-choice and multi-choice question evaluator.
   - Automated grading and post-submission review displaying official explanations for all options.
   - Confetti celebratory milestone trigger upon scoring ≥70%.
9. **My Learning, Progress & Certificates (`/my-learning`, `/progress`)**:
   - In-progress courses, completed courses, and earned competency badges.
   - **Verifiable Karmayogi Certificate Modal** (`frontend/src/components/certificate/CertificateModal.tsx`):
     - Official Government of India seal and MoSPI branding.
     - Officer name, course title, completion date, and unique verification ID.
     - Printable and PDF-exportable layout with dedicated print stylesheets.
10. **Admin Console (`frontend/src/app/admin/page.tsx` - `/admin`)**:
    - Restricted to users with the `admin` role.
    - Officer roster with cadre tracking, department filters, and completion percentages.
    - Course assignment modal allowing administrators to assign mandatory training to officers.
    - Question analytics detecting high failure-rate questions to guide curriculum improvements.
11. **Floating Karmayogi AI Widget (`frontend/src/components/shared/AiAssistantWidget.tsx`)**:
    - Accessible across every screen via a circular launcher in the bottom right corner.
    - Clean civil-service branding (*"Karmayogi AI - Civil Service Intelligence Assistant"*).
    - Communicates with the backend LangGraph endpoint (`POST /api/agents/chat`).

---

## 6. UI/UX Design System: The Muted Rose Standard

To reflect public-service dignity and ensure visual consistency across all pages, the platform uses a **Muted Rose Design System** (documented in [docs/UI_UX_CHANGES.md](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/docs/UI_UX_CHANGES.md)).

### Color Palette Tokens
| Token Name | Hex Code | Purpose / Application |
|---|---|---|
| **Primary** | `#965C66` | Primary action buttons, active tabs, institutional headers, brand icons. |
| **Secondary** | `#C8A8A9` | Structural borders, card outlines, subtle dividers, pill borders. |
| **Supporting** | `#BC9798` | Intermediate progress bars, badge highlights, active indicators. |
| **Light Supporting** | `#C2A0A2` | Hover states, subtle separators, delicate borders. |
| **Main Warm Background** | `#EEE8E9` | Warm off-white foundation for page bodies, modals, and input backgrounds. |
| **Charcoal Headings** | `#241E20` | High-contrast readable typography for titles and primary headers. |
| **Muted Charcoal** | `#5A5052` / `#7A4E57` | Subtitles, helper text, breadcrumbs, and secondary labels. |

### UI Design Principles
- **No Overbearing AI Gimmicks:** Avoid glowing neon cyan/purple gradients or floating cybernetic bots. Use clean, institutional styling.
- **Aspect Ratio Integrity:** Never crop or distort official photographs or infographics. Use `object-contain` within rounded framed containers.
- **Left-Aligned Structural Symmetry:** Metric headers, stat figures, and hero titles maintain strict left alignment matching the primary container boundaries.
- **Accessibility & Contrast:** High contrast text on warm backgrounds, clear focus rings on inputs (`focus-visible:ring-[#965C66]`), and keyboard navigability.

---

## 7. AI Copilot Architecture (LangGraph + LangChain)

The AI assistant backend is located in [backend/app/agents/router.py](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/backend/app/agents/router.py).

### Workflow Mechanics
```
[User Chat Request] ──▶ POST /api/agents/chat ──▶ LangGraph StateGraph
                                                          │
                    ┌─────────────────────────────────────┴─────────────────────────────────────┐
                    ▼                                     ▼                                     ▼
          [Google Gemini Key?]                  [OpenAI Key?]                       [No External Keys?]
                    │                                     │                                     │
           Invoke Gemini 1.5 Flash                Invoke GPT-4o-Mini               Invoke MoSPI Fallback Engine
       (source: "langgraph-gemini")          (source: "langgraph-openai")       (source: "langgraph-karmayogi-engine")
                    │                                     │                                     │
                    └─────────────────────────────────────┬─────────────────────────────────────┘
                                                          ▼
                                             [Structured Chat Response]
```

### Deterministic MoSPI Domain Fallback Engine
If no external API keys are configured, the assistant automatically routes queries through a built-in statistical domain knowledge base that accurately responds to:
- **CPI & Inflation:** Modified Laspeyres formula, 2012=100 base year, geometric mean elementary quotes.
- **NSS Methodologies:** Multi-stage stratified sampling, First Stage Units (FSUs), hamlet-group formation.
- **PFMS & Governance:** Treasury Single Account (TSA) mechanics, Aadhaar Payment Bridge.
- **Assessment Policies:** 70% passing threshold, unlimited retakes, official competency badges.
- **Policy Coding:** Vectorized Pandas routines vs. loops for public microdata processing.

---

## 8. Dockerization & DevOps Lifecycle

### Architecture & Configuration Files
- [backend/Dockerfile](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/backend/Dockerfile): Python 3.12-slim base, curl health checks, unbuffered logging.
- [backend/.dockerignore](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/backend/.dockerignore): Excludes `venv/`, `__pycache__/`, `karmayogi.db`.
- [frontend/Dockerfile](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/frontend/Dockerfile): 4-stage build (base ➔ deps ➔ builder ➔ runner) generating an unprivileged ~150MB standalone container.
- [frontend/Dockerfile.dev](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/frontend/Dockerfile.dev): Lightweight container for development with hot module replacement.
- [frontend/.dockerignore](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/frontend/.dockerignore): Excludes `node_modules/`, `.next/`, git files.
- [docker-compose.yml](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/docker-compose.yml): Production setup with persistent SQLite volume (`backend-data:/app/data`) and `/api/health` dependency ordering.
- [docker-compose.dev.yml](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/docker-compose.dev.yml): Development setup with host volume binds (`./frontend:/app`, `./backend:/app`) and protected anonymous volumes for `node_modules` and `venv`.

### Standard Container Commands
```bash
# 1. Start in Production Mode
docker compose up --build -d

# 2. Start in Development Mode (Live code changes reload instantly)
docker compose -f docker-compose.dev.yml up --build

# 3. View Logs
docker compose logs -f backend
docker compose logs -f frontend

# 4. Clean Rebuild (Bypassing cache)
docker compose build --no-cache
docker compose up -d

# 5. Stop Containers & Reset Database to fresh seed data
docker compose down -v
```

---

## 9. Recent Changes & Branch Synchronization

### Git History Highlights
- `79cc29f`: Dockerized entire application with production and development compose setups, updated README.
- `f8eb3fe`: Merged `arnav` branch into `main`.
- `4d2b65e` - `6a4b519`: UI/UX refinement pass on `Aarna` branch establishing the Muted Rose design system, aspect-ratio preserved hero images, circular AI widget, and clean navigation flow.
- `4380504`: Merged `Aarna` branch into `main`.
- Rebased `arnav` branch with `main` to maintain clean linear history.
- Added [README_arnav.md](file:///d:/Main_Files/AIMS/Hacks/SIH%2726/iGot_Karmayogi/README_arnav.md) documenting technical setup and verification steps.

---

## 10. Rules & Operational Guidelines for Future AI Agents

When continuing work on this codebase, all AI agents **MUST adhere to the following rules**:

### Rule 1: Respect the Muted Rose Design System
- Do NOT introduce generic bright blues (`bg-blue-600`), neon emeralds, or purples.
- Use `#965C66` for primary CTAs and active states, `#C8A8A9` for borders, `#EEE8E9` for backgrounds, and `#241E20` for text.
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

## 11. Roadmap: Phase 0 Boundaries vs. Phase 1+

| Feature Area | Phase 0 (Current Implementation) | Phase 1 & 2 (Planned Future Scope) |
|---|---|---|
| **LMS User Flow** | Complete Miro userflow implemented with real courses, lessons, and practice checks. | Adaptive course generation dynamically re-sequencing modules based on real-time quiz performance. |
| **Assessments** | 70% passing threshold MCQ engine, instant grading, full explanations, verifiable certificates. | Automated question generation from PDF course notes, AI-proctored webcam exam validation. |
| **AI Assistant** | Context-aware statistical copilot via LangGraph with multi-provider and local fallback support. | Multi-agent autonomous workflow: Personal Tutor Agent + Evaluation Agent + Cadre Alignment Agent. |
| **Admin Analytics** | Officer completion overview, course assignment modal, question difficulty/failure analytics. | Cross-ministry predictive competency gap analysis and automated training budget allocation. |
| **Authentication** | JWT with PBKDF2 hashing, demo quick logins, role protection (`admin` vs `learner`). | Parichay / Jan Parichay single sign-on (SSO) integration with official Government of India NIC gateway. |

---

*This document is maintained as the authoritative reference for agents and engineers working on the iGOT Karmayogi platform.*
