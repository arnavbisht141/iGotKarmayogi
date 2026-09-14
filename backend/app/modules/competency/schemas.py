from typing import List, Optional
from pydantic import BaseModel


class DomainGapSchema(BaseModel):
    domain_code: str
    domain_name: str
    target_level: float
    current_level: float
    gap: float
    generated_at: str

    class Config:
        from_attributes = True


class CompetencyProfileSchema(BaseModel):
    statistical_score: float
    technical_score: float
    digital_governance_score: float
    behavioural_score: float
    last_computed_at: Optional[str] = None
    is_default_framework: bool = True

    class Config:
        from_attributes = True


class GapAnalysisResponse(BaseModel):
    profile: CompetencyProfileSchema
    gaps: List[DomainGapSchema]
