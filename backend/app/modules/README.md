# LMS modules

Each child package owns one existing LMS feature boundary. Routers and their request
schemas were moved here without changing endpoint paths or business behavior.

Modules may import shared infrastructure from `app.core` and ORM entities from
`app.models`. New service or repository files should be introduced only when actual
behavior needs them; empty architectural layers are intentionally avoided.

See [`../../../docs/domain-boundaries.md`](../../../docs/domain-boundaries.md) for
the module map and ownership rules.
