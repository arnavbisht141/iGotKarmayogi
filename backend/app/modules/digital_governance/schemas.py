from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ScenarioOption(BaseModel):
    option_id: str
    text: str
    is_optimal: bool
    is_terminal: bool = False
    consequence_summary: str
    statutory_rationale: str
    next_question_id: Optional[str] = None
    compliance_delta: int = 20

class ScenarioQuestion(BaseModel):
    id: str
    scenario_id: str
    stage_title: str
    prompt: str
    context_update: Optional[str] = None
    options: List[ScenarioOption]
    governance_pillar: str

class CaseScenario(BaseModel):
    id: str
    title: str
    domain: str  # Cybersecurity, Data Privacy, Digital Signatures, Government Cloud, Digital Public Infrastructure
    ministry: str
    statutory_framework: List[str]
    difficulty: str = "intermediate"
    estimated_minutes: int = 15
    initial_context: str
    root_question_id: str
    questions: Dict[str, ScenarioQuestion]
    learning_objectives: List[str]

class ScenarioListItem(BaseModel):
    id: str
    title: str
    domain: str
    ministry: str
    statutory_framework: List[str]
    difficulty: str
    estimated_minutes: int
    summary: str
    objectives_count: int

class ScenarioSessionStartRequest(BaseModel):
    scenario_id: Optional[str] = None

class ScenarioSessionResponse(BaseModel):
    session_id: str
    scenario_id: str
    scenario_title: str
    domain: str
    ministry: str
    initial_context: str
    statutory_framework: List[str]
    current_question: ScenarioQuestion
    compliance_score: int
    step_number: int

class ScenarioAnswerRequest(BaseModel):
    option_id: str

class DecisionNodeLog(BaseModel):
    step: int
    stage_title: str
    question_prompt: str
    selected_option_id: str
    selected_option_text: str
    is_optimal: bool
    consequence_summary: str
    statutory_rationale: str
    score_after_decision: int

class ScenarioSummary(BaseModel):
    session_id: str
    scenario_id: str
    scenario_title: str
    domain: str
    ministry: str
    total_steps: int
    optimal_steps: int
    procedural_compliance_score: int
    resolved_satisfactorily: bool
    decision_trail: List[DecisionNodeLog]
    key_regulatory_takeaways: List[str]

class ScenarioAnswerResponse(BaseModel):
    session_id: str
    is_terminal: bool
    selected_option: ScenarioOption
    next_question: Optional[ScenarioQuestion] = None
    compliance_score: int
    step_number: int
    session_summary: Optional[ScenarioSummary] = None
