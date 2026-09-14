from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Course
from app.agents.recommendation.embeddings import get_embedding_client, build_course_embedding_text

_pinecone_index = None  # lazily constructed real Pinecone index, module-level cache


def _get_real_pinecone_index():
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        _pinecone_index = pc.Index(settings.PINECONE_INDEX_NAME)
    return _pinecone_index


def index_course(db: Session, course_id: int, pinecone_index=None) -> None:
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise ValueError(f"Course {course_id} not found")

    index = pinecone_index if pinecone_index is not None else _get_real_pinecone_index()
    embedding_client = get_embedding_client()
    text = build_course_embedding_text(course)
    vector = embedding_client.embed_query(text)

    index.upsert(vectors=[(
        f"course-{course.id}",
        vector,
        {"course_id": course.id, "category": course.category or "", "difficulty": course.difficulty or "", "title": course.title},
    )])
