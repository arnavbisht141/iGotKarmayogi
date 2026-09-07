# Catalog feature

Owns course discovery and course-detail screens, including search-parameter handling, catalog API requests, and enrollment actions. It consumes shared UI, auth, i18n, API, and types. Route files preserve `/discover` and `/courses/[courseId]` without owning domain logic.

Future folders: add `filters/` or `api/` only after those concerns have multiple concrete modules.
