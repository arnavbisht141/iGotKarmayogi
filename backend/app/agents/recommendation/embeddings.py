from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIMENSION = 768


def get_embedding_client() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=settings.GOOGLE_API_KEY)


def build_course_embedding_text(course) -> str:
    skill_names = [cs.skill.name for cs in course.course_skills] if course.course_skills else []
    parts = [course.title, course.overview, course.organization, course.category] + skill_names
    return " | ".join(p for p in parts if p)
