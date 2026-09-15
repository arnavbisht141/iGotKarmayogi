from typing import List

import httpx

from app.core.config import settings

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768
_EMBED_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBEDDING_MODEL}:embedContent"


class GeminiEmbeddingClient:
    """Calls the Gemini embedContent REST endpoint directly. Plain REST avoids the gRPC
    transport's c-ares DNS resolver, which fails in some networks."""

    def embed_query(self, text: str) -> List[float]:
        response = httpx.post(
            _EMBED_URL,
            params={"key": settings.GOOGLE_API_KEY},
            json={"content": {"parts": [{"text": text}]}, "outputDimensionality": EMBEDDING_DIMENSION},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()["embedding"]["values"]


def get_embedding_client() -> GeminiEmbeddingClient:
    return GeminiEmbeddingClient()


def build_course_embedding_text(course) -> str:
    skill_names = [cs.skill.name for cs in course.course_skills] if course.course_skills else []
    parts = [course.title, course.overview, course.organization, course.category] + skill_names
    return " | ".join(p for p in parts if p)
