# Question Authoring Guide

This guide explains how content creators and subject matter experts (MoSPI / NSSTA faculty) can author new parameterized question templates without modifying Python source code.

---

## 1. Template Structure

Question templates are stored in `backend/content/questions/<domain>.json`. Each template adheres to the following JSON schema:

```json
{
  "template_id": "price.cpi.weighted.mcq.001",
  "skill_id": "price.cpi.weighted_price_relatives",
  "type": "mcq",
  "difficulty": "intermediate",
  "prompt_template": "A district consumer basket consists of three essential commodity groups with the following price relatives and expenditure weights:\n• Food: Relative = {rel_food}, Weight = {w_food}\n• Housing: Relative = {rel_housing}, Weight = {w_housing}\n• Fuel & Light: Relative = {rel_fuel}, Weight = {w_fuel}\n\nCompute the overall Consumer Price Index (CPI).",
  "parameters": {
    "rel_food": {"type": "integer", "min": 110, "max": 140, "step": 5},
    "rel_housing": {"type": "integer", "min": 105, "max": 130, "step": 5},
    "rel_fuel": {"type": "integer", "min": 115, "max": 150, "step": 5},
    "w_food": {"type": "integer", "min": 40, "max": 50, "step": 5},
    "w_housing": {"type": "integer", "min": 25, "max": 35, "step": 5},
    "w_fuel": {"type": "integer", "min": 20, "max": 30, "step": 5}
  },
  "operation": "weighted_price_relatives_basket",
  "unit": "index_points",
  "distractor_rules": [
    {
      "type": "unweighted_average",
      "misconception_id": "err.cpi.unweighted_average",
      "description": "Computed simple arithmetic mean instead of weighted index"
    },
    {
      "type": "swapped_weights",
      "misconception_id": "err.cpi.swapped_weights",
      "description": "Inverted weight allocations across commodity groups"
    }
  ],
  "explanation_template": "CPI = Σ(W × R) / ΣW = [({w_food}×{rel_food}) + ({w_housing}×{rel_housing}) + ({w_fuel}×{rel_fuel})] / ({w_food} + {w_housing} + {w_fuel}) = {answer:.2f}."
}
```

---

## 2. Field Descriptions

| Field | Type | Description |
|---|---|---|
| `template_id` | `string` | Unique, stable identifier (e.g. `domain.concept.type.seq`). |
| `skill_id` | `string` | Foreign key referencing a skill in `content/competencies/*.json`. |
| `type` | `string` | `numeric`, `mcq`, `chart_interpretation`, or `true_false`. |
| `difficulty` | `string` | `basic`, `intermediate`, or `advanced`. |
| `prompt_template` | `string` | Question prompt with `{param_name}` replacement tokens. |
| `parameters` | `object` | Bounds, step sizes, and optional constraints for each variable. |
| `operation` | `string` | Registered computation in `BaseStatisticalModule`. |
| `distractor_rules` | `array` | Rule-based misconceptions for generating realistic MCQ distractors. |
| `explanation_template` | `string` | Step-by-step mathematical derivation formatted for the learner. |

---

## 3. Parameter Constraints

Parameters can define relational constraints using safe inequality expressions:

```json
"current_price": {
  "type": "integer",
  "min": 30,
  "max": 120,
  "constraint": "current_price > base_price"
}
```

---

## 4. Misconception Taxonomy

Each distractor should be linked to a known pedagogical misconception:
- `err.price.inverted_ratio`: Inverted base and current prices ($P_0 / P_1 \times 100$).
- `err.price.missing_percentage`: Forgot to multiply ratio by 100.
- `err.cpi.unweighted_average`: Used simple arithmetic average instead of expenditure weights.
- `err.fisher.arithmetic_mean`: Computed $(I_L + I_P) / 2$ instead of $\sqrt{I_L \times I_P}$.
