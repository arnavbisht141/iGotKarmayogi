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
    # Check if already seeded
    # Always ensure Digital Governance and Cyber Defense curriculum is seeded
    seed_digital_governance_curriculum(db)

    # Check if already seeded base data
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

    # 2. Skills
    skills_data = [
        ("Sample Survey Design & Sampling Techniques", "Statistical Methodology"),
        ("Consumer Price Index (CPI) & Inflation Analysis", "Economic Statistics"),
        ("Official Statistics Quality Framework (NQAF)", "Data Governance"),
        ("National Accounts Statistics & GDP Estimation", "Economic Statistics"),
        ("Digital Governance & PFMS Public Finance", "Public Administration"),
        ("Python & R for Public Sector Data Analytics", "Data Science"),
        ("Administrative Law & Official Procedures", "Civil Service Ethics")
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

    # 4. Courses
    # Course 1: NSS Surveys
    c1 = Course(
        title="Fundamentals of National Sample Surveys (NSS)",
        overview="Master the methodological framework of large-scale socio-economic surveys conducted by India's National Sample Survey Office (NSSO). Covers multi-stage stratified sampling, field schedules, non-sampling error minimization, and computer-assisted personal interviewing (CAPI).",
        instructor="Prof. M. R. Saluja & Smt. Ananya Sen, ISS",
        organization="National Sample Survey Office (NSSO)",
        duration_hours=6.5,
        difficulty="intermediate",
        source="internal",
        category="Sample Surveys",
        rating=4.9,
        enrolled_count=1420,
        is_popular=True,
        is_new=False
    )
    db.add(c1)
    db.flush()

    # Course 1 Modules and Lessons
    m1_1 = Module(course_id=c1.id, title="Module 1: Sampling Design & Frame Construction", description="Principles of probability proportional to size (PPS) sampling in rural and urban frames.", order=1)
    m1_2 = Module(course_id=c1.id, title="Module 2: Field Schedules & CAPI Execution", description="Administering household schedule 1.0 and enterprise survey instruments digitally.", order=2)
    m1_3 = Module(course_id=c1.id, title="Module 3: Multiplier Generation & Estimation", description="Deriving pooled estimates and standard errors across state and central samples.", order=3)
    db.add_all([m1_1, m1_2, m1_3])
    db.flush()

    l1_1_1 = Lesson(
        module_id=m1_1.id,
        title="Lesson 1: Structure of the First Stage Units (FSUs)",
        content_type="reading",
        duration_minutes=20,
        content="""# Structure of First Stage Units (FSUs) in NSS Surveys

The National Sample Survey typically adopts a **stratified two-stage design**:

1. **First Stage Units (FSUs)**:
   - In the rural sector: Census villages (Panchayat wards in Kerala).
   - In the urban sector: Urban Frame Survey (UFS) blocks.
   
2. **Second Stage Units (SSUs)**:
   - Households or enterprises selected systematically with random start.

### Stratification Criteria
Rural strata are formed within each district based on population density and geographical contiguity. Urban strata are delineated according to town population categories (Class I, II, III).

### Probability Proportional to Size (PPS)
FSUs are allocated circular systematically with probability proportional to size (PPSWR/PPSWOR), where size corresponds to village population or census household count.

> **Key Rule for Field Investigators**: An FSU cannot be substituted without prior written authorization from the Deputy Director of the Regional Office.""",
        activity_question="In rural NSS surveys, what is typically designated as the First Stage Unit (FSU)?",
        activity_options_json=json.dumps([
            "A census village",
            "An individual agricultural household",
            "A whole administrative district",
            "A block development office"
        ]),
        activity_correct_option=0,
        activity_explanation="In rural sector surveys of the NSSO, the First Stage Unit (FSU) is universally defined as the census village (or panchayat ward in select states).",
        order=1
    )

    l1_1_2 = Lesson(
        module_id=m1_1.id,
        title="Lesson 2: Hamlet-Group and Sub-Block Formation",
        content_type="video",
        duration_minutes=25,
        video_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        content="""# Hamlet-Group and Sub-Block Formation Rules

When an FSU is very large in terms of present population (usually exceeding 1,200 persons or 300 households), administering a total listing becomes cost-prohibitive.

### Delineation Procedures
1. Divide the FSU into an equal number of hamlet-groups (hg) or sub-blocks (sb) of approximately equal population size.
2. Ensure each hamlet-group has distinct, permanent natural boundaries (roads, water channels, railway lines).
3. Select two hamlet-groups for sample listing:
   - **hg 1**: Hamlet group with highest concentration of vulnerable/target population (selected purposively).
   - **hg 2**: Selected randomly from the remaining hamlet groups with equal probability.

This dual-selection design safeguards representation of target socio-economic strata while preserving unbiased estimation.""",
        activity_question="When is hamlet-group (hg) formation mandatory in a rural NSS sample village?",
        activity_options_json=json.dumps([
            "Whenever the village exceeds 1,200 population or ~300 households",
            "Only when requested by the village Sarpanch",
            "Only if the village has no electricity",
            "In every single sample village regardless of population"
        ]),
        activity_correct_option=0,
        activity_explanation="Per NSS field manual standards, hamlet-group formation is mandatory when the current village population exceeds approximately 1,200 persons or 300 households.",
        order=2
    )

    l1_2_1 = Lesson(
        module_id=m1_2.id,
        title="Lesson 3: Digitized CAPI Data Validation Checks",
        content_type="lab",
        duration_minutes=30,
        content="""# Digital CAPI Data Validation & Range Checks

With the transition to tablet-based CAPI (Computer-Assisted Personal Interviewing), real-time validation prevents inconsistencies at the point of data capture.

### Essential Consistency Checks
- **Age vs. Education Grade**: An individual under 14 cannot have an advanced post-graduate degree recorded.
- **Consumption Expenditure Balance**: Total monthly per-capita expenditure (MPCE) must cross-validate with food and non-food sub-aggregates within ±2%.
- **Land Possessed vs. Land Cultivated**: Land cultivated cannot exceed land possessed without corresponding leased-in land entries.

Field Supervisors must execute the digital integrity audit script before transmitting batches to the state server.""",
        activity_question="What is the primary benefit of CAPI over traditional paper schedules in NSS surveys?",
        activity_options_json=json.dumps([
            "Immediate automated logical validation and elimination of data entry backlogs",
            "Eliminating the need to train field investigators",
            "Allowing investigators to skip household visits",
            "Permitting non-random household replacements"
        ]),
        activity_correct_option=0,
        activity_explanation="CAPI eliminates physical paper transit delays, automates routing logic, and performs immediate validation checks right at the respondent's doorstep.",
        order=1
    )

    db.add_all([l1_1_1, l1_1_2, l1_2_1])
    db.flush()

    # Course 2: Consumer Price Index (CPI)
    c2 = Course(
        title="Compilation of Consumer Price Index (CPI) & Inflation Metrics",
        overview="Comprehensive practical guide to the compilation of All India Consumer Price Index (Rural, Urban, Combined). Learn item basket weighting, Laspeyres index formulation, geometric mean of price relatives, treatment of seasonal goods, and house rent imputation.",
        instructor="Dr. P. C. Mohanan & Shri Sunil Jain",
        organization="Central Statistics Office (CSO)",
        duration_hours=5.0,
        difficulty="advanced",
        source="internal",
        category="Price Statistics",
        rating=4.85,
        enrolled_count=980,
        is_popular=True,
        is_new=True
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

    # Course 3: Data Quality Framework
    c3 = Course(
        title="Data Quality Frameworks & Official Statistics in India",
        overview="Aligning Indian official statistics with the United Nations National Quality Assurance Framework (UN-NQAF). Study the 19 principles of statistical integrity, confidentiality safeguards, revision policies, and metadata standards.",
        instructor="Dr. G. C. Manna",
        organization="National Statistical Systems Training Academy (NSSTA)",
        duration_hours=4.0,
        difficulty="beginner",
        source="internal",
        category="Data Governance",
        rating=4.75,
        enrolled_count=640,
        is_popular=False,
        is_new=True
    )
    db.add(c3)
    db.flush()

    m3_1 = Module(course_id=c3.id, title="Module 1: Principles of Official Statistics", description="Institutional environment, objectivity, and confidentiality.", order=1)
    db.add(m3_1)
    db.flush()

    l3_1_1 = Lesson(
        module_id=m3_1.id,
        title="Lesson 1: UN Fundamental Principles of Official Statistics",
        content_type="reading",
        duration_minutes=15,
        content="""# UN Fundamental Principles of Official Statistics

Adopted by the United Nations General Assembly in 2014, these ten principles form the bedrock of official statistical systems:

1. **Relevance, Impartiality, and Equal Access**: Official statistics must represent public goods available to all citizens simultaneously.
2. **Professional Standards and Ethics**: Concepts and procedures must adhere purely to scientific statistical discipline without political intervention.
3. **Accountability and Transparency**: Presentation of sources and methods to facilitate interpretation.
4. **Prevention of Misuse**: The statistical agency has the duty to comment on erroneous interpretation.
5. **Confidentiality**: Individual data collected for statistical compilation must remain strictly confidential and never used for non-statistical purposes.""",
        activity_question="Under the UN Fundamental Principles, can census or survey response data of an individual be shared for law enforcement or taxation?",
        activity_options_json=json.dumps([
            "No, individual survey records are strictly confidential and protected by law",
            "Yes, if requested by local police",
            "Yes, provided the respondent paid tax",
            "Yes, after 1 year has elapsed"
        ]),
        activity_correct_option=0,
        activity_explanation="Principle 5 mandates absolute confidentiality: data collected by statistical agencies for compilation must remain strictly confidential and never used for investigation or taxation.",
        order=1
    )
    db.add(l3_1_1)
    db.flush()

    # Course 4: External Course (ISTM / DoPT)
    c4 = Course(
        title="Digital Governance & Public Financial Management System (PFMS)",
        overview="Direct Benefit Transfer (DBT), treasury integration, electronic bill processing, and expenditure tracking through PFMS. Authorized course accredited by ISTM for all central government employees.",
        instructor="Shri V. Ramaswamy, IDAS",
        organization="Institute of Secretariat Training & Management (ISTM)",
        duration_hours=7.0,
        difficulty="intermediate",
        source="external",  # External training catalog source
        category="Public Administration",
        rating=4.92,
        enrolled_count=2150,
        is_popular=True,
        is_new=False
    )
    db.add(c4)
    db.flush()

    m4_1 = Module(course_id=c4.id, title="Module 1: PFMS Architecture & DBT Portals", description="Integration between state treasuries, central ministries, and NPCI Aadhaar payment bridge.", order=1)
    db.add(m4_1)
    db.flush()

    l4_1_1 = Lesson(
        module_id=m4_1.id,
        title="Lesson 1: Treasury Single Account (TSA) Mechanism",
        content_type="reading",
        duration_minutes=20,
        content="""# The Treasury Single Account (TSA) and Just-in-Time Funding

The Treasury Single Account (TSA) system administered via PFMS ensures that government funds remain in the Consolidated Fund of India until the exact moment of payment to the ultimate vendor or beneficiary.

### Key Features
- Eliminates parking of unspent budgetary allocations in commercial bank accounts.
- Daily sweeping of balances to RBI.
- Real-time visibility into program expenditures for Central Sector Schemes.""",
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

    # Course 5: Python for Policy Analysis
    c5 = Course(
        title="Python and Statistical Computing for Public Policy",
        overview="Modern data analysis for official statisticians using Pandas, NumPy, and Statsmodels. Automate data cleaning, compute econometric models, and generate reproducible policy briefs.",
        instructor="Dr. Tanvi Grover",
        organization="MoSPI Data Lab",
        duration_hours=8.0,
        difficulty="intermediate",
        source="internal",
        category="Data Science",
        rating=4.95,
        enrolled_count=1680,
        is_popular=True,
        is_new=True
    )
    db.add(c5)
    db.flush()

    m5_1 = Module(course_id=c5.id, title="Module 1: Data Wrangling with Pandas", description="Cleaning messy ministerial Excel sheets and CSV survey microdata.", order=1)
    db.add(m5_1)
    db.flush()

    l5_1_1 = Lesson(
        module_id=m5_1.id,
        title="Lesson 1: Vectorized Operations on NSS Microdata",
        content_type="lab",
        duration_minutes=35,
        content="""# Vectorized Operations on Microdata using Pandas

When processing millions of NSS household observations, traditional Python `for` loops cause severe execution bottlenecks.

```python
import pandas as pd
import numpy as np

# Load NSS round microdata
df = pd.read_csv("nss_78th_round_microdata.csv")

# Vectorized weighted expenditure computation
df["weighted_mpce"] = df["mpce"] * df["multiplier"] / 100

# Aggregating by state and sector
state_summary = df.groupby(["state_code", "sector"]).apply(
    lambda x: np.average(x["mpce"], weights=x["multiplier"])
).reset_index(name="mean_mpce")
```

Vectorized operations execute in optimized C routines, yielding up to a 100x speedup over iterative loops.""",
        activity_question="Why should vectorized methods be preferred over row-by-row for-loops in Pandas when processing large survey datasets?",
        activity_options_json=json.dumps([
            "Vectorized calculations run in compiled C routines and are orders of magnitude faster",
            "Because for-loops are deprecated in Python 3.12",
            "Because vectorized methods use less hard disk space",
            "Because Pandas does not support for-loops"
        ]),
        activity_correct_option=0,
        activity_explanation="Pandas vectorization delegates calculations to internal compiled NumPy C code, executing operations across whole memory blocks without Python interpreter overhead.",
        order=1
    )
    db.add(l5_1_1)
    db.flush()

    # Link Course Skills
    cs_links = [
        (c1.id, skills[0].id),
        (c2.id, skills[1].id),
        (c3.id, skills[2].id),
        (c4.id, skills[4].id),
        (c5.id, skills[5].id)
    ]
    for cid, sid in cs_links:
        db.add(CourseSkill(course_id=cid, skill_id=sid))
    db.commit()

    # 5. Assessments for Courses
    # Assessment 1 for Course 1
    a1 = Assessment(
        course_id=c1.id,
        title="Comprehensive Competency Assessment: National Sample Surveys",
        description="Official certification examination testing sampling design, stratification rigor, hamlet-group formation, and CAPI field validation procedures.",
        time_limit_minutes=25,
        pass_threshold_percent=70.0
    )
    db.add(a1)
    db.flush()

    q1_1 = Question(
        assessment_id=a1.id,
        text="In a two-stage stratified sampling design used in NSS rural rounds, what represents the First Stage Unit (FSU)?",
        options_json=json.dumps([
            "A census village / revenue village",
            "An individual agricultural household",
            "A block development administrative zone",
            "A district statistical office"
        ]),
        correct_option_index=0,
        explanation="Census villages serve as the standard FSUs in the rural frame of NSS surveys.",
        order=1
    )
    q1_2 = Question(
        assessment_id=a1.id,
        text="When is hamlet-group (hg) formation compulsory in a sample village during NSS field execution?",
        options_json=json.dumps([
            "When current village population is approx. 1,200 or more (or 300+ households)",
            "Only if there are more than 5 distinct castes",
            "Whenever the field supervisor forgets paper schedules",
            "In every sample village without exception"
        ]),
        correct_option_index=0,
        explanation="NSS field manual prescribes hamlet group division when population reaches or exceeds 1,200 persons or 300 households.",
        order=2
    )
    q1_3 = Question(
        assessment_id=a1.id,
        text="What is the primary objective of Computer-Assisted Personal Interviewing (CAPI) in NSSO?",
        options_json=json.dumps([
            "Eliminate data-entry backlogs and enforce automated real-time logical validation",
            "Permit investigators to complete surveys without respondent interaction",
            "Reduce the total sample size by half",
            "Eliminate the need for statistical multipliers"
        ]),
        correct_option_index=0,
        explanation="CAPI captures responses digitally on tablets, enforcing validation constraints at the point of capture and removing post-survey data entry delays.",
        order=3
    )
    q1_4 = Question(
        assessment_id=a1.id,
        text="Which sampling selection method is used when allocating FSUs to account for population size differentials?",
        options_json=json.dumps([
            "Probability Proportional to Size with Replacement / Without Replacement (PPS)",
            "Simple Random Sampling with Equal Probability (SRSWOR)",
            "Convenience Snowball Sampling",
            "Voluntary Respondent Selection"
        ]),
        correct_option_index=0,
        explanation="PPS (Probability Proportional to Size) selection gives larger population units a proportionally higher likelihood of inclusion, optimizing efficiency.",
        order=4
    )
    db.add_all([q1_1, q1_2, q1_3, q1_4])

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

    db.commit()
    print("Database successfully seeded with realistic civil service curriculum and accounts!")


def seed_digital_governance_curriculum(db: Session):
    """
    Seeds the official Digital Governance, Cyber Defense & Public Digital Architecture curriculum,
    covering the 5 mandatory Government of India civil-service pillars:
    1. Cybersecurity (CERT-In directives, Section 70B IT Act 2000, CII protection, SOC telemetry)
    2. Data Privacy (Digital Personal Data Protection Act 2023, Data Fiduciaries, DPBI)
    3. Digital Signatures & PKI (IT Act Sections 3 & 3A, CCA, Class 3 DSC, e-Office, Indian Evidence Act Section 65B)
    4. Government Cloud (GI Cloud / MeghRaj, MeitY empanelment, STQC audits, data sovereignty)
    5. Digital Public Infrastructure (DPI / India Stack, Aadhaar e-KYC, DigiLocker, PFMS DBT, API Setu)
    """
    course_title = "Digital Governance, Cyber Defense & Public Digital Architecture"
    existing_course = db.query(Course).filter(Course.title == course_title).first()
    if existing_course:
        return

    print(f"Seeding official curriculum: '{course_title}'...")

    # 1. Ensure Department exists
    dept = db.query(Department).filter(Department.name.ilike("%National e-Governance Division%")).first()
    if not dept:
        dept = Department(
            name="National e-Governance Division (NeGD) & CERT-In",
            description="Apex national bodies administering digital governance architecture, India Stack integration, and national cyber incident response under MeitY."
        )
        db.add(dept)
        db.flush()

    # 2. Ensure Skills exist
    gov_skills = [
        ("Critical Infrastructure Cyber Defense & CERT-In Compliance", "Cybersecurity"),
        ("Data Privacy Compliance & DPDP Act 2023", "Data Governance"),
        ("Public Key Infrastructure (PKI) & Digital Signatures", "Digital Governance"),
        ("Government Cloud Architecture & MeghRaj Strategy", "Cloud Computing"),
        ("Digital Public Infrastructure (DPI) & India Stack", "Public Administration")
    ]
    skill_objs = []
    for s_name, s_cat in gov_skills:
        s_obj = db.query(Skill).filter(Skill.name == s_name).first()
        if not s_obj:
            s_obj = Skill(name=s_name, category=s_cat)
            db.add(s_obj)
            db.flush()
        skill_objs.append(s_obj)
    db.commit()

    # 3. Create Course
    course = Course(
        title=course_title,
        overview="Comprehensive capacity-building program for civil servants and public sector administrators on Government of India digital mandates. Covers CERT-In cyber defense directives, the Digital Personal Data Protection Act (DPDP 2023), Public Key Infrastructure (PKI) & eSign in e-Office, MeghRaj (GI Cloud) architecture, and Digital Public Infrastructure (DPI / India Stack).",
        instructor="Dr. Sanjay Bahl (DG, CERT-In) & Smt. Debjani Ghosh, NeGD",
        organization="National e-Governance Division (NeGD) & CERT-In",
        duration_hours=10.0,
        difficulty="intermediate",
        source="internal",
        category="Digital Governance",
        rating=4.96,
        enrolled_count=2450,
        is_popular=True,
        is_new=True
    )
    db.add(course)
    db.flush()

    # Link Course Skills
    for s_obj in skill_objs:
        db.add(CourseSkill(course_id=course.id, skill_id=s_obj.id))
    db.flush()

    # 4. Create 5 Modules with in-depth Lessons and In-Lesson Practice Activities (MCQs)

    # ── MODULE 1: Cybersecurity ──────────────────────────────────────────────
    m1 = Module(
        course_id=course.id,
        title="Module 1: Critical Infrastructure Cyber Defense & CERT-In Directives",
        description="Statutory reporting rules under Section 70B of IT Act 2000, NCIIPC audit framework, and SOC telemetry triage.",
        order=1
    )
    db.add(m1)
    db.flush()

    l1_1 = Lesson(
        module_id=m1.id,
        title="Lesson 1: Statutory Mandate of CERT-In & Mandatory 6-Hour Reporting",
        content_type="reading",
        duration_minutes=25,
        content="""# Statutory Mandate of CERT-In & Mandatory 6-Hour Incident Reporting

The **Indian Computer Emergency Response Team (CERT-In)** functions under Section 70B of the **Information Technology Act, 2000** as the national nodal agency for responding to computer security incidents.

### Mandatory Directives (Directions of 28 April 2022)
Under the provisions of sub-section (6) of section 70B of the IT Act, CERT-In issued mandatory cybersecurity directions:

1. **6-Hour Mandatory Reporting Window**:
   - Any service provider, intermediary, data center, body corporate, and government organization **must report specified cyber security incidents to CERT-In within six (6) hours** of noticing or being brought to notice of such incidents.
   - Reportable incidents include targeted scanning, compromise of critical systems, unauthorized access to IT systems/data, ransomware outbreaks, and identity theft attacks.

2. **System Clock Synchronization**:
   - All government entities and service providers must connect to the **Network Time Protocol (NTP)** servers of the National Physical Laboratory (NPL) or National Informatics Centre (NIC), or NTP servers traceable to them, to ensure uniform forensic timeline reconstruction.

3. **Mandatory 180-Day Log Retention**:
   - All ICT system logs across all servers, domain controllers, firewalls, and network appliances must be securely maintained within the Indian jurisdiction for a rolling duration of **at least 180 consecutive days**.

> **Crucial Rule for Civil Servants**: Failure to comply with CERT-In directions is punishable under Section 70B(7) of the IT Act with imprisonment up to one year, or with a fine up to one lakh rupees, or both.""",
        activity_question="Under CERT-In directions issued under Section 70B of the IT Act, within what mandatory timeframe must government organizations report cyber security incidents to CERT-In?",
        activity_options_json=json.dumps([
            "Within 6 hours of noticing or being brought to notice of the incident",
            "Within 24 hours of concluding internal departmental forensics",
            "Within 7 working days following public disclosure",
            "At the conclusion of the quarterly audit cycle"
        ]),
        activity_correct_option=0,
        activity_explanation="Under Section 70B(6) directions issued by CERT-In, all government bodies, intermediaries, and enterprises must report specified cyber incidents within six (6) hours of detection.",
        order=1
    )

    l1_2 = Lesson(
        module_id=m1.id,
        title="Lesson 2: SOC Authentication Telemetry & Incident Triage",
        content_type="lab",
        duration_minutes=30,
        content="""# SOC Authentication Telemetry & Incident Triage

Security Operations Center (SOC) analysts in government infrastructure continuously monitor authentication logs to protect sensitive public portals (such as PFMS, e-Office, and state treasury databases).

### Anatomy of an Authentication Attack
When investigating brute-force and credential-stuffing incidents (such as *Operation NightShift*):
1. **Telemetry Ingestion**: Review Windows Event ID `4625` (Anomalous Logon Failure) and Event ID `4624` (Successful Logon).
2. **Behavioral Spikes**: Hundreds of failed authentication attempts originating from a single external IP address targeting distinct usernames within minutes indicate dictionary brute-forcing.
3. **Breach Pivot**: A subsequent Event `4624` (Logon Type 10 - Remote Interactive / RDP) from that identical IP indicates compromise of administrative credentials.
4. **Post-Exploitation Triage**: Look for immediate execution of Living-off-the-Land Binaries (LOLBins) such as `powershell.exe -enc`, `certutil -urlcache`, or unauthorized user group modifications.

### Incident Containment Protocol
- Immediately isolate the target host at the network switch / VLAN layer.
- **Do not power down the physical server**, as powering down erases volatile RAM containing adversary memory injection artifacts.
- Preserve RAM image and disk forensics under Section 65B of the Indian Evidence Act.""",
        activity_question="During an off-hours security alert on a core government server, multiple rapid failed logins followed by a single successful interactive login from an anomalous external IP indicates which type of incident?",
        activity_options_json=json.dumps([
            "Brute-force credential stuffing followed by unauthorized account compromise",
            "Scheduled automated system backup synchronization",
            "Routine network packet jitter and latency fluctuation",
            "Legitimate remote maintenance by authorized system administrators"
        ]),
        activity_correct_option=0,
        activity_explanation="A burst of failed authentication attempts followed by a successful logon from an untrusted external IP is a classic indicator of brute force or credential stuffing, requiring immediate network isolation and triage.",
        order=2
    )
    db.add_all([l1_1, l1_2])
    db.flush()

    # ── MODULE 2: Data Privacy (DPDP Act 2023) ──────────────────────────────
    m2 = Module(
        course_id=course.id,
        title="Module 2: Data Privacy & Compliance under DPDP Act 2023",
        description="Obligations of Data Fiduciaries, Significant Data Fiduciaries (SDF), citizen consent frameworks, and Data Protection Board of India enforcement.",
        order=2
    )
    db.add(m2)
    db.flush()

    l2_1 = Lesson(
        module_id=m2.id,
        title="Lesson 1: Obligations of Data Fiduciaries & Significant Data Fiduciaries",
        content_type="reading",
        duration_minutes=25,
        content="""# Obligations of Data Fiduciaries under the DPDP Act 2023

Enacted in August 2023, the **Digital Personal Data Protection Act, 2023 (DPDP Act)** regulates the processing of digital personal data in India.

### Key Statutory Actors
- **Data Principal**: The citizen to whom the personal data relates.
- **Data Fiduciary**: Any person, ministry, department, or body corporate who determines the purpose and means of processing of personal data.
- **Data Processor**: An entity that processes personal data on behalf of a Data Fiduciary.

### Core Obligations of Government Data Fiduciaries (Section 8)
1. **Reasonable Security Safeguards**: Obligated to implement appropriate technical and organizational measures to prevent personal data breach.
2. **Mandatory Breach Reporting**: In the event of a personal data breach, the Data Fiduciary must give notice of the breach to the **Data Protection Board of India (DPBI)** and to each affected Data Principal.
3. **Purpose Limitation & Data Erasure**: Must erase personal data as soon as the specified purpose is no longer being served and retention is no longer necessary for legal or business purposes.

### Significant Data Fiduciaries (SDF) (Section 10)
Entities designated as SDFs (based on volume, sensitivity, and national security impact) must:
- Appoint a resident **Data Protection Officer (DPO)** who reports directly to the apex executive.
- Appoint an independent **Data Auditor** to evaluate compliance.
- Undertake periodic **Data Protection Impact Assessments (DPIA)**.""",
        activity_question="Under the Digital Personal Data Protection Act 2023 (DPDP), what constitutes a primary statutory obligation of a government department acting as a Data Fiduciary?",
        activity_options_json=json.dumps([
            "Implement reasonable security safeguards to prevent breaches and erase personal data once the specified purpose is fulfilled",
            "Monetize citizen demographic data to commercial third parties to subsidize portal maintenance",
            "Publish unredacted citizen registries and Aadhaar numbers on open public noticeboards",
            "Retain citizen personal records indefinitely without any purpose limitation"
        ]),
        activity_correct_option=0,
        activity_explanation="Under Section 8 of the DPDP Act 2023, a Data Fiduciary must implement reasonable technical and organizational safeguards and erase personal data as soon as the specified purpose is completed.",
        order=1
    )

    l2_2 = Lesson(
        module_id=m2.id,
        title="Lesson 2: Consent Standards, Notice & Citizens' Rights",
        content_type="reading",
        duration_minutes=25,
        content="""# Consent Standards, Notice & Enforcement under DPDP Act 2023

### Standard of Valid Consent (Section 6)
Consent must be:
- **Free, specific, informed, unconditional, and unambiguous**, with a clear affirmative action.
- Accompanied by a pre-consent **Notice** detailing the personal data to be collected, purpose of processing, how to exercise rights, and grievance redressal contact.
- Must be available in English or any of the **22 languages specified in the Eighth Schedule** to the Constitution.

### Rights of Citizens (Data Principals)
1. **Right to Access Information**: Summary of personal data processed and identities of Data Fiduciaries/Processors shared with.
2. **Right to Correction & Erasure**: Right to rectify inaccurate data and erase data no longer required.
3. **Right to Grievance Redressal**: Readily available dispute resolution mechanisms before approaching the Board.
4. **Right to Nominate**: Ability to designate a nominee in the event of death or incapacity.

### Penalties Imposed by the Data Protection Board of India
The Schedule prescribes stringent monetary penalties:
- **Up to ₹250 crore**: For significant failure to take reasonable security safeguards leading to a personal data breach.
- **Up to ₹200 crore**: For failure to notify the Board and affected citizens regarding a personal data breach.
- **Up to ₹200 crore**: For non-fulfillment of additional obligations in relation to processing children's data.""",
        activity_question="What is the maximum penalty that can be levied by the Data Protection Board of India on a Data Fiduciary for failure to implement reasonable security safeguards leading to a significant personal data breach?",
        activity_options_json=json.dumps([
            "Up to ₹250 crore",
            "Up to ₹50 lakh",
            "Up to ₹5 crore",
            "No financial penalty, only an informal administrative reprimand"
        ]),
        activity_correct_option=0,
        activity_explanation="The Schedule to the DPDP Act 2023 empowers the Data Protection Board of India to levy penalties of up to ₹250 crore for failure to take reasonable security safeguards to prevent a personal data breach.",
        order=2
    )
    db.add_all([l2_1, l2_2])
    db.flush()

    # ── MODULE 3: Digital Signatures & PKI ────────────────────────────────────
    m3 = Module(
        course_id=course.id,
        title="Module 3: Public Key Infrastructure (PKI), Digital Signatures & e-Office",
        description="Controller of Certifying Authorities (CCA) standards, cryptographic validity of Class 3 DSC, Aadhaar eSign, and non-repudiation.",
        order=3
    )
    db.add(m3)
    db.flush()

    l3_1 = Lesson(
        module_id=m3.id,
        title="Lesson 1: Cryptographic Foundations of Class 3 DSC & PKI Hierarchy",
        content_type="reading",
        duration_minutes=20,
        content="""# Cryptographic Foundations of Class 3 DSC & India's PKI Hierarchy

In official governance, electronic documents and procurement tenders must satisfy the highest levels of authenticity, non-repudiation, and integrity.

### India's PKI Legal Architecture
Under the **Information Technology Act, 2000 (Sections 17–34)**:
1. **Controller of Certifying Authorities (CCA)**: Apex regulatory authority appointed by the Central Government. The CCA operates the **Root Certifying Authority of India (RCAI)**.
2. **Licensed Certifying Authorities (CAs)**: Entities licensed by CCA (such as NICCA, CDAC, eMudhra) that issue Digital Signature Certificates (DSC) to officers.
3. **Class 3 DSC Standards**:
   - Issued on cryptographic FIPS 140-2 Level 2 USB cryptographic hardware tokens.
   - The private key is generated inside the hardware chip and can **never be exported**.
   - Employs asymmetric cryptography (RSA 2048-bit or ECDSA) with SHA-256 hashing.

### Digital Signature Process
1. A cryptographic hash (digest) of the electronic file is computed via SHA-256.
2. The hash is encrypted using the officer's **Private Key** (stored on the DSC token).
3. Any recipient verifies the file using the officer's **Public Key** obtained from the certified CA public registry.
4. If a single character in the document is altered, the decrypted hash does not match, immediately alerting the recipient to tampering.""",
        activity_question="In India's PKI hierarchy established under the IT Act 2000, who operates the National Root CA and regulates all licensed Certifying Authorities (CAs)?",
        activity_options_json=json.dumps([
            "The Controller of Certifying Authorities (CCA)",
            "Local district magistrates and collectors",
            "Individual commercial hardware token manufacturers",
            "Local telecom service providers"
        ]),
        activity_correct_option=0,
        activity_explanation="Under Section 18 of the IT Act 2000, the Controller of Certifying Authorities (CCA) operates the Root Certifying Authority of India (RCAI) and exercises statutory oversight over all licensed Certifying Authorities.",
        order=1
    )

    l3_2 = Lesson(
        module_id=m3.id,
        title="Lesson 2: e-Office Implementation & Non-Repudiation under Section 65B",
        content_type="reading",
        duration_minutes=25,
        content="""# e-Office Implementation & Non-Repudiation under Section 65B

The Government of India's **e-Office** system (developed by NIC) has digitized secretariat files and inter-ministerial correspondence.

### Non-Repudiation in e-Office
Non-repudiation is the assurance that the author of an electronic document or official notation cannot successfully dispute the authenticity of their signature:
- When an Under Secretary or Joint Secretary signs a file notation in e-Office using DSC or **Aadhaar eSign**, an indelible audit trail binds the user ID, timestamp, IP address, and cryptographic signature.
- **Aadhaar eSign (Online Electronic Signature Service)**: Uses Aadhaar biometric or OTP authentication to facilitate legally binding on-demand electronic signing under Second Schedule to the IT Act.

### Admissibility in Courts: Section 65B Certificate
Under **Section 65B of the Indian Evidence Act, 1872** (and corresponding provisions in the Bharatiya Sakshya Adhiniyam):
- Electronic records (emails, server logs, signed e-Office notes) are admissible as primary evidence provided they are accompanied by a **Section 65B Certificate**.
- The certificate must be signed by a person occupying a responsible official position in relation to the operation of the relevant device or management of relevant activities, identifying the electronic record and describing the device's regular operational integrity.""",
        activity_question="Why is an asymmetric cryptographic digital signature or Aadhaar eSign required for official notations in e-Office instead of a scanned handwritten image?",
        activity_options_json=json.dumps([
            "It provides cryptographic non-repudiation and tamper evidence that detects any post-signing alterations",
            "Because image scanners are prohibited in government offices",
            "Because scanned images consume more cloud storage bandwidth",
            "Because image formats cannot be viewed on mobile devices"
        ]),
        activity_correct_option=0,
        activity_explanation="Under Sections 3 and 3A of the IT Act, asymmetric public key cryptography binds the signatory to the document hash, ensuring tamper-evidence and legal non-repudiation in courts of law.",
        order=2
    )
    db.add_all([l3_1, l3_2])
    db.flush()

    # ── MODULE 4: Government Cloud (MeghRaj / GI Cloud) ──────────────────────
    m4 = Module(
        course_id=course.id,
        title="Module 4: Government Cloud Strategy (MeghRaj / GI Cloud) & Sovereignty",
        description="MeitY Cloud adoption guidelines, STQC audit empanelment, sovereign data localization, and tenant isolation.",
        order=4
    )
    db.add(m4)
    db.flush()

    l4_1 = Lesson(
        module_id=m4.id,
        title="Lesson 1: The MeghRaj Architecture & MeitY Empanelment Standards",
        content_type="reading",
        duration_minutes=20,
        content="""# The MeghRaj Architecture & MeitY Empanelment Standards

The Government of India launched the **GI Cloud initiative (named "MeghRaj")** to accelerate e-services delivery while optimizing government ICT spending.

### Core Architectural Models under MeghRaj
1. **National Cloud (NIC Cloud)**: Dedicated sovereign cloud infrastructure operated by the National Informatics Centre for critical central and state government workloads.
2. **MeitY Empaneled Commercial Cloud Service Providers (CSPs)**: Certified public cloud providers providing scalable compute, storage, and disaster recovery.
3. **Government Community Cloud (GCC)**: Physically and logically segregated cloud infrastructure dedicated exclusively to Indian government and public sector organizations, guaranteeing zero co-location with commercial private tenants.

### Empanelment Criteria
Before a CSP can host government applications:
- Must undergo rigorous third-party auditing by the **Standardisation Testing and Quality Certification (STQC) Directorate**.
- Must certify adherence to ISO 27001, ISO 27017 (Cloud Security), ISO 27018 (Cloud Privacy), and MeitY SLA terms.""",
        activity_question="Under the Government of India's MeghRaj policy, which national directorate conducts third-party technical security audits before a Cloud Service Provider is empaneled by MeitY?",
        activity_options_json=json.dumps([
            "Standardisation Testing and Quality Certification (STQC) Directorate",
            "Local municipal telecommunications board",
            "International commercial advertising councils",
            "Private unaccredited software vendors"
        ]),
        activity_correct_option=0,
        activity_explanation="MeitY mandates rigorous third-party auditing by the STQC Directorate to verify technical security, physical separation, and SLA compliance before cloud providers can host government data.",
        order=1
    )

    l4_2 = Lesson(
        module_id=m4.id,
        title="Lesson 2: Sovereign Data Localization, Tenant Isolation & Audits",
        content_type="reading",
        duration_minutes=25,
        content="""# Sovereign Data Localization, Tenant Isolation & Security Audits

When civil servants architect e-governance systems (such as land records, health registries, or DBT databases) on cloud platforms, national sovereignty principles apply.

### Strict Data Localization Mandate
- **All customer data, transit data, and data at rest must remain strictly within India**.
- **Disaster Recovery (DR) and Near-DR Sites**: All replicated backups and secondary sites must also be located exclusively within the territorial borders of India.
- **Cross-Border Transfer Restrictions**: Indian government data cannot be replicated to foreign jurisdictions or subjected to foreign extra-territorial subpoenas without prior explicit authorization from the Ministry of Electronics & IT.

### Virtual and Physical Isolation Controls
1. **Virtual Private Cloud (VPC)**: Isolated network segments with dedicated subnets, security groups, and access control lists.
2. **Hardware Security Modules (HSM)**: Dedicated FIPS 140-2 Level 3 HSMs for customer-managed encryption keys, ensuring the cloud provider cannot decrypt government databases.
3. **Continuous Auditing**: Regular vulnerability assessments (VAPT) and red teaming conducted by CERT-In empaneled security auditing organizations.""",
        activity_question="What is the mandatory data localization policy for all Indian sovereign government and citizen records hosted on empaneled clouds under MeghRaj?",
        activity_options_json=json.dumps([
            "All primary data, secondary backups, and disaster recovery sites must reside strictly within the territorial boundaries of India",
            "Data can be freely backed up to any foreign data center without notification",
            "Only user passwords must remain in India, citizen data may be exported freely",
            "Backups must be distributed across overseas unverified cloud tenants"
        ]),
        activity_correct_option=0,
        activity_explanation="MeitY's cloud adoption framework strictly mandates that all government data, including replication, logs, and disaster recovery copies, must reside exclusively within the geographic borders of India.",
        order=2
    )
    db.add_all([l4_1, l4_2])
    db.flush()

    # ── MODULE 5: Digital Public Infrastructure (DPI / India Stack) ──────────
    m5 = Module(
        course_id=course.id,
        title="Module 5: Digital Public Infrastructure (DPI) & India Stack Integration",
        description="Aadhaar authentication protocols, DigiLocker gateways, PFMS Direct Benefit Transfer (DBT), and API Setu interoperability.",
        order=5
    )
    db.add(m5)
    db.flush()

    l5_1 = Lesson(
        module_id=m5.id,
        title="Lesson 1: Foundational DPI: Aadhaar Authentication & DigiLocker Gateways",
        content_type="reading",
        duration_minutes=25,
        content="""# Foundational DPI: Aadhaar Authentication & DigiLocker Gateways

India's **Digital Public Infrastructure (DPI / India Stack)** provides population-scale digital building blocks that enable inclusive public service delivery.

### 1. The Identity Layer: Aadhaar Architecture
- **Aadhaar Authentication API (UIDAI)**: Verifies identity in real-time using biometric (fingerprint/iris/face) or OTP authentication.
- **e-KYC Service**: Secure, paperless electronic Know Your Customer process returning cryptographically signed citizen identity demographic data.
- **Virtual ID (VID) and Aadhaar Masking**: Privacy-preserving mechanisms ensuring the 12-digit physical Aadhaar number is never stored in plain text across departmental databases.

### 2. The Document Layer: DigiLocker Ecosystem
Operated under Rule 9A of the **Information Technology (Preservation and Retention of Information by Intermediaries Providing Digital Locker Facilities) Rules, 2016**:
- Issued documents in DigiLocker are **deemed to be at par with original physical documents**.
- **Issuers**: Public universities, transport departments, CBSE, and tax departments push authenticated machine-readable XML/PDF records directly to a citizen's URI.
- **Requesters**: Government agencies query citizen credentials with citizen consent via secure API, eliminating physical attestation and fraudulent paper certificates.""",
        activity_question="Under Rule 9A of the Information Technology (Digital Locker) Rules, 2016, what is the legal status of digital documents pulled directly through the DigiLocker system?",
        activity_options_json=json.dumps([
            "They are legally deemed to be at par with original physical documents",
            "They are considered invalid hearsay unless re-attested by a gazetted officer on stamp paper",
            "They are only valid for 24 hours from download",
            "They require notarization at a district civil court"
        ]),
        activity_correct_option=0,
        activity_explanation="Rule 9A of the IT Rules 2016 explicitly provides that electronic documents issued into or pulled through DigiLocker shall be treated at par with original physical documents.",
        order=1
    )

    l5_2 = Lesson(
        module_id=m5.id,
        title="Lesson 2: Public Financial Management (PFMS DBT) & API Setu Interoperability",
        content_type="reading",
        duration_minutes=25,
        content="""# Public Financial Management (PFMS DBT) & API Setu Interoperability

### Direct Benefit Transfer (DBT) & PFMS
The **Public Financial Management System (PFMS)** administered by the Controller General of Accounts (CGA):
1. **Treasury Single Account (TSA)**: Funds remain in the Consolidated Fund of India until the exact moment of beneficiary release, eliminating parking of idle funds in commercial bank accounts.
2. **Aadhaar Payment Bridge (APB)**: Integrates PFMS with NPCI, routing welfare subsidies directly to the Aadhaar-seeded bank account of the beneficiary.
3. **Public Accounts Verification**: Validates account validity and IFSC formatting prior to disbursement, virtually eliminating ghost beneficiaries and payment leakages.

### API Setu (OpenForge) Data Exchange
**API Setu** serves as the Government of India's national data exchange highway:
- Enables seamless, consent-based, machine-to-machine data exchange between diverse ministries and state departments.
- Standardizes OpenAPI specifications and eliminates duplicate paperwork (e.g., verifying vehicle registration via Vahan API during subsidy verification).""",
        activity_question="How does the Public Financial Management System (PFMS) ensure just-in-time funding and eliminate leakage in Direct Benefit Transfer (DBT) schemes?",
        activity_options_json=json.dumps([
            "Direct electronic fund transfer via the Aadhaar Payment Bridge (APB) to verified beneficiary accounts without intermediary parking",
            "Disbursing physical currency through unverified local agents",
            "Retaining block allocations indefinitely in commercial investment funds",
            "Transferring welfare grants to unauthorized private trusts"
        ]),
        activity_correct_option=0,
        activity_explanation="PFMS integrates directly with the Treasury Single Account and the NPCI Aadhaar Payment Bridge, enabling direct just-in-time transfers into verified citizen bank accounts.",
        order=2
    )
    db.add_all([l5_1, l5_2])
    db.flush()

    # 5. Comprehensive Certification Assessment (15 MCQs across all 5 Domains)
    assessment = Assessment(
        course_id=course.id,
        title="Digital Governance & National Cyber Defense Certification Examination",
        description="Comprehensive official competency examination evaluating mastery across the 5 pillars of Indian digital governance: Cybersecurity & CERT-In Directives, Data Privacy (DPDP Act 2023), Public Key Infrastructure & Digital Signatures, Government Cloud (MeghRaj), and Digital Public Infrastructure (DPI / India Stack).",
        time_limit_minutes=30,
        pass_threshold_percent=70.0
    )
    db.add(assessment)
    db.flush()

    # 15 Detailed Civil-Service Level Questions
    questions_data = [
        # Domain 1: Cybersecurity & CERT-In Directives (Q1, Q2, Q3)
        (
            "Under the mandatory directions issued by CERT-In under Section 70B(6) of the Information Technology Act 2000, within what timeframe must a government ministry or critical intermediary report a confirmed cyber security incident?",
            [
                "Within 6 hours of noticing or being brought to notice of the incident",
                "Within 24 hours of concluding the internal departmental inquiry",
                "Within 72 hours of receiving a formal request from local police",
                "Within 15 days in the monthly security review brief"
            ],
            0,
            "CERT-In directions of 28 April 2022 strictly mandate that all government departments, intermediaries, and enterprises must report specified cyber incidents within six (6) hours of noticing them."
        ),
        (
            "Which national agency is designated under Section 70A of the Information Technology Act 2000 as the National Nodal Agency in respect of Critical Information Infrastructure Protection (CIIP) in India?",
            [
                "National Critical Information Infrastructure Protection Centre (NCIIPC)",
                "National Disaster Management Authority (NDMA)",
                "Telecom Regulatory Authority of India (TRAI)",
                "Press Council of India (PCI)"
            ],
            0,
            "Section 70A of the IT Act 2000 establishes the National Critical Information Infrastructure Protection Centre (NCIIPC) as the designated nodal agency for protecting national critical information infrastructure."
        ),
        (
            "During an investigation of an off-hours security alert on a core government portal, what is the critical reason for avoiding a hard power-down of the compromised server?",
            [
                "Powering down wipes volatile system memory (RAM), destroying crucial in-memory malware artifacts, network sockets, and decryption keys",
                "Powering down triggers an automatic hardware self-destruct mechanism",
                "Powering down cancels the server's cloud subscription immediately",
                "Powering down corrupts the physical power supply cables"
            ],
            0,
            "In forensic triage, live system memory (RAM) contains critical volatile artifacts (injected shellcode, active network connections, injected DLLs). Powering down destroys volatile evidence required under Section 65B of the Evidence Act."
        ),

        # Domain 2: Data Privacy & DPDP Act 2023 (Q4, Q5, Q6)
        (
            "Under the Digital Personal Data Protection Act, 2023 (DPDP Act), what is the statutory status of an Indian government ministry or department that determines the purpose and means of processing citizens' personal data?",
            [
                "Data Fiduciary",
                "Data Principal",
                "Commercial Intermediary",
                "Arbitration Tribunal"
            ],
            0,
            "Under Section 2(i) of the DPDP Act 2023, any entity, department, or company that determines the purpose and means of personal data processing is legally classified as a Data Fiduciary."
        ),
        (
            "What is the maximum monetary penalty that may be levied by the Data Protection Board of India on a Data Fiduciary for significant failure to take reasonable security safeguards to prevent a personal data breach under the DPDP Act 2023?",
            [
                "Up to ₹250 crore",
                "Up to ₹50 lakh",
                "Up to ₹10 crore",
                "A non-monetary formal administrative reprimand"
            ],
            0,
            "The Schedule to the DPDP Act 2023 prescribes financial penalties of up to ₹250 crore for significant failure to implement reasonable security safeguards to prevent personal data breach."
        ),
        (
            "Which mandatory statutory requirement applies exclusively to entities designated as 'Significant Data Fiduciaries' (SDF) under Section 10 of the DPDP Act 2023?",
            [
                "Appoint an India-resident Data Protection Officer (DPO) and conduct periodic Data Protection Impact Assessments (DPIA)",
                "Publish raw citizen biometric databases in open CSV format",
                "Offer all government public services completely free of internet connectivity",
                "Migrate all database servers exclusively to foreign cloud providers"
            ],
            0,
            "Section 10 of the DPDP Act 2023 mandates that Significant Data Fiduciaries must appoint an India-based DPO, retain an independent data auditor, and undertake periodic DPIAs."
        ),

        # Domain 3: Digital Signatures & PKI (Q7, Q8, Q9)
        (
            "Under Section 18 of the Information Technology Act 2000, which apex statutory authority operates the National Root CA (NRCAI) and licenses Certifying Authorities across India?",
            [
                "The Controller of Certifying Authorities (CCA)",
                "The Governor of the Reserve Bank of India",
                "The Ministry of Parliamentary Affairs",
                "The Chief Justice of High Courts"
            ],
            0,
            "The Controller of Certifying Authorities (CCA) operates the Root Certifying Authority of India (RCAI) under the IT Act 2000 and licenses Certifying Authorities like NICCA and CDAC."
        ),
        (
            "In government e-procurement and e-Office file notings, how does an asymmetric cryptographic digital signature (Class 3 DSC) guarantee non-repudiation?",
            [
                "The document hash is encrypted with the signer's secret private key, proving conclusively that only the holder of the token could have signed it",
                "By watermarking the officer's name in red ink on the computer monitor",
                "By locking the computer keyboard for 24 hours following signature generation",
                "By automatically converting the entire document into an uneditable image"
            ],
            0,
            "Under Sections 3 and 3A of the IT Act, asymmetric public key cryptography encrypts the file hash using the private key, binding the signatory to the document and establishing legal non-repudiation."
        ),
        (
            "Under Section 65B of the Indian Evidence Act, what is mandatory for electronic records (such as e-Office files, emails, or server logs) to be admissible as evidence in a court of law?",
            [
                "A signed Certificate under Section 65B identifying the record and certifying the operational integrity of the producing computer system",
                "A verbal endorsement by a private commercial notary",
                "A handwritten physical transcription on judicial stamp paper",
                "A certificate of export issued by an international courier"
            ],
            0,
            "Section 65B mandates that electronic records must be accompanied by an official certificate identifying the electronic record, describing the production device, and affirming regular operations."
        ),

        # Domain 4: Government Cloud / MeghRaj (Q10, Q11, Q12)
        (
            "Under the Government of India's GI Cloud (MeghRaj) adoption guidelines, which mandatory technical audit must a commercial Cloud Service Provider (CSP) complete before empanelment by MeitY?",
            [
                "Third-party security and controls audit conducted by the STQC Directorate",
                "Financial credit evaluation by foreign banking syndicates",
                "Consumer satisfaction survey by digital marketing agencies",
                "Visual website branding inspection by municipal authorities"
            ],
            0,
            "MeitY requires all CSPs seeking empanelment to undergo rigorous technical security, architectural, and isolation audits conducted by the STQC (Standardisation Testing and Quality Certification) Directorate."
        ),
        (
            "What is the Government of India's mandatory policy regarding data localization and replication for sovereign government cloud workloads under MeghRaj?",
            [
                "All customer data, backups, replication streams, and disaster recovery data centers must reside exclusively within the territory of India",
                "Backups may be mirrored to any overseas server without prior notification",
                "Data may reside offshore as long as encryption keys are held on an officer's phone",
                "Disaster recovery sites must be deployed in neutral international waters"
            ],
            0,
            "MeitY's cloud adoption framework mandates that all government data, including replication and disaster recovery copies, must reside strictly within the geographical boundaries of India."
        ),
        (
            "What is the primary architectural differentiator of a Government Community Cloud (GCC) compared to a public cloud deployment under MeghRaj?",
            [
                "GCC ensures dedicated physical and logical segregation exclusively for government entities, with zero co-tenancy with commercial private tenants",
                "GCC provides unlimited free computing hardware to private corporations",
                "GCC operates entirely without internet access or networking cables",
                "GCC allows anonymous citizen logins without authentication"
            ],
            0,
            "A Government Community Cloud (GCC) provides physically or logically isolated infrastructure dedicated exclusively to Indian government entities, preventing co-mingling with commercial tenants."
        ),

        # Domain 5: Digital Public Infrastructure (DPI / India Stack) (Q13, Q14, Q15)
        (
            "Under Rule 9A of the Information Technology (Preservation and Retention of Information by Intermediaries Providing Digital Locker Facilities) Rules, 2016, how are digital certificates pulled via DigiLocker treated?",
            [
                "They are deemed legally at par with original physical documents",
                "They are treated as inadmissible hearsay unless physically notarized",
                "They expire automatically within 48 hours of citizen download",
                "They can only be used for informal non-official communication"
            ],
            0,
            "Rule 9A of the IT Rules 2016 provides that electronic documents issued into or pulled through DigiLocker shall be treated legally at par with original physical documents."
        ),
        (
            "In the context of Direct Benefit Transfer (DBT) administration, what role does the NPCI Aadhaar Payment Bridge (APB) perform within the PFMS ecosystem?",
            [
                "Routes welfare subsidy disbursements directly to the citizen's Aadhaar-seeded bank account without requiring manual entry of account numbers and IFSC",
                "Acts as an unverified peer-to-peer cryptocurrency exchange",
                "Converts central government funds into retail department shopping coupons",
                "Stores unencrypted paper records of citizen welfare transactions"
            ],
            0,
            "The Aadhaar Payment Bridge (APB) administered by NPCI allows welfare departments to credit funds directly using Aadhaar numbers, eliminating payment failures caused by bank merger IFSC changes."
        ),
        (
            "What is the strategic objective of the Government of India's API Setu (OpenForge) platform in public service delivery?",
            [
                "Facilitate standardized, consent-based, machine-to-machine data exchange between diverse departmental applications, eliminating redundant physical document submissions",
                "Charge citizens convenience fees for browsing government websites",
                "Replace civil service officers with automated phone answering systems",
                "Restrict public access to official gazette notifications"
            ],
            0,
            "API Setu serves as the national API exchange highway, enabling real-time, consent-based verification of citizen records (driving licenses, caste certificates, land records) between disparate government systems."
        )
    ]

    for order_idx, (q_text, opts, correct_idx, expl) in enumerate(questions_data, start=1):
        q_obj = Question(
            assessment_id=assessment.id,
            text=q_text,
            options_json=json.dumps(opts),
            correct_option_index=correct_idx,
            explanation=expl,
            order=order_idx
        )
        db.add(q_obj)

    db.commit()
    print("Digital Governance & Cyber Defense curriculum and 15-question examination successfully seeded!")
