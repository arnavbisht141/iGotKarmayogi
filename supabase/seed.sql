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

-- Seed courses (4 Flagship Competency Verticals)
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (1, 'Civil Service Conduct, Administrative Ethics & Interpersonal Leadership', 'Master statutory administrative ethics, CCS (Conduct) Rules 1964, Rule 14 disciplinary inquiries, natural justice doctrines, public grievance redressal, high-stakes stakeholder negotiation, and oral civil service defense.', 'Smt. Rashmi Verma, IAS (Retd.) & Shri P. K. Basu', 'Department of Personnel & Training (DoPT)', 6.0, 'intermediate', 'internal', 'Behavioural', NULL, 4.92, 1850, TRUE, TRUE, '2026-09-09 19:01:21.122747') ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, overview = EXCLUDED.overview, instructor = EXCLUDED.instructor, organization = EXCLUDED.organization, category = EXCLUDED.category;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (2, 'Compilation of Consumer Price Index (CPI) & Inflation Metrics', 'Comprehensive practical guide to the compilation of All India Consumer Price Index (Rural, Urban, Combined). Learn item basket weighting, Laspeyres index formulation, geometric mean of price relatives, treatment of seasonal goods, and house rent imputation.', 'Dr. P. C. Mohanan & Shri Sunil Jain', 'Central Statistics Office (CSO)', 5.0, 'advanced', 'internal', 'Statistical', NULL, 4.88, 1420, TRUE, FALSE, '2026-09-09 19:01:21.130370') ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, overview = EXCLUDED.overview, category = EXCLUDED.category;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (3, 'Python and Data Cleaning Pipelines for Public Policy', 'Modern automated data cleaning and reproducible data processing for civil service analysts using Pandas, NumPy, and Statsmodels. Automate messy survey ingestion, missing data imputation, schema validation, and pipeline orchestration.', 'Dr. Tanvi Grover & Prof. Rajesh Sen', 'MoSPI Data Lab', 8.0, 'intermediate', 'internal', 'Technical', NULL, 4.95, 1680, TRUE, TRUE, '2026-09-09 19:01:21.135450') ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, overview = EXCLUDED.overview, category = EXCLUDED.category;
INSERT INTO courses (id, title, overview, instructor, organization, duration_hours, difficulty, "source", category, thumbnail_url, rating, enrolled_count, is_popular, is_new, created_at) VALUES (4, 'Cybersecurity Defense & Digital Public Infrastructure Governance', 'Critical information infrastructure protection, CERT-In compliance directives, cyber incident response, Treasury Single Account (TSA) controls, and secure Direct Benefit Transfer (DBT) workflows across government platforms.', 'Shri V. Ramaswamy, IDAS & CERT-In Directorate', 'National Critical Information Infrastructure Protection Centre (NCIIPC)', 7.0, 'intermediate', 'external', 'Digital Governance', NULL, 4.91, 2150, TRUE, FALSE, '2026-09-09 19:01:21.134370') ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, overview = EXCLUDED.overview, category = EXCLUDED.category;

-- Seed modules
INSERT INTO modules (id, course_id, title, description, "order") VALUES (1, 1, 'Module 1: Statutory Code of Conduct & Ethics', 'CCS (Conduct) Rules 1964, integrity standards, and avoidance of conflict of interest.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (2, 1, 'Module 2: Quasi-Judicial Inquiries & Natural Justice', 'Conducting departmental proceedings under Rule 14 CCS (CCA) Rules.', 2) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (3, 1, 'Module 3: Administrative Negotiation & Public Leadership', 'High-pressure public communication, grievance redressal, and crisis leadership.', 3) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (4, 2, 'Module 1: Index Formulation & Basket Selection', 'Mathematical foundations of modified Laspeyres and Jevons price relatives.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (5, 2, 'Module 2: Imputation & Quality Adjustment', 'Techniques for disappearing items and seasonal goods.', 2) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (6, 3, 'Module 1: Data Wrangling & Cleaning with Pandas', 'Automating survey cleaning, missing value imputation, and reproducible pipelines.', 1) ON CONFLICT DO NOTHING;
INSERT INTO modules (id, course_id, title, description, "order") VALUES (7, 4, 'Module 1: Cyber Defense & PFMS Treasury Controls', 'Critical information infrastructure protection, CERT-In compliance, and TSA integration.', 1) ON CONFLICT DO NOTHING;

-- Seed lessons
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (1, 1, 'Lesson 1: Statutory Framework of CCS (Conduct) Rules, 1964', 'reading', 20, '# Statutory Framework of CCS (Conduct) Rules, 1964

Every civil servant in the Government of India is governed by the statutory provisions of the **Central Civil Services (Conduct) Rules, 1964**:

1. **Rule 3 — General Principles of Integrity**:
   - Maintain absolute integrity, devotion to duty, and do nothing unbecoming of a Government servant.
   - Uphold supremacy of the Constitution and democratic values.
   - Defend impartiality, political neutrality, and fairness in administrative decision-making.

2. **Rule 3C — Prohibition of Sexual Harassment**:
   - Prevention of Sexual Harassment of Women at Workplace (POSH Act) compliance.

> **Doctrine**: Discretionary administrative powers must be exercised strictly within statutory limits, guided by public interest without personal or pecuniary bias.', NULL, 'Under Rule 3 of the CCS (Conduct) Rules, what is the paramount obligation of an administrative officer?', '["To maintain absolute integrity, devotion to duty, and political neutrality", "To obey verbal instructions from non-official acquaintances", "To maximize fee collections arbitrarily", "To bypass statutory tender processes"]', 0, 'Rule 3(1) mandates absolute integrity, dedication to duty, and conduct worthy of an officer of the State.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (2, 2, 'Lesson 2: Principles of Natural Justice (Audi Alteram Partem)', 'video', 25, '# Audi Alteram Partem in Departmental Proceedings

In any quasi-judicial proceeding governed by Rule 14 of CCS (CCA) Rules, 1965:

1. **Right to Notice**:
   - Form 1 charge-sheet containing definite articles of charge, statement of imputations, and list of documents/witnesses.
2. **Right of Inspection**:
   - Under Rule 14(11), the Charged Officer must be permitted full physical or certified digital access to listed documentary evidence.
3. **Impartial Inquiring Authority**:
   - The IA acts as an independent quasi-judicial evaluator, not a prosecutor.', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'What does the doctrine of Audi Alteram Partem require during a Rule 14 inquiry?', '["Granting fair hearing and opportunity to inspect evidence and cross-examine witnesses", "Allowing the prosecution to hide confidential witness statements", "Ordering immediate punishment without recording evidence", "Conducting ex-parte hearings without notice"]', 0, 'Audi Alteram Partem guarantees no person shall be condemned unheard, requiring evidence disclosure and right of defense.', 2) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (3, 4, 'Lesson 1: The Modified Laspeyres Price Index Formula', 'reading', 25, '# The Modified Laspeyres Formula in CPI Compilation

In India''s official CPI (Base 2012=100), elementary price indices are aggregated using a **Modified Laspeyres Formula**:

$$I = \sum \left[ W_i \times \left( \frac{P_{i,t}}{P_{i,0}} \right) \right]$$

### Elementary Aggregation with Jevons
At the market level, price quotations across selected shops are aggregated using the **Geometric Mean (Jevons Index)** rather than the simple arithmetic mean to prevent upward substitution bias.', NULL, 'Which index formula is employed at the elementary quotation level to minimize substitution bias?', '["Geometric Mean (Jevons Index)", "Simple Harmonic Mean", "Carli Arithmetic Index", "Dutot Ratio of Averages"]', 0, 'International best practices and MoSPI guidelines use the Geometric Mean (Jevons) at the elementary quotation level because it exhibits transitivity and minimizes substitution bias.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (4, 6, 'Lesson 1: Vectorized Data Wrangling on Survey Microdata', 'lab', 35, '# Vectorized Data Wrangling with Pandas

When processing large-scale public policy microdata, traditional Python `for` loops cause severe execution bottlenecks.

```python
import pandas as pd
import numpy as np

# Load microdata
df = pd.read_csv("survey_microdata.csv")

# Vectorized weighted calculation
df["weighted_val"] = df["val"] * df["weight"] / 100
```

Vectorized operations execute in compiled C routines, yielding massive performance speedups over iterative loops.', NULL, 'Why should vectorized methods be preferred over row-by-row for-loops in Pandas?', '["Vectorized calculations run in compiled C routines and are orders of magnitude faster", "Because for-loops are deprecated in Python 3.12", "Because vectorized methods use less hard disk space", "Because Pandas does not support for-loops"]', 0, 'Pandas vectorization delegates calculations to compiled NumPy C routines without Python interpreter loop overhead.', 1) ON CONFLICT DO NOTHING;
INSERT INTO lessons (id, module_id, title, content_type, duration_minutes, content, video_url, activity_question, activity_options_json, activity_correct_option, activity_explanation, "order") VALUES (5, 7, 'Lesson 1: Treasury Single Account (TSA) & Cyber Hardening', 'reading', 20, '# Treasury Single Account (TSA) & Critical Infrastructure Protection

The Treasury Single Account (TSA) administered via PFMS ensures that government scheme funds remain in the Consolidated Fund of India until actual electronic disbursement.

### Cyber Safeguards
- End-to-end PKI signature validation for all e-bills.
- Mandatory 2FA and CERT-In compliant logging of system transactions.', NULL, 'What is the primary objective of implementing the Treasury Single Account (TSA) through PFMS?', '["To prevent parking of government funds in bank accounts and ensure just-in-time funding", "To increase paperwork in regional accounting offices", "To delay payments to social benefit recipients", "To replace commercial banks entirely"]', 0, 'TSA ensures that public funds stay in the Consolidated Fund of India until immediate disbursement, eliminating idle parked balances.', 1) ON CONFLICT DO NOTHING;

-- Seed course_skills
INSERT INTO course_skills (id, course_id, skill_id) VALUES (1, 1, 7) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (2, 2, 2) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (3, 3, 6) ON CONFLICT DO NOTHING;
INSERT INTO course_skills (id, course_id, skill_id) VALUES (4, 4, 5) ON CONFLICT DO NOTHING;

-- Seed user_skills
INSERT INTO user_skills (id, user_id, skill_id, source_course_id, acquired_at) VALUES (1, 2, 3, 3, '2026-09-09 19:01:21.179492') ON CONFLICT DO NOTHING;

-- Seed enrollments
INSERT INTO enrollments (id, user_id, course_id, status, started_at, completed_at, progress_percent, last_lesson_id) VALUES (1, 2, 1, 'in_progress', '2026-09-05 19:01:21.165069', NULL, 66.7, 2) ON CONFLICT DO NOTHING;

-- Seed progress_records
INSERT INTO progress_records (id, enrollment_id, module_id, lesson_id, completed, activity_completed, updated_at) VALUES (1, 1, 1, 1, TRUE, TRUE, '2026-09-09 19:01:21.177958') ON CONFLICT DO NOTHING;
INSERT INTO progress_records (id, enrollment_id, module_id, lesson_id, completed, activity_completed, updated_at) VALUES (2, 1, 1, 2, TRUE, TRUE, '2026-09-09 19:01:21.177958') ON CONFLICT DO NOTHING;

-- Seed assessments
INSERT INTO assessments (id, course_id, title, description, time_limit_minutes, pass_threshold_percent) VALUES (1, 1, 'Certification Exam: Civil Service Conduct & Administrative Ethics', 'Official certification examination testing statutory integrity standards, CCS (Conduct) Rules 1964, natural justice principles, and Rule 14 inquiry procedures.', 25, 70.0) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;
INSERT INTO assessments (id, course_id, title, description, time_limit_minutes, pass_threshold_percent) VALUES (2, 2, 'Certification Exam: Consumer Price Index (CPI) Compilation', 'Assesses mastery of price aggregation, Laspeyres index methodology, and outlier handling.', 20, 70.0) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, description = EXCLUDED.description;

-- Seed questions
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (1, 1, 'Under Rule 14(11) of the CCS (CCA) Rules 1965, what right does the Charged Officer have regarding documentary evidence?', '["Absolute right to inspect and receive certified copies of listed prosecution documents", "No right to inspect documents until final judgment", "Only verbal summary by the Presenting Officer", "Inspection permitted only after prosecution concludes witnesses"]', 0, 'Rule 14(11) guarantees the statutory right of the Charged Officer to inspect listed documents to prepare their defense.', 1) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (2, 1, 'What is the consequence if an Inquiring Authority proceeds ex-parte after a formal application alleging bias has been filed?', '["Proceedings are fatally vitiated for violating Audi Alteram Partem and will be quashed", "The inquiry is accelerated lawfully", "The officer automatically forfeits defense rights", "The Inquiring Authority receives special commendation"]', 0, 'Per established DoPT guidelines and judicial precedents, the IA must stay proceedings until the Disciplinary Authority decides the bias petition.', 2) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (3, 1, 'Under Rule 3 of CCS (Conduct) Rules, which duty is expressly mandated for every civil servant?', '["To maintain absolute integrity, devotion to duty, and do nothing unbecoming of a Government servant", "To prioritize personal commercial interests over official tasks", "To disclose classified statistical releases prematurely", "To accept costly gifts from contracting vendors"]', 0, 'Rule 3(1) is the core ethical obligation binding all central government employees.', 3) ON CONFLICT DO NOTHING;
INSERT INTO questions (id, assessment_id, text, options_json, correct_option_index, explanation, "order") VALUES (4, 1, 'When can a disciplinary authority dispense with a departmental inquiry before imposing major penalties?', '["Only under exceptional conditions covered strictly under Article 311(2) second proviso of the Constitution", "Whenever the inquiry would take more than one week", "If the accused officer submits a written denial", "At the arbitrary verbal instruction of an administrative head"]', 0, 'Article 311(2) proviso strictly delineates the rare constitutional exceptions (e.g. state security or impracticability).', 4) ON CONFLICT DO NOTHING;
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
