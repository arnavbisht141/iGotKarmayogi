-- Migration: 20260914000002_digital_governance_cybersecurity.sql
-- Description: Digital Governance, Cyber Defense CTF Sandbox & Civil Service Incident Simulations

-- 1. Human-Authored Cyber Sandbox Templates
CREATE TABLE IF NOT EXISTS public.cyber_sandbox_templates (
    id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    competency_id VARCHAR(100) DEFAULT 'soc_investigation',
    points INTEGER DEFAULT 100,
    duration_minutes INTEGER DEFAULT 45,
    tags_json TEXT DEFAULT '[]',
    mitre_techniques_json TEXT DEFAULT '[]',
    scenario_template TEXT NOT NULL,
    instructions_template TEXT NOT NULL,
    hints_template_json TEXT DEFAULT '[]',
    artifacts_spec_json TEXT DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cyber_templates_category ON public.cyber_sandbox_templates(category);
CREATE INDEX IF NOT EXISTS idx_cyber_templates_competency ON public.cyber_sandbox_templates(competency_id);

-- 2. Procedural & Flagship CTF Cyber Defense Challenges
CREATE TABLE IF NOT EXISTS public.cyber_sandbox_challenges (
    id VARCHAR(100) PRIMARY KEY,
    template_id VARCHAR(100) REFERENCES public.cyber_sandbox_templates(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) DEFAULT 'intermediate',
    points INTEGER DEFAULT 100,
    duration_minutes INTEGER DEFAULT 45,
    competency_id VARCHAR(100) DEFAULT 'soc_investigation',
    is_flagship BOOLEAN DEFAULT FALSE,
    tags_json TEXT DEFAULT '[]',
    mitre_techniques_json TEXT DEFAULT '[]',
    objectives_json TEXT DEFAULT '[]',
    scenario_markdown TEXT NOT NULL,
    flag VARCHAR(255) NOT NULL,
    hints_json TEXT DEFAULT '[]',
    artifacts_json TEXT DEFAULT '{}',
    notebook_code TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cyber_challenges_template ON public.cyber_sandbox_challenges(template_id);
CREATE INDEX IF NOT EXISTS idx_cyber_challenges_category ON public.cyber_sandbox_challenges(category);
CREATE INDEX IF NOT EXISTS idx_cyber_challenges_competency ON public.cyber_sandbox_challenges(competency_id);
CREATE INDEX IF NOT EXISTS idx_cyber_challenges_flagship ON public.cyber_sandbox_challenges(is_flagship);

-- 3. Ephemeral Sandbox Container Sessions
CREATE TABLE IF NOT EXISTS public.cyber_sandbox_sessions (
    id VARCHAR(100) PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id) ON DELETE CASCADE,
    challenge_id VARCHAR(100) NOT NULL REFERENCES public.cyber_sandbox_challenges(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'running',
    assigned_port INTEGER NOT NULL,
    flag VARCHAR(255) NOT NULL,
    unlocked_hints_json TEXT DEFAULT '[]',
    total_penalties INTEGER DEFAULT 0,
    final_score INTEGER DEFAULT 0,
    is_solved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    solved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_cyber_sessions_user_id ON public.cyber_sandbox_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_cyber_sessions_challenge_id ON public.cyber_sandbox_sessions(challenge_id);
CREATE INDEX IF NOT EXISTS idx_cyber_sessions_status ON public.cyber_sandbox_sessions(status);

-- 4. User Cybersecurity & Digital Governance Competencies
CREATE TABLE IF NOT EXISTS public.user_cyber_competencies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    soc_investigation INTEGER DEFAULT 0,
    phishing_analysis INTEGER DEFAULT 0,
    cloud_security INTEGER DEFAULT 0,
    dpi_security INTEGER DEFAULT 0,
    digital_forensics INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    solved_challenges_count INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_cyber_comp_user ON public.user_cyber_competencies(user_id);
CREATE INDEX IF NOT EXISTS idx_user_cyber_comp_score ON public.user_cyber_competencies(total_score DESC);

-- Enable Row Level Security (RLS) policies
ALTER TABLE public.cyber_sandbox_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cyber_sandbox_challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cyber_sandbox_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_cyber_competencies ENABLE ROW LEVEL SECURITY;

-- Read policies for all authenticated civil servants
CREATE POLICY "Allow public read access to cyber templates" ON public.cyber_sandbox_templates FOR SELECT USING (true);
CREATE POLICY "Allow public read access to cyber challenges" ON public.cyber_sandbox_challenges FOR SELECT USING (true);

-- Session policies: users view and operate only their own active sessions
CREATE POLICY "Allow users to view own cyber sessions" ON public.cyber_sandbox_sessions FOR SELECT USING (auth.uid()::text = user_id::text OR user_id IS NULL);
CREATE POLICY "Allow users to insert own cyber sessions" ON public.cyber_sandbox_sessions FOR INSERT WITH CHECK (auth.uid()::text = user_id::text OR user_id IS NULL);
CREATE POLICY "Allow users to update own cyber sessions" ON public.cyber_sandbox_sessions FOR UPDATE USING (auth.uid()::text = user_id::text);

-- Competency policies: users view all leaderboards and own competencies
CREATE POLICY "Allow public read access to cyber competencies" ON public.user_cyber_competencies FOR SELECT USING (true);
CREATE POLICY "Allow users to manage own cyber competencies" ON public.user_cyber_competencies FOR ALL USING (auth.uid()::text = user_id::text);
