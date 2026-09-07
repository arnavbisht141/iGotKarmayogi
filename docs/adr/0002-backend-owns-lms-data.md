# ADR 0002: The LMS backend owns LMS data

**Status:** Accepted

## Context

Learner records, assessment outcomes, progress, and certificates require authorization, consistency, and auditability.

## Decision

Only the LMS backend reads or writes LMS data. A future AI service will receive minimal request-scoped context from a backend adapter.

## Consequences

AI output is advisory and cannot issue certificates, change progress, or establish policy. Retrieval or analytics requires a separately approved data contract.
