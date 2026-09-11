from typing import Any, Dict, List, Optional
from app.statistical_engine.schemas.questions import QuestionDifficulty

class PersonalizationEngine:
    """
    Transparent, rule-based adaptive engine that selects appropriate skills and difficulty levels
    based on the learner's mastery profile and attempt history.
    """

    def select_skill_and_difficulty(
        self,
        competency_skills: List[Dict[str, Any]],
        learner_mastery: Dict[str, Dict[str, Any]],
        preferred_skill_id: Optional[str] = None,
        requested_difficulty: Optional[QuestionDifficulty] = None
    ) -> (str, QuestionDifficulty):
        """
        Determines the next skill and difficulty.
        """
        # If user explicitly requested a skill and difficulty
        if preferred_skill_id:
            target_skill = preferred_skill_id
        else:
            # Find the first unmastered skill or lowest mastery skill
            target_skill = None
            for s in competency_skills:
                s_id = s["id"]
                m = learner_mastery.get(s_id, {})
                score = m.get("score", 0.0)
                if score < s.get("mastery_threshold", 75.0):
                    target_skill = s_id
                    break

            if not target_skill and competency_skills:
                target_skill = competency_skills[0]["id"]

        # Difficulty progression
        if requested_difficulty:
            diff = requested_difficulty
        else:
            m = learner_mastery.get(target_skill, {})
            score = m.get("score", 0.0)
            if score >= 80.0:
                diff = QuestionDifficulty.ADVANCED
            elif score >= 50.0:
                diff = QuestionDifficulty.INTERMEDIATE
            else:
                diff = QuestionDifficulty.BASIC

        return target_skill, diff

personalization_engine = PersonalizationEngine()
