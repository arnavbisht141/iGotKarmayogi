from typing import List, Dict, Optional
from ..schemas import GovernmentDocument

OFFICIAL_GOVERNMENT_DOCUMENTS: List[GovernmentDocument] = [
    GovernmentDocument(
        id="doc_dopt_rule14_proceeding",
        title="Departmental Inquiry Proceeding under Rule 14 of CCS (CCA) Rules, 1965",
        document_type="Departmental Proceeding",
        issuing_authority="Department of Personnel & Training (DoPT), New Delhi",
        document_number="F.No. 11012/7/2025-Estt.(A-III)",
        statutory_reference="Central Civil Services (Classification, Control and Appeal) Rules, 1965 (CCS (CCA) Rules) - Rule 14 & Rule 15",
        date_of_issue="14 January 2026",
        full_text="""GOVERNMENT OF INDIA
MINISTRY OF PERSONNEL, PUBLIC GRIEVANCES AND PENSIONS
DEPARTMENT OF PERSONNEL AND TRAINING
NORTH BLOCK, NEW DELHI - 110001

MEMORANDUM OF INQUIRY PROCEEDINGS UNDER RULE 14

Subject: Initiation of Major Penalty Proceedings against Shri A.K. Verma, Deputy Director (Statistical Administration).

WHEREAS, the Disciplinary Authority proposes to hold an inquiry against the said Shri A.K. Verma under Rule 14 of the Central Civil Services (Classification, Control and Appeal) Rules, 1965.

The substance of the imputations of misconduct in respect of which the inquiry is proposed to be held is set out in the enclosed statement of:
1. Form 1: Articles of Charge (Unauthorized disclosure of preliminary non-cleared price index trends to an external market analysis firm prior to official embargo release).
2. Form 2: Statement of Imputations of Misconduct.
3. Form 3: List of documents by which the articles of charge are proposed to be sustained.
4. Form 4: Notice to delinquent officer to submit written statement of defense within 15 days.

PROCEDURAL CLAUSES & MANDATORY PROCEEDINGS:
1. Under Rule 14(4), the Government servant shall be required to submit his written statement of defense within 15 days of the date of receipt of the memorandum.
2. Under Rule 14(5)(a), on receipt of the written statement of defense, the Disciplinary Authority may itself inquire into such articles of charge, or appoint an Inquiring Authority.
3. Where the Charged Officer denies the charge, an oral inquiry must be instituted. No disciplinary action imposing major penalty (dismissal, removal, compulsory retirement, reduction in rank) can be legally sustained without affording reasonable opportunity to inspect prosecution exhibits and cross-examine state witnesses.
4. Failure to record reasons for rejecting defense evidence or declining requests for official defense witnesses constitutes a fundamental breach of Natural Justice (Audi Alteram Partem), rendering subsequent dismissal orders null and void ab initio in Central Administrative Tribunal (CAT).""",
        key_stakeholders=[
            "Disciplinary Authority (Joint Secretary / DG)",
            "Charged Officer (Deputy Director)",
            "Inquiring Authority (IA)",
            "Presenting Officer (PO)",
            "Defense Assistant (DA)"
        ],
        procedural_clauses=[
            "Mandatory 15-day notice period under Rule 14(4)",
            "Right of inspection of listed documents under Rule 14(11)",
            "Production and summoning of defense witnesses under Rule 14(17)",
            "Submission of Inquiry Report with reasoned findings under Rule 14(23)"
        ]
    ),
    GovernmentDocument(
        id="doc_gfr_gem_procurement_notice",
        title="Procurement Irregularity Scrutiny Notice & Vendor Debarment under GFR Rule 149 / 151",
        document_type="Notice",
        issuing_authority="Public Procurement Division, Department of Expenditure, Ministry of Finance",
        document_number="O.M. No. F.1/28/2025-PPD/GeM-AUDIT",
        statutory_reference="General Financial Rules (GFR) 2017 — Rules 144, 149, 151 & CVC Circular 02/05/2022",
        date_of_issue="03 February 2026",
        full_text="""GOVERNMENT OF INDIA
MINISTRY OF FINANCE, DEPARTMENT OF EXPENDITURE
PROCUREMENT POLICY DIVISION, LOK NAYAK BHAWAN, NEW DELHI

OFFICE MEMORANDUM & SCRUTINY DIRECTIVE

Subject: Vigilance Scrutiny on Collusive Bidding, Specification Tailoring, and Splitting of Indents on Government e-Marketplace (GeM).

1. Attention is invited to Rule 149 of General Financial Rules (GFR) 2017, mandating the procurement of common-use Goods and Services through GeM.
2. During continuous automated audit sweeps conducted by the Vigilance Division, systemic irregularities have been detected in Regional Procurement Divisions:
   (a) Splitting of Tenders: Splitting larger requirements into multiple miniature tranches below INR 5,00,000 to evade mandatory L1 Custom Bidding requirements under Rule 149(ii).
   (b) Restrictive Technical Parameters: Framing proprietary and exclusionary technical filters in Custom Bid documents that restrict competition to single favored OEMs.
   (c) Joint Bidding by Sister Concerns: Two bidding entities sharing identical IP addresses and registered GSTIN promoter directors submitting matching quotes.

STATUTORY PROCEEDING DIRECTIVE:
1. Head of Office / Procurement Committee Members are instructed to immediately issue a formal Show-Cause Notice under GFR Rule 151 to suspect entities prior to blacklisting or encashment of Bid Security / Performance Guarantee.
2. In the event of confirmed collusive bidding, the procuring entity must blacklist the supplier from participating in public procurement across Central Ministries for a period up to 2 years, after following due administrative inquiry and affording a 21-day representation period.
3. Summary debarment without issuing a show-cause notice is ultra vires Article 14 of the Constitution and liable to be quashed with institutional costs.""",
        key_stakeholders=[
            "Tender Inviting Authority (TIA)",
            "Procurement Committee Chairman",
            "Chief Vigilance Officer (CVO)",
            "GeM Incident Management Desk",
            "Bidding Entities & Original Equipment Manufacturers (OEMs)"
        ],
        procedural_clauses=[
            "Prohibition of indent splitting under GFR Rule 157",
            "Mandatory issuance of Show-Cause Notice under GFR Rule 151 prior to debarment",
            "Verification of independent bidding declarations and IP access logs",
            "Right of representation within 21 days"
        ]
    ),
    GovernmentDocument(
        id="doc_rti_first_appeal_proceeding",
        title="Statutory First Appellate Authority Proceeding under Section 19(1) of RTI Act, 2005",
        document_type="Statutory Form",
        issuing_authority="Office of the First Appellate Authority (FAA), Central Statistics Office, New Delhi",
        document_number="FAA/RTI/APPEAL/2026/088",
        statutory_reference="Right to Information Act, 2005 — Sections 7(1), 8(1)(j), 11 & 19(1)",
        date_of_issue="19 February 2026",
        full_text="""BEFORE THE FIRST APPELLATE AUTHORITY UNDER RTI ACT, 2005
CSO BHAWAN, JANPATH, NEW DELHI

IN THE MATTER OF:
Dr. R. Sengupta (Appellant, Senior Policy Researcher)
VERSUS
Central Public Information Officer (CPIO), MoSPI (Respondent)

PROCEEDING MEMORANDUM ON APPEAL FILED UNDER SECTION 19(1):

1. The Appellant filed an RTI application seeking unit-level household survey microdata containing anonymized consumption expenditure entries across urban sample blocks.
2. The CPIO rejected the application in toto citing Section 8(1)(j) of the RTI Act ("information which relates to personal information the disclosure of which has no relationship to any public activity or interest, or which would cause unwarranted invasion of the privacy of the individual").
3. The Appellant filed First Appeal under Section 19(1) contending:
   (a) The microdata sought is for peer-reviewed academic validation of national inflation series.
   (b) The collection of statistics was financed from public funds.
   (c) The survey records can be fully anonymized by severing identifier columns under Section 10 (Severability Clause).

STATUTORY MANDATES FOR THE APPELLATE AUTHORITY:
1. Section 10(1) allows access to that part of the record which does not contain any information exempt from disclosure.
2. The Public Information Officer cannot mechanically invoke blanket exemptions without demonstrating how anonymized statistical data harms privacy.
3. The Appellate Authority must either direct disclosure of severed/anonymized data within 15 days or pass a speaking quasi-judicial order recording specific reasons under Section 19(6). Failure to decide within 30 days triggers penalty proceedings before Central Information Commission (CIC) under Section 20.""",
        key_stakeholders=[
            "Appellant (Citizen / Researcher)",
            "Central Public Information Officer (CPIO)",
            "First Appellate Authority (FAA - Director / Joint Secretary rank)",
            "Central Information Commission (CIC)"
        ],
        procedural_clauses=[
            "Doctrine of Severability under Section 10(1)",
            "Mandatory adjudication timeline of 30 days under Section 19(6)",
            "Requirement of reasoned quasi-judicial speaking order",
            "Personal liability of CPIO under Section 20 for mala fide denial"
        ]
    ),
    GovernmentDocument(
        id="doc_mospi_nqaf_audit_notice",
        title="MoSPI National Quality Assurance Framework (NQAF) Audit Notice on Sampling Protocol Violations",
        document_type="Notice",
        issuing_authority="Statistical Audit & Quality Assurance Division (SAQAD), MoSPI",
        document_number="MoSPI/SAQAD/NQAF/AUDIT/2026/012",
        statutory_reference="Collection of Statistics Act, 2008 & UN-NQAF Quality Principle 4 (Sound Methodology)",
        date_of_issue="26 February 2026",
        full_text="""GOVERNMENT OF INDIA
MINISTRY OF STATISTICS AND PROGRAMME IMPLEMENTATION
STATISTICAL AUDIT & QUALITY ASSURANCE DIVISION (SAQAD)
SARDAR PATEL BHAWAN, NEW DELHI - 110001

QUALITY AUDIT SCRUTINY NOTICE & SHOW CAUSE

To: The Regional Director, NSSO Field Operations Division, Western Zone.

Subject: Unauthorized Hamlet-Group Substitutions and Non-Compliance with Circular Systematic Sampling in NSS Round 79.

1. During the on-site quality audit conducted by the National Statistical Systems Training Academy (NSSTA) inspection team in FSU No. 41028 (District Ratnagiri), significant deviations from prescribed field manuals were established:
   (a) Arbitrary Replacement of Hamlet-Group: Field staff replaced the assigned hamlet group with an adjacent settlement without obtaining mandatory prior sanction from the Deputy Director.
   (b) Purposive Selection of Sample Households: Instead of using circular systematic sampling with a random start, investigators interviewed readily accessible households adjoining the Gram Panchayat office.
   (c) Falsification of CAPI GPS Geotags: Digital timestamps indicated interviews taking place simultaneously across households separated by 12 kilometers.

REQUIRED STATUTORY PROCEEDINGS:
1. Under the Collection of Statistics Act, 2008, Section 15, willful neglect or submission of false statistical statements by an authorized officer constitutes an actionable offense.
2. You are directed to show cause within 7 calendar days why:
   - The entire batch of 64 schedules for FSU 41028 should not be formally nullified from the national pool.
   - Disciplinary action under Rule 16 (Minor Penalties) or Rule 14 (Major Penalties) of CCS (CCA) Rules should not be recommended against the Field Supervisor.
   - An independent re-survey audit team should not be deployed at the cost of the regional allocation.""",
        key_stakeholders=[
            "Statistical Auditor (Director rank)",
            "Regional Director (NSSO Western Zone)",
            "Supervisory Field Officer",
            "Survey Enumerators",
            "National Quality Council Committee"
        ],
        procedural_clauses=[
            "Absolute prohibition of unauthorized FSU/hamlet substitution",
            "Mandatory re-survey protocol for corrupted sampling frames",
            "Statutory notice period of 7 days for regional explanation",
            "Nullification criteria under UN-NQAF Principle 4"
        ]
    )
]

def get_all_documents() -> List[GovernmentDocument]:
    return OFFICIAL_GOVERNMENT_DOCUMENTS

def get_document_by_id(doc_id: str) -> Optional[GovernmentDocument]:
    for doc in OFFICIAL_GOVERNMENT_DOCUMENTS:
        if doc.id == doc_id:
            return doc
    return None
