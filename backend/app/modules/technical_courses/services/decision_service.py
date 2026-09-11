import re
from typing import Tuple, Optional
from app.modules.technical_courses.schemas import DecisionRequest, DecisionResponse


# Action verbs strongly correlated with hands-on labs (Bloom: Apply, Analyze, Create)
LAB_ACTION_VERBS = {
    "implement", "build", "write", "code", "develop", "create", "construct",
    "debug", "fix", "resolve", "patch", "troubleshoot",
    "refactor", "optimize", "rewrite", "modularize",
    "query", "filter", "aggregate", "join", "transform", "parse", "clean",
    "calculate", "compute", "validate", "serialize", "deserialize", "test"
}

# Action verbs strongly correlated with quizzes (Bloom: Remember, Understand)
QUIZ_ACTION_VERBS = {
    "define", "list", "name", "recall", "state", "identify", "recognize",
    "explain", "describe", "summarize", "classify", "compare", "differentiate",
    "understand", "outline", "discuss"
}

# Technical keywords suggesting hands-on coding requirements
HANDS_ON_KEYWORDS = {
    "function", "endpoint", "api", "route", "database", "dataframe", "array",
    "loop", "class", "method", "sql", "pandas", "fastapi", "python", "json",
    "regex", "algorithm", "variable", "parameter", "query", "syntax", "decorator"
}


class DecisionService:
    """
    Extensible decision layer that determines whether a learning objective is best suited
    for a Hands-on Lab or a Quiz.
    """

    @classmethod
    def evaluate(cls, req: DecisionRequest) -> DecisionResponse:
        objective_text = req.objective.strip()
        skill = req.skill.strip()
        action = (req.action or "").lower().strip()

        # Extract primary action verb if not explicitly provided
        if not action:
            first_word_match = re.search(r'^\s*([a-zA-Z]+)', objective_text)
            action = first_word_match.group(1).lower() if first_word_match else ""

        obj_lower = objective_text.lower()
        
        lab_score = 0
        quiz_score = 0

        # 1. Action verb analysis
        if action in LAB_ACTION_VERBS:
            lab_score += 3
        elif action in QUIZ_ACTION_VERBS:
            quiz_score += 3

        # 2. Keyword density analysis
        matched_lab_keywords = [kw for kw in HANDS_ON_KEYWORDS if kw in obj_lower]
        lab_score += min(len(matched_lab_keywords), 3)

        if any(term in obj_lower for term in ["concept", "theory", "history", "overview", "definition", "principles"]):
            quiz_score += 2

        # 3. Determine recommended lab type
        recommended_lab_type = None
        if action in ["debug", "fix", "troubleshoot"] or any(w in obj_lower for w in ["debug", "fix", "exception", "traceback"]):
            recommended_lab_type = "debugging"
        elif action in ["refactor", "optimize", "rewrite"]:
            recommended_lab_type = "refactoring"
        elif any(w in skill.lower() for w in ["pandas", "data science", "survey", "cpi", "dataset"]) or (action in ["clean", "aggregate"] and "api" not in obj_lower):
            recommended_lab_type = "data_analysis"
        else:
            recommended_lab_type = "implementation"

        # 4. Decision resolution
        if lab_score >= quiz_score:
            confidence = min(0.95, 0.60 + (lab_score * 0.08))
            mode = "lab"
            reasoning = (
                f"Objective emphasizes hands-on application/creation via action '{action}' "
                f"and technical elements ({', '.join(matched_lab_keywords[:3]) if matched_lab_keywords else skill}), "
                f"which is best evaluated through interactive sandbox code execution."
            )
        else:
            confidence = min(0.95, 0.60 + (quiz_score * 0.08))
            mode = "quiz"
            recommended_lab_type = None
            reasoning = (
                f"Objective focuses on conceptual comprehension and theoretical recall ('{action}'), "
                f"which is effectively assessed through standardized conceptual multiple-choice questions."
            )

        return DecisionResponse(
            assessment_mode=mode,
            confidence=round(confidence, 2),
            reasoning=reasoning,
            recommended_lab_type=recommended_lab_type
        )
