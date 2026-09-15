# LMS Portal Integration Guide — Statistical Competency Engine

This document provides complete instructions, API contracts, sequence diagrams, and curl examples for frontend and portal developers integrating the **Statistical Competency Engine**.

---

## 1. Interaction Flow & Sequence Diagram

```text
  Portal (Frontend)             Statistical Engine API
         │                                │
         │  1. POST /questions/next       │
         │───────────────────────────────>│
         │                                │  (Determines learner state,
         │                                │   generates params, calculates
         │                                │   deterministic answer & distractors)
         │  2. Returns QuestionInstance   │
         │<───────────────────────────────│
         │  (Answer key is withheld)      │
         │                                │
  [User answers question]                 │
         │                                │
         │  3. POST /questions/submit     │
         │───────────────────────────────>│
         │                                │  (Evaluates correctness server-side,
         │                                │   updates mastery, triggers branching)
         │  4. Returns SubmissionResponse │
         │<───────────────────────────────│
         │                                │
  [Displays feedback + next action]
```

---

## 2. Base Configuration

- **Development Base URL**: `http://localhost:8000/api/v1` (or `/api` fallback)
- **Headers**:
  ```http
  Content-Type: application/json
  ```

---

## 3. Endpoints Reference

### 3.1 Retrieve Next Adaptive Question
Selects an appropriate question for the learner based on their mastery history.

- **URL**: `POST /api/v1/questions/next`
- **Request Body**:
  ```json
  {
    "user_id": "officer-iss-8842",
    "competency_id": "price_statistics",
    "preferred_skill_id": "price.cpi.weighted_price_relatives"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "question_id": "price.cpi.weighted.mcq.001-839210",
    "skill_id": "price.cpi.weighted_price_relatives",
    "competency_id": "price_statistics",
    "type": "mcq",
    "difficulty": "intermediate",
    "prompt": "A district consumer basket consists of three essential commodity groups with the following price relatives and expenditure weights:\n• Food: Relative = 120, Weight = 45\n• Housing: Relative = 110, Weight = 30\n• Fuel & Light: Relative = 135, Weight = 25\n\nCompute the overall Consumer Price Index (CPI).",
    "data": {
      "rel_food": 120,
      "rel_housing": 110,
      "rel_fuel": 135,
      "w_food": 45,
      "w_housing": 30,
      "w_fuel": 25
    },
    "options": [
      {"id": "A", "text": "120.75"},
      {"id": "B", "text": "121.67"},
      {"id": "C", "text": "115.00"},
      {"id": "D", "text": "128.50"}
    ],
    "chart": null,
    "metadata": {
      "template_id": "price.cpi.weighted.mcq.001",
      "unit": "index_points",
      "seed": 839210
    }
  }
  ```

---

### 3.2 Submit Answer & Receive Evaluated Feedback
Evaluates the submitted answer server-side, updates learner mastery, and returns pedagogical branching.

- **URL**: `POST /api/v1/questions/submit`
- **Request Body**:
  ```json
  {
    "user_id": "officer-iss-8842",
    "question_id": "price.cpi.weighted.mcq.001-839210",
    "submitted_answer": "A",
    "time_taken_seconds": 42
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "question_id": "price.cpi.weighted.mcq.001-839210",
    "correct": true,
    "score": 1.0,
    "feedback": {
      "explanation": "CPI = Σ(W × R) / ΣW = [(45×120) + (30×110) + (25×135)] / (45 + 30 + 25) = 120.75.",
      "misconception_id": null,
      "correct_answer": 120.75
    },
    "mastery": {
      "skill_id": "price.cpi.weighted_price_relatives",
      "score": 80.0,
      "level": "advanced"
    },
    "next": {
      "type": "question",
      "question_id": "price.inf.num.001-94821",
      "target_skill_id": "price.inflation_rate",
      "message": "Mastery achieved in price.cpi.weighted_price_relatives! Advancing to price.inflation_rate."
    }
  }
  ```

---

### 3.3 Execute Standalone Statistical Calculation
Execute pure mathematical operations directly.

- **URL**: `POST /api/v1/stats/calculate`
- **Request Body**:
  ```json
  {
    "operation": "fisher_index",
    "inputs": {
      "laspeyres": 124.0,
      "paasche": 121.0
    }
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "operation": "fisher_index",
    "result": 122.4908,
    "unit": "index_points",
    "formula": "I_F = sqrt(I_L * I_P)",
    "steps": [
      "Product I_L * I_P = 124.0 * 121.0 = 15004.0000",
      "Square root = sqrt(15004.0000) = 122.4908"
    ],
    "metadata": {
      "laspeyres": 124.0,
      "paasche": 121.0
    }
  }
  ```

---

### 3.4 Retrieve Competencies
- **URL**: `GET /api/v1/competencies`
- **URL**: `GET /api/v1/competencies/{competency_id}`

---

## 4. Curl Examples

```bash
# Health Check
curl -X GET http://localhost:8000/api/v1/stats-engine/health

# Compute Price Relative
curl -X POST http://localhost:8000/api/v1/stats/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "price_relative", "inputs": {"current_price": 75, "base_price": 50}}'

# Request Next Question
curl -X POST http://localhost:8000/api/v1/questions/next \
  -H "Content-Type: application/json" \
  -d '{"user_id": "officer-01", "competency_id": "price_statistics"}'
```
