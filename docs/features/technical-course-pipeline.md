# 🛠️ Technical Course Content Generation Pipeline

> **Document Type:** Feature Specification & Architectural Manual  
> **Domain Subsystem:** Content Generation Pipeline — Technical Courses  
> **Status:** `Implemented` (Phase 0 / SIH '26 MVP)  
> **Module Path:** `backend/app/modules/technical_courses/`  
> **API Prefix:** `/api/technical-courses`  
> **Architectural Boundary:** Autonomous domain module within the modular monolith; interoperable with future statistical, governance, and behavioural generation pipelines.

---

## 1. Executive Summary & Problem Statement

Technical learning on iGOT Karmayogi requires civil servants and public sector engineers to acquire practical, hands-on capabilities (such as REST API implementation, survey data processing with Pandas, SQL analytics, and automated data validation) rather than passive video watching or purely theoretical multiple-choice quizzes.

The **Technical Course Content Generation Pipeline** ingests raw technical lecture transcripts and deterministically produces **validated, deployable hands-on coding labs**.

### Core Architectural Philosophy

```
Controlled Templates + Structured LLM Output + Deterministic Validation + Isolated Sandbox
```

Rather than prompting an LLM to freely invent arbitrary lab instructions and test architectures (which causes non-deterministic tests and hallucinations), this pipeline enforces:
1. **Human-Created Lab Templates:** Human instructional designers define constraints, starter code structure, and unit test harnesses.
2. **Controlled LLM Synthesis:** The LLM fills variable details to adapt the template to the specific course context.
3. **Reference Solution Validation:** An automated reference solution is generated and treated as **untrusted** until proven in an isolated execution sandbox.
4. **Isolated Sandbox Testing:** Solutions are executed against unit test suites inside an isolated Docker sandbox (with subprocess fallback for development).
5. **Quality Gate:** Only labs whose solutions pass 100% of test assertions in the sandbox are marked `validated` and stored for deployment.

---

## 2. Pipeline Workflow & Architecture

```
Technical Course Transcript (Video / Notes)
                 │
                 ▼
     [1. Transcript Processing]
     • Normalization & Cleaning (WebVTT / SRT / audio cue stripping)
     • Overlapping Semantic Chunking & Token Estimation
                 │
                 ▼
     [2. Structured Learning Objective Extraction]
     • Schema: objective, skill, difficulty, action verb
     • LLM: Groq (Primary) ──▶ OpenAI (Fallback 1) ──▶ Gemini (Fallback 2) ──▶ Deterministic Dev Engine
                 │
                 ▼
     [3. Quiz vs. Lab Decision Layer]
     • Bloom Taxonomy analysis + keyword scoring
     • High-order application (implement, debug, analyze) ──▶ LAB
     • Low-order recall (define, list, recall) ─────────────▶ QUIZ
                 │ (If Lab)
                 ▼
     [4. Human-Created Lab Template Matching]
     • Matches objective metadata (skill, difficulty, language, lab type, tags)
     • Human controls constraints, starter code skeleton, and test harnesses
                 │
                 ▼
     [5. Controlled Lab Generation]
     • Injects context into matched template
     • Strict Pydantic validation (GeneratedLabSchema)
                 │
                 ▼
     [6. Reference Solution Generation]
     • Synthesizes reference implementation
     • Marked 'untrusted' until sandbox verified
                 │
                 ▼
     [7. Isolated Sandbox Validation]
     • Primary Engine: Docker Container (--network none, memory limit, timeout, non-root)
     • Fallback Engine: Subprocess Sandbox (isolated temp workspace, strict timeout)
     • Runs test assertion harness and captures stdout, stderr, execution time
                 │
      ┌──────────┴──────────┐
      ▼ (All Tests Pass)    ▼ (Test Fails / Error)
[Mark Lab: VALIDATED]   [Mark Lab: REJECTED]
      │
      ▼
Persist in SQLite DB / Return to Orchestrator
```

---

## 3. Database Schema & Domain Models

All models reside in `backend/app/models/models.py`:

| Model Name | Table Name | Purpose |
|---|---|---|
| `TechnicalTranscript` | `technical_transcripts` | Stores raw text, cleaned text, chunk JSON, and metadata. |
| `TechnicalLearningObjective` | `technical_learning_objectives` | Structured learning objectives extracted from transcripts. |
| `TechnicalLabTemplate` | `technical_lab_templates` | Human-created lab templates with instructions, starter code, constraints, and test harness templates. |
| `TechnicalGeneratedLab` | `technical_generated_labs` | Concrete lab instances with status (`draft`, `pending_validation`, `validated`, `rejected`). |
| `TechnicalLabSolution` | `technical_lab_solutions` | Candidate reference solution code and explanation. |
| `TechnicalLabValidationResult` | `technical_lab_validation_results` | Execution results, exit code, execution time (ms), stdout, stderr, test summary JSON. |

---

## 4. API Endpoints

All endpoints are mounted under `/api/technical-courses`:

### 4.1 Transcript Ingestion
`POST /api/technical-courses/process`
- **Request:** `{ "title": "FastAPI Course", "raw_text": "...", "course_id": 1 }`
- **Response:** Cleaned text metrics, estimated tokens, semantic chunks.

### 4.2 Objective Extraction
`POST /api/technical-courses/objectives`
- **Request:** `{ "transcript_text": "...", "transcript_id": 1 }`
- **Response:** List of structured objectives with skill, difficulty, action, assessment mode (`lab` or `quiz`).

### 4.3 Quiz vs. Lab Decision
`POST /api/technical-courses/decide-mode`
- **Request:** `{ "objective": "Implement REST API route", "skill": "FastAPI", "action": "implement" }`
- **Response:** Assessment mode, confidence (0.0–1.0), reasoning, recommended lab type.

### 4.4 List Lab Templates
`GET /api/technical-courses/templates`
- **Response:** List of human-created templates in the catalog.

### 4.5 Match Template
`POST /api/technical-courses/match-template`
- **Request:** `{ "objective": "...", "skill": "Pandas", "language": "python" }`
- **Response:** Matched template details, match score, match reasoning.

### 4.6 Lab Generation
`POST /api/technical-courses/labs/generate`
- **Request:** `{ "objective": {...}, "template_id": "python-fastapi-crud-001" }`
- **Response:** Generated concrete lab adhering to `GeneratedLabSchema`.

### 4.7 Solution Generation
`POST /api/technical-courses/labs/{lab_id}/solution`
- **Response:** Reference solution code, explanation, `is_trusted: false`.

### 4.8 Sandbox Validation
`POST /api/technical-courses/labs/{lab_id}/validate`
- **Response:** Execution details, pass/fail status, individual test case durations.

### 4.9 Get Lab Details
`GET /api/technical-courses/labs/{lab_id}`
- **Response:** Complete lab details, reference solution, latest validation results, and validation history.

### 4.10 Full End-to-End Orchestration
`POST /api/technical-courses/pipeline/run-full`
- **Request:** `{ "title": "...", "transcript_text": "..." }`
- **Response:** End-to-end execution summary, extracted objectives, generated labs, validated count, timing breakdown.

---

## 5. Security & Sandbox Execution

- **Primary Sandbox Engine:** Docker Container with `--network none`, `--memory 128m`, `--cpus 0.5`, read-only workspace mount (`-v <temp_dir>:/sandbox:ro`), execution timeout (5s).
- **Development/Testing Fallback:** Isolated temporary directory, minimal environment variables (`PYTHONPATH=""`), strict `subprocess.run(timeout=5)`.
- **Untrusted Code Policy:** All LLM-generated code is treated as untrusted and never executed directly in the main backend process.

---

## 6. Verification & Automated Testing

The module is verified with a 22-test automated test suite in `backend/tests/test_technical_pipeline.py`:

```bash
cd backend
python -m pytest tests/test_technical_pipeline.py -v
```

Test coverage includes:
- Transcript subtitle stripping, chunking, and noise handling.
- Structured objective extraction and classification.
- Heuristic and Bloom taxonomy decision resolution.
- Human template matching and ranking.
- Template filling and Pydantic schema validation.
- Solution generation and untrusted status tracking.
- Sandbox validation under passing, failing, syntax error, and timeout conditions.
- End-to-end API integration and SQLite database persistence.

---

## 7. Current Implementation vs. Future Scope

| Component | Implemented (Phase 0 / SIH '26 MVP) | Planned Future Scope (Phase 1+) |
|---|---|---|
| **Course Transcript** | WebVTT/SRT cleaning, semantic chunking, token estimation. | Direct YouTube/Whisper audio transcription integration. |
| **Templates** | Human-created catalog for REST APIs, Pandas data pipelines, and Python debugging. | Visual template authoring GUI for instructors. |
| **LLM Synthesis** | Groq (Primary) ──▶ OpenAI (Fallback 1) ──▶ Gemini (Fallback 2) with deterministic dev fallback. | Fine-tuned public-sector code generation model. |
| **Validation** | Docker container sandbox + isolated subprocess fallback. | Distributed Kubernetes execution sandbox with network virtualization. |
| **LMS Integration** | Database models linking generated labs to courses and learning player. | Live interactive browser code editor widget (Monaco/Pyodide). |
