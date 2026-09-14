import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.models import Course
from app.agents.recommendation.indexer import index_course


@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_index_course_upserts_to_pinecone_with_correct_id_and_metadata(db_session, monkeypatch):
    course = Course(title="Intro to Python", overview="Learn Python basics", instructor="x", organization="ISTM", category="technical", difficulty="beginner")
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)

    fake_index = MagicMock()
    fake_embedding_client = MagicMock()
    fake_embedding_client.embed_query.return_value = [0.1] * 768
    monkeypatch.setattr("app.agents.recommendation.indexer.get_embedding_client", lambda: fake_embedding_client)

    index_course(db_session, course.id, pinecone_index=fake_index)

    fake_index.upsert.assert_called_once()
    call_kwargs = fake_index.upsert.call_args
    vectors = call_kwargs.kwargs.get("vectors") or call_kwargs.args[0]
    assert vectors[0][0] == f"course-{course.id}"
    assert vectors[0][1] == [0.1] * 768
    metadata = vectors[0][2]
    assert metadata["course_id"] == course.id
    assert metadata["category"] == "technical"
    assert metadata["title"] == "Intro to Python"


def test_index_course_raises_for_missing_course(db_session):
    with pytest.raises(ValueError):
        index_course(db_session, 99999, pinecone_index=MagicMock())
