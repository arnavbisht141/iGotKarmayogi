import json
import re
from typing import List, Optional
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage
from app.core.config import settings
from app.models.models import TechnicalLearningObjective
from app.modules.technical_courses.schemas import (
    LearningObjectiveSchema, ObjectiveExtractionRequest, ObjectiveExtractionResponse, DecisionRequest
)
from app.modules.technical_courses.services.decision_service import DecisionService


EXTRACTION_PROMPT_TEMPLATE = """You are an expert technical curriculum developer and instructional designer for official engineering and technical training.

Analyze the following technical course transcript / lecture notes and extract 2 to 5 concrete, actionable learning objectives.

Transcript:
{transcript}

Return ONLY a valid JSON array of objects. Do NOT include markdown code fences or conversational text.
Each JSON object must have the following schema:
[
  {{
    "objective": "Clear, measurable statement starting with an action verb (e.g., 'Implement a FastAPI route to paginate citizen records')",
    "skill": "Primary library, language, or concept (e.g., 'FastAPI', 'Pandas', 'Python', 'SQL')",
    "difficulty": "beginner, intermediate, or advanced",
    "action": "Action verb (e.g., 'implement', 'debug', 'analyze', 'refactor', 'query')"
  }}
]
"""


class ObjectiveExtractor:
    """
    Extracts structured, measurable learning objectives from technical course transcripts.
    Prioritizes configured LLM provider (Google Gemini / OpenAI), with a deterministic
    regex/heuristic engine used strictly as a development and testing fallback.
    """

    @classmethod
    def _extract_via_llm(cls, transcript_text: str) -> Optional[List[LearningObjectiveSchema]]:
        prompt = EXTRACTION_PROMPT_TEMPLATE.format(transcript=transcript_text[:4000])
        response_text = ""

        # Priority 1: Groq (Primary LLM Engine)
        if settings.GROQ_API_KEY:
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    model_name=settings.GROQ_MODEL,
                    api_key=settings.GROQ_API_KEY,
                    temperature=0.2
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[ObjectiveExtractor] Groq invocation fallback: {e}")

        # Priority 2: Fallback to OpenAI
        if not response_text and settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    api_key=settings.OPENAI_API_KEY,
                    temperature=0.2
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[ObjectiveExtractor] OpenAI invocation fallback: {e}")

        # Priority 3: Further Fallback to Google Gemini
        if not response_text and settings.GOOGLE_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.2
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[ObjectiveExtractor] Gemini invocation fallback: {e}")

        if not response_text:
            return None

        # Clean potential markdown fences
        cleaned_json = response_text.strip()
        if cleaned_json.startswith("```"):
            cleaned_json = re.sub(r"^```(?:json)?", "", cleaned_json).strip()
            cleaned_json = re.sub(r"```$", "", cleaned_json).strip()

        try:
            parsed = json.loads(cleaned_json)
            if isinstance(parsed, list):
                objectives: List[LearningObjectiveSchema] = []
                for item in parsed:
                    obj_str = item.get("objective", "").strip()
                    skill = item.get("skill", "Python").strip()
                    diff = item.get("difficulty", "intermediate").lower()
                    action = item.get("action", "implement").lower()
                    if obj_str:
                        # Evaluate assessment mode via DecisionService
                        decision = DecisionService.evaluate(DecisionRequest(
                            objective=obj_str,
                            skill=skill,
                            action=action,
                            difficulty=diff
                        ))
                        objectives.append(LearningObjectiveSchema(
                            objective=obj_str,
                            skill=skill,
                            difficulty=diff,
                            action=action,
                            assessment_mode=decision.assessment_mode,
                            suitability_reason=decision.reasoning
                        ))
                if objectives:
                    return objectives
        except Exception as e:
            print(f"[ObjectiveExtractor] JSON parse failure from LLM response: {e}")

        return None

    @classmethod
    def _extract_via_deterministic_fallback(cls, transcript_text: str) -> List[LearningObjectiveSchema]:
        """
        Deterministic heuristic extractor for development/testing environments without LLM keys.
        """
        text_lower = transcript_text.lower()
        extracted: List[LearningObjectiveSchema] = []

        # Pattern 1: FastAPI / REST API
        if any(w in text_lower for w in ["fastapi", "rest api", "endpoint", "route", "http", "status code", "pydantic"]):
            extracted.append(LearningObjectiveSchema(
                objective="Implement REST API endpoints with request validation and structured error handling using FastAPI",
                skill="FastAPI",
                difficulty="intermediate",
                action="implement",
                assessment_mode="lab",
                suitability_reason="Requires hands-on API endpoint construction and request/response verification."
            ))

        # Pattern 2: Pandas / Data Processing
        if any(w in text_lower for w in ["pandas", "dataframe", "csv", "clean", "null", "group by", "aggregate", "dataset"]):
            extracted.append(LearningObjectiveSchema(
                objective="Clean and transform structured datasets by filtering invalid rows and calculating aggregated statistics using Pandas",
                skill="Pandas",
                difficulty="intermediate",
                action="analyze",
                assessment_mode="lab",
                suitability_reason="Requires hands-on data manipulation and verification of numerical aggregation outputs."
            ))

        # Pattern 3: Debugging / Error Handling
        if any(w in text_lower for w in ["debug", "exception", "bug", "traceback", "fix", "error handling", "try except"]):
            extracted.append(LearningObjectiveSchema(
                objective="Debug and resolve runtime exceptions and edge-case calculation bugs in data pipelines",
                skill="Python Debugging",
                difficulty="intermediate",
                action="debug",
                assessment_mode="lab",
                suitability_reason="Debugging logic requires interactive test case reproduction in sandbox."
            ))

        # Pattern 4: SQL / Database
        if any(w in text_lower for w in ["sql", "query", "select", "join", "database", "table", "schema"]):
            extracted.append(LearningObjectiveSchema(
                objective="Write optimized SQL analytical queries with multi-table joins and aggregation filters",
                skill="SQL",
                difficulty="intermediate",
                action="query",
                assessment_mode="lab",
                suitability_reason="Hands-on SQL query execution produces verifiable query result sets."
            ))

        # Pattern 5: General Python logic / functions
        if not extracted or any(w in text_lower for w in ["function", "python", "algorithm", "loop", "dictionary"]):
            extracted.append(LearningObjectiveSchema(
                objective="Implement robust Python utility functions with strict input validation and boundary condition handling",
                skill="Python",
                difficulty="beginner" if "beginner" in text_lower or "basics" in text_lower else "intermediate",
                action="implement",
                assessment_mode="lab",
                suitability_reason="Practical coding exercise requiring unit test execution."
            ))

        return extracted

    @classmethod
    def extract_objectives(
        cls,
        req: ObjectiveExtractionRequest,
        db: Optional[Session] = None
    ) -> ObjectiveExtractionResponse:
        """
        Orchestrates objective extraction, applying LLM when available and falling back to
        deterministic rules for test/dev environments.
        """
        text = req.transcript_text.strip()
        if not text:
            return ObjectiveExtractionResponse(transcript_id=req.transcript_id, objectives=[])

        # Try LLM first
        objectives = cls._extract_via_llm(text)

        # Use deterministic testing fallback if LLM returned None
        if not objectives:
            objectives = cls._extract_via_deterministic_fallback(text)

        # Optional persistence
        if db is not None and req.transcript_id is not None:
            for obj in objectives:
                db_obj = TechnicalLearningObjective(
                    transcript_id=req.transcript_id,
                    objective=obj.objective,
                    skill=obj.skill,
                    difficulty=obj.difficulty,
                    action_verb=obj.action,
                    assessment_mode=obj.assessment_mode,
                    suitability_reason=obj.suitability_reason
                )
                db.add(db_obj)
            db.commit()

        return ObjectiveExtractionResponse(
            transcript_id=req.transcript_id,
            objectives=objectives
        )
