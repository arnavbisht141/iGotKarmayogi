-- Migration: 20260914000001_technical_course_pipeline.sql
-- Description: Technical Course Content Generation Pipeline & Hands-on Interactive Labs

-- 1. Technical Course Video/Audio Transcripts
CREATE TABLE IF NOT EXISTS public.technical_transcripts (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES public.courses(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    raw_text TEXT NOT NULL,
    cleaned_text TEXT NOT NULL,
    chunks_json TEXT NOT NULL,
    metadata_json TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_technical_transcripts_course_id ON public.technical_transcripts(course_id);

-- 2. Extracted Technical Learning Objectives
CREATE TABLE IF NOT EXISTS public.technical_learning_objectives (
    id SERIAL PRIMARY KEY,
    transcript_id INTEGER REFERENCES public.technical_transcripts(id) ON DELETE CASCADE,
    objective TEXT NOT NULL,
    skill VARCHAR(255) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    action_verb VARCHAR(100) NOT NULL,
    assessment_mode VARCHAR(50) DEFAULT 'lab',
    suitability_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tech_objectives_skill ON public.technical_learning_objectives(skill);
CREATE INDEX IF NOT EXISTS idx_tech_objectives_transcript_id ON public.technical_learning_objectives(transcript_id);

-- 3. Human-Curated Technical Lab Templates
CREATE TABLE IF NOT EXISTS public.technical_lab_templates (
    id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    skill VARCHAR(255) NOT NULL,
    language VARCHAR(50) DEFAULT 'python',
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    lab_type VARCHAR(100) DEFAULT 'implementation',
    tags_json TEXT DEFAULT '[]',
    instructions_template TEXT NOT NULL,
    starter_code_template TEXT NOT NULL,
    solution_template TEXT,
    constraints_json TEXT DEFAULT '[]',
    test_cases_template_json TEXT DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tech_templates_skill ON public.technical_lab_templates(skill);
CREATE INDEX IF NOT EXISTS idx_tech_templates_language ON public.technical_lab_templates(language);

-- 4. Generated Interactive Hands-on Labs
CREATE TABLE IF NOT EXISTS public.technical_generated_labs (
    id SERIAL PRIMARY KEY,
    template_id VARCHAR(100) REFERENCES public.technical_lab_templates(id) ON DELETE SET NULL,
    objective_id INTEGER REFERENCES public.technical_learning_objectives(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    objective TEXT NOT NULL,
    language VARCHAR(50) DEFAULT 'python',
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    instructions TEXT NOT NULL,
    starter_code TEXT NOT NULL,
    constraints_json TEXT DEFAULT '[]',
    test_cases_json TEXT DEFAULT '[]',
    expected_behavior TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tech_labs_template_id ON public.technical_generated_labs(template_id);
CREATE INDEX IF NOT EXISTS idx_tech_labs_objective_id ON public.technical_generated_labs(objective_id);

-- 5. Reference Solutions for Generated Labs
CREATE TABLE IF NOT EXISTS public.technical_lab_solutions (
    id SERIAL PRIMARY KEY,
    lab_id INTEGER UNIQUE NOT NULL REFERENCES public.technical_generated_labs(id) ON DELETE CASCADE,
    reference_code TEXT NOT NULL,
    explanation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Sandbox Execution & Validation Results
CREATE TABLE IF NOT EXISTS public.technical_lab_validation_results (
    id SERIAL PRIMARY KEY,
    lab_id INTEGER NOT NULL REFERENCES public.technical_generated_labs(id) ON DELETE CASCADE,
    solution_id INTEGER REFERENCES public.technical_lab_solutions(id) ON DELETE SET NULL,
    is_valid BOOLEAN NOT NULL DEFAULT FALSE,
    sandbox_type VARCHAR(50) DEFAULT 'docker',
    exit_code INTEGER DEFAULT 0,
    execution_time_ms DOUBLE PRECISION DEFAULT 0.0,
    stdout TEXT,
    stderr TEXT,
    test_summary_json TEXT,
    error_message TEXT,
    validated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tech_validation_lab_id ON public.technical_lab_validation_results(lab_id);
