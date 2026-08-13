"""Claim extractor — regex + heuristics, exempts hedged + process talk."""
import re
import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    text: str
    kind: str          # stat | named_entity | date | quote | tech_assertion | provenance
    span: tuple

    @property
    def key(self) -> str:
        return hashlib.sha1(self.text.lower().encode()).hexdigest()[:16]


RE_STAT = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|million|billion|trillion|x\b)",
    re.I,
)
RE_DATE = re.compile(
    r"\b(?:in|on|since|by|until|c\.|circa)\s+\d{3,4}\b"
    r"|\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{3,4}\b"
    r"|\b\d{3,4}\s*(?:BCE|CE|BC|AD)\b",
    re.I,
)
RE_QUOTE = re.compile(r"[\"'“‘]([^\"'”’]{12,})[\"'”’]")
RE_NAMED_FACT = re.compile(
    r"\b[A-Z][\w.&-]+(?:\s+[A-Z][\w.&-]+){0,4}\s+"
    r"(?:was|is|were|are|has|have|had|founded|invented|wrote|published|"
    r"released|launched|acquired|leads|reported|announced|attested|preserved|"
    r"discovered|composed|translated|compiled)\b"
)
RE_TECH = re.compile(
    r"\b(?:the|a|an)\s+\w+\s+"
    r"(?:API|function|method|command|flag|option|library|package|class|hook|tool)\s+\w+\b",
    re.I,
)
RE_VERSION = re.compile(r"\b(?:version|v)\s*\d+(?:\.\d+)+\b", re.I)
RE_PROVENANCE = re.compile(
    r"\b(?:first attested|earliest|originally|invented in|proposed in|"
    r"published in|composed in|attributed to|coined by|introduced by)\b",
    re.I,
)

# Hedge & uncertainty markers — sentences containing these are EXEMPT
HEDGE = re.compile(
    r"\b(?:I think|I believe|likely|probably|possibly|might|may|appears|seems|"
    r"in my recollection|from memory|unverified|approximately|roughly|around|"
    r"perhaps|allegedly|reportedly|by some accounts|according to some|"
    r"one tradition holds|in one lineage|the agent reported)\b",
    re.I,
)

# First-person process talk — exempt (not factual claims)
PROCESS = re.compile(
    r"\b(?:I will|I'll|let me|I'm going to|let's|I can|I'd like to|"
    r"I'll now|next, I|I'll start|I'll write|I'll run|I'll commit|"
    r"running|writing|committing|pushing|building)\b",
    re.I,
)

# Code blocks shouldn't be scanned for claims
RE_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)


def sentences(text: str):
    """Cheap sentence splitter."""
    for m in re.finditer(r"[^.!?\n]+[.!?]", text):
        yield m.group(0).strip(), m.span()


def extract_claims(text: str) -> list[Claim]:
    # Strip code blocks first — they shouldn't be claim-scanned
    cleaned = RE_CODE_FENCE.sub("", text)

    out = []
    seen_keys = set()

    for sent, span in sentences(cleaned):
        if len(sent) < 25:
            continue
        if PROCESS.search(sent):
            continue
        if HEDGE.search(sent):
            continue

        matched_kind = None
        for kind, pat in (
            ("stat", RE_STAT),
            ("date", RE_DATE),
            ("quote", RE_QUOTE),
            ("provenance", RE_PROVENANCE),
            ("named_entity", RE_NAMED_FACT),
            ("tech_assertion", RE_TECH),
            ("tech_assertion", RE_VERSION),
        ):
            if pat.search(sent):
                matched_kind = kind
                break

        if matched_kind:
            c = Claim(text=sent, kind=matched_kind, span=span)
            if c.key not in seen_keys:
                seen_keys.add(c.key)
                out.append(c)

    return out


if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    for c in extract_claims(text):
        print(f"[{c.kind}] {c.text}")
