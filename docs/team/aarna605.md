# Aarna — Contribution & Activity Log

> **Name:** Aarna  
> **GitHub Handle:** [@aarna605-dot](https://github.com/aarna605-dot)  
> **Role:** UI/UX Lead & Behavioral Assessment Architect  
> **Primary Subsystems:** Behavioral CGP (Carryforward Case Inquiries, Live Oral Board), Course Detail Behavioral Integration, UI Design System, Two-Column Hero Architecture, Auth Flows  

---

## 1. Summary of Responsibilities
Full-stack and UI/UX design lead for the **iGOT Karmayogi (MoSPI)** platform. Architected the **Behavioral Content Generation Pipeline (CGP)** on `cgp/behav-updated`, encompassing consequential branching case inquiries derived from authentic government statutory notices and a multimodal live oral examination board with real-time video/speech telemetry. Previously established the platform's landing page layout, two-column hero architecture, aspect-ratio preservation engine, and institutional authentication flows.

---

## 2. Visible Deliverables (Code & Repository Artifacts)

### 2.1 Course-Anchored Behavioral Case Inquiries (`backend/app/modules/behavioural_cgp/`, `4333815`)
- **Statutory Notice Corpus (`corpus.py`):** Curated authentic government proceedings across DoPT Rule 14 CCS (CCA) disciplinary inquiries, Ministry of Finance GFR 149/151 GeM procurement notices, RTI First Appeals, and UN-NQAF audits.
- **Carryforward Adaptive Branching (`carryforward_generator.py`, `carryforward_session.py`):** Engineered multi-stage consequential simulation where non-optimal administrative actions branch into regulatory hearings and vigilance inquiries until satisfactorily resolved.
- **6-Competency Evaluation Framework:** Scored performance across *Decision Making*, *Ethical Judgement*, *Leadership*, *Communication*, *Situational Awareness*, and *Accountability* with level bands (*Exemplary*, *Proficient*, *Needs Attention*) and APAR upskilling recommendations.
- **Case Inquiry Interface (`CarryforwardAssessmentPage.tsx`, `/behavioural/cases`):** Interactive decision tree exploration, statutory rationale review, consequence breadcrumbs, and competency dossier.

### 2.2 Multimodal Live Oral Examination Board (`LiveInterviewPage.tsx`, `4333815`, `c917a77`)
- **Course-Grounded AI Interviewer (`interview_service.py`):** Dynamic multi-turn oral examination adapting questions to syllabus themes of selected database courses.
- **Real-Time Telemetry & Audio Visualizer:** Integrated in-browser webcam monitoring (posture stability, head movement, gaze tracking) and Web Audio API frequency equalizer reflecting speech cadence (WPM), acoustic clarity, and filler frequency.
- **Stream Lifecycle Safeguard (`c917a77`):** Bound video elements with dynamic callback refs to guarantee reliable camera stream attachment upon board room entry.
- **Ethical AI Demarcation:** Embedded statutory disclaimers clarifying that observable telemetry reflects neutral physical metrics and does not constitute psychological profiling.

### 2.3 Course-Level Integration & Global Isolation (`CourseDetailPage.tsx`, `cfdff72`)
- **Course-Specific Targeting:** Anchored the Behavioral Pipeline exclusively to supported curriculum courses (`[1, 2, 3, 4, 5]`), rendering the **Behavioural Competency Pipeline** card and **AI Oral Board** button only where statutory notices exist.
- **Clean Navigation Isolation:** Purged sitewide behavioral links from `Navbar.tsx` and removed the global homepage banner from `HomePage.tsx` to maintain clean platform hierarchy.

### 2.4 Automated Test Suite & Backend Routing (`test_behavioural_cgp.py`, `router.py`, `4333815`)
- Built 12 automated unit tests verifying corpus retrieval, dynamic case generation, carryforward session branching, live interview turns, competency rubrics, and diagnostic reports.
- Registered `/api/behavioural` router with PyJWT compatibility and `GEMINI_API_KEY`/`GOOGLE_API_KEY` alias resolution in `config.py`.

### 2.5 UI Foundations & Landing Architecture (Prior Iterations)
- **Hero & Carousel (`page.tsx`):** Designed responsive two-column hero with strict photographic aspect-ratio preservation (`657/301`, `673/290`, `716/395`) and left-aligned statistics grid.
- **Karmayogi AI Widget (`AiAssistantWidget.tsx`):** Rebranded assistant launcher to an ergonomic circular trigger with institutional civil-service styling.
- **Authentication Flows (`login/page.tsx`, `register/page.tsx`):** Elevated card surfaces and responsive focus ring styling.

---

## 3. "Invisible" & Offline Contributions

### 3.1 Civil-Service Administrative & Statutory Research
- Analyzed DoPT CCS (CCA) Rules 1965, General Financial Rules (GFR 2017), Collection of Statistics Act 2008, and UN-NQAF guidelines to formulate authentic administrative dilemmas and consequence paths.

### 3.2 In-Browser WebRTC & Audio Meter Engineering
- Designed low-overhead Web Audio analyser pipelines (`fftSize = 64`) to calculate live speech cadence and volume meters without impacting Next.js rendering performance.

### 3.3 Ethical AI Demarcation & Regulatory Alignment
- Drafted statutory demarcation notices ensuring automated oral board telemetry remains strictly non-diagnostic and aligned with ethical civil-service evaluation norms.

### 3.4 WCAG AA/AAA Accessibility Audit
- Verified 11.4:1 contrast ratios for text readability and keyboard accessibility across interactive decision nodes and media controls.

---

## 4. Chronological Activity Log

| Date | Activity | Category | Notes / Deliverables |
|---|---|---|---|
| `2026-09-13` | Hardened webcam lifecycle with callback ref stream attachment | `Code` / `Fix` | Commit `c917a77` on `cgp/behav-updated` |
| `2026-09-13` | Isolated behavioral features to designated courses (`CourseDetailPage.tsx`) & cleaned navbar | `Code` / `Refactor` | Commit `cfdff72` on `cgp/behav-updated` |
| `2026-09-13` | Built 6-competency rubric, physical/speech telemetry dossier, and 12 unit tests | `Code` / `Backend` | Commit `4333815` on `cgp/behav-updated` |
| `2026-09-12` | Integrated live AI interview board room with Web Audio visualizer and course selection | `Code` / `Full-Stack` | Commit `5d32962` on `cgp/behavioural` |
| `2026-09-12` | Implemented government notice corpus, carryforward case generator, and `/cases` UI | `Code` / `Feature` | Commit `fd7a037` on `cgp/behavioural` |
| `2026-09-06` | Sourced official media assets, built two-column hero and aspect-ratio preservation engine | `Code` / `UI` | PR #2 merged into `main` (`65dbe6e`, `4380504`) |
| `2026-09-06` | Redesigned circular Karmayogi AI assistant launcher and authentication cards | `Code` / `UI` | `AiAssistantWidget.tsx`, `login/page.tsx` (`4380504`) |
| `2026-09-05` | Researched civil-service UI benchmarks (iGOT, UK CSL) and audited WCAG contrast ratios | `Design` / `Research` | Validated 11.4:1 contrast standards |

---

## 5. Notes & Context for Future AI Coding Agents
- **Course Isolation Rule:** The Behavioral Competency Pipeline (Case Inquiries & AI Live Interview) is strictly scoped to designated courses (`[1, 2, 3, 4, 5]`). Do NOT add global navbar links or sitewide homepage banners for this feature.
- **Webcam Mounting Convention:** Always use callback ref binding (`ref={(el) => ...}`) when rendering `<video>` feeds in conditionally mounted board rooms to ensure `srcObject` is assigned reliably across all browser lifecycles.
- **Statutory Notice Integrity:** Maintain authentic citations (CCS Rule 14, GFR 149/151, UN-NQAF) and ensure consequence branching maintains procedural due process (*Audi Alteram Partem*).
- **Ethical Disclaimer:** Retain the `observable_signals_disclaimer` on all live interview reports stating that physical telemetry reflects neutral physical metrics rather than psychological or character assessments.

