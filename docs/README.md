# Project documentation

This directory records the repository structure and the boundaries agreed for
future development. Documentation distinguishes current implementation from
planned work.

## Architecture

- [`architecture.md`](architecture.md) describes the current runtime and the
  planned independent AI-service boundary.
- [`domain-boundaries.md`](domain-boundaries.md) maps the existing LMS backend
  code to modular-monolith domains.
- [`development.md`](development.md) documents current development commands and
  explicitly identifies work that has not been implemented.
- [`adr/0001-modular-monolith-and-ai-boundary.md`](adr/0001-modular-monolith-and-ai-boundary.md)
  records the modular-monolith decision and future AI extraction.
- [`adr/0002-backend-owns-lms-data.md`](adr/0002-backend-owns-lms-data.md)
  records the future data-ownership boundary.

## Existing product and UI records

- [`PROJECT_CONTEXT_AND_PROGRESS.md`](PROJECT_CONTEXT_AND_PROGRESS.md)
- [`HOMEPAGE_UI_REFINEMENTS.md`](HOMEPAGE_UI_REFINEMENTS.md)
- [`UI_UX_CHANGES.md`](UI_UX_CHANGES.md)

Update the closest document whenever a structural boundary changes. Add a new
ADR for an architectural decision instead of silently rewriting an accepted
decision.
