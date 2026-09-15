import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.statistical_engine.config import engine_settings
from app.statistical_engine.core.exceptions import CompetencyNotFoundException
from app.statistical_engine.schemas.competencies import CompetencySchema, SkillSchema

class CompetencyGraph:
    """
    Manages competency structures, skills hierarchies, and prerequisite dependency graphs.
    """

    def __init__(self):
        self._competencies: Dict[str, Dict[str, Any]] = {}
        self._skills_map: Dict[str, Dict[str, Any]] = {}
        self._load_competencies()

    def _load_competencies(self):
        comp_dir = engine_settings.COMPETENCIES_DIR
        if not comp_dir.exists():
            return

        for filepath in comp_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    c_id = data["id"]
                    self._competencies[c_id] = data
                    for s in data.get("skills", []):
                        self._skills_map[s["id"]] = s
            except Exception as e:
                print(f"[WARN] Failed to load competency file {filepath}: {e}")

    def get_competency(self, competency_id: str) -> Dict[str, Any]:
        if competency_id not in self._competencies:
            raise CompetencyNotFoundException(competency_id)
        return self._competencies[competency_id]

    def list_competencies(self) -> List[Dict[str, Any]]:
        return list(self._competencies.values())

    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        return self._skills_map.get(skill_id)

    def get_prerequisites(self, skill_id: str) -> List[str]:
        skill = self.get_skill(skill_id)
        return skill.get("prerequisites", []) if skill else []

    def are_prerequisites_met(
        self,
        skill_id: str,
        learner_mastery: Dict[str, Dict[str, Any]],
        threshold: float = 70.0
    ) -> bool:
        prereqs = self.get_prerequisites(skill_id)
        for p in prereqs:
            m = learner_mastery.get(p, {})
            if m.get("score", 0.0) < threshold:
                return False
        return True

competency_graph = CompetencyGraph()
