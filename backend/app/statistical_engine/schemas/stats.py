from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

class CalculationRequest(BaseModel):
    operation: str = Field(..., description="Name of statistical operation (e.g., price_relative, inflation_rate, laspeyres_index)")
    inputs: Dict[str, Any] = Field(..., description="Validated parameters required for calculation")

class CalculationResult(BaseModel):
    operation: str
    result: Union[float, int, str]
    unit: str
    formula: str
    steps: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
