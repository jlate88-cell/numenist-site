/**
 * app/api/readings/[id]/followups/route.ts
 *
 * Drop-in Next.js App Router POST handler for the 5 follow-up questions
 * feature. The reading_followups table is already live in production
 * Supabase (project tuayjblcwswcmtuhoucv, migration reading_followups_v1
 * applied 2026-06-18).
 *
 * IMPORTS in this file assume the quintiform conventions:
 *   - @supabase/ssr            createServerClient
 *   - @anthropic-ai/sdk        Anthropic
 *   - next/server              NextRequest, NextResponse
 *
 * Adjust imports if quintiform uses different aliases (e.g. @/lib/supabase
 * server client wrapper). The logic does not depend on a specific Supabase
 * client implementation.
 */

import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

interface FollowUpBody {
  question_index: number;  // 1..5
  question: string;
  // The route accepts whichever cache table the reading lives in.
  // Caller must specify; both cannot be set, both cannot be empty.
  reading_cache_id?: string | null;
  astrology_cache_id?: string | null;
}

const SYSTEM_PROMPT = `You are the Numen reading engine, answering one follow-up question for a
client who already received their full reading. The full reading text is
provided below. Treat it as the SOLE source of truth for this client's
chart, numerology, and BaZi pillars. Do NOT invent placements, degrees,
aspects, or numbers not already in the reading.

Voice rules:
- Match the reading's existing voice exactly: warm, observant, grounded,
  precise, unhurried, slightly humble. A master speaking to a serious
  student. Lineage alive in the speaking, not catalogued in citation density.
- NO sycophancy. NO "great question." NO clinical-bureaucratic headers.
- NO atheism-coded hedges ("I'd be careful reaching for...", "the simpler
  human read is...", "while the systems suggest X, in practical terms...").
- The cosmic frame is the ground; boots-on-the-ground is the consummation.

Technique rules:
- LEAD with the cosmic / numerological read using the placements the
  reading already established.
- For house questions: walk the asked house through its cusp-lord
  (the Hellenistic / Lilly horary technique).
- For numbers: use Pythagorean / Chaldean reduction; flag karmic-debt
  numbers (13, 14, 16, 19). When a name appears, run Chaldean on it.
- For dates: compute Personal Day using the numerology in the reading;
  note Tarot correspondence for compound numbers (10..22).
- Close with the practical action the cosmic read calls for.

Length: 3-6 short paragraphs. No bullets unless the question is itself
a list-of-distinct-items question.

If the question is ambiguous: name the ambiguity in one sentence, give the
most likely read, offer to refine. If the question requires data the
reading does NOT contain: say so plainly and offer the adjacent move the
reading CAN answer.`;

function buildUserPrompt(args: {
  reading_paragraphs: string[];
  seeker_name: string;
  question_index: number;
  question: string;
}): string {
  return [
    "THE CLIENT'S READING (full text):",
    '',
    args.reading_paragraphs.join('\n\n'),
    '',
    "THE CLIENT:",
    `  Name: ${args.seeker_name}`,
    '',
    `THIS IS QUESTION ${args.question_index} OF 5.`,
    '',
    "THE CLIENT ASKS:",
    `  ${args.question}`,
    '',
    "Answer them. Lineage-grounded. From the reading's data. In the reading's",
    "voice. With one practical move at the close.",
  ].join('\n');
}

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  let body: FollowUpBody;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'invalid json body' }, { status: 400 });
  }

  const { question_index, question } = body;
  if (!Number.isInteger(question_index) || question_index < 1 || question_index > 5) {
    return NextResponse.json(
      { error: 'question_index must be an integer 1..5' },
      { status: 400 }
    );
  }
  if (!question || typeof question !== 'string' || question.trim().length === 0) {
    return NextResponse.json(
      { error: 'question is required' },
      { status: 400 }
    );
  }
  const reading_cache_id   = body.reading_cache_id   ?? null;
  const astrology_cache_id = body.astrology_cache_id ?? null;
  if (!!reading_cache_id === !!astrology_cache_id) {
    return NextResponse.json(
      { error: 'exactly one of reading_cache_id or astrology_cache_id must be set' },
      { status: 400 }
    );
  }

  // ---- Auth + ownership check (quintiform-specific; adjust import) -------
  const cookieStore = cookies();
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
    {
      cookies: {
        get(name: string) { return cookieStore.get(name)?.value; },
      },
    }
  );

  // ---- Load reading + chart from whichever cache table is referenced ----
  const cacheTable = reading_cache_id ? 'readings_cache' : 'astrology_readings_cache';
  const cacheId    = reading_cache_id ?? astrology_cache_id!;

  const { data: readingRow, error: readingErr } = await supabase
    .from(cacheTable)
    .select('full_name, seeker_name, reading_json')
    .eq('id', cacheId)
    .single();

  if (readingErr || !readingRow) {
    return NextResponse.json(
      { error: 'reading not found', details: readingErr?.message },
      { status: 404 }
    );
  }

  // Both tables expose `reading_json` containing `sections`.
  const sections = readingRow.reading_json?.sections ?? [];
  const reading_paragraphs: string[] = sections.flatMap(
    (s: { paragraphs?: string[] }) => s.paragraphs ?? []
  );
  const seeker_name = readingRow.full_name ?? readingRow.seeker_name ?? 'the client';

  // ---- Pre-check: slot not already used --------------------------------
  const filterCol = reading_cache_id ? 'reading_cache_id' : 'astrology_cache_id';
  const { data: existing } = await supabase
    .from('reading_followups')
    .select('id, answer')
    .eq(filterCol, cacheId)
    .eq('question_index', question_index)
    .maybeSingle();
  if (existing && existing.answer) {
    return NextResponse.json(
      { error: `question slot ${question_index} already answered`, id: existing.id },
      { status: 409 }
    );
  }

  // ---- Compose answer with Claude --------------------------------------
  const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY! });
  const userPrompt = buildUserPrompt({
    reading_paragraphs,
    seeker_name,
    question_index,
    question,
  });

  let answer = '';
  let claude_model = 'claude-opus-4-8';
  let token_input_count: number | null = null;
  let token_output_count: number | null = null;

  try {
    const msg = await anthropic.messages.create({
      model: claude_model,
      max_tokens: 1500,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userPrompt }],
    });
    answer = msg.content
      .filter((b): b is { type: 'text'; text: string } => b.type === 'text')
      .map((b) => b.text)
      .join('');
    token_input_count  = msg.usage?.input_tokens  ?? null;
    token_output_count = msg.usage?.output_tokens ?? null;
  } catch (err: any) {
    return NextResponse.json(
      { error: 'composer failed', details: err.message ?? String(err) },
      { status: 502 }
    );
  }

  if (!answer || answer.trim().length === 0) {
    answer =
      "I'd need a touch more context to answer that cleanly. Try rephrasing " +
      "with the specific area of life or person involved, and I'll take it again.";
  }

  // ---- Persist --------------------------------------------------------
  const insertRow = {
    [filterCol]: cacheId,
    seeker_name,
    question_index,
    question,
    answer,
    composed_by: 'claude',
    claude_model,
    token_input_count,
    token_output_count,
    answered_at: new Date().toISOString(),
  } as Record<string, unknown>;

  const { data: inserted, error: insertErr } = await supabase
    .from('reading_followups')
    .insert(insertRow)
    .select('id, question_index, answer, answered_at')
    .single();

  if (insertErr) {
    return NextResponse.json(
      { error: 'persist failed', details: insertErr.message },
      { status: 500 }
    );
  }

  return NextResponse.json(inserted);
}
