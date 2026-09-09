-- ========================================================
-- iGOT Karmayogi — Pre-Seeded Demonstration Data for Supabase
-- ========================================================

-- Seed departments
INSERT INTO departments (id, name, description) VALUES (1, 'Ministry of Statistics & Programme Implementation (MoSPI)', 'National statistical authority') ON CONFLICT DO NOTHING;
INSERT INTO departments (id, name, description) VALUES (2, 'National Sample Survey Office (NSSO)', 'Socio-economic sample surveys division') ON CONFLICT DO NOTHING;
INSERT INTO departments (id, name, description) VALUES (3, 'Central Statistics Office (CSO)', 'National accounts and price indices division') ON CONFLICT DO NOTHING;
INSERT INTO departments (id, name, description) VALUES (4, 'Institute of Secretariat Training & Management (ISTM)', 'Civil services management institute') ON CONFLICT DO NOTHING;
INSERT INTO departments (id, name, description) VALUES (5, 'Department of Personnel & Training (DoPT)', 'Civil services administrative cadre') ON CONFLICT DO NOTHING;

-- Seed skills
INSERT INTO skills (id, name, category) VALUES (1, 'Sample Survey Design & Sampling Techniques', 'Statistical Methodology') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (2, 'Consumer Price Index (CPI) & Inflation Analysis', 'Economic Statistics') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (3, 'Official Statistics Quality Framework (NQAF)', 'Data Governance') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (4, 'National Accounts Statistics & GDP Estimation', 'Economic Statistics') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (5, 'Digital Governance & PFMS Public Finance', 'Public Administration') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (6, 'Python & R for Public Sector Data Analytics', 'Data Science') ON CONFLICT DO NOTHING;
INSERT INTO skills (id, name, category) VALUES (7, 'Administrative Law & Official Procedures', 'Civil Service Ethics') ON CONFLICT DO NOTHING;

-- Seed users
INSERT INTO users (id, email, password_hash, full_name, role, is_active, created_at, updated_at) VALUES (1, 'admin@karmayogi.gov.in', '3c3eda828ff0185b93b1e428b7930fd0$72050005b368578c1599139ab986f77e6c4ec5f7322981315e8a60fd17c04546', 'Dr. Arvind Subramanian', 'admin', TRUE, '2026-09-09 19:01:20.949623', '2026-09-09 19:01:20.949623') ON CONFLICT DO NOTHING;
INSERT INTO users (id, email, password_hash, full_name, role, is_active, created_at, updated_at) VALUES (2, 'rajesh.kumar@mospi.gov.in', '88ec29d17fd11e795c74e9f402abc552$71da590fab5387cc1502dc68a992082f598c8a9a420b7de418cf2980abc8a6ad', 'Rajesh Kumar', 'learner', TRUE, '2026-09-09 19:01:21.033025', '2026-09-09 19:01:21.033025') ON CONFLICT DO NOTHING;
INSERT INTO users (id, email, password_hash, full_name, role, is_active, created_at, updated_at) VALUES (3, 'priya.sharma@mospi.gov.in', '17d540e8b28b103db7488d61947106ac$73fd86f36704d6f568169cf4004c4e98bc8c1d902489f7b6c7ebb41fad7a7962', 'Priya Sharma', 'learner', TRUE, '2026-09-09 19:01:21.114592', '2026-09-09 19:01:21.114592') ON CONFLICT DO NOTHING;

-- Seed user_profiles
INSERT INTO user_profiles (id, user_id, phone, bio, education, work_experience_years, prior_training, designation, department, job_role, current_assignment, areas_of_interest, language_pref, appearance_pref, profile_pic_url, onboarding_completed, daily_goal_minutes, current_streak_days, last_active_date, created_at, updated_at) VALUES (1, 1, '+91 98100 12345', 'Director General, National Statistical Systems Training Academy (NSSTA). Oversight of capacity building for Indian Statistical Service (ISS) officers.', 'Ph.D. in Econometrics, Delhi School of Economics', 22, 'LBSNAA Senior Leadership Program, IMF National Accounts Fellowship', 'Director General', 'Ministry of Statistics & Programme Implementation (MoSPI)', 'Institutional Capacity & Training Administrator', 'Oversight of ISS Cadre Training & Karmayogi Statistical Curriculum', 'National Accounts, Capacity Building, Data Governance', 'en', 'light', NULL, TRUE, 45, 14, '2026-09-09 19:01:21.035038', '2026-09-09 19:01:21.035038', '2026-09-09 19:01:21.035038') ON CONFLICT DO NOTHING;
INSERT INTO user_profiles (id, user_id, phone, bio, education, work_experience_years, prior_training, designation, department, job_role, current_assignment, areas_of_interest, language_pref, appearance_pref, profile_pic_url, onboarding_completed, daily_goal_minutes, current_streak_days, last_active_date, created_at, updated_at) VALUES (2, 2, '+91 98765 43210', 'Senior Statistical Officer in National Accounts Division, MoSPI. Passionate about price statistics and automated sample validation.', 'M.Sc. Statistics, Banaras Hindu University', 8, 'NSSTA Foundation Course, ISTM Public Procurement', 'Senior Statistical Officer (SSO)', 'Central Statistics Office (CSO)', 'Price Indices and Monthly CPI Compilation', 'Urban Consumer Basket Weight Revision 2026', 'Inflation Metrics, Sample Survey Design, Python Automation', 'en', 'light', NULL, TRUE, 30, 6, '2026-09-09 19:01:21.114592', '2026-09-09 19:01:21.115598', '2026-09-09 19:01:21.115598') ON CONFLICT DO NOTHING;
INSERT INTO user_profiles (id, user_id, phone, bio, education, work_experience_years, prior_training, designation, department, job_role, current_assignment, areas_of_interest, language_pref, appearance_pref, profile_pic_url, onboarding_completed, daily_goal_minutes, current_streak_days, last_active_date, created_at, updated_at) VALUES (3, 3, '+91 99112 88344', 'Assistant Director (ISS 2024 Batch), NSSO Field Operations Division.', 'M.Stat, Indian Statistical Institute (ISI) Kolkata', 2, 'Foundation Course at LBSNAA', 'Assistant Director', 'National Sample Survey Office (NSSO)', 'Field Survey Supervision & Quality Control', NULL, NULL, 'en', 'light', NULL, FALSE, 30, 1, '2026-09-09 19:01:21.115598', '2026-09-09 19:01:21.115598', '2026-09-09 19:01:21.115598') ON CONFLICT DO NOTHING;

-- Seed courses
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (1, 'Fundamentals of National Sample Surveys (NSS)', 'Master the methodological framework of large-scale socio-economic surveys conducted by India''s National Sample Survey Office (NSSO). Covers multi-stage stratified sampling, field schedules, non-sampling error minimization, and computer-assisted personal interviewing (CAPI).', 'Prof. M. R. Saluja & Smt. Ananya Sen, ISS', 'National Sample Survey Office (NSSO)', 6.5, 'intermediate', 'internal', 'Sample Surveys', NULL, 4.9, 1420, TRUE, FALSE, '2026-09-09 19:01:21.122747') ON CONFLICT DO NOTHING;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (2, 'Compilation of Consumer Price Index (CPI) & Inflation Metrics', 'Comprehensive practical guide to the compilation of All India Consumer Price Index (Rural, Urban, Combined). Learn item basket weighting, Laspeyres index formulation, geometric mean of price relatives, treatment of seasonal goods, and house rent imputation.', 'Dr. P. C. Mohanan & Shri Sunil Jain', 'Central Statistics Office (CSO)', 5.0, 'advanced', 'internal', 'Price Statistics', NULL, 4.85, 980, TRUE, TRUE, '2026-09-09 19:01:21.130370') ON CONFLICT DO NOTHING;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (3, 'Data Quality Frameworks & Official Statistics in India', 'Aligning Indian official statistics with the United Nations National Quality Assurance Framework (UN-NQAF). Study the 19 principles of statistical integrity, confidentiality safeguards, revision policies, and metadata standards.', 'Dr. G. C. Manna', 'National Statistical Systems Training Academy (NSSTA)', 4.0, 'beginner', 'internal', 'Data Governance', NULL, 4.75, 640, FALSE, TRUE, '2026-09-09 19:01:21.132372') ON CONFLICT DO NOTHING;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (4, 'Digital Governance & Public Financial Management System (PFMS)', 'Direct Benefit Transfer (DBT), treasury integration, electronic bill processing, and expenditure tracking through PFMS. Authorized course accredited by ISTM for all central government employees.', 'Shri V. Ramaswamy, IDAS', 'Institute of Secretariat Training & Management (ISTM)', 7.0, 'intermediate', 'external', 'Public Administration', NULL, 4.92, 2150, TRUE, FALSE, '2026-09-09 19:01:21.134370') ON CONFLICT DO NOTHING;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (5, 'Python and Statistical Computing for Public Policy', 'Modern data analysis for official statisticians using Pandas, NumPy, and Statsmodels. Automate data cleaning, compute econometric models, and generate reproducible policy briefs.', 'Dr. Tanvi Grover', 'MoSPI Data Lab', 8.0, 'intermediate', 'internal', 'Data Science', NULL, 4.95, 1680, TRUE, TRUE, '2026-09-09 19:01:21.135450') ON CONFLICT DO NOTHING;

-- Seed modules
INSERT INTO modules (id, course_id, title, description, "order") VALUES (1, 1, 'Module 1: Sampling Design & Frame Construction', 'Principles of probability proportional to size (PPS) sampling in rural and urban frames.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (2, 1, 'Module 2: Field Schedules & CAPI Execution', 'Administering household schedule 1.0 and enterprise survey instruments digitally.', 2) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (3, 1, 'Module 3: Multiplier Generation & Estimation', 'Deriving pooled estimates and standard errors across state and central samples.', 3) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (4, 2, 'Module 1: Index Formulation & Basket Selection', 'Mathematical foundations of modified Laspeyres and Jevons price relatives.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (5, 2, 'Module 2: Imputation & Quality Adjustment', 'Techniques for disappearing items and seasonal vegetables.', 2) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (6, 3, 'Module 1: Principles of Official Statistics', 'Institutional environment, objectivity, and confidentiality.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (7, 4, 'Module 1: PFMS Architecture & DBT Portals', 'Integration between state treasuries, central ministries, and NPCI Aadhaar payment bridge.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (8, 5, 'Module 1: Data Wrangling with Pandas', 'Cleaning messy ministerial Excel sheets and CSV survey microdata.', 1) ON CONFLICT DO NOTHING;

-- Seed lessons
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (1, 1, 'Lesson 1: Structure of the First Stage Units (FSUs)', 'reading', 20, '# Structure of First Stage Units (FSUs) in NSS Surveys

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

> **Key Rule for Field Investigators**: An FSU cannot be substituted without prior written authorization from the Deputy Director of the Regional Office.', NULL, 'In rural NSS surveys, what is typically designated as the First Stage Unit (FSU)?', '["A census village", "An individual agricultural household", "A whole administrative district", "A block development office"]', 0, 'In rural sector surveys of the NSSO, the First Stage Unit (FSU) is universally defined as the census village (or panchayat ward in select states).', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (2, 1, 'Lesson 2: Hamlet-Group and Sub-Block Formation', 'video', 25, '# Hamlet-Group and Sub-Block Formation Rules

When an FSU is very large in terms of present population (usually exceeding 1,200 persons or 300 households), administering a total listing becomes cost-prohibitive.

### Delineation Procedures
1. Divide the FSU into an equal number of hamlet-groups (hg) or sub-blocks (sb) of approximately equal population size.
2. Ensure each hamlet-group has distinct, permanent natural boundaries (roads, water channels, railway lines).
3. Select two hamlet-groups for sample listing:
   - **hg 1**: Hamlet group with highest concentration of vulnerable/target population (selected purposively).
   - **hg 2**: Selected randomly from the remaining hamlet groups with equal probability.

This dual-selection design safeguards representation of target socio-economic strata while preserving unbiased estimation.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'When is hamlet-group (hg) formation mandatory in a rural NSS sample village?', '["Whenever the village exceeds 1,200 population or ~300 households", "Only when requested by the village Sarpanch", "Only if the village has no electricity", "In every single sample village regardless of population"]', 0, 'Per NSS field manual standards, hamlet-group formation is mandatory when the current village population exceeds approximately 1,200 persons or 300 households.', 2) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (3, 2, 'Lesson 3: Digitized CAPI Data Validation Checks', 'lab', 30, '# Digital CAPI Data Validation & Range Checks

With the transition to tablet-based CAPI (Computer-Assisted Personal Interviewing), real-time validation prevents inconsistencies at the point of data capture.

### Essential Consistency Checks
- **Age vs. Education Grade**: An individual under 14 cannot have an advanced post-graduate degree recorded.
- **Consumption Expenditure Balance**: Total monthly per-capita expenditure (MPCE) must cross-validate with food and non-food sub-aggregates within ±2%.
- **Land Possessed vs. Land Cultivated**: Land cultivated cannot exceed land possessed without corresponding leased-in land entries.

Field Supervisors must execute the digital integrity audit script before transmitting batches to the state server.', NULL, 'What is the primary benefit of CAPI over traditional paper schedules in NSS surveys?', '["Immediate automated logical validation and elimination of data entry backlogs", "Eliminating the need to train field investigators", "Allowing investigators to skip household visits", "Permitting non-random household replacements"]', 0, 'CAPI eliminates physical paper transit delays, automates routing logic, and performs immediate validation checks right at the respondent''s doorstep.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (4, 4, 'Lesson 1: The Modified Laspeyres Price Index Formula', 'reading', 25, '# The Modified Laspeyres Formula in CPI Compilation

In India''s official CPI (Base 2012=100), elementary price indices are aggregated using a **Modified Laspeyres Formula**:

$$I = \sum \left[ W_i \times \left( \frac{P_{i,t}}{P_{i,0}} \right) \right]$$

Where:
- $W_i$ is the normalized expenditure weight of item $i$ derived from the Consumer Expenditure Survey (CES).
- $P_{i,t}$ is the current period average price of item $i$.
- $P_{i,0}$ is the base year price of item $i$.

### Elementary Aggregation with Jevons
At the market level, price quotations for a specific item across multiple selected shops are aggregated using the **Geometric Mean (Jevons Index)** rather than the simple arithmetic mean to prevent upward substitution bias.', NULL, 'Which index formula is employed at the elementary quotation level to minimize substitution bias?', '["Geometric Mean (Jevons Index)", "Simple Harmonic Mean", "Carli Arithmetic Index", "Dutot Ratio of Averages"]', 0, 'International best practices and MoSPI guidelines use the Geometric Mean (Jevons) at the elementary quotation level because it exhibits transitivity and minimizes substitution bias.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (5, 6, 'Lesson 1: UN Fundamental Principles of Official Statistics', 'reading', 15, '# UN Fundamental Principles of Official Statistics

Adopted by the United Nations General Assembly in 2014, these ten principles form the bedrock of official statistical systems:

1. **Relevance, Impartiality, and Equal Access**: Official statistics must represent public goods available to all citizens simultaneously.
2. **Professional Standards and Ethics**: Concepts and procedures must adhere purely to scientific statistical discipline without political intervention.
3. **Accountability and Transparency**: Presentation of sources and methods to facilitate interpretation.
4. **Prevention of Misuse**: The statistical agency has the duty to comment on erroneous interpretation.
5. **Confidentiality**: Individual data collected for statistical compilation must remain strictly confidential and never used for non-statistical purposes.', NULL, 'Under the UN Fundamental Principles, can census or survey response data of an individual be shared for law enforcement or taxation?', '["No, individual survey records are strictly confidential and protected by law", "Yes, if requested by local police", "Yes, provided the respondent paid tax", "Yes, after 1 year has elapsed"]', 0, 'Principle 5 mandates absolute confidentiality: data collected by statistical agencies for compilation must remain strictly confidential and never used for investigation or taxation.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (6, 7, 'Lesson 1: Treasury Single Account (TSA) Mechanism', 'reading', 20, '# The Treasury Single Account (TSA) and Just-in-Time Funding

The Treasury Single Account (TSA) system administered via PFMS ensures that government funds remain in the Consolidated Fund of India until the exact moment of payment to the ultimate vendor or beneficiary.

### Key Features
- Eliminates parking of unspent budgetary allocations in commercial bank accounts.
- Daily sweeping of balances to RBI.
- Real-time visibility into program expenditures for Central Sector Schemes.', NULL, 'What is the primary objective of implementing the Treasury Single Account (TSA) through PFMS?', '["To prevent parking of government funds in bank accounts and ensure just-in-time funding", "To increase paperwork in regional accounting offices", "To delay payments to social benefit recipients", "To replace commercial banks entirely"]', 0, 'TSA ensures that public funds stay in the Consolidated Fund of India until immediate disbursement, eliminating idle parked balances.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (7, 8, 'Lesson 1: Vectorized Operations on NSS Microdata', 'lab', 35, '# Vectorized Operations on Microdata using Pandas

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

Vectorized operations execute in optimized C routines, yielding up to a 100x speedup over iterative loops.', NULL, 'Why should vectorized methods be preferred over row-by-row for-loops in Pandas when processing large survey datasets?', '["Vectorized calculations run in compiled C routines and are orders of magnitude faster", "Because for-loops are deprecated in Python 3.12", "Because vectorized methods use less hard disk space", "Because Pandas does not support for-loops"]', 0, 'Pandas vectorization delegates calculations to internal compiled NumPy C code, executing operations across whole memory blocks without Python interpreter overhead.', 1) ON CONFLICT DO NOTHING;

-- Seed course_skills
INSERT INTO course_skills (id, course_id, skill_id) VALUES (1, 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (2, 2, 2) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (3, 3, 3) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (4, 4, 5) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (5, 5, 6) ON CONFLICT DO NOTHING;

-- Seed user_skills
INSERT INTO user_skills (id, user_id, skill_id, source_course_id, acquired_at) VALUES (1, 2, 3, 3, '2026-09-09 19:01:21.179492') ON CONFLICT DO NOTHING;

-- Seed enrollments
INSERT INTO enrollments (id, user_id, course_id, status, started_at, completed_at, progress_percent, last_lesson_id) VALUES (1, 2, 1, 'in_progress', '2026-09-05 19:01:21.165069', NULL, 66.7, 2) ON CONFLICT DO NOTHING;

-- Seed progress_records
INSERT INTO progress_records (id, enrollment_id, module_id, lesson_id, completed, activity_completed, updated_at) VALUES (1, 1, 1, 1, TRUE, TRUE, '2026-09-09 19:01:21.177958') ON CONFLICT DO NOTHING;
INSERT INTO progress_records (id, enrollment_id, module_id, lesson_id, completed, activity_completed, updated_at) VALUES (2, 1, 1, 2, TRUE, TRUE, '2026-09-09 19:01:21.177958') ON CONFLICT DO NOTHING;

-- Seed assessments
INSERT INTO assessments (id, course_id, title, description, time_limit_minutes, pass_threshold_percent) VALUES (1, 1, 'Comprehensive Competency Assessment: National Sample Surveys', 'Official certification examination testing sampling design, stratification rigor, hamlet-group formation, and CAPI field validation procedures.', 25, 70.0) ON CONFLICT DO NOTHING;
INSERT INTO assessments (id, course_id, title, description, time_limit_minutes, pass_threshold_percent) VALUES (2, 2, 'Certification Exam: Consumer Price Index (CPI) Compilation', 'Assesses mastery of price aggregation, Laspeyres index methodology, and outlier handling.', 20, 70.0) ON CONFLICT DO NOTHING;

-- Seed questions
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (1, 1, 'In a two-stage stratified sampling design used in NSS rural rounds, what represents the First Stage Unit (FSU)?', '["A census village / revenue village", "An individual agricultural household", "A block development administrative zone", "A district statistical office"]', 0, 'Census villages serve as the standard FSUs in the rural frame of NSS surveys.', 1) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (2, 1, 'When is hamlet-group (hg) formation compulsory in a sample village during NSS field execution?', '["When current village population is approx. 1,200 or more (or 300+ households)", "Only if there are more than 5 distinct castes", "Whenever the field supervisor forgets paper schedules", "In every sample village without exception"]', 0, 'NSS field manual prescribes hamlet group division when population reaches or exceeds 1,200 persons or 300 households.', 2) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (3, 1, 'What is the primary objective of Computer-Assisted Personal Interviewing (CAPI) in NSSO?', '["Eliminate data-entry backlogs and enforce automated real-time logical validation", "Permit investigators to complete surveys without respondent interaction", "Reduce the total sample size by half", "Eliminate the need for statistical multipliers"]', 0, 'CAPI captures responses digitally on tablets, enforcing validation constraints at the point of capture and removing post-survey data entry delays.', 3) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (4, 1, 'Which sampling selection method is used when allocating FSUs to account for population size differentials?', '["Probability Proportional to Size with Replacement / Without Replacement (PPS)", "Simple Random Sampling with Equal Probability (SRSWOR)", "Convenience Snowball Sampling", "Voluntary Respondent Selection"]', 0, 'PPS (Probability Proportional to Size) selection gives larger population units a proportionally higher likelihood of inclusion, optimizing efficiency.', 4) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (5, 2, 'At the elementary price quotation level, which average is recommended to eliminate upward substitution bias?', '["Geometric Mean (Jevons Index)", "Harmonic Mean", "Simple Arithmetic Mean (Carli)", "Mode of reported prices"]', 0, 'The geometric mean (Jevons) satisfies axiomatic time-reversal and treats price relatives symmetrically, minimizing substitution bias.', 1) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (6, 2, 'The item basket weights in the All-India CPI are fundamentally derived from which statistical source?', '["Household Consumer Expenditure Survey (CES / HCES)", "Annual Survey of Industries (ASI)", "Reserve Bank of India Monetary Policy Report", "Census decennial headcounts"]', 0, 'CPI item weights reflect consumer spending patterns measured directly in the nationwide Household Consumer Expenditure Survey.', 2) ON CONFLICT DO NOTHING;

-- Seed planned_courses
INSERT INTO planned_courses (id, user_id, course_id, planned_for, "source", created_at) VALUES (1, 2, 2, 'Q4 2026', 'self', '2026-09-09 19:01:21.176960') ON CONFLICT DO NOTHING;

-- Seed learning_history
INSERT INTO learning_history (id, user_id, course_id, viewed_at) VALUES (1, 2, 1, '2026-09-09 17:01:21.173957') ON CONFLICT DO NOTHING;
INSERT INTO learning_history (id, user_id, course_id, viewed_at) VALUES (2, 2, 3, '2026-09-08 19:01:21.173957') ON CONFLICT DO NOTHING;

-- Update serial sequence counters in PostgreSQL
SELECT setval(pg_get_serial_sequence('departments', 'id'), COALESCE(MAX(id), 1)) FROM departments;
SELECT setval(pg_get_serial_sequence('skills', 'id'), COALESCE(MAX(id), 1)) FROM skills;
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1)) FROM users;
SELECT setval(pg_get_serial_sequence('user_profiles', 'id'), COALESCE(MAX(id), 1)) FROM user_profiles;
SELECT setval(pg_get_serial_sequence('courses', 'id'), COALESCE(MAX(id), 1)) FROM courses;
SELECT setval(pg_get_serial_sequence('modules', 'id'), COALESCE(MAX(id), 1)) FROM modules;
SELECT setval(pg_get_serial_sequence('lessons', 'id'), COALESCE(MAX(id), 1)) FROM lessons;
SELECT setval(pg_get_serial_sequence('course_skills', 'id'), COALESCE(MAX(id), 1)) FROM course_skills;
SELECT setval(pg_get_serial_sequence('user_skills', 'id'), COALESCE(MAX(id), 1)) FROM user_skills;
SELECT setval(pg_get_serial_sequence('enrollments', 'id'), COALESCE(MAX(id), 1)) FROM enrollments;
SELECT setval(pg_get_serial_sequence('progress_records', 'id'), COALESCE(MAX(id), 1)) FROM progress_records;
SELECT setval(pg_get_serial_sequence('assessments', 'id'), COALESCE(MAX(id), 1)) FROM assessments;
SELECT setval(pg_get_serial_sequence('questions', 'id'), COALESCE(MAX(id), 1)) FROM questions;
SELECT setval(pg_get_serial_sequence('assessment_attempts', 'id'), COALESCE(MAX(id), 1)) FROM assessment_attempts;
SELECT setval(pg_get_serial_sequence('planned_courses', 'id'), COALESCE(MAX(id), 1)) FROM planned_courses;
SELECT setval(pg_get_serial_sequence('learning_history', 'id'), COALESCE(MAX(id), 1)) FROM learning_history;
