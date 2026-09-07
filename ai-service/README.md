# AI service boundary

This directory reserves the future independently deployable AI application. No AI
service has been implemented as part of the repository reorganization.

The existing assistant remains in `backend/app/agents` so the current behavior and
API contract stay unchanged. When AI development begins, its existing behavior can
be migrated here together with an explicit backend-to-AI contract.

The intended boundary is documented in [`../docs/architecture.md`](../docs/architecture.md) and the architecture
decision records. Future implementation may include agent workflows, model-provider
adapters, retrieval, evaluation, safety policies, background jobs, and observability.
Those directories are intentionally not scaffolded until corresponding code exists.
