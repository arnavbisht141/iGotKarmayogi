from abc import ABC, abstractmethod
from typing import Any, Dict
from app.statistical_engine.schemas.stats import CalculationResult

class BaseStatisticalModule(ABC):
    """Abstract base class for domain-specific statistical modules."""
    
    @abstractmethod
    def calculate(self, operation: str, inputs: Dict[str, Any]) -> CalculationResult:
        """Execute a deterministic statistical computation with input validation."""
        pass
