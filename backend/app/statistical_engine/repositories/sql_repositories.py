import json
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.models import StatEngineQuestion, StatEngineAttempt, StatEngineMastery
from app.statistical_engine.questions.generator import QuestionInternalRecord
from app.statistical_engine.repositories.memory_repositories import (
    BaseQuestionRepository,
    BaseAttemptRepository,
    BaseLearnerRepository,
)


class SQLQuestionRepository(BaseQuestionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_instance(self, record: QuestionInternalRecord) -> None:
        data = record.to_dict()
        row = StatEngineQuestion(
            question_id=data["question_id"],
            template_id=data["template_id"],
            skill_id=data["skill_id"],
            competency_id=data["competency_id"],
            question_type=data["question_type"],
            difficulty=data["difficulty"],
            prompt=data["prompt"],
            parameters_json=json.dumps(data["parameters"]),
            correct_answer_json=json.dumps(data["correct_answer"]),
            tolerance=data["tolerance"],
            options_map_json=json.dumps(data["options_map"]),
            correct_option_id=data["correct_option_id"],
            explanation=data["explanation"],
            unit=data["unit"],
            chart_json=json.dumps(data["chart"]) if data["chart"] is not None else None,
            seed=data["seed"],
        )
        self.db.merge(row)
        self.db.commit()

    def get_instance(self, question_id: str) -> Optional[QuestionInternalRecord]:
        row = self.db.query(StatEngineQuestion).filter_by(question_id=question_id).first()
        if not row:
            return None
        return QuestionInternalRecord.from_dict({
            "question_id": row.question_id,
            "template_id": row.template_id,
            "skill_id": row.skill_id,
            "competency_id": row.competency_id,
            "question_type": row.question_type,
            "difficulty": row.difficulty,
            "prompt": row.prompt,
            "parameters": json.loads(row.parameters_json),
            "correct_answer": json.loads(row.correct_answer_json),
            "tolerance": row.tolerance,
            "options_map": json.loads(row.options_map_json),
            "correct_option_id": row.correct_option_id,
            "explanation": row.explanation,
            "unit": row.unit,
            "chart": json.loads(row.chart_json) if row.chart_json else None,
            "seed": row.seed,
        })


class SQLAttemptRepository(BaseAttemptRepository):
    def __init__(self, db: Session):
        self.db = db

    def record_attempt(self, attempt_data: Dict[str, Any]) -> None:
        row = StatEngineAttempt(
            attempt_id=attempt_data["attempt_id"],
            user_id=str(attempt_data["user_id"]),
            question_id=attempt_data["question_id"],
            skill_id=attempt_data["skill_id"],
            submitted_answer=str(attempt_data.get("submitted_answer", "")),
            is_correct=bool(attempt_data.get("is_correct", False)),
            score=float(attempt_data.get("score", 0.0)),
            misconception_id=attempt_data.get("misconception_id"),
            time_taken_seconds=attempt_data.get("time_taken_seconds"),
        )
        self.db.add(row)
        self.db.commit()

    def get_user_attempts(self, user_id: str, skill_id: Optional[str] = None) -> List[Dict[str, Any]]:
        query = self.db.query(StatEngineAttempt).filter_by(user_id=str(user_id))
        if skill_id is not None:
            query = query.filter_by(skill_id=skill_id)
        rows = query.order_by(StatEngineAttempt.created_at.asc()).all()
        return [
            {
                "attempt_id": r.attempt_id,
                "user_id": r.user_id,
                "question_id": r.question_id,
                "skill_id": r.skill_id,
                "submitted_answer": r.submitted_answer,
                "is_correct": r.is_correct,
                "score": r.score,
                "misconception_id": r.misconception_id,
                "time_taken_seconds": r.time_taken_seconds,
                "timestamp": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]


class SQLLearnerRepository(BaseLearnerRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_mastery(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        rows = self.db.query(StatEngineMastery).filter_by(user_id=str(user_id)).all()
        return {r.skill_id: json.loads(r.mastery_json) for r in rows}

    def update_user_skill_mastery(self, user_id: str, skill_id: str, mastery_data: Dict[str, Any]) -> None:
        row = self.db.query(StatEngineMastery).filter_by(user_id=str(user_id), skill_id=skill_id).first()
        if row:
            row.mastery_json = json.dumps(mastery_data)
        else:
            row = StatEngineMastery(user_id=str(user_id), skill_id=skill_id, mastery_json=json.dumps(mastery_data))
            self.db.add(row)
        self.db.commit()
