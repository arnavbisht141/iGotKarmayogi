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
