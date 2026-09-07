# iGot Karmayogi backend

The backend is a FastAPI modular monolith. app.main composes feature routers under the configured API version. app.core owns configuration, database and session lifecycle, security, and seed data. SQLAlchemy ORM entities remain centralized in app.models because the current schema has deliberate relationships across learning domains.

## Module map

- app.modules.auth: identity and tokens.
- app.modules.onboarding and app.modules.profile: learner identity and preferences.
- app.modules.dashboard, app.modules.discover, and app.modules.courses: read models, catalogue, and enrollment entry points.
- app.modules.learning and app.modules.assessments: progression and certification workflows.
- app.modules.admin: protected operational workflows.
- app.agents: AI integration, intentionally isolated from domain modules.

A module exposes router.py. Request and response contracts live in schemas.py where a feature declares them. Business services and repositories are introduced only for non-trivial reusable workflows; never as empty ceremonial folders. HTTP API compatibility is preserved.

## Design invariants

- All versioned API routes are mounted only in app.main.
- Core infrastructure and ORM models do not import feature routers.
- Feature modules use dependency injection for database access and security.
- Schema and database migrations must preserve existing tables and route contracts.

## Local validation

From backend, run python -m compileall app and start with python run.py. The application currently seeds its development database at startup; use an isolated database for integration testing.