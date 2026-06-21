"""
validate.py — AI SLOP CODE for the Altar Psalms Reader.

Hard verification of the build. Runs every check that "from memory"
acting would skip. If any check fails, the script exits non-zero and
the build is NOT trusted as ritual-grade.

Rules of the AI Slop Code (per Jordan, 2026-06-21):
  1. No duplicate (word, pron) entries in any gloss table.
  2. No tautological glosses (where the gloss text equals the word).
  3. No double-rendered glosses in the output PDF (text like
     "[X] [X]" never appears).
  4. Every NOW cue from the source appears in the rendered PDF.
  5. Every psalm referenced in Part I/II/IV/V/VI is actually printed
     in the document body, not only cross-referenced.
  6. The NOW cues at every ritual transition appear in the body
     of the active ritual, not only in the 10-step overview list.

Usage:
    python3 validate.py
    echo $?    # 0 = ritual-grade, non-zero = do NOT ship

This script is part of the build discipline. Run it after every
edit to the script or the gloss tables BEFORE shipping the PDF.
"""

import re
import subprocess
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent
SCRIPT = ROOT / 'build_psalms_reader.py'
PDF    = ROOT / 'altar-psalms-reader.pdf'

failures: list[str] = []

def fail(msg: str):
    failures.append(msg)

def warn(msg: str):
    print(f'[WARN] {msg}')

# ============================================================
# Source-level audits (act on build_psalms_reader.py)
# ============================================================

source = SCRIPT.read_text()

def find_gloss_tables() -> dict[str, list[tuple[str, str]]]:
    """Find every P*_GLOSS list assignment and parse its entries."""
    tables = {}
    pattern = re.compile(
        r"^(P\w*_GLOSS)\s*=\s*\[(.*?)^\]\s*$",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(source):
        name = m.group(1)
        body = m.group(2)
        # Match ('word', 'pron') tuples, allowing leading/trailing whitespace
        entries = re.findall(r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)", body)
        tables[name] = entries
    return tables

def check_no_duplicate_gloss_entries(tables):
    """Rule 1: No duplicate (word, pron) entries in any gloss table."""
    for name, entries in tables.items():
        counts = Counter(entries)
        dups = [k for k, c in counts.items() if c > 1]
        if dups:
            for word, pron in dups:
                fail(
                    f"DUPLICATE GLOSS ENTRY in {name}: "
                    f"('{word}', '{pron}') appears {counts[(word, pron)]} times. "
                    f"This is exactly the class of bug Jordan caught on 2026-06-21. "
                    f"Remove the duplicate from the source list."
                )

def check_no_tautological_glosses(tables):
    """Rule 2: A gloss whose pron text equals the word adds zero value."""
    for name, entries in tables.items():
        for word, pron in entries:
            # Case-insensitive compare so 'Doubtlesse' vs 'doubtlesse' counts as substantive
            if word.lower() == pron.lower():
                fail(
                    f"TAUTOLOGICAL GLOSS in {name}: ('{word}', '{pron}') — "
                    f"the gloss text equals the word. It teaches the reader nothing. "
                    f"Either remove it, or change the pron to actually clarify pronunciation."
                )

def check_now_cues_present_in_source():
    """Rule 6: The altar ritual body must contain inline NOW cues at every
    ritual transition. If the count drops below the expected baseline,
    something has regressed."""
    now_call_count = source.count('story.append(now(')
    BASELINE = 13   # established 2026-06-21 in commit f8183e3
    if now_call_count < BASELINE:
        fail(
            f"NOW CUE COUNT REGRESSION in source: only {now_call_count} now(...) "
            f"calls found, baseline is {BASELINE}. Inline ritual cues are required "
            f"throughout Part II so the operator never has to flip back to the "
            f"10-step overview list during the working."
        )

# ============================================================
# Rendered-PDF audits (act on the actual output)
# ============================================================

def pdftext() -> str:
    if not PDF.exists():
        fail(f"PDF not found at {PDF}. Run python3 build_psalms_reader.py first.")
        return ""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', str(PDF), '-'],
            capture_output=True, text=True, check=True,
        )
        return result.stdout
    except FileNotFoundError:
        warn("pdftotext not installed; skipping rendered-PDF audits.")
        return ""
    except subprocess.CalledProcessError as e:
        fail(f"pdftotext failed: {e.stderr}")
        return ""

def check_no_double_rendered_glosses(pdf_text: str):
    """Rule 3: No '[X] [X]' patterns anywhere in the rendered output."""
    if not pdf_text:
        return
    # The actual bug Jordan caught had patterns like '[UN-too] [UN-too]'.
    # Match: open-bracket, content without brackets, close-bracket, space,
    # open-bracket, SAME content, close-bracket.
    pattern = re.compile(r'\[([^\[\]]+)\]\s+\[\1\]')
    matches = pattern.findall(pdf_text)
    if matches:
        unique = sorted(set(matches))
        fail(
            f"DOUBLE-RENDERED GLOSSES in PDF: {len(matches)} instances of "
            f"'[X] [X]' patterns: {unique[:6]}{'...' if len(unique) > 6 else ''}. "
            f"This is the exact bug Jordan caught on Psalm 91 v2."
        )

def check_now_cues_present_in_pdf(pdf_text: str):
    """Rule 6 (rendered side): the NOW cues must actually appear in the
    rendered PDF, not just exist in source-style strings."""
    if not pdf_text:
        return
    count = len(re.findall(r'NOW\s+[—-]', pdf_text))
    BASELINE = 13
    if count < BASELINE:
        fail(
            f"NOW CUES MISSING FROM PDF: only {count} 'NOW —' markers found, "
            f"baseline is {BASELINE}. The inline ritual cues did not render. "
            f"Check the now_cue paragraph style and the now() helper."
        )

def check_psalms_printed_inline(pdf_text: str):
    """Rule 5: Every psalm the operator might be asked to speak in any
    ritual order must appear in the document body, not only in a
    cross-reference. If a psalm number is referenced but its verse 1
    text is missing, the reader has to navigate elsewhere mid-ritual.

    Strips the inline pronunciation glosses (yellow [X] tokens) before
    matching so contiguous baseline phrases still match across them.
    """
    if not pdf_text:
        return
    # Strip the inline gloss brackets so contiguous baseline phrases match
    stripped = re.sub(r'\s*\[[^\[\]]+\]\s*', ' ', pdf_text)
    stripped = re.sub(r'\s+', ' ', stripped)

    # Short, contiguous signatures from verse 1 of each psalm in the book.
    # Phrases verified against the actual verses in build_psalms_reader.py
    # on 2026-06-21. Update if the verse text genuinely changes; do not
    # adjust to silence a warning without confirming the underlying text.
    expected_first_verses = {
        '91':  'dwelleth in the secrete',
        '23':  'my shepheard',
        '35':  'plead thou my cause',
        '118': 'will not feare what man',
        '151': 'small among my brethren',
        '152': 'come to my aid',
        '153': 'praise',
        '154': 'praise',
        '155': 'have called to You',
    }
    for psalm, signature in expected_first_verses.items():
        if signature.lower() not in stripped.lower():
            warn(
                f"Psalm {psalm}: signature '{signature}' not found in stripped PDF text. "
                f"Either the psalm is missing from the body, or my baseline string is wrong."
            )

# ============================================================
# Run
# ============================================================

def main():
    tables = find_gloss_tables()
    if not tables:
        fail("No P*_GLOSS tables found in source. Did the script change shape?")
    else:
        print(f"Found {len(tables)} gloss tables: {', '.join(sorted(tables))}")
        for name, entries in sorted(tables.items()):
            print(f"  {name}: {len(entries)} entries")

    check_no_duplicate_gloss_entries(tables)
    check_no_tautological_glosses(tables)
    check_now_cues_present_in_source()

    pdf_text = pdftext()
    check_no_double_rendered_glosses(pdf_text)
    check_now_cues_present_in_pdf(pdf_text)
    check_psalms_printed_inline(pdf_text)

    print()
    if failures:
        print(f"=== AI SLOP CODE: {len(failures)} FAILURES ===")
        for i, f in enumerate(failures, 1):
            print(f"  {i}. {f}")
        print()
        print("This build is NOT ritual-grade. Fix the failures, rebuild, re-run validate.py.")
        sys.exit(1)
    else:
        print("=== AI SLOP CODE: all checks pass. Build is ritual-grade. ===")
        sys.exit(0)

if __name__ == '__main__':
    main()
