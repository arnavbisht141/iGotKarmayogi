# iGOT Karmayogi — AI-Enabled Skill Intelligence & Learning Platform

> **Phase 0 Implementation** — Official Statistical System (MoSPI) & Civil Services Capacity Building

Built with **Next.js (App Router, shadcn/ui, TypeScript, Tailwind CSS)** on the frontend, **FastAPI** on the backend, and **LangGraph + LangChain** for the AI Assistant agent.

---

## 🏛️ System Architecture

- **Frontend (`frontend/`)**: Next.js App Router, shadcn/ui, Lucide Icons, Canvas-Confetti, i18n English/Hindi dictionary, responsive civic-tech aesthetic.
- **Backend (`backend/`)**: FastAPI with modular domain packages (`auth`, `onboarding`, `dashboard`, `discover`, `courses`, `learning`, `assessments`, `profile`, `admin`, `agents`).
- **AI Agent (`backend/app/agents/`)**: LangGraph `StateGraph` workflow compiling a single-node AI assistant that handles civil service regulations, statistical methodology questions, and platform guidance with fallback engine.
- **Database**: SQLite (`karmayogi.db`) via SQLAlchemy 2.0 with pre-seeded MoSPI statistical curriculum.

---

## 🚀 Quick Start Guide

### 1. Launch Backend (FastAPI)
```powershell
# From the repository root
cd backend
.\venv\Scripts\python run.py
```
*The backend runs at `http://localhost:8000` (API docs at `http://localhost:8000/docs`).*

### 2. Launch Frontend (Next.js)
```powershell
# In a separate terminal
cd frontend
npm run dev
```
*The frontend runs at `http://localhost:3000`.*

---

## 👤 Pre-Seeded Demonstration Accounts

| Role | Email | Password | Features Highlighted |
|---|---|---|---|
| **Administrator** | `admin@karmayogi.gov.in` | `Admin@123` | Full Admin Console, Cadre tracking, Course Assignment to officials, Assessment Difficulty Analytics |
| **Senior Statistical Officer** | `rajesh.kumar@mospi.gov.in` | `Learner@123` | Onboarded user, Active enrollment (66%), Learning streak (6 days), Today's study goal progress |
| **New Civil Servant** | `priya.sharma@mospi.gov.in` | `Learner@123` | Fresh user triggering the **5-step Onboarding Wizard** immediately upon login |

---

## 🗺️ Miro User Flow Realization

```
ENTRY (/) ──▶ AUTH (/login & /register) ──▶ ONBOARD (/onboarding, 5 steps) ──▶ HOME (/home)
                                                                                  │
  ┌───────────────────────────────┬───────────────────────────────────────────────┘
  ▼                               ▼
Discover (/discover) ────▶ Learn (/learn/[courseId]) ──▶ Assess (/assess/[assessmentId])
  │                          (Coursera-inspired player)    (MCQ Engine + Passing 70%)
  │                                                               │
  ▼                                                               ▼
Course Page (/courses/[id])                               Analytics & Certificates (/my-learning)
```

1. **ENTRY (`/`)**: Landing page with About Platform, Explore Courses (unauthenticated preview), How it Works, Login & Register CTAs.
2. **AUTH (`/login`, `/register`, `/forgot-password`)**: Official email validation, JWT session persistence, role-aware routing.
3. **ONBOARD (`/onboarding`)**: 5-step wizard (Profile Setup → Personal Info → Education/Workex → Designation/Role → Assignments & Interests → Save Profile).
4. **HOME (`/home`)**: All 10 confirmed Phase 0 sections (Continue Learning, Today's Goals, Learning Streak, Recommended Courses, Current Course Progress, Recently Explored, Learning History, Trending Courses, Future Planned Courses, Progress & Competencies snapshots).
5. **DISCOVER (`/discover`)**: Keyword search, recent searches, categories (Popular, New), and external training filters (ISTM/DoPT).
6. **COURSE PAGE (`/courses/[id]`)**: Overview, faculty info, content breakdown (videos, readings, labs), expandable syllabus.
7. **LEARN PLAYER (`/learn/[id]`)**: Collapsible syllabus tree, reading & video player, in-lesson practice activity with instant validation, complete & next logic.
8. **ASSESS (`/assess/[id]`)**: Instructions, MCQ examination runner, immediate grading, detailed answer explanations, pass/fail outcome.
9. **PROGRESS & CERTIFICATES (`/my-learning`, `/progress`)**: Verifiable printable/downloadable Karmayogi Certificate preview modal, competency radar.
10. **ADMIN CONSOLE (`/admin`)**: User list & progress tracking, course assignment modal, question difficulty error-rate analysis.
11. **AI ASSISTANT (Floating Copilot)**: LangGraph + LangChain powered statistical assistant accessible from any screen.
