import os
from pathlib import Path
from pydantic_settings import BaseSettings

class EngineSettings(BaseSettings):
    ENGINE_NAME: str = "iGOT Karmayogi Statistical Competency Engine"
    API_VERSION: str = "v1"
    
    # Path configuration
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    CONTENT_DIR: Path = BASE_DIR / "content"
    COMPETENCIES_DIR: Path = CONTENT_DIR / "competencies"
    QUESTIONS_DIR: Path = CONTENT_DIR / "questions"
    
    # Numerical validation defaults
    DEFAULT_NUMERIC_TOLERANCE: float = 0.5
    DEFAULT_MAX_ATTEMPTS: int = 3
    DEFAULT_MASTERY_INCREMENT: float = 10.0
    DEFAULT_MASTERY_DECREMENT: float = 5.0
    PROMOTION_THRESHOLD: float = 80.0
    REMEDIATION_THRESHOLD: float = 50.0

    class Config:
        case_sensitive = True

engine_settings = EngineSettings()
