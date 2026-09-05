# CONTEXT.md — AI-Enabled Skill Intelligence & Learning Platform

**Status:** Living document — Phase 0
**Last updated:** 2026-09-05

> This document is project memory and a feature blueprint, not a technical spec. It exists so anyone — a teammate, Antigravity, or another AI coding agent — can quickly understand what we're building, what's confirmed, and what's intentionally out of scope for now. Implementation details (schemas, endpoints, component structure) are decided during development, not here.

---

## 1. Project Overview

We're building an AI-enabled Skill Intelligence and Learning Platform for government employees — initially officials in India's Official Statistical System — in the spirit of platforms like iGOT Karmayogi, Coursera, and Khan Academy.

Learners get structured, trackable professional training: browse and search a course catalogue, work through courses with videos/lessons/labs, take assessments, and track their own progress and skills growth. Administrators manage the catalogue, assign courses, and monitor learner progress. Over time, the platform grows into a more AI-driven experience (personalized recommendations, an AI tutor, generated content) — but Phase 0 is about getting the core learning-platform experience right first.

---

## 2. Project Goals

- Give government employees a modern, trustworthy place to complete required and self-directed training.
- Give administrators visibility into who's learning what, and where they're struggling.
- Establish a clean, modular foundation that can be extended with real AI capabilities in later phases without a rewrite.
- Validate the AI-agent stack (LangGraph + LangChain) early with a small, real feature, rather than bolting AI on later.

**Phase 0's goal specifically:** ship the full non-AI learning-platform experience (auth, onboarding, browsing, courses, assessments, progress, basic admin) plus one minimal AI Assistant feature, using mock data wherever a real backend/integration doesn't exist yet.

---

## 3. Phase 0 Scope

Everything below is confirmed Phase 0. None of it is optional or deferred.

1. **Login & Signup** — government/work email, password, forgot/reset password, multilingual UI.
2. **Entry / Landing Page** — introduces the platform, its features, and what it can do (including a preview of content-generation capabilities), with real or realistic imagery/examples, not placeholders.
3. **First-Time Onboarding** — collects personal info, designation/job role/department, responsibilities, experience, prior training, required competencies, current assignment. Feeds the dashboard and future personalization.
4. **Main Dashboard** — Continue Learning, Today's Goals, Learning Streak, Recommended/Suggested learning, Current Course Progress, Recently Explored Courses, Learning History, Trending Courses, Future Planned Courses.
5. **My Learning** — In Progress, Completed, Skills and Progress, Practice, organized into roughly 3–4 tabs/sections (exact layout decided during implementation).
6. **Navigation** — Explore, My Learning, Search, Profile, plus anything else the Miro flow implies is needed.
7. **User Profile** — profile dropdown, personal info, onboarding info (editable), profile picture, language settings, appearance/dark mode.
8. **Search** — search bar, trending/field-related searches, recent search history, recently viewed courses, filters (duration, field/topic, level), sorting.
9. **Course Page & Learning Experience** — overview, start/resume, instructor/organization, duration, content counts (videos/tests/labs/other), difficulty, expandable modules, skills gained; a course-player view with a module/content sidebar, current content, and progress.
10. **Assessments** — MCQ-based, correctness-based results, basic result/progress handling.
11. **Progress & Analytics** — overall and module progress, quiz/test scores, learning hours, skills gained and skill progress, weak concepts, revision pointers.
12. **Admin Dashboard** — view/enroll users, assign courses, view detailed user progress, create/manage courses and assessments, course analytics, easy/difficult question identification, where users struggle.
13. **AI Assistant** — a minimal, single-turn "Ask AI" feature (see [Section 7](#7-ai-assistant)).

---

## 4. User Roles

- **Learner / Government Employee** — registers, onboards, browses/searches, takes courses and assessments, tracks their own progress, manages their profile.
- **Administrator** — everything above (assumed additive, not exclusive) plus the Admin Dashboard capabilities in Section 3.12.

No other roles exist in Phase 0. This document does not assign features to individual developers — that split happens later, by the team, once the codebase exists.

---

## 5. Overall User Journey

Based on the team's Miro board (`LMS Userflow`). Miro is the reference for *how* users move; the feature list above remains the authority for *what* must exist — if Miro doesn't explicitly show something from Section 3, it's still in scope.

**First-time user:**
`Entry` (About Platform / Explore Courses / How it Works) → `Login & Register` → `Register` (Basic Info → Create Account) → `Onboard` (Profile Setup → Personal Info → Education/Workex/Previous Training → Designation/Department/Job Role → Current Assignment/Areas of Interest → Save Profile) → `Home`.

**Returning user:**
`Entry` → `Login & Register` → `Existing User` (Credentials → Authenticate) → `Home` directly (onboarding isn't expected to re-run on every login — see [Section 13](#13-project-decisions)).

**Discovery / browsing:**
`Home` → `Discover`, which branches into `Search`, `Categories` (Popular, New), and `External Training` (Course List → Filter → Course Page). All roads lead to a `Course Page`.

**Learning journey:**
`Course Page` → `Learn` (Course → Module → Lesson → Learning Content → Activity) → `Assess` (Instructions → Questions → Submit → Results → Pass/Fail) → `Analytics` (Learning Progress → Course Completion → Assessment Performance → Competency Profile → Certificates).

**Home dashboard** fans out into its own sections (Recommended/Suggested, Continue Learning/Recently Accessed, My Learning/Progress, Competencies/Analytics), which is where Section 3.4's dashboard items live.

**Admin journey (high level):** a separate admin entry point into the Admin Dashboard, from which an admin manages users/enrollment, courses, assessments, and views analytics. The Miro board doesn't detail this flow — it's built from the written requirements alone, kept simple for Phase 0.

---

## 6. Feature Blueprint

High-level description of each major area — what it does and why, not how it's built.

- **Login & Signup:** Lets employees get into the platform using their work identity. Government/work email keeps the user base scoped to intended employees; forgot/reset password is a baseline usability need. Multilingual UI matters because the user base spans different regions/languages.

- **Landing Page:** The public face of the platform for people who haven't logged in yet — sells the value of the platform and gives a taste of what's inside (including AI-driven content generation, positioned as a differentiator) before asking for a login.

- **Onboarding:** A one-time data-collection step that makes the rest of the platform relevant to the individual — job role, experience, and current training feed directly into what the dashboard recommends and how admins can filter/report on users.

- **Dashboard:** The learner's home base — a snapshot of where they left off, what's expected of them today, what's trending, and what's coming up, so they don't have to go hunting for it.

- **My Learning:** The learner's personal library — everything they've started, finished, or are actively building skills in.

- **Navigation:** Keeps the platform easy to move around regardless of where the learner currently is.

- **Profile:** Where a learner manages their own identity and preferences on the platform, and can revisit/edit what they gave at onboarding.

- **Search:** The main way learners find something new to learn, beyond what the dashboard surfaces for them.

- **Course Page & Learning Experience:** The core "product" of the platform — a modern, Coursera-like course browsing and consumption experience learners will spend most of their time in.

- **Assessments:** Validates that learning actually happened, and produces the data the progress/analytics features depend on.

- **Progress & Analytics:** Gives the learner (and eventually the admin) a clear picture of growth, gaps, and what to revisit.

- **Admin Dashboard:** Gives whoever runs the platform the ability to manage content and track outcomes across the whole user base, not just one learner at a time.

- **AI Assistant:** See [Section 7](#7-ai-assistant).

---

## 7. AI Assistant

The AI Assistant is intentionally part of Phase 0 — not because the product needs a fully-fledged AI tutor yet, but to prove out the LangGraph + LangChain integration path before more advanced AI work is built on top of it later.

**Phase 0 version (this is what gets built now):**
- A simple "Ask AI" widget, available from the dashboard and course pages.
- Single-turn interaction — no multi-turn conversation memory.
- Built as a single LangGraph node/graph, using LangChain for the LLM call.
- No retrieval/RAG over course content, no tool use, no personalization, no awareness of the learner's own progress or enrollment.

**Explicitly future phase (not built now):**
- RAG-based, course-grounded tutoring.
- Long-term memory across sessions.
- Complex agentic workflows and tool use.
- Adaptive learning and advanced personalization.
- AI-generated courses, content, and assessments.
- Advanced, ML-driven recommendations.

The distinction matters: Phase 0 validates that the AI-agent plumbing works end-to-end; it is deliberately not trying to be a smart assistant yet.

---

## 8. High-Level Data / Information Model

The kinds of information the system needs to represent — not a schema, just the shape of the domain:

- **User** — identity, credentials, role (Learner/Administrator).
- **Profile / Onboarding Info** — personal info, designation, department, job role, responsibilities, experience, current assignment, language/appearance preferences.
- **Department / Role reference data** — supports onboarding and admin filtering.
- **Course** — title, description, instructor/organization, duration, difficulty, content structure, source (internal vs. external training).
- **Module / Lesson / Content** — the structure within a course.
- **Enrollment** — a user's relationship to a course (started, in progress, completed).
- **Progress** — position and completion within an enrollment, at the module/lesson level.
- **Assessment / Question** — MCQ tests tied to a course.
- **Assessment Result / Attempt** — a learner's submitted attempt, score, pass/fail.
- **Skill** — a named competency, linked to courses and to users who've gained it.
- **Learning History** — what a learner has viewed or engaged with over time.
- **Search History** — a learner's recent searches.
- **Today's Goal / Learning Streak** — lightweight, computed rather than heavily modeled — a daily target and a consecutive-activity count.
- **Planned Courses** — courses queued up for a learner, whether self-planned or admin-assigned.
- **Course Assignment** — an admin assigning a course to a user or group (can reuse the Enrollment concept rather than needing something new).
- **Training History** — prior training reported at onboarding, plus training completed on-platform.
- **AI Assistant** — no persistent data is expected for the Phase 0 stub; if configuration (e.g. which LLM/provider) needs to live somewhere, it's simple app configuration, not a domain entity.

The exact fields, tables, and relationships are a development-time decision, not something this document locks in.

---

## 9. Technology Stack

**Confirmed — do not substitute without an explicit decision:**

| Layer | Technology |
|---|---|
| Frontend framework | Next.js |
| UI library | React |
| Component/design system | shadcn/ui |
| Backend framework | FastAPI |
| AI orchestration | LangGraph |
| AI/LLM tooling | LangChain |

Infrastructure specifics that aren't yet decided (database engine, ORM, hosting, exact session/auth mechanism) are left open and can be resolved at implementation time — they don't affect the framework-level decisions above.

---

## 10. Phase 0 vs. Future Phases

**Phase 0 (build now):** everything in [Section 3](#3-phase-0-scope), including the minimal AI Assistant stub. Real/production integrations that don't exist yet (SSO, external content sources, a real recommendation engine) are mocked behind simple interfaces so they can be swapped in later without reworking the features around them.

**Future phases (do not build now, but keep the door open for):**
- RAG-based AI tutor, grounded in course content.
- Long-term memory and agentic workflows for the AI Assistant.
- AI-generated courses, content, and assessments, including a content-generation pipeline.
- Advanced, ML-driven personalization and recommendations.
- Adaptive learning paths.
- Skill-gap analysis against a formal competency framework.
- Predictive/concept-level analytics (beyond the simple weak-concept flagging in Phase 0).
- Real government SSO/identity integration.
- Deeper government knowledge-base integrations.
- Advanced admin intelligence (auto-flagging struggling learners, AI-assisted content authoring).
- Proctoring.

If something isn't explicitly listed as Phase 0 in Section 3, treat it as future scope — but that only applies to genuinely new capabilities, not to anything already named as a Phase 0 feature.

---

## 11. Out of Scope for Phase 0

Simplified Phase 0 versions exist for these — this list is about what's *not* built yet, not what's missing entirely:

- Any ML/AI-driven personalization, recommendation, or question generation (Phase 0 uses static/curated lists and a single-turn, ungrounded AI Assistant).
- Skill-gap analysis against a formal competency framework (Phase 0: raw score/completion aggregation only).
- Real SSO/government identity integration (Phase 0: standard email/password behind a swappable interface).
- Adaptive or cross-course practice (Phase 0: simple per-lesson practice/activity only).
- Certificate verification infrastructure (Phase 0: a static certificate record).
- Advanced admin intelligence or AI-assisted authoring (Phase 0: basic CRUD and manual review).
- Full translation of learning content itself (Phase 0: UI-chrome multilingual support only; course content stays single-language for now).
- Proctoring of any kind.

---

## 12. Current Project Status

- **Planning:** Complete
- **Miro flow:** Complete
- **CONTEXT.md:** Complete
- **Project foundation / initial commit:** Not started
- **Authentication:** Not started
- **Landing page:** Not started
- **Onboarding:** Not started
- **Dashboard:** Not started
- **My Learning:** Not started
- **Navigation:** Not started
- **Profile:** Not started
- **Search:** Not started
- **Course page & learning experience:** Not started
- **Assessments:** Not started
- **Progress & analytics:** Not started
- **Admin dashboard:** Not started
- **AI Assistant:** Not started

Update this list as work actually progresses — don't mark something complete until it is.

---

## 13. Project Decisions

- **Phase 0 scope is fixed** as listed in [Section 3](#3-phase-0-scope); it is the written-requirements baseline and takes precedence over the Miro board where the two disagree on *what* must exist (Miro governs *how* users move, per [Section 5](#5-overall-user-journey)).
- **Technology stack is confirmed**: Next.js + React + shadcn/ui, FastAPI, LangGraph + LangChain (see [Section 9](#9-technology-stack)).
- **AI Assistant is in Phase 0, deliberately minimal** — single-turn, no memory, no RAG — to validate the LangGraph/LangChain integration early (see [Section 7](#7-ai-assistant)).
- **Architecture will be kept modular** (feature/domain-based, on both frontend and backend) so that once the initial project foundation exists, multiple developers can pick up different feature areas with minimal overlap. This document does not decide who builds what.
- **Assumption (not yet confirmed):** onboarding runs once, on first login, rather than re-appearing on every login, despite the Miro board drawing both the login and register branches into `Onboard`. Flag this for confirmation before building the post-login redirect logic.
- **Assumption:** Administrators retain Learner capabilities (can also take courses) unless the team decides otherwise.

---

## 14. Change Log

### 2026-09-05
- **Change:** Initial creation of `CONTEXT.md` from the written Phase 0 requirements and the Miro `LMS Userflow` board.
- **Reason:** Establish a concise, readable source of truth for Phase 0 before implementation begins, without over-specifying implementation details.
- **Impact:** None yet — first version of the document.
