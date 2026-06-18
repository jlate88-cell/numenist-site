-- =============================================================
-- reading_followups — 5 follow-up questions per reading
-- =============================================================
-- Schema migration for the Numen reading-engine. Adds the ability
-- for a client to ask up to 5 clarifying questions after receiving
-- their reading; each question is answered by Claude using the
-- reading paragraphs as context, preserving voice and accuracy.
--
-- A reading row may live in EITHER readings_cache (17-section
-- flagship) OR astrology_readings_cache (15-section combined
-- astrology). The schema below supports both via two nullable FKs;
-- a CHECK enforces exactly one is set per follow-up row.
--
-- Apply via Supabase migration:
--    supabase db push    OR
--    mcp.apply_migration(project=..., sql=<this file>)
-- =============================================================

CREATE TABLE IF NOT EXISTS public.reading_followups (
  id                  uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at          timestamptz NOT NULL DEFAULT now(),

  -- Polymorphic link: exactly one of these must be set.
  reading_cache_id    uuid        REFERENCES public.readings_cache(id)            ON DELETE CASCADE,
  astrology_cache_id  uuid        REFERENCES public.astrology_readings_cache(id)  ON DELETE CASCADE,

  seeker_name         text        NOT NULL,
  question_index      smallint    NOT NULL CHECK (question_index BETWEEN 1 AND 5),
  question            text        NOT NULL,
  answer              text,

  asked_at            timestamptz NOT NULL DEFAULT now(),
  answered_at         timestamptz,

  -- Provenance of the answer composition
  composed_by         text        DEFAULT 'claude' CHECK (composed_by IN ('claude','deterministic')),
  claude_model        text,
  token_input_count   integer,
  token_output_count  integer,

  -- Exactly one of the two FKs must be set
  CONSTRAINT reading_followups_one_parent CHECK (
    (reading_cache_id   IS NOT NULL AND astrology_cache_id IS NULL) OR
    (reading_cache_id   IS NULL     AND astrology_cache_id IS NOT NULL)
  ),

  -- A reading can only have one question per slot 1..5
  CONSTRAINT reading_followups_unique_flagship UNIQUE NULLS NOT DISTINCT (reading_cache_id,   question_index),
  CONSTRAINT reading_followups_unique_astro    UNIQUE NULLS NOT DISTINCT (astrology_cache_id, question_index)
);

CREATE INDEX IF NOT EXISTS idx_reading_followups_seeker     ON public.reading_followups (seeker_name);
CREATE INDEX IF NOT EXISTS idx_reading_followups_reading    ON public.reading_followups (reading_cache_id);
CREATE INDEX IF NOT EXISTS idx_reading_followups_astrology  ON public.reading_followups (astrology_cache_id);
CREATE INDEX IF NOT EXISTS idx_reading_followups_unanswered
    ON public.reading_followups (asked_at)
    WHERE answer IS NULL;

-- =============================================================
-- Row-level security: each client only sees their own follow-ups
-- =============================================================
ALTER TABLE public.reading_followups ENABLE ROW LEVEL SECURITY;

-- Adapt policies to match your auth schema (profiles, memberships, etc.).
-- The simplest pattern, assuming a seeker_email column or join via profiles:
-- (left as a TODO with a clearly-marked placeholder).
--
-- DROP POLICY IF EXISTS followups_owner_select ON public.reading_followups;
-- CREATE POLICY followups_owner_select ON public.reading_followups
--   FOR SELECT USING (
--     auth.uid() IS NOT NULL AND seeker_name = (
--       SELECT full_name FROM public.profiles WHERE user_id = auth.uid()
--     )
--   );

-- =============================================================
-- Optional: pre-seat 5 empty slots per reading so the UI can
-- show "0 / 5 questions asked" on day one without needing
-- application-side counting.
-- (Skip if your UI counts from rows present.)
-- =============================================================

COMMENT ON TABLE  public.reading_followups IS '5 follow-up questions per reading; Claude-composed answers grounded in the reading paragraphs.';
COMMENT ON COLUMN public.reading_followups.question_index IS '1..5; enforced by CHECK and UNIQUE-per-reading constraints.';
COMMENT ON COLUMN public.reading_followups.composed_by    IS 'claude (default) or deterministic (template-answered).';
