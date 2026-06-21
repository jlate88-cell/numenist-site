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

Five rules. The validator checks every one of them mechanically:

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

4. **The NOW cue baseline must hold.** Part II of the reader contains 13
   inline "NOW —" cues that guide the operator through the ritual
   without flipping back to the 10-step overview. The validator counts
   them in source and in the rendered PDF; either count below baseline
   fails the build.

5. **Every psalm referenced in any ritual order must be printed inline,
   not cross-referenced.** The validator checks every psalm's verse-1
   signature against the rendered PDF.

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

The session MUST follow this protocol exactly:

1. **Read the relevant section of the source FIRST.** Do not edit
   blindly. Use the `Read` tool or `Grep`. Verify what is there.
2. **Identify EVERY existing entry that touches your change.** If
   you are adding gloss entries, grep the table for the words you are
   about to add. If a word is already glossed, do not add it again.
3. **Make the edit.**
4. **Rebuild:** `python3 build_psalms_reader.py`.
5. **Run the validator:** `python3 validate.py`.
6. **If the validator reports any FAIL, fix the failure and re-run
   from step 4. Do NOT ship a build that fails validation.**
7. **Visually spot-check the rendered PDF** for the page(s) you
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

## When in doubt

Stop. Run `validate.py`. Read the actual source. Verify before acting.

— Discipline installed 2026-06-21 by Claude, at Jordan's instruction,
after the duplicate-gloss bug Jordan caught on p8 v2.
