# 📝 Assessment Engine & Verifiable Certification

> **Status:** `Implemented` (Phase 0)  
> **Primary Modules:**  
> - Backend: `backend/app/modules/assessments/`  
> - Frontend: `/assess/[assessmentId]`, `frontend/src/components/certificate/CertificateModal.tsx`  
> **Key Database Models:** `Assessment`, `Question`, `AssessmentAttempt`, `UserSkill`  

---

## 1. Executive Summary & Problem Statement

Accredited capacity building under Mission Karmayogi requires rigorous, objective assessment of competencies. To guarantee that civil servants attain verifiable mastery over statistical methods and public administration standards, the platform provides a standardized **Assessment Engine** with a strict 70% passing benchmark, automated explanatory grading, and tamper-verifiable digital certificates.

---

## 2. End-to-End User Flow

```
[Complete Course Modules] 
       │
       ▼
[Enter Assessment (/assess/[assessmentId])]
   ├── Timed environment (e.g. 20-30 mins)
   ├── Multiple Choice Questions (Single & Multiple selection)
   └── Interactive progress tracker
       │
       ▼ (Submit Answers)
[Automated Evaluation & Scoring]
   ├── If Score >= 70%: PASS ──▶ Confetti Celebration ──▶ Issue Verifiable Certificate
   └── If Score < 70%: RETAKE ──▶ Review Explanations ──▶ Re-attempt Allowed
```

---

## 3. Detailed Component Breakdown

### 3.1 Timed Assessment Environment (`frontend/src/app/assess/[assessmentId]/page.tsx`)
- **Examination Protocol:**
  - Standard instructions screen specifying duration, question count, and 70% passing threshold.
  - Active countdown timer with warning alerts as time expires.
  - Question navigation index allowing civil servants to jump between questions, flag items for review, and inspect answered status.
- **Question Format:**
  - Clean MCQ cards with option selection.
  - Support for single-choice and multi-choice statistical scenarios.

### 3.2 Automated Grading & Post-Submission Review
- **Instant Result Computation:** Compares officer choices against pre-seeded correct answers in `backend/app/models/models.py`.
- **Explanatory Regulatory Rationale:** Displays thorough official explanations for why each option is correct or incorrect, turning exams into learning opportunities.
- **Milestone Celebration:** Scoring 70% or higher triggers a celebratory milestone animation via `canvas-confetti`.

### 3.3 Verifiable Digital Certificate Modal (`frontend/src/components/certificate/CertificateModal.tsx`)
- **Institutional Authority:**
  - Official Government of India seal and Ministry of Statistics & Programme Implementation (MoSPI) branding.
  - Recipient officer name, designation, completed course title, and issuance date.
  - Unique cryptographic verification hash ID (e.g., `KARM-MOSPI-2026-XXXX`).
- **Export & Print Ready:**
  - Formatted to standard A4 landscape proportions.
  - Dedicated print stylesheet (`@media print`) stripping UI chrome, buttons, and modals for one-click pristine PDF generation.

---

## 4. Backend Architecture & API Endpoints

### 4.1 Endpoints Inventory
| HTTP Method | Endpoint | Module | Description |
|---|---|---|---|
| `GET` | `/api/assessments/{id}` | `assessments` | Fetch assessment details and questions (excluding answers). |
| `POST` | `/api/assessments/{id}/submit` | `assessments` | Submit answers, calculate score, evaluate pass/fail, and log attempt. |
| `GET` | `/api/assessments/{id}/history` | `assessments` | Retrieve previous attempt history and scores for the current user. |
| `GET` | `/api/certificates/{certificate_id}` | `assessments` | Verify and fetch certificate metadata by unique verification ID. |

### 4.2 Database Schema & Relationships (`backend/app/models/models.py`)

| Model | Table Name | Purpose & Relationships |
|---|---|---|
| `Assessment` | `assessments` | Master test record linked to a `Course` or `Module`. Stores passing score percentage (default `70%`). |
| `Question` | `questions` | MCQs with options (JSON array), correct answer index, difficulty rating, and explanatory text. |
| `AssessmentAttempt` | `assessment_attempts` | History of all exam submissions, score percentage, passed flag, officer answers, and submission timestamp. |
| `UserSkill` | `user_skills` | Updates learner acquired competency score upon successfully passing an accredited assessment. |

---

## 5. Rules & Operational Guidelines for AI Agents

> [!IMPORTANT]
> **Passing Threshold Standard:**
> The passing standard across all official assessments is strictly **70%**. Do not alter this threshold without an explicit Architecture Decision Record (ADR).

> [!CAUTION]
> **Answer Sanitization:**
> The `GET /api/assessments/{id}` endpoint must NEVER return `correct_answer` or option explanations to the client before submission. Answers and rationales must only be returned in the submission response payload.

> [!TIP]
> **Print Stylesheet Integrity:**
> When modifying `CertificateModal.tsx`, ensure all print media queries (`@media print`) remain intact so browser `window.print()` outputs clean vector PDF certificates without modal backdrops or buttons.
