from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.statistical_engine.questions.generator import QuestionInternalRecord

class BaseQuestionRepository(ABC):
    @abstractmethod
    def save_instance(self, record: QuestionInternalRecord) -> None:
        pass

    @abstractmethod
    def get_instance(self, question_id: str) -> Optional[QuestionInternalRecord]:
        pass

class BaseAttemptRepository(ABC):
    @abstractmethod
    def record_attempt(self, attempt_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_user_attempts(self, user_id: str, skill_id: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

class BaseLearnerRepository(ABC):
    @abstractmethod
    def get_user_mastery(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        pass

    @abstractmethod
    def update_user_skill_mastery(self, user_id: str, skill_id: str, mastery_data: Dict[str, Any]) -> None:
        pass

# --- In-Memory Implementations for fast testing & fallback ---

class InMemoryQuestionRepository(BaseQuestionRepository):
    def __init__(self):
        self._instances: Dict[str, QuestionInternalRecord] = {}

    def save_instance(self, record: QuestionInternalRecord) -> None:
        self._instances[record.question_id] = record

    def get_instance(self, question_id: str) -> Optional[QuestionInternalRecord]:
        return self._instances.get(question_id)

class InMemoryAttemptRepository(BaseAttemptRepository):
    def __init__(self):
        self._attempts: List[Dict[str, Any]] = []

    def record_attempt(self, attempt_data: Dict[str, Any]) -> None:
        self._attempts.append(attempt_data)

    def get_user_attempts(self, user_id: str, skill_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return [
            a for a in self._attempts
            if a.get("user_id") == user_id and (skill_id is None or a.get("skill_id") == skill_id)
        ]

class InMemoryLearnerRepository(BaseLearnerRepository):
    def __init__(self):
        # user_id -> skill_id -> mastery_dict
        self._learner_states: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def get_user_mastery(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        return self._learner_states.get(user_id, {})

    def update_user_skill_mastery(self, user_id: str, skill_id: str, mastery_data: Dict[str, Any]) -> None:
        if user_id not in self._learner_states:
            self._learner_states[user_id] = {}
        self._learner_states[user_id][skill_id] = mastery_data

question_repo = InMemoryQuestionRepository()
attempt_repo = InMemoryAttemptRepository()
learner_repo = InMemoryLearnerRepository()
