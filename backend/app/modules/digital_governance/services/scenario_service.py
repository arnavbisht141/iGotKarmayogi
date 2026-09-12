import uuid
from typing import Dict, List, Optional
from app.modules.digital_governance.schemas import (
    CaseScenario, ScenarioQuestion, ScenarioOption, ScenarioListItem,
    ScenarioSessionResponse, ScenarioAnswerResponse, ScenarioSummary,
    DecisionNodeLog
)

class ScenarioRepository:
    """In-memory authoritative store for Digital Governance tabletop case scenarios."""
    
    _scenarios: Dict[str, CaseScenario] = {}

    @classmethod
    def initialize_scenarios(cls):
        if cls._scenarios:
            return

        # ── SCENARIO 1: CYBERSECURITY ─────────────────────────────────────────
        s1 = CaseScenario(
            id="dg-sec-01-ransomware-treasury",
            title="Operation Vajra: Critical Ransomware Outbreak on State Treasury Payment Gateway",
            domain="Cybersecurity",
            ministry="Department of Expenditure & National Informatics Centre (NIC)",
            statutory_framework=[
                "Information Technology Act, 2000 (Section 70B)",
                "CERT-In Cybersecurity Directions (28 April 2022)",
                "Indian Evidence Act (Section 65B / Bharatiya Sakshya Adhiniyam)"
            ],
            difficulty="intermediate",
            estimated_minutes=15,
            initial_context=(
                "At 02:15 AM on a Saturday, the automated monitoring system of the State Treasury Payment Gateway (PFMS gateway node) "
                "alerts the on-call Security Operations Center (SOC) team. Database volumes on `TREASURY-DB-01` are experiencing rapid file "
                "modifications appending the `.encryp` extension. Continuous outbound command-and-control (C2) beaconing to an unassigned foreign IP "
                "is observed on port 4444. Citizen pension disbursements of ₹180 crore are scheduled for processing in 6 hours."
            ),
            root_question_id="s1_q1_containment",
            learning_objectives=[
                "Enforce emergency network isolation without destroying volatile memory artifacts required for legal evidence",
                "Comply strictly with CERT-In's mandatory 6-hour incident reporting window under Section 70B",
                "Execute clean recovery from offline backups and preserve forensic chain of custody under Section 65B"
            ],
            questions={
                "s1_q1_containment": ScenarioQuestion(
                    id="s1_q1_containment",
                    scenario_id="dg-sec-01-ransomware-treasury",
                    stage_title="Stage 1: Emergency Threat Containment",
                    prompt=(
                        "Ransomware encryption is actively propagating across the subnet. System administrators recommend immediately "
                        "pulling the physical power plugs on all infected servers to stop encryption instantly. As the Incident Commander, "
                        "what is your direct operational order?"
                    ),
                    governance_pillar="Cybersecurity",
                    options=[
                        ScenarioOption(
                            option_id="s1_q1_opt_a",
                            text="Order immediate network isolation at the switch / firewall level (disconnect network cables / isolate VLAN) while keeping servers powered on.",
                            is_optimal=True,
                            consequence_summary="Network propagation is halted instantly. Host power remains on, preserving volatile RAM containing encryption keys, socket states, and adversary process injections.",
                            statutory_rationale="Forensic integrity under Section 65B of the Indian Evidence Act requires preserving volatile memory. Hard power-off destroys volatile RAM, preventing key recovery and adversary identification.",
                            next_question_id="s1_q2_certin",
                            compliance_delta=30
                        ),
                        ScenarioOption(
                            option_id="s1_q1_opt_b",
                            text="Approve pulling the physical power plugs immediately to prevent further disk writes.",
                            is_optimal=False,
                            consequence_summary="Disk writes stop, but all volatile RAM contents are completely wiped. In-memory decryption keys and running malware artifacts are permanently lost.",
                            statutory_rationale="Violates Digital Forensic Standard Operating Procedures mandated by CERT-In and destroys admissible electronic evidence under Section 65B.",
                            next_question_id="s1_q2_certin",
                            compliance_delta=-20
                        ),
                        ScenarioOption(
                            option_id="s1_q1_opt_c",
                            text="Take no immediate action and wait for the senior director to arrive at 09:00 AM.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Ransomware completely encrypts the entire departmental SAN array and spreads to central PFMS bridges. Total service collapse ensues.",
                            statutory_rationale="Gross dereliction of statutory duty under Section 70B of the IT Act, leading to catastrophic infrastructure loss and disciplinary sanction.",
                            compliance_delta=-50
                        )
                    ]
                ),
                "s1_q2_certin": ScenarioQuestion(
                    id="s1_q2_certin",
                    scenario_id="dg-sec-01-ransomware-treasury",
                    stage_title="Stage 2: Statutory CERT-In Incident Reporting",
                    context_update="Network isolation is in place. The time is now 04:30 AM (2 hours and 15 minutes since initial anomaly detection).",
                    prompt=(
                        "The internal team is still analyzing the ransomware variant and has not yet determined the full root cause. "
                        "The departmental public relations officer suggests postponing any external notification until a full investigation report is completed next week. "
                        "What is the legally compliant decision?"
                    ),
                    governance_pillar="Cybersecurity",
                    options=[
                        ScenarioOption(
                            option_id="s1_q2_opt_a",
                            text="Submit an initial cyber incident report (Annexure-I) to CERT-In Incident Response Desk immediately within the mandatory 6-hour window, providing details known so far.",
                            is_optimal=True,
                            consequence_summary="CERT-In receives timely notification within 4 hours. CERT-In's National Cyber Coordination Centre assists with threat signatures and IOC tracking.",
                            statutory_rationale="Section 70B(6) of the Information Technology Act and CERT-In directions strictly mandate incident reporting within six (6) hours. Submitting initial details complies with statutory obligations.",
                            next_question_id="s1_q3_recovery",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s1_q2_opt_b",
                            text="Wait until internal forensic analysis completes in 3 days before sending any communication to CERT-In.",
                            is_optimal=False,
                            consequence_summary="The 6-hour statutory window lapses. CERT-In detects external indicators from telecom telemetry and initiates compliance proceedings against the department.",
                            statutory_rationale="Direct violation of Section 70B(7) of the IT Act 2000, punishable with imprisonment up to 1 year or monetary fines.",
                            next_question_id="s1_q3_recovery",
                            compliance_delta=-30
                        )
                    ]
                ),
                "s1_q3_recovery": ScenarioQuestion(
                    id="s1_q3_recovery",
                    scenario_id="dg-sec-01-ransomware-treasury",
                    stage_title="Stage 3: Admissible Recovery & Evidence Custody",
                    context_update="A ransom demand of ₹50 lakh in cryptocurrency is displayed on the console. Offline immutable air-gapped backups from 24 hours ago are verified intact.",
                    prompt=(
                        "How should the department proceed with restoration and legal prosecution?"
                    ),
                    governance_pillar="Cybersecurity",
                    options=[
                        ScenarioOption(
                            option_id="s1_q3_opt_a",
                            text="Acquire full bitstream forensic disk and RAM images with cryptographic SHA-256 hashes, prepare Section 65B Certificate, refuse extortion, and restore from air-gapped backups.",
                            is_optimal=True,
                            is_terminal=True,
                            consequence_summary="Treasury services are fully restored within 4 hours without financial loss. Digital evidence is court-admissible, enabling law enforcement prosecution.",
                            statutory_rationale="Full compliance with Section 65B of the Indian Evidence Act and National Cyber Security Guidelines. Government policy strictly prohibits paying ransoms.",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s1_q3_opt_b",
                            text="Negotiate and pay the ransom from secret service funds to obtain the decryption key faster.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Ransom is paid; adversary provides a corrupt decryption key. Public funds are misappropriated, triggering a CAG audit and CBI inquiry.",
                            statutory_rationale="Illegal expenditure of public treasury funds and violation of Government Financial Rules (GFR) 2017.",
                            compliance_delta=-50
                        )
                    ]
                )
            }
        )

        # ── SCENARIO 2: DATA PRIVACY (DPDP ACT 2023) ──────────────────────────
        s2 = CaseScenario(
            id="dg-priv-02-dbt-cloud-breach",
            title="Operation Raksha: Aadhaar-Linked DBT Citizen Pension Registry Exposure on Public Cloud",
            domain="Data Privacy",
            ministry="Ministry of Rural Development & State Social Welfare Directorate",
            statutory_framework=[
                "Digital Personal Data Protection Act, 2023 (Sections 8, 9, 10 & Schedule)",
                "Aadhaar (Targeted Delivery of Financial and Other Subsidies) Act, 2016 (Section 29)",
                "Information Technology (Reasonable Security Practices) Rules"
            ],
            difficulty="intermediate",
            estimated_minutes=15,
            initial_context=(
                "A cybersecurity researcher informs the Departmental Computer Emergency Team via responsible disclosure that a publicly accessible "
                "cloud storage bucket belonging to the State Social Welfare Directorate contains 75,000 unredacted citizen records. "
                "The records include citizen full names, unmasked 12-digit Aadhaar numbers, bank account details, disability status, and monthly pension allocations."
            ),
            root_question_id="s2_q1_access_containment",
            learning_objectives=[
                "Exercise Data Fiduciary responsibilities under Section 8 of the DPDP Act 2023",
                "Execute mandatory notification to the Data Protection Board of India and affected citizens",
                "Implement Aadhaar masking and Significant Data Fiduciary compliance controls"
            ],
            questions={
                "s2_q1_access_containment": ScenarioQuestion(
                    id="s2_q1_access_containment",
                    scenario_id="dg-priv-02-dbt-cloud-breach",
                    stage_title="Stage 1: Immediate Triage & Data Securing",
                    prompt=(
                        "Upon receiving and validating the researcher's report, what is the immediate first action the Data Fiduciary must execute?"
                    ),
                    governance_pillar="Data Privacy",
                    options=[
                        ScenarioOption(
                            option_id="s2_q1_opt_a",
                            text="Immediately modify the cloud bucket access policy to block public access, rotate service credentials, and preserve cloud access logs.",
                            is_optimal=True,
                            consequence_summary="Public exposure is plugged within minutes. Cloud logs are preserved to identify which external entities accessed or downloaded the files.",
                            statutory_rationale="Fulfills the core obligation under Section 8(5) of the DPDP Act 2023 requiring reasonable security safeguards to protect personal data in possession.",
                            next_question_id="s2_q2_dpbi_notice",
                            compliance_delta=30
                        ),
                        ScenarioOption(
                            option_id="s2_q1_opt_b",
                            text="Send a legal threat letter to the researcher demanding immediate silence and ignore the cloud bucket settings.",
                            is_optimal=False,
                            consequence_summary="The cloud bucket remains open to threat actors. The researcher publishes proof on social media, sparking national public outcry.",
                            statutory_rationale="Flagrant disregard of Section 8 security duties, exposing the department to peak statutory penalties up to ₹250 crore.",
                            next_question_id="s2_q2_dpbi_notice",
                            compliance_delta=-35
                        )
                    ]
                ),
                "s2_q2_dpbi_notice": ScenarioQuestion(
                    id="s2_q2_dpbi_notice",
                    scenario_id="dg-priv-02-dbt-cloud-breach",
                    stage_title="Stage 2: Breach Notification to DPBI & Data Principals",
                    context_update="Cloud access logs confirm that 18 distinct external IP addresses downloaded portions of the citizen registry during the 48-hour exposure window.",
                    prompt=(
                        "Under Section 8(6) of the DPDP Act 2023, what is the mandatory reporting obligation regarding the confirmed breach?"
                    ),
                    governance_pillar="Data Privacy",
                    options=[
                        ScenarioOption(
                            option_id="s2_q2_opt_a",
                            text="Give formal notice of the personal data breach to the Data Protection Board of India and directly notify each affected citizen (Data Principal) with remedial safety advice.",
                            is_optimal=True,
                            consequence_summary="The Board acknowledges proactive statutory compliance. Citizens are alerted to monitor their bank accounts and enable biometric locking on Aadhaar.",
                            statutory_rationale="Section 8(6) of the DPDP Act mandates dual notification: first to the Data Protection Board of India, and second to each affected Data Principal.",
                            next_question_id="s2_q3_sdf_hardening",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s2_q2_opt_b",
                            text="Notify only internal departmental leadership and classify the incident as a confidential administrative matter.",
                            is_optimal=False,
                            consequence_summary="Failure to notify is detected by the Board. The Data Protection Board initiates suo-motu proceedings with penalty proceedings up to ₹200 crore.",
                            statutory_rationale="Section 8(6) violation; failure to report personal data breach is an independent offense under the Schedule to the DPDP Act 2023.",
                            next_question_id="s2_q3_sdf_hardening",
                            compliance_delta=-30
                        )
                    ]
                ),
                "s2_q3_sdf_hardening": ScenarioQuestion(
                    id="s2_q3_sdf_hardening",
                    scenario_id="dg-priv-02-dbt-cloud-breach",
                    stage_title="Stage 3: Significant Data Fiduciary Architectural Remediation",
                    context_update="Due to the volume and sensitivity of holding records of over 10 million citizens statewide, the directorate is classified as a Significant Data Fiduciary (SDF).",
                    prompt=(
                        "What institutional architecture must now be deployed to achieve full legal compliance?"
                    ),
                    governance_pillar="Data Privacy",
                    options=[
                        ScenarioOption(
                            option_id="s2_q3_opt_a",
                            text="Appoint an India-based Data Protection Officer (DPO), engage an independent Data Auditor, conduct periodic DPIAs, and implement mandatory Aadhaar masking.",
                            is_optimal=True,
                            is_terminal=True,
                            consequence_summary="Comprehensive privacy governance established. Plaintext Aadhaar numbers are replaced with Virtual IDs (VID), rendering future leaks harmless.",
                            statutory_rationale="Strict compliance with Section 10 of DPDP Act 2023 and Section 29 of the Aadhaar Act 2016 prohibiting plain-text Aadhaar publishing.",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s2_q3_opt_b",
                            text="Abolish electronic databases and return to manual paper ledgers in district offices.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Direct conflict with Government Digital India objectives; welfare delivery stalls across the entire state.",
                            statutory_rationale="Violates e-Governance policy mandates under the Information Technology Act and National Digital Mission.",
                            compliance_delta=-30
                        )
                    ]
                )
            }
        )

        # ── SCENARIO 3: DIGITAL SIGNATURES & PKI ──────────────────────────────
        s3 = CaseScenario(
            id="dg-pki-03-gem-tender-dispute",
            title="Operation Mudra: Disputed High-Value e-Procurement Tender & DSC Token Revocation",
            domain="Digital Signatures",
            ministry="Government e-Marketplace (GeM) & Ministry of Commerce and Industry",
            statutory_framework=[
                "Information Technology Act, 2000 (Sections 3, 3A, 5, 18 & 35)",
                "Controller of Certifying Authorities (CCA) Guidelines",
                "Indian Evidence Act (Section 65B)"
            ],
            difficulty="intermediate",
            estimated_minutes=15,
            initial_context=(
                "At 16:59:45 PM on tender submission day, an electronic bid for a ₹45 crore medical supply contract is signed and submitted "
                "via the e-Procurement portal using the Class 3 Digital Signature Certificate (DSC) of Contractor M/s MedTech Solutions. "
                "The following morning, after financial bids are opened and MedTech is named L1 bidder with aggressive rates, the contractor submits "
                "a dispute claiming their authorized director's USB DSC token was stolen by an ex-employee and the bid is invalid."
            ),
            root_question_id="s3_q1_crl_check",
            learning_objectives=[
                "Verify asymmetric cryptographic validity and timestamp non-repudiation under IT Act Sections 3 & 3A",
                "Inspect Online Certificate Status Protocol (OCSP) and Certificate Revocation Lists (CRL)",
                "Produce admissible electronic evidence certificates under Section 65B of the Indian Evidence Act"
            ],
            questions={
                "s3_q1_crl_check": ScenarioQuestion(
                    id="s3_q1_crl_check",
                    scenario_id="dg-pki-03-gem-tender-dispute",
                    stage_title="Stage 1: Cryptographic Timestamp & Revocation Verification",
                    prompt=(
                        "As the Tender Adjudication Committee Officer, what is the essential technical verification step to determine bid validity?"
                    ),
                    governance_pillar="Digital Signatures",
                    options=[
                        ScenarioOption(
                            option_id="s3_q1_opt_a",
                            text="Inspect the e-tender signing cryptographic timestamp, CA OCSP responder logs, and the Certificate Revocation List (CRL) at the exact second of bid submission.",
                            is_optimal=True,
                            consequence_summary="Forensic log confirms the DSC was fully valid and active at 16:59:45 PM. The revocation request was only logged by the contractor at 09:30 AM the next day.",
                            statutory_rationale="Under Section 35 of the IT Act and CCA standards, a digital signature remains legally valid and binding on the subscriber until formal revocation is registered with the licensed CA.",
                            next_question_id="s3_q2_non_repudiation",
                            compliance_delta=30
                        ),
                        ScenarioOption(
                            option_id="s3_q1_opt_b",
                            text="Accept the contractor's verbal claim immediately and cancel the tender.",
                            is_optimal=False,
                            consequence_summary="Tender cancellation causes critical drug shortages in state hospitals and invites litigation from other legitimate bidders.",
                            statutory_rationale="Violates Central Vigilance Commission (CVC) public procurement guidelines and IT Act non-repudiation principles.",
                            next_question_id="s3_q2_non_repudiation",
                            compliance_delta=-30
                        )
                    ]
                ),
                "s3_q2_non_repudiation": ScenarioQuestion(
                    id="s3_q2_non_repudiation",
                    scenario_id="dg-pki-03-gem-tender-dispute",
                    stage_title="Stage 2: Adjudication of Non-Repudiation",
                    context_update="The contractor insists they are not bound because the token was out of their physical possession, citing breach of contract principles.",
                    prompt=(
                        "How does the IT Act 2000 govern subscriber responsibility over private keys in Class 3 DSC tokens?"
                    ),
                    governance_pillar="Digital Signatures",
                    options=[
                        ScenarioOption(
                            option_id="s3_q2_opt_a",
                            text="Hold the contractor strictly liable under Section 42 of the IT Act: the subscriber is statutorily responsible for retaining exclusive custody of the private key until revocation.",
                            is_optimal=True,
                            consequence_summary="The committee upholds the bid as legally binding. The contractor is ordered to execute performance guarantees or forfeit their earnest money deposit (EMD).",
                            statutory_rationale="Section 42 of the Information Technology Act 2000 mandates that the subscriber shall exercise reasonable care to retain control of the private key corresponding to the public key listed in the Digital Signature Certificate.",
                            next_question_id="s3_q3_court_filing",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s3_q2_opt_b",
                            text="Agree with the contractor and release their earnest money deposit without any penalty.",
                            is_optimal=False,
                            consequence_summary="Sets a catastrophic precedent where bidders retract bids at will whenever competitor prices are revealed.",
                            statutory_rationale="Direct breach of GFR 2017 Rule 170 and Section 5 of the IT Act giving legal equivalence to electronic signatures.",
                            next_question_id="s3_q3_court_filing",
                            compliance_delta=-35
                        )
                    ]
                ),
                "s3_q3_court_filing": ScenarioQuestion(
                    id="s3_q3_court_filing",
                    scenario_id="dg-pki-03-gem-tender-dispute",
                    stage_title="Stage 3: Judicial Defense & Section 65B Certification",
                    context_update="The contractor files an emergency writ petition in the High Court seeking a stay on tender award.",
                    prompt=(
                        "What documentation must the government standing counsel submit to guarantee admissibility of the electronic tender logs?"
                    ),
                    governance_pillar="Digital Signatures",
                    options=[
                        ScenarioOption(
                            option_id="s3_q3_opt_a",
                            text="Submit an official Certificate under Section 65B of the Evidence Act certifying server operational integrity, accompanied by cryptographic SHA-256 hash digests and CA audit trails.",
                            is_optimal=True,
                            is_terminal=True,
                            consequence_summary="High Court dismisses the contractor's petition with costs, citing complete cryptographic proof of authenticity and Section 65B compliance.",
                            statutory_rationale="Section 65B of the Indian Evidence Act establishes that electronic records accompanied by a proper certificate are admissible as primary proof without requiring physical device seizure.",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s3_q3_opt_b",
                            text="Submit a casual photocopied screenshot of the website without any system certificate.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Court rejects the evidence as inadmissible hearsay under Supreme Court precedents (Anvar P.V. v. P.K. Basheer). Stay order is granted.",
                            statutory_rationale="Violates mandatory Section 65B conditions: secondary electronic evidence without an official certificate is legally inadmissible.",
                            compliance_delta=-40
                        )
                    ]
                )
            }
        )

        # ── SCENARIO 4: GOVERNMENT CLOUD (MEGHRAJ) ───────────────────────────
        s4 = CaseScenario(
            id="dg-cloud-04-meghraj-sovereignty",
            title="Operation Megh: Unauthorized Foreign Region Workload Migration & Sovereign Cloud Audit",
            domain="Government Cloud",
            ministry="Ministry of Electronics & Information Technology (MeitY) & State Data Centre (SDC)",
            statutory_framework=[
                "MeghRaj (GI Cloud) Strategic Framework",
                "MeitY Guidelines for Cloud Service Providers (CSPs)",
                "STQC Cloud Security Auditing Matrix (ISO 27017 / 27018)"
            ],
            difficulty="intermediate",
            estimated_minutes=15,
            initial_context=(
                "During a scheduled performance review of the State Integrated Land Records System ('Bhoomi Portal'), "
                "the state cybersecurity auditor notices that a system integrator (SI) deployed automated load-balancing containers "
                "into an overseas commercial data center region to manage festival peak traffic. Live land ownership titles and biometric deed records "
                "are being processed through unempaneled foreign servers."
            ),
            root_question_id="s4_q1_sovereign_quarantine",
            learning_objectives=[
                "Enforce mandatory sovereign data localization within the territorial boundaries of India",
                "Apply STQC audit and MeitY empanelment requirements for Government Cloud workloads",
                "Safeguard Government Community Cloud (GCC) isolation against unauthorized cloud spillover"
            ],
            questions={
                "s4_q1_sovereign_quarantine": ScenarioQuestion(
                    id="s4_q1_sovereign_quarantine",
                    scenario_id="dg-cloud-04-meghraj-sovereignty",
                    stage_title="Stage 1: Emergency Traffic Rerouting & Data Quarantine",
                    prompt=(
                        "What is the immediate operational command the State Chief Information Security Officer (CISO) must issue?"
                    ),
                    governance_pillar="Government Cloud",
                    options=[
                        ScenarioOption(
                            option_id="s4_q1_opt_a",
                            text="Immediately cut traffic routing to foreign instances, redirect workloads to domestic MeitY-empaneled GCC instances, and quarantine data streams on foreign hosts.",
                            is_optimal=True,
                            consequence_summary="Cross-border data transit ceases immediately. Workloads seamlessly failover to sovereign Indian cloud infrastructure.",
                            statutory_rationale="MeitY Cloud adoption guidelines strictly mandate that all government data and processing must reside exclusively within the territory of India.",
                            next_question_id="s4_q2_stqc_enforcement",
                            compliance_delta=30
                        ),
                        ScenarioOption(
                            option_id="s4_q1_opt_b",
                            text="Allow the foreign instances to complete the month to minimize compute costs.",
                            is_optimal=False,
                            consequence_summary="Foreign jurisdiction authorities subject the cloud host to extraterritorial subpoena, accessing sensitive citizen land ownership records.",
                            statutory_rationale="Critical violation of national data sovereignty and Government Cloud adoption policy.",
                            next_question_id="s4_q2_stqc_enforcement",
                            compliance_delta=-35
                        )
                    ]
                ),
                "s4_q2_stqc_enforcement": ScenarioQuestion(
                    id="s4_q2_stqc_enforcement",
                    scenario_id="dg-cloud-04-meghraj-sovereignty",
                    stage_title="Stage 2: Contractor Empanelment & Compliance Audit",
                    context_update="The vendor argues that the cloud provider holds international SOC 2 certifications and claims no Indian rules were broken.",
                    prompt=(
                        "How should the department evaluate the vendor's legal and technical compliance defense?"
                    ),
                    governance_pillar="Government Cloud",
                    options=[
                        ScenarioOption(
                            option_id="s4_q2_opt_a",
                            text="Reject the defense: affirm that only STQC-audited and MeitY-empaneled Cloud Service Providers with facilities inside India are legally authorized for public sector workloads.",
                            is_optimal=True,
                            consequence_summary="The department issues a formal show-cause notice and imposes contractual liquidated damages for willful policy violation.",
                            statutory_rationale="Under MeghRaj guidelines, international certifications do not substitute for mandatory STQC security auditing and MeitY empanelment.",
                            next_question_id="s4_q3_cryptographic_purge",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s4_q2_opt_b",
                            text="Accept the vendor's claim and retroactively grant permission for foreign cloud hosting.",
                            is_optimal=False,
                            consequence_summary="Triggers a national security audit by the Ministry of Home Affairs; senior officials face disciplinary proceedings.",
                            statutory_rationale="Ultra vires administrative action violating cabinet-approved cloud security policies.",
                            next_question_id="s4_q3_cryptographic_purge",
                            compliance_delta=-40
                        )
                    ]
                ),
                "s4_q3_cryptographic_purge": ScenarioQuestion(
                    id="s4_q3_cryptographic_purge",
                    scenario_id="dg-cloud-04-meghraj-sovereignty",
                    stage_title="Stage 3: Verification of Data Sanitation & Sanitized Purge",
                    context_update="Foreign instances have been halted. Residual cached citizen records may remain on disk blocks in the overseas data center.",
                    prompt=(
                        "What is the final technical verification required to guarantee complete data sanitation?"
                    ),
                    governance_pillar="Government Cloud",
                    options=[
                        ScenarioOption(
                            option_id="s4_q3_opt_a",
                            text="Demand cryptographically verifiable secure erasure certificates (NIST SP 800-88 compliance) and complete sanitization logs attested by the cloud provider's certified auditor.",
                            is_optimal=True,
                            is_terminal=True,
                            consequence_summary="Audited cryptographic sanitization confirms no orphaned government records remain on overseas hardware. Full compliance restored.",
                            statutory_rationale="Adheres to MeitY guidelines on data sanitization and exit management protocols for cloud service termination.",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s4_q3_opt_b",
                            text="Rely on an informal verbal promise over telephone from the contractor's local sales agent.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Residual data is later discovered by security researchers on decommissioned disks, leading to regulatory penalties under DPDP Act.",
                            statutory_rationale="Gross non-compliance with ISO 27001 / ISO 27018 asset sanitization standards.",
                            compliance_delta=-35
                        )
                    ]
                )
            }
        )

        # ── SCENARIO 5: DIGITAL PUBLIC INFRASTRUCTURE (DPI) ───────────────────
        s5 = CaseScenario(
            id="dg-dpi-05-apisetu-replay-attack",
            title="Operation Setu: High-Volume Replay Attack on Citizen e-KYC & API Setu Highway",
            domain="Digital Public Infrastructure",
            ministry="Unique Identification Authority of India (UIDAI) & National e-Governance Division (NeGD)",
            statutory_framework=[
                "Aadhaar (Authentication and Offline Verification) Regulations",
                "API Setu (OpenForge) Interoperability Guidelines",
                "Information Technology Act, 2000 (Section 43 & 66)"
            ],
            difficulty="intermediate",
            estimated_minutes=15,
            initial_context=(
                "API Setu gateway telemetry shows an abnormal traffic spike: 65,000 requests per second targeting the state citizen scholarship "
                "verification gateway. Attackers appear to be replaying captured valid e-KYC response packets from legitimate beneficiaries to trigger "
                "unauthorized scholarship disbursement approvals across fake beneficiary bank accounts."
            ),
            root_question_id="s5_q1_nonce_enforcement",
            learning_objectives=[
                "Detect and mitigate cryptographic replay attacks on citizen authentication APIs",
                "Enforce strict timestamp windows and single-use cryptographic nonces",
                "Maintain citizen public service availability while enforcing rate limits on DPI endpoints"
            ],
            questions={
                "s5_q1_nonce_enforcement": ScenarioQuestion(
                    id="s5_q1_nonce_enforcement",
                    scenario_id="dg-dpi-05-apisetu-replay-attack",
                    stage_title="Stage 1: Cryptographic Nonce & Timestamp Verification",
                    prompt=(
                        "What is the immediate technical defense at the API Gateway layer to neutralize the replayed authentication packets?"
                    ),
                    governance_pillar="Digital Public Infrastructure",
                    options=[
                        ScenarioOption(
                            option_id="s5_q1_opt_a",
                            text="Enforce strict cryptographic nonce validation and restrict clock-skew tolerance to under 300 milliseconds, dropping all previously seen transaction tokens.",
                            is_optimal=True,
                            consequence_summary="All 65,000 replayed requests are dropped immediately at the gateway boundary without reaching back-end database servers.",
                            statutory_rationale="Complies with UIDAI Authentication Security Standards and API Setu specifications requiring single-use nonces and mutual TLS authentication.",
                            next_question_id="s5_q2_rate_limiting",
                            compliance_delta=30
                        ),
                        ScenarioOption(
                            option_id="s5_q1_opt_b",
                            text="Shut down the entire API gateway service statewide, blocking all citizen scholarship applications.",
                            is_optimal=False,
                            consequence_summary="Millions of genuine students across the state are locked out of scholarship deadlines, sparking massive public distress.",
                            statutory_rationale="Violates citizen service level delivery guarantees and Citizens' Charter obligations.",
                            next_question_id="s5_q2_rate_limiting",
                            compliance_delta=-30
                        )
                    ]
                ),
                "s5_q2_rate_limiting": ScenarioQuestion(
                    id="s5_q2_rate_limiting",
                    scenario_id="dg-dpi-05-apisetu-replay-attack",
                    stage_title="Stage 2: Adaptive Rate Limiting & Identity Protection",
                    context_update="Adversaries pivot to distributed botnets attempting brute-force queries against DigiLocker document-fetch URIs.",
                    prompt=(
                        "How should the department protect citizen DigiLocker credential URIs from automated exfiltration?"
                    ),
                    governance_pillar="Digital Public Infrastructure",
                    options=[
                        ScenarioOption(
                            option_id="s5_q2_opt_a",
                            text="Implement adaptive token-bucket rate limiting per citizen Virtual ID (VID), enforce mutual TLS with client certificate pinning, and require biometric/OTP citizen consent.",
                            is_optimal=True,
                            consequence_summary="Automated scraping is rendered technically impossible. Citizen privacy is preserved while genuine API Setu document queries proceed smoothly.",
                            statutory_rationale="Under Rule 9A of the IT Rules 2016 and DigiLocker security guidelines, requester systems must strictly authenticate and respect citizen consent tokens.",
                            next_question_id="s5_q3_nccc_alert",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s5_q2_opt_b",
                            text="Disable citizen consent verification to accelerate API transaction throughput.",
                            is_optimal=False,
                            consequence_summary="Massive citizen data breach occurs as unauthorized bots harvest education certificates and driving licenses.",
                            statutory_rationale="Direct violation of DPDP Act 2023 consent mandates and IT Act Section 43.",
                            next_question_id="s5_q3_nccc_alert",
                            compliance_delta=-45
                        )
                    ]
                ),
                "s5_q3_nccc_alert": ScenarioQuestion(
                    id="s5_q3_nccc_alert",
                    scenario_id="dg-dpi-05-apisetu-replay-attack",
                    stage_title="Stage 3: National Cyber Coordination & IOC Dissemination",
                    context_update="The attack pattern indicates a sophisticated state-sponsored threat actor testing automated vulnerabilities in national DPI infrastructure.",
                    prompt=(
                        "What is the final statutory coordination action required to safeguard other states and central ministries?"
                    ),
                    governance_pillar="Digital Public Infrastructure",
                    options=[
                        ScenarioOption(
                            option_id="s5_q3_opt_a",
                            text="Export sanitized Indicators of Compromise (IOCs), botnet IP ranges, and attack signatures to CERT-In and the National Cyber Coordination Centre (NCCC) for nationwide threat sharing.",
                            is_optimal=True,
                            is_terminal=True,
                            consequence_summary="CERT-In broadcasts nationwide cyber advisories. Other state portals preemptively block the botnet IPs, preventing coordinated welfare fraud.",
                            statutory_rationale="Fulfills the mandate of the National Cyber Security Strategy and Section 70B cyber threat intelligence sharing protocols.",
                            compliance_delta=35
                        ),
                        ScenarioOption(
                            option_id="s5_q3_opt_b",
                            text="Delete all logs immediately to cover up the fact that the gateway was targeted.",
                            is_optimal=False,
                            is_terminal=True,
                            consequence_summary="Threat actor strikes adjacent state portals with identical methods. Obstruction of justice charges are filed.",
                            statutory_rationale="Gross violation of CERT-In's mandatory 180-day log retention directive and destruction of evidence under Indian Penal Code / Bharatiya Nyaya Sanhita.",
                            compliance_delta=-50
                        )
                    ]
                )
            }
        )

        cls._scenarios[s1.id] = s1
        cls._scenarios[s2.id] = s2
        cls._scenarios[s3.id] = s3
        cls._scenarios[s4.id] = s4
        cls._scenarios[s5.id] = s5

    @classmethod
    def list_scenarios(cls) -> List[ScenarioListItem]:
        cls.initialize_scenarios()
        items = []
        for s in cls._scenarios.values():
            items.append(ScenarioListItem(
                id=s.id,
                title=s.title,
                domain=s.domain,
                ministry=s.ministry,
                statutory_framework=s.statutory_framework,
                difficulty=s.difficulty,
                estimated_minutes=s.estimated_minutes,
                summary=s.initial_context[:180] + "...",
                objectives_count=len(s.learning_objectives)
            ))
        return items

    @classmethod
    def get_scenario(cls, scenario_id: str) -> Optional[CaseScenario]:
        cls.initialize_scenarios()
        return cls._scenarios.get(scenario_id)


class ScenarioSessionManager:
    """Manages active user tabletop simulation sessions in memory."""

    _active_sessions: Dict[str, Dict] = {}

    @classmethod
    def start_session(cls, scenario_id: Optional[str] = None) -> ScenarioSessionResponse:
        ScenarioRepository.initialize_scenarios()
        if not scenario_id or scenario_id not in ScenarioRepository._scenarios:
            scenario_id = "dg-sec-01-ransomware-treasury"

        scenario = ScenarioRepository._scenarios[scenario_id]
        session_id = str(uuid.uuid4())
        root_q = scenario.questions[scenario.root_question_id]

        session_data = {
            "session_id": session_id,
            "scenario_id": scenario.id,
            "current_question_id": root_q.id,
            "compliance_score": 50,  # Base starting score
            "step_number": 1,
            "optimal_count": 0,
            "total_steps": 0,
            "is_terminal": False,
            "decision_trail": []
        }
        cls._active_sessions[session_id] = session_data

        return ScenarioSessionResponse(
            session_id=session_id,
            scenario_id=scenario.id,
            scenario_title=scenario.title,
            domain=scenario.domain,
            ministry=scenario.ministry,
            initial_context=scenario.initial_context,
            statutory_framework=scenario.statutory_framework,
            current_question=root_q,
            compliance_score=50,
            step_number=1
        )

    @classmethod
    def submit_answer(cls, session_id: str, option_id: str) -> ScenarioAnswerResponse:
        session = cls._active_sessions.get(session_id)
        if not session:
            raise KeyError(f"Session {session_id} not found or expired")

        scenario = ScenarioRepository.get_scenario(session["scenario_id"])
        current_q = scenario.questions[session["current_question_id"]]

        # Find chosen option
        chosen_opt = next((o for o in current_q.options if o.option_id == option_id), None)
        if not chosen_opt:
            raise ValueError(f"Option {option_id} not found on question {current_q.id}")

        # Update scoring
        session["step_number"] += 1
        session["total_steps"] += 1
        if chosen_opt.is_optimal:
            session["optimal_count"] += 1

        new_score = max(0, min(100, session["compliance_score"] + chosen_opt.compliance_delta))
        session["compliance_score"] = new_score

        # Log decision trail node
        log_node = DecisionNodeLog(
            step=session["total_steps"],
            stage_title=current_q.stage_title,
            question_prompt=current_q.prompt,
            selected_option_id=chosen_opt.option_id,
            selected_option_text=chosen_opt.text,
            is_optimal=chosen_opt.is_optimal,
            consequence_summary=chosen_opt.consequence_summary,
            statutory_rationale=chosen_opt.statutory_rationale,
            score_after_decision=new_score
        )
        session["decision_trail"].append(log_node)

        # Check terminal state
        is_terminal = chosen_opt.is_terminal or not chosen_opt.next_question_id
        next_q = None

        if not is_terminal and chosen_opt.next_question_id:
            next_q = scenario.questions.get(chosen_opt.next_question_id)
            if next_q:
                session["current_question_id"] = next_q.id
            else:
                is_terminal = True

        session["is_terminal"] = is_terminal
        summary = None

        if is_terminal:
            resolved_satisfactorily = session["compliance_score"] >= 70
            summary = ScenarioSummary(
                session_id=session_id,
                scenario_id=scenario.id,
                scenario_title=scenario.title,
                domain=scenario.domain,
                ministry=scenario.ministry,
                total_steps=session["total_steps"],
                optimal_steps=session["optimal_count"],
                procedural_compliance_score=session["compliance_score"],
                resolved_satisfactorily=resolved_satisfactorily,
                decision_trail=session["decision_trail"],
                key_regulatory_takeaways=[
                    f"Compliance Framework: {', '.join(scenario.statutory_framework)}",
                    f"Procedural Compliance: {session['compliance_score']}% ({'Pass Standard Achieved' if resolved_satisfactorily else 'Procedural Deficiencies Noted'})",
                    f"Optimal Incident Decisions: {session['optimal_count']} of {session['total_steps']} decision checkpoints",
                    f"Institutional Stakeholder: {scenario.ministry}"
                ]
            )

        return ScenarioAnswerResponse(
            session_id=session_id,
            is_terminal=is_terminal,
            selected_option=chosen_opt,
            next_question=next_q,
            compliance_score=new_score,
            step_number=session["step_number"],
            session_summary=summary
        )

    @classmethod
    def get_session_summary(cls, session_id: str) -> Optional[ScenarioSummary]:
        session = cls._active_sessions.get(session_id)
        if not session or not session.get("is_terminal"):
            return None

        scenario = ScenarioRepository.get_scenario(session["scenario_id"])
        resolved_satisfactorily = session["compliance_score"] >= 70
        return ScenarioSummary(
            session_id=session_id,
            scenario_id=scenario.id,
            scenario_title=scenario.title,
            domain=scenario.domain,
            ministry=scenario.ministry,
            total_steps=session["total_steps"],
            optimal_steps=session["optimal_count"],
            procedural_compliance_score=session["compliance_score"],
            resolved_satisfactorily=resolved_satisfactorily,
            decision_trail=session["decision_trail"],
            key_regulatory_takeaways=[
                f"Statutory Framework: {', '.join(scenario.statutory_framework)}",
                f"Evaluated Grade: {session['compliance_score']}% procedural adherence",
                f"Incident Triage Completed under {scenario.ministry} operational standards"
            ]
        )
