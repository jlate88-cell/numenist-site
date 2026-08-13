# Verification-Before-Assertion Hook

Mechanical enforcement layer for the four operating directives. Runs on every
`Stop` event — after Claude finishes a turn — scans the response for factual
claims, attempts verification, and either passes silently, warns into next
turn's context, or blocks the stop to force revision.

## Why this exists

The four directive files (`cosmological`, `truth-wholeness`, `no-assumptions`,
`provenance`) inject behavioral instructions into Claude's context but live
*inside* the same machine that produces failures. This hook lives *outside*
the model — a deterministic process that inspects the draft response before
the turn officially closes.

## Components

- `claim_extractor.py` — regex + heuristics over sentences. Catches `stat`,
  `date`, `quote`, `provenance`, `named_entity`, `tech_assertion`. Exempts
  hedged sentences (`from memory`, `I believe`, `unverified`) and first-
  person process talk (`I will run`, `let me check`).
- `search_backend.py` — Brave Search API client. Reads `BRAVE_API_KEY` env
  var. If absent, emits `{"status": "no_backend"}` and the decision module
  downgrades hard-blocks to soft warnings.
- `verifier.py` — runs claims through the backend with 4-way concurrency,
  18s hard budget, 7-day filesystem cache at `.claude/hooks/verify/cache/`.
- `ledger.py` — session-scoped state at `.claude/hooks/verify/ledger/<sid>.json`.
  Dedupes already-verified claims across turns, tracks block count.
- `decision.py` — three verdicts: `pass`, `warn`, `block`. Hard kinds block;
  tech assertions warn. Block counter capped at 2 per session to prevent
  wedging.
- `stop_verify.py` — entry point. **Checks `stop_hook_active` first** to
  prevent infinite loops (canonical Stop-hook bug per Anthropic issue #55754).

## Hook contract

On `decision: block`, emits `{"decision": "block", "reason": "...",
"suppressOutput": true}` — Claude is forced to produce a revised turn.
On `warn`, emits `additionalContext` injected into the next prompt.
On `pass`, exits 0 silently.

Loop-safety invariant: `stop_hook_active` short-circuits before any other
work happens.

## Latency budget

Target: <8s P50. Hard self-abort at 18s. Settings timeout 25s.
Cache hits are zero-cost.

## To enable real verification

Set `BRAVE_API_KEY` in the environment. Until then, the hook runs in
warn-only mode — surfaces unverified claims as `additionalContext`
into the next turn, doesn't block.

## Test

```bash
echo '{"session_id":"smoke","transcript_path":"/path/to/transcript.jsonl","stop_hook_active":false}' \
  | python3 .claude/hooks/verify/stop_verify.py
```
