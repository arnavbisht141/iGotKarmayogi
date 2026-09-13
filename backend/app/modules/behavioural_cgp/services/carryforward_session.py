import uuid
from typing import Dict, Optional, List
from ..schemas import (
    CaseScenario,
    CarryforwardQuestion,
    CarryforwardOption,
    DecisionNodeLog,
    CarryforwardAnswerResponse,
    CarryforwardSessionSummary
)
from .carryforward_generator import get_case_by_id, get_all_cases

class CarryforwardSession:
    def __init__(self, session_id: str, case_scenarios: List[CaseScenario]):
        self.session_id = session_id
        self.case_scenarios = case_scenarios
        self.current_case_index = 0
        self.current_question_id: str = case_scenarios[0].root_question_id
        self.decision_trail: List[DecisionNodeLog] = []
        self.total_steps = 0
        self.optimal_steps = 0
        self.session_completed = False

    @property
    def current_case(self) -> Optional[CaseScenario]:
        if self.current_case_index < len(self.case_scenarios):
            return self.case_scenarios[self.current_case_index]
        return None

    @property
    def current_question(self) -> Optional[CarryforwardQuestion]:
        case = self.current_case
        if not case:
            return None
        return case.questions.get(self.current_question_id)

    def submit_answer(self, question_id: str, selected_option_id: str) -> CarryforwardAnswerResponse:
        case = self.current_case
        if not case:
            raise ValueError("No active case scenario in this session")

        question = case.questions.get(question_id)
        if not question:
            raise ValueError(f"Question '{question_id}' not found in current case")

        selected_opt: Optional[CarryforwardOption] = None
        for opt in question.options:
            if opt.option_id.upper() == selected_option_id.upper():
                selected_opt = opt
                break

        if not selected_opt:
            raise ValueError(f"Option '{selected_option_id}' not found for question '{question_id}'")

        self.total_steps += 1
        if selected_opt.is_optimal:
            self.optimal_steps += 1

        # Record decision node
        node_log = DecisionNodeLog(
            question_id=question.id,
            stage_type=question.stage_type,
            question_prompt=question.prompt,
            selected_option_id=selected_opt.option_id,
            selected_option_text=selected_opt.text,
            is_optimal=selected_opt.is_optimal,
            is_satisfactory_terminal=selected_opt.is_satisfactory_terminal,
            consequence_summary=selected_opt.consequence_summary,
            statutory_rationale=selected_opt.statutory_rationale
        )
        self.decision_trail.append(node_log)

        # Carryforward logic
        carryforward_active = False
        scenario_completed = False
        next_question: Optional[CarryforwardQuestion] = None
        next_case_id: Optional[str] = None

        if selected_opt.is_satisfactory_terminal:
            # Current case scenario is satisfactorily answered!
            scenario_completed = True
            self.current_case_index += 1

            if self.current_case_index < len(self.case_scenarios):
                # Advance to next case scenario!
                next_case = self.case_scenarios[self.current_case_index]
                self.current_question_id = next_case.root_question_id
                next_question = next_case.questions.get(self.current_question_id)
                next_case_id = next_case.id
            else:
                self.session_completed = True
                self.current_question_id = None
        else:
            # Carryforward to consequential follow-up branch
            if selected_opt.next_question_id and selected_opt.next_question_id in case.questions:
                carryforward_active = True
                self.current_question_id = selected_opt.next_question_id
                next_question = case.questions[self.current_question_id]
            else:
                # Terminal fallback if branch wasn't specified
                scenario_completed = True
                self.current_case_index += 1
                if self.current_case_index < len(self.case_scenarios):
                    next_case = self.case_scenarios[self.current_case_index]
                    self.current_question_id = next_case.root_question_id
                    next_question = next_case.questions.get(self.current_question_id)
                    next_case_id = next_case.id
                else:
                    self.session_completed = True
                    self.current_question_id = None

        current_score = round((self.optimal_steps / max(1, self.total_steps)) * 100, 1)

        return CarryforwardAnswerResponse(
            is_optimal=selected_opt.is_optimal,
            is_satisfactory_terminal=selected_opt.is_satisfactory_terminal,
            consequence_summary=selected_opt.consequence_summary,
            statutory_rationale=selected_opt.statutory_rationale,
            carryforward_active=carryforward_active,
            scenario_completed=scenario_completed,
            session_completed=self.session_completed,
            current_score=current_score,
            total_steps_taken=self.total_steps,
            next_question=next_question,
            next_case_id=next_case_id
        )

    def get_summary(self) -> CarryforwardSessionSummary:
        resolved_index = min(self.current_case_index, max(0, len(self.case_scenarios) - 1))
        if self.session_completed and self.decision_trail:
            last_qid = self.decision_trail[-1].question_id
            case = next(
                (c for c in self.case_scenarios if last_qid in c.questions),
                self.case_scenarios[resolved_index] if self.case_scenarios else None,
            )
        else:
            case = self.case_scenarios[resolved_index] if self.case_scenarios else None
        compliance_score = round((self.optimal_steps / max(1, self.total_steps)) * 100, 1) if self.total_steps else 0.0
        
        # Competency Evaluation across 6 key civil service dimensions
        opt_ratio = (self.optimal_steps / max(1, self.total_steps)) if self.total_steps else 0.0
        
        comp_scores: Dict[str, float] = {
            "Decision Making": round(min(98.0, max(50.0, 65.0 + opt_ratio * 30.0)), 1),
            "Ethical Judgement": round(min(98.0, max(55.0, 70.0 + opt_ratio * 25.0)), 1),
            "Leadership": round(min(95.0, max(50.0, 60.0 + opt_ratio * 32.0)), 1),
            "Communication": round(min(96.0, max(55.0, 68.0 + opt_ratio * 26.0)), 1),
            "Situational Awareness": round(min(98.0, max(45.0, 58.0 + opt_ratio * 36.0)), 1),
            "Accountability": round(min(97.0, max(52.0, 64.0 + opt_ratio * 31.0)), 1)
        }

        from ..schemas import CarryforwardCompetencyResult
        comp_results: List[CarryforwardCompetencyResult] = []
        for comp_name, score in comp_scores.items():
            if score >= 85.0:
                lvl = "Exemplary"
                desc = f"Displays superior executive proficiency and constitutional compliance in {comp_name.lower()}."
            elif score >= 72.0:
                lvl = "Proficient"
                desc = f"Demonstrates solid working grasp of {comp_name.lower()}; minor refinement in complex escalations recommended."
            else:
                lvl = "Needs Attention"
                desc = f"Shows vulnerability to procedural errors; targeted upskilling in {comp_name.lower()} required."
            comp_results.append(CarryforwardCompetencyResult(
                competency=comp_name,
                score=score,
                level=lvl,
                description=desc
            ))

        strengths = []
        weaknesses = []
        upskilling = []

        if opt_ratio >= 0.75:
            strengths.append("High degree of procedural compliance and adherence to Audi Alteram Partem.")
            strengths.append("Decisive handling of statutory notices without compromising due process.")
            strengths.append("Protected administrative orders from judicial/tribunal invalidation.")
        else:
            strengths.append("Recognized operational deadlines and administrative imperatives.")
            strengths.append("Engaged actively with complex multi-stage procedural scenarios.")

        if opt_ratio < 1.0:
            weaknesses.append("Initial choices triggered procedural complications or carryforward consequence branches.")
            weaknesses.append("Vulnerability to administrative challenges before Central Administrative Tribunal (CAT) or vigilance scrutiny.")
        else:
            weaknesses.append("Continue maintaining consistency across unlisted edge cases and multi-jurisdictional inquiries.")

        c_title = case.course_title if case and case.course_title else "Official Cadre Training"
        upskilling.append(f"Targeted Refresher: Procedural Law & Due Process in '{c_title}'")
        upskilling.append("Executive Workshop: Quasi-Judicial Decision Making and Natural Justice Compliance")
        upskilling.append("Simulation Lab: Drafting Reasoned Speaking Orders under Statutory Frameworks")

        takeaways = [
            "Always verify statutory notice periods before issuing adverse debarment or penalty orders.",
            "Ensure complete documentation and opportunity of inspection under Audi Alteram Partem."
        ]
        if compliance_score >= 80:
            takeaways.insert(0, "Exceptional adherence to statutory civil service rules and principles of natural justice.")
        elif compliance_score >= 60:
            takeaways.insert(0, "Proficient procedural knowledge; minor remediation required in initial interlocutory orders.")
        else:
            takeaways.insert(0, "Multiple administrative lapses committed leading to unnecessary litigation and vigilance risks.")

        return CarryforwardSessionSummary(
            session_id=self.session_id,
            case_id=case.id if case else "general",
            case_title=case.title if case else "Civil Service Case Assessment",
            document_title=case.document_title if case else "Government Notice",
            document_type=case.document_type if case else "Notice",
            total_steps=self.total_steps,
            optimal_steps=self.optimal_steps,
            procedural_compliance_score=compliance_score,
            resolved_satisfactorily=self.session_completed or any(d.is_satisfactory_terminal for d in self.decision_trail),
            decision_trail=self.decision_trail,
            competency_scores=comp_scores,
            competency_results=comp_results,
            strengths=strengths,
            weaknesses=weaknesses,
            recommended_upskilling=upskilling,
            key_takeaways=takeaways
        )


class CarryforwardSessionManager:
    """Manages active in-memory sessions."""
    _sessions: Dict[str, CarryforwardSession] = {}

    @classmethod
    def create_session(cls, case_id: Optional[str] = None, custom_case: Optional[CaseScenario] = None) -> CarryforwardSession:
        session_id = f"cf_sess_{uuid.uuid4().hex[:12]}"
        
        scenarios: List[CaseScenario] = []
        if custom_case:
            scenarios = [custom_case]
        elif case_id:
            case = get_case_by_id(case_id)
            if case:
                scenarios = [case]
            else:
                scenarios = get_all_cases()
        else:
            scenarios = get_all_cases()

        session = CarryforwardSession(session_id=session_id, case_scenarios=scenarios)
        cls._sessions[session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[CarryforwardSession]:
        return cls._sessions.get(session_id)
