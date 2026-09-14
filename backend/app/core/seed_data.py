import json
import datetime
from sqlalchemy.orm import Session
from app.models.models import (
    User, UserProfile, Department, Course, Module, Lesson,
    Skill, CourseSkill, UserSkill, Enrollment, Progress,
    Assessment, Question, PlannedCourse, LearningHistory
)
from app.core.security import get_password_hash

def seed_database(db: Session):
    # 0. Ensure Technical Course Lab Templates are seeded even if curriculum exists
    from app.modules.technical_courses.services.template_service import BUILTIN_LAB_TEMPLATES
    from app.models.models import TechnicalLabTemplate
    
    if not db.query(TechnicalLabTemplate).first():
        for t in BUILTIN_LAB_TEMPLATES:
            tc_json = json.dumps([tc.model_dump() for tc in t.test_cases_template])
            tmpl_record = TechnicalLabTemplate(
                id=t.id,
                title=t.title,
                skill=t.skill,
                language=t.language,
                difficulty=t.difficulty,
                lab_type=t.lab_type,
                tags_json=json.dumps(t.tags),
                instructions_template=t.instructions_template,
                starter_code_template=t.starter_code_template,
                solution_template=t.solution_template,
                constraints_json=json.dumps(t.constraints),
                test_cases_template_json=tc_json
            )
            db.merge(tmpl_record)
        db.commit()

    # Check if core curriculum already seeded
    if db.query(User).first():
        return

    print("Seeding iGot Karmayogi database with official civil service curriculum...")

    # 1. Departments
    depts = [
        Department(name="Ministry of Statistics & Programme Implementation (MoSPI)", description="National statistical authority"),
        Department(name="National Sample Survey Office (NSSO)", description="Socio-economic sample surveys division"),
        Department(name="Central Statistics Office (CSO)", description="National accounts and price indices division"),
        Department(name="Institute of Secretariat Training & Management (ISTM)", description="Civil services management institute"),
        Department(name="Department of Personnel & Training (DoPT)", description="Civil services administrative cadre")
    ]
    db.add_all(depts)
    db.commit()

    # 2. Skills (4 Core Competency Verticals)
    skills_data = [
        ("Civil Service Conduct Rules & Administrative Ethics", "Behavioural Competency"),
        ("Consumer Price Index (CPI) & Inflation Analysis", "Statistical Competency"),
        ("Data Cleaning, Wrangling & Python Automation", "Technical Competency"),
        ("Cybersecurity Defense & Digital Public Infrastructure", "Digital Governance")
    ]
    skills = []
    for name, cat in skills_data:
        s = Skill(name=name, category=cat)
        db.add(s)
        skills.append(s)
    db.commit()

    # 3. Users
    admin_user = User(
        email="admin@karmayogi.gov.in",
        password_hash=get_password_hash("Admin@123"),
        full_name="Dr. Arvind Subramanian",
        role="admin"
    )
    db.add(admin_user)
    db.flush()

    admin_profile = UserProfile(
        user_id=admin_user.id,
        phone="+91 98100 12345",
        bio="Director General, National Statistical Systems Training Academy (NSSTA). Oversight of capacity building for Indian Statistical Service (ISS) officers.",
        education="Ph.D. in Econometrics, Delhi School of Economics",
        work_experience_years=22,
        prior_training="LBSNAA Senior Leadership Program, IMF National Accounts Fellowship",
        designation="Director General",
        department="Ministry of Statistics & Programme Implementation (MoSPI)",
        job_role="Institutional Capacity & Training Administrator",
        current_assignment="Oversight of ISS Cadre Training & Karmayogi Statistical Curriculum",
        areas_of_interest="National Accounts, Capacity Building, Data Governance",
        language_pref="en",
        appearance_pref="light",
        onboarding_completed=True,
        daily_goal_minutes=45,
        current_streak_days=14
    )
    db.add(admin_profile)

    learner_user = User(
        email="rajesh.kumar@mospi.gov.in",
        password_hash=get_password_hash("Learner@123"),
        full_name="Rajesh Kumar",
        role="learner"
    )
    db.add(learner_user)
    db.flush()

    learner_profile = UserProfile(
        user_id=learner_user.id,
        phone="+91 98765 43210",
        bio="Senior Statistical Officer in National Accounts Division, MoSPI. Passionate about price statistics and automated sample validation.",
        education="M.Sc. Statistics, Banaras Hindu University",
        work_experience_years=8,
        prior_training="NSSTA Foundation Course, ISTM Public Procurement",
        designation="Senior Statistical Officer (SSO)",
        department="Central Statistics Office (CSO)",
        job_role="Price Indices and Monthly CPI Compilation",
        current_assignment="Urban Consumer Basket Weight Revision 2026",
        areas_of_interest="Inflation Metrics, Sample Survey Design, Python Automation",
        language_pref="en",
        appearance_pref="light",
        onboarding_completed=True,
        daily_goal_minutes=30,
        current_streak_days=6
    )
    db.add(learner_profile)

    new_user = User(
        email="priya.sharma@mospi.gov.in",
        password_hash=get_password_hash("Learner@123"),
        full_name="Priya Sharma",
        role="learner"
    )
    db.add(new_user)
    db.flush()

    new_profile = UserProfile(
        user_id=new_user.id,
        phone="+91 99112 88344",
        bio="Assistant Director (ISS 2024 Batch), NSSO Field Operations Division.",
        education="M.Stat, Indian Statistical Institute (ISI) Kolkata",
        work_experience_years=2,
        prior_training="Foundation Course at LBSNAA",
        designation="Assistant Director",
        department="National Sample Survey Office (NSSO)",
        job_role="Field Survey Supervision & Quality Control",
        onboarding_completed=False,  # Triggers 5-step wizard on first login!
        daily_goal_minutes=30,
        current_streak_days=1
    )
    db.add(new_profile)
    db.commit()

    # 4. Courses (4 Core Competency Verticals)
    # Course 1: Behavioural Competency
    c1 = Course(
        title="Civil Service Conduct, Administrative Ethics & Interpersonal Leadership",
        overview="Master statutory administrative ethics, CCS (Conduct) Rules 1964, Rule 14 disciplinary inquiries, natural justice doctrines, public grievance redressal, high-stakes stakeholder negotiation, and oral civil service defense.",
        instructor="Smt. Rashmi Verma, IAS (Retd.) & Shri P. K. Basu",
        organization="Department of Personnel & Training (DoPT)",
        duration_hours=6.0,
        difficulty="intermediate",
        source="internal",
        category="Behavioural",
        rating=4.92,
        enrolled_count=1850,
        is_popular=True,
        is_new=True
    )
    db.add(c1)
    db.flush()

    m1_1 = Module(course_id=c1.id, title="Module 1: Statutory Code of Conduct & Ethics", description="CCS (Conduct) Rules 1964, integrity standards, and avoidance of conflict of interest.", order=1)
    m1_2 = Module(course_id=c1.id, title="Module 2: Quasi-Judicial Inquiries & Natural Justice", description="Conducting departmental proceedings under Rule 14 CCS (CCA) Rules.", order=2)
    m1_3 = Module(course_id=c1.id, title="Module 3: Administrative Negotiation & Public Leadership", description="High-pressure public communication, grievance redressal, and crisis leadership.", order=3)
    db.add_all([m1_1, m1_2, m1_3])
    db.flush()

    l1_1_1 = Lesson(
        module_id=m1_1.id,
        title="Lesson 1: Statutory Framework of CCS (Conduct) Rules, 1964",
        content_type="reading",
        duration_minutes=20,
        content="""# Statutory Framework of CCS (Conduct) Rules, 1964

Every civil servant in the Government of India is governed by the statutory provisions of the **Central Civil Services (Conduct) Rules, 1964**:

1. **Rule 3 — General Principles of Integrity**:
   - Maintain absolute integrity, devotion to duty, and do nothing unbecoming of a Government servant.
   - Uphold supremacy of the Constitution and democratic values.
   - Defend impartiality, political neutrality, and fairness in administrative decision-making.

2. **Rule 3C — Prohibition of Sexual Harassment**:
   - Prevention of Sexual Harassment of Women at Workplace (POSH Act) compliance.

> **Doctrine**: Discretionary administrative powers must be exercised strictly within statutory limits, guided by public interest without personal or pecuniary bias.""",
        activity_question="Under Rule 3 of the CCS (Conduct) Rules, what is the paramount obligation of an administrative officer?",
        activity_options_json=json.dumps([
            "To maintain absolute integrity, devotion to duty, and political neutrality",
            "To obey verbal instructions from non-official acquaintances",
            "To maximize fee collections arbitrarily",
            "To bypass statutory tender processes"
        ]),
        activity_correct_option=0,
        activity_explanation="Rule 3(1) mandates absolute integrity, dedication to duty, and conduct worthy of an officer of the State.",
        order=1
    )

    l1_1_2 = Lesson(
        module_id=m1_2.id,
        title="Lesson 2: Principles of Natural Justice (Audi Alteram Partem)",
        content_type="video",
        duration_minutes=25,
        video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        content="""# Audi Alteram Partem in Departmental Proceedings

In any quasi-judicial proceeding governed by Rule 14 of CCS (CCA) Rules, 1965:

1. **Right to Notice**:
   - Form 1 charge-sheet containing definite articles of charge, statement of imputations, and list of documents/witnesses.
2. **Right of Inspection**:
   - Under Rule 14(11), the Charged Officer must be permitted full physical or certified digital access to listed documentary evidence.
3. **Impartial Inquiring Authority**:
   - The IA acts as an independent quasi-judicial evaluator, not a prosecutor.""",
        activity_question="What does the doctrine of Audi Alteram Partem require during a Rule 14 inquiry?",
        activity_options_json=json.dumps([
            "Granting fair hearing and opportunity to inspect evidence and cross-examine witnesses",
            "Allowing the prosecution to hide confidential witness statements",
            "Ordering immediate punishment without recording evidence",
            "Conducting ex-parte hearings without notice"
        ]),
        activity_correct_option=0,
        activity_explanation="Audi Alteram Partem guarantees no person shall be condemned unheard, requiring evidence disclosure and right of defense.",
        order=2
    )
    db.add_all([l1_1_1, l1_1_2])
    db.flush()

    # Course 2: Statistical Competency
    c2 = Course(
        title="Compilation of Consumer Price Index (CPI) & Inflation Metrics",
        overview="Comprehensive practical guide to the compilation of All India Consumer Price Index (Rural, Urban, Combined). Learn item basket weighting, Laspeyres index formulation, geometric mean of price relatives, treatment of seasonal goods, and house rent imputation.",
        instructor="Dr. P. C. Mohanan & Shri Sunil Jain",
        organization="Central Statistics Office (CSO)",
        duration_hours=5.0,
        difficulty="advanced",
        source="internal",
        category="Statistical",
        rating=4.88,
        enrolled_count=1420,
        is_popular=True,
        is_new=False
    )
    db.add(c2)
    db.flush()

    m2_1 = Module(course_id=c2.id, title="Module 1: Index Formulation & Basket Selection", description="Mathematical foundations of modified Laspeyres and Jevons price relatives.", order=1)
    m2_2 = Module(course_id=c2.id, title="Module 2: Imputation & Quality Adjustment", description="Techniques for disappearing items and seasonal vegetables.", order=2)
    db.add_all([m2_1, m2_2])
    db.flush()

    l2_1_1 = Lesson(
        module_id=m2_1.id,
        title="Lesson 1: The Modified Laspeyres Price Index Formula",
        content_type="reading",
        duration_minutes=25,
        content="""# The Modified Laspeyres Formula in CPI Compilation

In India's official CPI (Base 2012=100), elementary price indices are aggregated using a **Modified Laspeyres Formula**:

$$I = \\sum \\left[ W_i \\times \\left( \\frac{P_{i,t}}{P_{i,0}} \\right) \\right]$$

Where:
- $W_i$ is the normalized expenditure weight of item $i$ derived from the Consumer Expenditure Survey (CES).
- $P_{i,t}$ is the current period average price of item $i$.
- $P_{i,0}$ is the base year price of item $i$.

### Elementary Aggregation with Jevons
At the market level, price quotations for a specific item across multiple selected shops are aggregated using the **Geometric Mean (Jevons Index)** rather than the simple arithmetic mean to prevent upward substitution bias.""",
        activity_question="Which index formula is employed at the elementary quotation level to minimize substitution bias?",
        activity_options_json=json.dumps([
            "Geometric Mean (Jevons Index)",
            "Simple Harmonic Mean",
            "Carli Arithmetic Index",
            "Dutot Ratio of Averages"
        ]),
        activity_correct_option=0,
        activity_explanation="International best practices and MoSPI guidelines use the Geometric Mean (Jevons) at the elementary quotation level because it exhibits transitivity and minimizes substitution bias.",
        order=1
    )
    db.add(l2_1_1)
    db.flush()

    # Course 3: Technical Competency
    c3 = Course(
        title="Python and Data Cleaning Pipelines for Public Policy",
        overview="Modern automated data cleaning and reproducible data processing for civil service analysts using Pandas, NumPy, and Statsmodels. Automate messy survey ingestion, missing data imputation, schema validation, and pipeline orchestration.",
        instructor="Dr. Tanvi Grover & Prof. Rajesh Sen",
        organization="MoSPI Data Lab",
        duration_hours=8.0,
        difficulty="intermediate",
        source="internal",
        category="Technical",
        rating=4.95,
        enrolled_count=1680,
        is_popular=True,
        is_new=True
    )
    db.add(c3)
    db.flush()

    m3_1 = Module(course_id=c3.id, title="Module 1: Data Wrangling & Cleaning with Pandas", description="Cleaning messy survey sheets, missing data imputation, and microdata wrangling.", order=1)
    db.add(m3_1)
    db.flush()

    l3_1_1 = Lesson(
        module_id=m3_1.id,
        title="Lesson 1: Vectorized Data Wrangling on Survey Microdata",
        content_type="lab",
        duration_minutes=35,
        content="""# Vectorized Data Wrangling with Pandas

When processing large-scale public policy microdata, traditional Python `for` loops cause severe execution bottlenecks.

```python
import pandas as pd
import numpy as np

# Load survey microdata
df = pd.read_csv("survey_microdata.csv")

# Vectorized weighted calculation
df["weighted_val"] = df["val"] * df["weight"] / 100
```

Vectorized operations execute in compiled C routines, yielding massive performance speedups over iterative loops.""",
        activity_question="Why should vectorized methods be preferred over row-by-row for-loops in Pandas?",
        activity_options_json=json.dumps([
            "Vectorized calculations run in compiled C routines and are orders of magnitude faster",
            "Because for-loops are deprecated in Python 3.12",
            "Because vectorized methods use less hard disk space",
            "Because Pandas does not support for-loops"
        ]),
        activity_correct_option=0,
        activity_explanation="Pandas vectorization delegates calculations to compiled NumPy C routines without Python interpreter loop overhead.",
        order=1
    )
    db.add(l3_1_1)
    db.flush()

    # Course 4: Digital Governance
    c4 = Course(
        title="Cybersecurity Defense & Digital Public Infrastructure Governance",
        overview="Critical information infrastructure protection, CERT-In compliance directives, cyber incident response, Treasury Single Account (TSA) controls, and secure Direct Benefit Transfer (DBT) workflows across government platforms.",
        instructor="Shri V. Ramaswamy, IDAS & CERT-In Directorate",
        organization="National Critical Information Infrastructure Protection Centre (NCIIPC)",
        duration_hours=7.0,
        difficulty="intermediate",
        source="external",
        category="Digital Governance",
        rating=4.91,
        enrolled_count=2150,
        is_popular=True,
        is_new=False
    )
    db.add(c4)
    db.flush()

    m4_1 = Module(course_id=c4.id, title="Module 1: Cyber Defense & PFMS Treasury Controls", description="Critical information infrastructure protection, CERT-In compliance, and TSA integration.", order=1)
    db.add(m4_1)
    db.flush()

    l4_1_1 = Lesson(
        module_id=m4_1.id,
        title="Lesson 1: Treasury Single Account (TSA) & Cyber Hardening",
        content_type="reading",
        duration_minutes=20,
        content="""# Treasury Single Account (TSA) & Critical Infrastructure Protection

The Treasury Single Account (TSA) administered via PFMS ensures that government scheme funds remain in the Consolidated Fund of India until actual electronic disbursement.

### Cyber Safeguards
- End-to-end PKI signature validation for all e-bills.
- Mandatory 2FA and CERT-In compliant logging of system transactions.""",
        activity_question="What is the primary objective of implementing the Treasury Single Account (TSA) through PFMS?",
        activity_options_json=json.dumps([
            "To prevent parking of government funds in bank accounts and ensure just-in-time funding",
            "To increase paperwork in regional accounting offices",
            "To delay payments to social benefit recipients",
            "To replace commercial banks entirely"
        ]),
        activity_correct_option=0,
        activity_explanation="TSA ensures that public funds stay in the Consolidated Fund of India until immediate disbursement, eliminating idle parked balances.",
        order=1
    )
    db.add(l4_1_1)
    db.flush()

    # Link Course Skills
    cs_links = [
        (c1.id, skills[0].id),
        (c2.id, skills[1].id),
        (c3.id, skills[2].id),
        (c4.id, skills[3].id)
    ]
    for cid, sid in cs_links:
        db.add(CourseSkill(course_id=cid, skill_id=sid))
    db.commit()

    # 5. Assessments for Courses
    # Assessment 1 for Course 1 (Behavioural)
    a1 = Assessment(
        course_id=c1.id,
        title="Certification Exam: Civil Service Conduct & Administrative Ethics",
        description="Official certification examination testing statutory integrity standards, CCS (Conduct) Rules 1964, natural justice principles, and Rule 14 inquiry procedures.",
        time_limit_minutes=25,
        pass_threshold_percent=70.0
    )
    db.add(a1)
    db.flush()

    q1_1 = Question(
        assessment_id=a1.id,
        text="Under Rule 14(11) of the CCS (CCA) Rules 1965, what right does the Charged Officer have regarding documentary evidence?",
        options_json=json.dumps([
            "Absolute right to inspect and receive certified copies of listed prosecution documents",
            "No right to inspect documents until final judgment",
            "Only verbal summary by the Presenting Officer",
            "Inspection permitted only after prosecution concludes witnesses"
        ]),
        correct_option_index=0,
        explanation="Rule 14(11) guarantees the statutory right of the Charged Officer to inspect listed documents to prepare their defense.",
        order=1
    )
    q1_2 = Question(
        assessment_id=a1.id,
        text="What is the consequence if an Inquiring Authority proceeds ex-parte after a formal application alleging bias has been filed?",
        options_json=json.dumps([
            "Proceedings are fatally vitiated for violating Audi Alteram Partem and will be quashed",
            "The inquiry is accelerated lawfully",
            "The officer automatically forfeits defense rights",
            "The Inquiring Authority receives special commendation"
        ]),
        correct_option_index=0,
        explanation="Per established DoPT guidelines and judicial precedents, the IA must stay proceedings until the Disciplinary Authority decides the bias petition.",
        order=2
    )
    q1_3 = Question(
        assessment_id=a1.id,
        text="Under Rule 3 of CCS (Conduct) Rules, which duty is expressly mandated for every civil servant?",
        options_json=json.dumps([
            "To maintain absolute integrity, devotion to duty, and do nothing unbecoming of a Government servant",
            "To prioritize personal commercial interests over official tasks",
            "To disclose classified statistical releases prematurely",
            "To accept costly gifts from contracting vendors"
        ]),
        correct_option_index=0,
        explanation="Rule 3(1) is the core ethical obligation binding all central government employees.",
        order=3
    )
    q1_4 = Question(
        assessment_id=a1.id,
        text="When can a disciplinary authority dispense with a departmental inquiry before imposing major penalties?",
        options_json=json.dumps([
            "Only under exceptional conditions covered strictly under Article 311(2) second proviso of the Constitution",
            "Whenever the inquiry would take more than one week",
            "If the accused officer submits a written denial",
            "At the arbitrary verbal instruction of an administrative head"
        ]),
        correct_option_index=0,
        explanation="Article 311(2) proviso strictly delineates the rare constitutional exceptions (e.g. state security or impracticability).",
        order=4
    )
    db.add_all([q1_1, q1_2, q1_3, q1_4])
    db.flush()

    # Assessment 2 for Course 2
    a2 = Assessment(
        course_id=c2.id,
        title="Certification Exam: Consumer Price Index (CPI) Compilation",
        description="Assesses mastery of price aggregation, Laspeyres index methodology, and outlier handling.",
        time_limit_minutes=20,
        pass_threshold_percent=70.0
    )
    db.add(a2)
    db.flush()

    q2_1 = Question(
        assessment_id=a2.id,
        text="At the elementary price quotation level, which average is recommended to eliminate upward substitution bias?",
        options_json=json.dumps([
            "Geometric Mean (Jevons Index)",
            "Harmonic Mean",
            "Simple Arithmetic Mean (Carli)",
            "Mode of reported prices"
        ]),
        correct_option_index=0,
        explanation="The geometric mean (Jevons) satisfies axiomatic time-reversal and treats price relatives symmetrically, minimizing substitution bias.",
        order=1
    )
    q2_2 = Question(
        assessment_id=a2.id,
        text="The item basket weights in the All-India CPI are fundamentally derived from which statistical source?",
        options_json=json.dumps([
            "Household Consumer Expenditure Survey (CES / HCES)",
            "Annual Survey of Industries (ASI)",
            "Reserve Bank of India Monetary Policy Report",
            "Census decennial headcounts"
        ]),
        correct_option_index=0,
        explanation="CPI item weights reflect consumer spending patterns measured directly in the nationwide Household Consumer Expenditure Survey.",
        order=2
    )
    db.add_all([q2_1, q2_2])
    db.commit()

    # 6. Active Enrollment & Progress for Learner Rajesh Kumar
    enr1 = Enrollment(
        user_id=learner_user.id,
        course_id=c1.id,
        status="in_progress",
        started_at=datetime.datetime.utcnow() - datetime.timedelta(days=4),
        progress_percent=66.7,
        last_lesson_id=l1_1_2.id
    )
    db.add(enr1)
    db.flush()

    prog1 = Progress(enrollment_id=enr1.id, module_id=m1_1.id, lesson_id=l1_1_1.id, completed=True, activity_completed=True)
    prog2 = Progress(enrollment_id=enr1.id, module_id=m1_1.id, lesson_id=l1_1_2.id, completed=True, activity_completed=True)
    db.add_all([prog1, prog2])

    # Planned Course for Learner
    p_course = PlannedCourse(
        user_id=learner_user.id,
        course_id=c2.id,
        planned_for="Q4 2026",
        source="self"
    )
    db.add(p_course)

    # Learning History
    lh1 = LearningHistory(user_id=learner_user.id, course_id=c1.id, viewed_at=datetime.datetime.utcnow() - datetime.timedelta(hours=2))
    lh2 = LearningHistory(user_id=learner_user.id, course_id=c3.id, viewed_at=datetime.datetime.utcnow() - datetime.timedelta(days=1))
    db.add_all([lh1, lh2])

    # Seed User Skill
    us1 = UserSkill(user_id=learner_user.id, skill_id=skills[2].id, source_course_id=c3.id)
    db.add(us1)

    # 10. Seed Technical Course Lab Templates (Human-Created)
    from app.modules.technical_courses.services.template_service import BUILTIN_LAB_TEMPLATES
    from app.models.models import TechnicalLabTemplate
    
    for t in BUILTIN_LAB_TEMPLATES:
        tc_json = json.dumps([tc.model_dump() for tc in t.test_cases_template])
        tmpl_record = TechnicalLabTemplate(
            id=t.id,
            title=t.title,
            skill=t.skill,
            language=t.language,
            difficulty=t.difficulty,
            lab_type=t.lab_type,
            tags_json=json.dumps(t.tags),
            instructions_template=t.instructions_template,
            starter_code_template=t.starter_code_template,
            solution_template=t.solution_template,
            constraints_json=json.dumps(t.constraints),
            test_cases_template_json=tc_json
        )
        db.merge(tmpl_record)

    db.commit()
    print("Database successfully seeded with realistic civil service curriculum, accounts, and technical lab templates!")
