from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.statistical_engine.config import engine_settings
from app.statistical_engine.schemas.competencies import LearnerSkillMasterySchema

class MasteryEvaluator:
    """
    Interpretable skill mastery tracking on a normalized 0-100 scale.
    """

    def compute_level(self, score: float) -> str:
        if score >= 90.0:
            return "master"
        elif score >= 75.0:
            return "advanced"
        elif score >= 50.0:
            return "intermediate"
        elif score >= 25.0:
            return "basic"
        return "novice"

    def update_mastery(
        self,
        current_mastery: Optional[Dict[str, Any]],
        skill_id: str,
        correct: bool,
        score_weight: float = 1.0,
        misconception_id: Optional[str] = None
    ) -> LearnerSkillMasterySchema:
        score = current_mastery.get("score", 0.0) if current_mastery else 0.0
        attempts = current_mastery.get("attempts_count", 0) if current_mastery else 0
        correct_count = current_mastery.get("correct_count", 0) if current_mastery else 0
        confidence = current_mastery.get("confidence", 0.5) if current_mastery else 0.5
        consecutive_errors = current_mastery.get("consecutive_errors", 0) if current_mastery else 0

        attempts += 1
        now_str = datetime.now(timezone.utc).isoformat()

        if correct:
            correct_count += 1
            consecutive_errors = 0
            # Increment score smoothly toward 100
            gain = engine_settings.DEFAULT_MASTERY_INCREMENT * score_weight
            score = min(100.0, score + gain)
            confidence = min(1.0, confidence + 0.08)
            remediation = False
        else:
            consecutive_errors += 1
            loss = engine_settings.DEFAULT_MASTERY_DECREMENT
            score = max(0.0, score - loss)
            confidence = max(0.1, confidence - 0.06)
            remediation = consecutive_errors >= 2 or bool(misconception_id)

        level = self.compute_level(score)

        return LearnerSkillMasterySchema(
            skill_id=skill_id,
            score=round(score, 1),
            level=level,
            confidence=round(confidence, 2),
            attempts_count=attempts,
            correct_count=correct_count,
            remediation_recommended=remediation,
            last_attempt_at=now_str
        )

mastery_evaluator = MasteryEvaluator()
