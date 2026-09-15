# Supabase Database Schema & Data Architecture

> **Document Type:** Database Architecture & Supabase Data Dictionary  
> **Platform:** iGOT Karmayogi (Competency Governance Platform)  
> **Authority:** Ministry of Statistics & Programme Implementation (MoSPI), Government of India  
> **Target Audience:** Backend Engineers, AI Pipeline Agents, Database Administrators, Security Auditors  

---

## 1. Architectural Overview & Supabase Strategy

The iGOT Karmayogi platform leverages **Supabase (PostgreSQL 15+)** as its primary cloud data infrastructure. The architecture operates in a **hybrid resilient model**:

- **Production Cloud (Supabase PostgreSQL)**: Authoritative cloud store providing managed PostgreSQL, automated point-in-time recovery, Row Level Security (RLS), real-time change subscriptions, and PostgREST API access.
- **Local Development / Offline Prototyping (SQLite)**: Rapid offline development and unit/integration testing executed against `backend/karmayogi.db` using identical SQLAlchemy ORM models.
- **Database Migrations (`supabase/migrations/`)**: All DDL changes are tracked via sequential SQL migrations:
  1. `20260910000000_initial_schema.sql` (Core LMS, Identity, Curriculum, Assessments)
  2. `20260914000001_technical_course_pipeline.sql` (Technical Pipeline, Transcripts, Lab Templates, Docker Validations)
  3. `20260914000002_digital_governance_cybersecurity.sql` (Cyber Defense Templates, CTF Challenges, Marimo Sessions, User Cyber Competency)

```
                       ┌──────────────────────────────────────────────┐
                       │          Client Applications (Web)          │
                       └──────────────────────┬───────────────────────┘
                                              │
                              HTTPS / REST    │  Auth Token (JWT)
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │          FastAPI Backend Application         │
                       │    (SQLAlchemy 2.0 ORM / Connection Pool)   │
                       └──────────────┬───────────────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
                 ▼                                         ▼
  ┌─────────────────────────────┐           ┌─────────────────────────────┐
  │   Supabase Cloud Postgres   │           │   Local SQLite (karmayogi)  │
  │ • Real-time DB              │           │ • Test Suite Execution      │
  │ • Row Level Security (RLS)  │           │ • Offline Development       │
  │ • Production Civil Servants │           │ • Local Container Sandboxes │
  └─────────────────────────────┘           └─────────────────────────────┘
```

---

## 2. Exhaustive Schema & Table Directory

The database consists of **27 normalized relational tables** organized into **6 functional competency domains**:

| Domain | Tables | Primary Purpose |
|---|---|---|
| **Core Identity & RBAC** | `users`, `user_profiles`, `departments` | Authentication, Civil Service cadre, designations, and ministries. |
| **Institutional Curriculum** | `courses`, `modules`, `lessons`, `skills`, `course_skills`, `user_skills` | Course catalog, official syllabus, skills taxonomy, and learner proficiencies. |
| **Progress & Learning State** | `enrollments`, `progress`, `planned_courses`, `learning_history`, `search_history` | Course completion tracking, daily learning streaks, and discovery telemetry. |
| **Statistical & Adaptive Testing** | `assessments`, `questions`, `assessment_attempts` | Item Response Theory (IRT) parameters, 3PL adaptive CAT exams, and civil service certifications. |
| **Technical Hands-on Labs** | `technical_transcripts`, `technical_learning_objectives`, `technical_lab_templates`, `technical_generated_labs`, `technical_lab_solutions`, `technical_lab_validation_results` | Video transcript ingestion, AI objective extraction, Jupyter/Marimo lab generation, and Docker sandbox test runners. |
| **Digital Governance & Cyber Defense** | `cyber_sandbox_templates`, `cyber_sandbox_challenges`, `cyber_sandbox_sessions`, `user_cyber_competencies` | CERT-In compliance scenarios, procedural CTF challenges, isolated Marimo containers, and dynamic flag validation. |

---

## 3. Detailed Field-by-Field Reference

### Domain 1: Core Identity & Institutional Structure

#### Table: `public.users`
Stores civil service user accounts and credential metadata.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique civil servant identifier. |
| `email` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL`, `INDEXED` | Institutional email (e.g., `*.gov.in` or `*.nic.in`). |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | PBKDF2-HMAC-SHA256 salted password hash. |
| `full_name` | `VARCHAR(255)` | `NOT NULL` | Officer's full civil service name. |
| `role` | `VARCHAR(50)` | `DEFAULT 'learner'` | RBAC role: `'learner'`, `'instructor'`, `'admin'`. |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Account enablement flag. |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp of account registration. |

#### Table: `public.user_profiles`
Detailed civil service cadre, ministerial hierarchy, and onboarding data.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Profile record identifier. |
| `user_id` | `INTEGER` | `UNIQUE`, `NOT NULL`, `FK -> users.id (CASCADE)` | Associated user account. |
| `department_id` | `INTEGER` | `FK -> departments.id (SET NULL)` | Ministry/Department posting. |
| `designation` | `VARCHAR(255)` | `NULLABLE` | Official post (e.g., *Deputy Director, Data Analyst*). |
| `cadre` | `VARCHAR(100)` | `NULLABLE` | Cadre branch (e.g., *Indian Statistical Service (ISS)*). |
| `phone` | `VARCHAR(50)` | `NULLABLE` | Secure official contact number. |
| `state` | `VARCHAR(100)` | `NULLABLE` | State cadre or central ministry posting location. |
| `preferred_language` | `VARCHAR(10)` | `DEFAULT 'en'` | Default language preference (`'en'` or `'hi'`). |
| `onboarding_completed` | `BOOLEAN` | `DEFAULT FALSE` | Tracks if officer completed the 5-step competency wizard. |
| `competency_scores_json`| `TEXT` | `DEFAULT '{}'` | Baseline score distribution across competencies. |

#### Table: `public.departments`
Institutional government ministries and training academies.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Department identifier. |
| `name` | `VARCHAR(255)` | `NOT NULL`, `UNIQUE` | Ministry/body title (e.g., *MoSPI, NeGD, CERT-In, ISTM*). |
| `description` | `TEXT` | `NULLABLE` | Institutional mandate and training charter. |

---

### Domain 2: Institutional Curriculum & Competencies

#### Table: `public.courses`
The central catalog of civil service training courses across all four competencies.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique course identifier (`1`=Behavioural, `2`=Statistical, `3`=Technical, `4`=Digital Governance). |
| `title` | `VARCHAR(255)` | `NOT NULL` | Course title. |
| `overview` | `TEXT` | `NOT NULL` | Detailed executive summary and pedagogical objectives. |
| `instructor` | `VARCHAR(255)` | `NOT NULL` | Senior civil servant, directorate, or academy faculty. |
| `organization` | `VARCHAR(255)` | `NOT NULL` | Administering agency (e.g., *NCIIPC, MoSPI, ISTM*). |
| `duration_hours` | `DOUBLE PRECISION` | `DEFAULT 5.0` | Total accredited training duration. |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Difficulty level: `'beginner'`, `'intermediate'`, `'advanced'`. |
| `source` | `VARCHAR(50)` | `DEFAULT 'internal'` | Source repository: `'internal'` (iGOT) or `'external'`. |
| `category` | `VARCHAR(100)` | `NOT NULL`, `INDEXED` | Competency track: `'Behavioural'`, `'Statistical'`, `'Technical'`, `'Digital Governance'`. |
| `thumbnail_url` | `VARCHAR(500)` | `NULLABLE` | Institutional banner or emblem image. |
| `rating` | `DOUBLE PRECISION` | `DEFAULT 4.8` | Evaluator and peer learner satisfaction score (1.0 to 5.0). |
| `enrolled_count` | `INTEGER` | `DEFAULT 0` | Total enrolled civil servants. |
| `is_popular` | `BOOLEAN` | `DEFAULT FALSE` | Highlighted on national cadre dashboard. |
| `is_new` | `BOOLEAN` | `DEFAULT FALSE` | Newly notified curriculum directive flag. |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Date course was promulgated. |

#### Table: `public.modules`
Sequential curricular modules dividing a course into syllabus units.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Module identifier. |
| `course_id` | `INTEGER` | `NOT NULL`, `FK -> courses.id (CASCADE)` | Parent course reference. |
| `title` | `VARCHAR(255)` | `NOT NULL` | Module title (e.g., *Module 1: CPI Weighting Diagrams*). |
| `description` | `TEXT` | `NULLABLE` | Detailed module coverage summary. |
| `order` | `INTEGER` | `DEFAULT 1` | Sequence display order within course. |

#### Table: `public.lessons`
Individual atomic learning units (readings, instructional videos, or interactive labs).

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Lesson identifier. |
| `module_id` | `INTEGER` | `NOT NULL`, `FK -> modules.id (CASCADE)` | Parent module reference. |
| `title` | `VARCHAR(255)` | `NOT NULL` | Lesson title. |
| `content_type` | `VARCHAR(50)` | `NOT NULL` | Learning medium: `'reading'`, `'video'`, `'lab'`. |
| `duration_minutes`| `INTEGER` | `DEFAULT 15` | Expected completion duration. |
| `content` | `TEXT` | `NULLABLE` | Markdown lesson notes, regulatory excerpts, or guide. |
| `video_url` | `VARCHAR(500)` | `NULLABLE` | Streamable institutional lecture URL. |
| `activity_question` | `TEXT` | `NULLABLE` | Formative concept-check question. |
| `activity_options_json` | `TEXT` | `NULLABLE` | JSON array of MCQ options. |
| `activity_correct_option`| `INTEGER` | `NULLABLE` | Zero-indexed integer of correct choice. |
| `activity_explanation` | `TEXT` | `NULLABLE` | Administrative reasoning and official manual citation. |
| `order` | `INTEGER` | `DEFAULT 1` | Sequence within module. |

#### Table: `public.skills` & `public.course_skills`
Official National Competency Framework taxonomy and course mappings.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY` | Skill identifier. |
| `name` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | Competency name (e.g., *Index Number Theory, CERT-In DFIR*). |
| `category` | `VARCHAR(100)` | `NOT NULL` | High-level competency domain. |
| `course_skills.course_id` | `INTEGER` | `FK -> courses.id` | Cross-reference course mapping. |
| `course_skills.skill_id` | `INTEGER` | `FK -> skills.id` | Cross-reference skill mapping. |

---

### Domain 3: Learner Progress & Daily Streaks

#### Table: `public.enrollments`
Tracks learner lifecycle and completion across courses.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Enrollment record. |
| `user_id` | `INTEGER` | `NOT NULL`, `FK -> users.id (CASCADE)` | Enrolled officer. |
| `course_id` | `INTEGER` | `NOT NULL`, `FK -> courses.id (CASCADE)` | Enrolled course. |
| `status` | `VARCHAR(50)` | `DEFAULT 'in_progress'` | Lifecycle state: `'in_progress'`, `'completed'`, `'dropped'`. |
| `progress_percent` | `DOUBLE PRECISION`| `DEFAULT 0.0` | Granular completion progress (0% to 100%). |
| `completed_lessons`| `INTEGER` | `DEFAULT 0` | Total lessons marked completed. |
| `last_accessed` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Recent session access timestamp. |
| `enrolled_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Date enrollment began. |
| `completed_at` | `TIMESTAMPTZ` | `NULLABLE` | Date course was 100% completed. |

#### Table: `public.progress`
Per-lesson atomic completion timestamps.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Progress record. |
| `enrollment_id` | `INTEGER` | `NOT NULL`, `FK -> enrollments.id` | Associated enrollment. |
| `lesson_id` | `INTEGER` | `NOT NULL`, `FK -> lessons.id` | Completed lesson. |
| `is_completed` | `BOOLEAN` | `DEFAULT TRUE` | Completion flag. |
| `completed_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp of lesson completion. |

#### Table: `public.learning_history`
Granular daily activity records for streak calculation and analytics.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | History record. |
| `user_id` | `INTEGER` | `NOT NULL`, `FK -> users.id` | Learner. |
| `date` | `DATE` | `NOT NULL` | Calendar date of study activity. |
| `minutes_spent` | `INTEGER` | `DEFAULT 0` | Total logged study time in minutes. |
| `lessons_completed`| `INTEGER` | `DEFAULT 0` | Lessons completed on this calendar date. |

---

### Domain 4: Statistical Competency & Adaptive Examination (CAT / IRT)

#### Table: `public.assessments`
Final accredited competency assessments and exams.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Assessment identifier. |
| `course_id` | `INTEGER` | `UNIQUE`, `FK -> courses.id` | Associated course. |
| `title` | `VARCHAR(255)` | `NOT NULL` | Assessment title. |
| `description` | `TEXT` | `NULLABLE` | Exam instructions and scope. |
| `passing_score` | `INTEGER` | `DEFAULT 70` | Required minimum percentage to pass (typically 70%). |
| `time_limit_minutes`| `INTEGER` | `DEFAULT 30` | Maximum allowed exam duration. |
| `total_questions` | `INTEGER` | `DEFAULT 10` | Total questions presented. |

#### Table: `public.questions`
Item Bank containing psychometric Item Response Theory (IRT) calibrated parameters.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Question identifier. |
| `assessment_id` | `INTEGER` | `NOT NULL`, `FK -> assessments.id` | Parent assessment. |
| `question_text` | `TEXT` | `NOT NULL` | Question statement, scenario, or formulation. |
| `options_json` | `TEXT` | `NOT NULL` | JSON array of 4 answer options. |
| `correct_option` | `INTEGER` | `NOT NULL` | Index of correct option (0-3). |
| `explanation` | `TEXT` | `NOT NULL` | Detailed statistical derivation and policy manual citation. |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'medium'` | Categorical tier: `'easy'`, `'medium'`, `'hard'`. |
| `irt_difficulty_b` | `DOUBLE PRECISION`| `DEFAULT 0.0` | **IRT Parameter $b$**: Location parameter on ability scale $\theta \in [-3, +3]$. |
| `irt_discrimination_a`| `DOUBLE PRECISION`| `DEFAULT 1.0` | **IRT Parameter $a$**: Steepness of item characteristic curve ($a > 0$). |
| `irt_guessing_c` | `DOUBLE PRECISION`| `DEFAULT 0.25` | **IRT Parameter $c$**: Pseudo-chance guessing lower asymptote (0.25 for 4-option MCQ). |

#### Table: `public.assessment_attempts`
Records full item-by-item response history and latent trait ability estimates $\hat{\theta}$.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Attempt identifier. |
| `user_id` | `INTEGER` | `NOT NULL`, `FK -> users.id` | Examinee officer. |
| `assessment_id` | `INTEGER` | `NOT NULL`, `FK -> assessments.id`| Exam attempted. |
| `score_percent` | `DOUBLE PRECISION`| `NOT NULL` | Classical percentage score achieved. |
| `passed` | `BOOLEAN` | `NOT NULL` | Pass/fail determination against passing standard. |
| `answers_json` | `TEXT` | `NOT NULL` | JSON map of question IDs to selected answers and correctness. |
| `theta_estimate` | `DOUBLE PRECISION`| `DEFAULT 0.0` | Converged Maximum Likelihood / EAP latent ability estimate $\hat{\theta}$. |
| `standard_error` | `DOUBLE PRECISION`| `DEFAULT 0.5` | Standard Error of Measurement (SEM) $SE(\hat{\theta})$. |
| `attempted_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Examination timestamp. |

---

### Domain 5: Technical Competency & Interactive Hands-on Labs

#### Table: `public.technical_transcripts`
Raw and chunked video/audio transcripts ingested for curriculum pipeline.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Transcript record identifier. |
| `course_id` | `INTEGER` | `FK -> courses.id (SET NULL)` | Associated technical course (Course 3). |
| `title` | `VARCHAR(255)` | `NOT NULL` | Video lecture or pipeline transcript title. |
| `raw_text` | `TEXT` | `NOT NULL` | Raw transcribed text (Whisper / manual captioning). |
| `cleaned_text` | `TEXT` | `NOT NULL` | Normalized text with noise and fillers eliminated. |
| `chunks_json` | `TEXT` | `NOT NULL` | JSON array of chunked sections with timestamps and word boundaries. |
| `metadata_json` | `TEXT` | `NULLABLE` | Ingestion metadata, source URL, duration, speaker. |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Ingestion timestamp. |

#### Table: `public.technical_learning_objectives`
Extracted Bloom's Taxonomy actionable coding objectives.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Objective identifier. |
| `transcript_id` | `INTEGER` | `FK -> technical_transcripts.id (CASCADE)` | Parent transcript source. |
| `objective` | `TEXT` | `NOT NULL` | Concrete coding objective (e.g., *Filter missing records using Pandas*). |
| `skill` | `VARCHAR(255)` | `NOT NULL`, `INDEXED` | Specific technical skill (e.g., *Data Cleaning, Vectorization*). |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Coding complexity tier. |
| `action_verb` | `VARCHAR(100)` | `NOT NULL` | Bloom's action verb (*Implement, Debug, Parse*). |
| `assessment_mode`| `VARCHAR(50)` | `DEFAULT 'lab'` | Evaluative mode (`'lab'`, `'marimo'`, `'quiz'`). |
| `suitability_reason`| `TEXT` | `NULLABLE` | Justification for automated sandbox testing. |

#### Table: `public.technical_lab_templates`
Curated human golden templates for reproducible coding exercises.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `VARCHAR(100)` | `PRIMARY KEY` | Stable template key (e.g., `tmpl_pandas_cleaning_01`). |
| `title` | `VARCHAR(255)` | `NOT NULL` | Human-readable title. |
| `skill` | `VARCHAR(255)` | `NOT NULL`, `INDEXED` | Target competency skill. |
| `language` | `VARCHAR(50)` | `DEFAULT 'python'` | Programming runtime (`python`, `sql`, `r`). |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Difficulty tier. |
| `lab_type` | `VARCHAR(100)` | `DEFAULT 'implementation'`| Lab style (`implementation`, `pipeline`, `audit`). |
| `tags_json` | `TEXT` | `DEFAULT '[]'` | JSON array of categorical tags. |
| `instructions_template`| `TEXT` | `NOT NULL` | Markdown instructions with parameter placeholders. |
| `starter_code_template`| `TEXT` | `NOT NULL` | Boilerplate code given to learner. |
| `solution_template` | `TEXT` | `NULLABLE` | Verified reference solution template. |
| `constraints_json` | `TEXT` | `DEFAULT '[]'` | Memory, execution time, and package constraints. |
| `test_cases_template_json`| `TEXT`| `DEFAULT '[]'` | Unit test cases run against learner code. |

#### Table: `public.technical_generated_labs`
Instantiated interactive exercises generated from templates & objectives.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Generated lab instance identifier. |
| `template_id` | `VARCHAR(100)` | `FK -> technical_lab_templates.id (SET NULL)` | Source golden template. |
| `objective_id` | `INTEGER` | `FK -> technical_learning_objectives.id (SET NULL)` | Associated objective. |
| `title` | `VARCHAR(255)` | `NOT NULL` | Instantiated exercise title. |
| `objective` | `TEXT` | `NOT NULL` | Core task description. |
| `language` | `VARCHAR(50)` | `DEFAULT 'python'` | Runtime language. |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Difficulty rating. |
| `instructions` | `TEXT` | `NOT NULL` | Formatted prompt instructions. |
| `starter_code` | `TEXT` | `NOT NULL` | Starter code rendered in editor. |
| `constraints_json`| `TEXT` | `DEFAULT '[]'` | Execution constraints. |
| `test_cases_json` | `TEXT` | `DEFAULT '[]'` | JSON array of executable test assertions. |
| `expected_behavior`| `TEXT` | `NULLABLE` | Expected output format and terminal response. |
| `status` | `VARCHAR(50)` | `DEFAULT 'draft'` | Status (`'draft'`, `'validated'`, `'published'`). |

#### Table: `public.technical_lab_solutions` & `technical_lab_validation_results`
Reference solutions and Docker execution test telemetry.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `technical_lab_solutions.lab_id` | `INTEGER` | `UNIQUE`, `FK -> technical_generated_labs.id` | Lab foreign key. |
| `technical_lab_solutions.reference_code` | `TEXT` | `NOT NULL` | Validated model solution. |
| `technical_lab_solutions.explanation` | `TEXT` | `NULLABLE` | Pedagogical rationale. |
| `technical_lab_validation_results.is_valid` | `BOOLEAN` | `DEFAULT FALSE` | Unit test execution outcome. |
| `technical_lab_validation_results.exit_code` | `INTEGER` | `DEFAULT 0` | Process exit status. |
| `technical_lab_validation_results.execution_time_ms`| `DOUBLE PRECISION`| `DEFAULT 0.0` | Runtime duration in milliseconds. |
| `technical_lab_validation_results.stdout` | `TEXT` | `NULLABLE` | Standard output stream captured from sandbox. |
| `technical_lab_validation_results.stderr` | `TEXT` | `NULLABLE` | Error stream captured if sandbox tests fail. |

---

### Domain 6: Digital Governance & Cyber Defense CTF Sandbox

#### Table: `public.cyber_sandbox_templates`
Authoritative blueprints for defensive cyber forensics, incident response, and governance challenges.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `VARCHAR(100)` | `PRIMARY KEY` | Template key (e.g., `tmpl_phishing_dfir_01`). |
| `title` | `VARCHAR(255)` | `NOT NULL` | Investigation title. |
| `category` | `VARCHAR(100)` | `NOT NULL`, `INDEXED` | DFIR domain: `'Incident Response'`, `'SOC Analysis'`, `'Cloud Security'`, `'DPI Security'`. |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Difficulty: `'beginner'`, `'intermediate'`, `'advanced'`. |
| `competency_id` | `VARCHAR(100)` | `DEFAULT 'soc_investigation'` | Competency axis: `'soc_investigation'`, `'phishing_analysis'`, `'cloud_security'`, `'dpi_security'`, `'digital_forensics'`. |
| `points` | `INTEGER` | `DEFAULT 100` | Base points awarded upon solving. |
| `duration_minutes`| `INTEGER` | `DEFAULT 45` | Recommended time limit. |
| `tags_json` | `TEXT` | `DEFAULT '[]'` | Search keywords and frameworks. |
| `mitre_techniques_json`| `TEXT` | `DEFAULT '[]'` | Mapped MITRE ATT&CK technique IDs (e.g., `["T1078", "T1566"]`). |
| `scenario_template`| `TEXT` | `NOT NULL` | CERT-In simulated incident backdrop markdown. |
| `instructions_template`| `TEXT`| `NOT NULL` | Investigation briefing and triage steps. |
| `hints_template_json`| `TEXT` | `DEFAULT '[]'` | Multi-tier guidance hints with scoring deductions. |
| `artifacts_spec_json`| `TEXT` | `DEFAULT '{}'` | Specification of auth logs, PCAP headers, or cloud trails. |

#### Table: `public.cyber_sandbox_challenges`
Procedurally generated or flagship challenges with unique cryptographic verification flags.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `VARCHAR(100)` | `PRIMARY KEY` | Challenge identifier (e.g., `chal_soc_auth_001`). |
| `template_id` | `VARCHAR(100)` | `FK -> cyber_sandbox_templates.id (SET NULL)` | Parent blueprint reference. |
| `title` | `VARCHAR(255)` | `NOT NULL` | Challenge title. |
| `category` | `VARCHAR(100)` | `NOT NULL`, `INDEXED` | DFIR category. |
| `difficulty` | `VARCHAR(50)` | `DEFAULT 'intermediate'` | Difficulty level. |
| `points` | `INTEGER` | `DEFAULT 100` | Solved score value. |
| `duration_minutes`| `INTEGER` | `DEFAULT 45` | Time allocation. |
| `competency_id` | `VARCHAR(100)` | `DEFAULT 'soc_investigation'` | Skill domain. |
| `is_flagship` | `BOOLEAN` | `DEFAULT FALSE`, `INDEXED` | Featured core challenge in national training module. |
| `tags_json` | `TEXT` | `DEFAULT '[]'` | Categorical tags. |
| `mitre_techniques_json`| `TEXT`| `DEFAULT '[]'` | MITRE ATT&CK mappings. |
| `objectives_json`| `TEXT` | `DEFAULT '[]'` | Specific deliverables required from the officer. |
| `scenario_markdown`| `TEXT` | `NOT NULL` | Detailed incident briefing presented in the UI. |
| `flag` | `VARCHAR(255)` | `NOT NULL` | Master verification flag format: `FLAG{...}`. |
| `hints_json` | `TEXT` | `DEFAULT '[]'` | Active hints with penalty deduction points. |
| `artifacts_json` | `TEXT` | `DEFAULT '{}'` | Map of simulated log files, headers, and certificates. |
| `notebook_code` | `TEXT` | `NOT NULL` | Executable Marimo reactive Python notebook investigating evidence. |

#### Table: `public.cyber_sandbox_sessions`
Ephemeral Marimo container runtime allocations assigned per officer.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `VARCHAR(100)` | `PRIMARY KEY` | Unique session key (`sess_<random_hex>`). |
| `user_id` | `INTEGER` | `FK -> users.id (CASCADE)` | Officer conducting investigation. |
| `challenge_id` | `VARCHAR(100)` | `NOT NULL`, `FK -> cyber_sandbox_challenges.id` | Target challenge. |
| `status` | `VARCHAR(50)` | `DEFAULT 'running'`, `INDEXED`| Lifecycle state: `'running'`, `'stopped'`, `'expired'`, `'solved'`. |
| `assigned_port` | `INTEGER` | `NOT NULL` | Localhost or container port assigned to interactive Marimo instance. |
| `flag` | `VARCHAR(255)` | `NOT NULL` | Session-specific dynamic flag to prevent plagiarized answers. |
| `unlocked_hints_json`| `TEXT`| `DEFAULT '[]'` | Array of hint indices unlocked by user during session. |
| `total_penalties`| `INTEGER` | `DEFAULT 0` | Cumulative score penalty from unlocked hints. |
| `final_score` | `INTEGER` | `DEFAULT 0` | Points awarded upon successful flag submission. |
| `is_solved` | `BOOLEAN` | `DEFAULT FALSE` | True once user submits the matching cryptographic flag. |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Session launch timestamp. |
| `expires_at` | `TIMESTAMPTZ` | `NOT NULL` | Hard deadline timestamp when container auto-terminates. |
| `solved_at` | `TIMESTAMPTZ` | `NULLABLE` | Timestamp when correct flag was verified. |

#### Table: `public.user_cyber_competencies`
Aggregate civil service cyber defense score across the 5 national pillars.

| Field Name | Type | Constraints | Description & Usage |
|---|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` | Competency record identifier. |
| `user_id` | `INTEGER` | `UNIQUE`, `NOT NULL`, `FK -> users.id (CASCADE)`| Civil servant account. |
| `soc_investigation`| `INTEGER`| `DEFAULT 0` | Accumulated points in SOC log analysis & triage. |
| `phishing_analysis`| `INTEGER`| `DEFAULT 0` | Points in spear-phishing deobfuscation & headers. |
| `cloud_security` | `INTEGER` | `DEFAULT 0` | Points in MeghRaj / AWS / Azure cloud auditing. |
| `dpi_security` | `INTEGER` | `DEFAULT 0` | Points in India Stack API security & HMAC verification. |
| `digital_forensics`| `INTEGER`| `DEFAULT 0` | Points in memory, disk, and Linux forensics. |
| `total_score` | `INTEGER` | `DEFAULT 0`, `INDEXED` | Cumulative cyber score for national cadre ranking. |
| `solved_challenges_count`| `INTEGER`| `DEFAULT 0` | Total distinct challenges solved. |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Last score update timestamp. |

---

## 4. Row Level Security (RLS) & Authorization Architecture

Supabase provides granular **Row Level Security (RLS)** to enforce strict institutional data isolation:

```sql
-- 1. Read access for curricula & public challenge templates
ALTER TABLE public.cyber_sandbox_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to cyber templates" 
    ON public.cyber_sandbox_templates FOR SELECT USING (true);

-- 2. Strict isolation for user runtime sandbox sessions
ALTER TABLE public.cyber_sandbox_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow users to view own cyber sessions" 
    ON public.cyber_sandbox_sessions FOR SELECT 
    USING (auth.uid()::text = user_id::text OR user_id IS NULL);

CREATE POLICY "Allow users to operate own cyber sessions" 
    ON public.cyber_sandbox_sessions FOR ALL 
    USING (auth.uid()::text = user_id::text);

-- 3. Competency scores are readable across cadre for transparent rankings
ALTER TABLE public.user_cyber_competencies ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to cyber competencies" 
    ON public.user_cyber_competencies FOR SELECT USING (true);

CREATE POLICY "Allow users to update own cyber competencies" 
    ON public.user_cyber_competencies FOR ALL 
    USING (auth.uid()::text = user_id::text);
```

---

## 5. Backend Supabase Client Usage & Environment Config

FastAPI integrates with Supabase via `backend/app/core/config.py` and dedicated service modules:

| Environment Variable | Description | Backend Scope |
|---|---|---|
| `SUPABASE_URL` | Supabase project API gateway endpoint (`https://<id>.supabase.co`). | Core database client & storage. |
| `SUPABASE_KEY` / `SUPABASE_ANON_KEY` | Public anon key for client-safe queries. | Unauthenticated health checks and catalog sync. |
| `SUPABASE_SERVICE_ROLE_KEY` | High-privilege service key bypassing RLS. | Backend trusted data ingestion and admin scoring. |

### Supabase Service Class (`app/modules/digital_governance/services/supabase_service.py`)
Provides resilient fallback and synchronization methods:
- `is_configured()`: Inspects if valid credentials are present in runtime environment.
- `sync_challenge(challenge_data)`: Upserts CTF challenges to remote Supabase repository.
- `record_session(session_data)`: Telemeters active container port allocations and timestamps.
- `update_competency(user_id, competency_scores)`: Synchronizes national cyber scores with cloud datastore.
- `get_flagship_challenges()`: Reads flagship exercises with automatic fallback to local database if offline.

---

## 6. Migration Execution Guide

To execute these migrations against a remote Supabase instance:

```bash
# 1. Install Supabase CLI (if not already installed)
npm install -g supabase

# 2. Link your local project to the Supabase remote project
supabase link --project-ref <your-project-id>

# 3. Apply all sequential migrations
supabase db push

# 4. Alternatively, execute migrations directly using psql:
psql "$DATABASE_URL" -f supabase/migrations/20260910000000_initial_schema.sql
psql "$DATABASE_URL" -f supabase/migrations/20260914000001_technical_course_pipeline.sql
psql "$DATABASE_URL" -f supabase/migrations/20260914000002_digital_governance_cybersecurity.sql
```
