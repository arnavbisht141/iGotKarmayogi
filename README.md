# 🏛️ iGOT Karmayogi — AI-Enabled Skill Intelligence & Learning Platform

> **Phase 0 Implementation** — Official Statistical System (MoSPI) & Civil Services Capacity Building

A modern, accredited digital learning platform built with **Next.js (App Router, shadcn/ui, TypeScript, Tailwind CSS)** on the frontend, **FastAPI (Python 3.12, SQLAlchemy 2.0)** on the backend, **Supabase** for cloud database & CLI migration management, and **LangGraph + LangChain** for the AI Assistant agent.

---

## 📋 Table of Contents
1. [Architecture Overview](#-architecture-overview)
2. [Prerequisites](#-prerequisites)
3. [Quick Start (Local Running Instructions)](#-quick-start-local-running-instructions)
   - [1. Backend Setup (FastAPI)](#1-backend-setup-fastapi)
   - [2. Frontend Setup (Next.js)](#2-frontend-setup-nextjs)
4. [Supabase Backend & CLI Workflow](#-supabase-backend--cli-workflow)
   - [1. Link Remote Supabase Project](#1-link-your-supabase-project)
   - [2. Push Migrations & Seed Data](#2-push-migrations--seed-to-supabase)
   - [3. Configure FastAPI with Supabase](#3-configure-fastapi-with-supabase)
5. [Service Endpoints & Verification](#-service-endpoints--verification)
6. [Database Initialization & Reset](#-database-initialization--reset)
7. [Pre-Seeded Demonstration Accounts](#-pre-seeded-demonstration-accounts)
8. [Miro User Flow Realization](#-miro-user-flow-realization)
9. [Environment Variables](#-environment-variables)
10. [Repository Organization](#repository-organization)

---

## 🏛️ Architecture Overview

```
iGot_Karmayogi/
├── frontend/                     # Next.js 16 (App Router, TypeScript, Tailwind CSS, shadcn/ui)
│   ├── package.json              # Frontend dependencies (@supabase/supabase-js, Lucide, Tailwind)
│   ├── next.config.ts            # Next.js configuration
│   └── src/                      # App router, components, lib (auth, api, supabase, i18n)
│
├── backend/                      # FastAPI (Python 3.12, SQLAlchemy 2.0, Pydantic v2)
│   ├── requirements.txt          # Python dependencies (fastapi, psycopg2, supabase, langchain)
│   ├── run.py                    # Uvicorn entry point (port 8000, reload enabled)
│   └── app/                      # Modular domain routers (auth, onboarding, dashboard, discover,
│                                 # courses, learning, assessments, profile, admin, agents)
│
├── supabase/                     # Supabase CLI configuration and database scripts
│   ├── config.toml               # Supabase project configuration
│   ├── migrations/               # PostgreSQL DDL migrations (20260910000000_initial_schema.sql)
│   └── seed.sql                  # Production demonstration seed SQL script
│
├── .env.example                  # Environment configuration template
├── package.json                  # Root convenience scripts for Supabase CLI
└── README.md
```

- **Frontend:** Next.js 16 App Router application with React 19, Tailwind CSS, Lucide icons, and `@supabase/supabase-js`.
- **Backend:** FastAPI modular monolith running on Python 3.12 with dual database compatibility (native **Supabase PostgreSQL** via psycopg2 or offline local SQLite fallback).
- **Supabase CLI:** Standardized PostgreSQL migrations, schema versioning, and pre-seeded demonstration data.
- **AI Copilot (LangGraph):** Compiled `StateGraph` workflow with LangChain model wrapper, supporting Google Gemini, OpenAI, or the built-in official statistical knowledge engine.

---

## 📦 Prerequisites

Ensure you have the following installed on your host machine:

- **Node.js**: v18.0.0 or higher (Node.js 20+ LTS recommended) & `npm`
- **Python**: v3.12 (or Python 3.10+) & `pip`
- **Git**

---

## 🚀 Quick Start (Local Running Instructions)

Follow these steps to run both backend and frontend locally in two terminal sessions.

### Optional: Configure Environment Variables

```bash
# In repository root
cp .env.example .env
```
*(Default settings work out-of-the-box using the local pre-seeded SQLite database without modifying `.env`)*

---

### 1. Backend Setup (FastAPI)

Open a terminal and navigate to the `backend` folder:

#### On Windows (PowerShell):
```powershell
cd backend

# Create virtual environment (specify Python 3.12)
py -3.12 -m venv venv
# Or if python maps directly to 3.12: python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend server
python run.py
```
> *Note: Use `py -3.12 -m venv venv` on Windows if you have Python 3.14 or another version set as your global default. If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, or activate via CMD `venv\Scripts\activate.bat`.*

#### On macOS / Linux (Bash / Zsh):
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python run.py
```

Alternatively, start with Uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### 2. Frontend Setup (Next.js)

Open a **second terminal** and navigate to the `frontend` folder:

```bash
cd frontend

# Install Node dependencies
npm install

# Start development server with hot-reload
npm run dev
```

The Next.js application will start and listen on [http://localhost:3000](http://localhost:3000).

---

## ⚡ Supabase Backend & CLI Workflow

The repository includes a complete **Supabase CLI** setup for managing schema migrations and database instances.

### 1. Link Your Supabase Project
From the repository root:

```bash
# Authenticate Supabase CLI
npx supabase login

# Link repository to your remote Supabase project
npx supabase link --project-ref <your-project-id>
```

### 2. Push Migrations & Seed to Supabase
Once linked, push the official 17-model schema and pre-seeded demonstration data directly to your remote Supabase PostgreSQL database:

```bash
# Apply migrations (supabase/migrations/20260910000000_initial_schema.sql)
npx supabase db push

# (Optional) Reset and seed remote database:
# npx supabase db reset
```

You can also use the convenience npm scripts from the root directory:
```bash
npm run supabase:link
npm run supabase:db:push
npm run supabase:db:pull
npm run supabase:status
```

### 3. Configure FastAPI with Supabase
In your `.env` file, point `DATABASE_URL` to your Supabase PostgreSQL connection URI:

```env
DATABASE_URL=postgresql+psycopg2://postgres.<project-ref>:<db-password>@aws-0-<region>.pooler.supabase.com:6543/postgres
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>

# Frontend client variables:
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-anon-key>
```

FastAPI automatically configures connection pooling (`pool_pre_ping=True`, `pool_size=10`) and normalizes URLs for psycopg2.

---

## 🌐 Service Endpoints & Verification

Once both servers are running, access the services:

| Service | URL | Description |
|---|---|---|
| **Frontend Web App** | [http://localhost:3000](http://localhost:3000) | Full Karmayogi learning experience UI |
| **Backend API** | [http://localhost:8000/api](http://localhost:8000/api) | FastAPI API root endpoint |
| **Interactive API Docs (Swagger UI)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Test and inspect all REST endpoints interactively |
| **ReDoc Specification** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative API documentation view |
| **Health Check Probe** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | System and database status probe |

---

## 🗄️ Database Initialization & Reset

The platform supports both local SQLite and remote Supabase PostgreSQL via SQLAlchemy 2.0:

- **Local SQLite Auto-Initialization:** If `DATABASE_URL` is set to SQLite (default), `backend/app/core/seed_data.py` automatically initializes tables and hydrates demo courses, lessons, assessments, and test users if the database is not yet populated.
- **To Reset Local SQLite:**
  1. Stop the backend server (`Ctrl + C`).
  2. Delete the SQLite file:
     - **Windows PowerShell:** `Remove-Item backend\karmayogi.db`
     - **macOS / Linux:** `rm backend/karmayogi.db`
  3. Start the backend again with `python run.py`.
- **To Reset Supabase PostgreSQL:**
  Run `npx supabase db reset` or re-execute `supabase/seed.sql` in the Supabase SQL Editor.

---

## 👤 Pre-Seeded Demonstration Accounts

| Role | Email | Password | Features Highlighted |
|---|---|---|---|
| **Administrator** | `admin@karmayogi.gov.in` | `Admin@123` | Full Admin Console, Cadre tracking, Course Assignment to officials, Assessment Difficulty Analytics |
| **Senior Statistical Officer** | `rajesh.kumar@mospi.gov.in` | `Learner@123` | Onboarded user, Active enrollment (66%), Learning streak (6 days), Today's study goal progress |
| **New Civil Servant** | `priya.sharma@mospi.gov.in` | `Learner@123` | Fresh user triggering the **5-step Onboarding Wizard** immediately upon login |

*Tip: The login page at `/login` provides one-click quick login buttons for all three accounts.*

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

1. **ENTRY (`/`)**: Landing page with About Platform, Explore Courses (unauthenticated preview), How it Works, and Login & Register CTAs.
2. **AUTH (`/login`, `/register`, `/forgot-password`)**: Official email validation, JWT session management, role-based access, and one-click demo credentials.
3. **ONBOARD (`/onboarding`)**: 5-step wizard (Profile Setup → Personal Info → Education/Workex → Designation/Role → Assignments & Technical Interests → Save Profile).
4. **HOME (`/home`)**: All 10 confirmed Phase 0 sections (Continue Learning, Today's Goals, Learning Streak, Recommended Courses, Current Course Progress, Recently Explored, Learning History, Trending Courses, Future Planned Courses, Progress & Competency snapshots).
5. **DISCOVER (`/discover`)**: Search bar with trending pills, category navigation (Popular, New), and external training filters (MoSPI Internal vs. ISTM/DoPT External).
6. **COURSE PAGE (`/courses/[id]`)**: Overview, instructors, syllabus accordion, content breakdown (videos, readings, labs, assessments), and Start/Resume logic.
7. **LEARN PLAYER (`/learn/[id]`)**: Coursera-inspired player with collapsible syllabus tree, video/markdown renderer, and in-lesson Practice Activity with immediate validation feedback.
8. **ASSESS (`/assess/[id]`)**: Instructions (70% passing standard), MCQ test runner, automated grading, detailed regulatory explanations, and pass/fail outcome.
9. **PROGRESS & CERTIFICATES (`/my-learning`, `/progress`)**: Verifiable printable/downloadable Karmayogi Certificate modal with official government seal and digital identifier.
10. **ADMIN CONSOLE (`/admin`)**: User list with course progress, course assignment modal, curriculum creation, and question error-rate analytics.
11. **AI ASSISTANT (Floating Copilot)**: LangGraph + LangChain powered statistical assistant accessible from any screen.

---

## ⚙️ Environment Variables

A template `.env.example` is included at the repository root:

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Secret key for signing JWT tokens | `karmayogi-secret-jwt-key-2026-phase-0` |
| `DATABASE_URL` | SQLAlchemy database URI (SQLite or Supabase PostgreSQL) | `sqlite:///./karmayogi.db` |
| `SUPABASE_URL` | Remote Supabase project URL | *Optional* |
| `SUPABASE_ANON_KEY` | Supabase anon public API key | *Optional* |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key for administrative workflows | *Optional* |
| `NEXT_PUBLIC_SUPABASE_URL` | Frontend public Supabase URL | *Optional* |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Frontend public Supabase anon key | *Optional* |
| `GOOGLE_API_KEY` | Google Gemini API key for LangGraph Copilot | *Optional (built-in fallback engine active)* |
| `OPENAI_API_KEY` | OpenAI API key for LangGraph Copilot | *Optional (built-in fallback engine active)* |
| `NEXT_PUBLIC_API_URL` | Public endpoint for backend API | `http://localhost:8000/api` |

---

## Repository Organization

The implementation is organized as a modular-monolith backend, a feature-oriented frontend, and Supabase migrations:

- [`supabase/`](supabase/) contains Supabase configuration, PostgreSQL migrations, and seed scripts.
- [`backend/README.md`](backend/README.md) documents backend ownership and modules.
- [`frontend/README.md`](frontend/README.md) documents frontend feature boundaries.
- [`ai-service/README.md`](ai-service/README.md) reserves the future independent AI boundary; it contains no implementation yet.
- [`docs/README.md`](docs/README.md) indexes architecture records and existing project documentation.
- [`.github/CODEOWNERS`](.github/CODEOWNERS) contains placeholders for team ownership.
