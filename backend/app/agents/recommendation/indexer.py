from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Course
from app.agents.recommendation.embeddings import get_embedding_client, build_course_embedding_text, EMBEDDING_DIMENSION

_pinecone_index = None  # lazily constructed real Pinecone index, module-level cache


def get_real_pinecone_index():
    """Lazily constructs (and caches) the real Pinecone index client, creating the index
    itself if it doesn't exist yet. Import of the pinecone package is deferred so this
    module still imports cleanly in environments without the package installed."""
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        if settings.PINECONE_INDEX_NAME not in [idx.name for idx in pc.list_indexes()]:
            pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        _pinecone_index = pc.Index(settings.PINECONE_INDEX_NAME)
    return _pinecone_index


def index_course(db: Session, course_id: int, pinecone_index=None) -> None:
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        raise ValueError(f"Course {course_id} not found")

    index = pinecone_index if pinecone_index is not None else get_real_pinecone_index()
    embedding_client = get_embedding_client()
    text = build_course_embedding_text(course)
    vector = embedding_client.embed_query(text)

    index.upsert(vectors=[(
        f"course-{course.id}",
        vector,
        {"course_id": course.id, "category": course.category or "", "difficulty": course.difficulty or "", "title": course.title},
    )])
