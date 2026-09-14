import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.models import GapAnalysis, Course, Recommendation
from app.agents.igot.client import MockIgotClient
from app.agents.recommendation.embeddings import get_embedding_client

logger = logging.getLogger(__name__)

MAX_RECOMMENDATIONS = 5


def _structured_candidates(db: Session, domain_code: str) -> List[Course]:
    return db.query(Course).filter(Course.category == domain_code).all()


def _vector_rerank(pinecone_index, gap_description: str, candidate_ids: List[int]) -> List[int]:
    """Returns candidate_ids re-ordered by semantic similarity to gap_description.
    Falls back to the original order (unchanged) if Pinecone errors."""
    if not candidate_ids:
        return []
    try:
        embedding_client = get_embedding_client()
        query_vector = embedding_client.embed_query(gap_description)
        result = pinecone_index.query(vector=query_vector, top_k=10, include_metadata=True)
        matched_ids_in_order = [
            m["metadata"]["course_id"] for m in result.get("matches", [])
            if m.get("metadata", {}).get("course_id") in candidate_ids
        ]
        remaining = [cid for cid in candidate_ids if cid not in matched_ids_in_order]
        return matched_ids_in_order + remaining
    except Exception as e:
        logger.warning("Pinecone vector rerank failed, falling back to structured order: %s", e)
        return candidate_ids


def _write_rationale(llm_client, gap_description: str, courses: List[Course]) -> dict:
    """Returns {course_id: rationale_text}. Falls back to a templated rationale
    per course if the LLM call fails."""
    try:
        course_list_text = "\n".join(f"- {c.title} ({c.category}, {c.difficulty}): {c.overview}" for c in courses)
        prompt = (
            f"An official has this skill gap: {gap_description}\n\n"
            f"Candidate courses:\n{course_list_text}\n\n"
            "For each course, write one short paragraph explaining why it helps close this gap. "
            "Format as 'Course Title: rationale text', one per line."
        )
        response = llm_client.invoke(prompt)
        text = response.content
        rationales = {}
        for line in text.split("\n"):
            if ":" not in line:
                continue
            title_part, rationale_part = line.split(":", 1)
            match = next((c for c in courses if c.title.strip() == title_part.strip()), None)
            if match:
                rationales[match.id] = rationale_part.strip()
        for c in courses:
            rationales.setdefault(c.id, f"Recommended to help close your {gap_description} gap.")
        return rationales
    except Exception as e:
        logger.warning("LLM rationale generation failed, using templated fallback: %s", e)
        return {c.id: f"Recommended to help close your {gap_description} gap." for c in courses}


def generate_recommendations(
    db: Session, user_id: int, pinecone_index=None, llm_client=None
) -> List[Recommendation]:
    igot_client = MockIgotClient(db)
    gaps = db.query(GapAnalysis).filter(GapAnalysis.user_id == user_id, GapAnalysis.gap > 0).order_by(GapAnalysis.generated_at.desc()).all()

    seen_domains = set()
    recommendations: List[Recommendation] = []

    for gap in gaps:
        if gap.domain.code in seen_domains:
            continue  # only the most recent gap row per domain
        seen_domains.add(gap.domain.code)

        candidates = _structured_candidates(db, gap.domain.code)
        candidates = [c for c in candidates if igot_client.get_enrollment_status(user_id, c.id) != "completed"]
        if not candidates:
            continue

        gap_description = f"progress from level {gap.current_level:.1f} to {gap.target_level:.1f} in {gap.domain.name}"

        candidate_ids = [c.id for c in candidates]
        if pinecone_index is not None:
            candidate_ids = _vector_rerank(pinecone_index, gap_description, candidate_ids)

        ranked_courses = [c for cid in candidate_ids for c in candidates if c.id == cid][:MAX_RECOMMENDATIONS]
        if not ranked_courses:
            continue

        rationales = _write_rationale(llm_client, gap_description, ranked_courses) if llm_client is not None else {
            c.id: f"Recommended to help close your {gap_description} gap." for c in ranked_courses
        }

        for rank, course in enumerate(ranked_courses):
            rec = Recommendation(
                user_id=user_id, course_id=course.id,
                reason=rationales.get(course.id, ""),
                score=round(1.0 - (rank * 0.1), 2),
            )
            db.add(rec)
            recommendations.append(rec)

    db.commit()
    for rec in recommendations:
        db.refresh(rec)
    return recommendations
