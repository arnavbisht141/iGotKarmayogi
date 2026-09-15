import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import GapAnalysis, Course, Recommendation
from app.agents.igot.client import MockIgotClient, domain_category_filter
from app.agents.recommendation.embeddings import get_embedding_client

logger = logging.getLogger(__name__)

MAX_RECOMMENDATIONS = 5


def _structured_candidates(db: Session, domain_code: str) -> List[Course]:
    return db.query(Course).filter(domain_category_filter(domain_code)).all()


def _vector_rerank(pinecone_index, gap_description: str, candidate_ids: List[int]) -> List[int]:
    """Returns candidate_ids re-ordered by semantic similarity to gap_description.
    Falls back to the original order (unchanged) if Pinecone errors."""
    if not candidate_ids:
        return []
    try:
        embedding_client = get_embedding_client()
        query_vector = embedding_client.embed_query(gap_description)
        result = pinecone_index.query(vector=query_vector, top_k=10, include_metadata=True)
        # pinecone SDK returns a QueryResponse object; test fakes return a plain dict
        matches = result.get("matches", []) if isinstance(result, dict) else (result.matches or [])
        matched_ids_in_order = []
        for m in matches:
            metadata = m.get("metadata", {}) if isinstance(m, dict) else (m.metadata or {})
            course_id = metadata.get("course_id")
            if course_id is not None and int(course_id) in candidate_ids:
                matched_ids_in_order.append(int(course_id))
        remaining = [cid for cid in candidate_ids if cid not in matched_ids_in_order]
        return matched_ids_in_order + remaining
    except Exception as e:
        logger.warning("Pinecone vector rerank failed, falling back to structured order: %s", e)
        return candidate_ids


def template_rationale(course: Course, gap_description: str) -> str:
    """Offline rationale used when no LLM is configured or the LLM call fails."""
    skills = [cs.skill.name for cs in (course.course_skills or []) if cs.skill]
    focus = f" in {' and '.join(skills[:2])}" if skills else ""
    level = course.difficulty or "self-paced"
    return f"This {level} course ({course.duration_hours or 0:g} hours) builds skills{focus} to help you {gap_description}."


def _write_rationale(llm_client, gap_description: str, courses: List[Course]) -> dict:
    """Returns {course_id: rationale_text}. Falls back to a templated rationale
    per course if the LLM call fails."""
    try:
        from app.agents.llm_utils import parse_llm_json

        course_list_text = "\n".join(f"- id {c.id}: {c.title} ({c.category}, {c.difficulty}): {c.overview}" for c in courses)
        prompt = (
            f"An official in India's Official Statistical System has this skill gap: {gap_description}\n\n"
            f"Candidate courses:\n{course_list_text}\n\n"
            "For each course write 2 sentences explaining how it closes this specific gap. "
            'Respond ONLY with a JSON object mapping each course id (as a string) to its rationale, e.g. {"12": "..."}.'
        )
        response = llm_client.invoke(prompt)
        payload = parse_llm_json(response.content)
        valid_ids = {c.id for c in courses}
        rationales = {}
        for key, value in (payload.items() if isinstance(payload, dict) else []):
            try:
                course_id = int(str(key).strip())
            except ValueError:
                continue
            if course_id in valid_ids and isinstance(value, str) and value.strip():
                rationales[course_id] = value.strip()
        for c in courses:
            rationales.setdefault(c.id, template_rationale(c, gap_description))
        return rationales
    except Exception as e:
        logger.warning("LLM rationale generation failed, using templated fallback: %s", e)
        return {c.id: template_rationale(c, gap_description) for c in courses}


def get_llm_client():
    """Constructs the real LLM client using the same Groq -> OpenAI -> Gemini fallback
    chain as app/agents/router.py's process_query_node, but returns the client object
    instead of invoking it. Returns None if no key works."""
    if settings.GROQ_API_KEY:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(model_name=settings.GROQ_MODEL, api_key=settings.GROQ_API_KEY, temperature=0.3)
        except Exception as e:
            logger.warning("Groq client construction failed, falling back: %s", e)

    if settings.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=settings.OPENAI_MODEL, api_key=settings.OPENAI_API_KEY, temperature=0.3)
        except Exception as e:
            logger.warning("OpenAI client construction failed, falling back: %s", e)

    if settings.GOOGLE_API_KEY:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, google_api_key=settings.GOOGLE_API_KEY, temperature=0.3)
        except Exception as e:
            logger.warning("Gemini client construction failed: %s", e)

    return None


def generate_recommendations(
    db: Session, user_id: int, pinecone_index=None, llm_client=None
) -> List[Recommendation]:
    igot_client = MockIgotClient(db)

    # dedup gap_analyses (a history table) to the latest row per domain BEFORE filtering
    # on gap > 0, otherwise a closed gap (latest row, gap==0) can be shadowed by an older
    # still-open row for the same domain that the SQL filter would have kept instead.
    all_gap_rows = db.query(GapAnalysis).filter(GapAnalysis.user_id == user_id).order_by(GapAnalysis.generated_at.desc()).all()
    latest_by_domain = {}
    for row in all_gap_rows:
        if row.domain_id not in latest_by_domain:
            latest_by_domain[row.domain_id] = row
    gaps = [row for row in latest_by_domain.values() if row.gap > 0]

    # supersede prior pending recommendations so re-running /generate doesn't accumulate
    # duplicate rows; rows the user has already acted on (enrolled/dismissed) are untouched.
    db.query(Recommendation).filter_by(user_id=user_id, status="pending").delete()

    seen_domains = set()
    recommendations: List[Recommendation] = []

    for gap in gaps:
        if gap.domain.code in seen_domains:
            continue  # defensive: latest_by_domain already dedups by domain_id
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
            c.id: template_rationale(c, gap_description) for c in ranked_courses
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
