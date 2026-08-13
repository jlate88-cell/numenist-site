# Engine Additions — The Twelve Doors + 5 Follow-Up Questions

Two add-ons for the Numen reading engine. Both apply to BOTH products:
the 15-section combined-astrology reading and the 17-section flagship
"Reading."

## Add-on 1 — The Twelve Doors (Houses & Their Lords)

A new section that walks all 12 houses through the classical Hellenistic
"lord of the cusp" technique. Closes the gap a planet-centric reading
leaves open: empty houses get their own pass, traced through where their
ruler actually lives.

**Files:**
- `houses_and_lords.py` — deterministic composer. No LLM call. Takes a
  chart dict, returns one section object matching the engine schema:
  `{ id, heading, paragraphs[], blocks[] }`. Section id is
  `houses-and-lords`; heading is `The Twelve Doors — Houses & Their Lords`.

**Where it goes in the section sequence:**

| Product | Section id sequence (after) | Section id sequence (before) |
|---------|----------------------------|------------------------------|
| 15-section combined-astrology | `configurations` | `timing` |
| 17-section flagship "Reading" | `astrology` | `master-count` |

**Wire-up — Python:**

```python
from houses_and_lords import compose_houses_and_lords

# After the engine has composed all the other sections:
new_section = compose_houses_and_lords(chart_dict)

# 15-section astrology product:
idx = next(i for i, s in enumerate(sections) if s["id"] == "configurations")
sections.insert(idx + 1, new_section)

# 17-section flagship "Reading":
idx = next(i for i, s in enumerate(sections) if s["id"] == "astrology")
sections.insert(idx + 1, new_section)
```

The chart dict must include `asc` and the seven traditional planets
(sun, moon, mercury, venus, mars, jupiter, saturn). Outer planets are
not used as house rulers in this technique; if you pass them, they're
ignored. Each planet is shape:

```python
{"sign": "Pisces", "deg": 24.87, "house": 7, "retrograde": False}
```

**Smoke-tested** against Jordan Ross Atkins's chart (verified data from
`astrology_readings_cache`): emits 14 paragraphs (intro + 12 houses +
closing), all classical-rulership correct (1st&10th→Mercury, 2nd&9th
→Venus, 3rd&8th→Mars, 4th&7th→Jupiter, 5th&6th→Saturn, 11th→Moon,
12th→Sun). 2nd-house read for Jordan: cusp Libra, lord Venus in detriment
in 8th, money runs through depth/shared resource — matches the read I
walked him through manually.

## Add-on 2 — Five Follow-Up Questions

After a client receives their reading, they can ask up to 5 clarifying
questions. Each is answered by Claude using the reading's full text as
context, in the same voice, grounded in the placements already
established. The 5-question ceiling is hard-enforced at the database
level so cost is predictable and the follow-up surface can't cannibalize
the reading.

**Files:**
- `follow_up_questions.sql` — Supabase migration. Adds
  `public.reading_followups` table with polymorphic FK to either
  `readings_cache` or `astrology_readings_cache`, CHECK that
  `question_index` is in 1..5, UNIQUE constraint preventing duplicate
  slots, RLS scaffold, indexes.
- `follow_up_prompt.md` — the Claude prompt template (system + user)
  plus the API contract and UI sketch.

**Apply the migration:**

```sql
-- Via Supabase MCP:
mcp__supabase__apply_migration({
  project_id: 'tuayjblcwswcmtuhoucv',
  name: 'reading_followups_v1',
  query: <contents of follow_up_questions.sql>
})

-- Or via Supabase CLI:
supabase db push
```

**Wire-up — Next.js route handler (sketch):**

```ts
// app/api/readings/[id]/followups/route.ts
import { Anthropic } from '@anthropic-ai/sdk';
import { renderFollowUpPrompt } from '@/lib/numen/followup-prompt';

export async function POST(req, { params }) {
  const { question_index, question } = await req.json();
  const reading_id = params.id;

  // 1. auth check: this client owns this reading
  // 2. validate question_index 1..5, not already used
  // 3. load reading paragraphs + structured chart
  const { reading, chart } = await loadReading(reading_id);

  // 4. render prompts
  const { system, user } = renderFollowUpPrompt({
    reading, chart, question, question_index
  });

  // 5. call Claude
  const anthropic = new Anthropic();
  const msg = await anthropic.messages.create({
    model: 'claude-opus-4-7',
    max_tokens: 1500,
    system,
    messages: [{ role: 'user', content: user }]
  });

  const answer = msg.content.map(b => b.text).join('');

  // 6. persist
  await supabase.from('reading_followups').insert({
    [cacheTableForReading(reading_id)]: reading_id,
    seeker_name: chart.seeker_name,
    question_index,
    question,
    answer,
    composed_by: 'claude',
    claude_model: 'claude-opus-4-7',
    answered_at: new Date().toISOString(),
    token_input_count: msg.usage.input_tokens,
    token_output_count: msg.usage.output_tokens,
  });

  return Response.json({ answer });
}
```

**Wire-up — UI on the reading page:**

```tsx
// After the closing section in app/reading/[id]/page.tsx
<section className="reading-section followup-section">
  <h2>Five Follow-Up Questions</h2>
  <p className="kicker">
    Ask up to 5 questions to deepen this reading. Each is answered in
    the reading's own voice, grounded in the chart you were given.
  </p>
  <FollowUpQuestions readingId={reading.id} />
</section>
```

The `<FollowUpQuestions>` component manages the 0–5 state, POSTs to the
route handler above, and renders the answer in the same prose style as
the rest of the reading.

## Deploy order

1. Apply `follow_up_questions.sql` migration.
2. Drop `houses_and_lords.py` into the engine's composer module
   alongside the existing per-section composers.
3. Edit the section-composition pipeline so it appends
   `compose_houses_and_lords(chart)` after `configurations` (astrology
   product) and after `astrology` (flagship "Reading").
4. Add the Next.js route handler from the wire-up sketch above.
5. Add the `<FollowUpQuestions>` UI component.
6. Re-run the engine's composer for one test reading; verify the
   `houses-and-lords` section appears in the rendered output and the
   follow-up form posts cleanly.

## What this preserves

- Engine voice across both the new section and the follow-ups.
- No fabricated placements: deterministic composer for the houses
  section, reading-grounded Claude prompt for the follow-ups.
- Hard cost ceiling on follow-ups (5 max per reading, enforced in DB).
- Both products get the same upgrade.

## What still needs the engine repo

The engine code that composes sections, calls Claude, and inserts rows
into the cache tables is not in this `numenist-site` repo — it lives in
the separate Next.js Vercel app. To deploy these add-ons, the files
above need to land in that repo. The deterministic composer and the
SQL migration are self-contained; they can be dropped in without
modification. The route handler and UI component need to be adapted to
the engine repo's existing auth and Supabase client patterns.
