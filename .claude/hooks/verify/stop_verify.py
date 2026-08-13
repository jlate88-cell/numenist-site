#!/usr/bin/env python3
"""Stop hook entry — reads transcript, extracts claims, verifies, decides.

The whole architecture targets <8s P50 with an 18s hard self-abort,
well within the 25s settings.json timeout.

CRITICAL: stop_hook_active is checked first to prevent infinite loops.
"""
import json
import pathlib
import sys
import time

# Make sibling modules importable
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from claim_extractor import extract_claims  # noqa: E402
from verifier import verify_batch  # noqa: E402
from ledger import Ledger  # noqa: E402
from decision import decide  # noqa: E402


HARD_BUDGET_SEC = 18.0
MIN_MESSAGE_LEN = 40


def read_last_assistant(transcript_path: str) -> str:
    """Walk the JSONL transcript backward to find the last assistant text."""
    try:
        lines = pathlib.Path(transcript_path).read_text().splitlines()
    except Exception:
        return ""
    for line in reversed(lines):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") == "assistant" or rec.get("role") == "assistant":
            msg = rec.get("message", rec)
            content = msg.get("content", "")
            if isinstance(content, list):
                return "\n".join(
                    b.get("text", "")
                    for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            if isinstance(content, str):
                return content
    return ""


def main():
    t0 = time.time()
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # CRITICAL loop guard — non-negotiable
    if payload.get("stop_hook_active"):
        sys.exit(0)

    # Source: prefer explicit last_assistant_message if harness provides it,
    # otherwise walk the transcript JSONL
    text = (
        payload.get("last_assistant_message")
        or read_last_assistant(payload.get("transcript_path", ""))
    )
    if not text or len(text) < MIN_MESSAGE_LEN:
        sys.exit(0)

    session_id = payload.get("session_id", "unknown")
    try:
        ledger = Ledger(session_id)
    except Exception:
        # If ledger can't load, fail open — don't block the user
        sys.exit(0)

    claims = extract_claims(text)
    novel = [c for c in claims if not ledger.is_verified(c.key)]

    if not novel:
        sys.exit(0)

    remaining = HARD_BUDGET_SEC - (time.time() - t0)
    if remaining < 2.0:
        sys.exit(0)

    results = verify_batch(novel, time_budget=remaining)
    ledger.record_batch(results)

    verdict = decide(results, ledger)

    if verdict.action == "block":
        json.dump({
            "decision": "block",
            "reason": verdict.reason,
            "suppressOutput": True,
        }, sys.stdout)
    elif verdict.action == "warn":
        json.dump({
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": verdict.reason,
            }
        }, sys.stdout)
    # action == "pass": exit silently

    sys.exit(0)


if __name__ == "__main__":
    main()
