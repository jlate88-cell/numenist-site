"""
reading_compose.py — deterministic reading pipeline (the tuning circuit).

Run this BEFORE writing any cosmological reading. It pulls the data so the
prose has rails. Emits a structured reading object: numerology for the
date, Tarot correspondences for every compound number, and the
houses-and-lords composer output for Jordan's chart.

Usage:
    python3 reading_compose.py 2026-06-26
    python3 reading_compose.py            # defaults to nothing — date REQUIRED
                                          # (no Date.now guessing; pass the
                                          #  date verified from the time hook)

The pipeline is deterministic — no LLM call, no guessing. Same date in ->
same numbers out. That determinism is the framework the Reading Protocol
Directive requires: the antenna tunes against fixed structure.
"""

import sys
import json
from datetime import date

sys.path.insert(0, "reading-engine-additions")
from houses_and_lords import compose_houses_and_lords  # noqa: E402

# ---- Jordan's cached chart (from the Cosmological Directive). The natal
# placements match houses_and_lords.py's verified demo block.
JORDAN_CHART = {
    "asc":     {"sign": "Virgo",     "deg": 18.45},
    "sun":     {"sign": "Pisces",    "deg": 24.87, "house": 7,  "retrograde": False},
    "moon":    {"sign": "Pisces",    "deg": 20.12, "house": 7,  "retrograde": False},
    "mercury": {"sign": "Aries",     "deg": 7.67,  "house": 8,  "retrograde": False},
    "venus":   {"sign": "Aries",     "deg": 26.43, "house": 8,  "retrograde": False},
    "mars":    {"sign": "Gemini",    "deg": 20.73, "house": 10, "retrograde": False},
    "jupiter": {"sign": "Leo",       "deg": 3.88,  "house": 12, "retrograde": True},
    "saturn":  {"sign": "Aquarius",  "deg": 3.87,  "house": 6,  "retrograde": False},
    "uranus":  {"sign": "Capricorn", "deg": 13.22, "house": 5,  "retrograde": False},
    "neptune": {"sign": "Capricorn", "deg": 16.32, "house": 5,  "retrograde": False},
    "pluto":   {"sign": "Scorpio",   "deg": 20.35, "house": 3,  "retrograde": True},
}

JORDAN_NUMEROLOGY = {
    "life_path": "11/2",
    "expression": 9,
    "soul_urge": 5,
    "personality": 4,
    "birthday": 6,
    "personal_year_2026": 1,
    "active_pinnacle_2026_2034": 8,
}

# Tarot correspondences for compound numbers (Cosmological Directive table).
TAROT = {
    10: "Wheel of Fortune", 11: "Justice (or Strength)", 12: "Hanged Man",
    13: "Death", 14: "Temperance", 15: "Devil", 16: "Tower", 17: "Star",
    18: "Moon", 19: "Sun", 20: "Judgement", 21: "World", 22: "Fool/Master",
}
KARMIC_DEBT = {13, 14, 16, 19}


def digit_sum(n: int) -> int:
    return sum(int(c) for c in str(n))


def reduce_keep_compound(n: int):
    """Reduce to a single digit but report the last compound number seen
    on the way (so 15 -> compound 15, reduced 6)."""
    steps = [n]
    while n > 9:
        n = digit_sum(n)
        steps.append(n)
    # the compound is the value just before the final single digit, if any
    compound = steps[-2] if len(steps) >= 2 else steps[0]
    return {"reduced": steps[-1], "compound": compound, "chain": steps}


def personal_day(d: date) -> dict:
    """Jordan's Personal Day. PY 2026 = 1. PM = PY + month, reduced. PD =
    PM + day-digits, reduced. Keep the compound for Tarot."""
    py = JORDAN_NUMEROLOGY["personal_year_2026"]
    pm_raw = py + d.month
    pm = reduce_keep_compound(pm_raw)["reduced"]
    pd_raw = pm + digit_sum(d.day)
    pd = reduce_keep_compound(pd_raw)
    return {
        "personal_year": py,
        "personal_month_raw": pm_raw, "personal_month": pm,
        "personal_day_raw": pd_raw,
        "personal_day_compound": pd["compound"],
        "personal_day_reduced": pd["reduced"],
        "personal_day_chain": pd["chain"],
    }


def universal_day(d: date) -> dict:
    raw = sum(int(c) for c in d.strftime("%Y%m%d"))
    u = reduce_keep_compound(raw)
    return {"raw": raw, "compound": u["compound"], "reduced": u["reduced"],
            "chain": u["chain"]}


def tarot_for(n: int):
    label = TAROT.get(n)
    return {"number": n, "card": label, "karmic_debt": n in KARMIC_DEBT} if label else None


def compose(d: date) -> dict:
    pd = personal_day(d)
    ud = universal_day(d)
    tarot_notes = []
    for n in {pd["personal_day_compound"], ud["compound"]}:
        t = tarot_for(n)
        if t:
            tarot_notes.append(t)
    houses = compose_houses_and_lords(JORDAN_CHART)
    return {
        "date": d.isoformat(),
        "weekday": d.strftime("%A"),
        "numerology": {
            "personal_day": pd,
            "universal_day": ud,
            "tarot": tarot_notes,
            "static_chart": JORDAN_NUMEROLOGY,
        },
        "houses_and_lords": houses,
        "frame_reminder": (
            "Read every house through active Pinnacle 8 (2026-2034, material "
            "mastery) and Personal Year 1 (founding). Do not frame money as "
            "permanently hard under the 8 Pinnacle."
        ),
    }


def main():
    if len(sys.argv) < 2:
        print("usage: python3 reading_compose.py YYYY-MM-DD  (date required; "
              "pass the date verified from the time hook, do not guess)")
        sys.exit(2)
    try:
        y, m, dd = (int(x) for x in sys.argv[1].split("-"))
        d = date(y, m, dd)
    except Exception as e:
        print(f"bad date '{sys.argv[1]}': {e}")
        sys.exit(2)
    out = compose(d)
    # save a copy at root so reading_validator.py can verify [ENGINE] quotes
    with open("reading_output_latest.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
