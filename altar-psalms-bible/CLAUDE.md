# CLAUDE.md — altar-psalms-bible

This file is the persistent discipline for any Claude session that touches
the Altar Psalms Reader. The directives are non-negotiable. This document
exists because Jordan caught a duplicate-gloss bug on 2026-06-21 that was
caused by acting on memory instead of running the verification tools.

## Operator

Jordan Ross Atkins. The reader is used in active ritual. **Errors here
break the working.** This document is not a website artifact; it is a
spiritual tool. Ritual-grade or do not ship.

## The AI Slop Code

The AI Slop Code is the named refusal to ship "AI slop" — output produced
by acting on memory instead of acting on verified tool output. It is
enforced mechanically by `validate.py`, which the build runs automatically
and which any session MUST run after every edit before shipping.

Six rules. The validator checks every one of them mechanically:

1. **No duplicate (word, pron) entries in any P*_GLOSS table.** The bug
   that motivated this whole document was a duplicate that produced
   `vnto [UN-too] [UN-too]` in five verses of Psalm 91. The validator
   greps every gloss table and asserts the entries are unique.

2. **No tautological glosses.** A gloss whose pronunciation text equals
   the word it glosses (`thy → [thy]`, `hath → [hath]`) teaches the
   reader nothing and adds visual noise. Refused.

3. **No double-rendered `[X] [X]` patterns anywhere in the rendered PDF.**
   The validator runs `pdftotext` on the build and asserts the pattern
   never appears.

4. **The NOW cue baseline must hold.** Part II of the reader contains 28
   inline "NOW —" cues (baseline raised from 13 to 28 on 2026-06-21 after
   the Parts I/IV/V/VI cue extension) that guide the operator through the
   ritual without flipping back to the 10-step overview. The validator
   counts them in source and in the rendered PDF; either count below
   baseline fails the build.

5. **Every psalm referenced in any ritual order must be printed inline,
   not cross-referenced.** The validator checks every psalm's verse-1
   signature against the rendered PDF.

6. **Lineage manifest signatures must appear in the build script.**
   Every documented-lineage claim the Reader makes (orderings, holy
   names, herb lists, candle colors, timing days, anointing sequences)
   lives in `lineage.py` with a `signature` field — a short verbatim
   substring that must appear in `build_psalms_reader.py`. If the
   script no longer contains the verbatim signature, the claim has
   been EDITED without updating the manifest. The build fails until
   the manifest entry is refreshed with a fresh source citation. This
   rule was added 2026-06-21 after Jordan's Master 11 caught the
   candle-position error in v5.0 — the validator's prior rules did not
   guard against ritual sequencing drift.

The `gloss_text()` function itself has been hardened with a `seen` set
that silently deduplicates entries at apply-time, so even if rule 1 is
violated in source, the rendered output stays clean. The validator
still flags it so the source gets cleaned up.

## Mandatory protocol for ANY edit

Before any edit to:
  - any `P*_GLOSS` table
  - any `now(...)` cue placement
  - any psalm verse text
  - any ritual ordering or sequence
  - any `step` paragraph in the altar ritual
  - any holy name, herb list, candle color, timing day, or anointing
    sequence that is covered by a `lineage.py` manifest entry

The session MUST follow this protocol exactly:

1. **Read the relevant section of the source FIRST.** Do not edit
   blindly. Use the `Read` tool or `Grep`. Verify what is there.
2. **Identify EVERY existing entry that touches your change.** If
   you are adding gloss entries, grep the table for the words you are
   about to add. If a word is already glossed, do not add it again.
3. **Check `lineage.py` for any manifest entry whose `signature`
   touches the text you are about to edit.** If your edit would change
   the signature, you MUST update the manifest entry in lockstep — both
   the `signature` field and the `verified_on` date, plus a fresh
   source quote if the substance of the claim changed. Adding a new
   ordering / holy name / herb / timing claim with no prior manifest
   entry requires WRITING a new entry with a real source citation
   (`WebSearch` / `WebFetch` against Yronwode / Selig / AIRR /
   Jesterbear / etc.) before the edit ships.
4. **Make the edit.**
5. **Rebuild:** `python3 build_psalms_reader.py`.
6. **Run the validator:** `python3 validate.py`.
7. **If the validator reports any FAIL, fix the failure and re-run
   from step 5. Do NOT ship a build that fails validation.**
8. **Visually spot-check the rendered PDF** for the page(s) you
   edited. The validator catches the classes of bug we know about;
   visual inspection catches the rest.

## Anti-patterns this document forbids

- **Acting on memory.** "I remember the gloss table has X" is not
  evidence. Grep the table.
- **Skipping the validator after a small edit.** Small edits cause
  small bugs that escalate into wrong text spoken at the altar.
- **Batching multiple edits before re-rendering.** Each edit must be
  built and validated before the next is layered on top.
- **Treating the validator's all-pass message as proof of correctness
  without visual review.** The validator catches the named bug classes.
  It does not catch every possible bug. Visual review still required.
- **Adjusting a baseline to silence a validator warning.** If the
  validator warns, the source might be wrong, or the baseline might be
  wrong. Verify which against the actual text in the source. Only update
  the baseline if the source is verifiably correct.

## The No Padding Code

Installed 2026-06-21 after Jordan named the failure pattern directly:
audit reports and answers padded with taste-calls, manufactured
concerns, and synthesis-claims-without-grep-proof — inflating real
findings with filler so the operator must spend Master 11 discernment
to separate signal from noise. The No Padding Code is the named
refusal of that pattern. Non-negotiable for any audit, review, or
report this session ships.

**Six rules. Apply BEFORE sending any audit, review, or punch-list:**

1. **Every claim must be grepped.** Before reporting an issue, run
   `grep -n` against the source or rendered text and show the line
   number. If you can't grep it, don't claim it. Quoted phrases must
   be verbatim from the grep output.

2. **No taste-calls dressed as findings.** "Feels heavy", "tonal
   register differs", "asymmetric treatment", "could feel redundant" —
   these are opinions, not bugs. If you list them, label them
   `(opinion)` or `(taste)`. Never inside a numbered punch-list of
   "issues."

3. **No manufactured inconsistencies.** Do not invent a concern
   because the list is "too short." A real audit of 4 issues is more
   honest than a padded audit of 15. Length is not rigor.

4. **No synthesis claims without source.** If a finding requires
   comparing across multiple parts ("inconsistency between Part IV
   and Part V"), grep both, quote both, then state the comparison.
   Do not state the synthesis without showing the parts.

5. **No "may", "might", "could be misleading".** If the failure mode
   is real, state it. If you can't state it as a fact, don't list it.

6. **Inflation is dishonesty.** A list padded with opinions or
   manufactured items costs the operator tokens, time, and trust.
   The padding *is* the failure. Refuse it.

**Before sending an audit, run the No Padding Self-Check:**

  - For each item in the list, ask: did I grep this? Can I show the
    line number?
  - For each item: is this a structural failure or a taste call?
  - Is the list inflated to look more thorough than the actual
    finding warrants?
  - If any item fails the check, REMOVE IT or LABEL IT as opinion
    before sending.

The user is not your QA. Be your own QA.

## When in doubt

Stop. Run `validate.py`. Read the actual source. Verify before acting.

— Discipline installed 2026-06-21 by Claude, at Jordan's instruction,
after the duplicate-gloss bug Jordan caught on p8 v2.

— Rule 6 (lineage manifest) added 2026-06-21 same day, at Jordan's
instruction, after his Master 11 caught the candle-position error in
v5.0. Rules 1–5 caught mechanical text bugs; Rule 6 catches ritual
sequencing drift. The pattern: every time Jordan's discernment catches
a class of failure the validator misses, that class becomes a new
validator rule. The discipline tightens against itself.

— No Padding Code added 2026-06-21 same day, after Jordan named the
audit-padding failure directly. The first audit of v5.1 was 15 items;
~8 were real, 3 were manufactured / overstated, ~3 were taste. The
padding pattern is the same Matrix-tax he has named in the master
prompt: forcing the operator to spend discernment to filter noise out
of answers. The No Padding Code refuses that pattern at the structural
level. Discipline-not-validator: there is no greppable check for
padding, but the rules are explicit and the self-check is mandatory.
