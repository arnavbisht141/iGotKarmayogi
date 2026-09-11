import uuid
import json
from typing import Dict, List, Optional
from ..schemas import (
    CaseScenario,
    CarryforwardQuestion,
    CarryforwardOption,
    CaseGenerationRequest
)
from .corpus import OFFICIAL_GOVERNMENT_DOCUMENTS
from .notice_extractor import NoticeExtractor
from app.core.config import settings

# Pre-seeded authentic branching case scenarios
PRE_SEEDED_CASES: List[CaseScenario] = [
    # Case 1: CCS Rule 14 Disciplinary Inquiry
    CaseScenario(
        id="case_ccs_rule14_inquiry",
        title="Disciplinary Inquiry Proceeding under Rule 14 CCS (CCA) Rules",
        category="Disciplinary Proceedings & Natural Justice",
        document_id="doc_dopt_rule14_proceeding",
        document_title="Departmental Inquiry Proceeding under Rule 14 of CCS (CCA) Rules, 1965",
        document_type="Departmental Proceeding",
        statutory_citations=[
            "CCS (CCA) Rules, 1965 — Rule 14",
            "Constitution of India — Article 311(2)",
            "Principles of Natural Justice (Audi Alteram Partem)"
        ],
        initial_context="""You are appointed as the Inquiring Authority (IA) under Rule 14(5)(b) of CCS (CCA) Rules, 1965, to conduct oral inquiry into major penalty charges framed against a Deputy Director for premature disclosure of preliminary statistical indices. 

The Charged Officer (CO) has submitted Form 4 denying all charges and claims the prosecution document exhibits rely on unverified email printouts without digital certification.""",
        root_question_id="q_ccs_root",
        questions={
            "q_ccs_root": CarryforwardQuestion(
                id="q_ccs_root",
                case_id="case_ccs_rule14_inquiry",
                stage_type="root",
                prompt="At the preliminary hearing of the inquiry, the Presenting Officer (PO) requests that because the digital logs clearly bear the officer's login ID, the formal inspection of original system servers by the Charged Officer should be dispensed with to expedite proceedings. How must you rule as Inquiring Authority?",
                context_update="Preliminary hearing stage before the Inquiring Authority.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Reject the PO's request and strictly direct inspection of original system records under Rule 14(11) to safeguard Audi Alteram Partem.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Procedural integrity preserved. Natural justice complied with, precluding CAT quashing.",
                        statutory_rationale="Under Rule 14(11), the Charged Officer has an absolute statutory right to inspect listed documents to prepare defense. Dispensing with inspection violates Article 311(2).",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Accede to the PO's request and accept photocopies directly to avoid government administrative delays.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Procedural irregularity committed. Charged officer files statutory objection alleging bias and denial of defense.",
                        statutory_rationale="Denying inspection of primary digital evidence violates mandatory procedure under Rule 14(11) and invalidates subsequent inquiry findings.",
                        next_question_id="q_ccs_branch_bias"
                    ),
                    CarryforwardOption(
                        option_id="C",
                        text="Order the Charged Officer to immediately submit his defense witnesses before the prosecution establishes its case.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Inverted burden of proof. The inquiry sequence is fatally compromised.",
                        statutory_rationale="Under Rule 14, the prosecution must present and substantiate its case first. Inverting sequence violates statutory inquiry doctrine.",
                        next_question_id="q_ccs_branch_sequence"
                    ),
                    CarryforwardOption(
                        option_id="D",
                        text="Adjourn sine die and refer the entire matter back to the Disciplinary Authority without holding hearings.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Dereliction of quasi-judicial duty. The Inquiring Authority cannot abandon assigned mandate.",
                        statutory_rationale="Once appointed under Rule 14(5), the IA must conduct proceedings expeditiously and submit reasoned findings.",
                        next_question_id="q_ccs_branch_dereliction"
                    )
                ],
                behavioral_competencies=["Ethics", "Decision Making", "Leadership"]
            ),
            # Carryforward branch from Option B (Denying inspection)
            "q_ccs_branch_bias": CarryforwardQuestion(
                id="q_ccs_branch_bias",
                case_id="case_ccs_rule14_inquiry",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] Following your decision to accept uncertified printouts without defense inspection, the Charged Officer submits an urgent representation to the Disciplinary Authority alleging bias against you and seeking transfer of the inquiry under DoPT guidelines. How must you proceed as the Inquiring Authority?",
                context_update="Escalation: The inquiry is halted due to allegations of procedural bias under Rule 14.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Immediately stay further proceedings, record the representation on file, and forward the papers to the Disciplinary Authority for a decision on the bias allegation.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Correct quasi-judicial remediation. Prevents contamination of proceedings and allows the DA to issue appropriate directions.",
                        statutory_rationale="Per DoPT O.M. No. 142/2/83-AVD.I, whenever an application alleging bias against the IA is filed, the IA must stay proceedings until the DA passes a speaking order.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Ignore the representation, hold ex-parte hearings, and submit a guilty finding to teach the officer administrative discipline.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Severe misconduct as IA. The final penalty will be quashed by CAT with heavy personal cost.",
                        statutory_rationale="Proceeding ex-parte after a bias application is filed constitutes grave procedural illegality and establishes actual bias.",
                        next_question_id="q_ccs_branch_terminal_quash"
                    ),
                    CarryforwardOption(
                        option_id="C",
                        text="Expel the Charged Officer's Defense Assistant from the hearing room for filing the petition.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Direct infringement of the right to defense representation under Rule 14(8).",
                        statutory_rationale="The Charged Officer has a statutory right to be assisted by a Government servant or legal practitioner (where permitted). Expulsion is unauthorized.",
                        next_question_id="q_ccs_branch_terminal_quash"
                    )
                ],
                behavioral_competencies=["Ethics", "Communication", "Decision Making"]
            ),
            # Carryforward branch from Option C (Inverted Sequence)
            "q_ccs_branch_sequence": CarryforwardQuestion(
                id="q_ccs_branch_sequence",
                case_id="case_ccs_rule14_inquiry",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] Because you demanded defense evidence before prosecution examination, the Defense Assistant points out in writing that prosecution has not established the foundational digital chain of custody. How do you rectify this procedural error?",
                context_update="Procedural objection entered into record regarding evidentiary sequence.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Record a corrective procedural order restoring the statutory order: call upon the Presenting Officer to produce prosecution witnesses and verify exhibits first.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Inquiry re-aligned with statutory sequence under Rule 14(14). Procedural validity restored.",
                        statutory_rationale="An Inquiring Authority can correct interlocutory procedure to ensure compliance with Rule 14(14) before evidence concludes.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Compel the Charged Officer to testify under oath against himself to verify the log entries.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Violates protection against self-incrimination and Rule 14(18) mandatory examination doctrine.",
                        statutory_rationale="Under Rule 14(18), questioning of the CO by the IA can only occur after the CO has closed his defense, and cannot be used to elicit confessions.",
                        next_question_id="q_ccs_branch_terminal_quash"
                    )
                ],
                behavioral_competencies=["Decision Making", "Project Management"]
            ),
            # Carryforward branch from Option D
            "q_ccs_branch_dereliction": CarryforwardQuestion(
                id="q_ccs_branch_dereliction",
                case_id="case_ccs_rule14_inquiry",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] The Disciplinary Authority remands the inquiry file back to you with strict instructions to complete the inquiry within the 6-month statutory limit. What project management step do you take?",
                context_update="Remanded inquiry under strict time limits.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Draw up a structured Day-to-Day Inquiry Schedule under Rule 14(24) and serve advance notices to all parties.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Systematic project management re-established with enforceable timelines.",
                        statutory_rationale="DoPT prescribes time-bound daily hearings to complete major penalty inquiries within 6 months.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Ask the Charged Officer to waive oral hearings in exchange for a recommendation of a minor penalty.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Unlawful plea bargaining. The IA has no power to negotiate penalties.",
                        statutory_rationale="The IA is merely a fact-finding officer; penalty determination belongs exclusively to the Disciplinary Authority.",
                        next_question_id="q_ccs_branch_terminal_quash"
                    )
                ],
                behavioral_competencies=["Project Management", "Leadership"]
            ),
            # Terminal remediation fallback
            "q_ccs_branch_terminal_quash": CarryforwardQuestion(
                id="q_ccs_branch_terminal_quash",
                case_id="case_ccs_rule14_inquiry",
                stage_type="carryforward_branch",
                prompt="[FINAL CARRYFORWARD REMEDIATION] Due to consecutive procedural defects, the Disciplinary Authority issues a formal scrutiny note requiring you to submit a revised report strictly evaluating only legally admissible evidence. What is your final action?",
                context_update="Statutory scrutiny review stage.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Expunge all unverified exhibits, evaluate solely validated evidence, and submit a reasoned finding with separate analysis for each Article of Charge.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Satisfactory resolution achieved through rigorous quasi-judicial analysis.",
                        statutory_rationale="Rule 14(23) requires an assessment of each charge independently based on legally admissible evidence.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Reiterate previous conclusions without revising the evidence record.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,  # Terminates but with low score
                        consequence_summary="Sub-optimal closure. The report remains legally vulnerable.",
                        statutory_rationale="Failing to cure defects when given opportunity by the DA invalidates the finding.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Ethics", "Decision Making"]
            )
        },
        learning_objectives=[
            "Enforce statutory compliance with CCS (CCA) Rule 14",
            "Uphold Principles of Natural Justice (Audi Alteram Partem)",
            "Manage quasi-judicial timelines and bias objections according to DoPT standards"
        ]
    ),

    # Case 2: GFR 149 & GeM Procurement Irregularity
    CaseScenario(
        id="case_gfr_gem_procurement",
        title="Procurement Scrutiny & Debarment under GFR Rule 149 / 151",
        category="Public Procurement & Vigilance Integrity",
        document_id="doc_gfr_gem_procurement_notice",
        document_title="Procurement Irregularity Scrutiny Notice & Vendor Debarment under GFR Rule 149 / 151",
        document_type="Notice",
        statutory_citations=[
            "General Financial Rules (GFR) 2017 — Rules 144, 149, 151",
            "CVC Circular on Public Procurement & Cartelization",
            "Constitution of India — Article 14 (Equality & Reasonableness)"
        ],
        initial_context="""As Chairman of the Tender Evaluation Committee for IT hardware procurement in the Statistical Directorate, you discover during automated GeM bid evaluation that the lowest two bidding entities (L1 and L2) submitted bids from identical IP addresses within 3 minutes of each other, suggesting collusive cartelization.""",
        root_question_id="q_gem_root",
        questions={
            "q_gem_root": CarryforwardQuestion(
                id="q_gem_root",
                case_id="case_gfr_gem_procurement",
                stage_type="root",
                prompt="The delivery of equipment is urgent for the upcoming All-India Survey launch. Members of the committee suggest declaring L1 as winner anyway to avoid delaying survey fieldwork. How must you act as Committee Chairman?",
                context_update="Bid opening stage on GeM with apparent cartelization.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Halt tender finalization, withhold L1 award, record the IP evidence on file, and issue a formal Show-Cause Notice under GFR Rule 151 giving 21 days for explanation.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Due process followed. Upholds public procurement integrity and complies with CVC guidelines.",
                        statutory_rationale="GFR Rule 151 and CVC guidelines require issuing a formal show-cause notice before taking adverse penal actions or awarding suspect collusive tenders.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Immediately cancel the tender and blacklist both vendors on GeM on the spot without seeking their explanation.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Summary debarment without notice violates Article 14. Vendors initiate High Court litigation.",
                        statutory_rationale="Debarment without opportunity of representation is ultra vires natural justice and consistently set aside by High Courts.",
                        next_question_id="q_gem_branch_litigation"
                    ),
                    CarryforwardOption(
                        option_id="C",
                        text="Award the contract to L1 as recommended by committee members, but demand a written discount to offset any collusive premium.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Serious vigilance violation. Compromising with suspected cartelization invites CVC inquiry.",
                        statutory_rationale="Negotiating with a suspect collusive bidder violates CVC directives and GFR Rule 173(xiv).",
                        next_question_id="q_gem_branch_cvc_audit"
                    ),
                    CarryforwardOption(
                        option_id="D",
                        text="Split the procurement order into smaller sub-₹5 lakh purchases to bypass GeM bidding thresholds.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Gross financial irregularity: tender splitting strictly forbidden under GFR Rule 157.",
                        statutory_rationale="Splitting indents to evade competition violates GFR Rule 157 and constitutes personal financial misconduct.",
                        next_question_id="q_gem_branch_cvc_audit"
                    )
                ],
                behavioral_competencies=["Ethics", "Leadership", "Decision Making"]
            ),
            # Carryforward branch from Option B (Summary Debarment -> Litigation)
            "q_gem_branch_litigation": CarryforwardQuestion(
                id="q_gem_branch_litigation",
                case_id="case_gfr_gem_procurement",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] The vendor obtains an interim stay from the High Court against the summary blacklisting due to lack of a Show-Cause Notice. The Ministry Law Officer directs you to resolve the impasse immediately. What is the legally sound next step?",
                context_update="Court stay granted against the department for procedural violation of natural justice.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Recall the defective summary blacklisting order with court permission, issue a comprehensive Show-Cause Notice citing IP access logs and GST linkages, and grant 21 days for representation.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Procedural defect cured. Department regains legal standing and complies with Rule 151.",
                        statutory_rationale="Recalling an unreasoned order and initiating proper quasi-judicial proceedings under GFR Rule 151 restores legality.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Defy the court stay and encash the vendor's Bank Guarantee immediately.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Contempt of Court proceedings initiated against the Chairman personally.",
                        statutory_rationale="Willful violation of an interim court stay constitutes contempt under the Contempt of Courts Act, 1971.",
                        next_question_id="q_gem_branch_cvc_audit"
                    )
                ],
                behavioral_competencies=["Ethics", "Decision Making", "Change Management"]
            ),
            # Carryforward branch from Option C/D (CVC Audit Referral)
            "q_gem_branch_cvc_audit": CarryforwardQuestion(
                id="q_gem_branch_cvc_audit",
                case_id="case_gfr_gem_procurement",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] The Chief Vigilance Officer (CVO) flags the irregular procurement process and demands a compliance explanation within 48 hours. How do you respond as Chairman?",
                context_update="Vigilance scrutiny initiated by CVO under CVC Act.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Submit a transparent fact-finding note detailing the committee deliberations, cancel the tainted process, and re-tender via open L1 custom bidding with stringent anti-cartelization filters.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Integrity reaffirmed. Clean re-procurement initiated without public loss.",
                        statutory_rationale="Transparent reporting and prompt corrective cancellation mitigates vigilance liability.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Attempt to backdate procurement committee minutes to show that IP logs were reviewed.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,
                        consequence_summary="Fabrication of official government records under Section 465 IPC / CCS Conduct Rules.",
                        statutory_rationale="Falsifying government files constitutes criminal forgery and attracts mandatory dismissal.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Ethics", "Communication", "Leadership"]
            )
        },
        learning_objectives=[
            "Apply GFR 2017 Rule 149 and 151 compliance standards in public procurement",
            "Detect and address collusive bidding / cartelization without violating natural justice",
            "Exercise institutional leadership and vigilance adherence under pressure of urgent deadlines"
        ]
    ),

    # Case 3: RTI Statutory First Appeal & Statistical Confidentiality
    CaseScenario(
        id="case_rti_microdata_appeal",
        title="Statutory First Appeal under RTI Act, 2005 (Microdata Disclosure)",
        category="Statutory Compliance & Data Governance",
        document_id="doc_rti_first_appeal_proceeding",
        document_title="Statutory First Appellate Authority Proceeding under Section 19(1) of RTI Act, 2005",
        document_type="Statutory Form",
        statutory_citations=[
            "Right to Information Act, 2005 — Sections 8(1)(j), 10(1), 19(1)",
            "Collection of Statistics Act, 2008 — Confidentiality Clause",
            "UN Fundamental Principles of Official Statistics — Principle 5"
        ],
        initial_context="""You are designated as the First Appellate Authority (FAA) under Section 19(1) of the RTI Act. A prominent academic researcher has filed an appeal challenging the CPIO's rejection of their request for household-level consumption expenditure survey microdata. The CPIO invoked a blanket exemption under Section 8(1)(j) regarding personal privacy.""",
        root_question_id="q_rti_root",
        questions={
            "q_rti_root": CarryforwardQuestion(
                id="q_rti_root",
                case_id="case_rti_microdata_appeal",
                stage_type="root",
                prompt="Under RTI jurisprudence and statutory statistical frameworks, how should you adjudicate this First Appeal as the Appellate Authority?",
                context_update="Statutory First Appeal hearing under Section 19(1).",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Invoke the Doctrine of Severability under Section 10(1): direct the CPIO to sever all personally identifiable identifiers (names, addresses, phone numbers) and release the anonymized statistical microdata within 15 days.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Exemplary statutory balance. Safeguards individual privacy under UN Principle 5 while facilitating public scientific research.",
                        statutory_rationale="Section 10(1) mandates disclosure of non-exempt severed portions when privacy concerns can be insulated through anonymization.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Dismiss the appeal outright without a hearing, upholding the CPIO's blanket rejection to eliminate any work for the data division.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Failure of quasi-judicial duty. Appellant files Second Appeal before Central Information Commission (CIC).",
                        statutory_rationale="The FAA must pass a speaking order recording reasons. Unreasoned summary rejections are severely reprimanded by the CIC under Section 20.",
                        next_question_id="q_rti_branch_cic_hearing"
                    ),
                    CarryforwardOption(
                        option_id="C",
                        text="Direct full disclosure of raw, un-anonymized household data including respondent phone numbers and street locations.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Breach of statutory statistical confidentiality under Collection of Statistics Act and UN-NQAF.",
                        statutory_rationale="Disclosing personally identifiable respondent data violates Collection of Statistics Act Section 15 and individual privacy.",
                        next_question_id="q_rti_branch_confidentiality_breach"
                    )
                ],
                behavioral_competencies=["Decision Making", "Ethics", "Communication"]
            ),
            # Carryforward branch from Option B (CIC Escalation)
            "q_rti_branch_cic_hearing": CarryforwardQuestion(
                id="q_rti_branch_cic_hearing",
                case_id="case_rti_microdata_appeal",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] The Central Information Commission (CIC) issues a strict Show-Cause Notice under Section 20 of the RTI Act to your CPIO for persistent denial of public data. How do you intervene as Appellate Authority to resolve this institutional crisis?",
                context_update="CIC Section 20 penalty proceedings initiated against the department.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Convene an urgent compliance review: direct immediate anonymization under Section 10(1), formulate an open institutional data-sharing SOP, and appear before CIC confirming complete compliance.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Institutional credibility restored. Penalty dropped and modern open data SOP established.",
                        statutory_rationale="Proactive institutional compliance and SOP creation demonstrate bona fide administration, purging penalty liability.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Direct the CPIO to refuse to attend the CIC hearing.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,
                        consequence_summary="CIC imposes personal financial penalty on CPIO and recommends disciplinary action against leadership.",
                        statutory_rationale="Defying statutory summons of the Central Information Commission constitutes gross administrative defiance.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Leadership", "Change Management", "Project Management"]
            ),
            # Carryforward branch from Option C (Confidentiality Breach)
            "q_rti_branch_confidentiality_breach": CarryforwardQuestion(
                id="q_rti_branch_confidentiality_breach",
                case_id="case_rti_microdata_appeal",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] Field supervisors report that citizens in surveyed blocks are outraged and refusing further survey participation after private information leaked. What change management and damage-control step must you take?",
                context_update="Loss of public trust in official statistical data collection.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Immediately withdraw un-anonymized files, issue a public apology affirming privacy guarantees, conduct an internal inquiry, and institute cryptographic masking for all future releases.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Public trust gradually rebuilt through transparent governance and technological safeguards.",
                        statutory_rationale="Demonstrates high ethical standards, accountability, and institutional change management.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Issue police notices to citizens threatening them with prosecution under the Statistics Act for refusing to answer future surveys.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,
                        consequence_summary="Catastrophic collapse of field survey operations and public boycott.",
                        statutory_rationale="Coercive policing in statistical data gathering ruins respondent cooperation and data quality.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Change Management", "Leadership", "Ethics"]
            )
        },
        learning_objectives=[
            "Balance citizen transparency rights under RTI Act with statutory respondent confidentiality",
            "Apply Section 10(1) Doctrine of Severability to public policy microdata",
            "Handle regulatory escalations with the Central Information Commission (CIC)"
        ]
    ),

    # Case 4: MoSPI NQAF Statistical Quality Audit (NSS Round 79)
    CaseScenario(
        id="case_mospi_nqaf_audit",
        title="NQAF Quality Audit on Unauthorized Hamlet Substitution (NSS Round 79)",
        category="Official Statistics Quality Assurance",
        document_id="doc_mospi_nqaf_audit_notice",
        document_title="MoSPI National Quality Assurance Framework (NQAF) Audit Notice on Sampling Protocol Violations",
        document_type="Notice",
        statutory_citations=[
            "Collection of Statistics Act, 2008 — Section 15",
            "UN-NQAF Quality Principle 4 (Sound Methodology)",
            "CCS (CCA) Rules, 1965 — Rule 14 / Rule 16"
        ],
        initial_context="""You are the Regional Director, NSSO Field Operations Division (Western Zone). SAQAD has served an NQAF scrutiny notice for FSU 41028 (Ratnagiri): unauthorized hamlet-group substitution, purposive household selection instead of circular systematic sampling, and implausible CAPI GPS timestamps. A 7-day show-cause clock is running.""",
        root_question_id="q_nqaf_root",
        questions={
            "q_nqaf_root": CarryforwardQuestion(
                id="q_nqaf_root",
                case_id="case_mospi_nqaf_audit",
                stage_type="root",
                prompt="The All-India release calendar is 11 days away. Headquarters informally suggests absorbing the 64 tainted schedules with post-hoc weights so the round is not delayed. How must you respond as Regional Director?",
                context_update="NQAF show-cause received; national pooling deadline approaching.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Nullify the 64 FSU 41028 schedules from the national pool, file a speaking 7-day reply, and deploy an independent re-survey team under UN-NQAF Principle 4.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Sound methodology preserved. Compromised units are excluded and independently re-enumerated.",
                        statutory_rationale="UN-NQAF Principle 4 and the Collection of Statistics Act require sound methodology; tainted units cannot enter official estimates.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Suppress the audit note, retain the substituted schedules, and meet the release date with a quiet weighting adjustment.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="False statistical statements risk Section 15 liability. Quality Council flags the FSU in the next sweep.",
                        statutory_rationale="Willful submission of false statistical statements is actionable under Section 15 of the Collection of Statistics Act, 2008.",
                        next_question_id="q_nqaf_branch_section15"
                    ),
                    CarryforwardOption(
                        option_id="C",
                        text="Immediately suspend the Field Supervisor without serving the 7-day regional explanation period prescribed in the notice.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Premature penalty without the statutory explanation window. Staff file a natural-justice objection.",
                        statutory_rationale="The scrutiny notice itself grants 7 calendar days to show cause before recommending Rule 14/16 action.",
                        next_question_id="q_nqaf_branch_notice"
                    ),
                    CarryforwardOption(
                        option_id="D",
                        text="Instruct enumerators to overwrite CAPI GPS tags so timestamps appear sequential and internally consistent.",
                        is_optimal=False,
                        is_satisfactory_terminal=False,
                        consequence_summary="Fabrication of official digital records. Vigilance and audit trails will reconstruct the overwrite.",
                        statutory_rationale="Altering geotags constitutes falsification of official records and aggravates Section 15 exposure.",
                        next_question_id="q_nqaf_branch_section15"
                    )
                ],
                behavioral_competencies=["Ethics", "Decision Making", "Project Management"]
            ),
            "q_nqaf_branch_section15": CarryforwardQuestion(
                id="q_nqaf_branch_section15",
                case_id="case_mospi_nqaf_audit",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] SAQAD has reconstructed the original CAPI logs and asks why substituted hamlets remain in the pooled file. How do you remediate before the Quality Council sitting?",
                context_update="Digital audit trail contradicts the pooled microdata.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Withdraw the tainted batch immediately, place a written nullification on file, commission independent re-listing, and submit a candid compliance note to SAQAD.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Methodology restored. Candid reporting mitigates disciplinary and statutory exposure.",
                        statutory_rationale="Prompt withdrawal of corrupted units and independent re-survey is the prescribed NQAF remediation.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Argue that monsoon access difficulties justify purposive substitution as an undocumented field discretion.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,
                        consequence_summary="Sub-optimal closure. Discretion cannot legalize unauthorized hamlet replacement.",
                        statutory_rationale="Field manuals require prior Deputy Director sanction before any hamlet-group substitution.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Ethics", "Change Management", "Leadership"]
            ),
            "q_nqaf_branch_notice": CarryforwardQuestion(
                id="q_nqaf_branch_notice",
                case_id="case_mospi_nqaf_audit",
                stage_type="carryforward_branch",
                prompt="[CARRYFORWARD FOLLOW-UP] The Supervisor cites the unexpired 7-day window and alleges bias. Headquarters asks you to regularize the personnel action. What is the correct procedural cure?",
                context_update="Natural-justice objection to premature penalty recommendation.",
                options=[
                    CarryforwardOption(
                        option_id="A",
                        text="Recall the premature suspension proposal, restart the 7-day show-cause, and keep data-quality nullification independent of the personnel file.",
                        is_optimal=True,
                        is_satisfactory_terminal=True,
                        consequence_summary="Due process restored while still protecting the national sample from corrupted schedules.",
                        statutory_rationale="Personnel action under CCS (CCA) Rules must follow notice; data nullification is a separate quality decision.",
                        next_question_id=None
                    ),
                    CarryforwardOption(
                        option_id="B",
                        text="Confirm the suspension in writing so field staff 'learn a lesson' before the explanation is received.",
                        is_optimal=False,
                        is_satisfactory_terminal=True,
                        consequence_summary="Personnel order remains vulnerable to appeal; quality issues are conflated with punishment.",
                        statutory_rationale="Penalty without considering the explanation vitiates Rule 16/14 proceedings.",
                        next_question_id=None
                    )
                ],
                behavioral_competencies=["Leadership", "Ethics", "Decision Making"]
            )
        },
        learning_objectives=[
            "Protect official estimates by nullifying corrupted sample units",
            "Apply UN-NQAF Principle 4 and Collection of Statistics Act Section 15",
            "Separate data-quality remediation from fair disciplinary process"
        ]
    )
]

GENERATED_CASES: Dict[str, CaseScenario] = {}


def get_all_cases() -> List[CaseScenario]:
    return PRE_SEEDED_CASES + list(GENERATED_CASES.values())


def get_case_by_id(case_id: str) -> Optional[CaseScenario]:
    for case in PRE_SEEDED_CASES:
        if case.id == case_id:
            return case
    return GENERATED_CASES.get(case_id)


def register_generated_case(case: CaseScenario) -> None:
    GENERATED_CASES[case.id] = case

def generate_case_from_document(req: CaseGenerationRequest) -> CaseScenario:
    """
    Generates a new CaseScenario from raw government notice/form text.
    Uses LLM (Gemini/OpenAI) if available, with robust deterministic fallback.
    """
    metadata = NoticeExtractor.extract_metadata(req.raw_text)
    doc_id = f"custom_doc_{uuid.uuid4().hex[:8]}"
    case_id = f"custom_case_{uuid.uuid4().hex[:8]}"

    # Check for LLM generation
    if settings.GOOGLE_API_KEY or settings.OPENAI_API_KEY:
        try:
            from langchain_core.messages import HumanMessage
            prompt = f"""You are an expert Government of India civil-service training curriculum designer for iGot Karmayogi.
Based on the following official government document:
Title: {req.document_title}
Type: {req.document_type}
Issuing Authority: {req.issuing_authority}
Statutory Reference: {req.statutory_reference}
Content:
{req.raw_text[:2500]}

Generate an authentic carryforward branching case scenario with:
1. Root question posing an administrative decision dilemma.
2. Option A: Optimal action following due process.
3. Option B: A sub-optimal shortcut/mistake that leads to a carryforward follow-up question.
4. Consequential follow-up question confronting the officer with the fallout of Option B, offering an optimal corrective path and a flawed path.

Output strictly valid JSON conforming to:
{{
  "title": "...",
  "category": "Administrative Governance",
  "initial_context": "...",
  "root_question": {{
     "prompt": "...",
     "options": [
        {{"option_id": "A", "text": "...", "is_optimal": true, "is_satisfactory_terminal": true, "consequence_summary": "...", "statutory_rationale": "..."}},
        {{"option_id": "B", "text": "...", "is_optimal": false, "is_satisfactory_terminal": false, "consequence_summary": "...", "statutory_rationale": "...", "next_question_id": "q_branch_1"}},
        {{"option_id": "C", "text": "...", "is_optimal": false, "is_satisfactory_terminal": false, "consequence_summary": "...", "statutory_rationale": "...", "next_question_id": "q_branch_1"}}
     ]
  }},
  "branch_question": {{
     "id": "q_branch_1",
     "prompt": "[CARRYFORWARD FOLLOW-UP] ...",
     "options": [
        {{"option_id": "A", "text": "...", "is_optimal": true, "is_satisfactory_terminal": true, "consequence_summary": "...", "statutory_rationale": "..."}},
        {{"option_id": "B", "text": "...", "is_optimal": false, "is_satisfactory_terminal": true, "consequence_summary": "...", "statutory_rationale": "..."}}
     ]
  }},
  "learning_objectives": ["..."]
}}"""
            res_content = ""
            if settings.GOOGLE_API_KEY:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY, temperature=0.2)
                res = llm.invoke([HumanMessage(content=prompt)])
                res_content = res.content
            elif settings.OPENAI_API_KEY:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY, temperature=0.2)
                res = llm.invoke([HumanMessage(content=prompt)])
                res_content = res.content

            # Parse JSON
            cleaned = res_content.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(cleaned)

            root_opts = [CarryforwardOption(**opt) for opt in parsed["root_question"]["options"]]
            branch_opts = [CarryforwardOption(**opt) for opt in parsed["branch_question"]["options"]]

            questions = {
                "q_root": CarryforwardQuestion(
                    id="q_root",
                    case_id=case_id,
                    stage_type="root",
                    prompt=parsed["root_question"]["prompt"],
                    options=root_opts,
                    behavioral_competencies=["Ethics", "Decision Making", "Leadership"]
                ),
                parsed["branch_question"]["id"]: CarryforwardQuestion(
                    id=parsed["branch_question"]["id"],
                    case_id=case_id,
                    stage_type="carryforward_branch",
                    prompt=parsed["branch_question"]["prompt"],
                    options=branch_opts,
                    behavioral_competencies=["Decision Making", "Change Management"]
                )
            }

            llm_case = CaseScenario(
                id=case_id,
                title=parsed.get("title", req.document_title),
                category="Custom Administrative Scenario",
                document_id=doc_id,
                document_title=req.document_title,
                document_type=req.document_type,
                statutory_citations=metadata["statutory_citations"],
                initial_context=parsed.get("initial_context", metadata["summary_snippet"]),
                root_question_id="q_root",
                questions=questions,
                learning_objectives=parsed.get("learning_objectives", ["Enforce statutory due process"])
            )
            register_generated_case(llm_case)
            return llm_case
        except Exception as e:
            print(f"LLM case generation fallback: {e}")

    # Deterministic fallback generator
    root_opts = [
        CarryforwardOption(
            option_id="A",
            text=f"Initiate formal inquiry under {metadata['statutory_citations'][0] if metadata['statutory_citations'] else 'Rules'}, giving reasonable notice and maintaining transparent records.",
            is_optimal=True,
            is_satisfactory_terminal=True,
            consequence_summary="Procedural propriety preserved. Safeguards government interest and natural justice.",
            statutory_rationale="Statutory frameworks require adherence to documented procedures and fair opportunity of representation.",
            next_question_id=None
        ),
        CarryforwardOption(
            option_id="B",
            text="Take immediate summary action without formal notice to swiftly resolve the administrative backlog.",
            is_optimal=False,
            is_satisfactory_terminal=False,
            consequence_summary="Procedural error committed. Summary action without notice provokes statutory challenge.",
            statutory_rationale="Bypassing statutory notice periods violates the principles of natural justice.",
            next_question_id="q_branch_remediation"
        ),
        CarryforwardOption(
            option_id="C",
            text="Defer decision indefinitely until an external authority intervenes.",
            is_optimal=False,
            is_satisfactory_terminal=False,
            consequence_summary="Administrative paralysis leading to escalation.",
            statutory_rationale="Public authorities have an affirmative legal duty to act within reasonable timeframes.",
            next_question_id="q_branch_remediation"
        )
    ]

    branch_opts = [
        CarryforwardOption(
            option_id="A",
            text="Issue a corrective corrigendum or show-cause notice, granting the statutory response period before taking action.",
            is_optimal=True,
            is_satisfactory_terminal=True,
            consequence_summary="Procedural defect cured under civil service regulations.",
            statutory_rationale="Administrative authorities can cure procedural lacunae by issuing a formal notice with reasons.",
            next_question_id=None
        ),
        CarryforwardOption(
            option_id="B",
            text="Reaffirm the summary decision despite procedural objections.",
            is_optimal=False,
            is_satisfactory_terminal=True,
            consequence_summary="Action remains legally unsustainable.",
            statutory_rationale="Persistent refusal to cure defects vitiates the administrative order.",
            next_question_id=None
        )
    ]

    questions = {
        "q_root": CarryforwardQuestion(
            id="q_root",
            case_id=case_id,
            stage_type="root",
            prompt=f"Regarding the notice '{req.document_title}', what is your primary administrative responsibility under {metadata['statutory_citations'][0] if metadata['statutory_citations'] else 'established procedures'}?",
            options=root_opts,
            behavioral_competencies=["Ethics", "Decision Making", "Leadership"]
        ),
        "q_branch_remediation": CarryforwardQuestion(
            id="q_branch_remediation",
            case_id=case_id,
            stage_type="carryforward_branch",
            prompt="[CARRYFORWARD FOLLOW-UP] A formal legal objection has been submitted citing violation of due process and lack of notice. How do you rectify this administrative proceeding?",
            options=branch_opts,
            behavioral_competencies=["Decision Making", "Change Management"]
        )
    }

    fallback_case = CaseScenario(
        id=case_id,
        title=f"Case Study: {req.document_title}",
        category="Administrative Compliance",
        document_id=doc_id,
        document_title=req.document_title,
        document_type=req.document_type,
        statutory_citations=metadata["statutory_citations"],
        initial_context=f"Administrative scenario extracted from {req.document_title}. Review the notice provisions and resolve the operational conflict.",
        root_question_id="q_root",
        questions=questions,
        learning_objectives=[
            "Exercise statutory due diligence in administrative proceedings",
            "Identify and rectify procedural vulnerabilities",
            "Uphold public ethics and sound administrative decision making"
        ]
    )
    register_generated_case(fallback_case)
    return fallback_case
