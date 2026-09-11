from typing import List, Optional
from pydantic import BaseModel, Field

class SkillSchema(BaseModel):
    id: str
    name: str
    description: str
    difficulty: List[str]
    prerequisites: List[str] = Field(default_factory=list)
    question_types: List[str]
    formula: Optional[str] = None
    mastery_threshold: float = 75.0

class CompetencySchema(BaseModel):
    id: str
    domain: str
    name: str
    description: str
    authority: Optional[str] = None
    standard: Optional[str] = None
    skills: List[SkillSchema]

class LearnerSkillMasterySchema(BaseModel):
    skill_id: str
    score: float = Field(ge=0.0, le=100.0)
    level: str = "novice" # novice, basic, intermediate, advanced, master
    confidence: float = 0.5
    attempts_count: int = 0
    correct_count: int = 0
    remediation_recommended: bool = False
    last_attempt_at: Optional[str] = None
