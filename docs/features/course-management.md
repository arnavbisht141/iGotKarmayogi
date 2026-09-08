# Course Management & Learning Player

> **Status:** `Implemented` (Phase 0)  
> **Primary Modules:**  
> - Backend: `backend/app/modules/discover/`, `backend/app/modules/courses/`, `backend/app/modules/learning/`  
> - Frontend: `/discover`, `/courses/[courseId]`, `/learn/[courseId]`  
> **Key Database Models:** `Course`, `Module`, `Lesson`, `Enrollment`, `Progress`, `Skill`, `CourseSkill`  

---

## 1. Executive Summary & Problem Statement

Civil service training requires accredited, structured syllabi covering national statistical methodologies, data quality rubrics, and administrative systems. The **Course Management & Learning Player** provides an end-to-end learning lifecycle: catalog discovery, syllabus inspection, enrollment tracking, and a Coursera-style split-screen learning environment with interactive concept check checkpoints.

---

## 2. End-to-End User Flow

```
[Discover Catalog (/discover)] 
       │
       ▼
[Course Detail (/courses/[courseId])] 
       │
       ▼ (Enroll / Resume)
[Learning Player (/learn/[courseId])]
   ├── Left: Collapsible Curriculum Tree (Modules & Lessons)
   └── Right: Content Area (Video Lectures + Markdown Readings + Mini Practice Checks)
       │
       ▼ (Pass Lessons & Concept Checks)
[Course Completion & Assessment Unlock]
```

---

## 3. Detailed Component Breakdown

### 3.1 Course Discovery Catalog (`frontend/src/app/discover/page.tsx` & `frontend/src/features/catalog/components/DiscoverPage.tsx`)
- **Institutional Visual Hierarchy:** Full-width white header (`bg-white border-b border-slate-200`) with uppercase ministry eyebrow (`Building2` icon) and slate workspace canvas (`bg-[#F8FAFC]`), harmonizing seamlessly with the national homepage design system.
- **Emoji-Free Government Typography:** All decorative emojis (`🔥`, `✨`, text stars `★`) and artificial rectangular colored pill boxes have been completely eliminated in favor of clean Lucide SVG icons and government-standard typography.
- **Comprehensive Bilingual (Hindi/English) Support:** Integrated with `useI18n()` providing instant toggle between English and Hindi across the entire catalog—including search inputs, trending keywords (*National Sample Survey* / *राष्ट्रीय नमूना सर्वेक्षण*, *Consumer Price Index* / *उपभोक्ता मूल्य सूचकांक*), discipline categories (*Data Science* / *डेटा विज्ञान*), filter options, course titles, syllabus overviews, accredited organizations, and action buttons.
- **Instant Search & Interactive Filtering:** Debounced search bar with clear button, provider source toggle (*MoSPI Internal* vs. *External Accredited*), difficulty level dropdown (*Beginner*, *Intermediate*, *Advanced*), dynamic sorting (*Most Enrolled*, *Highest Rated*, *Newly Published*, *Shortest Duration*), and one-click filter reset.
- **Accreditation Trust Ribbon:** Institutional accreditation footer affirming MoSPI accreditation, CBC competency guidelines, and verifiable cryptographic credentials.
- **Turbopack / Standalone Guard:** Query parameter reading is wrapped inside a React `<Suspense>` boundary to maintain Next.js standalone container compatibility.

### 3.2 Course Overview & Syllabus (`frontend/src/app/courses/[courseId]/page.tsx` & `frontend/src/features/catalog/components/CourseDetailPage.tsx`)
- **Metadata Card:** Estimated duration, lesson count, difficulty level, accrediting body (MoSPI/ISTM), and acquired competency badges using unified Navy `#1E3A8A` / Sober Yellow `#EAB308` palette.
- **Collapsible Syllabus Tree:** Accordion breakdown of modules and contained atomic lessons with lesson duration and practice indicator badges.
- **Dynamic Action Button:** Context-aware CTA toggling between *Start Course*, *Resume Learning*, and *Completed* based on enrollment state, with full Hindi localization.

### 3.3 Coursera-Style Split-Screen Learning Player (`frontend/src/app/learn/[courseId]/page.tsx`)
- **Curriculum Sidebar (Left):**
  - Displays all syllabus modules with expandable lesson items.
  - Real-time completion checkboxes updating upon lesson finish.
- **Content Viewer (Right):**
  - Video lecture player with progress tracking.
  - Rich markdown viewer for official government manuals and technical readings.
  - **Interactive Concept Practice Activity:**
    - Embedded mini-quizzes testing comprehension before advancing.
    - Provides immediate regulatory feedback explaining correct and incorrect options.
- **Progress Synchronization:** Every lesson completion calls `POST /api/learning/progress` to record granular completion timestamps.

---

## 4. Backend Architecture & API Endpoints

### 4.1 Endpoints Inventory
| HTTP Method | Endpoint | Module | Description |
|---|---|---|---|
| `GET` | `/api/courses` | `courses` | List all available courses with optional filter parameters. |
| `GET` | `/api/courses/{id}` | `courses` | Fetch comprehensive course details including syllabus modules and lessons. |
| `POST` | `/api/courses/{id}/enroll` | `courses` | Enroll the authenticated user in the course. |
| `GET` | `/api/learning/{course_id}/player` | `learning` | Load player state, active lesson, and previous progress. |
| `POST` | `/api/learning/progress` | `learning` | Record lesson completion and advance course progress percentage. |
| `POST` | `/api/learning/practice-check` | `learning` | Validate answers for embedded in-lesson concept checks. |

### 4.2 Database Schema & Relationships (`backend/app/models/models.py`)

| Model | Table Name | Purpose & Relationships |
|---|---|---|
| `Course` | `courses` | Catalog metadata, title, description, thumbnail, duration, provider. Relates to `Module` and `CourseSkill`. |
| `Module` | `modules` | Syllabus sections within a course, ordered by sequence number (`order_index`). |
| `Lesson` | `lessons` | Atomic learning unit: video URLs, markdown content, practice check payload. |
| `Enrollment` | `enrollments` | Tracks learner enrollment status (`active`, `completed`), date started, and overall completion percentage. |
| `Progress` | `progress` | Granular per-lesson completion records with timestamps. |
| `Skill` | `skills` | Competency taxonomy (e.g. *Survey Sampling*, *National Accounts*). |
| `CourseSkill` | `course_skills` | Junction table mapping courses to instilled competencies. |

---

## 5. Rules & Operational Guidelines for AI Agents

> [!IMPORTANT]
> **Suspense Boundary Requirement:**
> Any Next.js page or component in `frontend/src/app/discover/` or `frontend/src/app/courses/` that consumes `useSearchParams()` MUST be wrapped inside a `<Suspense>` boundary. Failing to do so breaks the Next.js standalone container build.

> [!NOTE]
> **Data Integrity:**
> Course completion percentage in `enrollments` must be calculated dynamically based on total completed `progress` rows against total course `lessons`.
