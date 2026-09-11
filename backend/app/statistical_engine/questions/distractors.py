import random
from typing import Any, Dict, List, Optional, Tuple
from app.statistical_engine.schemas.questions import MCQOption

class DistractorGenerator:
    """
    Generates pedagogically meaningful distractors based on established misconception patterns.
    Ensures options are distinct and non-trivial.
    """

    def generate_distractors(
        self,
        template_id: str,
        operation: str,
        params: Dict[str, Any],
        correct_answer: float,
        distractor_rules: List[Dict[str, Any]],
        rng: random.Random
    ) -> List[Tuple[float, str, Optional[str]]]:
        """
        Returns list of tuples: (distractor_value, formatted_text, misconception_id)
        """
        distractors: List[Tuple[float, str, Optional[str]]] = []
        seen_values = {round(correct_answer, 2)}

        for rule in distractor_rules:
            rule_type = rule.get("type")
            misconception_id = rule.get("misconception_id")
            val: Optional[float] = None

            # Price Relative distractors
            if rule_type == "inverted_ratio":
                base = params.get("base_price", 100)
                curr = params.get("current_price", 120)
                if curr > 0:
                    val = round((base / curr) * 100.0, 2)
            elif rule_type == "absolute_difference":
                base = params.get("base_price", 100)
                curr = params.get("current_price", 120)
                val = float(abs(curr - base))
            elif rule_type == "missing_percentage":
                base = params.get("base_price", 100)
                curr = params.get("current_price", 120)
                if base > 0:
                    val = round(curr / base, 2)

            # Weighted CPI distractors
            elif rule_type == "unweighted_average":
                relatives = [params.get("rel_food", 120), params.get("rel_housing", 110), params.get("rel_fuel", 130)]
                val = round(sum(relatives) / len(relatives), 2)
            elif rule_type == "swapped_weights":
                # Invert weights: give highest weight to lowest relative
                w_food, w_housing, w_fuel = params.get("w_food", 45), params.get("w_housing", 30), params.get("w_fuel", 25)
                rel_food, rel_housing, rel_fuel = params.get("rel_food", 120), params.get("rel_housing", 110), params.get("rel_fuel", 130)
                val = round((rel_food * w_fuel + rel_housing * w_housing + rel_fuel * w_food) / (w_food + w_housing + w_fuel), 2)
            elif rule_type == "offset_index":
                offset = rng.choice([-4.5, 3.8, -2.5, 5.2])
                val = round(correct_answer + offset, 2)

            # Fisher distractors
            elif rule_type == "arithmetic_mean":
                lasp = params.get("laspeyres", 125.0)
                paas = params.get("paasche", 121.0)
                val = round((lasp + paas) / 2.0, 2)
            elif rule_type == "geometric_difference":
                lasp = params.get("laspeyres", 125.0)
                paas = params.get("paasche", 121.0)
                val = round(abs(lasp - paas), 2)
            elif rule_type == "laspeyres_bias":
                val = round(params.get("laspeyres", 125.0), 2)

            # Laspeyres basket distractors
            elif rule_type == "inverted_laspeyres":
                val = round((10000.0 / correct_answer), 2) if correct_answer != 0 else 90.0
            elif rule_type == "unweighted_price_change":
                p0_a, p0_b = params.get("p0_a", 10), params.get("p0_b", 20)
                p1_a, p1_b = params.get("p1_a", 15), params.get("p1_b", 25)
                avg_rel = ((p1_a / p0_a) + (p1_b / p0_b)) / 2.0 * 100.0
                val = round(avg_rel, 2)
            elif rule_type == "paasche_substitution":
                val = round(correct_answer * 0.96, 2)

            # Fallback perturbation
            if val is None or val in seen_values:
                perturbation = rng.choice([-10.0, 8.5, -5.0, 6.2, 12.0])
                val = round(correct_answer + perturbation, 2)

            if val not in seen_values:
                seen_values.add(val)
                distractors.append((val, f"{val:.2f}", misconception_id))

        # Ensure we have at least 3 distractors for a 4-option MCQ
        attempts = 0
        while len(distractors) < 3 and attempts < 10:
            attempts += 1
            delta = rng.choice([-15.0, -7.5, 5.0, 9.5, 14.0])
            cand = round(correct_answer + delta, 2)
            if cand > 0 and cand not in seen_values:
                seen_values.add(cand)
                distractors.append((cand, f"{cand:.2f}", "err.generic.arithmetic_offset"))

        return distractors[:3]

distractor_generator = DistractorGenerator()
