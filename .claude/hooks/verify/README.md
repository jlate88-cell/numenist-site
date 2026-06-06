# Verification-Before-Assertion Hook

A Stop-event hook that scans the assistant's response for unverified factual
claims and either passes the turn, injects a soft warning into the next turn,
or forces a revision via `decision: "block"`.

## Files

- `stop_verify.py` — entry point. Reads transcript JSONL, extracts claims,
  verifies them, decides pass/warn/block.
- `claim_extractor.py` — regex + heuristics. Date / stat / quote / named_entity
  / tech_assertion / provenance kinds. Exempts hedged language ("from memory…",
  "I believe…", "unverified") and process talk ("I will check…", "let me…").
- `verifier.py` — runs each claim through `search_backend.py` with 7-day cache
  and bounded concurrency. P50 well under 8s.
- `ledger.py` — session-level JSON ledger at `ledger/<session_id>.json`.
  Tracks verified / unknown claims and block count.
- `decision.py` — pass / warn / block logic. Two-strike escape valve prevents
  wedging.
- `search_backend.py` — Brave Search via `BRAVE_API_KEY` env var. Falls back
  to `no_backend` mode when key is missing (architecture still works, all
  claims route to soft warning instead of hard block).

## Wiring

`.claude/settings.json` registers the Stop hook with 25s timeout. The hook
itself self-aborts at 18s to leave headroom.

## Loop safety

- `stop_hook_active` is checked as the first executable line in `stop_verify.py`
  — exit 0 immediately if true. Without this, every revision triggers another
  verification pass forever.
- Max 2 blocks per session — after that, hard-blocks downgrade to soft warnings
  so the human breaks the loop rather than the hook.

## Activating real verification

```bash
export BRAVE_API_KEY=your-key-here   # ~$3 / 1000 queries
```

Without a key, the hook still detects and lists factual claims as soft warnings
attached to the next turn's context.

## Manual smoke test

```bash
echo '{"session_id":"smoke","transcript_path":"/path/to/transcript.jsonl","stop_hook_active":false}' \
  | python3 .claude/hooks/verify/stop_verify.py
```

Exit 0 with JSON on stdout (or empty if pass).
