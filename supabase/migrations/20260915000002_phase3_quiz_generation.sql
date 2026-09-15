-- Migration: 20260915000002_phase3_quiz_generation.sql
-- Description: AI-generated quizzes/MCQs from uploaded learning materials, with learner attempts.

CREATE TABLE IF NOT EXISTS public.generated_quizzes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(20) NOT NULL,
    source_excerpt TEXT,
    difficulty VARCHAR(20) DEFAULT 'intermediate',
    generator VARCHAR(20) DEFAULT 'llm',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_generated_quizzes_user_id ON public.generated_quizzes(user_id);

CREATE TABLE IF NOT EXISTS public.generated_quiz_questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES public.generated_quizzes(id) ON DELETE CASCADE,
    "order" INTEGER DEFAULT 1,
    question_text TEXT NOT NULL,
    options_json TEXT NOT NULL,
    correct_option_index INTEGER NOT NULL,
    explanation TEXT,
    concept VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_generated_quiz_questions_quiz_id ON public.generated_quiz_questions(quiz_id);

CREATE TABLE IF NOT EXISTS public.quiz_attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES public.generated_quizzes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    answers_json TEXT NOT NULL,
    correct_count INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    score_percent DOUBLE PRECISION DEFAULT 0,
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz_id ON public.quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user_id ON public.quiz_attempts(user_id);
