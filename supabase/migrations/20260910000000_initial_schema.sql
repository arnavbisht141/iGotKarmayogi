-- ========================================================
-- iGOT Karmayogi — Official Supabase PostgreSQL Migration
-- Initial Schema Definition (Phase 0 Platform Specification)
-- ========================================================

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'learner' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. User Profiles Table (5-Step Onboarding & Learner Preferences)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    phone VARCHAR(50),
    bio TEXT,
    education VARCHAR(255),
    work_experience_years INTEGER DEFAULT 0,
    prior_training TEXT,
    designation VARCHAR(255),
    department VARCHAR(255),
    job_role VARCHAR(255),
    current_assignment TEXT,
    areas_of_interest TEXT,
    language_pref VARCHAR(20) DEFAULT 'en',
    appearance_pref VARCHAR(20) DEFAULT 'light',
    profile_pic_url VARCHAR(500),
    onboarding_completed BOOLEAN DEFAULT FALSE NOT NULL,
    daily_goal_minutes INTEGER DEFAULT 30,
    current_streak_days INTEGER DEFAULT 1,
    last_active_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

-- 3. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- 4. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    overview TEXT NOT NULL,
    instructor VARCHAR(255) NOT NULL,
    organization VARCHAR(255) NOT NULL,
    duration_hours DOUBLE PRECISION DEFAULT 4.0,
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    source VARCHAR(50) DEFAULT 'internal',
    category VARCHAR(100) DEFAULT 'General',
    thumbnail_url VARCHAR(500),
    rating DOUBLE PRECISION DEFAULT 4.8,
    enrolled_count INTEGER DEFAULT 0,
    is_popular BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_courses_title ON courses(title);
CREATE INDEX IF NOT EXISTS idx_courses_category ON courses(category);
CREATE INDEX IF NOT EXISTS idx_courses_difficulty ON courses(difficulty);

-- 5. Modules Table
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    "order" INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_modules_course_id ON modules(course_id);

-- 6. Lessons Table
CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) DEFAULT 'reading',
    duration_minutes INTEGER DEFAULT 15,
    content TEXT NOT NULL,
    video_url VARCHAR(500),
    activity_question TEXT,
    activity_options_json TEXT,
    activity_correct_option INTEGER,
    activity_explanation TEXT,
    "order" INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_lessons_module_id ON lessons(module_id);

-- 7. Skills Table
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100) DEFAULT 'Technical'
);

-- 8. Course-Skill Association Table
CREATE TABLE IF NOT EXISTS course_skills (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_course_skills_course_id ON course_skills(course_id);
CREATE INDEX IF NOT EXISTS idx_course_skills_skill_id ON course_skills(skill_id);

-- 9. User-Skill Acquisition Table
CREATE TABLE IF NOT EXISTS user_skills (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    source_course_id INTEGER REFERENCES courses(id) ON DELETE SET NULL,
    acquired_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_user_skills_user_id ON user_skills(user_id);
CREATE INDEX IF NOT EXISTS idx_user_skills_skill_id ON user_skills(skill_id);

-- 10. Enrollments Table
CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'in_progress',
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMPTZ,
    progress_percent DOUBLE PRECISION DEFAULT 0.0,
    last_lesson_id INTEGER,
    CONSTRAINT uq_user_course_enrollment UNIQUE (user_id, course_id)
);
CREATE INDEX IF NOT EXISTS idx_enrollments_user_id ON enrollments(user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course_id ON enrollments(course_id);

-- 11. Progress Records Table
CREATE TABLE IF NOT EXISTS progress_records (
    id SERIAL PRIMARY KEY,
    enrollment_id INTEGER NOT NULL REFERENCES enrollments(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL,
    lesson_id INTEGER NOT NULL,
    completed BOOLEAN DEFAULT TRUE NOT NULL,
    activity_completed BOOLEAN DEFAULT FALSE NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_enrollment_lesson_progress UNIQUE (enrollment_id, lesson_id)
);
CREATE INDEX IF NOT EXISTS idx_progress_records_enrollment_id ON progress_records(enrollment_id);

-- 12. Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER UNIQUE NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    time_limit_minutes INTEGER DEFAULT 30,
    pass_threshold_percent DOUBLE PRECISION DEFAULT 70.0
);
CREATE INDEX IF NOT EXISTS idx_assessments_course_id ON assessments(course_id);

-- 13. Questions Table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_option_index INTEGER NOT NULL,
    explanation TEXT,
    "order" INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_questions_assessment_id ON questions(assessment_id);

-- 14. Assessment Attempts Table
CREATE TABLE IF NOT EXISTS assessment_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assessment_id INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    score_percent DOUBLE PRECISION NOT NULL,
    passed BOOLEAN NOT NULL,
    answers_json TEXT NOT NULL,
    submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_assessment_attempts_user_id ON assessment_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_assessment_attempts_assessment_id ON assessment_attempts(assessment_id);

-- 15. Planned Courses Table
CREATE TABLE IF NOT EXISTS planned_courses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    planned_for VARCHAR(100),
    source VARCHAR(50) DEFAULT 'self',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_user_planned_course UNIQUE (user_id, course_id)
);
CREATE INDEX IF NOT EXISTS idx_planned_courses_user_id ON planned_courses(user_id);

-- 16. Learning History Table
CREATE TABLE IF NOT EXISTS learning_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    viewed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_learning_history_user_id ON learning_history(user_id);

-- 17. Search History Table
CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query VARCHAR(255) NOT NULL,
    searched_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_search_history_user_id ON search_history(user_id);
