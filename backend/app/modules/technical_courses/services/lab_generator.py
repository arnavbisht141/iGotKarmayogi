import json
import re
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage
from app.core.config import settings
from app.models.models import TechnicalGeneratedLab
from app.modules.technical_courses.schemas import (
    GeneratedLabSchema, LabGenerationRequest, LabGenerationResponse,
    LabTemplateSchema, TestCaseSchema
)
from app.modules.technical_courses.services.template_service import TemplateService


LAB_GEN_PROMPT_TEMPLATE = """You are an expert technical curriculum engineer creating a hands-on programming lab for civil servants and technical learners.

A human educator has defined the following LAB TEMPLATE structure and constraints:
--------------------------------------------------
Template ID: {template_id}
Title: {template_title}
Skill: {template_skill}
Language: {template_language}
Difficulty: {template_difficulty}
Base Constraints: {constraints}
Starter Code Structure:
{starter_code_template}

Test Cases Harness Template:
{test_cases_template}
--------------------------------------------------

Your task is to adapt this HUMAN-CONTROLLED TEMPLATE for the following SPECIFIC LEARNING OBJECTIVE:
Learning Objective: {objective}
Additional Context: {course_context}

INSTRUCTIONS:
1. Preserve the core function signature and test logic from the template.
2. Customize the problem description, variable names, and context to match the learning objective.
3. Return ONLY a valid JSON object strictly matching this schema:
{{
  "title": "{template_title}",
  "objective": "{objective}",
  "language": "{template_language}",
  "difficulty": "{template_difficulty}",
  "instructions": "Detailed markdown instructions for the learner...",
  "starter_code": "Python code with function definition and docstring...",
  "constraints": ["constraint 1", "constraint 2"],
  "test_cases": [
    {{
      "name": "test_case_name",
      "description": "what this test verifies",
      "test_code": "python assertion code...",
      "is_hidden": false,
      "weight": 1.0
    }}
  ],
  "expected_behavior": "Description of expected output or return values"
}}
"""


class LabGenerator:
    """
    Generates a concrete, machine-readable hands-on coding lab by filling
    a human-created lab template using structured LLM synthesis.
    """

    @classmethod
    def _generate_via_llm(
        cls,
        template: LabTemplateSchema,
        req: LabGenerationRequest
    ) -> Optional[GeneratedLabSchema]:
        constraints_str = json.dumps(template.constraints)
        test_cases_str = json.dumps([tc.model_dump() for tc in template.test_cases_template], indent=2)

        prompt = LAB_GEN_PROMPT_TEMPLATE.format(
            template_id=template.id,
            template_title=template.title,
            template_skill=template.skill,
            template_language=template.language,
            template_difficulty=template.difficulty,
            constraints=constraints_str,
            starter_code_template=template.starter_code_template,
            test_cases_template=test_cases_str,
            objective=req.objective.objective,
            course_context=req.course_context or "Government data & engineering workflows"
        )

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
                print(f"[LabGenerator] Groq invocation fallback: {e}")

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
                print(f"[LabGenerator] OpenAI invocation fallback: {e}")

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
                print(f"[LabGenerator] Gemini invocation fallback: {e}")

        if not response_text:
            return None

        # Clean JSON fences
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            data = json.loads(cleaned)
            test_cases = [TestCaseSchema(**tc) for tc in data.get("test_cases", [])]
            return GeneratedLabSchema(
                title=data.get("title") or template.title,
                objective=data.get("objective") or req.objective.objective,
                language=template.language,
                difficulty=template.difficulty,
                instructions=data.get("instructions") or template.instructions_template.format(
                    objective=req.objective.objective,
                    function_name="process_data"
                ),
                starter_code=data.get("starter_code") or template.starter_code_template,
                constraints=data.get("constraints") or template.constraints,
                test_cases=test_cases if test_cases else template.test_cases_template,
                expected_behavior=data.get("expected_behavior")
            )
        except Exception as e:
            print(f"[LabGenerator] Failed to parse generated lab JSON: {e}")

        return None

    @classmethod
    def _generate_via_template_fallback(
        cls,
        template: LabTemplateSchema,
        req: LabGenerationRequest
    ) -> GeneratedLabSchema:
        """
        Deterministic filling of human-created template for development/testing without LLM keys.
        """
        instructions = template.instructions_template.format(
            objective=req.objective.objective,
            function_name="solution_function"
        )
        return GeneratedLabSchema(
            title=f"{template.title} - {req.objective.skill}",
            objective=req.objective.objective,
            language=template.language,
            difficulty=template.difficulty,
            instructions=instructions,
            starter_code=template.starter_code_template,
            constraints=template.constraints,
            test_cases=template.test_cases_template,
            expected_behavior=f"Code must satisfy all {len(template.test_cases_template)} unit test assertions without throwing unexpected exceptions."
        )

    @classmethod
    def generate_lab(
        cls,
        req: LabGenerationRequest,
        db: Optional[Session] = None
    ) -> LabGenerationResponse:
        """
        Generates a concrete lab from a matched template and learning objective.
        """
        template = TemplateService.get_template_by_id(req.template_id, db=db)
        if not template:
            # Fallback to general template
            templates = TemplateService.get_all_templates(db=db)
            template = templates[0]

        # 1. Attempt LLM generation
        generated = cls._generate_via_llm(template, req)

        # 2. Testing fallback
        if not generated:
            generated = cls._generate_via_template_fallback(template, req)

        # 3. Optional Persistence
        lab_id = None
        if db is not None:
            tc_data = [tc.model_dump() for tc in generated.test_cases]
            db_lab = TechnicalGeneratedLab(
                template_id=template.id,
                title=generated.title,
                objective=generated.objective,
                language=generated.language,
                difficulty=generated.difficulty,
                instructions=generated.instructions,
                starter_code=generated.starter_code,
                constraints_json=json.dumps(generated.constraints),
                test_cases_json=json.dumps(tc_data),
                expected_behavior=generated.expected_behavior,
                status="draft"
            )
            db.add(db_lab)
            db.commit()
            db.refresh(db_lab)
            lab_id = db_lab.id

        return LabGenerationResponse(
            lab_id=lab_id,
            template_id=template.id,
            lab=generated,
            status="draft"
        )
