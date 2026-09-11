# Statistical Competency Engine — Architecture

## 1. Overview & System Purpose

The **Statistical Competency Engine** is an independent, deterministic backend service designed to power competency-based training, assessment, and adaptive progression across India's civil services (under MoSPI and Capacity Building Commission mandates).

The engine enforces a strict separation between **statistical truth** and **presentation**:
- All computations, parameter generation, answer keys, scoring, chart datasets, and validations are **deterministic**.
- An LLM (when enabled) acts strictly as a language transformer for explanations or scenarios, but never as an authoritative source of numerical truth.
- The LMS portal interacts with the engine exclusively through stable JSON APIs.

---

## 2. Component Pipeline

```text
Competency Hierarchy (JSON)
          ↓
Skill & Difficulty Selection (Personalization Engine)
          ↓
Question Template Definition
          ↓
Parameter Generator (Pseudo-Random with Seed)
          ↓
Deterministic Statistics Module (PriceStatisticsModule)
          ↓
Answer Key + Misconception Distractors
          ↓
Pre-Flight Validator (QuestionValidator)
          ↓
Chart Specification Generator (ChartGenerator)
          ↓
HTTP / JSON API Response (/questions/next)
          ↓
Learner Submits Answer (/questions/submit)
          ↓
Deterministic Answer Evaluation (Server-side)
          ↓
Mastery Update (0-100 Normalized Scale)
          ↓
Declarative Branching Engine (Next Question / Remediation)
```

---

## 3. Directory Layout

```text
backend/
├── app/
│   ├── statistical_engine/
│   │   ├── api/
│   │   │   └── router.py              # FastAPI endpoints (/api/v1/stats, questions, etc.)
│   │   ├── competency/
│   │   │   ├── graph.py               # Competency graph & prerequisite validator
│   │   │   └── mastery.py             # 0-100 mastery tracking & level transitions
│   │   ├── core/
│   │   │   └── exceptions.py          # Structured domain exceptions
│   │   ├── questions/
│   │   │   ├── generator.py           # Template-driven question instance generator
│   │   │   ├── distractors.py         # Misconception-based distractor engine
│   │   │   ├── validator.py           # Pre-flight question integrity validator
│   │   │   ├── branching.py           # Declarative pedagogical branching rules
│   │   │   └── personalization.py     # Rule-based skill & difficulty progression
│   │   ├── charts/
│   │   │   └── generator.py           # Frontend-agnostic chart specifications
│   │   ├── repositories/
│   │   │   └── memory_repositories.py # In-memory & pluggable persistence interfaces
│   │   ├── schemas/                   # Pydantic request/response models
│   │   ├── stats/
│   │   │   ├── base.py                # BaseStatisticalModule abstract class
│   │   │   └── price_statistics.py    # Pure, deterministic calculations (Price Stats)
│   │   └── config.py                  # Engine configuration & path resolution
├── content/
│   ├── competencies/
│   │   └── price_statistics.json      # Price Statistics skills & prerequisites
│   └── questions/
│       └── price_statistics.json      # Parameterized question templates
└── tests/
    └── stats_engine/                  # Automated pytest suite (29 tests)
```
