# Development guide

## Prerequisites

Docker Desktop is the fastest path. For local services use Python 3.12+ and the Node version declared by the frontend.

```bash
cp .env.example .env
docker compose -f docker-compose.dev.yml up --build
```

The frontend remains at `http://localhost:3000` and the LMS API at `http://localhost:8000/api`.

## Future AI service

The separately deployed AI service and its backend adapter are architectural plans, not current implementation. `ai-service/README.md` records the intended boundary without scaffolding empty or speculative code. The current `/api/agents/chat` behavior remains in the backend.
