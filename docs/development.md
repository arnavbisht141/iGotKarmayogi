# 🛠️ Development & Operations Guide

> **Platform:** iGOT Karmayogi (MoSPI)  
> **Target Audience:** Developers, DevOps Engineers & AI Coding Agents  

---

## 1. Quick Start with Docker (Recommended)

Docker Desktop is the fastest and most consistent way to run the entire system.

### 1.1 Development Mode (Live Hot-Reloading)
In development mode, source code is volume-mounted so any edits to frontend or backend files trigger immediate live reloads.

```bash
# 1. Initialize environment variables
cp .env.example .env

# 2. Start all services in live development mode
docker compose -f docker-compose.dev.yml up --build
```
- **Frontend:** `http://localhost:3000` (Next.js 16 with Hot Module Replacement)
- **Backend API:** `http://localhost:8000/api` (FastAPI with Uvicorn `--reload`)
- **API Swagger Docs:** `http://localhost:8000/docs`

### 1.2 Production Container Mode
Runs the optimized multi-stage standalone frontend runner (~150MB) and production FastAPI container with persistent SQLite volume.

```bash
docker compose up --build -d
```

### 1.3 Essential Docker Operational Commands
```bash
# View live backend logs
docker compose logs -f backend

# View live frontend logs
docker compose logs -f frontend

# Rebuild without Docker cache
docker compose build --no-cache && docker compose up -d

# Stop all containers and reset database to pristine seed data
docker compose down -v
```

---

## 2. Pre-Seeded Accounts & Live Evaluation Personas

The database is automatically populated upon initial startup by `backend/app/core/seed_data.py`. 
You can switch between these personas on `/login` using the **1-click demo buttons**:

| Role | Email | Password | Pre-Configured State & Key Demonstration Flow |
|---|---|---|---|
| **Administrator** | `admin@karmayogi.gov.in` | `Admin@123` | Full access to `/admin` console. Inspect officer roster, monitor cadre completion rates, assign mandatory courses, and review question difficulty metrics. |
| **Senior Statistical Officer** | `rajesh.kumar@mospi.gov.in` | `Learner@123` | Fully onboarded officer. Has active 66% progress in *National Sample Survey Methodologies*, a 6-day learning streak, today's goals, and acquired competency badges. |
| **New Civil Servant** | `priya.sharma@mospi.gov.in` | `Learner@123` | Brand new officer with `is_onboarded = False`. Logging in immediately routes into the **5-step Onboarding Wizard**. |

---

## 3. Local Development (Without Docker)

### 3.1 Backend Setup (FastAPI & Python 3.12)
```bash
cd backend
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux / macOS:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

> [!CAUTION]
> Do NOT install `passlib[bcrypt]` due to known upstream Python 3.12 compatibility bugs. The repository uses native NIST PBKDF2 in `backend/app/core/security.py`.

### 3.2 Frontend Setup (Next.js 16 & React 19)
```bash
cd frontend
npm install
npm run dev
```

---

## 4. Verification & Testing Commands

```bash
# Verify frontend production build
cd frontend
npm run build

# Verify backend health check
curl http://localhost:8000/api/health
```

---

## 5. Architectural Boundaries

For domain modules, see [domain-boundaries.md](domain-boundaries.md).  
For runtime boundaries and AI extraction plans, see [architecture.md](architecture.md).  
For ADRs, inspect the [adr/](adr/) directory.
