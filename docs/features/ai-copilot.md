# 🤖 AI Copilot (Karmayogi AI Assistant)

> **Status:** `Implemented` (Phase 0)  
> **Primary Modules:** `backend/app/agents/`, `frontend/src/components/shared/AiAssistantWidget.tsx`  
> **Backend Endpoint:** `POST /api/agents/chat`  
> **Architectural Boundary:** In-process assistant within LMS backend; future extraction reserved in `ai-service/`  

---

## 1. Executive Summary & Problem Statement

Civil servants and statistical officers navigating specialized government methodologies (such as NSS multi-stage sampling, CPI Laspeyres index compilation, PFMS Treasury Single Accounts, and UN-NQAF data quality standards) require on-demand doubt clearance, policy guidance, and course recommendations directly within their learning workflows.

The **Karmayogi AI Assistant** provides an intelligent, context-aware conversational agent tailored for public service without relying solely on external commercial LLM APIs.

---

## 2. User Persona & Experience

- **Target Persona:** All civil servants, evaluators, and learners across all ministries.
- **Access Point:** Persistent floating circular launcher button (`AiAssistantWidget.tsx`) accessible on the bottom-right corner of every screen.
- **Brand Identity:** Dignified institutional styling labeled *"Karmayogi AI - Civil Service Intelligence Assistant"* with no vendor or third-party engine badges.

---

## 3. Workflow Mechanics & Architecture

```
[User Chat Request] ──▶ POST /api/agents/chat ──▶ LangGraph StateGraph
                                                          │
                    ┌─────────────────────────────────────┴─────────────────────────────────────┐
                    ▼                                     ▼                                     ▼
          [Google Gemini Key?]                  [OpenAI Key?]                       [No External Keys?]
                    │                                     │                                     │
           Invoke Gemini 1.5 Flash                Invoke GPT-4o-Mini               Invoke MoSPI Fallback Engine
       (source: "langgraph-gemini")          (source: "langgraph-openai")       (source: "langgraph-karmayogi-engine")
                    │                                     │                                     │
                    └─────────────────────────────────────┬─────────────────────────────────────┘
                                                          ▼
                                             [Structured Chat Response]
```

### Deterministic MoSPI Domain Fallback Engine
When neither `GOOGLE_API_KEY` nor `OPENAI_API_KEY` is present in the runtime environment, the assistant gracefully falls back to a deterministic MoSPI statistical knowledge engine (`backend/app/agents/router.py`). It reliably answers queries concerning:
1. **Consumer Price Index (CPI) & Inflation:** Modified Laspeyres formula, 2012=100 base year, geometric mean elementary quotes, item basket weighting.
2. **NSS Survey Methodologies:** Multi-stage stratified sampling, First Stage Units (FSUs), hamlet-group formation, enterprise surveys.
3. **PFMS & Governance:** Treasury Single Account (TSA) mechanics, Just-in-Time funding, Aadhaar Payment Bridge.
4. **Platform & Assessment Policies:** 70% passing threshold, retake rules, accredited digital competency badges.
5. **Policy Coding:** Vectorized Pandas routines vs. Python loops for high-throughput public microdata processing.

---

## 4. Technical Specifications

### 4.1 Frontend Component (`frontend/src/components/shared/AiAssistantWidget.tsx`)
- **Trigger:** Circular button (`h-14 w-14 rounded-full bg-[#965C66] hover:bg-[#824E57] text-white shadow-lg border border-white/20`) with online status badge.
- **Drawer / Dialog:** Expandable clean chat modal styled in the Muted Rose standard (`#965C66` header, `#EEE8E9` background).
- **Communication:** Sends JSON `{ message: string, history?: [...] }` to `/api/agents/chat`.
- **Response Handling:** Renders structured markdown, message timestamps, and provider attribution (subtly displayed).

### 4.2 Backend Implementation (`backend/app/agents/router.py`)
- **Framework:** LangGraph + LangChain Core (`StateGraph` workflow compilation).
- **Endpoint:** `POST /api/agents/chat` (also aliased under `/agents/chat`).
- **Input Schema (`ChatRequest`):**
  - `message: str` — Current user query.
  - `history: Optional[List[Dict[str, str]]]` — Conversation history.
  - `course_id: Optional[str]` — Optional course context to narrow responses.
- **Output Schema (`ChatResponse`):**
  - `reply: str` — Assistant answer formatted in markdown.
  - `source: str` — Origin of response (`"langgraph-gemini"`, `"langgraph-openai"`, or `"langgraph-karmayogi-engine"`).
  - `timestamp: datetime` — Response generation timestamp.

---

## 5. Rules & Operational Guidelines for AI Agents

> [!CAUTION]
> **Zero External Dependency Lock:**
> The assistant must NEVER fail or return an unhandled 500 error if external model provider API keys are missing or invalid. Any change to `backend/app/agents/router.py` must maintain the deterministic MoSPI fallback engine.

> [!IMPORTANT]
> **Architectural Boundary (ADR 0001 & ADR 0002):**
> The assistant is an in-process component of the FastAPI backend in Phase 0. Do NOT create duplicate data stores or expose provider keys directly to the browser. The `ai-service/` directory is reserved for future extraction.

> [!TIP]
> **UI Aesthetic Consistency:**
> Do NOT revert the chat widget to generic chat bubbles with glowing neon AI badges or purple cyberpunk gradients. Adhere strictly to `#965C66` and neutral slate surfaces.
