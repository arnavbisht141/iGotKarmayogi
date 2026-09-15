from typing import Any, Dict, Optional
from app.statistical_engine.schemas.questions import NextActionSchema

class BranchingEngine:
    """
    Evaluates declarative branching rules based on answer correctness, misconceptions,
    consecutive failures, and skill relationships.
    """

    def evaluate(
        self,
        skill_id: str,
        correct: bool,
        misconception_id: Optional[str],
        consecutive_errors: int,
        mastery_score: float
    ) -> NextActionSchema:
        # Rule 1: High Consecutive Errors -> Prerequisite or remediation
        if not correct and consecutive_errors >= 2:
            if skill_id == "price.cpi.weighted_price_relatives":
                return NextActionSchema(
                    type="remediation",
                    target_skill_id="price.price_relative",
                    message="Repeated difficulties detected. Routing to foundational Price Relative concepts."
                )
            elif skill_id == "price.fisher_index":
                return NextActionSchema(
                    type="remediation",
                    target_skill_id="price.laspeyres_index",
                    message="Routing to Laspeyres index revision before attempting Fisher ideal index."
                )
            else:
                return NextActionSchema(
                    type="remediation",
                    target_skill_id=skill_id,
                    message="Foundational review recommended before advancing."
                )

        # Rule 2: Targeted Misconception Remediation
        if not correct and misconception_id:
            if misconception_id == "err.price.inverted_ratio":
                return NextActionSchema(
                    type="remediation",
                    target_skill_id="price.price_relative",
                    message="Notice: Price relative must place Current Price in the numerator and Base Price in denominator."
                )
            elif misconception_id == "err.fisher.arithmetic_mean":
                return NextActionSchema(
                    type="remediation",
                    target_skill_id="price.fisher_index",
                    message="Recall: Fisher index is the geometric mean (square root of product), not the arithmetic mean."
                )

        # Rule 3: Correct answer with high mastery -> Advance to next skill
        if correct and mastery_score >= 80.0:
            skill_progression = {
                "price.price_relative": "price.weights",
                "price.weights": "price.cpi.weighted_price_relatives",
                "price.cpi.weighted_price_relatives": "price.inflation_rate",
                "price.inflation_rate": "price.laspeyres_index",
                "price.laspeyres_index": "price.paasche_index",
                "price.paasche_index": "price.fisher_index",
                "price.fisher_index": "price.real_vs_nominal",
            }
            next_skill = skill_progression.get(skill_id)
            if next_skill:
                return NextActionSchema(
                    type="question",
                    target_skill_id=next_skill,
                    message=f"Mastery achieved in {skill_id}! Advancing to {next_skill}."
                )
            else:
                return NextActionSchema(
                    type="competency_complete",
                    target_skill_id=skill_id,
                    message="Congratulations! All core skills in Price Statistics mastered."
                )

        # Default: Continue on same skill
        return NextActionSchema(
            type="question",
            target_skill_id=skill_id,
            message="Keep practicing to reinforce mastery."
        )

branching_engine = BranchingEngine()
