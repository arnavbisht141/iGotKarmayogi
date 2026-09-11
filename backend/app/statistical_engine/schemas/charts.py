from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ChartAxis(BaseModel):
    field: str
    label: str

class ChartSpec(BaseModel):
    type: str = Field(..., description="Chart type: bar, line, pie, scatter")
    title: str
    description: Optional[str] = None
    xAxis: ChartAxis
    yAxis: ChartAxis
    data: List[Dict[str, Any]]
    unit: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChartGenerateRequest(BaseModel):
    type: str
    title: str
    description: Optional[str] = None
    xAxis: ChartAxis
    yAxis: ChartAxis
    data: List[Dict[str, Any]]
    unit: Optional[str] = None
