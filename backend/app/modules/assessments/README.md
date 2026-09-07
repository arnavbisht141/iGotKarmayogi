# assessments module

## Ownership

This bounded module owns the assessments HTTP surface and its domain orchestration. It does not own database engine or session lifecycle, authentication primitives, or ORM model definitions. Those remain in app.core and app.models.

## Public API

The router is mounted by app.main beneath the version prefix. Current operations: GET /{assessment_id}, POST /{assessment_id}/submit. Route URLs and response shapes are compatibility commitments.

schemas.py owns Pydantic request and response contracts.

## Dependencies and invariants

- Uses shared SQLAlchemy models and gets request-scoped sessions through app.core.database.get_db.
- Uses app.core.security dependencies for identity and authorization where required.
- Preserve existing transaction boundaries, status codes, and response messages before behavior changes.
- Cross-module reads may use shared models. Move shared or multi-step mutations into an explicit service when warranted.

## Extension points

Add service.py for reusable business workflows and repository.py only once persistence queries are shared, complex, or independently testable. Do not add empty layers.