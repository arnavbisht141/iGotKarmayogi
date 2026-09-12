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


# ==========================================
# Cybersecurity Sandbox & CTF Pipeline Schemas
# ==========================================

class SandboxChallengeSummary(BaseModel):
    id: str
    title: str
    category: str
    difficulty: str
    points: int
    duration_minutes: int
    is_flagship: bool = False
    solved: bool = False
    competency_id: str
    tags: List[str] = []
    mitre_techniques: List[str] = []
    objectives: List[str] = []


class SandboxGenerateRequest(BaseModel):
    transcript_text: str
    student_id: Optional[str] = "nodal_officer_01"


class SandboxGenerateResponse(BaseModel):
    challenge_id: str
    title: str
    category: str
    difficulty: str
    points: int
    objectives: List[str]
    scenario_md: str
    extracted_meta: Dict[str, Any]


class SandboxStartRequest(BaseModel):
    challenge_id: str
    duration_minutes: Optional[int] = 45


class SandboxSessionResponse(BaseModel):
    session_id: str
    challenge_id: str
    title: str
    category: str
    difficulty: str
    points: int
    expires_at: str
    remaining_seconds: int
    status: str
    assigned_port: int
    marimo_url: str
    hints: List[Dict[str, Any]]
    scenario_md: str
    objectives: List[str]
    solved: bool = False


class SandboxFlagSubmitRequest(BaseModel):
    session_id: str
    flag: str


class SandboxFlagSubmitResponse(BaseModel):
    correct: bool
    message: str
    points_awarded: int
    competency_id: str
    competency_score: int


class SandboxHintUnlockRequest(BaseModel):
    session_id: str
    hint_id: int


class SandboxHintUnlockResponse(BaseModel):
    hint_id: int
    content: str
    penalty: int
    remaining_points: int


class UserCompetencyRadar(BaseModel):
    soc_investigation: int = 0
    phishing_analysis: int = 0
    cloud_security: int = 0
    dpi_security: int = 0
    digital_forensics: int = 0
    total_score: int = 0
    solved_challenges_count: int = 0


class TopicGenerateRequest(BaseModel):
    topic_name: str
    student_id: Optional[str] = "officer_1"


