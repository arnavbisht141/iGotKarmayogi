import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import TechnicalLabTemplate
from app.modules.technical_courses.schemas import (
    LabTemplateSchema, TestCaseSchema, TemplateMatchRequest, TemplateMatchResponse
)


# Standard human-created starter templates for built-in catalog
BUILTIN_LAB_TEMPLATES: List[LabTemplateSchema] = [
    LabTemplateSchema(
        id="python-fastapi-crud-001",
        title="REST API Endpoint Implementation with FastAPI",
        skill="FastAPI",
        language="python",
        difficulty="intermediate",
        lab_type="implementation",
        tags=["fastapi", "api", "rest", "http", "crud", "pydantic", "backend"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Implement the requested FastAPI endpoint logic in the function `{function_name}`.
2. Ensure proper HTTP status codes and input validation using Pydantic models.
3. Handle error cases: return status code 404 when an entity is missing, and status code 400 for malformed parameters.
4. Follow clean code and type annotations.
""",
        starter_code_template="""from typing import List, Optional, Dict, Any

def process_api_request(items: List[Dict[str, Any]], query_id: Optional[int] = None) -> Dict[str, Any]:
    \"\"\"
    TODO: Implement the required endpoint logic.
    - Filter items if query_id is provided.
    - Return a dict with 'status': 'success', 'data': [...], 'count': int
    - If query_id is negative, raise ValueError("Invalid query_id")
    \"\"\"
    # Write your solution below:
    pass
""",
        solution_template="""from typing import List, Optional, Dict, Any

def process_api_request(items: List[Dict[str, Any]], query_id: Optional[int] = None) -> Dict[str, Any]:
    if query_id is not None and query_id < 0:
        raise ValueError("Invalid query_id")
    
    if query_id is not None:
        filtered = [item for item in items if item.get("id") == query_id]
    else:
        filtered = list(items)
        
    return {
        "status": "success",
        "data": filtered,
        "count": len(filtered)
    }
""",
        constraints=[
            "Do not import unauthorized subprocess or filesystem libraries.",
            "Use type hints for function arguments and return types.",
            "Ensure input validation raises ValueError for negative ID."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_get_all_items",
                description="Verifies endpoint returns all records when query_id is None",
                test_code="""
items = [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]
res = process_api_request(items, None)
assert res["status"] == "success", f"Expected status 'success', got {res.get('status')}"
assert res["count"] == 2, f"Expected count 2, got {res.get('count')}"
assert len(res["data"]) == 2
"""
            ),
            TestCaseSchema(
                name="test_filter_by_id",
                description="Verifies endpoint filters correctly by ID",
                test_code="""
items = [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}, {"id": 3, "name": "Item C"}]
res = process_api_request(items, 2)
assert res["count"] == 1, f"Expected count 1, got {res.get('count')}"
assert res["data"][0]["name"] == "Item B"
"""
            ),
            TestCaseSchema(
                name="test_negative_id_validation",
                description="Verifies ValueError is raised for negative query ID",
                test_code="""
items = [{"id": 1, "name": "Item A"}]
try:
    process_api_request(items, -1)
    assert False, "Expected ValueError for negative query_id"
except ValueError:
    pass
"""
            )
        ]
    ),
    LabTemplateSchema(
        id="python-pandas-transform-001",
        title="Data Cleaning & Aggregation Pipeline with Pandas",
        skill="Pandas",
        language="python",
        difficulty="intermediate",
        lab_type="data_analysis",
        tags=["pandas", "data", "dataframe", "cleaning", "aggregation", "statistics", "csv"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Implement the data pipeline function `{function_name}`.
2. Filter out rows containing null values in the primary numerical columns.
3. Compute the group-by mean and total count for each category.
4. Return a structured dictionary containing the summary statistics.
""",
        starter_code_template="""from typing import List, Dict, Any

def clean_and_aggregate(records: List[Dict[str, Any]], group_col: str, value_col: str) -> Dict[str, Dict[str, float]]:
    \"\"\"
    TODO: Implement the data cleaning and aggregation logic.
    - Ignore records where group_col or value_col is None.
    - For each distinct group in group_col, calculate 'mean' and 'count' of value_col.
    - Return format: { group_name: {'mean': float, 'count': float} }
    \"\"\"
    # Write your solution below:
    pass
""",
        solution_template="""from typing import List, Dict, Any
from collections import defaultdict

def clean_and_aggregate(records: List[Dict[str, Any]], group_col: str, value_col: str) -> Dict[str, Dict[str, float]]:
    groups = defaultdict(list)
    for r in records:
        g = r.get(group_col)
        v = r.get(value_col)
        if g is not None and v is not None:
            groups[str(g)].append(float(v))
            
    result = {}
    for g, vals in groups.items():
        result[g] = {
            "mean": sum(vals) / len(vals),
            "count": float(len(vals))
        }
    return result
""",
        constraints=[
            "Handle empty input gracefully by returning an empty dictionary.",
            "Null/None values in either column must be filtered out before calculation.",
            "Results must be strictly typed floating-point numbers."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_clean_and_aggregate_basic",
                description="Tests standard grouping and mean calculation",
                test_code="""
data = [
    {"dept": "Statistics", "score": 80},
    {"dept": "Statistics", "score": 100},
    {"dept": "Finance", "score": 90}
]
res = clean_and_aggregate(data, "dept", "score")
assert "Statistics" in res
assert res["Statistics"]["mean"] == 90.0
assert res["Statistics"]["count"] == 2.0
assert res["Finance"]["mean"] == 90.0
"""
            ),
            TestCaseSchema(
                name="test_handle_null_values",
                description="Tests filtering of records with None values",
                test_code="""
data = [
    {"dept": "HR", "score": None},
    {"dept": None, "score": 50},
    {"dept": "HR", "score": 70}
]
res = clean_and_aggregate(data, "dept", "score")
assert "HR" in res
assert res["HR"]["count"] == 1.0
assert res["HR"]["mean"] == 70.0
assert None not in res
"""
            ),
            TestCaseSchema(
                name="test_empty_input",
                description="Tests that empty input returns an empty dict",
                test_code="""
res = clean_and_aggregate([], "dept", "score")
assert res == {}, f"Expected empty dict, got {res}"
"""
            )
        ]
    ),
    LabTemplateSchema(
        id="python-debugging-pfms-001",
        title="Debugging & Exception Resolution in Data Validation Routines",
        skill="Python Debugging",
        language="python",
        difficulty="intermediate",
        lab_type="debugging",
        tags=["debugging", "python", "bug", "exception", "validation", "troubleshoot", "fix"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Inspect the buggy implementation of `{function_name}`.
2. Identify the bug causing incorrect boundary validation and division-by-zero errors.
3. Fix the implementation so all edge-case assertions pass cleanly.
""",
        starter_code_template="""from typing import List, Dict, Any

def validate_and_calculate_ratio(numerator_records: List[float], denominator_records: List[float]) -> float:
    \"\"\"
    BUGGY IMPLEMENTATION:
    Currently fails when lists have mismatched lengths or when denominator sum is zero.
    
    Fix this function so that:
    1. It raises ValueError("Mismatched list lengths") if len(num) != len(denom).
    2. If denominator sum is 0, it raises ZeroDivisionError("Total denominator is zero").
    3. Otherwise, returns (sum(numerator) / sum(denominator)) rounded to 4 decimal places.
    \"\"\"
    # FIX THE CODE BELOW:
    return sum(numerator_records) / sum(denominator_records)
""",
        solution_template="""from typing import List, Dict, Any

def validate_and_calculate_ratio(numerator_records: List[float], denominator_records: List[float]) -> float:
    if len(numerator_records) != len(denominator_records):
        raise ValueError("Mismatched list lengths")
    denom_sum = sum(denominator_records)
    if denom_sum == 0:
        raise ZeroDivisionError("Total denominator is zero")
    return round(sum(numerator_records) / denom_sum, 4)
""",
        constraints=[
            "Strictly raise ValueError on mismatched input lengths.",
            "Strictly raise ZeroDivisionError when denominator total is zero.",
            "Do not modify the function signature."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_valid_calculation",
                description="Tests correct ratio calculation on clean data",
                test_code="""
nums = [10.0, 20.0, 30.0]
denoms = [5.0, 5.0, 10.0]
res = validate_and_calculate_ratio(nums, denoms)
assert res == 3.0, f"Expected 3.0, got {res}"
"""
            ),
            TestCaseSchema(
                name="test_mismatched_length_exception",
                description="Tests ValueError on mismatched lists",
                test_code="""
try:
    validate_and_calculate_ratio([1.0, 2.0], [1.0])
    assert False, "Expected ValueError"
except ValueError as e:
    assert "Mismatched" in str(e)
"""
            ),
            TestCaseSchema(
                name="test_zero_division_exception",
                description="Tests ZeroDivisionError when sum of denominator is 0",
                test_code="""
try:
    validate_and_calculate_ratio([10.0, 20.0], [5.0, -5.0])
    assert False, "Expected ZeroDivisionError"
except ZeroDivisionError:
    pass
"""
            )
        ]
    ),
    LabTemplateSchema(
        id="python-sql-analytics-001",
        title="SQL Analytics & In-Memory Table Query Engine",
        skill="SQL",
        language="python",
        difficulty="intermediate",
        lab_type="data_analysis",
        tags=["sql", "query", "database", "sqlite", "table", "analytics", "filter", "aggregate", "join", "select"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Implement the database query function `{function_name}` using Python's `sqlite3` library.
2. Create an in-memory database table, insert the given records, and execute the required SQL query.
3. Return the query results as a list of dictionaries with column names as keys.
4. Handle cases where the dataset is empty by returning an empty list.
""",
        starter_code_template="""import sqlite3
from typing import List, Dict, Any

def run_sql_query(records: List[Dict[str, Any]], min_score: float = 0.0) -> List[Dict[str, Any]]:
    \"\"\"
    TODO: Create an in-memory sqlite3 database table named 'submissions',
    insert records, and run:
    SELECT department, COUNT(*) as total_records, AVG(score) as avg_score
    FROM submissions
    WHERE score >= ?
    GROUP BY department
    ORDER BY department ASC
    
    Return the result as a list of dicts:
    [{'department': str, 'total_records': int, 'avg_score': float}]
    \"\"\"
    # Write your solution below:
    pass
""",
        solution_template="""import sqlite3
from typing import List, Dict, Any

def run_sql_query(records: List[Dict[str, Any]], min_score: float = 0.0) -> List[Dict[str, Any]]:
    if not records:
        return []
    
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE submissions (id INTEGER, department TEXT, score REAL)")
    
    for r in records:
        cursor.execute("INSERT INTO submissions VALUES (?, ?, ?)", (r.get("id"), r.get("department"), r.get("score")))
    
    conn.commit()
    
    query = \"\"\"
    SELECT department, COUNT(*) as total_records, AVG(score) as avg_score
    FROM submissions
    WHERE score >= ?
    GROUP BY department
    ORDER BY department ASC
    \"\"\"
    cursor.execute(query, (min_score,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"department": row[0], "total_records": row[1], "avg_score": round(float(row[2]), 2)}
        for row in rows
    ]
""",
        constraints=[
            "Use sqlite3 in-memory database ':memory:'.",
            "Ensure connection is properly closed after query execution.",
            "Order query results by department ascending."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_sql_aggregation",
                description="Tests standard SQL aggregation with grouping",
                test_code="""
data = [
    {"id": 1, "department": "Statistics", "score": 85.0},
    {"id": 2, "department": "Statistics", "score": 95.0},
    {"id": 3, "department": "Finance", "score": 70.0}
]
res = run_sql_query(data, min_score=80.0)
assert len(res) == 1
assert res[0]["department"] == "Statistics"
assert res[0]["total_records"] == 2
assert res[0]["avg_score"] == 90.0
"""
            ),
            TestCaseSchema(
                name="test_sql_empty_input",
                description="Tests that empty records return empty list",
                test_code="""
res = run_sql_query([], min_score=50.0)
assert res == []
"""
            )
        ]
    ),
    LabTemplateSchema(
        id="python-ml-evaluation-001",
        title="Machine Learning Model Evaluation & Classification Metrics",
        skill="AI/ML",
        language="python",
        difficulty="intermediate",
        lab_type="data_analysis",
        tags=["ai-ml", "machine-learning", "metrics", "accuracy", "precision", "recall", "f1", "evaluation", "classification"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Implement `{function_name}` to calculate classification performance metrics.
2. Compute True Positives (TP), False Positives (FP), True Negatives (TN), and False Negatives (FN).
3. Calculate Accuracy, Precision, Recall, and F1-Score.
4. If (Precision + Recall) is 0, F1-Score should be returned as 0.0.
""",
        starter_code_template="""from typing import List, Dict

def evaluate_classification_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    \"\"\"
    TODO: Compute binary classification metrics.
    Return a dict:
    {
        'accuracy': float,
        'precision': float,
        'recall': float,
        'f1_score': float
    }
    Raise ValueError("Length mismatch") if len(y_true) != len(y_pred).
    \"\"\"
    # Write your solution below:
    pass
""",
        solution_template="""from typing import List, Dict

def evaluate_classification_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch")
    if not y_true:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}
        
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    total = len(y_true)
    
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }
""",
        constraints=[
            "Raise ValueError when input lists have differing lengths.",
            "Guard against ZeroDivisionError for precision, recall, and F1 calculations.",
            "Round returned float values to 4 decimal places."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_perfect_predictions",
                description="Tests metrics when predictions are 100% accurate",
                test_code="""
yt = [1, 0, 1, 1, 0]
yp = [1, 0, 1, 1, 0]
metrics = evaluate_classification_metrics(yt, yp)
assert metrics["accuracy"] == 1.0
assert metrics["precision"] == 1.0
assert metrics["recall"] == 1.0
assert metrics["f1_score"] == 1.0
"""
            ),
            TestCaseSchema(
                name="test_imperfect_predictions",
                description="Tests standard metrics with some false positives and false negatives",
                test_code="""
yt = [1, 1, 0, 0]
yp = [1, 0, 1, 0]
metrics = evaluate_classification_metrics(yt, yp)
assert metrics["accuracy"] == 0.5
assert metrics["precision"] == 0.5
assert metrics["recall"] == 0.5
assert metrics["f1_score"] == 0.5
"""
            ),
            TestCaseSchema(
                name="test_length_mismatch_error",
                description="Tests ValueError when input list lengths differ",
                test_code="""
try:
    evaluate_classification_metrics([1, 0], [1])
    assert False, "Expected ValueError"
except ValueError:
    pass
"""
            )
        ]
    ),
    LabTemplateSchema(
        id="python-data-viz-001",
        title="Data Distribution & Histogram Binning for Visual Analytics",
        skill="Data Visualization",
        language="python",
        difficulty="intermediate",
        lab_type="data_analysis",
        tags=["data-visualization", "visualization", "chart", "trend", "bins", "distribution", "summary", "open-data", "gis"],
        instructions_template="""### Objective
{objective}

### Task Instructions
1. Implement `{function_name}` to calculate frequency distributions for numerical survey indicators.
2. Given a list of numerical values and custom bin edges, compute the item count and percentage distribution for each bin.
3. Return the formatted summary ready for charting engines.
""",
        starter_code_template="""from typing import List, Dict, Any

def compute_histogram_bins(values: List[float], bin_edges: List[float]) -> List[Dict[str, Any]]:
    \"\"\"
    TODO: Given values and sorted bin_edges (e.g. [0, 50, 100]),
    compute counts for intervals [bin_edges[i], bin_edges[i+1]).
    For the last bin, include the right edge (inclusive).
    
    Return list of dicts:
    [{'bin': '0.0-50.0', 'count': int, 'percentage': float}]
    \"\"\"
    # Write your solution below:
    pass
""",
        solution_template="""from typing import List, Dict, Any

def compute_histogram_bins(values: List[float], bin_edges: List[float]) -> List[Dict[str, Any]]:
    if not values or len(bin_edges) < 2:
        return []
        
    total = len(values)
    bins = []
    
    for i in range(len(bin_edges) - 1):
        low = bin_edges[i]
        high = bin_edges[i+1]
        is_last = (i == len(bin_edges) - 2)
        
        if is_last:
            count = sum(1 for v in values if low <= v <= high)
        else:
            count = sum(1 for v in values if low <= v < high)
            
        pct = round((count / total) * 100.0, 2)
        bins.append({
            "bin": f"{low}-{high}",
            "count": count,
            "percentage": pct
        })
        
    return bins
""",
        constraints=[
            "Return empty list if values list is empty or bin_edges has fewer than 2 elements.",
            "Last bin interval must include the right edge value.",
            "Percentages must be rounded to 2 decimal places."
        ],
        test_cases_template=[
            TestCaseSchema(
                name="test_histogram_distribution",
                description="Tests standard bin count and percentage distribution",
                test_code="""
vals = [10.0, 25.0, 40.0, 60.0, 80.0, 100.0]
edges = [0.0, 50.0, 100.0]
res = compute_histogram_bins(vals, edges)
assert len(res) == 2
assert res[0]["bin"] == "0.0-50.0"
assert res[0]["count"] == 3
assert res[0]["percentage"] == 50.0
assert res[1]["bin"] == "50.0-100.0"
assert res[1]["count"] == 3
assert res[1]["percentage"] == 50.0
"""
            ),
            TestCaseSchema(
                name="test_empty_values_returns_empty",
                description="Tests empty inputs gracefully return empty list",
                test_code="""
assert compute_histogram_bins([], [0.0, 10.0]) == []
assert compute_histogram_bins([5.0], [0.0]) == []
"""
            )
        ]
    )
]


class TemplateService:
    """
    Service for managing, retrieving, and matching human-created Lab Templates.
    Enforces the human-controlled architecture: Humans define the constraints and test harnesses;
    the LLM fills the variable content within the template.
    """

    @classmethod
    def get_all_templates(cls, db: Optional[Session] = None) -> List[LabTemplateSchema]:
        """
        Retrieves all templates from DB and built-in catalogue.
        """
        templates_map: Dict[str, LabTemplateSchema] = {t.id: t for t in BUILTIN_LAB_TEMPLATES}

        if db is not None:
            db_templates = db.query(TechnicalLabTemplate).all()
            for dbt in db_templates:
                try:
                    tags = json.loads(dbt.tags_json) if dbt.tags_json else []
                    constraints = json.loads(dbt.constraints_json) if dbt.constraints_json else []
                    test_cases_raw = json.loads(dbt.test_cases_template_json) if dbt.test_cases_template_json else []
                    test_cases = [TestCaseSchema(**tc) for tc in test_cases_raw]
                    
                    templates_map[dbt.id] = LabTemplateSchema(
                        id=dbt.id,
                        title=dbt.title,
                        skill=dbt.skill,
                        language=dbt.language,
                        difficulty=dbt.difficulty,
                        lab_type=dbt.lab_type,
                        tags=tags,
                        instructions_template=dbt.instructions_template,
                        starter_code_template=dbt.starter_code_template,
                        solution_template=dbt.solution_template,
                        constraints=constraints,
                        test_cases_template=test_cases
                    )
                except Exception as e:
                    print(f"[TemplateService] Error parsing DB template {dbt.id}: {e}")

        return list(templates_map.values())

    @classmethod
    def get_template_by_id(cls, template_id: str, db: Optional[Session] = None) -> Optional[LabTemplateSchema]:
        templates = cls.get_all_templates(db=db)
        for t in templates:
            if t.id == template_id:
                return t
        return None

    @classmethod
    def match_template(
        cls,
        req: TemplateMatchRequest,
        db: Optional[Session] = None
    ) -> TemplateMatchResponse:
        """
        Matches a learning objective to the most appropriate human-created lab template.
        Operates primarily via metadata: skill, language, difficulty, lab_type, and tags.
        """
        templates = cls.get_all_templates(db=db)
        if not templates:
            return TemplateMatchResponse(
                matched=False,
                match_score=0.0,
                match_reason="No lab templates registered in repository."
            )

        best_template: Optional[LabTemplateSchema] = None
        best_score = -1.0
        match_details: List[str] = []

        target_skill = req.skill.lower().strip()
        target_obj = req.objective.lower()
        target_type = (req.lab_type or "").lower().strip()
        target_lang = (req.language or "python").lower().strip()

        for t in templates:
            score = 0.0
            reasons = []

            # 1. Language compatibility check
            if t.language.lower() == target_lang:
                score += 20.0
                reasons.append(f"Language match ({t.language})")
            else:
                continue  # Incompatible programming language

            # 2. Skill & Tag matching
            template_skill = t.skill.lower()
            if template_skill in target_skill or target_skill in template_skill or target_skill in target_obj:
                score += 40.0
                reasons.append(f"Skill alignment ({t.skill})")
            
            matched_tags = [tag for tag in t.tags if tag.lower() in target_obj or tag.lower() in target_skill]
            if matched_tags:
                score += min(len(matched_tags) * 10.0, 30.0)
                reasons.append(f"Matching tags: {', '.join(matched_tags)}")

            # 3. Lab type matching
            if target_type and t.lab_type.lower() == target_type:
                score += 15.0
                reasons.append(f"Lab type match ({t.lab_type})")
            elif not target_type:
                score += 5.0

            # 4. Difficulty alignment
            if t.difficulty.lower() == (req.difficulty or "intermediate").lower():
                score += 10.0
                reasons.append(f"Difficulty match ({t.difficulty})")

            if score > best_score:
                best_score = score
                best_template = t
                match_details = reasons

        if best_template and best_score >= 30.0:
            normalized_score = min(1.0, round(best_score / 100.0, 2))
            return TemplateMatchResponse(
                matched=True,
                template=best_template,
                match_score=normalized_score,
                match_reason=f"Matched template '{best_template.id}' with score {normalized_score}: {'; '.join(match_details)}"
            )

        # Fallback to default Python implementation template if one exists
        default_template = next((t for t in templates if t.language.lower() == target_lang), templates[0])
        return TemplateMatchResponse(
            matched=True,
            template=default_template,
            match_score=0.40,
            match_reason=f"Default general technical template '{default_template.id}' selected (low specific keyword overlap)."
        )
