# Digital Governance, Cybersecurity Architecture & CTF Sandbox

> **Status:** `Active Implementation` (Branch: `cgp/digital-governance`)  
> **Lead Engineer:** Diwakar Ujjwal (@diwakarujjwal)  
> **Accrediting Authorities:** National e-Governance Division (NeGD) & Indian Computer Emergency Response Team (CERT-In), Ministry of Electronics & IT (MeitY)  
> **Primary Subsystems:**  
> - Official Curriculum & In-Lesson Quizzes (`backend/app/core/seed_data.py`)  
> - 15-Question Certification Examination (`backend/app/modules/assessments/`)  
> - Multi-Stage Incident Response Tabletop Engine (`backend/app/modules/digital_governance/`)  
> - TryHackMe/HTB-Style Dynamic CTF Sandbox & Marimo Execution (`backend/content/cybersec_challenges/`, `testing_marimo/`)  

---

## 1. Executive Summary & Statutory Foundations

The **Digital Governance & Cybersecurity Ecosystem** on iGOT Karmayogi equips Indian civil servants, ministry IT coordinators, and public sector administrators with operational and regulatory mastery across the Government of India's digital frameworks.

The curriculum and evaluation engines strictly center on **5 Core National Pillars**:
1. **Cybersecurity**: Statutory cyber incident response and mandatory 6-hour reporting to CERT-In under Section 70B(6) of the Information Technology Act 2000; Critical Information Infrastructure (CII) protection administered by NCIIPC under Section 70A; live Security Operations Center (SOC) telemetry triage.
2. **Data Privacy**: Digital Personal Data Protection Act, 2023 (DPDP Act); statutory duties of Data Fiduciaries and Significant Data Fiduciaries (SDF); consent manager architecture; citizen rights (access, correction, erasure); Data Protection Board of India enforcement and penalty regimes (up to ₹250 crore).
3. **Digital Signatures & Public Key Infrastructure (PKI)**: IT Act 2000 Sections 3, 3A, and 5; apex oversight by the Controller of Certifying Authorities (CCA); Class 3 FIPS 140-2 Level 2 cryptographic hardware tokens; Aadhaar eSign in e-Office; evidentiary admissibility and non-repudiation under Section 65B of the Indian Evidence Act.
4. **Government Cloud (MeghRaj / GI Cloud)**: MeitY Cloud adoption guidelines; mandatory third-party technical security audits by the Standardisation Testing and Quality Certification (STQC) Directorate; sovereign data localization for primary and disaster recovery records; Government Community Cloud (GCC) isolation.
5. **Digital Public Infrastructure (DPI / India Stack)**: Population-scale digital platforms including Aadhaar authentication APIs and e-KYC 2.5; DigiLocker Rule 9A legal parity with physical documents; Public Financial Management System (PFMS) Direct Benefit Transfer (DBT) via the NPCI Aadhaar Payment Bridge (APB); inter-ministerial data exchange via API Setu / OpenForge.

---

## 2. Curriculum & Assessment Architecture (Milestone 1)

### 2.1 Course Specification
- **Title:** `Digital Governance, Cyber Defense & Public Digital Architecture`
- **Category:** `Digital Governance`
- **Organization:** `National e-Governance Division (NeGD) & CERT-In`
- **Target Audience:** Indian Administrative Service (IAS), Indian Statistical Service (ISS), Central Secretariat Service (CSS), and departmental IT nodal officers.
- **Duration:** 10.0 Hours | Intermediate Difficulty | 5 Modules | 10 Lessons.

### 2.2 In-Lesson Practice Activities (MCQs)
Every lesson embeds an authentic, civil-service-graded practice question within the `CourseLearningPlayerPage.tsx` interface:
- Immediate client-side validation against backend endpoint `POST /api/learning/lesson/{id}/activity`.
- Contextual regulatory feedback citing specific Acts, statutory rules, or circulars.
- Confetti celebration upon correct submission.

### 2.3 Comprehensive Certification Examination
Attached directly to the course via the core `Assessment` and `Question` schema:
- **Duration:** 30 minutes timed examination.
- **Passing Threshold:** 70.0% verified score.
- **15 Examination Questions:** 3 rigorous questions for each of the 5 pillars, testing statutory definitions, administrative protocols, and forensic triage.
- Fully compatible with `AssessmentTestPage.tsx` at `/assess/[assessmentId]`, offering detailed question analysis breakdowns and credential certificate generation.

---

## 3. Multi-Stage Incident Response Tabletop Engine (Milestone 2)

### 3.1 Overview & Simulation Mechanics
Located at `/digital-governance/scenarios` (backed by `backend/app/modules/digital_governance/`), the Tabletop Engine presents real-world crisis management simulations for government officers.

### 3.2 The 5 National Pillars & Scenario Catalog
1. **Cybersecurity (`dg-sec-01-ransomware-treasury`)**: *Operation Vajra*
   - Context: Active ransomware file encryption on State Treasury Payment Gateway (`TREASURY-DB-01`) at 02:15 AM before ₹180 crore pension release.
   - Core Statutory Decision: Network segmentation vs. hard power-off (preserving volatile memory under Section 65B of Indian Evidence Act); adherence to CERT-In's mandatory 6-hour incident reporting window under Section 70B(6) of IT Act 2000.
2. **Data Privacy (`dg-priv-02-dbt-cloud-breach`)**: *Operation Raksha*
   - Context: Unauthenticated public cloud storage bucket exposing 75,000 unredacted citizen bank records and Aadhaar numbers.
   - Core Statutory Decision: Immediate credential revocation; dual notification to the Data Protection Board of India and affected Data Principals under Section 8(6) of DPDP Act 2023; appointment of Data Protection Officer (DPO) and DPIA under Section 10.
3. **Digital Signatures & PKI (`dg-pki-03-gem-tender-dispute`)**: *Operation Mudra*
   - Context: Contractor disputes a ₹45 crore e-tender submitted via GeM with their Class 3 DSC token, claiming token theft.
   - Core Statutory Decision: Verification against CA OCSP responder and CRL revocation logs; non-repudiation enforcement under Sections 3, 3A, and 42 of IT Act 2000; Section 65B evidentiary certification for High Court defense.
4. **Government Cloud / MeghRaj (`dg-cloud-04-meghraj-sovereignty`)**: *Operation Megh*
   - Context: System integrator deploys automated containers into an unempaneled overseas data center to handle festival traffic spikes.
   - Core Statutory Decision: Emergency traffic cutoff and failover to domestic GCC; enforcement of STQC security auditing and MeitY empanelment; NIST SP 800-88 cryptographic sanitization verification.
5. **Digital Public Infrastructure / DPI (`dg-dpi-05-apisetu-replay-attack`)**: *Operation Setu*
   - Context: 65,000 requests/second replay attack against state scholarship e-KYC gateway.
   - Core Statutory Decision: Gateway-level cryptographic nonce verification and clock-skew tolerance (<300ms); adaptive token-bucket rate limiting per Virtual ID (VID); threat intelligence sharing with CERT-In and NCCC.

### 3.3 Interactive Client Player (`CyberScenariosPage.tsx`)
- **Pillar Filter Tabs**: Quick filtering across the 5 domains.
- **Dynamic Decision Nodes**: Step-by-step branching prompts with instant operational consequence callouts and statutory rationale citations.
- **Compliance Score Tracking**: Real-time scoring meter ($0–100\%$) rewarding statutory compliance and penalizing procedural infractions.
- **Executive Debrief Report**: Chronological decision trail, optimal vs sub-optimal breakdown, and printable compliance summary.

---

## 4. Verification & Testing

- **Curriculum & MCQs Tests (`backend/tests/test_digital_governance.py`)**:
  - `test_01_course_metadata`: Verifies course title, NeGD/CERT-In accreditation, and module counts.
  - `test_02_modules_and_in_lesson_activities`: Verifies all 10 lessons and their 4-option practice activities.
  - `test_03_certification_assessment_and_15_questions`: Validates 30-min time limit, 70% threshold, and all 15 questions.
  - `test_04_skills_association`: Confirms linkage across all 5 digital governance skills.
- **Tabletop Scenarios Tests (`backend/tests/test_scenarios.py`)**:
  - `test_01_all_five_domains_represented`: Validates full coverage of the 5 national pillars.
  - `test_02_scenario_session_lifecycle_and_branching`: Tests multi-stage branching on the Treasury Ransomware case.
  - `test_03_suboptimal_path_handling`: Tests score deduction and consequence delivery on procedural violations.
  - `test_04_session_summary_retrieval`: Validates final executive debrief generation and decision trail logging.

