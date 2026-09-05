# CONTEXT.md — AI-Enabled Skill Intelligence & Learning Platform

**Status:** Living document — Phase 0 definition
**Last updated:** 2026-09-05
**Audience:** Antigravity (coding agent) for initial project foundation, and the four developers who will build Phase 0 features afterward.

> **Read this document in full before writing or generating any code.** It is the single source of truth for what the product is, what Phase 0 contains, what it explicitly does not contain, the user flow, the data model, and the architecture the initial commit must establish.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Phase Structure](#2-phase-structure)
3. [Purpose of This Document](#3-purpose-of-this-document)
4. [Miro User Flow (Source of Truth)](#4-miro-user-flow-source-of-truth)
5. [Phase 0 Functional Requirements](#5-phase-0-functional-requirements)
6. [Main Dashboard (HOME)](#6-main-dashboard-home)
7. [My Learning](#7-my-learning)
8. [Navigation](#8-navigation)
9. [User Profile and Settings](#9-user-profile-and-settings)
10. [Search and Discovery](#10-search-and-discovery)
11. [Course Page](#11-course-page)
12. [Course Learning Experience](#12-course-learning-experience)
13. [Assessments](#13-assessments)
14. [Progress and Analytics](#14-progress-and-analytics)
15. [Admin Dashboard](#15-admin-dashboard)
16. [User Roles](#16-user-roles)
17. [Domain / Data Model](#17-domain--data-model)
18. [High-Level Architecture](#18-high-level-architecture)
19. [Modularity for Future Parallel Development](#19-modularity-for-future-parallel-development)
20. [Initial Commit Requirements](#20-initial-commit-requirements)
21. [Feature Isolation](#21-feature-isolation)
22. [User Journeys](#22-user-journeys)
23. [UI/UX Principles](#23-uiux-principles)
24. [Multilingual Support](#24-multilingual-support)
25. [Mock Data](#25-mock-data)
26. [Future Phases](#26-future-phases)
27. [Phase 0 Out of Scope](#27-phase-0-out-of-scope)
28. [Antigravity Implementation Guidelines](#28-antigravity-implementation-guidelines)
29. [Project Progress](#29-project-progress)
30. [Change Log](#30-change-log)
31. [Decision Log](#31-decision-log)
32. [Requirements Traceability](#32-requirements-traceability)
33. [Assumptions and Open Questions](#33-assumptions-and-open-questions)
34. [Technology Decisions](#34-technology-decisions)

---

## 1. Project Overview

We are building an **AI-enabled Skill Intelligence and Learning Platform** for government employees — initially officials in India's Official Statistical System — inspired in parts by iGOT Karmayogi, Coursera, Khan Academy, and NPTEL/SWAYAM.

The platform's long-term vision includes competency mapping, skill-gap analysis, content generation pipeline in the four domains, personalized learning recommendations, AI-generated assessments, and an AI learning assistant. **None of the AI-driven capabilities are part of Phase 0** (except the minimal AI Assistant stub in [Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)). Phase 0 establishes the core learning-platform experience — authentication, onboarding, browsing, structured course consumption, simple MCQ assessments, progress tracking, and a basic admin surface — on top of which future AI capabilities can be layered without rework.

**Primary users:** government employees / officials (learners) who need structured, trackable professional training, and administrators who manage the course catalogue, assignments, and reporting.

---

## 2. Phase Structure

This is a multi-phase project. **We are currently defining and implementing Phase 0 only.**

- **Phase 0** — the functional learning platform described in this document: auth, onboarding, browse/search, course consumption, MCQ assessments, progress, profile, and a basic admin surface, all with mock or minimal-real data where production integrations don't yet exist.
- **Future Phases** — AI-driven capabilities and deeper government-system integrations (see [Section 26](#26-future-phases)). These are documented for context and extensibility only. They must not be implemented, scaffolded as "coming soon" features, or silently pulled into Phase 0 work.

If something in this document is ambiguous as to which bucket it belongs in, treat it as **Phase 0 only if explicitly listed as Phase 0 below**; otherwise treat it as future scope.

---

## 3. Purpose of This Document

This document gives Antigravity everything needed to generate the **initial project foundation commit** and gives the four developers everything needed to subsequently divide and build Phase 0 features independently. It intentionally does **not** assign features to individual developers — that division happens after the initial commit, by the team, and is out of scope for this document.

---

## 4. Miro User Flow (Source of Truth)

The product team supplied a Miro board (`LMS Userflow`) as the authoritative source for navigation and user-journey structure. The board was inspected directly (via screenshot, since the live Miro link could not be fetched by the agent producing this document). The flow below is transcribed faithfully from that board and takes precedence over the prose feature list in [Section 5](#5-phase-0-functional-requirements) wherever the two disagree — conflicts are called out explicitly.

### 4.1 Transcribed flow structure

```text
ENTRY
 ├─ About Platform
 ├─ Explore Courses
 ├─ How it Works
 └─ Login & Register ──▶ AUTH

AUTH
 ├─ Existing User ──▶ Credentials ──▶ Authenticate ──┐
 └─ Register ──▶ Basic Info ──▶ Create Account ──────┼──▶ ONBOARD
                                                       │
ONBOARD (vertical sub-flow)
 Profile Setup
   ▼
 Personal Info
   ▼
 Education / Workex / Previous Training
   ▼
 Designation / Department / Job Role
   ▼
 Current Assignment / Areas of Interest
   ▼
 Save Profile ──▶ HOME

HOME
 ├─ (dashboard sections, see 4.2) Recommended/Suggested Courses/Explore,
 │   Continue Learning/Recently Accessed, My Learning/Progress,
 │   Competencies/Analytics
 └─▶ Discover

Discover
 ├─ Search
 ├─ Categories ──▶ Popular, New
 └─ External Training ──▶ Course List, Filter, Course Page
 └─▶ Learn

Learn
 Course ▼ Module ▼ Lesson ▼ Learning Content ▼ Activity
   └─▶ Assess

Assess
 Instructions ▼ Questions ▼ Submit ▼ Results ▼ (pass | fail)
   └─▶ Analytics

Analytics
 Learning Progress ▼ Course Completion ▼ Assessment Performance ▼
 Competency Profile ▼ Certificates
```

### 4.2 Reading the diagram — screens and relationships

- **ENTRY** is the public landing page. It exposes three informational children (`About Platform`, `Explore Courses`, `How it Works`) that a visitor can view without authenticating, plus the `Login & Register` entry point into `AUTH`. `Explore Courses` from ENTRY implies **unauthenticated course browsing is part of Phase 0** (see conflict note below).
- **AUTH** branches into `Existing User` (login: Credentials → Authenticate) and `Register` (signup: Basic Info → Create Account). Both branches converge into `ONBOARD` on the diagram.
- **ONBOARD** is drawn as a single linear vertical sequence, not a branching wizard: Profile Setup → Personal Info → Education/Workex/Previous Training → Designation/Department/Job Role → Current Assignment/Areas of Interest → Save Profile. `Save Profile` is the exit point, leading to `HOME`.
- **HOME** is the main dashboard. The four boxes drawn beneath it (`Recommended/Suggested Courses/Explore`, `Continue Learning/Recently Accessed`, `My Learning/Progress`, `Competencies/Analytics`) are dashboard sections/cards reachable from HOME, not separate top-level flow states — they map directly to the dashboard sections in [Section 6](#6-main-dashboard-home).
- **Discover** is the browse/search hub, reached from HOME. It fans out into `Search`, `Categories` (→ `Popular`, `New`), and `External Training` (→ `Course List`, `Filter`, `Course Page`). `External Training` having its own `Course Page` suggests externally-sourced training content is modeled similarly to internal courses but is a distinct catalogue source — treat this as a data-source distinction, not a separate UI paradigm (see [Section 17](#17-domain--data-model) and [Section 32](#32-assumptions-and-open-questions)).
- **Learn** is the in-course experience: `Course → Module → Lesson → Learning Content → Activity`, a strictly nested hierarchy (Course contains Modules, Modules contain Lessons, Lessons contain Learning Content/Activity).
- **Assess** follows Learn: `Instructions → Questions → Submit → Results → (pass/fail)`.
- **Analytics** follows Assess and aggregates the learner's outcomes: `Learning Progress → Course Completion → Assessment Performance → Competency Profile → Certificates`. This is presented as a single downstream flow rather than a dashboard of independent widgets, implying these are best modeled as sequential facets of one "My Progress / Analytics" screen for Phase 0.

### 4.3 Conflicts between the Miro flow and the written requirements

| # | Conflict | Interpretation used in this document |
|---|---|---|
| 1 | Written requirements (§4.3 of the source brief) describe onboarding fields loosely ("potential information"); Miro draws a fixed, ordered 5-step sequence. | The Miro order is authoritative for the onboarding step sequence: Profile Setup → Personal Info → Education/Work Experience/Previous Training → Designation/Department/Job Role → Current Assignment/Areas of Interest → Save. See [Section 5.3](#53-first-time-signupvisualonboarding). |
| 2 | Miro shows **both** the login (`Authenticate`) branch and the register (`Create Account`) branch flowing into `ONBOARD`, which would mean returning/existing users re-enter onboarding on every login. | Interpreted as a diagramming simplification, not a literal requirement. **Assumption:** onboarding runs only once, on first login after account creation; existing users with a completed profile go `Authenticate → HOME` directly. Flagged as an open question in [Section 33](#33-assumptions-and-open-questions) — needs confirmation before the onboarding-skip logic is implemented. |
| 3 | ENTRY exposes `Explore Courses` directly, implying anonymous/unauthenticated browsing, while the written requirements frame login as the gateway to the whole product. | Phase 0 supports a limited **unauthenticated preview**: landing page + a read-only course catalogue browse (titles, overviews) without progress, enrollment, or content playback, which require authentication. This preserves both the Miro affordance and the login-gated learning experience. |
| 4 | Written requirements list `Practice` as part of My Learning; Miro does not show a distinct `Practice` node — the closest analog is `Activity` under `Learn`. | Treated as the same concept: Phase 0 "Practice" is the `Activity` step inside a lesson (simple, non-adaptive practice tied to the lesson just completed), not a separate top-level area. A standalone cross-course Practice hub is deferred to future phases. |
| 5 | Written requirements list a generic `Search` capability with filters/sorting; Miro nests `Search` under `Discover` alongside `Categories` and `External Training`, without depicting a separate global search bar accessible from every screen. | Phase 0 includes both: a persistent search entry point in primary navigation (per written requirements, [Section 8](#8-navigation)) and the richer `Discover → Search` experience with categories/filters as the destination screen. |
| 6 | Written requirements list `Today's Goals`, `Learning Streak`, `Recently Explored Courses`, `Learning History`, `Trending Courses`, and `Future Planned Courses` as explicit dashboard items; none of these six appear as boxes under Miro's `HOME` node, which shows only `Recommended/Suggested`, `Continue Learning/Recently Accessed`, `My Learning/Progress`, and `Competencies/Analytics`. | Per [Section 8, Rule](#5-phase-0-functional-requirements) of this document's governing principle — the written feature list is the source of truth for *what the system must provide*, Miro is the source of truth for *flow* — all six remain **Phase 0 requirements**. They are added to the `HOME` dashboard as additional sections beyond Miro's four boxes, each explicitly labeled **"written requirement — not shown in Miro"** rather than presented as Miro-derived. Lightweight, non-gamified Phase 0 implementations are defined in [Section 6](#6-main-dashboard-home). See also [Decision 007](#decision-007--dashboard-features-confirmed-from-written-requirements). |

---

## 5. Phase 0 Functional Requirements

### 5.1 Login and Signup

Maps to Miro `ENTRY → Login & Register → AUTH`.

**Phase 0 must include:**
- Login (existing user): email + password (`Credentials → Authenticate`).
- Signup (new user): government/work email + password + minimal basic info (`Basic Info → Create Account`).
- Forgot password / reset password flow.
- Logout.
- Auth states: unauthenticated, authenticating, authenticated, session-expired, error.
- Multilingual UI on all auth screens (see [Section 24](#24-multilingual-support)).

**Mocking strategy:** Real government SSO/identity infrastructure is not available yet. Phase 0 implements a standard email+password auth flow (real password hashing, real sessions/tokens) against the platform's own user store, with the **interface** shaped so a future SSO/government-IdP provider can be substituted without changing consuming code (i.e., auth calls go through a single auth-service abstraction, not scattered direct calls). Email verification and real email delivery are mocked/stubbed for Phase 0.

### 5.2 Entry / Landing Page

Maps to Miro `ENTRY`.

Must communicate what the platform is, who it's for, key benefits/features, and provide entry points into `About Platform`, `Explore Courses` (unauthenticated catalogue preview), `How it Works`, and `Login & Register`. Should read as a real product page, not a placeholder — use real (or realistically mocked) course previews rather than lorem ipsum.

### 5.3 First-Time Signup/Onboarding

Maps to Miro `ONBOARD` (see [Section 4.2](#42-reading-the-diagram--screens-and-relationships), conflict #1).

Ordered steps (Phase 0, per Miro):
1. **Profile Setup** — intro/start step.
2. **Personal Info** — name, contact details, etc.
3. **Education / Work Experience / Previous Training**.
4. **Designation / Department / Job Role**.
5. **Current Assignment / Areas of Interest**.
6. **Save Profile** → routes to `HOME`.

| Field group | Required? | Editable later? | Used for |
|---|---|---|---|
| Personal Info | Required | Yes, in Profile settings | Identity, display |
| Education/Workex/Previous Training | Required (can allow "none") | Yes | Profile, future recommendations |
| Designation/Department/Job Role | Required | Yes (may need admin approval in future — Phase 0: user-editable) | Profile, admin filtering, future personalization |
| Current Assignment/Areas of Interest | Optional | Yes | Profile, future personalization |

Do not build any recommendation logic on top of this data in Phase 0 — collect and store it only.

### 5.4 Dashboard, My Learning, Navigation, Profile, Search, Course Page, Learning Experience, Assessments, Progress/Analytics, Admin

See dedicated sections 6–15 below — each corresponds directly to a portion of the Miro flow.

### 5.5 AI Assistant (Phase 0 stub — added by team decision, not shown in Miro)

**This is an explicit addition to Phase 0 scope, made by team decision on 2026-09-05 (see [Decision 006](#decision-006--phase-0-ai-assistant-stub)), not derived from the Miro flow.** It exists to prove out the **LangGraph + LangChain** integration end-to-end before real AI features are built in future phases — it is intentionally minimal.

**What it is:**
- A single-turn "Ask AI" chat widget, available from `HOME` and the `Course Page` as a non-blocking, optional affordance (floating button or panel — not part of the primary navigation or the core Miro journey).
- User types a question; the backend runs one **LangGraph** graph with a single node that calls an LLM via **LangChain**'s chat-model wrapper; the answer is returned and shown in the widget.
- No conversation memory across turns, no retrieval/RAG over course content, no tool calls, no personalization, no grounding in the user's enrollment/progress data.

**What it explicitly is not (still future phase — see [Section 26](#26-future-phases) and [Section 27](#27-phase-0-out-of-scope)):**
- Not the AI tutor, not RAG-based, not adaptive, not aware of course content or user progress.
- Not integrated into the Learn/Assess flow — it is a standalone utility widget only.

**Data/backend:** new `agents/` FastAPI package ([Section 21](#21-feature-isolation)) exposing a single endpoint (e.g. `POST /agents/chat`) wrapping the LangGraph graph. No new persistent entities required — requests/responses are not stored in Phase 0.

**Mocking:** the underlying LLM provider/API key is configured via environment variables per [Section 25](#25-mock-data); if no key is configured, the widget shows a clear "AI assistant unavailable" state rather than failing silently.

---

## 6. Main Dashboard (HOME)

Maps to Miro `HOME` and its four child sections, **plus additional sections required by the written brief that Miro does not depict** (see [Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements), conflict #6, and [Decision 007](#decision-007--dashboard-features-confirmed-from-written-requirements)). All sections below are confirmed **Phase 0** — none are optional, deferred, or future-phase. Each row is labeled with whether it derives from the Miro board or from the written requirements.

| Section | Purpose | Data shown | Click destination | Data source (Phase 0) | Source | Empty / Loading / Error state | Phase |
|---|---|---|---|---|---|---|---|
| Continue Learning / Recently Accessed | Resume in-progress work | Last-opened course(s), % complete, current module/lesson | Course learning view, resumed at last position | `Enrollment` + `Progress` records | Miro (`HOME` child box) | "You haven't started a course yet" + CTA to Discover / skeleton cards / "Couldn't load recent activity" + retry | 0 |
| **Today's Goals** | Simple daily learning target and progress toward it | A single configurable/static daily target (e.g. minutes studied or lessons completed) plus today's progress against it | None — informational card (may link into My Learning) | Lightweight Phase 0 implementation: a static or simply-configurable per-user/platform target compared against today's `Progress` activity; **no new entity required** — see [Section 17](#17-domain--data-model) | **Written requirement — not shown in Miro** | "No goal set for today" (rare) / skeleton / retry | 0 |
| **Learning Streak** | Motivate consistent engagement | Current streak count (consecutive days with qualifying login/learning activity) | None — informational card | Lightweight Phase 0 implementation: a simple consecutive-day calculation over login or `Progress`-update timestamps; **no gamification system, badges, or leaderboards** — just the count | **Written requirement — not shown in Miro** | "Start today to begin your streak" / skeleton / retry | 0 |
| Recommended / Suggested Courses / Explore | Surface courses to start | Course cards (title, thumbnail, duration) | Course page | **Mocked**: curated/static list, not personalized ML output | Miro (`HOME` child box) | Fallback to trending/popular list / skeleton cards / falls back to Explore link | 0 (mocked; real personalization is Future) |
| **Current Course Progress** | At-a-glance progress on the course the learner is actively working through | % complete and current module/lesson for the most recent active enrollment | Course learning view | Same `Enrollment` + `Progress` data as Continue Learning, surfaced as its own explicitly-requested block | **Written requirement** — overlaps in substance with Miro's `Continue Learning/Recently Accessed` box, but kept as a distinct labeled section since it was separately and explicitly requested | Shares Continue Learning's empty/loading/error states | 0 |
| **Recently Explored Courses** | Quick return to courses recently *viewed* (not necessarily started/enrolled) | Last few viewed course cards | Course page | `LearningHistory` | **Written requirement — not shown in Miro** | "Nothing viewed yet" / skeleton / retry | 0 |
| **Learning History** | Fuller chronological record of past learning activity | List of viewed/started/completed courses over time | My Learning page, or the relevant course page | `LearningHistory`, `Enrollment` | **Written requirement — not shown in Miro** | "No history yet" / skeleton / retry | 0 |
| **Trending Courses** | Surface platform-wide popular courses | Course cards ranked by a simple popularity signal | Course page | Mocked/simple: a static curated "trending" list, or a simple enrollment-count ranking over the mock catalogue — **no real-time or ML-driven trending algorithm** | **Written requirement — not shown in Miro**; conceptually adjacent to Miro's `Discover → Categories → Popular`, but surfaced directly on the dashboard per the written brief | Fallback to Recommended list / skeleton / retry | 0 |
| **Future Planned Courses** | Show the learner what's queued up next | Simple list of planned/upcoming courses | Course page | `PlannedCourse`, populated from mock/seed data for Phase 0 (no admin-scheduling UI yet); the model is kept extensible for later self-service or admin-driven planning — see [Section 17](#17-domain--data-model) | **Written requirement — not shown in Miro** | "Nothing planned yet" / skeleton / retry | 0 |
| My Learning / Progress | Snapshot of overall learning | In-progress count, completed count, overall progress % | My Learning page | `Enrollment` + `Progress` aggregation | Miro (`HOME` child box) | "No courses yet" + CTA / skeleton / retry | 0 |
| Competencies / Analytics | Snapshot of skill/competency growth | Skills gained count, top skills | Progress/Analytics page | `UserSkill` records | Miro (`HOME` child box) | "Complete a course to see skills here" / skeleton / retry | 0 |

**On scope:** Today's Goals, Learning Streak, Trending Courses, and Future Planned Courses were previously (incorrectly) treated as optional/deferred in an earlier draft of this document because they don't appear in the Miro board. That was a drafting error, corrected per [Decision 007](#decision-007--dashboard-features-confirmed-from-written-requirements) — they are baseline Phase 0 scope from the written requirements, implemented with deliberately lightweight, non-sophisticated logic rather than being cut or deferred.

---

## 7. My Learning

Maps to Miro `HOME → My Learning/Progress`, and conceptually to `Learn`.

- **In Progress:** enrolled courses with completion %, current module/lesson, Resume action → deep-links into `Learn`.
- **Completed:** finished courses with completion date; certificate link if issued (see [Section 14](#14-progress-and-analytics)).
- **Skills and Progress:** skills gained (from `CourseSkill`/`UserSkill`), simple progress bars per skill (count of courses contributing, not an adaptive skill score).
- **Practice:** per [Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements) conflict #4, Phase 0 practice = the `Activity` step within a lesson. No standalone cross-course practice hub in Phase 0.

---

## 8. Navigation

Primary navigation (persistent, per written requirements + Miro's top-level nodes):

- **Discover** (Explore/browse — Miro `Discover`)
- **My Learning** (Miro `My Learning/Progress`)
- **Search** (global entry point into `Discover → Search`)
- **Profile** (avatar/menu)
- Role-based: **Admin** entry visible only to Administrator role.

Behavior:
- Active state reflects current top-level section.
- Profile is a dropdown: Profile, Settings, Logout.
- Responsive: collapses to a hamburger/menu on narrow viewports; Search may collapse to an icon that expands.
- Role-based visibility: Admin link hidden entirely for Learner role, not just disabled.

---

## 9. User Profile and Settings

Maps to Miro's onboarding data resurfacing, plus `HOME`-level access.

- **Personal Information** — editable, sourced from onboarding.
- **Professional/Onboarding Information** — Education/Workex, Designation/Department/Job Role, Current Assignment/Areas of Interest — editable by the user in Phase 0 (no admin-approval workflow yet).
- **Settings** — Language selection, Appearance (light/dark), profile picture, notification preferences (if trivial to add; otherwise defer).

| Data | Editable by | System-generated? |
|---|---|---|
| Personal Info, Professional Info | User | No |
| Language/Appearance preference | User | No |
| Enrollment/Progress/Assessment records | Nobody (derived) | Yes |
| Role assignment | Admin only | No |

---

## 10. Search and Discovery

Maps to Miro `Discover → Search / Categories (Popular, New) / External Training (Course List, Filter, Course Page)`.

- **Search:** keyword search over course titles/descriptions. Recent searches and recently viewed courses stored per user.
- **Categories:** `Popular` and `New` are the two Phase 0 category views (matches Miro exactly — do not invent additional category types beyond what the mock catalogue supports).
- **External Training:** a distinct catalogue source (possibly externally sourced/curated courses) that still resolves to a `Course Page`, filterable via `Filter`, listed via `Course List`. Phase 0 models this as courses with a `source` field (`internal` | `external`) rather than a parallel data model — see [Section 17](#17-domain--data-model).
- **Filters:** duration, topic/field, difficulty — apply to both internal and external course lists.

Search result structure: paginated list of course cards (title, source badge, duration, difficulty, thumbnail) with filter/sort controls persisted in the URL/query state.

---

## 11. Course Page

Maps to Miro `Discover → ... → Course Page` and the entry into `Learn → Course`.

Must show: title, overview, Start/Resume button, instructor, organization/creator, duration, counts of videos/tests/labs/other content types, difficulty, expandable module list (with descriptions), and skills gained. State must reflect current enrollment/progress if any (Start vs. Resume).

---

## 12. Course Learning Experience

Maps to Miro `Learn: Course → Module → Lesson → Learning Content → Activity`.

Structure (Coursera-inspired, per written brief, validated against Miro's strict nesting):
- Persistent course sidebar listing Modules, expandable to Lessons.
- Main content area renders the current Lesson's Learning Content.
- `Activity` = the lightweight in-lesson practice step (see [Section 7](#7-my-learning)).
- Progress indicator per module and overall course.
- Completing the last lesson/activity in a course transitions into `Assess` (Miro's next stage) if the course has an associated assessment.

State transitions (validated against Miro, supersedes the brief's example sequence which is otherwise consistent):
```text
Discover → Course Page → Start/Resume → Learn(Course→Module→Lesson→Content→Activity) → Assess → Analytics
```

---

## 13. Assessments

Maps to Miro `Assess: Instructions → Questions → Submit → Results → (pass/fail)`.

Phase 0 scope: simple MCQ assessments only.
- Instructions screen before starting.
- Question-by-question or single-page MCQ presentation (implementation detail, not mandated by Miro — pick single-page for Phase 0 simplicity unless a developer decision changes this).
- Submission computes score against stored correct answers.
- Results screen shows score, correct/incorrect breakdown, and a pass/fail outcome against a stored passing threshold.
- One attempt is recorded per submission (`AssessmentAttempt`). **Retry policy for Phase 0:** allow unlimited retakes with the latest attempt determining progress-counted status, unless a stricter policy is decided (open question, [Section 33](#33-assumptions-and-open-questions)).
- Score persists and updates the course's progress record.
- Admins can view aggregate assessment data ([Section 15](#15-admin-dashboard)).

Not in Phase 0: adaptive question selection, AI-generated questions, proctoring.

---

## 14. Progress and Analytics

Maps to Miro `Analytics: Learning Progress → Course Completion → Assessment Performance → Competency Profile → Certificates`.

**Directly calculable in Phase 0** (deterministic aggregation of stored records, no ML):
- Overall course progress, module progress (from `Progress`/`Enrollment`).
- Quiz/test scores (from `AssessmentAttempt`).
- Learning hours (sum of time-tracked activity, if tracked; otherwise estimated from lesson durations — implementation detail).
- Skills gained (from completed `CourseSkill` → `UserSkill`).
- Course completion status and certificate issuance (simple: certificate = completion record + static template, no verification infrastructure).

**Requires future AI/analytics infrastructure (do NOT implement in Phase 0):**
- Weak-concept / concept-level mastery detection.
- Skill-gap analysis relative to a competency framework.
- Predictive or adaptive analytics.

---

## 15. Admin Dashboard

Maps to written requirements; Miro does not depict a separate admin flow, so this section is built from the brief alone, kept intentionally minimal for Phase 0.

Phase 0 admin capabilities:
- **User Management:** view users, view enrollment and progress per user.
- **Course Assignment:** assign a course to a user/group; view participation.
- **Course Management:** create/edit/manage courses and modules (basic CRUD; no rich authoring tools).
- **Assessment Management:** create/edit questions and assessments (basic CRUD).
- **Analytics:** course-level completion, per-question performance (basic correct/incorrect rates), aggregate user progress.

Not in Phase 0: advanced admin intelligence, automated flagging of struggling learners, AI-assisted content authoring.

---

## 16. User Roles

- **Learner / Government Employee:** register/login, onboarding, browse/search, start/resume courses, take assessments, view own progress, manage own profile.
- **Administrator:** all Admin Dashboard capabilities ([Section 15](#15-admin-dashboard)). Whether Administrator also retains Learner capabilities (i.e., can an admin also take courses) is an open question ([Section 33](#33-assumptions-and-open-questions)) — default assumption: yes, roles are additive, not exclusive.

Miro does not show additional roles; none are added beyond these two for Phase 0.

---

## 17. Domain / Data Model

Entities actually required for Phase 0, with purpose, key fields, relationships, and future relevance. Entities from the original brainstormed list that are **not** included are noted at the end with rationale.

| Entity | Purpose | Key fields | Relationships | Phase 0? |
|---|---|---|---|---|
| `User` | Auth identity | id, email, passwordHash, role, createdAt | 1—1 `UserProfile` | Yes |
| `UserProfile` | Onboarding + profile data | personalInfo, educationWorkex, designation, department, jobRole, currentAssignment, areasOfInterest, languagePref, appearancePref | belongs to `User` | Yes |
| `Department` | Org grouping | id, name | referenced by `UserProfile` | Yes (simple lookup table) |
| `Course` | Learning unit | id, title, overview, instructor, org, duration, difficulty, source (`internal`\|`external`), skillIds | has many `Module`; has many `CourseSkill` | Yes |
| `Module` | Course subdivision | id, courseId, title, description, order | has many `Lesson` | Yes |
| `Lesson` | Content unit | id, moduleId, title, content, activity, order | belongs to `Module` | Yes |
| `Enrollment` | User↔Course link | id, userId, courseId, startedAt, status | belongs to `User`, `Course` | Yes |
| `Progress` | Tracks position/completion | id, enrollmentId, moduleId, lessonId, percentComplete, updatedAt | belongs to `Enrollment` | Yes |
| `Assessment` | MCQ test tied to a course | id, courseId, passThreshold | has many `Question` | Yes |
| `Question` | MCQ item | id, assessmentId, text, options, correctOptionId | belongs to `Assessment` | Yes |
| `AssessmentAttempt` | A submitted attempt | id, userId, assessmentId, answers, score, passed, submittedAt | belongs to `User`, `Assessment` | Yes |
| `Skill` | Named competency/skill | id, name | referenced by `CourseSkill`, `UserSkill` | Yes |
| `CourseSkill` | Course↔Skill link | courseId, skillId | join table | Yes |
| `UserSkill` | User's acquired skills | userId, skillId, acquiredAt, sourceCourseId | join table | Yes |
| `SearchHistory` | Recent searches | userId, query, searchedAt | belongs to `User` | Yes (simple) |
| `LearningHistory` | Recently viewed courses (backs both "Recently Explored Courses" and "Learning History" dashboard sections, [Section 6](#6-main-dashboard-home)) | userId, courseId, viewedAt | belongs to `User`, `Course` | Yes (simple) |
| `PlannedCourse` | Backs the "Future Planned Courses" dashboard section ([Section 6](#6-main-dashboard-home)) — a course queued up for a learner | id, userId, courseId, plannedFor (optional date), source (`self`\|`admin`), createdAt | belongs to `User`, references `Course` | Yes — Phase 0 populates this via mock/seed data (no self-planning or admin-scheduling UI yet); the shape is kept extensible so those UIs can write to the same table later without a schema change |

**Today's Goals and Learning Streak require no new entities in Phase 0.** Learning Streak is computed on read from existing `Progress`/`Enrollment` update timestamps (or a last-activity timestamp on `User`) via a simple consecutive-day calculation — there is no dedicated streak table. Today's Goals compares a single configurable target (a static value, or a simple per-user/platform config field) against the current day's `Progress` activity — again, no new entity, just a computed comparison. **Course Assignment** (admin assigning a course to a user, [Section 15](#15-admin-dashboard)) also requires no new entity — it is simply an `Enrollment` record created by an admin rather than by the learner themself.

**Deliberately excluded from Phase 0** (from the original brainstormed entity list):
- `Competency` (as a formal framework/taxonomy distinct from `Skill`) — future phase; Phase 0 uses the simpler `Skill` entity only.
- `TrainingHistory` (as a distinct entity from `Enrollment`/`Progress`/`UserProfile.educationWorkex`) — Phase 0 covers this via `UserProfile` (prior training reported at onboarding) and `Enrollment`/`Progress` (training taken on-platform); a unified historical ledger is future scope if the two need reconciling.

---

## 18. High-Level Architecture

Priorities (in order): simplicity, maintainability, separation of concerns, easy future extension, easy parallel development post-initial-commit, minimal merge conflicts, avoiding over-engineering.

Stack is confirmed — see [Section 34](#34-technology-decisions): **Next.js + React + shadcn/ui** on the frontend, **FastAPI** on the backend, **LangGraph + LangChain** used for the minimal Phase 0 AI Assistant stub ([Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)) and reserved for the larger AI-agent capabilities that otherwise belong to future phases (see [Section 26](#26-future-phases)).

**Frontend (Next.js + React + shadcn/ui):** organized by **feature modules** using Next.js's App Router, each feature owning its own route segment(s), components, and API-client calls. shadcn/ui components are the primitive building blocks (button, card, input, dialog, dropdown, form, etc.) — install/generate only the primitives a feature actually needs rather than pre-generating the whole library. A thin shared layer provides the design tokens/theme, the root layout shell, the auth/session context, and the i18n mechanism only.

**Backend (FastAPI):** a modular API exposing REST endpoints grouped by domain (auth, onboarding, courses, learning, assessments, profile, search, admin) using FastAPI's `APIRouter` per domain, each mounted onto the main app with a single `include_router(...)` line. Each domain's router, Pydantic schemas, business logic, and data-access code live together in their own package; a thin shared layer provides the DB session dependency, auth dependency/middleware, and common error/response models only.

**AI-agent layer (LangGraph + LangChain):** the bulk of the AI capability — the AI tutor, RAG-based learning assistant, AI-generated assessments/content, and personalized-recommendation logic in [Section 26](#26-future-phases) — remains future-phase and is **not** built in Phase 0. However, by team decision ([Decision 006](#decision-006--phase-0-ai-assistant-stub)), Phase 0 **does** include one minimal stub — the AI Assistant single-turn chat widget ([Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)) — implemented as a single **LangGraph** graph calling an LLM via **LangChain**, exposed through the FastAPI `agents/` domain package. This is deliberately the smallest possible slice of the AI-agent layer: it exists to validate the integration path, not to deliver real AI functionality. Everything beyond it (memory, retrieval/RAG, tool use, personalization) stays future-phase and must not be added to this package without a corresponding scope decision.

**Data layer:** a single relational database modeling the entities in [Section 17](#17-domain--data-model), accessed through domain-scoped data-access code (e.g., SQLAlchemy models/queries per domain package), with FastAPI's dependency-injection used for the DB session. No feature reaches into another feature's tables directly; cross-feature reads go through that feature's exposed service functions.

**Auth boundary:** all authentication/authorization logic sits behind a single auth-service abstraction (see [Section 5.1](#51-login-and-signup)), implemented as a FastAPI dependency, so the mocked email/password implementation can be swapped for a government SSO/IdP later without touching consuming routers.

**Shared components:** design tokens/theme (Tailwind config feeding shadcn/ui), root layout shell (nav + content area), the shadcn/ui primitive set, the auth/session context/provider, and the i18n mechanism. Nothing feature-specific belongs here.

**Routing:** Next.js App Router top-level route segments correspond to the Miro top-level nodes (Entry, Auth, Onboard, Home, Discover, Course, Learn, Assess, Analytics/Progress, Profile, Admin), each owned by its feature module; FastAPI top-level routers mirror the same domains on the backend.

**State management:** local/feature-scoped React state (and server state via Next.js data-fetching/server components where appropriate) by default; a small amount of global client state for auth/session and language/theme preference only. Avoid a single global store that every feature must edit.

---

## 19. Modularity for Future Parallel Development

Design goal: **after the initial commit, four developers can divide Phase 0 features among themselves with minimal restructuring and minimal merge conflicts.**

To support this:
- Feature-based modules (frontend and backend) as the primary organizing unit — see [Section 21](#21-feature-isolation).
- Each feature owns its own components/pages, its own API-client or route handlers, and its own local state.
- Shared components/types/utilities are kept intentionally small and stable so they rarely need editing once established.
- No feature should need to edit another feature's files for normal work.
- Central files (root app/router, root server entry) should only ever need a **one-line registration** addition per new feature (e.g., adding a route/module to a list), not internal edits.
- Shared type/interface definitions for cross-feature contracts (e.g., the shape of a `Course` object) live in one shared location so features agree on data shapes without importing each other's internals.

This document does not assign the eight-ish feature areas (auth, onboarding, dashboard, discover/search, course/learn, assessments, profile, admin) to specific developers — that division is a team decision made after the initial commit.

---

## 20. Initial Commit Requirements

This is what Antigravity should build **first**, before any Phase 0 feature is implemented. The initial commit establishes the common foundation only.

Must include:
- Repository/project setup: a Next.js (App Router) frontend project with shadcn/ui initialized, and a FastAPI backend project — per [Section 34](#34-technology-decisions).
- Frontend scaffold with the feature-module folder structure ([Section 21](#21-feature-isolation)) pre-created (even if most feature folders start empty/stubbed), and shadcn/ui set up with a base theme/design tokens.
- Backend scaffold with the same domain-module structure pre-created ([Section 21](#21-feature-isolation)), including the `agents/` package with the **LangGraph + LangChain** dependencies added and the minimal Phase 0 AI Assistant stub graph/endpoint wired per [Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro) — this is the one exception to "foundation only," since the point of building it now is to prove the integration works before other features are layered on.
- Base application shell: layout, primary navigation skeleton ([Section 8](#8-navigation)), routing skeleton covering the top-level Miro nodes.
- Global styles/theme and a small set of shared UI primitives.
- Shared types/interfaces for the core entities in [Section 17](#17-domain--data-model).
- Configuration and environment-variable structure (including placeholders for the future-swappable auth provider).
- Database foundation: schema/migration setup for the Phase 0 entities (structure only — seed/mock data can follow per feature).
- Auth interface/placeholder: the auth-service abstraction described in [Section 18](#18-high-level-architecture), with a working mock email/password implementation behind it.
- API structure: route/module registration pattern that later features plug into with a one-line addition.
- Loading/error-handling foundations (shared UI states, shared API-error shape).
- Basic responsive layout foundation.
- `README.md` (setup/run instructions) and this `CONTEXT.md`.

**Must not** attempt to implement full Phase 0 features (e.g., do not build the entire onboarding wizard or course player) — only the shell/foundation each feature will be built into.

**Critical constraint:** no feature should require editing the same central `App`/root page/root server/root routes file beyond a single registration line. If a proposed structure would force multiple developers into the same file for unrelated features, it violates this requirement and should be restructured.

---

## 21. Feature Isolation

Folder shape for the confirmed stack (Next.js/React/shadcn frontend, FastAPI backend):

**Frontend (Next.js App Router):**
```text
app/
├── (auth)/            # Login, Register, Forgot/Reset Password
├── onboarding/         # Profile Setup wizard (5-step sequence, §5.3)
├── (dashboard)/home/     # HOME + its four sections
├── discover/               # Search, Categories, External Training
├── courses/[courseId]/      # Course Page
├── learn/[courseId]/          # Learn: Course/Module/Lesson/Content/Activity
├── assess/[assessmentId]/       # Assess: Instructions/Questions/Submit/Results
├── progress/                      # Analytics: Progress/Completion/Performance/Competency/Certificates
├── profile/                         # Profile + Settings
└── admin/                             # Admin Dashboard

components/
├── ui/                # shadcn/ui generated primitives (shared, small, stable)
└── shared/             # layout shell, nav, other genuinely cross-feature components

lib/
├── auth/                # auth/session context + client-side auth helpers
├── i18n/                 # i18n mechanism + resources
└── types/                  # shared cross-feature type definitions (e.g. Course, User)
```

**Backend (FastAPI):**
```text
app/
├── main.py               # app factory; one include_router(...) call per domain
├── core/                  # DB session dependency, auth dependency, shared error/response models, config
├── auth/                    # router + schemas + service (login/register/reset/logout)
├── onboarding/                # router + schemas + service
├── dashboard/                   # router + schemas + service
├── discover/                      # router + schemas + service (search, categories, external training)
├── courses/                         # router + schemas + service
├── learning/                          # router + schemas + service (progress tracking)
├── assessments/                         # router + schemas + service
├── profile/                               # router + schemas + service
├── admin/                                   # router + schemas + service
└── agents/                                    # Phase 0 AI Assistant stub (LangGraph + LangChain, §5.5) — everything beyond this stays future-phase (§26)
```

Each feature/domain package is expected to contain its own pages/components (frontend) or router/schemas/service (backend), and any feature-local state/types. Cross-feature contracts (e.g., what a `Course` object looks like) live in `lib/types/` (frontend) and `core/` shared schemas (backend) so features don't import each other's internals. `main.py` and the root Next.js layout should only ever need a one-line addition per new feature, never internal edits.

---

## 22. User Journeys

Validated against Miro (Section 4); matches the written brief closely with the adjustments noted in [Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements).

- **New user:** Entry → Login & Register → Register → Onboard (5 steps) → Home.
- **Returning user:** Entry → Login & Register → Existing User → Authenticate → Home *(assumption: onboarding skipped — see conflict #2)*.
- **Discovery:** Home → Discover → Search / Categories (Popular, New) / External Training → Course Page.
- **Learning:** Course Page → Start/Resume → Learn (Course→Module→Lesson→Content→Activity) → Assess (Instructions→Questions→Submit→Results→pass/fail) → Analytics.
- **Profile:** Home → Profile → Settings → edit Personal/Professional Info.
- **Administrator:** Admin login → Admin Dashboard → Users / Course Assignment / Course Management / Assessment Management / Analytics.

---

## 23. UI/UX Principles

The platform should feel professional, modern, trustworthy, government-appropriate, accessible, and learning-focused — not a generic CRUD admin panel. It may draw visual/interaction inspiration from Coursera/Khan Academy/iGOT but should establish its own visual identity (see the frontend-design guidance used at implementation time).

Required considerations throughout: responsive layouts, accessibility (semantic markup, keyboard navigation, sufficient contrast), and explicit loading/empty/error/success states and form validation feedback for every data-driven screen (as itemized per dashboard section in [Section 6](#6-main-dashboard-home) and expected elsewhere by the same pattern). Navigation must remain consistent across all features, and user actions (save, submit, enroll, etc.) must give clear feedback.

---

## 24. Multilingual Support

Phase 0 requirement. No hard-coded user-facing strings — all UI text routed through an i18n mechanism from the start (established in the initial commit's shared layer, [Section 20](#20-initial-commit-requirements)).

- Language selection available in Settings ([Section 9](#9-user-profile-and-settings)) and persisted per user (`UserProfile.languagePref`).
- Translation resources organized per language, loaded via the i18n mechanism.
- **Phase 0 covers UI chrome/labels/system text only.** Full translation of dynamic learning content (course text, questions) is **not** required in Phase 0 — content is authored/stored in a single language for now, with the data model left open to add localized content fields later (future phase).

---

## 25. Mock Data

| Mocked subsystem | What's mocked | Why | Expected interface | Replacement path |
|---|---|---|---|---|
| Course catalogue & content | Course/Module/Lesson records | No production content pipeline yet | `Course`/`Module`/`Lesson` entities per [Section 17](#17-domain--data-model) | Replace seed data with real authored/imported content; schema unchanged |
| External Training source | `Course` records flagged `source: external` | No live external-provider integration yet | Same `Course` shape, `source` field distinguishes origin | Swap the seed/import step for a real external-provider sync job |
| Assessments | Question banks | No content-authoring tool yet | `Assessment`/`Question` entities | Replace via Admin's Assessment Management CRUD, or bulk import |
| Auth/identity | Government SSO/IdP | Not available yet | Single auth-service abstraction ([Section 18](#18-high-level-architecture)) | Swap mock provider for real IdP behind the same interface |
| Recommended/Suggested courses | Static curated list, not personalized | Personalization/ML is future scope | Same course-card list shape as other course lists | Replace static list with a real recommendation service call |
| Analytics beyond simple aggregation | N/A — not mocked, simply not built | Would require future AI/analytics infra | — | Build in a future phase per [Section 14](#14-progress-and-analytics) |
| AI Assistant LLM provider | API key/provider configured via environment variable; no fallback local model | No production LLM contract finalized yet | A single LangChain chat-model client, provider-agnostic at the call site | Swap provider/model via config; graph/endpoint code unchanged |

---

## 26. Future Phases

Documented for context only — **not** Phase 0 requirements. (The one exception is the minimal AI Assistant stub in [Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro), which is Phase 0; everything below it is a further build-out of the same `agents/` package that stays future-phase.)

- AI-generated learning content and AI-generated assessments, including a **content generation pipeline across the four domains**, — likely built as further **LangGraph/LangChain** agents/pipelines added to the same backend `agents/` package ([Section 18](#18-high-level-architecture), [21](#21-feature-isolation)) that hosts the Phase 0 stub. *(The "four domains" are as stated by the team; not otherwise defined in this document — see [Section 33](#33-assumptions-and-open-questions).)*
- Personalized/ML-driven recommendations; adaptive learning paths — future LangGraph/LangChain-driven service, not Phase 0's static curated list.
- AI tutor / RAG-based learning assistant — evolving the Phase 0 single-turn stub into a **LangGraph**-orchestrated, **LangChain**-backed conversational agent with memory, tool use, and retrieval over course content.
- Skill-gap analysis and intelligent competency mapping against a formal `Competency` framework.
- Advanced analytics (predictive, concept-level mastery/weak-area detection).
- Deeper government knowledge-base integration and real SSO/IdP.
- Simulations and practical exercises.
- Advanced administrator intelligence (auto-flagging struggling learners, AI-assisted authoring).
- Proctoring module (mentioned as a consideration but not scoped — would need its own requirements pass before entering any phase).
- Self-service course planning (learners scheduling their own upcoming courses) and admin-driven course scheduling, both writing into the same `PlannedCourse` table that Phase 0's "Future Planned Courses" dashboard section reads from mock/seed data ([Section 6](#6-main-dashboard-home), [Section 17](#17-domain--data-model)).

---

## 27. Phase 0 Out of Scope

To prevent overbuilding, the following are explicitly **not** implemented in Phase 0, even though related simplified versions exist:

- Any ML/AI-driven personalization, recommendation, question generation, or tutoring (simplified version: static curated lists, static MCQ banks, and the single-turn, ungrounded AI Assistant stub in [Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro) — no memory, no RAG, no course-content grounding, no tool use).
- Skill-gap analysis / weak-concept detection (simplified version: raw score and completion aggregation only).
- Real government SSO/identity integration (simplified version: mocked email/password behind a swappable interface).
- Adaptive or cross-course practice hub (simplified version: per-lesson `Activity` step only).
- Certificate verification infrastructure (simplified version: a static certificate record/template on completion).
- Advanced admin intelligence and content-authoring tools (simplified version: basic CRUD).
- Full translation of learning content (simplified version: UI-chrome-only multilingual support).
- Proctoring of any kind.
- Real self-service or admin-driven course-planning/scheduling infrastructure (simplified version: `Future Planned Courses` dashboard section backed by mock/seed `PlannedCourse` data, [Section 6](#6-main-dashboard-home)).
- Sophisticated gamification around Learning Streak (badges, leaderboards, streak-recovery mechanics) — simplified version: a plain consecutive-day count.

---

## 28. Antigravity Implementation Guidelines

1. Read this `CONTEXT.md` in full before making implementation decisions.
2. Implement **Phase 0 only** — do not scaffold future-phase functionality "for later."
3. Treat the Miro flow ([Section 4](#4-miro-user-flow-source-of-truth)) as the primary source of truth for navigation/user journeys; use the written requirements to fill in detail Miro doesn't specify.
4. Do not silently resolve the open conflicts/questions in [Sections 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements) and [33](#33-assumptions-and-open-questions) in a way that contradicts the stated interpretation — flag instead if a different resolution seems necessary.
5. Prefer modular, feature-based architecture ([Sections 18](#18-high-level-architecture)–[21](#21-feature-isolation)); keep feature logic isolated.
6. Avoid giant files/components; avoid a monolithic root file that every feature must edit.
7. Keep shared files limited to genuinely shared functionality (design primitives, auth/session context, i18n, common types).
8. Reuse shared components rather than duplicating them across features.
9. Keep interfaces between modules/features explicit and minimal.
10. Do not over-engineer — Phase 0 favors simple, direct implementations (see [Section 27](#27-phase-0-out-of-scope)).
11. Use mock data where real integrations aren't available ([Section 25](#25-mock-data)), behind interfaces that make later replacement straightforward.
12. Preserve extension points for future phases (e.g., `source` field on `Course`, swappable auth provider) without building the future functionality itself.
13. Maintain consistent UX across features per [Section 23](#23-uiux-principles).
14. Update this document (Change Log, Decision Log, Progress) when significant architecture/product decisions are made or change.
15. Do not introduce major dependencies without a documented reason (add to Decision Log).
16. The initial commit builds the foundation only ([Section 20](#20-initial-commit-requirements)) — do not attempt full feature implementation in that commit.

---

## 29. Project Progress

### Current Status

- **Current phase:** Phase 0 — not yet started (pre-initial-commit).
- **Completed features:** none yet.
- **In-progress features:** none yet.
- **Known issues:** none yet.
- **Deferred features:** see [Section 26](#26-future-phases) and [Section 27](#27-phase-0-out-of-scope).
- **Technical debt:** none yet.
- **Open questions:** see [Section 33](#33-assumptions-and-open-questions).

### Phase 0 Checklist

Broken down per feature so completion is actually verifiable, not just a top-level box per feature area. No developer assignments are implied by this ordering.

- [ ] Project foundation (initial commit, [Section 20](#20-initial-commit-requirements))

- [ ] Authentication ([Section 5.1](#51-login-and-signup))
  - [ ] Login (email + password)
  - [ ] Signup (government/work email + password + basic info)
  - [ ] Forgot / reset password
  - [ ] Logout
  - [ ] Auth states (unauthenticated, authenticating, authenticated, session-expired, error)

- [ ] Landing page ([Section 5.2](#52-entry--landing-page))
  - [ ] About Platform
  - [ ] Explore Courses (unauthenticated catalogue preview)
  - [ ] How it Works
  - [ ] Login & Register entry point

- [ ] Onboarding ([Section 5.3](#53-first-time-signupvisualonboarding))
  - [ ] Profile Setup (intro step)
  - [ ] Personal Info
  - [ ] Education / Work Experience / Previous Training
  - [ ] Designation / Department / Job Role
  - [ ] Current Assignment / Areas of Interest
  - [ ] Save Profile → routes to Home

- [ ] Dashboard ([Section 6](#6-main-dashboard-home))
  - [ ] Continue Learning
  - [ ] Today's Goals
  - [ ] Learning Streak
  - [ ] Recommended / Suggested content
  - [ ] Current Course Progress
  - [ ] Recently Explored Courses
  - [ ] Learning History
  - [ ] Trending Courses
  - [ ] Future Planned Courses
  - [ ] My Learning / Progress snapshot
  - [ ] Competencies / Analytics snapshot

- [ ] Navigation ([Section 8](#8-navigation))
  - [ ] Discover
  - [ ] My Learning
  - [ ] Search
  - [ ] Profile
  - [ ] Role-based Admin link (hidden for Learner role)

- [ ] Search & Discovery ([Section 10](#10-search-and-discovery))
  - [ ] Search (keyword, trending searches/suggestions, recent search history)
  - [ ] Recently viewed courses
  - [ ] Categories (Popular, New)
  - [ ] External Training (Course List, Filter, Course Page)
  - [ ] Filters (duration, topic/field, difficulty)
  - [ ] Sorting

- [ ] My Learning ([Section 7](#7-my-learning))
  - [ ] In Progress courses
  - [ ] Completed courses
  - [ ] Skills and Progress
  - [ ] Practice (per-lesson Activity step)

- [ ] Course Page ([Section 11](#11-course-page))
  - [ ] Course overview
  - [ ] Start / Resume
  - [ ] Instructor / Organization
  - [ ] Duration
  - [ ] Content counts (videos, tests, labs, other content types)
  - [ ] Difficulty
  - [ ] Expandable modules with module contents
  - [ ] Skills gained

- [ ] Course Learning Experience ([Section 12](#12-course-learning-experience))
  - [ ] Persistent course sidebar (modules → lessons)
  - [ ] Current lesson content rendering
  - [ ] Activity (in-lesson practice) step
  - [ ] Module and overall course progress indicators

- [ ] Assessments ([Section 13](#13-assessments))
  - [ ] Instructions screen
  - [ ] MCQ question presentation
  - [ ] Submit + scoring
  - [ ] Results (score, correctness breakdown, pass/fail)
  - [ ] Attempt persistence (`AssessmentAttempt`)

- [ ] Progress and Analytics ([Section 14](#14-progress-and-analytics))
  - [ ] Overall course progress
  - [ ] Module progress
  - [ ] Previous quiz/test scores
  - [ ] Learning hours
  - [ ] Skills gained / skill progress
  - [ ] Certificates (static record + template)

- [ ] Profile and Settings ([Section 9](#9-user-profile-and-settings))
  - [ ] Personal information (editable)
  - [ ] Professional/onboarding information (editable)
  - [ ] Profile picture
  - [ ] Language selection
  - [ ] Appearance (dark mode)

- [ ] Admin Dashboard ([Section 15](#15-admin-dashboard))
  - [ ] Users enrolled / user list
  - [ ] Assign courses to users/groups
  - [ ] User course-progress overview
  - [ ] Create / manage courses
  - [ ] Create / manage assessments
  - [ ] Course-level analytics
  - [ ] Question difficulty / performance analytics

- [ ] AI Assistant stub ([Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)) — single-turn LangGraph + LangChain chat widget

- [ ] Multilingual UI ([Section 24](#24-multilingual-support)) — i18n mechanism + language setting, all Phase 0 screens routed through it

- [ ] Mock data seeded for all mocked subsystems ([Section 25](#25-mock-data))

- [ ] Integration pass across features

- [ ] QA pass

---

## 30. Change Log

### 2026-09-05
- **Change:** Initial creation of `CONTEXT.md`, incorporating the Miro `LMS Userflow` board and the written Phase 0 requirements brief.
- **Reason:** Establish the single source of truth before handing off to Antigravity for the initial project foundation commit.
- **Impact:** None yet (no prior version existed).
- **Status:** Complete.

### 2026-09-05 (update)
- **Change:** Confirmed technology stack — Next.js + React + shadcn/ui (frontend), FastAPI (backend), LangGraph + LangChain (future AI-agent phases). Updated Sections 18, 20, 21, 26, 31, 33, 34 accordingly.
- **Reason:** Team confirmed the stack; this closes the open question previously logged in Section 33.
- **Impact:** Architecture and initial-commit sections now name concrete frameworks/folder structures instead of stack-agnostic placeholders; the backend reserves an empty `agents/` package for future LangGraph/LangChain work.
- **Status:** Complete.

### 2026-09-05 (update 2)
- **Change:** Added a Phase 0 AI Assistant stub (Section 5.5) — a minimal single-turn chat widget built with LangGraph + LangChain, exposed via a new FastAPI `agents/` package. Updated Sections 18, 20, 21, 25, 26, 27, 29, 31, 32, 34 to reflect that this one AI feature is now real Phase 0 scope rather than fully deferred.
- **Reason:** Team decision to prove out the LangGraph/LangChain integration within Phase 0.
- **Impact:** The `agents/` backend package is no longer empty/reserved-only — it now ships a working (if intentionally minimal) feature in the initial commit. This is documented as an explicit, deliberate addition beyond the Miro-derived scope, not a silent one.
- **Status:** Complete.

### 2026-09-05 (update 3)
- **Change:** Updated the long-term vision statement (Section 1) to include a "content generation pipeline in the four domains," and reflected it in the Future Phases list (Section 26).
- **Reason:** Team-provided correction to the vision statement.
- **Impact:** The "four domains" are not defined elsewhere in this document — logged as open question 8 in Section 33 rather than guessed at.
- **Status:** Complete.

### 2026-09-05 (update 4 — second-pass revision)
- **Change:** Corrected an earlier drafting error in which `Today's Goals`, `Learning Streak`, `Recently Explored Courses`, `Learning History`, `Trending Courses`, and `Future Planned Courses` were treated as optional/deferred dashboard additions because they don't appear in the Miro `HOME` diagram. All six are restored as confirmed **Phase 0** requirements, sourced from the written baseline feature list rather than Miro, each given a deliberately lightweight (non-gamified, non-ML) Phase 0 implementation. Added a new `PlannedCourse` entity to the data model (previously listed as deliberately excluded) to back `Future Planned Courses`. Added [Decision 007](#decision-007--dashboard-features-confirmed-from-written-requirements) recording this as a confirmed decision, and resolved [Section 33](#33-assumptions-and-open-questions) item 2 accordingly (previously an open assumption, now resolved). Also corrected an internal contradiction in [Decision 005](#decision-005--confirmed-technology-stack)'s impact text, which had stated no LangGraph/LangChain dependency would be added until a future-phase feature needed it — a statement superseded the same day by Decision 006 but left unedited in Decision 005 itself. Expanded the Phase 0 checklist ([Section 29](#29-project-progress)) into per-feature sub-items so completion is actually verifiable. Expanded the requirements traceability table ([Section 32](#32-requirements-traceability)) to list the six restored dashboard items individually rather than folding them into a single "Dashboard" row. Added a conflict entry (#6) to [Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements) documenting the Miro/written-requirements gap that caused the original error. Added corresponding notes to [Future Phases](#26-future-phases) and [Phase 0 Out of Scope](#27-phase-0-out-of-scope) distinguishing Phase 0's lightweight versions of these features from their future-phase, fully-built-out forms.
- **Reason:** Review feedback: the original Phase 0 feature list supplied by the team is the baseline scope and must not be downgraded, moved to future phases, or marked optional merely because a feature isn't explicitly drawn on the Miro board. Miro is authoritative for navigation/flow; the written requirements are authoritative for feature scope.
- **Impact:** No features were removed. No new product scope was invented — all six items were already explicitly in the original written requirements; this revision restores them to their intended Phase 0 status and makes their (previously vague or absent) Phase 0 implementation concrete. Confirmed technology decisions, initial-commit boundaries, and the AI Assistant stub's scope were reviewed for contradictions and found to already be internally consistent, apart from the Decision 005 text corrected above.
- **Status:** Complete.
- **Status:** Complete.

---

## 31. Decision Log

### Decision 001 — Feature-based architecture
**Decision (Confirmed):** Organize both frontend and backend by feature/domain module rather than by technical layer.
**Reason:** Four developers will eventually divide Phase 0 features and work in parallel; feature isolation minimizes merge conflicts.
**Impact:** Initial commit must pre-create the feature-module structure; central files must only need one-line registrations per feature.
**Date:** 2026-09-05

### Decision 002 — Auth behind a swappable abstraction
**Decision (Confirmed):** All authentication/authorization logic goes through a single auth-service abstraction; Phase 0 implements it with mocked email/password.
**Reason:** Real government SSO/IdP is not yet available; the interface must not need to change when it becomes available.
**Impact:** No feature calls an identity provider directly; all auth goes through the shared abstraction.
**Date:** 2026-09-05

### Decision 003 — Single `Course` entity with a `source` field for external training
**Decision (Recommendation):** Model `External Training` as `Course` records with `source: external` rather than a parallel entity/UI.
**Reason:** Miro shows External Training resolving to the same `Course Page` as other courses; a parallel model would duplicate the course-page/learn/assess pipeline.
**Impact:** Simpler data model and UI reuse; external-source metadata is a field, not a fork.
**Date:** 2026-09-05
**Status:** Recommendation — confirm before the initial commit's schema is finalized.

### Decision 004 — Onboarding runs once, not on every login
**Decision (Assumption, not yet confirmed):** Existing/returning users skip `ONBOARD` and go straight to `HOME` after authentication, despite the Miro diagram showing both auth branches flowing into `ONBOARD`.
**Reason:** Re-running a 5-step onboarding wizard on every login is not a typical or usable pattern and isn't supported by the written brief.
**Impact:** Onboarding-completion must be tracked (e.g., a flag on `UserProfile`) to gate the redirect.
**Date:** 2026-09-05
**Status:** Open question — see [Section 33](#33-assumptions-and-open-questions), item 1.

### Decision 005 — Confirmed technology stack
**Decision (Confirmed):** Frontend: Next.js + React + shadcn/ui. Backend: FastAPI. AI-agent layer (future phases only): LangGraph + LangChain.
**Reason:** Team-confirmed stack.
**Impact:** Resolves the previously open stack question ([Section 33](#33-assumptions-and-open-questions), former item 7). Backend domain modules are FastAPI `APIRouter` packages; frontend feature modules are Next.js App Router route segments with shadcn/ui as the shared primitive layer. At the moment of this decision, the plan was to scaffold an empty, reserved `agents/` backend package with no LangGraph/LangChain dependency until a future-phase feature needed it. **That plan was superseded the same day by [Decision 006](#decision-006--phase-0-ai-assistant-stub)**, which adds a minimal Phase 0 AI Assistant stub — and, with it, the LangGraph/LangChain dependencies — to the initial commit. Decision 006 (not the original plan described here) reflects the current, confirmed scope.
**Date:** 2026-09-05

### Decision 006 — Phase 0 AI Assistant stub
**Decision (Confirmed):** Include one minimal AI feature in Phase 0 — a single-turn "Ask AI" chat widget built as one LangGraph graph calling an LLM via LangChain, exposed through a new FastAPI `agents/` package. No memory, RAG, tool use, or personalization.
**Reason:** Team decision to validate the LangGraph/LangChain integration path before Phase 0 is complete, rather than deferring all AI-agent work to a future phase.
**Impact:** Adds a new Phase 0 feature area ([Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)) and a real dependency (LangGraph + LangChain, plus an LLM provider API key) to the Phase 0 backend and initial commit, which is otherwise scoped to the confirmed Miro flow. This is a deliberate, explicit deviation from the Miro board (which does not show it) — not a silent addition.
**Date:** 2026-09-05

### Decision 007 — Dashboard features confirmed from written requirements
**Decision (Confirmed):** `Today's Goals`, `Learning Streak`, `Recently Explored Courses`, `Learning History`, `Trending Courses`, and `Future Planned Courses` are confirmed **Phase 0** dashboard sections, sourced from the written requirements baseline rather than the Miro board. Each gets a deliberately lightweight Phase 0 implementation (see [Section 6](#6-main-dashboard-home)): no gamification system for the streak, no ML/personalization for trending or recommendations, and mock/seed data for planned courses where no scheduling infrastructure exists yet.
**Reason:** An earlier draft of this document incorrectly treated these as optional or deferred solely because they don't appear in the Miro `HOME` diagram. Miro is the source of truth for navigation/flow, not for feature scope ([Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements)); the written requirements are the baseline scope and take precedence for *what the system must provide*.
**Impact:** [Section 6](#6-main-dashboard-home) dashboard table, [Section 17](#17-domain--data-model) data model (adds `PlannedCourse`), [Section 29](#29-project-progress) Phase 0 checklist, and [Section 32](#32-requirements-traceability) traceability table are all updated to reflect these as confirmed Phase 0, not optional. [Section 33](#33-assumptions-and-open-questions) item 2 is resolved accordingly.
**Date:** 2026-09-05

---

## 32. Requirements Traceability

| Requirement | Screen | User Flow | Data/Backend | Phase | Status |
|---|---|---|---|---|---|
| Login | Login | Entry → Login & Register → Existing User → Authenticate | `User` | 0 | Planned |
| Signup | Register | Entry → Login & Register → Register → Create Account | `User`, `UserProfile` | 0 | Planned |
| Forgot/Reset password | Auth | Login → Forgot Password | `User` | 0 | Planned |
| Onboarding | Onboard (5 steps) | Auth → Onboard → Save Profile → Home | `UserProfile` | 0 | Planned |
| Landing page | Entry | Entry (About/Explore/How it Works) | `Course` (preview only) | 0 | Planned |
| Dashboard (Miro-derived sections) | Home | Home (Continue Learning, Recommended, My Learning/Progress, Competencies/Analytics) | `Enrollment`, `Progress`, `UserSkill` | 0 | Planned |
| Today's Goals | Home | Written requirement — not in Miro (§4.3 conflict #6) | Computed from `Progress`/`Enrollment` timestamps + configurable target, no new entity | 0 | Planned |
| Learning Streak | Home | Written requirement — not in Miro (§4.3 conflict #6) | Computed from login/activity timestamps, no new entity | 0 | Planned |
| Current Course Progress | Home | Written requirement — overlaps Miro's Continue Learning box | `Enrollment`, `Progress` | 0 | Planned |
| Recently Explored Courses | Home | Written requirement — not in Miro (§4.3 conflict #6) | `LearningHistory` | 0 | Planned |
| Learning History | Home / My Learning | Written requirement — not in Miro (§4.3 conflict #6) | `LearningHistory` | 0 | Planned |
| Trending Courses | Home | Written requirement — related to Miro `Discover → Categories → Popular` | Mocked/simple ranking over `Course` | 0 | Planned |
| Future Planned Courses | Home | Written requirement — not in Miro (§4.3 conflict #6) | `PlannedCourse` (mock/seed data) | 0 | Planned |
| Discover/Search | Discover | Home → Discover → Search/Categories/External Training | `Course`, `SearchHistory` | 0 | Planned |
| Course page | Course Page | Discover → Course Page | `Course`, `Module`, `CourseSkill` | 0 | Planned |
| Learning experience | Learn | Course Page → Learn (Course→Module→Lesson→Content→Activity) | `Module`, `Lesson`, `Progress` | 0 | Planned |
| Assessments | Assess | Learn → Assess (Instructions→Questions→Submit→Results) | `Assessment`, `Question`, `AssessmentAttempt` | 0 | Planned |
| Progress/Analytics | Analytics/My Learning | Assess → Analytics | `Progress`, `AssessmentAttempt`, `UserSkill` | 0 | Planned |
| Profile & Settings | Profile | Home → Profile → Settings | `UserProfile` | 0 | Planned |
| Admin — Users | Admin Dashboard | Admin login → Users | `User`, `Enrollment`, `Progress` | 0 | Planned |
| Admin — Course/Assessment mgmt | Admin Dashboard | Admin login → Course/Assessment Mgmt | `Course`, `Module`, `Assessment`, `Question` | 0 | Planned |
| Admin — Analytics | Admin Dashboard | Admin login → Analytics | aggregated `Progress`/`AssessmentAttempt` | 0 | Planned |
| Multilingual UI | All screens | N/A (cross-cutting) | `UserProfile.languagePref` + i18n resources | 0 | Planned |
| AI Assistant stub | AI Assistant widget (Home, Course Page) | Not in Miro — standalone utility, §5.5 | `agents/` FastAPI package (LangGraph + LangChain), no persistent entity | 0 | Planned |

---

## 33. Assumptions and Open Questions

1. **Does onboarding re-run on every login, or only once?** Miro's diagram draws both auth branches into `ONBOARD`. **Assumption used:** onboarding runs once; a completion flag gates future logins straight to `HOME`. **Decision needed before implementing the post-auth redirect logic.**
2. ~~Are "Learning Streak" and "Today's Goals" (from the written brief but absent from Miro) in Phase 0?~~ — **Resolved:** Yes. Both, along with `Recently Explored Courses`, `Learning History`, `Trending Courses`, and `Future Planned Courses`, are confirmed Phase 0 dashboard requirements from the written baseline, not optional additions. See [Section 4.3](#43-conflicts-between-the-miro-flow-and-the-written-requirements) conflict #6, [Section 6](#6-main-dashboard-home), and [Decision 007](#decision-007--dashboard-features-confirmed-from-written-requirements).
3. **Assessment retry policy** — unlimited retakes vs. limited attempts. **Assumption:** unlimited retakes for Phase 0, latest attempt counts. **Decision needed** if a stricter policy is actually intended.
4. **Does the Administrator role retain Learner capabilities?** **Assumption:** yes, roles are additive. **Low-impact; confirm during role/permission implementation.**
5. **Is `External Training` a genuinely different data source (e.g., a real third-party catalogue) or just a UI grouping over the same internal catalogue?** **Assumption:** a `source` field on `Course` distinguishing `internal`/`external`, with `external` currently populated via mock/seed data. **Decision needed** if a real external integration is anticipated soon, as it may need its own sync/import architecture sooner than Phase 0 otherwise requires.
6. **Certificate format/verification** — Phase 0 assumes a simple static certificate record with no external verification. **Confirm this is sufficient for the hackathon/demo context.**
7. ~~Technology stack~~ — **Resolved:** Next.js + React + shadcn/ui (frontend), FastAPI (backend), LangGraph + LangChain (future AI-agent phases). See [Section 34](#34-technology-decisions) and Decision 005.
8. **What are the "four domains" for the future content generation pipeline ([Section 1](#1-project-overview), [Section 26](#26-future-phases))?** Not defined anywhere in the inputs to this document. **No impact on Phase 0** (the pipeline itself is future-phase), but should be defined by the team before that future-phase work is scoped in detail.

---

## 34. Technology Decisions

**Confirmed by the team** (see [Decision 005](#decision-005--confirmed-technology-stack)):

| Layer | Technology | Notes |
|---|---|---|
| Frontend framework | **Next.js** (App Router) | Route segments map to Miro top-level nodes ([Section 21](#21-feature-isolation)) |
| UI library | **React** | Standard Next.js rendering model; use server components where they don't need interactivity |
| Component/design system | **shadcn/ui** | Primitive components live in `components/ui/`; generate only what's needed per feature, styled via a shared Tailwind theme |
| Backend framework | **FastAPI** | Domain-scoped `APIRouter`s per feature ([Section 21](#21-feature-isolation)), Pydantic schemas for request/response validation |
| AI-agent orchestration | **LangGraph** | Phase 0: powers the single-node AI Assistant stub graph ([Section 5.5](#55-ai-assistant-phase-0-stub--added-by-team-decision-not-shown-in-miro)). Future phases: the AI tutor and other agentic workflows in [Section 26](#26-future-phases) extend the same package |
| AI/LLM tooling | **LangChain** | Phase 0: chat-model client for the AI Assistant stub. Future phases: RAG, AI-generated content/assessments, and recommendation logic in [Section 26](#26-future-phases) |

**Not yet specified and left open** (team should confirm; not blocking the initial commit):
- Relational database engine (e.g., Postgres vs. others) and ORM/migration tooling for the FastAPI backend.
- Auth/session mechanism specifics (e.g., JWT vs. server-side sessions) behind the auth-service abstraction ([Section 5.1](#51-login-and-signup), [18](#18-high-level-architecture)).
- Hosting/deployment target.

Antigravity should make the smallest reasonable choice for these open items to produce a working initial commit, and record the choice here as a new dated entry with status **"Recommendation — pending team confirmation"** rather than leaving it undocumented.
