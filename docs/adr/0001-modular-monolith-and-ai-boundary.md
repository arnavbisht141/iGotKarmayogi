# ADR 0001: Keep LMS as a modular monolith; run AI orchestration separately

**Status:** Accepted

## Context

The LMS needs transactional domain rules and a coherent source of truth. AI providers have independent credentials, latency, reliability, cost, and change cadence.

## Decision

Keep auth, learning, assessment, catalogue, profile, dashboard, and administration modules in the LMS backend. Preserve the existing in-process assistant during this structural reorganization. When AI development begins, extract model orchestration into a separate service reached only through a backend adapter.

## Consequences

The LMS remains a modular monolith without prematurely inventing AI-service behavior. A future extraction will require a second deployment and an explicit API contract. The separate service will not be a microservice decomposition of LMS domain data.
