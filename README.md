# 🏛️ iGOT Karmayogi — AI-Enabled Skill Intelligence & Learning Platform

> **Phase 0 Implementation** — Official Statistical System (MoSPI) & Civil Services Capacity Building

A modern, accredited digital learning platform built with **Next.js (App Router, shadcn/ui, TypeScript, Tailwind CSS)** on the frontend, **FastAPI (Python 3.12)** on the backend, and **LangGraph + LangChain** for the AI Assistant agent.

---

## 📋 Table of Contents
1. [Architecture Overview](#-architecture-overview)
2. [Quick Start with Docker (Recommended)](#-quick-start-with-docker-recommended)
   - [Production Container Mode](#1-production-mode-optimized-build)
   - [Development Mode with Live Hot-Reload](#2-development-mode-with-live-hot-reload)
3. [Building, Rebuilding & Managing Containers](#-container-lifecycle--management)
4. [Running Locally Without Docker](#-running-locally-without-docker)
5. [Pre-Seeded Demonstration Accounts](#-pre-seeded-demonstration-accounts)
6. [Miro User Flow Realization](#-miro-user-flow-realization)
7. [Environment Variables](#-environment-variables)

---

## 🏛️ Architecture Overview

```
iGot_Karmayogi/
├── frontend/                     # Next.js 16 (App Router, TypeScript, Tailwind CSS, shadcn/ui)
│   ├── Dockerfile                # Multi-stage production container (Node 20 Alpine, standalone)
│   ├── Dockerfile.dev            # Development container with hot module replacement (HMR)
│   ├── .dockerignore
│   └── src/                      # App router, components, lib (auth, api, i18n)
│
├── backend/                      # FastAPI (Python 3.12, SQLAlchemy 2.0, Pydantic v2)
│   ├── Dockerfile                # Python 3.12 slim container with healthcheck
│   ├── .dockerignore
│   ├── requirements.txt
│   └── app/                      # Modular domain routers (auth, onboarding, dashboard, discover,
│                                 # courses, learning, assessments, profile, admin, agents)
│
├── docker-compose.yml            # Production container orchestration with health checks & data persistence
├── docker-compose.dev.yml        # Development orchestration with volume mounts for instant live-reload
├── .env.example                  # Environment configuration template
└── README.md
```

- **Frontend Container:** Multi-stage build producing an optimized ~150MB standalone runner with non-root security.
- **Backend Container:** Python 3.12 slim container with automated SQLite data volume persistence and automated health checks.
- **AI Copilot (LangGraph):** Compiled `StateGraph` workflow with LangChain model wrapper, supporting Google Gemini, OpenAI, or the built-in official statistical knowledge engine.

---

## 🐳 Quick Start with Docker (Recommended)

Make sure **Docker Desktop** is installed and running on your machine.

### 1. Production Mode (Optimized Build)

To build and start both the frontend and backend in isolated production containers:

```bash
# Clone the repository and navigate to root
cd iGot_Karmayogi

# Copy environment template (optional, defaults work out-of-the-box)
cp .env.example .env

# Build and start all containers in detached mode
docker compose up --build -d
```

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API & Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Endpoint:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

### 2. Development Mode with Live Hot-Reload

When actively developing features or styling UI, use `docker-compose.dev.yml`. This mounts your local folders (`./frontend` and `./backend`) into the containers, so **any code change on your host machine immediately hot-reloads inside the container without rebuilding**:

```bash
# Start in development mode with live volume mounting
docker compose -f docker-compose.dev.yml up --build
```

- Edits to React components in `frontend/src` hot-reload instantly in the browser.
- Edits to Python endpoints in `backend/app` reload Uvicorn automatically.

---

## 🔄 Container Lifecycle & Management

### View Running Containers & Health
```bash
docker compose ps
```

### Inspect Live Logs
```bash
# Follow logs for all services
docker compose logs -f

# Follow logs for backend only
docker compose logs -f backend

# Follow logs for frontend only
docker compose logs -f frontend
```

### How to Rebuild Containers

Whenever you modify dependencies (`requirements.txt` or `package.json`) or create major architectural changes:

```bash
# 1. Rebuild with cache
docker compose build

# 2. Rebuild cleanly from scratch (bypassing cached layers)
docker compose build --no-cache

# 3. Restart the updated containers
docker compose up -d
```

### Restart a Single Service
```bash
# Restart only the backend service
docker compose restart backend

# Restart only the frontend service
docker compose restart frontend
```

### Stopping and Cleaning Up Containers
```bash
# Stop containers without removing persisted data
docker compose down

# Stop containers AND delete the SQLite database volume (resets to fresh seed data)
docker compose down -v
```

---

## 💻 Running Locally Without Docker

If you prefer running natively without containers:

### 1. Backend (FastAPI)
```powershell
cd backend
.\venv\Scripts\activate          # Or source venv/bin/activate on Linux/Mac
pip install -r requirements.txt
python run.py
```
*Backend runs on `http://localhost:8000`.*

### 2. Frontend (Next.js)
```powershell
cd frontend
npm install
npm run dev
```
*Frontend runs on `http://localhost:3000`.*

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
| `DATABASE_URL` | SQLAlchemy database connection URI | `sqlite:////app/data/karmayogi.db` |
| `GOOGLE_API_KEY` | Google Gemini API key for LangGraph Copilot | *Optional (built-in fallback engine active)* |
| `OPENAI_API_KEY` | OpenAI API key for LangGraph Copilot | *Optional (built-in fallback engine active)* |
| `NEXT_PUBLIC_API_URL` | Public endpoint for backend API | `http://localhost:8000/api` |

---

## Repository organization

The existing implementation is organized as a modular-monolith backend and a
feature-oriented frontend. No business logic was changed as part of this move.

- [`backend/README.md`](backend/README.md) documents backend ownership and modules.
- [`frontend/README.md`](frontend/README.md) documents frontend feature boundaries.
- [`ai-service/README.md`](ai-service/README.md) reserves the future independent AI boundary; it contains no implementation yet.
- [`docs/README.md`](docs/README.md) indexes architecture records and existing project documentation.
- [`.github/CODEOWNERS`](.github/CODEOWNERS) contains placeholders for team ownership.
