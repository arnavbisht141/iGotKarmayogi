# 🔐 Authentication, Role-Based Access Control & Onboarding

> **Status:** `Implemented` (Phase 0)  
> **Primary Modules:**  
> - Backend: `backend/app/modules/auth/`, `backend/app/modules/onboarding/`, `backend/app/core/security.py`  
> - Frontend: `/login`, `/register`, `/onboarding`  
> **Key Database Models:** `User`, `UserProfile`, `Department`  

---

## 1. Executive Summary & Problem Statement

As a civil-service platform, secure identity verification, department attribution, and role segregation are foundational requirements. The **Auth & RBAC Subsystem** handles user registration, NIST-grade password hashing, JWT session lifecycle, a 5-step civil-service onboarding wizard, and role enforcement (`admin` vs `learner`).

---

## 2. Pre-Seeded Accounts & Live Evaluation Personas

The database is pre-seeded on startup via `backend/app/core/seed_data.py`. The `/login` page provides **1-click demo buttons** to instantly switch personas during demonstrations:

| Role | Email | Password | Pre-Configured State & Key Demonstration Flow |
|---|---|---|---|
| **Administrator** | `admin@karmayogi.gov.in` | `Admin@123` | Full access to `/admin` console. Can inspect officer roster, monitor cadre completion rates, assign mandatory courses, and review question difficulty metrics. |
| **Senior Statistical Officer** | `rajesh.kumar@mospi.gov.in` | `Learner@123` | Fully onboarded officer. Has active 66% progress in *National Sample Survey Methodologies*, a 6-day learning streak, today's goals, and acquired competency badges. |
| **New Civil Servant** | `priya.sharma@mospi.gov.in` | `Learner@123` | Brand new officer with `is_onboarded = False`. Logging in immediately routes into the **5-step Onboarding Wizard**. |

---

## 3. End-to-End User Flows

### 3.1 Registration & Onboarding Flow
```
[/register] ──▶ Create Account (Email, Password) ──▶ Set is_onboarded=False ──▶ Redirect to /onboarding
                                                                                       │
┌──────────────────────────────────────────────────────────────────────────────────────┘
▼
[/onboarding - 5-Step Wizard]
  ├── Step 1: Profile Setup (Full Name, Phone)
  ├── Step 2: Personal Information (Service Cadre: ISS / SSS / Non-Cadre, Batch Year)
  ├── Step 3: Education & Prior Experience (Degrees, Statistical Training)
  ├── Step 4: Designation & Department Assignment (MoSPI, DoPT, ISTM, Finance)
  └── Step 5: Technical Interests & Competency Focus (National Accounts, Survey Sampling)
        │
        ▼ (Submit Wizard)
Set is_onboarded=True ──▶ Redirect to /home Dashboard
```

### 3.2 Login Flow & Role Dispatching
- Authenticates credentials against PBKDF2 hash.
- Generates signed JWT access token stored in client cookie/state.
- If `role == "admin"`, user has privileged access to `/admin`.
- If `is_onboarded == False`, forces redirection to `/onboarding`.
- Otherwise, dispatches directly to `/home`.

---

## 4. Backend Architecture & Security Standards

### 4.1 PBKDF2-HMAC-SHA256 Password Security (`backend/app/core/security.py`)
- **Deprecated:** `passlib[bcrypt]` was removed due to upstream compatibility issues with Python 3.12.
- **Current Standard:** NIST-recommended PBKDF2 with SHA-256 and 100,000 iterations using Python standard library `hashlib`:
  ```python
  salt = secrets.token_hex(16)
  key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
  ```

### 4.2 Endpoints Inventory
| HTTP Method | Endpoint | Module | Description |
|---|---|---|---|
| `POST` | `/api/auth/login` | `auth` | Authenticates email/password, returns JWT token and user profile. |
| `POST` | `/api/auth/register` | `auth` | Registers a new account, validates email format and unique constraints. |
| `GET` | `/api/auth/me` | `auth` | Returns authenticated user identity, role, and department. |
| `POST` | `/api/onboarding/complete` | `onboarding` | Saves the 5-step wizard responses and updates `is_onboarded=True`. |
| `GET` | `/api/profile` | `profile` | Retrieves current user profile details and settings. |

### 4.3 Database Schema & Relationships (`backend/app/models/models.py`)

| Model | Table Name | Purpose & Relationships |
|---|---|---|
| `User` | `users` | Primary auth record: `id`, `email`, `hashed_password`, `role` (`admin`/`learner`), `is_active`. |
| `UserProfile` | `user_profiles` | Civil service details: `user_id`, `department_id`, `designation`, `cadre`, `batch_year`, `is_onboarded`. |
| `Department` | `departments` | Government ministry/cadre entity: `id`, `name`, `code` (e.g. `MoSPI`, `DoPT`). |

---

## 5. Rules & Operational Guidelines for AI Agents

> [!CAUTION]
> **No bcrypt / passlib Re-introduction:**
> Do NOT attempt to install or re-introduce `passlib[bcrypt]` or `bcrypt` package dependencies. Always maintain the native PBKDF2-HMAC-SHA256 implementation in `backend/app/core/security.py`.

> [!IMPORTANT]
> **Seed Data Synchronization:**
> If adding new profile fields or auth parameters, ensure `backend/app/core/seed_data.py` is updated simultaneously so that resetting `backend/karmayogi.db` and restarting the backend continues to produce a fully seeded demo environment.
