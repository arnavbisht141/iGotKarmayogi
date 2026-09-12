from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# --- Government Document Corpus Schemas ---

class GovernmentDocument(BaseModel):
    id: str
    title: str
    document_type: str = Field(description="Notice | Statutory Form | Departmental Proceeding")
    issuing_authority: str
    document_number: str
    statutory_reference: str
    date_of_issue: str
    full_text: str
    key_stakeholders: List[str]
    procedural_clauses: List[str]

# --- Carryforward Branching MCQ Schemas ---

class CarryforwardOption(BaseModel):
    option_id: str
    text: str
    is_optimal: bool
    is_satisfactory_terminal: bool = Field(
        default=False,
        description="True if this choice satisfactorily resolves the scenario and concludes this case thread"
    )
    consequence_summary: str
    statutory_rationale: str
    next_question_id: Optional[str] = Field(
        default=None,
        description="ID of the consequential follow-up question if this option triggers a carryforward branch"
    )

class CarryforwardQuestion(BaseModel):
    id: str
    case_id: str
    stage_type: str = Field(description="'root' or 'carryforward_branch'")
    prompt: str
    context_update: Optional[str] = Field(
        default=None,
        description="Updates or procedural escalations that led to this question"
    )
    options: List[CarryforwardOption]
    behavioral_competencies: List[str] = Field(default_factory=list)

class CaseScenario(BaseModel):
    id: str
    title: str
    category: str
    course_id: Optional[int] = Field(default=None, description="ID of the related database course")
    course_title: Optional[str] = Field(default=None, description="Title of the related database course")
    course_organization: Optional[str] = Field(default=None, description="Issuing organization of course")
    document_id: str
    document_title: str
    document_type: str
    statutory_citations: List[str]
    initial_context: str
    root_question_id: str
    questions: Dict[str, CarryforwardQuestion]
    learning_objectives: List[str]

class CourseCaseOverview(BaseModel):
    course_id: int
    title: str
    organization: str
    category: str
    overview: str
    mapped_notices: List[str] = Field(default_factory=list)
    case_count: int = 0

class GenerateCaseForCourseRequest(BaseModel):
    course_id: int
    document_id: Optional[str] = None
    custom_notice_text: Optional[str] = None
    focus_topic: Optional[str] = None

# --- Interactive Carryforward Session Schemas ---

class CarryforwardSessionStartRequest(BaseModel):
    case_id: Optional[str] = None
    custom_document_id: Optional[str] = None

class CarryforwardAnswerRequest(BaseModel):
    question_id: str
    selected_option_id: str

class DecisionNodeLog(BaseModel):
    question_id: str
    stage_type: str
    question_prompt: str
    selected_option_id: str
    selected_option_text: str
    is_optimal: bool
    is_satisfactory_terminal: bool
    consequence_summary: str
    statutory_rationale: str

class CarryforwardAnswerResponse(BaseModel):
    is_optimal: bool
    is_satisfactory_terminal: bool
    consequence_summary: str
    statutory_rationale: str
    carryforward_active: bool
    scenario_completed: bool
    session_completed: bool
    current_score: float
    total_steps_taken: int
    next_question: Optional[CarryforwardQuestion] = None
    next_case_id: Optional[str] = None

class CarryforwardSessionSummary(BaseModel):
    session_id: str
    case_id: str
    case_title: str
    document_title: str
    document_type: str
    total_steps: int
    optimal_steps: int
    procedural_compliance_score: float
    resolved_satisfactorily: bool
    decision_trail: List[DecisionNodeLog]
    key_takeaways: List[str]

# --- Dynamic Generation from Government Document ---

class CaseGenerationRequest(BaseModel):
    raw_text: str
    document_title: str
    document_type: str = "Government Notice"
    issuing_authority: str = "Department of Personnel & Training (DoPT)"
    statutory_reference: str = "CCS (Conduct) Rules / GFR 2017"

# --- AI Live Feed Interview Schemas ---

class InterviewStartRequest(BaseModel):
    course_id: int
    officer_name: Optional[str] = "Officer"
    target_duration_minutes: int = Field(default=30, ge=25, le=35)

class InterviewTurnRequest(BaseModel):
    session_id: str
    officer_response: str
    elapsed_seconds: int


class InterviewEndRequest(BaseModel):
    session_id: str

class InterviewTurnResponse(BaseModel):
    turn_number: int
    ai_question: str
    phase_name: str
    phase_target_competency: str
    elapsed_seconds: int
    target_duration_minutes: int
    turns_completed: int
    is_final_turn: bool
    pacing_advice: Optional[str] = None
    acknowledgement_note: Optional[str] = None

class CompetencyScore(BaseModel):
    competency_name: str
    score_percent: float
    rating_band: str  # "Exemplary", "Proficient", "Needs Attention"
    key_evidence: str
    growth_opportunity: str

class TranscriptEntry(BaseModel):
    speaker: str  # "AI Interviewer" or "Officer"
    content: str
    timestamp_seconds: int
    behavioral_tags: List[str] = Field(default_factory=list)

class InterviewAnalysisResponse(BaseModel):
    session_id: str
    course_id: int
    course_title: str
    officer_name: str
    total_duration_formatted: str
    total_turns: int
    overall_score_percent: float
    overall_rating_band: str
    executive_summary: str
    competency_scores: Dict[str, CompetencyScore]
    core_strengths: List[str]
    priority_development_areas: List[str]
    recommended_apar_actions: List[str]
    transcript: List[TranscriptEntry]
