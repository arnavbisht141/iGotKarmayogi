# Architecture and domain boundaries

## Current implementation

The browser talks only to the LMS backend at `NEXT_PUBLIC_API_URL` (normally `http://localhost:8000/api`). The backend is a modular FastAPI application and is the system of record for users, roles, courses, enrolments, learning progress, assessments, certificates, and administration.

The current LangGraph assistant still runs inside the LMS backend. The `ai-service` directory contains documentation only and reserves a future independently deployable AI boundary. No AI runtime was created or extracted during this repository reorganization.

```text
Browser -> Frontend -> LMS backend -> LMS data store
                              |
                              +-> existing in-process assistant

Future: LMS backend -> AI service -> model providers
```

This preserves a single client API and prevents model prompts from becoming a second source of truth for LMS data.

## Responsibilities

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Frontend | presentation and calls to LMS API | business records or provider keys |
| LMS backend | authorization, LMS rules, data mutations, AI context shaping | direct browser exposure of AI providers |
| Future AI service | orchestration, prompts, provider selection, response generation | LMS persistence, certificate decisions, user authorization |
| Model providers | generated text | platform truth or authoritative decisions |

## Planned extensions

Retrieval, ingestion, evaluation, guardrails, background jobs, audit/telemetry, and long-term conversation state are deliberate future subsystems. They are documented rather than represented as empty directories because their data classification, retention, access control, and operating model are not yet approved.
