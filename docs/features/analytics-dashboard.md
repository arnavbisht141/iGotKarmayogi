# 📊 Analytics, Dashboards & Administrative Console

> **Status:** `Implemented` (Phase 0)  
> **Primary Modules:**  
> - Backend: `backend/app/modules/dashboard/`, `backend/app/modules/admin/`  
> - Frontend: `/home`, `/admin`, `/my-learning`  
> **Key Database Models:** `LearningHistory`, `SearchHistory`, `UserSkill`, `Skill`, `AssessmentAttempt`  

---

## 1. Executive Summary & Problem Statement

Civil-service learning requires both individualized motivation and executive oversight. The platform achieves this via two specialized interfaces:
1. **The Learner Home Dashboard:** A 10-widget hub showing streaks, daily goals, in-progress modules, and acquired MoSPI competency radars.
2. **The Admin Console:** An institutional supervisory portal enabling training administrators to review officer progress, assign mandatory courses across cadres, and detect curriculum pain-points through question analytics.

---

## 2. Learner Home Dashboard: The 10 Phase 0 Widgets (`/home`)

The learner home dashboard (`frontend/src/app/(dashboard)/home/page.tsx`) implements all 10 confirmed widgets per the validated Miro user flow:

| Widget # | Name | Description & Interaction |
|---|---|---|
| **1** | **Continue Learning** | Primary hero resume card displaying the most recent active course, module title, and progress bar with 1-click resume. |
| **2** | **Today's Learning Goals** | Interactive daily task checklist (e.g., complete 1 lesson, attempt concept check) rewarding consistency. |
| **3** | **Learning Streak Counter** | Motivational streak tracker highlighting consecutive active days with badge indicators. |
| **4** | **Recommended Courses** | Cadre-tailored statistical suggestions based on officer designation and declared technical interests. |
| **5** | **Course Progress Breakdown** | Multi-card view showing percentage completion across all currently enrolled courses. |
| **6** | **Recently Explored** | Fast access to previously visited modules and syllabus sections. |
| **7** | **Official Learning History** | Chronological log of recent learning sessions with time spent and completion markers. |
| **8** | **Trending MoSPI Courses** | Aggregated list of the most popular statistical courses across civil service cadres. |
| **9** | **Future Planned Courses** | Bookmarked courses marked by the officer for upcoming capacity building cycles. |
| **10** | **Competencies Radar Summary** | Visual competency breakdown mapping acquired skills across MoSPI functional domains (e.g. National Accounts, Survey Sampling). |

---

## 3. Administrative Supervisory Console (`/admin`)

Restricted strictly to users with the `admin` role (`admin@karmayogi.gov.in`):

### 3.1 Officer Roster & Cadre Management
- Searchable directory of registered civil servants with department and cadre filters (ISS, SSS, Subordinate).
- Real-time tracking of overall completion rates, enrolled courses, and passed certifications.

### 3.2 Mandatory Course Assignment Modal
- Allows administrators to assign mandatory training modules to individual officers or entire cadres.
- Sets target completion dates and triggers dashboard notifications for assigned learners.

### 3.3 Curriculum Question Failure-Rate Analytics
- Analyzes all `AssessmentAttempt` records to detect questions with unusually high failure rates.
- Provides actionable diagnostic insights to curriculum coordinators to refine unclear questions or expand prerequisite lesson material.

---

## 4. Backend Architecture & API Endpoints

### 4.1 Endpoints Inventory
| HTTP Method | Endpoint | Module | Description |
|---|---|---|---|
| `GET` | `/api/dashboard/home` | `dashboard` | Aggregates all 10 widget data payloads into a single optimized read model. |
| `GET` | `/api/dashboard/my-learning` | `dashboard` | Fetches active enrollments, completed certifications, and skill radar points. |
| `GET` | `/api/admin/users` | `admin` | Fetches officer roster with cadre filters and progress metrics. |
| `POST` | `/api/admin/assign-course` | `admin` | Assigns a mandatory course to one or more civil servants. |
| `GET` | `/api/admin/analytics/questions` | `admin` | Computes question failure rates and average attempt metrics. |

### 4.2 Database Schema & Relationships (`backend/app/models/models.py`)

| Model | Table Name | Purpose & Relationships |
|---|---|---|
| `LearningHistory` | `learning_history` | Historical log of learning sessions, time spent, and streak calculations. |
| `SearchHistory` | `search_history` | Recorded searches for discovery recommendations and trending queries. |
| `PlannedCourse` | `planned_courses` | Future target courses bookmarked by learners on their dashboard. |
| `UserSkill` | `user_skills` | Tracks competency scores per skill acquired by individual learners. |
| `Skill` | `skills` | Standard competency definitions (e.g., *Survey Sampling*, *UN-NQAF Standards*). |

---

## 5. Rules & Operational Guidelines for AI Agents

> [!IMPORTANT]
> **Admin Authorization Guard:**
> All endpoints under `backend/app/modules/admin/` and frontend views under `/admin` must strictly enforce `role == "admin"`. Non-admin users attempting access must receive an HTTP 403 Forbidden.

> [!NOTE]
> **Read Model Performance:**
> The `GET /api/dashboard/home` endpoint is a read-heavy aggregation. Ensure queries avoid N+1 bottlenecks by utilizing SQLAlchemy `joinedload` / `selectinload` for user profiles and enrollments.
