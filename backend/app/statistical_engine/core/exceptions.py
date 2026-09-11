from typing import Any, Dict, Optional

class StatisticalEngineException(Exception):
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

class InvalidStatisticalInputException(StatisticalEngineException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(code="INVALID_STATISTICAL_INPUT", message=message, details=details)

class CompetencyNotFoundException(StatisticalEngineException):
    def __init__(self, competency_id: str):
        super().__init__(
            code="COMPETENCY_NOT_FOUND",
            message=f"Competency with ID '{competency_id}' was not found.",
            details={"competency_id": competency_id}
        )

class QuestionGenerationException(StatisticalEngineException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(code="QUESTION_GENERATION_FAILED", message=message, details=details)

class ValidationException(StatisticalEngineException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(code="QUESTION_VALIDATION_FAILED", message=message, details=details)

class AttemptNotFoundException(StatisticalEngineException):
    def __init__(self, question_id: str):
        super().__init__(
            code="QUESTION_INSTANCE_NOT_FOUND",
            message=f"No stored question instance found for ID '{question_id}'.",
            details={"question_id": question_id}
        )
