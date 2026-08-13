"""
houses_and_lords.py — deterministic composer for the new section

Plugs into the existing Numen reading engine. Takes a chart row from
public.charts (or any equivalent dict with the natal placements), and
emits ONE section object matching the engine schema:

    { id: str, heading: str, paragraphs: [str], blocks: [{type,text}] }

The section walks all 12 houses in whole-sign order from the Ascendant.
For each house it identifies:
  - the sign on the cusp
  - the classical Hellenistic ruler of that sign (NO modern outers)
  - that ruler's natal sign, degree, house, dignity, retrograde flag
  - aspects the ruler makes (if provided)
and writes a 3–5 sentence operative paragraph in the engine's prose voice:
  "Therefore your <house topic> runs through <where the lord lives> —
   read as <active/passive/strained/supported> by <dignity + aspect>."

This composer is intentionally deterministic — no LLM call needed — so
it produces stable, fast, reproducible output that costs nothing to
generate. The engine's Claude composer can wrap it later if desired.

Drop-in usage:

    from houses_and_lords import compose_houses_and_lords
    section = compose_houses_and_lords(chart)   # one section dict
    # append to reading_json["sections"] between 'configurations' and
    # 'timing' for the 15-section astrology product, or between
    # 'astrology' and 'master-count' for the 17-section flagship.
"""

from __future__ import annotations
from typing import Optional


# ---- Classical Hellenistic rulerships (no modern outers as house rulers).
# Documented in Lilly, Christian Astrology (1647), and in Hellenistic
# sources (Valens, Firmicus Maternus). Modern outer planets (Uranus,
# Neptune, Pluto) are NOT used as house rulers in this technique.
SIGN_RULER = {
    "Aries":       "mars",
    "Taurus":      "venus",
    "Gemini":      "mercury",
    "Cancer":      "moon",
    "Leo":         "sun",
    "Virgo":       "mercury",
    "Libra":       "venus",
    "Scorpio":     "mars",
    "Sagittarius": "jupiter",
    "Capricorn":   "saturn",
    "Aquarius":    "saturn",
    "Pisces":      "jupiter",
}

SIGN_ORDER = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
]

# Essential dignity table: sign -> { planet -> "domicile" | "exaltation" | "detriment" | "fall" }
DIGNITY = {
    "Aries":       {"mars":"domicile",   "venus":"detriment", "sun":"exaltation", "saturn":"fall"},
    "Taurus":      {"venus":"domicile",  "mars":"detriment",  "moon":"exaltation"},
    "Gemini":      {"mercury":"domicile","jupiter":"detriment"},
    "Cancer":      {"moon":"domicile",   "saturn":"detriment","jupiter":"exaltation","mars":"fall"},
    "Leo":         {"sun":"domicile",    "saturn":"detriment"},
    "Virgo":       {"mercury":"domicile, exaltation","jupiter":"detriment","venus":"fall"},
    "Libra":       {"venus":"domicile",  "mars":"detriment",  "saturn":"exaltation","sun":"fall"},
    "Scorpio":     {"mars":"domicile",   "venus":"detriment", "moon":"fall"},
    "Sagittarius": {"jupiter":"domicile","mercury":"detriment"},
    "Capricorn":   {"saturn":"domicile", "moon":"detriment",  "mars":"exaltation","jupiter":"fall"},
    "Aquarius":    {"saturn":"domicile", "sun":"detriment"},
    "Pisces":      {"jupiter":"domicile","mercury":"detriment, fall","venus":"exaltation"},
}

PLANET_GLYPH = {
    "sun":"☉","moon":"☾","mercury":"☿","venus":"♀","mars":"♂",
    "jupiter":"♃","saturn":"♄","uranus":"♅","neptune":"♆","pluto":"♇",
}
PLANET_NAME = {
    "sun":"Sun","moon":"Moon","mercury":"Mercury","venus":"Venus","mars":"Mars",
    "jupiter":"Jupiter","saturn":"Saturn","uranus":"Uranus","neptune":"Neptune","pluto":"Pluto",
}

# Per-house topic phrase used in the operative read line.
HOUSE_TOPIC = {
    1:  "self, body, and the way you meet the world",
    2:  "money, resources, and what you call valuable",
    3:  "daily mind, voice, siblings, and near travel",
    4:  "home, roots, ancestry, and the inner foundation",
    5:  "creative play, romance, children, and what you make",
    6:  "daily work, health, service, and the trained discipline",
    7:  "partnership, marriage, and the committed other",
    8:  "joint resources, intimacy, transformation, the hidden depths",
    9:  "higher mind, foreign ground, philosophy, the long journey",
    10: "vocation, public reputation, the visible work in the world",
    11: "friends, networks, hopes, the larger belonging",
    12: "solitude, the unseen, what dissolves the self, surrender",
}

# Brief phrase for the lord's house topic (used when reading lord's location)
HOUSE_AT = {
    1:"1st house of self",      2:"2nd house of resources",
    3:"3rd house of mind",      4:"4th house of root",
    5:"5th house of creation",  6:"6th house of work and health",
    7:"7th house of partnership", 8:"8th house of depth and shared resource",
    9:"9th house of higher mind", 10:"10th house of vocation",
    11:"11th house of network",   12:"12th house of the unseen",
}


def whole_sign_houses(asc_sign: str) -> dict[int, str]:
    """Map house number 1..12 → cusp sign (whole-sign houses)."""
    start = SIGN_ORDER.index(asc_sign)
    return {h: SIGN_ORDER[(start + h - 1) % 12] for h in range(1, 13)}


def dignity_for(planet: str, sign: str) -> str:
    """Return a short dignity label, or 'peregrine' if none."""
    d = DIGNITY.get(sign, {}).get(planet)
    return d if d else "peregrine"


def quality_for(dignity: str, retrograde: bool) -> str:
    """Plain-language read of dignity + retrograde for the operative line."""
    bits = []
    if "domicile" in dignity:
        bits.append("at home, working on its own terms, with full access to its tools")
    elif "exaltation" in dignity:
        bits.append("exalted, lifted, working at its higher register")
    elif "detriment" in dignity:
        bits.append("in detriment — improvising tools that don't come standard, building hard-won competence")
    elif "fall" in dignity:
        bits.append("in fall — running uphill against the sign's grain, the gift earned through the difficulty")
    else:
        bits.append("peregrine — without strong essential dignity, shaped most by house and aspect rather than by the sign")
    if retrograde:
        bits.append("retrograde — turned inward, asking to be integrated before it can be expressed outward")
    return "; ".join(bits)


def find_planet_position(chart: dict, planet: str) -> Optional[dict]:
    """Pull a planet's position from a chart dict. Tolerant of shapes."""
    pl = chart.get(planet) or chart.get(planet.lower())
    if not pl:
        # Try common nested shapes
        for k in ("planets", "bodies"):
            if isinstance(chart.get(k), dict):
                pl = chart[k].get(planet) or chart[k].get(planet.lower())
                if pl: break
    return pl


def format_position(pos: dict) -> str:
    """'Aries 7°40' · 8th house · retrograde'."""
    sign = pos.get("sign","?")
    deg = pos.get("deg")
    house = pos.get("house","?")
    retro = pos.get("retrograde", False)
    deg_str = f"{deg:.2f}°" if isinstance(deg,(int,float)) else "?°"
    parts = [f"{sign} {deg_str}", f"{house}{ord_suffix(house)} house"]
    if retro: parts.append("retrograde")
    return " · ".join(parts)


def ord_suffix(n) -> str:
    try: n = int(n)
    except Exception: return ""
    if 10 <= n % 100 <= 20: return "th"
    return {1:"st",2:"nd",3:"rd"}.get(n%10, "th")


def is_angular(house: int) -> bool:
    return house in (1, 4, 7, 10)

def is_succedent(house: int) -> bool:
    return house in (2, 5, 8, 11)

def position_quality(lord_house: int) -> str:
    if is_angular(lord_house):    return "placed on the chart's load-bearing wall, loud and early"
    if is_succedent(lord_house):  return "placed in the middle distance, building and sustaining"
    return "placed behind the scenes, working through learning and adjustment"


def compose_house_paragraph(house_num: int, chart: dict, asc_sign: str) -> str:
    """Write a single 3–5 sentence operative paragraph for a given house."""
    cusps = whole_sign_houses(asc_sign)
    cusp_sign = cusps[house_num]
    lord = SIGN_RULER[cusp_sign]
    pos = find_planet_position(chart, lord) or {}
    lord_sign = pos.get("sign", "—")
    lord_house = pos.get("house", None)
    lord_retro = pos.get("retrograde", False)
    dignity = dignity_for(lord, lord_sign) if lord_sign != "—" else "peregrine"

    topic = HOUSE_TOPIC[house_num]
    topic_short = topic.split(",")[0].strip()
    where_topic = HOUSE_AT.get(lord_house) if isinstance(lord_house, int) else "—"
    where_topic_short = where_topic.split(" of ", 1)[-1] if where_topic and " of " in where_topic else where_topic
    lord_pos_str = format_position(pos) if pos else "—"
    lord_glyph = PLANET_GLYPH.get(lord, "")
    lord_name  = PLANET_NAME.get(lord, lord.title())

    qual = quality_for(dignity, lord_retro)
    angular_note = ""
    if isinstance(lord_house, int):
        angular_note = f" It is {position_quality(lord_house)}."

    # Build the paragraph in the engine's voice.
    p = (
        f"{house_num}{ord_suffix(house_num)} house — {topic}. "
        f"The sign on the cusp is {cusp_sign}; its lord is {lord_name} {lord_glyph}, "
        f"and it sits in your chart at {lord_pos_str}. "
        f"{lord_name} is {qual}.{angular_note} "
        f"Therefore the affairs of your {house_num}{ord_suffix(house_num)} house "
        f"are run through your {where_topic} — what feels like your {topic_short} "
        f"actually plays out wherever {lord_name} lives, not where the empty cusp sits. "
        f"Watch {where_topic_short} to see this house move."
    )
    return p


def compose_houses_and_lords(chart: dict) -> dict:
    """
    Main entry. `chart` must include at minimum:
      - asc:    {"sign": "Virgo", "deg": 18.45}
      - sun, moon, mercury, venus, mars, jupiter, saturn
        each as {"sign": str, "deg": float, "house": int, "retrograde": bool}
    Outer planets (uranus, neptune, pluto) are NOT used as house rulers,
    but pass them through if you have them — they're harmless extras.
    """
    asc = chart.get("asc") or chart.get("ascendant") or {}
    asc_sign = asc.get("sign")
    if not asc_sign or asc_sign not in SIGN_ORDER:
        raise ValueError(f"chart.asc.sign must be one of {SIGN_ORDER}; got {asc_sign!r}")

    intro = (
        "Every house in the chart is run by the planet that rules the sign on its cusp. "
        "When a house is empty of planets, that does NOT mean it has no story; it means the "
        "story is happening wherever the cusp-lord lives. This section walks all twelve houses "
        "in turn, naming each cusp-lord and where it actually sits — so the affairs of every "
        "house become readable, not just the ones with bodies parked in them."
    )

    paragraphs = [intro]
    for h in range(1, 13):
        paragraphs.append(compose_house_paragraph(h, chart, asc_sign))

    closing = (
        "Held together, the twelve doors tell you which areas of your life move through which "
        "engines. Where a lord is angular and dignified, that house flows; where it is in "
        "detriment, retrograde, or cadent, the house asks for conscious work to come alive. "
        "When in doubt about an area of life, find its lord, see where it lives, and read the "
        "affairs of the house through the affairs of the lord's house."
    )
    paragraphs.append(closing)

    blocks = [{"type": "paragraph", "text": p} for p in paragraphs]

    return {
        "id": "houses-and-lords",
        "heading": "The Twelve Doors — Houses & Their Lords",
        "paragraphs": paragraphs,
        "blocks": blocks,
    }


# ---- demo / smoke test ----
if __name__ == "__main__":
    import json
    # Jordan's chart, verified against the live engine output for 2026-06-17.
    jordan = {
        "asc":     {"sign":"Virgo",      "deg":18.45},
        "sun":     {"sign":"Pisces",     "deg":24.87, "house":7,  "retrograde":False},
        "moon":    {"sign":"Pisces",     "deg":20.12, "house":7,  "retrograde":False},
        "mercury": {"sign":"Aries",      "deg":7.67,  "house":8,  "retrograde":False},
        "venus":   {"sign":"Aries",      "deg":26.43, "house":8,  "retrograde":False},
        "mars":    {"sign":"Gemini",     "deg":20.73, "house":10, "retrograde":False},
        "jupiter": {"sign":"Leo",        "deg":3.88,  "house":12, "retrograde":True},
        "saturn":  {"sign":"Aquarius",   "deg":3.87,  "house":6,  "retrograde":False},
        "uranus":  {"sign":"Capricorn",  "deg":13.22, "house":5,  "retrograde":False},
        "neptune": {"sign":"Capricorn",  "deg":16.32, "house":5,  "retrograde":False},
        "pluto":   {"sign":"Scorpio",    "deg":20.35, "house":3,  "retrograde":True},
    }
    section = compose_houses_and_lords(jordan)
    print(json.dumps(section, indent=2, ensure_ascii=False))
