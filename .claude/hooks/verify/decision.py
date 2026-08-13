"""Decision module — pass / warn / block based on verification results."""
from dataclasses import dataclass


@dataclass
class Verdict:
    action: str          # "pass" | "warn" | "block"
    reason: str = ""


# Hard-block on these claim kinds when unverified
HARD_BLOCK_KINDS = {"stat", "date", "quote", "named_entity", "provenance"}
WARN_KINDS = {"tech_assertion"}

# Max blocks per session — escape valve to prevent wedging
MAX_BLOCKS_PER_SESSION = 2


def decide(results, ledger) -> Verdict:
    # If the search backend isn't configured, downgrade everything to warn
    no_backend = all(r.get("status") == "no_backend" for r in results) if results else False
    if no_backend and results:
        bullets = "\n".join(f"- ({r['claim'].kind}) {r['claim'].text}" for r in results[:4])
        return Verdict("warn", reason=(
            "Verification hook detected the following factual claims in your "
            "previous response, but no search backend is configured "
            "(set BRAVE_API_KEY to enable verification):\n"
            f"{bullets}\n"
            "These were not verified. The user's no-assumptions / truth-wholeness "
            "directives still apply — flag any claim you didn't verify in-turn."
        ))

    failed_hard = [
        r for r in results
        if r["status"] not in ("verified",) and r["claim"].kind in HARD_BLOCK_KINDS
    ]
    failed_soft = [
        r for r in results
        if r["status"] not in ("verified",) and r["claim"].kind in WARN_KINDS
    ]

    # Escape valve: if blocked twice already, downgrade to warn — let the
    # human break the loop rather than the hook.
    if ledger.block_count() >= MAX_BLOCKS_PER_SESSION:
        failed_soft = failed_hard + failed_soft
        failed_hard = []

    if failed_hard:
        bullets = "\n".join(
            f"- ({r['claim'].kind}) {r['claim'].text}"
            for r in failed_hard[:6]
        )
        ledger.bump_block()
        return Verdict("block", reason=(
            "Before finalizing, verify the following factual claims in your "
            "previous draft. For each: either (a) cite a source you actually "
            "checked via tool use, (b) rewrite with an explicit hedge "
            "(\"from memory…\", \"I'm not sure but…\", \"unverified — \"), "
            "or (c) remove the claim. Do NOT re-assert without verification. "
            "This directive comes from the user's mechanically-enforced "
            "verification hook, not a soft request.\n\n"
            f"{bullets}"
        ))

    if failed_soft:
        bullets = "\n".join(f"- {r['claim'].text}" for r in failed_soft[:4])
        return Verdict("warn", reason=(
            "Verification hook: these technical assertions in the last response "
            f"were not corroborated by a quick verification pass:\n{bullets}\n"
            "Treat as soft — if the user relies on any of them, verify first."
        ))

    return Verdict("pass")
