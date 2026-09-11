import json
import re
from typing import Optional
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage
from app.core.config import settings
from app.models.models import TechnicalGeneratedLab, TechnicalLabSolution
from app.modules.technical_courses.schemas import (
    GeneratedLabSchema, SolutionGenerationRequest, SolutionGenerationResponse
)
from app.modules.technical_courses.services.template_service import TemplateService


SOLUTION_PROMPT_TEMPLATE = """You are an expert software engineer generating an authoritative, clean, and robust reference solution for a programming lab.

Lab Title: {title}
Objective: {objective}
Language: {language}
Instructions:
{instructions}

Constraints:
{constraints}

Starter Code:
{starter_code}

Test Cases to Satisfy:
{test_cases}

INSTRUCTIONS:
1. Write the complete, production-grade Python solution that satisfies all instructions, constraints, and test assertions.
2. Return ONLY a valid JSON object with the following schema:
{{
  "reference_code": "Complete valid Python code with imports and function definitions...",
  "explanation": "Concise step-by-step explanation of the reference solution logic..."
}}
"""


class SolutionGenerator:
    """
    Generates reference solution code for a generated lab.
    NOTE: All solutions are treated as UNTRUSTED until verified by SandboxService.
    """

    @classmethod
    def _generate_via_llm(cls, lab: GeneratedLabSchema) -> Optional[dict]:
        prompt = SOLUTION_PROMPT_TEMPLATE.format(
            title=lab.title,
            objective=lab.objective,
            language=lab.language,
            instructions=lab.instructions,
            constraints=json.dumps(lab.constraints),
            starter_code=lab.starter_code,
            test_cases=json.dumps([tc.model_dump() for tc in lab.test_cases], indent=2)
        )

        response_text = ""

        # Priority 1: Groq (Primary LLM Engine)
        if settings.GROQ_API_KEY:
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    model_name=settings.GROQ_MODEL,
                    api_key=settings.GROQ_API_KEY,
                    temperature=0.1
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[SolutionGenerator] Groq invocation fallback: {e}")

        # Priority 2: Fallback to OpenAI
        if not response_text and settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    api_key=settings.OPENAI_API_KEY,
                    temperature=0.1
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[SolutionGenerator] OpenAI invocation fallback: {e}")

        # Priority 3: Further Fallback to Google Gemini
        if not response_text and settings.GOOGLE_API_KEY:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.1
                )
                res = llm.invoke([HumanMessage(content=prompt)])
                response_text = res.content
            except Exception as e:
                print(f"[SolutionGenerator] Gemini invocation fallback: {e}")

        if not response_text:
            return None

        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            data = json.loads(cleaned)
            if "reference_code" in data:
                return data
        except Exception as e:
            print(f"[SolutionGenerator] Failed to parse JSON: {e}")

        return None

    @classmethod
    def _generate_via_template_fallback(cls, lab: GeneratedLabSchema, template_id: Optional[str] = None) -> dict:
        """
        Fallback reference solution from human template for testing without external LLM keys.
        """
        if template_id:
            template = TemplateService.get_template_by_id(template_id)
            if template and template.solution_template:
                return {
                    "reference_code": template.solution_template,
                    "explanation": f"Reference solution derived from human template '{template_id}'."
                }

        # Generic default Python solution based on starter code keywords
        if "process_api_request" in lab.starter_code:
            code = """from typing import List, Optional, Dict, Any

def process_api_request(items: List[Dict[str, Any]], query_id: Optional[int] = None) -> Dict[str, Any]:
    if query_id is not None and query_id < 0:
        raise ValueError("Invalid query_id")
    if query_id is not None:
        filtered = [item for item in items if item.get("id") == query_id]
    else:
        filtered = list(items)
    return {
        "status": "success",
        "data": filtered,
        "count": len(filtered)
    }
"""
        elif "clean_and_aggregate" in lab.starter_code:
            code = """from typing import List, Dict, Any
from collections import defaultdict

def clean_and_aggregate(records: List[Dict[str, Any]], group_col: str, value_col: str) -> Dict[str, Dict[str, float]]:
    groups = defaultdict(list)
    for r in records:
        g = r.get(group_col)
        v = r.get(value_col)
        if g is not None and v is not None:
            groups[str(g)].append(float(v))
    result = {}
    for g, vals in groups.items():
        result[g] = {
            "mean": sum(vals) / len(vals),
            "count": float(len(vals))
        }
    return result
"""
        elif "validate_and_calculate_ratio" in lab.starter_code:
            code = """from typing import List

def validate_and_calculate_ratio(numerator_records: List[float], denominator_records: List[float]) -> float:
    if len(numerator_records) != len(denominator_records):
        raise ValueError("Mismatched list lengths")
    denom_sum = sum(denominator_records)
    if denom_sum == 0:
        raise ZeroDivisionError("Total denominator is zero")
    return round(sum(numerator_records) / denom_sum, 4)
"""
        else:
            code = lab.starter_code

        return {
            "reference_code": code,
            "explanation": "Deterministic baseline solution adhering to template validation logic."
        }

    @classmethod
    def generate_solution(
        cls,
        req: SolutionGenerationRequest,
        db: Optional[Session] = None
    ) -> SolutionGenerationResponse:
        lab_schema = req.lab_schema
        template_id = None
        db_lab = None

        if req.lab_id is not None and db is not None:
            db_lab = db.query(TechnicalGeneratedLab).filter(TechnicalGeneratedLab.id == req.lab_id).first()
            if db_lab:
                template_id = db_lab.template_id
                test_cases_raw = json.loads(db_lab.test_cases_json) if db_lab.test_cases_json else []
                constraints_raw = json.loads(db_lab.constraints_json) if db_lab.constraints_json else []
                from app.modules.technical_courses.schemas import TestCaseSchema
                lab_schema = GeneratedLabSchema(
                    title=db_lab.title,
                    objective=db_lab.objective,
                    language=db_lab.language,
                    difficulty=db_lab.difficulty,
                    instructions=db_lab.instructions,
                    starter_code=db_lab.starter_code,
                    constraints=constraints_raw,
                    test_cases=[TestCaseSchema(**tc) for tc in test_cases_raw],
                    expected_behavior=db_lab.expected_behavior
                )

        if not lab_schema:
            raise ValueError("Either lab_id or lab_schema must be provided for solution generation.")

        # 1. Try LLM
        sol_data = cls._generate_via_llm(lab_schema)

        # 2. Fallback
        if not sol_data:
            sol_data = cls._generate_via_template_fallback(lab_schema, template_id=template_id)

        ref_code = sol_data["reference_code"]
        explanation = sol_data.get("explanation", "")

        solution_id = None
        if db is not None and db_lab is not None:
            # Check existing solution or create new
            existing = db.query(TechnicalLabSolution).filter(TechnicalLabSolution.lab_id == db_lab.id).first()
            if existing:
                existing.reference_code = ref_code
                existing.explanation = explanation
                db.commit()
                db.refresh(existing)
                solution_id = existing.id
            else:
                db_sol = TechnicalLabSolution(
                    lab_id=db_lab.id,
                    reference_code=ref_code,
                    explanation=explanation
                )
                db.add(db_sol)
                db.commit()
                db.refresh(db_sol)
                solution_id = db_sol.id

        return SolutionGenerationResponse(
            lab_id=req.lab_id,
            solution_id=solution_id,
            reference_code=ref_code,
            explanation=explanation,
            is_trusted=False  # Must pass sandbox validation before becoming trusted
        )
