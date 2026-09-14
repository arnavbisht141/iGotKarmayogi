-- Migration: 20260914000003_competency_intelligence_layer.sql
-- Description: Competency Intelligence Layer - taxonomy, profiling, gap analysis, recommendations, and statistical engine

-- 1. Competency Domain Taxonomy
CREATE TABLE IF NOT EXISTS public.competency_domains (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_competency_domains_code ON public.competency_domains(code);

-- 2. Individual Competencies within Domains
CREATE TABLE IF NOT EXISTS public.competencies (
    id SERIAL PRIMARY KEY,
    domain_id INTEGER NOT NULL REFERENCES public.competency_domains(id) ON DELETE CASCADE,
    code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    max_level INTEGER DEFAULT 5
);

CREATE INDEX IF NOT EXISTS idx_competencies_domain_id ON public.competencies(domain_id);
CREATE INDEX IF NOT EXISTS idx_competencies_code ON public.competencies(code);

-- 3. User Competency Profile (summary scores across domains)
CREATE TABLE IF NOT EXISTS public.competency_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    statistical_score DOUBLE PRECISION DEFAULT 0.0,
    technical_score DOUBLE PRECISION DEFAULT 0.0,
    digital_governance_score DOUBLE PRECISION DEFAULT 0.0,
    behavioural_score DOUBLE PRECISION DEFAULT 0.0,
    last_computed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_competency_profiles_user_id ON public.competency_profiles(user_id);

-- 4. User Competency Scores (per-competency mastery levels)
CREATE TABLE IF NOT EXISTS public.user_competency_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    competency_id INTEGER NOT NULL REFERENCES public.competencies(id) ON DELETE CASCADE,
    level DOUBLE PRECISION DEFAULT 0.0,
    evidence_source VARCHAR(50) DEFAULT 'self_declared',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_competency_scores_user_id ON public.user_competency_scores(user_id);
CREATE INDEX IF NOT EXISTS idx_user_competency_scores_competency_id ON public.user_competency_scores(competency_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_user_competency ON public.user_competency_scores(user_id, competency_id);

-- 5. Gap Analysis (identifies competency gaps for users)
CREATE TABLE IF NOT EXISTS public.gap_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    domain_id INTEGER NOT NULL REFERENCES public.competency_domains(id) ON DELETE CASCADE,
    target_level DOUBLE PRECISION NOT NULL,
    current_level DOUBLE PRECISION NOT NULL,
    gap DOUBLE PRECISION NOT NULL,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gap_analyses_user_id ON public.gap_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_gap_analyses_domain_id ON public.gap_analyses(domain_id);

-- 6. Personalized Course Recommendations
CREATE TABLE IF NOT EXISTS public.recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES public.courses(id) ON DELETE SET NULL,
    reason TEXT NOT NULL,
    score DOUBLE PRECISION DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'pending',
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON public.recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_course_id ON public.recommendations(course_id);

-- 7. Statistical Engine Questions (parametric question templates)
CREATE TABLE IF NOT EXISTS public.stat_engine_questions (
    question_id VARCHAR(100) PRIMARY KEY,
    template_id VARCHAR(100) NOT NULL,
    skill_id VARCHAR(100) NOT NULL,
    competency_id VARCHAR(100) NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    correct_answer_json TEXT NOT NULL,
    tolerance DOUBLE PRECISION DEFAULT 0.0,
    options_map_json TEXT NOT NULL,
    correct_option_id VARCHAR(50),
    explanation TEXT,
    unit VARCHAR(100),
    chart_json TEXT,
    seed INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stat_engine_questions_skill_id ON public.stat_engine_questions(skill_id);

-- 8. Statistical Engine Attempt Tracking
CREATE TABLE IF NOT EXISTS public.stat_engine_attempts (
    id SERIAL PRIMARY KEY,
    attempt_id VARCHAR(100) NOT NULL UNIQUE,
    user_id VARCHAR(100) NOT NULL,
    question_id VARCHAR(100) NOT NULL,
    skill_id VARCHAR(100) NOT NULL,
    submitted_answer VARCHAR(255),
    is_correct BOOLEAN DEFAULT FALSE,
    score DOUBLE PRECISION DEFAULT 0.0,
    misconception_id VARCHAR(100),
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stat_engine_attempts_user_id ON public.stat_engine_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_stat_engine_attempts_skill_id ON public.stat_engine_attempts(skill_id);

-- 9. Statistical Engine Mastery Tracking
CREATE TABLE IF NOT EXISTS public.stat_engine_mastery (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    skill_id VARCHAR(100) NOT NULL,
    mastery_json TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stat_engine_mastery_user_id ON public.stat_engine_mastery(user_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_stat_mastery_user_skill ON public.stat_engine_mastery(user_id, skill_id);

-- 10. Behavioural Session Results (carry-forward and interview simulations)
CREATE TABLE IF NOT EXISTS public.behavioural_session_results (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL UNIQUE,
    session_type VARCHAR(20) NOT NULL,
    user_id INTEGER REFERENCES public.users(id) ON DELETE SET NULL,
    case_or_course_id VARCHAR(100),
    score DOUBLE PRECISION DEFAULT 0.0,
    result_json TEXT NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_behavioural_session_results_session_id ON public.behavioural_session_results(session_id);
CREATE INDEX IF NOT EXISTS idx_behavioural_session_results_user_id ON public.behavioural_session_results(user_id);
