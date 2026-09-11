# Statistical Competency Engine — Antigravity Implementation Plan

## 1. Purpose

Build a production-ready Statistical Competency Engine that can be integrated into the existing LMS portal as an independent backend service. The engine must power statistical competency learning and assessment across the ten planned competency domains: Survey Design, Sampling, National Accounts, Price Statistics, Labour Statistics, Agricultural Statistics, Industrial Statistics, SDG Indicators, Metadata Standards, and Data Quality Frameworks.

The implementation must prioritize correctness, deterministic computation, explainability, modularity, testability, and clean API integration. The portal should not need to know how statistical calculations, question generation, branching, personalization, or chart specifications are implemented internally. The portal should consume stable JSON APIs and render the returned content.

The first implementation milestone must be a complete vertical slice for one competency domain, preferably Price Statistics, demonstrating deterministic calculations, generated datasets, chart specifications, parameterized questions, answer validation, branching, remediation, learner-state updates, and API integration. Once this vertical slice is stable, the same architecture should be extended to the remaining domains.

## 2. Core Architectural Principle

The system must separate statistical truth from language generation. All numerical calculations, derived values, answer keys, scoring, parameter constraints, chart datasets, and validation must be deterministic. An LLM may optionally assist with question wording, contextual scenarios, hints, or explanations, but it must never be the authoritative source for numerical answers.

The engine should therefore follow the pipeline: competency definition → skill/concept selection → question template → deterministic parameter generation → deterministic answer generation → validation → optional explanation generation → chart specification generation when required → branching decision → JSON API response.

The system must not depend on an LLM being available for its core functionality. Every core assessment flow must work using deterministic templates and statistical functions alone.

## 3. Recommended Technology Stack

Use Python as the implementation language because the project is computation-heavy and benefits from the scientific Python ecosystem. Use FastAPI for the HTTP API, Pydantic for request and response schemas, NumPy and pandas where appropriate for numerical and tabular operations, SciPy only where statistically justified, and pytest for automated testing.

Use a relational database such as PostgreSQL for persistent competency, question, attempt, and learner-state data if the portal does not already own these records. Keep persistence behind repository/service interfaces so the engine can initially run with SQLite or an in-memory implementation during development.

Use Docker for reproducible deployment. Generate an OpenAPI specification automatically through FastAPI and provide a human-readable integration guide for the portal developer.

Do not introduce unnecessary ML infrastructure during the first implementation. The adaptive layer should initially use transparent rules. A future knowledge-tracing model can replace or augment the rule engine after sufficient learner interaction data exists.

## 4. Repository Structure

Create a clean repository with the following logical structure.

```text
statistical-competency-engine/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── stats.py
│   │   ├── questions.py
│   │   ├── charts.py
│   │   ├── competencies.py
│   │   └── users.py
│   ├── core/
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── models/
│   │   ├── competency.py
│   │   ├── question.py
│   │   ├── attempt.py
│   │   └── learner_state.py
│   ├── schemas/
│   │   ├── stats.py
│   │   ├── questions.py
│   │   ├── charts.py
│   │   ├── competencies.py
│   │   └── attempts.py
│   ├── stats/
│   │   ├── base.py
│   │   ├── descriptive.py
│   │   ├── survey_design.py
│   │   ├── sampling.py
│   │   ├── national_accounts.py
│   │   ├── price_statistics.py
│   │   ├── labour_statistics.py
│   │   ├── agricultural_statistics.py
│   │   ├── industrial_statistics.py
│   │   ├── sdg_indicators.py
│   │   ├── metadata.py
│   │   └── data_quality.py
│   ├── questions/
│   │   ├── generator.py
│   │   ├── templates.py
│   │   ├── parameters.py
│   │   ├── distractors.py
│   │   ├── validator.py
│   │   ├── branching.py
│   │   └── personalization.py
│   ├── charts/
│   │   ├── generator.py
│   │   ├── transformations.py
│   │   └── schemas.py
│   ├── competency/
│   │   ├── graph.py
│   │   ├── mastery.py
│   │   └── progression.py
│   ├── repositories/
│   │   ├── competency_repository.py
│   │   ├── question_repository.py
│   │   ├── attempt_repository.py
│   │   └── learner_repository.py
│   └── services/
│       ├── assessment_service.py
│       ├── statistics_service.py
│       ├── chart_service.py
│       └── learner_service.py
├── content/
│   ├── competencies/
│   ├── questions/
│   ├── scenarios/
│   └── explanations/
├── tests/
│   ├── stats/
│   ├── questions/
│   ├── charts/
│   ├── branching/
│   ├── personalization/
│   └── api/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── STATISTICAL_METHODS.md
│   ├── QUESTION_AUTHORING.md
│   ├── API_REFERENCE.md
│   └── PORTAL_INTEGRATION.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

The exact filenames may be adjusted if the existing project has an established convention, but the separation of responsibilities must remain.

## 5. Competency Model

Represent each competency as a hierarchy rather than as a flat list. A competency should contain a domain, subdomains, skills, concepts, prerequisites, difficulty levels, question types, and mastery criteria.

The initial domains are Survey Design, Sampling, National Accounts, Price Statistics, Labour Statistics, Agricultural Statistics, Industrial Statistics, SDG Indicators, Metadata Standards, and Data Quality Frameworks.

Each domain should be decomposed into atomic skills. For example, Price Statistics can contain price relatives, CPI, Laspeyres index, Paasche index, Fisher index, weights, inflation rate, base periods, interpretation of indices, and real versus nominal concepts.

Each skill should have a unique stable ID. IDs must not depend on display text because the portal may change labels later.

Use a structure similar to:

```json
{
  "id": "price.cpi.weighted_price_relatives",
  "domain": "price_statistics",
  "name": "Calculate CPI using weighted price relatives",
  "difficulty": ["basic", "intermediate", "advanced"],
  "prerequisites": [
    "price.price_relative",
    "price.weights"
  ],
  "question_types": [
    "numeric",
    "mcq",
    "chart_interpretation"
  ]
}
```

Create the initial competency graph explicitly in configuration/content files so dependencies are inspectable and editable without modifying application code.

## 6. Deterministic Statistics Engine

Build every statistical method as a pure, independently testable function wherever possible. Functions should accept validated structured inputs and return structured results containing the result, unit, formula, intermediate steps when useful, and metadata.

A calculation response should follow a consistent structure.

```json
{
  "operation": "weighted_mean",
  "result": 23.0,
  "unit": "value",
  "formula": "Σ(wx) / Σw",
  "steps": [
    "Calculate weighted values",
    "Sum weighted values",
    "Divide by total weight"
  ],
  "metadata": {}
}
```

Implement strict validation for missing values, incompatible lengths, zero denominators, negative values where prohibited, invalid weights, invalid periods, and other domain-specific constraints. Do not silently produce NaN or infinite answers for invalid educational inputs.

Use explicit rounding policies. Keep the internally calculated value at sufficient precision and only round at the presentation boundary. The answer validator must use a configurable tolerance for numeric answers.

## 7. Initial Price Statistics Implementation

The first vertical slice must fully implement Price Statistics.

Implement price relative as current price divided by base price multiplied by 100. Implement inflation as percentage change in the relevant index or price measure. Implement weighted price relatives using validated weights. Implement Laspeyres, Paasche, and Fisher price indices with clearly defined inputs and formulas.

Support base-period and current-period metadata. Make formulas available in machine-readable and human-readable form.

For every calculation provide test cases containing normal inputs, edge cases, invalid inputs, and manually verified expected outputs.

Create at least ten deterministic calculation tests for Price Statistics before moving to adaptive assessment.

## 8. Expand the Statistics Modules

After the first vertical slice is stable, implement the other competency domains incrementally.

Survey Design should cover concepts such as survey objectives, questionnaire design, variables, sampling frames, response concepts, sources of bias, and survey quality concepts. Where numerical computation is appropriate, keep it deterministic; conceptual competencies can use rule-based answer validation.

Sampling should cover simple random sampling, systematic sampling, stratified sampling, sample fraction, sample mean, sampling error, confidence intervals where within scope, and related concepts.

National Accounts should cover GDP/GVA concepts, expenditure/income/production approaches where appropriate, nominal versus real values, growth rates, deflators, and per-capita measures.

Labour Statistics should cover labour force, employment, unemployment, LFPR, WPR, unemployment rate, and interpretation of labour indicators.

Agricultural Statistics should cover production, yield, area, productivity, growth rates, and relevant agricultural indicators that are appropriate to the project's competency curriculum.

Industrial Statistics should cover production indices, industrial output, growth rates, sector comparisons, and interpretation.

SDG Indicators should cover indicator definitions, numerator/denominator interpretation, rates, ratios, percentages, time trends, disaggregation, and target interpretation.

Metadata Standards should primarily use structured conceptual question templates, terminology matching, scenario classification, and metadata-field interpretation rather than forcing numerical calculations.

Data Quality Frameworks should cover dimensions such as relevance, accuracy, timeliness, accessibility, coherence, comparability, and related quality-assessment scenarios.

Do not invent official definitions for domain-specific statistical standards. Where official definitions are required, content should be authored from authoritative source material and stored with source metadata.

## 9. Question Engine

Create a generic question model that supports multiple question types. At minimum support multiple choice, numeric answer, true/false, single-select classification, multi-select where needed, chart interpretation, scenario-based questions, and short structured responses if the portal supports them.

Every question must have a stable ID, competency/skill ID, difficulty, question type, prompt, data, options when applicable, answer specification, explanation, metadata, branching information, and version.

Example:

```json
{
  "id": "price.cpi.q001",
  "skill_id": "price.cpi.weighted_price_relatives",
  "type": "numeric",
  "difficulty": "intermediate",
  "prompt": "Calculate the CPI using the weighted price relatives.",
  "data": {},
  "answer": {},
  "explanation": {},
  "branching": {},
  "version": 1
}
```

Separate question content from the generation engine. Store reusable templates in structured content files rather than embedding all question text inside Python functions.

## 10. Parameterized Question Generation

The preferred first-generation personalization mechanism is parameterized questions.

A template should define valid parameter ranges, relationships between parameters, calculation operation, answer generation method, and difficulty constraints.

For example:

```json
{
  "template_id": "sampling.fraction.numeric.001",
  "skill_id": "sampling.sample_fraction",
  "parameters": {
    "population": {
      "type": "integer",
      "min": 5000,
      "max": 50000
    },
    "sample": {
      "type": "derived",
      "constraint": "sample < population"
    }
  },
  "answer_expression": "sample / population * 100"
}
```

The parameter generator must reject combinations that create ambiguous, trivial, duplicate, or invalid questions.

Use deterministic seeds when a reproducible question instance is needed. Store the generated parameter set with the attempt so the exact question can be reconstructed later.

## 11. Distractor Generation

For MCQs, do not generate random incorrect options. Generate distractors based on known misconception patterns.

For example, for a weighted index question, distractors can represent using an unweighted average, reversing the ratio, forgetting to multiply by 100, or using incorrect weights.

Each distractor should have an optional misconception ID. This allows the learner model to identify likely conceptual errors.

The correct answer must always be produced independently from distractor generation and validated before the question is released.

## 12. Question Validation

Build a validator that runs before any generated question is returned by the API.

The validator must check that exactly one answer is correct where the question type requires one answer, all numerical values are finite, all options are distinct, no option accidentally equals the correct answer after rounding unless intended, formulas evaluate successfully, generated data satisfies constraints, chart data is valid, and the explanation is consistent with the computed answer.

For numerical questions, evaluate the answer from the stored parameter set rather than trusting a text field.

For MCQs, independently calculate the correct answer and compare it against the declared answer.

Invalid questions must be rejected and regenerated or returned as an internal generation error. Never expose an invalid question to the learner.

## 13. Chart and Graph Generator

The chart engine must generate structured chart specifications rather than screenshots or frontend-specific chart code.

The chart specification should contain chart type, title, description, axis definitions, series mappings, dataset, units, and optional interpretation metadata.

Support at minimum bar, line, pie, histogram, scatter, and box-plot representations where statistically meaningful.

The chart engine should accept deterministic datasets produced by the statistics engine or question generator.

Example:

```json
{
  "type": "bar",
  "title": "Unemployment Rate by Year",
  "xAxis": {
    "field": "year",
    "label": "Year"
  },
  "yAxis": {
    "field": "rate",
    "label": "Unemployment Rate (%)"
  },
  "data": [
    {"year": 2021, "rate": 6.2},
    {"year": 2022, "rate": 5.8},
    {"year": 2023, "rate": 5.4}
  ]
}
```

The portal developer should be free to render the specification using the frontend chart library already used by the portal.

## 14. Chart-Based Questions

Build a pipeline in which deterministic data can be converted into a chart and then used to create questions.

Support questions such as identifying maxima/minima, calculating changes, identifying trends, comparing categories, interpreting distributions, identifying anomalies, and selecting correct statements.

The correct answer must be computed directly from the underlying dataset. Do not derive the answer by visually interpreting the generated chart.

Store both the dataset and chart specification with the question instance so that the question remains reproducible.

## 15. Branching Question Engine

Implement branching as a declarative rule system.

A question can define outcomes such as correct, incorrect, partially correct where supported, time-out, or misconception-specific errors. Each outcome maps to the next question, remediation content, difficulty adjustment, or competency transition.

Example:

```json
{
  "branches": [
    {
      "condition": {
        "type": "correct"
      },
      "action": {
        "type": "next_skill",
        "target": "price.inflation"
      }
    },
    {
      "condition": {
        "type": "incorrect"
      },
      "action": {
        "type": "remediation",
        "target": "price.cpi.basic"
      }
    }
  ]
}
```

Support additional conditions such as consecutive errors, score threshold, difficulty threshold, misconception ID, and mastery state.

Keep the rule evaluator deterministic and unit-testable.

## 16. Personalization Engine

Personalization must initially be transparent and rule-based.

Inputs may include competency mastery estimate, recent correctness, number of attempts, previous error type, current difficulty, prerequisite mastery, time taken, and learning history.

The engine should use these signals to select an appropriate next question.

A basic policy can increase difficulty after sustained success, decrease difficulty after repeated failure, route misconception errors to remediation, and move to a prerequisite skill when prerequisite weakness is detected.

Do not use sensitive personal information for question personalization.

The question generator should be able to produce different numerical instances of the same skill so that repeated practice does not simply repeat the exact same question.

## 17. Learner Mastery Model

Create a simple interpretable mastery model for the first version.

Represent mastery per skill on a normalized scale, for example 0–100, together with confidence and attempt history.

Use configurable rules rather than hardcoding a universal threshold.

For example, repeated correct answers can increase mastery, incorrect answers can decrease confidence and trigger remediation, and consistent performance at a difficulty level can qualify the learner for the next level.

Keep the mastery calculation behind an interface so it can later be replaced by Bayesian Knowledge Tracing, Item Response Theory, or another validated method without rewriting the question API.

## 18. Assessment Session Flow

Implement the complete lifecycle:

```text
Start assessment
    ↓
Identify competency / skill
    ↓
Determine learner state
    ↓
Select question template
    ↓
Generate parameters
    ↓
Calculate answer
    ↓
Generate distractors
    ↓
Generate chart if required
    ↓
Validate question
    ↓
Return question
    ↓
Learner submits answer
    ↓
Evaluate answer deterministically
    ↓
Record attempt
    ↓
Update mastery
    ↓
Evaluate branching rules
    ↓
Return next question or completion state
```

The portal should only need to call the appropriate APIs at each step.

## 19. API Design

Implement versioned APIs under `/api/v1`.

The minimum endpoints are:

```text
POST /api/v1/stats/calculate
POST /api/v1/questions/generate
POST /api/v1/questions/next
POST /api/v1/questions/submit
POST /api/v1/charts/generate
GET  /api/v1/competencies
GET  /api/v1/competencies/{competency_id}
GET  /api/v1/users/{user_id}/competencies
GET  /api/v1/health
```

`/stats/calculate` should accept an operation and validated inputs and return the deterministic calculation result.

`/questions/generate` should create a standalone question instance based on a skill, difficulty, question type, and optional learner context.

`/questions/next` should select the next adaptive question based on learner state and assessment context.

`/questions/submit` should evaluate an answer, record the attempt, update mastery, apply branching, and return the next action.

`/charts/generate` should accept structured data and return a frontend-independent chart specification.

`/competencies` endpoints should expose the competency hierarchy and metadata needed by the portal.

## 20. Standard Question Response

Use a stable response contract similar to:

```json
{
  "question_id": "price.cpi.q001-instance-123",
  "skill_id": "price.cpi.weighted_price_relatives",
  "competency_id": "price_statistics",
  "type": "mcq",
  "difficulty": "intermediate",
  "prompt": "Calculate the CPI using the weighted price relatives.",
  "data": {},
  "options": [],
  "chart": null,
  "metadata": {
    "estimated_time_seconds": 60
  }
}
```

Do not send the correct answer to the learner-facing question endpoint unless the portal has a secure architecture where this is explicitly required. The server should retain the answer key and validate the submitted answer.

## 21. Answer Submission Response

Return a response similar to:

```json
{
  "question_id": "price.cpi.q001-instance-123",
  "correct": true,
  "score": 1.0,
  "feedback": {
    "explanation": "...",
    "misconception_id": null
  },
  "mastery": {
    "skill_id": "price.cpi.weighted_price_relatives",
    "score": 74.0,
    "level": "intermediate"
  },
  "next": {
    "type": "question",
    "question_id": "price.inflation.q003"
  }
}
```

Never trust a client-provided score. Recalculate correctness and score server-side.

## 22. Integration Contract for the Portal Developer

Create `docs/PORTAL_INTEGRATION.md`.

Explain the authentication mechanism, base URL configuration, request/response formats, error handling, question rendering requirements, chart rendering requirements, answer submission flow, competency-progress display, and expected lifecycle.

The portal developer should not need to import Python code or understand the internal repository. Integration should be HTTP/JSON based.

Provide curl examples and sample JSON requests/responses for every endpoint.

Include a sequence diagram showing:

```text
Portal → Engine: request next question
Engine → Portal: question JSON
Portal → User: render
User → Portal: answer
Portal → Engine: submit answer
Engine → Portal: result + mastery + next action
Portal → User: feedback / next question
```

## 23. Error Handling

Define consistent API error responses.

Use appropriate HTTP status codes and machine-readable error identifiers.

Example:

```json
{
  "error": {
    "code": "INVALID_STATISTICAL_INPUT",
    "message": "Weights must contain at least one positive value.",
    "details": {}
  }
}
```

Do not expose stack traces, internal file paths, database details, or implementation secrets.

## 24. Security and Integrity

The answer key must not be exposed through learner-facing endpoints.

Validate all request payloads using Pydantic.

Authenticate portal-to-engine requests using the integration mechanism agreed with the portal architecture. Keep secrets in environment variables and provide `.env.example`.

Add request IDs and structured logs.

Rate-limit expensive generation endpoints if required.

Do not log sensitive learner information unnecessarily.

## 25. Persistence

Persist question instances or enough information to reconstruct them. For generated numerical questions, store the template ID, seed, parameters, version, and answer specification.

Persist attempts with user ID, question ID, skill ID, submitted answer, correctness, score, time taken, misconception ID when available, timestamp, and engine/content version.

Persist learner state per skill so adaptive progression is reproducible.

Avoid tightly coupling the engine to the portal's user database. Use stable external user IDs and repository interfaces.

## 26. Content Authoring System

Create structured content files for competency definitions and question templates.

Do not force content authors to modify Python code for ordinary question additions.

A template should specify its skill, difficulty, question type, parameters, validation constraints, answer logic, explanation template, and branching metadata.

Create an authoring guide describing how a new question template is added and tested.

## 27. LLM Integration Boundary

If an LLM is used, isolate it behind a service interface such as `ExplanationGenerator` or `ScenarioGenerator`.

The deterministic engine must first compute the truth. The LLM receives the already-computed facts and is only allowed to transform them into educational language.

For example, the deterministic layer can provide:

```json
{
  "formula": "Current price / Base price × 100",
  "inputs": {
    "base_price": 100,
    "current_price": 120
  },
  "result": 120
}
```

The LLM may generate an explanation from those facts, but the engine remains responsible for validating that the explanation does not introduce contradictory numerical claims.

LLM-generated content should be optional and must never prevent a question from being served.

## 28. Testing Strategy

Testing is a first-class deliverable.

Create unit tests for every statistical function. Test normal cases, boundary cases, invalid cases, rounding behavior, zero denominators, missing values, and numerical tolerances.

Create question-generation tests ensuring parameter constraints are respected, answers are correct, options are unique, and generated questions are reproducible with a seed.

Create branching tests for every rule path.

Create personalization tests for beginner, intermediate, advanced, strong-performance, weak-performance, and misconception cases.

Create chart tests ensuring specifications are structurally valid and datasets match their declared fields.

Create API integration tests for all endpoints.

Add a regression test suite so adding new competency content cannot silently break existing calculations.

## 29. Statistical Verification

Do not rely only on implementation tests. For important formulas, create manually verified reference examples.

Where appropriate, cross-check selected computations against established scientific libraries or independently calculated reference values.

Every implemented statistical method must document its formula, assumptions, units, expected input structure, output structure, and edge cases.

For official statistical concepts, maintain source attribution in the content metadata. The source metadata should identify the authoritative reference used during content authoring.

## 30. Performance Requirements

The deterministic calculation and question-generation paths should be lightweight and synchronous for ordinary requests.

Avoid loading large datasets or machine-learning models on every request.

Cache static competency definitions and reusable templates.

If expensive generation is introduced later, separate it from the synchronous question-serving path.

The `/questions/next` endpoint should be optimized because it will be called frequently during learning sessions.

## 31. Docker and Deployment

Create a production-ready Dockerfile and a development `docker-compose.yml`.

The container must start the FastAPI service using a production-capable ASGI server.

Expose the health endpoint.

Use environment variables for database URLs, authentication configuration, optional LLM configuration, logging level, and CORS settings.

Document local setup, testing, Docker startup, database initialization, and production deployment assumptions.

## 32. API Documentation

FastAPI's generated Swagger/OpenAPI interface must be complete enough for the portal developer to test requests without reading source code.

Every endpoint must have descriptions, request schemas, response schemas, error responses, and representative examples.

The repository should include a generated or exportable OpenAPI JSON/YAML file if the integration process requires it.

## 33. Frontend Independence

Do not build the statistical engine around React components, browser-specific logic, or a specific chart library.

The engine returns JSON.

The portal owns rendering.

For charts, return chart specifications.

For questions, return question objects.

For progress, return competency/mastery objects.

For explanations, return text and optional structured formula/step data.

## 34. First Vertical Slice Definition of Done

The first milestone is complete only when the following scenario works end-to-end.

A learner requests the next Price Statistics question. The engine identifies the learner's current state, selects an appropriate CPI-related template, generates valid parameters, deterministically calculates the answer, creates distractors, creates a chart if the question requires one, validates the complete question, and returns it through `/questions/next`.

The learner submits an answer through `/questions/submit`. The engine independently evaluates the answer, records the attempt, updates the learner's Price Statistics skill mastery, identifies a misconception if applicable, applies branching rules, and returns the next action.

The exact same question instance must be reproducible from its stored template version and generation parameters.

The complete flow must be covered by automated API tests.

## 35. Initial Deliverables

Antigravity must produce the following deliverables.

The first deliverable is the complete source repository implementing the architecture.

The second deliverable is the deterministic Price Statistics module with tested calculations.

The third deliverable is the question-template and parameter-generation framework.

The fourth deliverable is the chart-specification generator.

The fifth deliverable is the branching and rule-based personalization engine.

The sixth deliverable is the learner mastery/progression layer.

The seventh deliverable is the FastAPI service with versioned endpoints.

The eighth deliverable is the OpenAPI documentation.

The ninth deliverable is `docs/PORTAL_INTEGRATION.md` written specifically for the portal developer.

The tenth deliverable is a comprehensive automated test suite.

The eleventh deliverable is Docker configuration and local setup documentation.

## 36. Extension Plan

Once the Price Statistics vertical slice is accepted, extend the same interfaces rather than creating domain-specific APIs for every competency.

Add Sampling next because it provides strong numerical question-generation opportunities. Then add Labour Statistics and National Accounts, followed by Agricultural Statistics, Industrial Statistics, SDG Indicators, Survey Design, Metadata Standards, and Data Quality Frameworks.

Each new competency must add statistical functions or content templates behind the existing interfaces. The portal API should remain stable.

## 37. Future Adaptive Intelligence

Do not implement a complicated ML-based learner model in the first milestone.

The architecture should nevertheless preserve the ability to introduce advanced methods later.

Potential future components include Bayesian Knowledge Tracing for skill mastery, Item Response Theory for item difficulty and learner ability estimation, misconception classification, semantic response evaluation for conceptual answers, and data-driven question selection.

These should be introduced only after the system has collected sufficient validated learner interaction data.

## 38. Non-Goals for the First Version

Do not build a complete portal frontend.

Do not duplicate the portal's authentication or user-management system unnecessarily.

Do not make an LLM responsible for numerical correctness.

Do not implement an opaque recommendation model before the rule-based system is working.

Do not generate chart images as the primary integration format.

Do not hardcode all question text inside Python.

Do not create separate APIs for every individual statistical formula.

Do not attempt to implement all ten competencies before validating the architecture with the first vertical slice.

## 39. Development Sequence

Follow this implementation order strictly unless the existing repository requires a small structural adjustment.

First inspect the existing repository and identify the current backend, frontend, database, authentication, deployment, and coding conventions. Do not overwrite an existing architecture without understanding it.

Second create the engine module boundaries, schemas, configuration, logging, exception handling, and test infrastructure.

Third implement the competency model and Price Statistics competency definition.

Fourth implement deterministic Price Statistics calculations and exhaustive tests.

Fifth implement the question schema, template system, parameter generator, answer calculator, and question validator.

Sixth implement MCQ and numeric question types.

Seventh implement chart specifications and chart-based question support.

Eighth implement branching rules.

Ninth implement learner state and rule-based personalization.

Tenth connect everything through `/questions/next` and `/questions/submit`.

Eleventh add API integration tests.

Twelfth containerize the service and produce OpenAPI documentation.

Thirteenth write the portal integration guide with exact example requests and responses.

Fourteenth demonstrate the complete vertical slice.

Only after this acceptance should additional competency domains be implemented.

## 40. Acceptance Checklist

The implementation is acceptable only if all of the following are true.

- [x] The engine can calculate supported statistical operations deterministically.
- [x] Every calculation has automated tests (13 deterministic calculation tests passing).
- [x] Generated questions have reproducible parameter sets (verified with seed fixtures).
- [x] Generated questions are validated before being served (`QuestionValidator`).
- [x] Numerical answers are calculated by the engine rather than by an LLM.
- [x] Distractors can be associated with misconception patterns (`DistractorGenerator`).
- [x] Charts are returned as frontend-independent specifications (`ChartGenerator`).
- [x] Question branching is declarative and testable (`BranchingEngine`).
- [x] Personalization works using learner state and transparent rules (`PersonalizationEngine`).
- [x] Learner attempts and mastery can be persisted or cleanly delegated through repository interfaces (`InMemoryRepositories`).
- [x] The answer key is protected from learner-facing responses (`QuestionInstance` answer withholding).
- [x] The portal can integrate using HTTP/JSON without importing engine internals (`/api/v1/`).
- [x] Swagger/OpenAPI documentation works (`/docs`).
- [x] The Price Statistics end-to-end vertical slice passes automated tests (29/29 pytest passed).
- [x] The repository contains clear architecture, methods, authoring, and portal integration documentation (`docs/statistical_engine/`).
- [x] Adding a new question template does not require rewriting the core engine.
- [x] Adding a new statistical competency does not require changing the portal API.

### Phase 1 Execution Status (Completed):
- **Implementation**: `backend/app/statistical_engine/`
- **Content Definitions**: `backend/content/competencies/price_statistics.json`, `backend/content/questions/price_statistics.json`
- **Automated Tests**: 29 passing unit, generation, branching, mastery, and API tests in `backend/tests/stats_engine/`.
- **Portal Guide**: `docs/statistical_engine/PORTAL_INTEGRATION.md`


## 41. Final Engineering Principle

Build this as a reusable statistical assessment platform, not as a collection of hardcoded questions.

The stable core should be:

```text
Competency Model
      ↓
Skill Selection
      ↓
Question Template
      ↓
Parameter Generator
      ↓
Deterministic Statistics Engine
      ↓
Answer + Distractors
      ↓
Question Validator
      ↓
Chart Generator
      ↓
Branching / Personalization
      ↓
API
      ↓
Portal
```

The most important architectural boundary is that the engine owns statistical correctness and assessment intelligence, while the portal owns user-facing rendering and LMS presentation.

A successful first milestone is not "we implemented CPI." A successful first milestone is "we established a reusable pipeline through which any statistical competency can produce validated, personalized, interactive assessment content and expose it cleanly to the portal."
