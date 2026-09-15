-- Migration: 20260915000001_phase2_evidence_mapping.sql
-- Description: Bridges free-text skill/competency identifiers from the statistical
-- engine and behavioural sessions to the competency taxonomy (Phase 2).

CREATE TABLE IF NOT EXISTS public.evidence_competency_mapping (
    id SERIAL PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    source_key VARCHAR(255) NOT NULL,
    competency_id INTEGER NOT NULL REFERENCES public.competencies(id) ON DELETE CASCADE,
    CONSTRAINT uq_evidence_mapping_source UNIQUE (source_system, source_key)
);

CREATE INDEX IF NOT EXISTS idx_evidence_mapping_competency_id ON public.evidence_competency_mapping(competency_id);
