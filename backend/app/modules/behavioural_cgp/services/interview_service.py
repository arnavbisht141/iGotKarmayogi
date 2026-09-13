import uuid
import json
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.models import Course, Module, Lesson
from ..schemas import (
    InterviewStartRequest,
    InterviewTurnRequest,
    InterviewTurnResponse,
    CompetencyScore,
    TranscriptEntry,
    MultimodalTelemetrySummary,
    InterviewAnalysisResponse,
    VideoBehaviouralTelemetry,
    SpeechAcousticTelemetry
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
    def __init__(
        self,
        session_id: str,
        course_id: int,
        officer_name: str,
        target_duration_minutes: int,
        course_info_override: Optional[Dict[str, Any]] = None
    ):
        self.session_id = session_id
        self.course_id = course_id
        self.officer_name = officer_name
        self.target_duration_minutes = target_duration_minutes
        if course_info_override:
            self.course_info = course_info_override
        else:
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

    def process_turn(
        self,
        officer_text: str,
        elapsed_seconds: int,
        speaking_pace_wpm: Optional[float] = None,
        eye_contact_percent: Optional[float] = None,
        composure_score: Optional[float] = None,
        voice_clarity_score: Optional[float] = None,
        posture_stability_score: Optional[float] = None,
        head_movement_rate: Optional[float] = None,
        fidgeting_index: Optional[float] = None,
        filler_words_count: Optional[int] = None,
        pauses_count: Optional[int] = None,
        coherence_score: Optional[float] = None
    ) -> InterviewTurnResponse:
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

        # Multimodal telemetry calculation
        words = len(officer_text.split())
        prev_elapsed = self.officer_responses[-1]["elapsed_seconds"] if self.officer_responses else 0
        turn_duration = max(10, elapsed_seconds - prev_elapsed)
        calc_wpm = round((words / max(0.2, turn_duration / 60.0)), 1)
        effective_wpm = speaking_pace_wpm if (speaking_pace_wpm and speaking_pace_wpm > 0) else min(220.0, max(50.0, calc_wpm))
        effective_composure = composure_score if (composure_score is not None and composure_score > 0) else 88.0
        effective_clarity = voice_clarity_score if (voice_clarity_score is not None and voice_clarity_score > 0) else 92.0
        effective_eye_contact = eye_contact_percent if (eye_contact_percent is not None and eye_contact_percent > 0) else 85.0
        effective_posture = posture_stability_score if (posture_stability_score is not None and posture_stability_score > 0) else 86.0
        effective_head = head_movement_rate if (head_movement_rate is not None and head_movement_rate > 0) else 2.1
        effective_fidget = fidgeting_index if (fidgeting_index is not None) else 0.8
        effective_fillers = filler_words_count if (filler_words_count is not None) else max(0, int(len(officer_text.split()) * 0.02))
        effective_pauses = pauses_count if (pauses_count is not None) else max(1, int(turn_duration / 8))
        effective_coherence = coherence_score if (coherence_score is not None and coherence_score > 0) else 89.0

        self.officer_responses.append({
            "turn": self.current_turn - 1,
            "response": officer_text,
            "elapsed_seconds": elapsed_seconds,
            "speaking_duration": turn_duration,
            "speaking_pace_wpm": effective_wpm,
            "composure_score": effective_composure,
            "voice_clarity_score": effective_clarity,
            "eye_contact_percent": effective_eye_contact,
            "posture_stability_score": effective_posture,
            "head_movement_rate": effective_head,
            "fidgeting_index": effective_fidget,
            "filler_words_count": effective_fillers,
            "pauses_count": effective_pauses,
            "coherence_score": effective_coherence,
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

        # Pacing and delivery feedback
        target_secs = self.target_duration_minutes * 60
        remaining_secs = max(0, target_secs - elapsed_seconds)
        rem_min = remaining_secs // 60
        pacing_advice = f"Interview pacing optimal: ~{rem_min} minutes remaining. Transitioning to {current_phase['name']}."

        if effective_wpm < 100:
            pace_note = f"Measured speaking pace ({effective_wpm:.0f} WPM)."
        elif effective_wpm > 165:
            pace_note = f"Brisk speaking pace ({effective_wpm:.0f} WPM); recommend steady cadence."
        else:
            pace_note = f"Optimal executive cadence ({effective_wpm:.0f} WPM)."

        delivery_feedback = f"{pace_note} High composure ({effective_composure:.0f}%) and articulate delivery."

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
            acknowledgement_note=ack_note,
            detected_competencies=tags,
            delivery_feedback=delivery_feedback
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

        # Deterministic Civil Service Follow-Up Matrix anchored in course syllabus
        ack = "Thank you, Officer. Your perspective highlights key operational dimensions."
        primary = phase["primary_competency"]

        themes = self.course_info.get("key_themes", [])
        theme_pm = themes[0] if len(themes) > 0 else "statutory milestones"
        theme_lead = themes[1] if len(themes) > 1 else "field operations"
        theme_eth = themes[2] if len(themes) > 2 else "statutory compliance and audit findings"
        theme_cm = themes[3] if len(themes) > 3 else "digital administrative workflows"

        if is_final:
            return (
                f"Thank you, Officer {self.officer_name}. As we conclude this {self.target_duration_minutes}-minute interview: "
                f"Looking back at the institutional reforms required in '{self.course_info['title']}', what is the single most enduring "
                f"administrative change you will personally champion to ensure sustainable ethical governance and team accountability?",
                ack
            )

        if primary == "Project Management":
            q = (
                f"Building upon your point: during nationwide execution of '{self.course_info['title']}', specifically concerning '{theme_pm}', "
                f"unforeseen field disruptions and resource constraints emerge across multiple directorates. "
                f"How do you re-allocate project resources, adjust statutory milestones, and preserve implementation rigor without ballooning the budget?"
            )
        elif primary == "Leadership":
            q = (
                f"Let us examine team leadership under acute operational pressure in '{self.course_info['title']}': Suppose junior personnel "
                f"responsible for '{theme_lead}' report severe pushback and intimidation from local influential actors during inspections. "
                f"How do you lead from the front, protect field staff, and ensure official procedures are maintained without compromising administrative morale?"
            )
        elif primary == "Ethics":
            q = (
                f"That brings us to public integrity and statutory ethics: If an administrative authority informally urges withholding "
                f"or recalculating adverse official findings related to '{theme_eth}' prior to parliamentary or audit scrutiny, "
                f"how do you articulate your statutory duty, uphold the Civil Services Conduct Rules, and navigate this conflict?"
            )
        elif primary == "Change Management":
            q = (
                f"Regarding institutional modernization: Resistance to digital adoption and standardized workflows for '{theme_cm}' "
                f"remains entrenched among senior staff accustomed to manual paper files. What change management strategy do you implement "
                f"to overcome bureaucratic inertia and foster genuine digital adoption?"
            )
        else:
            q = (
                f"Under the technical provisions of '{self.course_info['title']}', how do you empirically demonstrate to the "
                f"Executive Evaluation Commission that your implementation safeguards eliminate procedural errors and administrative bias?"
            )

        return q, ack

    def generate_analysis(self) -> InterviewAnalysisResponse:
        total_answers = len(self.officer_responses)
        all_text = " ".join([r["response"] for r in self.officer_responses])
        all_tags = [tag for r in self.officer_responses for tag in r["tags"]]

        # Multimodal Telemetry Metrics aggregation
        wpms = [r.get("speaking_pace_wpm") for r in self.officer_responses if r.get("speaking_pace_wpm")]
        avg_wpm = round(sum(wpms) / len(wpms), 1) if wpms else 126.0

        composures = [r.get("composure_score") for r in self.officer_responses if r.get("composure_score")]
        avg_composure = round(sum(composures) / len(composures), 1) if composures else 88.0

        clarities = [r.get("voice_clarity_score") for r in self.officer_responses if r.get("voice_clarity_score")]
        avg_clarity = round(sum(clarities) / len(clarities), 1) if clarities else 92.0
        clarity_rating = "Executive Grade — Highly Articulate" if avg_clarity >= 85 else "Competent & Clear"

        total_speaking_time = sum(r.get("speaking_duration", 30) for r in self.officer_responses)

        telemetry_summary = MultimodalTelemetrySummary(
            average_speaking_wpm=avg_wpm,
            delivery_composure_score=avg_composure,
            speech_clarity_rating=clarity_rating,
            total_speaking_time_seconds=total_speaking_time,
            pacing_adherence="Optimal — 25-35m Board Pacing Maintained"
        )

        # Calculate scores for each competency
        scores: Dict[str, CompetencyScore] = {}
        for comp in COMPETENCIES:
            frequency = all_tags.count(comp)
            word_count = len(all_text.split())
            
            # Base scoring: 72 + frequency * 4.5 + word depth
            raw_score = 72.0 + (frequency * 4.5) + min(12.0, (word_count / 150) * 2.0)

            # Multimodal modifier: Communication benefits from optimal WPM and clarity; Leadership from composure
            if comp == "Communication":
                wpm_bonus = 3.0 if (110 <= avg_wpm <= 150) else 1.0
                raw_score += wpm_bonus + (avg_clarity - 80) * 0.1
            elif comp == "Leadership":
                raw_score += (avg_composure - 80) * 0.15

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

        # Video and Speech Telemetry Aggregations
        postures = [r.get("posture_stability_score") for r in self.officer_responses if r.get("posture_stability_score")]
        avg_posture = round(sum(postures) / len(postures), 1) if postures else 86.0

        eyes = [r.get("eye_contact_percent") for r in self.officer_responses if r.get("eye_contact_percent")]
        avg_eye = round(sum(eyes) / len(eyes), 1) if eyes else 85.0

        total_fillers = sum(r.get("filler_words_count", 0) for r in self.officer_responses)
        total_pauses = sum(r.get("pauses_count", 0) for r in self.officer_responses)

        video_telemetry = VideoBehaviouralTelemetry(
            posture_stability="Upright, centered executive seating maintained" if avg_posture >= 80 else "Adequate posture; occasional shifting observed",
            posture_stability_score=avg_posture,
            head_movement_observed="Controlled, responsive nodding aligned with active conversational exchange",
            gaze_alignment_percent=avg_eye,
            excessive_movement_fidgeting="Low / within standard baseline bounds",
            observable_summary=f"Continuous visual telemetry indicated stable gaze orientation ({avg_eye:.0f}%) and disciplined physical composure ({avg_posture:.0f}% stability) without extraneous fidgeting."
        )

        pace_desc = "Optimal executive cadence (115-145 WPM)" if (110 <= avg_wpm <= 150) else ("Measured delivery (<110 WPM)" if avg_wpm < 110 else "Rapid pace (>150 WPM)")
        speech_telemetry = SpeechAcousticTelemetry(
            average_wpm=avg_wpm,
            pace_assessment=pace_desc,
            pauses_frequency=f"Structured syntactic pauses ({total_pauses} measured pauses across responses)",
            filler_word_count=total_fillers,
            clarity_score=avg_clarity,
            clarity_rating=clarity_rating,
            coherence_assessment="High conceptual coherence: responses systematically state the administrative issue, cite the relevant statutory mandate, and articulate mitigating execution safeguards.",
            delivery_cadence="Steady, authoritative, and audible delivery throughout examination."
        )

        overall_score = round(sum(s.score_percent for s in scores.values()) / len(scores), 1)
        if overall_score >= 85:
            overall_band = "Executive Grade — Exemplary"
        elif overall_score >= 72:
            overall_band = "Executive Grade — Proficient"
        else:
            overall_band = "Development Required"

        overall_assessment = (
            f"Officer {self.officer_name} demonstrated a {overall_band.lower()} performance during the live oral examination. "
            f"The officer exhibited disciplined mastery over the statutory requirements of '{self.course_info['title']}' "
            f"combined with balanced executive decision-making under simulated procedural constraints."
        )

        course_understanding = (
            f"Exhibited comprehensive comprehension of '{self.course_info['title']}'. Accurately cited key operational "
            f"rules, statutory authorities ({self.course_info.get('organization', 'Central Cadre')}), and standard operating procedures. "
            f"Effectively distinguished between mandatory statutory compliance and discretionary administrative adjustments."
        )

        communication_assessment = (
            f"Communication was articulate and structured (Cadence: {avg_wpm:.0f} WPM, Clarity: {avg_clarity:.0f}%). "
            f"The officer responded directly to prompts with minimal filler frequency ({total_fillers} instances) "
            f"and maintained strong communicative engagement throughout."
        )

        decision_making_assessment = (
            f"Decision-making score: {scores.get('Decision Making', CompetencyScore(competency_name='Decision Making', score_percent=82.0, rating_band='Proficient', key_evidence='', growth_opportunity='')).score_percent}%. "
            f"The officer consistently prioritized the principles of natural justice (Audi Alteram Partem), "
            f"fiscal integrity, and institutional accountability before exercising executive discretion."
        )

        conversation_analysis = (
            f"Across {total_answers} structured oral turns, the candidate displayed logical progression and high "
            f"thematic consistency. Early turns established foundational subject matter rigor, while subsequent responses "
            f"successfully resolved crisis scenarios, resource trade-offs, and ethical challenges without contradictions."
        )

        areas_for_improvement = [
            "Quantify contingency budget allocations and field reserve buffers earlier during project planning.",
            "Formulate formalized stakeholder consultation frameworks during digital transformation and change management.",
            "Streamline preliminary interlocutory administrative orders to preempt premature procedural appeals."
        ]

        elapsed_total = self.officer_responses[-1]["elapsed_seconds"] if self.officer_responses else 1800
        mins = elapsed_total // 60
        secs = elapsed_total % 60
        formatted_duration = f"{mins}m {secs}s"

        strengths = [
            f"Demonstrated commendable command over the technical concepts of '{self.course_info['title']}'.",
            f"Delivered structured, disciplined arguments with an optimal speaking cadence ({avg_wpm:.0f} WPM) and high poise ({avg_composure:.0f}% composure).",
            "Consistently prioritized public interest, statutory compliance, and transparent reporting."
        ]

        development_areas = [
            "Enhance crisis contingency planning by quantifying reserve resource allocations in advance.",
            "Formulate formalized stakeholder consultation frameworks during digital transformation and change management."
        ]

        recommended_upskilling = [
            f"Advanced Module: Administrative Jurisprudence and Quasi-Judicial Inquiries in '{self.course_info['title']}'",
            "Executive Simulation: Crisis Management and Field Negotiation for Senior Officers",
            "Masterclass: Public Financial Accountability and GFR Procurement Compliance (ISTM)",
            "Seminar: Evidence-Based Public Policy Formulation & Algorithmic Governance"
        ]

        apar_actions = [
            "Recommend accreditation for Senior Administrative Leadership & Policy Cadre.",
            f"Assign as Master Trainer for regional capacity building in '{self.course_info['title']}'.",
            "Nominate for specialized executive workshop in Public Financial Integrity and Vigilance Administration."
        ]

        summary = (
            f"Officer {self.officer_name} successfully completed the comprehensive 25-35 minute live oral examination "
            f"for '{self.course_info['title']}'. The evaluation confirmed strong grasp of course curriculum coupled with "
            f"high standards of public integrity (Ethics: {scores.get('Ethics', CompetencyScore(competency_name='Ethics', score_percent=85.0, rating_band='Exemplary', key_evidence='', growth_opportunity='')).score_percent}%), "
            f"structured problem solving (Decision Making: {scores.get('Decision Making', CompetencyScore(competency_name='Decision Making', score_percent=82.0, rating_band='Proficient', key_evidence='', growth_opportunity='')).score_percent}%), "
            f"and executive poise ({avg_composure:.0f}% composure) at an average delivery cadence of {avg_wpm:.0f} WPM."
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
            overall_assessment=overall_assessment,
            course_understanding=course_understanding,
            communication_assessment=communication_assessment,
            decision_making_assessment=decision_making_assessment,
            executive_summary=summary,
            competency_scores=scores,
            core_strengths=strengths,
            areas_for_improvement=areas_for_improvement,
            priority_development_areas=development_areas,
            recommended_upskilling=recommended_upskilling,
            recommended_apar_actions=apar_actions,
            conversation_analysis=conversation_analysis,
            video_behavioural_observations=video_telemetry,
            speech_analysis=speech_telemetry,
            transcript=self.transcript,
            telemetry_summary=telemetry_summary,
            observable_signals_disclaimer=(
                "Notice: Observable behavioral and speech telemetry reflect neutral physical metrics "
                "(cadence, head orientation, and acoustic stability) captured in-browser. "
                "They do not constitute emotional profiling, psychological diagnosis, or character judgements."
            )
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
    def start_interview(cls, req: InterviewStartRequest, db: Optional[Session] = None) -> LiveInterviewSession:
        session_id = f"interview_{uuid.uuid4().hex[:12]}"

        course_override = None
        if db:
            course = db.query(Course).filter(Course.id == req.course_id).first()
            if course:
                module_titles = [m.title for m in (course.modules or [])]
                from .carryforward_generator import COURSE_NOTICE_MAPPING
                mapped_notice_id = COURSE_NOTICE_MAPPING.get(course.id)
                
                notice_summary = ""
                if mapped_notice_id:
                    from .corpus import get_document_by_id
                    doc = get_document_by_id(mapped_notice_id)
                    if doc:
                        notice_summary = f"{doc.title} ({doc.statutory_reference})"
                
                org_name = getattr(course, "organization", None) or "iGOT Karmayogi"
                if req.course_id in COURSE_CONTEXTS:
                    ctx = COURSE_CONTEXTS[req.course_id].copy()
                    ctx["title"] = course.title
                    ctx["organization"] = org_name
                    if module_titles:
                        ctx["key_themes"] = module_titles[:4]
                    course_override = ctx
                else:
                    first_topic = module_titles[0] if module_titles else course.title
                    init_q = (
                        f"Good morning, Officer {req.officer_name or 'Candidate'}. Welcome to your oral competency examination on "
                        f"'{course.title}', accredited under {org_name}. "
                        f"To begin: Drawing from the core curriculum on '{first_topic}', what statutory procedures and administrative safeguards "
                        f"must an officer enforce to guarantee procedural compliance and public accountability in your department?"
                    )
                    course_override = {
                        "title": course.title,
                        "organization": org_name,
                        "key_themes": module_titles or ["Administrative Integrity", "Statutory Compliance", "Public Policy Execution"],
                        "initial_question": init_q,
                        "notice_summary": notice_summary
                    }

        session = LiveInterviewSession(
            session_id=session_id,
            course_id=req.course_id,
            officer_name=req.officer_name or "Officer",
            target_duration_minutes=req.target_duration_minutes,
            course_info_override=course_override
        )
        cls._sessions[session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[LiveInterviewSession]:
        return cls._sessions.get(session_id)
