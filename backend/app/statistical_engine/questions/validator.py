import math
from typing import Any, Dict, List, Optional
from app.statistical_engine.core.exceptions import ValidationException

class QuestionValidator:
    """
    Validates question instances prior to API exposure.
    Enforces strict mathematical, pedagogical, and structural guarantees.
    """

    def validate_numeric_question(
        self,
        prompt: str,
        answer: float,
        params: Dict[str, Any],
        tolerance: float
    ) -> None:
        if not prompt or not prompt.strip():
            raise ValidationException("Question prompt must not be empty.")
        if not math.isfinite(answer):
            raise ValidationException("Calculated answer must be a finite numerical value.", details={"answer": str(answer)})
        if tolerance < 0:
            raise ValidationException("Tolerance cannot be negative.", details={"tolerance": tolerance})

    def validate_mcq_question(
        self,
        prompt: str,
        correct_option_id: str,
        options: List[Dict[str, Any]],
        correct_value: float
    ) -> None:
        if not prompt or not prompt.strip():
            raise ValidationException("MCQ prompt must not be empty.")
        if not options or len(options) < 2:
            raise ValidationException("MCQ must contain at least 2 options.", details={"options_count": len(options) if options else 0})

        option_ids = [opt["id"] for opt in options]
        if len(option_ids) != len(set(option_ids)):
            raise ValidationException("Duplicate option IDs found in MCQ.", details={"option_ids": option_ids})

        option_texts = [str(opt["text"]).strip().lower() for opt in options]
        if len(option_texts) != len(set(option_texts)):
            raise ValidationException("Duplicate option texts found in MCQ.", details={"options": option_texts})

        if correct_option_id not in option_ids:
            raise ValidationException(
                f"Correct option ID '{correct_option_id}' is not present in options.",
                details={"correct_id": correct_option_id, "available_ids": option_ids}
            )

        # Check that exactly one option matches correct_option_id
        matching = [opt for opt in options if opt["id"] == correct_option_id]
        if len(matching) != 1:
            raise ValidationException("Exactly one option must be designated as correct.")

    def validate_chart_spec(self, chart_spec: Dict[str, Any]) -> None:
        if not chart_spec:
            raise ValidationException("Chart specification cannot be empty.")
        if "type" not in chart_spec or not chart_spec["type"]:
            raise ValidationException("Chart specification missing required 'type'.")
        if "data" not in chart_spec or not isinstance(chart_spec["data"], list) or len(chart_spec["data"]) == 0:
            raise ValidationException("Chart data array must contain at least one data point.")
        
        # Validate data fields
        x_field = chart_spec.get("xAxis", {}).get("field")
        y_field = chart_spec.get("yAxis", {}).get("field")
        for idx, pt in enumerate(chart_spec["data"]):
            if x_field and x_field not in pt:
                raise ValidationException(f"Chart data point at index {idx} missing x-field '{x_field}'.")
            if y_field and y_field not in pt:
                raise ValidationException(f"Chart data point at index {idx} missing y-field '{y_field}'.")

question_validator = QuestionValidator()
