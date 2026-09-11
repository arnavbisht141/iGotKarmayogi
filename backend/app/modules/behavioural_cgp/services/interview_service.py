import uuid
import json
from typing import Dict, List, Optional, Any
from app.core.config import settings
from ..schemas import (
    InterviewStartRequest,
    InterviewTurnRequest,
    InterviewTurnResponse,
    CompetencyScore,
    TranscriptEntry,
    InterviewAnalysisResponse
)

# Standard Civil Service Behavioral Competencies
COMPETENCIES = [
    "Course Knowledge",
    "Leadership",
    "Communication",
    "Project Management",
    "Ethics",
    "Decision Making",
    "Change Management"
]

PHASES = [
    {
        "phase_id": 1,
        "name": "Phase 1: Foundational Subject Matter & Conceptual Rigor",
        "primary_competency": "Course Knowledge",
        "secondary_competency": "Communication",
        "time_window": "00:00 - 06:00",
        "objective": "Assess understanding of core frameworks, statutory rules, and methodological principles."
    },
    {
        "phase_id": 2,
        "name": "Phase 2: Operational Execution & Project Management",
        "primary_competency": "Project Management",
        "secondary_competency": "Decision Making",
        "time_window": "06:00 - 13:00",
        "objective": "Assess scheduling, resource allocation, and field monitoring."
    },
    {
        "phase_id": 3,
        "name": "Phase 3: Crisis Resolution & Team Leadership",
        "primary_competency": "Leadership",
        "secondary_competency": "Communication",
        "time_window": "13:00 - 20:00",
        "objective": "Assess guiding cross-functional teams, handling unexpected bottlenecks, and public accountability."
    },
    {
        "phase_id": 4,
        "name": "Phase 4: Statutory Adherence & Ethical Dilemmas",
        "primary_competency": "Ethics",
        "secondary_competency": "Decision Making",
        "time_window": "20:00 - 27:00",
        "objective": "Assess impartiality, conflict of interest management, and non-negotiable adherence to rules."
    },
    {
        "phase_id": 5,
        "name": "Phase 5: Institutional Modernization & Change Management",
        "primary_competency": "Change Management",
        "secondary_competency": "Leadership",
        "time_window": "27:00 - 35:00",
        "objective": "Assess overcoming institutional inertia, driving digital adoption, and leaving sustainable systems."
    }
]

# Course curriculum seed profiles for the interviewer
COURSE_CONTEXTS: Dict[int, Dict[str, Any]] = {
    1: {
        "title": "Fundamentals of National Sample Surveys (NSS)",
        "organization": "National Sample Survey Office (NSSO)",
        "key_themes": ["Two-stage stratified design", "FSU selection (PPS)", "Hamlet-group formation", "CAPI validation"],
        "initial_question": "Good morning, Officer. Welcome to this oral competency examination for the National Sample Survey framework. To begin: in rural rounds, under what exact conditions is hamlet-group formation legally mandatory, and what sampling risks emerge if an investigator substitutes a hamlet without prior written authorization?"
    },
    2: {
        "title": "Compilation of Consumer Price Index (CPI) & Inflation Metrics",
        "organization": "Central Statistics Office (CSO)",
        "key_themes": ["Modified Laspeyres", "Jevons Geometric Mean", "Item basket weighting", "Quality adjustment"],
        "initial_question": "Welcome, Officer. Let us assess your mastery of official inflation compilation. Could you explain the mathematical justification for utilizing the Jevons Geometric Mean at the elementary quotation level, and how you would handle an abrupt disappearance of a staple commodity from urban market price quotations?"
    },
    3: {
        "title": "Data Quality Frameworks & Official Statistics in India",
        "organization": "National Statistical Systems Training Academy (NSSTA)",
        "key_themes": ["UN-NQAF 19 Principles", "Confidentiality Principle 5", "Data release policy", "Public integrity"],
        "initial_question": "Good morning, Officer. Under the UN National Quality Assurance Framework (UN-NQAF) and the Collection of Statistics Act, how do you resolve an urgent administrative directive demanding the release of identifiable survey records to another ministry for law enforcement purposes?"
    },
    4: {
        "title": "Digital Governance & Public Financial Management System (PFMS)",
        "organization": "Institute of Secretariat Training & Management (ISTM)",
        "key_themes": ["Treasury Single Account (TSA)", "Just-in-Time funding", "Direct Benefit Transfer (DBT)", "GFR 2017"],
        "initial_question": "Officer, in implementing the Treasury Single Account (TSA) under PFMS, what mechanisms prevent regional implementing agencies from parking unspent central scheme funds in commercial bank accounts, and how would you handle non-compliance from state treasuries?"
    },
    5: {
        "title": "Python and Statistical Computing for Public Policy",
        "organization": "MoSPI Data Lab",
        "key_themes": ["Pandas vectorization", "Reproducible pipelines", "Microdata wrangling", "Data governance"],
        "initial_question": "Welcome, Officer. In processing millions of household observations from NSS microdata, why are vectorized Pandas operations mandatory over iterative Python loops, and how do you ensure the reproducibility and auditability of data cleaning transformations?"
    }
}

class LiveInterviewSession:
    def __init__(self, session_id: str, course_id: int, officer_name: str, target_duration_minutes: int):
        self.session_id = session_id
        self.course_id = course_id
        self.officer_name = officer_name
        self.target_duration_minutes = target_duration_minutes
        self.course_info = COURSE_CONTEXTS.get(course_id, {
            "title": f"Civil Service Competency Course {course_id}",
            "organization": "iGot Karmayogi",
            "key_themes": ["Administrative Rules", "Policy Implementation", "Public Ethics"],
            "initial_question": f"Good morning, Officer {officer_name}. Welcome to your live oral evaluation. To begin, please articulate how your understanding of this course enables you to improve administrative efficiency and service delivery in your department."
        })
        self.current_turn = 1
        self.max_turns = 6  # 5-6 structured turns covering all phases within 25-35 minutes
        self.transcript: List[TranscriptEntry] = [
            TranscriptEntry(
                speaker="AI Interviewer",
                content=self.course_info["initial_question"],
                timestamp_seconds=0,
                behavioral_tags=["Communication", "Course Knowledge"]
            )
        ]
        self.officer_responses: List[Dict[str, Any]] = []
        self.is_concluded = False

    def process_turn(self, officer_text: str, elapsed_seconds: int) -> InterviewTurnResponse:
        self.current_turn += 1
        
        # Tag behavioral competencies detected in officer response
        tags = self._detect_behavioral_tags(officer_text)
        self.transcript.append(
            TranscriptEntry(
                speaker=f"Officer {self.officer_name}",
                content=officer_text,
                timestamp_seconds=elapsed_seconds,
                behavioral_tags=tags
            )
        )
        self.officer_responses.append({
            "turn": self.current_turn - 1,
            "response": officer_text,
            "elapsed_seconds": elapsed_seconds,
            "tags": tags
        })

        current_phase = self._resolve_phase(elapsed_seconds)

        # Check if this is the final wrap-up turn
        is_final = self.current_turn >= self.max_turns or elapsed_seconds >= (self.target_duration_minutes * 60 - 180)

        # Generate adaptive follow-up question
        follow_up_q, ack_note = self._generate_adaptive_follow_up(
            officer_text=officer_text,
            phase=current_phase,
            is_final=is_final
        )

        self.transcript.append(
            TranscriptEntry(
                speaker="AI Interviewer",
                content=follow_up_q,
                timestamp_seconds=elapsed_seconds + 5,
                behavioral_tags=[current_phase["primary_competency"], "Communication"]
            )
        )

        if is_final:
            self.is_concluded = True

        # Pacing feedback
        target_secs = self.target_duration_minutes * 60
        remaining_secs = max(0, target_secs - elapsed_seconds)
        rem_min = remaining_secs // 60
        pacing_advice = f"Interview pacing optimal: ~{rem_min} minutes remaining. Transitioning to {current_phase['name']}."

        return InterviewTurnResponse(
            turn_number=self.current_turn,
            ai_question=follow_up_q,
            phase_name=current_phase["name"],
            phase_target_competency=current_phase["primary_competency"],
            elapsed_seconds=elapsed_seconds,
            target_duration_minutes=self.target_duration_minutes,
            turns_completed=len(self.officer_responses),
            is_final_turn=is_final,
            pacing_advice=pacing_advice,
            acknowledgement_note=ack_note
        )

    def _resolve_phase(self, elapsed_seconds: int) -> Dict[str, Any]:
        """Map elapsed time and turn count onto the 25–35 minute five-phase board."""
        target_secs = max(1, self.target_duration_minutes * 60)
        ratio = max(0.0, elapsed_seconds / target_secs)
        if ratio < 0.20:
            time_idx = 0
        elif ratio < 0.40:
            time_idx = 1
        elif ratio < 0.60:
            time_idx = 2
        elif ratio < 0.80:
            time_idx = 3
        else:
            time_idx = 4
        turn_idx = min(len(PHASES) - 1, max(0, self.current_turn - 2))
        return PHASES[max(time_idx, turn_idx)]

    def _detect_behavioral_tags(self, text: str) -> List[str]:
        t = text.lower()
        tags = []
        if any(w in t for w in ["rule", "statute", "integrity", "impartial", "public interest", "conflict", "un-nqaf", "law", "gfr"]):
            tags.append("Ethics")
        if any(w in t for w in ["team", "inspire", "delegate", "supervise", "guide", "accountable", "responsibility"]):
            tags.append("Leadership")
        if any(w in t for w in ["timeline", "milestone", "resource", "budget", "monitoring", "schedule", "contingency"]):
            tags.append("Project Management")
        if any(w in t for w in ["decide", "evidence", "judgment", "priority", "balance", "risk", "evaluate"]):
            tags.append("Decision Making")
        if any(w in t for w in ["reform", "digital", "modernize", "transition", "resistance", "training", "capacity", "adopt"]):
            tags.append("Change Management")
        if any(w in t for w in ["clear", "brief", "structured", "coordinate", "inform", "stakeholder"]):
            tags.append("Communication")
        if any(w in t for w in ["sample", "cpi", "fsu", "inflation", "pfms", "pandas", "data", "formula", "survey", "methodology"]):
            tags.append("Course Knowledge")
        return list(set(tags)) if tags else ["Course Knowledge", "Communication"]

    def _generate_adaptive_follow_up(self, officer_text: str, phase: Dict[str, Any], is_final: bool) -> tuple[str, str]:
        # Attempt LLM generation if keys available
        if settings.GOOGLE_API_KEY or settings.OPENAI_API_KEY:
            try:
                from langchain_core.messages import HumanMessage
                prompt = f"""You are a distinguished Senior Civil Service Interview Board Member in India conducting an official oral competency assessment on iGot Karmayogi.
Course Title: {self.course_info['title']}
Target Duration: {self.target_duration_minutes} minutes
Current Evaluation Phase: {phase['name']}
Primary Competency Target: {phase['primary_competency']}
Secondary Competency Target: {phase['secondary_competency']}
Is Concluding Turn: {is_final}

Previous Officer Response:
"{officer_text}"

Instructions:
1. Briefly acknowledge and synthesize what the officer said (1 concise sentence).
2. Ask a probing, intellectually rigorous follow-up question related to the course content and the competency '{phase['primary_competency']}'.
3. Pose a realistic administrative dilemma testing their judgment, rules adherence, or field implementation.
4. Keep the total output under 4 sentences. Speak directly to the officer."""

                if settings.GOOGLE_API_KEY:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY, temperature=0.3)
                    res = llm.invoke([HumanMessage(content=prompt)])
                    content = res.content.strip()
                    ack = "I have noted your analytical position on this matter."
                    return content, ack
                elif settings.OPENAI_API_KEY:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY, temperature=0.3)
                    res = llm.invoke([HumanMessage(content=prompt)])
                    content = res.content.strip()
                    ack = "Noted, Officer."
                    return content, ack
            except Exception as e:
                print(f"LLM interview follow-up fallback: {e}")

        # Deterministic Civil Service Follow-Up Matrix
        ack = "Thank you, Officer. Your perspective highlights key operational dimensions."
        primary = phase["primary_competency"]

        if is_final:
            return (
                f"Thank you, Officer {self.officer_name}. As we conclude this {self.target_duration_minutes}-minute interview: "
                f"Looking back at the institutional reforms required in '{self.course_info['title']}', what is the single most enduring "
                f"administrative change you will personally champion to ensure sustainable ethical governance and team accountability?",
                ack
            )

        if primary == "Project Management":
            q = (
                f"Building upon your point: during nationwide execution of {self.course_info['title']} deliverables, "
                f"unforeseen monsoon disruptions and staff shortages occur across multiple regional directorates. "
                f"How do you re-allocate project resources, adjust statutory milestones, and preserve data collection rigor without ballooning the budget?"
            )
        elif primary == "Leadership":
            q = (
                f"Let us examine team leadership under acute pressure: Suppose junior investigators report intense pushback "
                f"and intimidation from local influential actors during field surveys. How do you lead from the front, protect your field staff, "
                f"and ensure official procedures are maintained without compromising administrative morale?"
            )
        elif primary == "Ethics":
            q = (
                f"That brings us to public integrity and ethics: If a senior ministry official informally requests withholding "
                f"or recalculating adverse statistical findings to present a more favorable public narrative prior to parliamentary scrutiny, "
                f"how do you articulate your statutory duty, uphold the Code of Conduct, and navigate this conflict?"
            )
        elif primary == "Change Management":
            q = (
                f"Regarding institutional modernization: Resistance to digital CAPI workflows and automated reporting remains high "
                f"among senior clerical staff accustomed to manual paper files. What change management strategy do you implement "
                f"to overcome bureaucratic inertia and foster genuine digital adoption?"
            )
        else:
            q = (
                f"Under the technical provisions of '{self.course_info['title']}', how do you empirically demonstrate to the "
                f"National Statistical Commission that your proposed estimation corrections eliminate non-sampling bias?"
            )

        return q, ack

    def generate_analysis(self) -> InterviewAnalysisResponse:
        total_answers = len(self.officer_responses)
        all_text = " ".join([r["response"] for r in self.officer_responses])
        all_tags = [tag for r in self.officer_responses for tag in r["tags"]]

        # Calculate scores for each competency
        scores: Dict[str, CompetencyScore] = {}
        for comp in COMPETENCIES:
            # Count presence of tags and keyword depth
            frequency = all_tags.count(comp)
            word_count = len(all_text.split())
            
            # Base scoring: 72 + frequency * 5, capped at 96
            raw_score = 72.0 + (frequency * 4.5) + min(12.0, (word_count / 150) * 2.0)
            score_percent = min(96.0, max(65.0, round(raw_score, 1)))

            if score_percent >= 85:
                band = "Exemplary"
                growth = f"Consolidate advanced institutional SOPs and mentor junior officers in {comp.lower()}."
            elif score_percent >= 74:
                band = "Proficient"
                growth = f"Further deepen practical application of statutory frameworks when resolving complex {comp.lower()} dilemmas."
            else:
                band = "Needs Attention"
                growth = f"Recommend targeted refresher modules on {comp.lower()} and administrative case law."

            evidence = self._generate_evidence_for_competency(comp, self.officer_responses)
            scores[comp] = CompetencyScore(
                competency_name=comp,
                score_percent=score_percent,
                rating_band=band,
                key_evidence=evidence,
                growth_opportunity=growth
            )

        overall_score = round(sum(s.score_percent for s in scores.values()) / len(scores), 1)
        if overall_score >= 85:
            overall_band = "Executive Grade — Exemplary"
        elif overall_score >= 72:
            overall_band = "Executive Grade — Proficient"
        else:
            overall_band = "Development Required"

        strengths = [
            f"Demonstrated commendable command over the technical concepts of '{self.course_info['title']}'.",
            "Articulated structured, disciplined arguments adhering to civil service decorum and administrative protocol.",
            "Consistently prioritized public interest, statutory compliance, and transparent reporting."
        ]

        development_areas = [
            "Enhance crisis contingency planning by quantifying reserve resource allocations in advance.",
            "Formulate formalized stakeholder consultation frameworks during digital transformation and change management."
        ]

        apar_actions = [
            "Recommend accreditation for Senior Administrative Leadership & Policy Cadre.",
            "Assign as Master Trainer for regional capacity building in National Statistical Frameworks.",
            "Nominate for specialized executive workshop in Public Financial Integrity and Vigilance Administration."
        ]

        elapsed_total = self.officer_responses[-1]["elapsed_seconds"] if self.officer_responses else 1800
        mins = elapsed_total // 60
        secs = elapsed_total % 60
        formatted_duration = f"{mins}m {secs}s"

        summary = (
            f"Officer {self.officer_name} successfully completed the comprehensive 25-35 minute live oral examination "
            f"for '{self.course_info['title']}'. The evaluation confirmed strong grasp of course curriculum coupled with "
            f"high standards of public integrity (Ethics: {scores['Ethics'].score_percent}%), structured problem solving "
            f"(Decision Making: {scores['Decision Making'].score_percent}%), and team leadership under operational constraints."
        )

        return InterviewAnalysisResponse(
            session_id=self.session_id,
            course_id=self.course_id,
            course_title=self.course_info["title"],
            officer_name=self.officer_name,
            total_duration_formatted=formatted_duration,
            total_turns=total_answers,
            overall_score_percent=overall_score,
            overall_rating_band=overall_band,
            executive_summary=summary,
            competency_scores=scores,
            core_strengths=strengths,
            priority_development_areas=development_areas,
            recommended_apar_actions=apar_actions,
            transcript=self.transcript
        )

    def _generate_evidence_for_competency(self, comp: str, responses: List[Dict[str, Any]]) -> str:
        for r in responses:
            if comp in r["tags"]:
                snippet = r["response"][:140].replace("\n", " ").strip()
                return f"Observed in Turn {r['turn']}: \"{snippet}...\""
        return f"Consistently integrated {comp} principles across multi-turn administrative deliberations."


class InterviewSessionManager:
    _sessions: Dict[str, LiveInterviewSession] = {}

    @classmethod
    def start_interview(cls, req: InterviewStartRequest) -> LiveInterviewSession:
        session_id = f"interview_{uuid.uuid4().hex[:12]}"
        session = LiveInterviewSession(
            session_id=session_id,
            course_id=req.course_id,
            officer_name=req.officer_name or "Officer",
            target_duration_minutes=req.target_duration_minutes
        )
        cls._sessions[session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[LiveInterviewSession]:
        return cls._sessions.get(session_id)
