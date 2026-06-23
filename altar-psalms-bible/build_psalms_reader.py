"""
The Altar Psalms Reader — Plain Order & Pronunciation
======================================================

The operator's everyday edition. Companion #2 to The Altar Psalms Bible
and the Working Integration document.

What this book does that the other two don't:
  1. Sorts the seven Psalms into USE-CATEGORIES (everyday, altar ritual,
     money & prosperity, protection, crisis, consecration, clarity,
     travel, funerary) with the right ORDER for each context.
  2. Gives PRONUNCIATION for every hard word — the Geneva 1599 period
     spellings, the Hebrew altar lines, and the divine Names.
  3. Applies THE MONAD RULE consistently: every English substitute-title
     "Lord" in spoken text reads "Monad." Actual Names (Elyon, Shaddai,
     YHWH-spoken-as-Adonai, Elohim, God, most High, Almightie) stay.
     Every substitution point is listed so the operator can audit.

Structure note (v3): Daily Reading at the front (Parts I and II);
Pronunciation Guide as Part III reference. Psalm 118:6-9 sovereignty
seal between Psalm 23 and petition. Psalm 35:1-10 first-sign enemies/
court order in Part VI. Monad Rule extended to gendered pronouns —
"he/him/his" referring to the Monad now reads "the Monad" or "the
Monad's"; the Monad is the Unmanifest, not on the gender spectrum.
Yellow inline highlight for every archaic Geneva word so the eye
tracks pronunciation in-place; reference tables retained in Part III.

Text sources (verified this session against primary sources):
  - Geneva 1599 Psalms 23 & 91: wording verified against BibleGateway GNV;
    period orthography per the 1599 printing conventions and prior
    facsimile work in the main Altar Psalms Bible.
  - Geneva 1599 Psalm 118:6-9: wording verified against BibleGateway GNV
    in this session; period orthography harmonized to match the book's
    existing 1599 style for consistency.
  - Brenton 1851 LXX Psalm 151: verified against ebible.org.
  - Hebrew Psalm 91:1-2: verified against Sefaria (Masoretic).
  - Psalms 152-155: Charlesworth/Sanders diction as carried in the main
    Altar Psalms Bible; substance verified against Wright 1886
    (tertullian.org) — superscriptions of 152/153 match Wright verbatim.

Hebrew is set on dedicated right-to-left lines only (no inline Hebrew
inside parentheses) to avoid the bidirectional rendering artifacts found
in the Working Integration document.

Compiled for Jordan Ross Atkins / Numen. Atlanta, June 2026.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    PageTemplate, Frame, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Line, Circle, String, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('SerifBold', '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('SerifItalic', '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('SerifBoldItalic', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'))
registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBoldItalic')

INK = HexColor('#1a1a1a')
SUB = HexColor('#5a5a5a')
ACCENT = HexColor('#7a2e2e')
GOLD = HexColor('#8a6a2e')
PAPER = HexColor('#fbf8f1')
GREEN = HexColor('#2e6a3c')

def s(name, **kw):
    base = dict(fontName='Serif', fontSize=11, leading=15, textColor=INK,
                alignment=TA_LEFT, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name=name, **base)

S = {
    'cover_title':   s('cover_title', fontName='SerifBold', fontSize=34, leading=40, alignment=TA_CENTER, spaceAfter=14),
    'cover_sub':     s('cover_sub', fontName='SerifItalic', fontSize=14, leading=20, textColor=SUB, alignment=TA_CENTER, spaceAfter=6),
    'cover_line':    s('cover_line', fontSize=10, textColor=SUB, alignment=TA_CENTER, spaceAfter=3),
    'cover_lineage': s('cover_lineage', fontName='SerifItalic', fontSize=10, textColor=GOLD, alignment=TA_CENTER, spaceAfter=3),
    'part':          s('part', fontName='SerifBold', fontSize=24, leading=30, textColor=ACCENT, alignment=TA_CENTER, spaceBefore=20, spaceAfter=14),
    'h1':            s('h1', fontName='SerifBold', fontSize=18, leading=22, textColor=ACCENT, spaceBefore=16, spaceAfter=8),
    'h2':            s('h2', fontName='SerifBold', fontSize=14, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=5),
    'h3':            s('h3', fontName='SerifBoldItalic', fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
    'body':          s('body', alignment=TA_JUSTIFY, spaceAfter=6),
    'body_left':     s('body_left', spaceAfter=6),
    'small':         s('small', fontSize=9, leading=12, textColor=SUB, spaceAfter=4),
    'small_center':  s('small_center', fontSize=9, leading=12, textColor=SUB, alignment=TA_CENTER, spaceAfter=4),
    'italic':        s('italic', fontName='SerifItalic', spaceAfter=6),
    'quote':         s('quote', leftIndent=20, rightIndent=10, fontName='SerifItalic', spaceAfter=6),
    'verse':         s('verse', leftIndent=14, fontSize=11.5, leading=16.5, spaceAfter=4),
    'speak':         s('speak', leftIndent=14, fontSize=12, leading=17, spaceAfter=5),
    'hebrew':        s('hebrew', fontSize=15, leading=22, alignment=TA_RIGHT, spaceAfter=3),
    'translit':      s('translit', fontName='SerifBoldItalic', fontSize=11, leading=15, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=3),
    'gloss':         s('gloss', fontSize=10, leading=13, alignment=TA_CENTER, textColor=SUB, spaceAfter=8),
    'step':          s('step', fontSize=11.5, leading=16, leftIndent=10, spaceAfter=6),
    'greenbox':      s('greenbox', fontSize=10, leading=13.5, textColor=GREEN, leftIndent=10, spaceAfter=4),
    # Inline ritual instruction — appears AT the moment the operator should
    # perform the gesture, so the reader never has to flip back to the
    # 10-step overview. Distinctive color + bold "NOW —" prefix makes it
    # immediately recognizable as a do-this-right-now interrupt.
    'now_cue':       s('now_cue', fontName='SerifBold', fontSize=12, leading=17,
                       textColor=HexColor('#a02540'),
                       leftIndent=16, rightIndent=16, spaceBefore=8, spaceAfter=8),
}

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

def header_footer(c, doc):
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    if doc.page > 1:
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.4)
        c.line(MARGIN, PAGE_H - MARGIN + 22, PAGE_W - MARGIN, PAGE_H - MARGIN + 22)
        c.setFont('SerifItalic', 9)
        c.setFillColor(SUB)
        title = getattr(doc, 'current_section', 'The Altar Psalms Reader')
        c.drawString(MARGIN, PAGE_H - MARGIN + 28, title)
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 28, f'{doc.page}')
    c.setFont('SerifItalic', 8)
    c.setFillColor(SUB)
    c.drawCentredString(PAGE_W / 2, MARGIN / 2, 'Numen · The Altar Psalms Reader')
    c.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(MARGIN, MARGIN, PAGE_W - 2*MARGIN, PAGE_H - 2*MARGIN, id='main',
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=12)
        self.addPageTemplates([PageTemplate(id='body', frames=frame, onPage=header_footer)])
        self.current_section = ''

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            if flowable.style.name in ('part', 'h1'):
                self.current_section = flowable.getPlainText()

def P(text, style='body'):
    return Paragraph(text, S[style])

def spacer(h=8):
    return Spacer(1, h)

def pagebreak():
    return PageBreak()

def vr(num, txt):
    return Paragraph(f'<b>{num}.</b> {txt}', S['speak'])

# Inline yellow-highlighted pronunciation gloss for archaic words.
# Apply each gloss to the FIRST occurrence in the verse only — once the eye
# has seen it, the rest of the verse can read past it.
GLOSS_BG = "#ffeb80"   # highlighter yellow
GLOSS_FG = "#5a4a1a"   # dark amber text for contrast on the yellow

import re as _re
def gloss_text(txt, glosses):
    out = txt
    seen = set()
    for word, pron in glosses:
        # Defensive deduplication: if the same (word, pron) appears twice
        # in the table, only apply it once. Previously a duplicate entry
        # caused the word to be glossed twice in the rendered verse
        # (e.g. "unto [UN-too] [UN-too]"). Discovered by Jordan p8 v2.
        key = (word, pron)
        if key in seen:
            continue
        seen.add(key)
        marker = f'{word} <font backColor="{GLOSS_BG}" color="{GLOSS_FG}">[{pron}]</font>'
        pattern = r'\b' + _re.escape(word) + r'\b'
        out, n = _re.subn(pattern, marker, out, count=1)
    return out

def vrg(num, txt, glosses):
    return Paragraph(f'<b>{num}.</b> {gloss_text(txt, glosses)}', S['speak'])

def now(txt):
    """Inline ritual cue. Prefixes 'NOW —' and styles distinctively so the
    operator sees the gesture-to-perform at the moment it is needed, without
    flipping back to the 10-step overview."""
    return Paragraph(f'<b>NOW &mdash;</b> {txt}', S['now_cue'])

def cross_diagram():
    """Vector diagram of the Hermetic cross on the body. Five stations:
    1 Forehead → 2 Heart → 3 Right shoulder → 4 Left shoulder → 5 Heart
    (return / seal). Right index finger touches each station; one continuous
    breath through the whole gesture."""
    import math
    rose = HexColor('#a02540')
    sub  = HexColor('#5a5a5a')
    ink  = HexColor('#1a1a1a')

    W, H = 360, 200
    d = Drawing(W, H)
    cx, cy = W/2, H/2 - 6
    arm = 55
    r   = 11

    # Cross arms
    d.add(Line(cx, cy + arm - r, cx, cy + r,
               strokeColor=rose, strokeWidth=1.4))
    d.add(Line(cx + r, cy, cx + arm - r, cy,
               strokeColor=rose, strokeWidth=1.4))
    d.add(Line(cx + arm - r, cy, cx - arm + r, cy,
               strokeColor=rose, strokeWidth=1.4))

    def arrow(x, y, dx, dy):
        # Solid arrowhead with its tip at (x, y), pointing in (dx, dy).
        ang = math.atan2(dy, dx)
        sz  = 5
        x1  = x - sz * math.cos(ang - 0.45)
        y1  = y - sz * math.sin(ang - 0.45)
        x2  = x - sz * math.cos(ang + 0.45)
        y2  = y - sz * math.sin(ang + 0.45)
        d.add(Polygon(points=[x, y, x1, y1, x2, y2],
                      fillColor=rose, strokeColor=rose))

    # 1. forehead → heart  (down stroke)
    arrow(cx, cy + r + 3, 0, -1)
    # 2. heart → right     (rightward)
    arrow(cx + arm - r - 3, cy, 1, 0)
    # 3. right → left      (leftward — long stroke across the body)
    arrow(cx - arm + r + 3, cy, -1, 0)
    # 4. (left → heart, return for the seal — implicit; station 5 is the heart again)

    def station(x, y, n_text):
        d.add(Circle(x, y, r, fillColor=rose, strokeColor=rose))
        d.add(String(x, y - 3.5, n_text,
                     fontName='SerifBold', fontSize=10.5,
                     textAnchor='middle', fillColor=HexColor('#ffffff')))

    station(cx, cy + arm, '1')
    station(cx + arm, cy, '3')
    station(cx - arm, cy, '4')
    station(cx, cy, '2·5')   # 2·5 — start and seal

    # Labels
    d.add(String(cx, cy + arm + r + 11, 'Forehead',
                 fontName='SerifBold', fontSize=10,
                 textAnchor='middle', fillColor=ink))
    d.add(String(cx, cy + arm + r + 23, '(Monad above)',
                 fontName='SerifItalic', fontSize=9,
                 textAnchor='middle', fillColor=sub))

    d.add(String(cx + arm + r + 6, cy + 3, 'Right shoulder',
                 fontName='SerifBold', fontSize=10,
                 textAnchor='start', fillColor=ink))
    d.add(String(cx + arm + r + 6, cy - 8, '(structure)',
                 fontName='SerifItalic', fontSize=9,
                 textAnchor='start', fillColor=sub))

    d.add(String(cx - arm - r - 6, cy + 3, 'Left shoulder',
                 fontName='SerifBold', fontSize=10,
                 textAnchor='end', fillColor=ink))
    d.add(String(cx - arm - r - 6, cy - 8, '(flow)',
                 fontName='SerifItalic', fontSize=9,
                 textAnchor='end', fillColor=sub))

    d.add(String(cx, cy - r - 11, 'Heart',
                 fontName='SerifBold', fontSize=10,
                 textAnchor='middle', fillColor=ink))
    d.add(String(cx, cy - r - 23, '(body altar — start & seal)',
                 fontName='SerifItalic', fontSize=9,
                 textAnchor='middle', fillColor=sub))

    return d

# Geneva 1599 pronunciation tables for inline gloss. Order matters: longer
# phrases first so they win before sub-strings can match.
P91_GLOSS = [
    ('noone day', 'NOON day'),
    ('dwelleth', 'DWELL-uth'),
    ('secrete', 'SEE-kret'),
    ('Almightie', 'all-MY-tee'),
    ('shadowe', 'SHAD-oh'),
    ('fortresse', 'FOR-tres'),
    ('noysome', 'NOY-sum'),
    ('pestilence', 'PES-tih-lens'),
    ('trueth', 'trooth'),
    ('shielde', 'sheeld'),
    ('buckler', 'BUK-ler'),
    ('afraide', 'uh-FRAYD'),
    ('feare', 'feer'),
    ('flyeth', 'FLY-uth'),
    ('darkenesse', 'DARK-nes'),
    ('destroyeth', 'dih-STROY-uth'),
    ('Doubtlesse', 'DOWT-les'),
    ('beholde', 'bee-HOHLD'),
    ('tabernacle', 'TAB-er-nak-ul'),
    ('tenne', 'ten'),
    ('neere', 'neer'),
    ('wayes', 'ways'),
    ('beare', 'bair'),
    ('foote', 'fuut'),
    ('treade', 'tred'),
    ('lyon', 'LY-un'),
    ('aspe', 'asp'),
    ('walke', 'wawk'),
    ('knowen', 'NOH-un'),
    ('heare', 'heer'),
    ('glorifie', 'GLOR-ih-fy'),
    ('satisfie', 'SAT-is-fy'),
    ('shew', 'shoh'),
    # Audit additions — words that genuinely change pronunciation from
    # the eye's expectation. Same-as-word glosses are NOT added because
    # they help nothing and clutter the page.
    # v/u swap entries removed v6: unto/upon/under/over/deliver/cover/give/
    # loved/salvation/evill/runneth over were modernized in the verse text,
    # so their glosses no longer match anything and are dead weight.
    ('winges', 'wings'),
    ('feathers', 'FETH-erz'),
    ('walketh', 'WAWK-uth'),
    ('handes', 'handz'),
    ('yong', 'yung'),
    ('feete', 'feet'),
    ('thine', 'thyn'),
    ('thou', 'thow'),
]

P23_GLOSS = [
    ('Names sake', 'NAYMZ sayk'),
    ('shepheard', 'SHEP-erd'),
    ('greene', 'green'),
    ('soule', 'sohl'),
    ('righteousnesse', 'RY-chus-nes'),
    ('shadowe', 'SHAD-oh'),
    ('walke', 'wawk'),
    ('feare', 'feer'),
    ('staffe', 'staf'),
    ('doest', 'DOO-est'),
    ('anoynt', 'uh-NOYNT'),
    ('oyle', 'oyl'),
    ('cuppe', 'kup'),
    ('Doubtlesse', 'DOWT-les'),
    ('kindnesse', 'KYND-nes'),
    ('mercie', 'MER-see'),
    ('dayes', 'days'),
    ('remaine', 'rih-MAYN'),
    # v/u swap entries removed v6: runneth over / evill / adversaries were
    # modernized in the verse text (runneth over / evill / adversaries).
]

P118_GLOSS = [
    ('feare', 'feer'),
    ('helpe', 'help'),
    ('enemies', 'EN-uh-meez'),
    ('then', 'than'),
    ('princes', 'PRIN-sez'),
    # v/u swap entries removed v6: unto / upon / have were modernized.
]

P35_GLOSS = [
    ('shielde', 'sheeld'),
    ('buckler', 'BUK-ler'),
    ('speare', 'speer'),
    ('soule', 'sohl'),
    ('confounded', 'kon-FOWN-ded'),
    ('chaffe', 'chaf'),
    ('slipperie', 'SLIP-er-ee'),
    ('joyfull', 'JOY-ful'),
    ('rejoyce', 'rih-JOYS'),
    ('miserie', 'MIZ-er-ee'),
    ('spoileth', 'SPOYL-uth'),
    ('poore', 'poor'),
    ('helpe', 'help'),
    # v/u swap entries removed v6: strive / salvation / unawares / privily /
    # deliverest / upon / unto / vp / have were modernized in the verse text.
]

def pron_table(rows, widths=None):
    if widths is None:
        widths = [1.5*inch, 1.7*inch, 3.0*inch]
    data = [[Paragraph('<b>Written</b>', S['small']),
             Paragraph('<b>Say it</b>', S['small']),
             Paragraph('<b>It is just the word</b>', S['small'])]]
    for w, say, mean in rows:
        data.append([Paragraph(w, S['body_left']),
                     Paragraph(f'<b>{say}</b>', S['body_left']),
                     Paragraph(mean, S['small'])])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
        ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#f0ece2')),
    ]))
    return t


story = []

# ============================ COVER ============================
story.append(Spacer(1, 1.3*inch))
story.append(P('THE ALTAR PSALMS READER', 'cover_title'))
story.append(P('Plain Order &amp; Pronunciation', 'cover_sub'))
story.append(Spacer(1, 0.35*inch))
story.append(P('Everyday readings · Altar ritual · Money &amp; prosperity · Protection', 'cover_line'))
story.append(P('Crisis · Consecration · Clarity · Travel · Funerary', 'cover_line'))
story.append(Spacer(1, 0.3*inch))
story.append(P('With the Monad Rule applied and every hard word sounded out', 'cover_line'))
story.append(Spacer(1, 0.45*inch))
story.append(P('— companion to —', 'cover_lineage'))
story.append(P('The Altar Psalms Bible · The Working Integration', 'cover_line'))
story.append(Spacer(1, 0.5*inch))
story.append(P('Compiled for Jordan Ross Atkins · Numen · numenist.com', 'cover_lineage'))
story.append(P('Atlanta · June 2026', 'cover_lineage'))
story.append(pagebreak())

# ============================ HOW TO USE ============================
story.append(P('How to Use This Book', 'h1'))
story.append(P(
    'This is the speaking edition. The Altar Psalms Bible holds the scholarship; the Working '
    'Integration holds the verse-by-verse frequency filter; this book holds <b>what to say, in what '
    'order, for which purpose, and how to pronounce it</b>. Find your situation in the contents, '
    'open to that section, and read aloud. Everything you speak is printed in full where you need it.',
    'body'))
story.append(P('The two basic modes', 'h2'))
story.append(P(
    '<b>Everyday reading</b> — you just woke up. No candle, no altar, two to three minutes. '
    'Section I.',
    'body_left'))
story.append(P(
    '<b>Altar ritual</b> — you are at the altar with the candle. The full working order, '
    'with the sovereignty seal added. Section II.',
    'body_left'))
story.append(P(
    'Pronunciation reference for Geneva 1599 spellings, Hebrew altar lines, and the divine '
    'Names is Section III. Every other section (money &amp; prosperity, protection, crisis, '
    'consecration, clarity, travel, funerary) tells you which psalms to add or swap, and in '
    'what order, for that purpose.',
    'body'))
story.append(spacer(6))

story.append(P('The Monad Rule', 'h2'))
story.append(P(
    'Everywhere the English text used the substitute-title <b>"Lord,"</b> this book reads '
    '<b>"Monad"</b> — the actual Source, the One, the Hermetic ALL. The real Names are kept as '
    'they are: <b>Elyon</b> (the Most High), <b>Shaddai</b> (the Almighty), <b>YHWH</b> (the '
    'Tetragrammaton — spoken aloud as <b>Adonai</b>), <b>Elohim / "my God,"</b> and the English '
    'renderings "the most High" and "the Almightie," which translate Elyon and Shaddai.',
    'body'))
story.append(P(
    'Why: "Lord" is a title, not a Name. It translates Hebrew <i>Adonai</i>, Greek <i>Kyrios</i>, '
    'Latin <i>Dominus</i> — and at the linguistic level it is the same word as <i>Ba\'al</i> '
    '(lord/master). Hosea 2:16 itself records the Monad saying: <i>"You will call Me Ishi, and no '
    'more will you call Me Baali"</i> (verified against the Hebrew at Sefaria). Chaldean: '
    'LORD = 16/7 — the Tower, a karmic-debt number. MONAD = 21/3 — the World, the completion '
    'arcana, the same 21 carried by YESHUA and ELYON. The substitution moves the spoken text '
    'from the Tower vibration to the World vibration.',
    'body'))
story.append(P('The Pronoun Extension', 'h3'))
story.append(P(
    'The Monad has no gender. The Monad is the Unmanifest, the source from which polarity '
    '(including the principle of Gender) emanates — it is not on the spectrum, it generates the '
    'spectrum. The masculine pronouns "he/him/his" in the Geneva text are translation artifacts '
    'inherited from grammatically-gendered Hebrew (no neuter), carried through Greek and Latin, '
    'then hardened into doctrinal masculine deity by patriarchal church structures. The same '
    'editorial-control pattern that gave us "Lord" gave us "He." Both are removed here.',
    'body'))
story.append(P(
    'Wherever the Geneva 1599 used "he/him/his" referring to the Monad, this book reads '
    '<b>"the Monad"</b> or <b>"the Monad\'s"</b>. Specific emanations of the Monad that carry '
    'gender by lineage attestation (Sophia / Ruach HaKodesh — She; the Father-current of the '
    'lineage formula — He) keep their pronouns where they are specifically invoked. Pronouns '
    'referring to the human operator are left in their inherited form.',
    'body'))
story.append(P('Every substitution point in this book, so you can audit:', 'h3'))
story.append(P('· Psalm 91 — LORD→Monad at vv.2, 9; pronoun→Monad at vv.2 (×2), 3, 4 (×4), 11 (×2)', 'body_left'))
story.append(P('· Psalm 23 — LORD→Monad at vv.1, 6; pronoun→Monad at vv.2, 3 (×2)', 'body_left'))
story.append(P('· Psalm 35 — LORD→Monad at vv.1, 5, 6, 9, 10; pronoun→Monad at v.9', 'body_left'))
story.append(P('· Psalm 118 — LORD→Monad at vv.6, 7, 8, 9 (all four)', 'body_left'))
story.append(P('· Psalm 151 — LORD→Monad at v.3 (×2), v.5; pronoun→Monad at vv.3, 4 (×4)', 'body_left'))
story.append(P('· Psalm 152 — LORD→Monad at vv.4, 6', 'body_left'))
story.append(P('· Psalm 153 — LORD→Monad at v.1; pronoun→Monad throughout vv.1–6 (×14)', 'body_left'))
story.append(P('· Psalm 154 — LORD→Monad at v.9; pronoun→Monad at vv.1, 2 (×2), 4 (×3), 6, 7 (×2), 9 (×2), 10, 14, 17 (×3), 20 (×2)', 'body_left'))
story.append(P('· Psalm 155 — pronoun→Monad at v.14 (×2)', 'body_left'))
story.append(P(
    'Twenty title substitutions plus fifty-two pronoun substitutions: seventy-two total. Every other '
    'word of the source texts is unchanged.',
    'small'))
story.append(P('The Yellow Highlights', 'h3'))
story.append(P(
    'Every archaic Geneva 1599 word that does not pronounce as modern English carries a '
    '<font backColor="#ffeb80" color="#5a4a1a">[YELLOW BRACKET]</font> right next to it the '
    'first time it appears in each verse. Eyes track the highlight; never flip pages to find a '
    'pronunciation. The reference tables in Part III remain available for full lookups.',
    'body'))
story.append(pagebreak())

# ============================ PART I — EVERYDAY ============================
story.append(P('PART I', 'part'))
story.append(P('The Everyday Reading', 'cover_sub'))
story.append(P('On rising. No candle. Two to three minutes.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Everyday Order', 'h1'))
story.append(P(
    'This is for the morning you just want to say the Psalms and start the day right — no altar, '
    'no candle, no ritual. The on-rising practice is <b>Psalm 23 spoken on waking</b>; the going-out '
    'practice is <b>Psalm 91 verse 11 spoken three times before stepping out of the house</b>. '
    '<i>Provenance note: both forms are documented Hoodoo working tradition rooted in Selig\'s '
    'Kabbalist frame. Selig\'s own Psalm 23 instruction is fasting + bathing + holy name Jah for '
    'visions; the on-rising daily form is the Hoodoo working layer over Selig. The Psalm 91:11 '
    'doorway recitation is folk Hoodoo, not Selig\'s text.</i>',
    'body'))
story.append(spacer(8))

story.append(P('Psalm 23 — the everyday text', 'h2'))
story.append(P('Geneva 1599, with the Monad Rule at verses 1 and 6.', 'small'))
story.append(spacer(4))
story.append(now('Sit up in bed (or stand if you are already up). One slow breath in, one slow breath out. Then speak Psalm 23 aloud, verse by verse.'))
story.append(P('<i>A Psalme of David.</i>', 'quote'))
story.append(vrg(1, 'The <b>Monad</b> is my shepheard, I shall not want.', P23_GLOSS))
story.append(vrg(2, 'The <b>Monad</b> maketh me to rest in greene pasture, and leadeth me by the still waters.', P23_GLOSS))
story.append(vrg(3, 'The <b>Monad</b> restoreth my soule, and leadeth me in the paths of righteousnesse for the <b>Monad\'s</b> Names sake.', P23_GLOSS))
story.append(vrg(4, 'Yea, though I should walke through the valley of the shadowe of death, I will feare no evill: for thou art with me: thy rod and thy staffe, they comfort me.', P23_GLOSS))
story.append(vrg(5, 'Thou doest prepare a table before me in the sight of mine adversaries: thou doest anoynt mine head with oyle, and my cuppe runneth over.', P23_GLOSS))
story.append(vrg(6, 'Doubtlesse kindnesse and mercie shall follow me all the dayes of my life, and I shall remaine a long season in the house of the <b>Monad</b>.', P23_GLOSS))
story.append(spacer(6))
story.append(P('At verse 4 the voice shifts from third-person to "Thou" — let your voice meet it. In the everyday reading you do not need the crown-touch; that belongs to the altar.', 'small'))
story.append(spacer(8))
story.append(now('Speak one line of gratitude in your own words. <i>&#8220;Thank you for this day.&#8221;</i> &mdash; or whatever rises. One line is enough.'))
story.append(spacer(4))

story.append(P('The door verse — Psalm 91:11, three times', 'h2'))
story.append(vrg(11, 'For the <b>Monad</b> shall give the <b>Monad\'s</b> Angels charge over thee to keepe thee in all thy wayes.', P91_GLOSS))
story.append(spacer(4))
story.append(now('At the door, hand on the latch, before you step out: speak verse 11 three times. Then step through and go live the day.'))
story.append(pagebreak())

# ============================ PART II — ALTAR RITUAL ============================
story.append(P('PART II', 'part'))
story.append(P('The Altar Ritual', 'cover_sub'))
story.append(P('The full working order, at the candle. With the sovereignty seal.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Altar Order', 'h1'))
story.append(P(
    'This is the standing daily working — the Hoodoo structure your ancestors transmitted '
    '(91 opens the perimeter, 23 seals the blessing), applied to the cleaner text, with the '
    'Monad Rule enacted and Psalm 118:6-9 added as the sovereignty seal between the '
    'path-ward and the petition. Ten steps:',
    'body'))
story.append(spacer(4))
story.append(P('<b>1. The Hermetic cross on the body.</b> Forehead → heart → right shoulder → left shoulder → back to heart. One slow breath through the whole gesture. Forehead is the Monad above; heart is the body\'s altar; right is structure; left is flow; the return to heart seals it.', 'step'))
story.append(P('<b>2. The lineage formula, aloud:</b> <i>"In the name of the Father, the Son, and the Holy Spirit."</i> You are invoking the Monad behind those words — not the institutional egregore — through the formula your ancestors carried.', 'step'))
story.append(P('<b>3. Light the candle</b> (or continue the standing burn). The documented Hoodoo order &mdash; Yronwode / Lucky Mojo &mdash; is that the working psalm is spoken <i>as you light the candle</i>, not after. The flame is the seat of the working from this point through the snuff. Every spoken word that follows rides this flame.', 'step'))
story.append(P('<b>4. Psalm 91, aloud</b> — the perimeter (full text next page). If you want the Hebrew opening first: <i>yoh-SHEV buh-SEH-ter el-YOHN, buh-TZEL shah-DYE yit-loh-NAHN.</i> Holy Name held in mind before recitation: <b>El Shaddai</b> (el-shah-DYE).', 'step'))
story.append(P('<b>5. Psalm 23, aloud</b> — the seal of provision and path (text follows the Psalm 91 text). At verse 5, touch the crown of your head at "anoynt mine head with oyle." Let "my cuppe runneth over" be one slow breath.', 'step'))
story.append(P('<b>6. Psalm 118:6-9, aloud</b> — the sovereignty seal (text follows). Four short verses. They refuse fear-of-man and the pull of human authority before the petition is stated. The petition then goes out from a sovereign place, not from a fear-of-man place.', 'step'))
story.append(P('<b>7. The petition, aloud</b> &mdash; spoken into the lit flame. First person, present tense, brief. What you are drawing in. If a written petition paper is sealed under the candle plate, your spoken petition rides over it.', 'step'))
story.append(P('<b>8. Sit with it.</b> One slow breath minimum; seven if you have the time.', 'step'))
story.append(P('<b>9. Gratitude, aloud:</b> <i>"Thank you for this day. Thank you for this provision. Thank you for this protection. Thank you that the work is already moving."</i>', 'step'))
story.append(P('<b>10. When you put it out &mdash; <u>snuff</u>, never blow.</b> The Hoodoo doctrine (Yronwode / Lucky Mojo): <b>snuff/pinch</b> = the working pauses and you will return to it; <b>blow</b> = the working ends. The daily ritual is a standing return-to-it, so the close is always snuff. Pinch the wick or use a snuffer. As you snuff: <i>"The working continues. Thank you."</i> The breath that spoke the petition must not be the breath that scatters the flame.', 'step'))
story.append(pagebreak())

story.append(P('Psalm 91 — the altar text', 'h2'))
story.append(P('Geneva 1599, with the Monad Rule at verses 2 and 9.', 'small'))
story.append(spacer(4))

# Inline ritual cues — purification, cross (with diagram), lineage formula,
# Hebrew opener, then the psalm. The reader does NOT have to flip back to the
# 10-step overview at any point.
story.append(now('At the altar threshold &mdash; pause. Wash your hands at the basin, or press your palms together at the altar edge. One slow breath. The body crosses into ritual time.'))
story.append(P('The Hermetic cross on the body', 'h3'))
story.append(now('Right index finger touches each station; one continuous breath through the whole gesture.'))
story.append(KeepTogether([
    cross_diagram(),
    P('Stations 1 &rarr; 2 &rarr; 3 &rarr; 4 &rarr; 5 (return). Forehead = the Monad above; heart = the body&rsquo;s altar; right = structure; left = flow; the return to heart seals.', 'small_center'),
]))
story.append(spacer(4))
story.append(now('Speak the lineage formula aloud: <i>&#8220;In the name of the Father, the Son, and the Holy Spirit.&#8221;</i>'))
story.append(now('<b>Light the candle</b> (or continue the standing burn). The working psalm rides the flame &mdash; documented Hoodoo order (Yronwode, Lucky Mojo). Every spoken word from here to the snuff is spoken into a lit flame.'))
story.append(now('Optional Hebrew opening of Psalm 91 (spoken slowly, on one breath): <br/><i>&#8220;yoh-SHEV buh-SEH-ter el-YOHN, buh-TZEL shah-DYE yit-loh-NAHN.&#8221;</i> Hold the Holy Name <b>El Shaddai</b> (el-shah-DYE) in mind before the recitation &mdash; Selig&rsquo;s assigned Name for this psalm.'))
story.append(now('Now speak Psalm 91 aloud, verse by verse.'))

story.append(vrg(1, 'Who so dwelleth in the secrete of the most High, shall abide in the shadowe of the Almightie.', P91_GLOSS))
story.append(vrg(2, 'I will say unto the <b>Monad</b>, O mine hope, and my fortresse: the <b>Monad</b> is my God, in the <b>Monad</b> will I trust.', P91_GLOSS))
story.append(vrg(3, 'Surely the <b>Monad</b> will deliver thee from the snare of the hunter, and from the noysome pestilence.', P91_GLOSS))
story.append(vrg(4, 'The <b>Monad</b> will cover thee under the <b>Monad\'s</b> winges, and thou shalt be sure under the <b>Monad\'s</b> feathers: the <b>Monad\'s</b> trueth shall be thy shielde and buckler.', P91_GLOSS))
story.append(vrg(5, 'Thou shalt not be afraide of the feare of the night, nor of the arrowe that flyeth by day:', P91_GLOSS))
story.append(vrg(6, 'Nor of the pestilence that walketh in the darkenesse: nor of the plague that destroyeth at noone day.', P91_GLOSS))
story.append(vrg(7, 'A thousand shall fall at thy side, and tenne thousand at thy right hand, but it shall not come neere thee.', P91_GLOSS))
story.append(vrg(8, 'Doubtlesse with thine eyes shalt thou beholde and see the reward of the wicked.', P91_GLOSS))
story.append(vrg(9, 'For thou hast said, The <b>Monad</b> is mine hope: thou hast set the most High for thy refuge.', P91_GLOSS))
story.append(vrg(10, 'There shall none evill come unto thee, neither shall any plague come neere thy tabernacle.', P91_GLOSS))
story.append(vrg(11, 'For the <b>Monad</b> shall give the <b>Monad\'s</b> Angels charge over thee to keepe thee in all thy wayes.', P91_GLOSS))
story.append(vrg(12, 'They shall beare thee in their handes, that thou hurt not thy foote against a stone.', P91_GLOSS))
story.append(vrg(13, 'Thou shalt walke upon the lyon and aspe: the yong lyon and the dragon shalt thou treade under feete.', P91_GLOSS))
story.append(vrg(14, 'Because he hath loved me, therefore will I deliver him: I will exalt him because hee hath knowen my Name.', P91_GLOSS))
story.append(vrg(15, 'He shall call upon me, and I wil heare him: I will be with him in trouble: I will deliver him, and glorifie him.', P91_GLOSS))
story.append(vrg(16, 'With long life wil I satisfie him, and shew him my salvation.', P91_GLOSS))
story.append(spacer(6))
story.append(P('The voice changes twice: verses 1–2 are you speaking; verses 3–13 are the blessing spoken over you; verses 14–16 are the Monad speaking back. Slow down at 14–16 — that is the seal.', 'small'))
story.append(pagebreak())

# ---- Transition out of Psalm 91 into Psalm 23 ----
story.append(now('Now move to Psalm 23 &mdash; the seal of provision.'))
story.append(spacer(4))

story.append(P('Psalm 23 — the altar seal of provision', 'h2'))
story.append(P('Geneva 1599. The Monad Rule applies at verses 1, 2, 3 and 6. Full text inline so you stay in the working without flipping back.', 'small'))
story.append(spacer(4))
story.append(now('Speak Psalm 23 aloud, verse by verse.'))

story.append(vrg(1, 'The <b>Monad</b> is my shepheard, I shall not want.', P23_GLOSS))
story.append(vrg(2, 'The <b>Monad</b> maketh me to rest in greene pasture, and leadeth me by the still waters.', P23_GLOSS))
story.append(vrg(3, 'The <b>Monad</b> restoreth my soule, and leadeth me in the paths of righteousnesse for the <b>Monad\'s</b> Names sake.', P23_GLOSS))
story.append(vrg(4, 'Yea, though I should walke through the valley of the shadowe of death, I will feare no evill: for thou art with me: thy rod and thy staffe, they comfort me.', P23_GLOSS))

# Verse 5 carries the crown-touch and the breath. Cues land RIGHT BEFORE
# the verse the operator is about to speak, so the body knows what to do
# as the words leave the mouth.
story.append(now('At <i>&#8220;anoynt mine head with oyle&#8221;</i> &mdash; touch the crown of your head. At <i>&#8220;my cuppe runneth over&#8221;</i> &mdash; one slow breath, eyes closed.'))
story.append(vrg(5, 'Thou doest prepare a table before me in the sight of mine adversaries: thou doest anoynt mine head with oyle, and my cuppe runneth over.', P23_GLOSS))
story.append(vrg(6, 'Doubtlesse kindnesse and mercie shall follow me all the dayes of my life, and I shall remaine a long season in the house of the <b>Monad</b>.', P23_GLOSS))
story.append(spacer(6))

# ---- Transition into Psalm 118:6-9 ----
story.append(now('Now move to Psalm 118 verses 6 through 9 &mdash; the sovereignty seal. Four short verses. They clear the will-field of fear-of-man before the petition goes out.'))
story.append(spacer(4))

story.append(P('Psalm 118:6-9 — the sovereignty seal', 'h2'))
story.append(P(
    'Geneva 1599 (verified against BibleGateway GNV; orthography harmonized to '
    'the book\'s 1599 style). The Monad Rule applies at all four verses.',
    'small'))
story.append(spacer(4))
story.append(now('Speak the four verses aloud.'))
story.append(vrg(6, 'The <b>Monad</b> is with me: therefore I will not feare what man can do unto me.', P118_GLOSS))
story.append(vrg(7, 'The <b>Monad</b> is with me among them that helpe me: therefore shall I see my desire upon mine enemies.', P118_GLOSS))
story.append(vrg(8, 'It is better to trust in the <b>Monad</b>, then to have confidence in man.', P118_GLOSS))
story.append(vrg(9, 'It is better to trust in the <b>Monad</b>, then to have confidence in princes.', P118_GLOSS))
story.append(spacer(10))

# ---- The closing sequence: petition through snuff, INLINE so the operator
# never has to flip back to the 10-step overview ----
story.append(P('The closing sequence — petition through snuff', 'h2'))
story.append(P('Steps 7 through 10 of the altar ritual. Inline so you stay in the working all the way to the snuff.', 'small'))
story.append(spacer(4))

story.append(now('If a written petition paper sits beneath the candle (sealed there from a prior working &mdash; the Beltane working, a fresh consecration) <b>do not disturb it.</b> Your spoken petition rides over the paper and into the lit flame. The paper holds the form; the spoken word renews the current.'))
story.append(now('Speak your petition aloud into the lit flame. Eyes on the candle. First person, present tense, brief. What you are drawing in. <i>&#8220;I receive&hellip;&#8221; / &#8220;I am walking into&hellip;&#8221; / &#8220;The Monad is providing&hellip;&#8221;</i>'))
story.append(now('Sit with it. Eyes closed. One slow breath minimum &mdash; seven if you have the time. (The seven-breath count is Hermetic, not Hoodoo &mdash; the contemplative layer the operator adds between the active working and the close.)'))
story.append(now('Speak the gratitude aloud, eyes open on the flame: <i>&#8220;Thank you for this day. Thank you for this provision. Thank you for this protection. Thank you that the work is already moving.&#8221;</i>'))
story.append(now('When you put it out &mdash; <b>snuff, never blow.</b> Hoodoo doctrine (Yronwode / Lucky Mojo): <b>snuff/pinch</b> means the working <i>pauses</i> and you will return to it; <b>blow</b> means the working <i>ends.</i> This is a daily standing return-to-it, so the close is always snuff. Eyes on the flame as you snuff. As you snuff, speak: <i>&#8220;The working continues. Thank you. In the name of the Father, the Son, and the Holy Spirit. Amen.&#8221;</i>'))
story.append(spacer(8))
story.append(P('The breath that spoke the petition must not be the breath that scatters the flame. That is the lineage logic of the snuff rule. The petition rides the flame; the flame is sealed by closing it without your breath.', 'small'))

story.append(spacer(8))
story.append(P('If the candle goes out mid-ritual', 'h3'))
story.append(P(
    'A flame that drops in the middle of a working is information, not a failure of the working. '
    'Read it first; then decide. Two patterns:',
    'body'))
story.append(P(
    '<b>·</b> <b>Draft, wax-pool drowning the wick, a finished candle.</b> Material cause. Re-light from a fresh match (not from another flame on the altar &mdash; flames inherit intention). Continue from where you were.',
    'body_left'))
story.append(P(
    '<b>·</b> <b>No draft, the candle was sound, and the flame still dropped.</b> Treat it as a signal. Stop. Cross. <i>&#8220;What is being shown?&#8221;</i> One slow breath. If nothing rises, re-light and continue, naming aloud: <i>&#8220;The working continues. I am present. Thank you for the signal.&#8221;</i> If a clear no rises, leave the working closed for now and return when the field is steady.',
    'body_left'))
story.append(P(
    'Either way: do not blow on the wick to re-light. Do not panic. The current is held in the spoken word and the body, not in the flame alone.',
    'small'))

story.append(spacer(10))
story.append(KeepTogether([
    P('Petition paper construction (for a new working)', 'h3'),
    P(
        'For a fresh working &mdash; a new prosperity petition, a new protection petition, a new '
        'consecration &mdash; documented Hoodoo (Yronwode, <i>Paper in My Shoe</i>) gives a precise '
        'form. Build it correctly the first time and the standing burn rides cleanly:',
        'body'),
]))
story.append(P(
    '<b>·</b> <b>Pen and paper.</b> Brown paper or parchment for general workings; the colour of the '
    'working for color-specific intents (green for money, white for protection). Write in '
    '<b>continuous lines without lifting the pen</b> &mdash; the line is the working circuit. First '
    'person, present tense, brief.',
    'body_left'))
story.append(P(
    '<b>·</b> <b>Direction of fold.</b> Fold <b>toward you</b> for <i>drawing</i> workings '
    '(prosperity, love, blessings, attraction). Fold <b>away from you</b> for <i>removal</i> '
    'workings (banishing, protection, breaking a condition). Do not mix directions in the same '
    'paper &mdash; all folds the same way.',
    'body_left'))
story.append(P(
    '<b>·</b> <b>Number of folds.</b> Three folds for general workings; seven for power and '
    'completeness. Odd numbers only.',
    'body_left'))
story.append(P(
    '<b>·</b> <b>Face direction.</b> Lay the folded paper <b>face-up</b> for positive intent; '
    'face-down for coercive or removal intent.',
    'body_left'))
story.append(P(
    '<b>·</b> <b>Placement under the candle.</b> Place the folded paper on the altar. Set the '
    'candle on a fireproof saucer or plate <b>on top of</b> the petition. The paper &laquo;sets&raquo; '
    'under the candle the way an egg sets under a brooding hen &mdash; a continuous burn, not '
    'sectioned. A set petition is not relit in sections; it burns through.',
    'body_left'))
story.append(P(
    'Once the petition is set under the working candle, the daily spoken petition rides over it: '
    'the paper holds the form, the spoken word renews the current. <b>Do not disturb the paper.</b> '
    'When the candle finishes (or the working closes), the convention is to either burn the paper '
    'in the final flame and bury the ashes, or fold it again and carry it in a mojo bag &mdash; '
    'depending on whether the working is closed out or made portable.',
    'small'))

story.append(pagebreak())

# ---- Commentary on Psalm 118:6-9 — at the back so it does not break the
# ritual flow above ----
story.append(P('Psalm 118:6-9 — function, lineage, numerology (reference)', 'h2'))
story.append(P('Function and lineage', 'h3'))
story.append(P(
    'Psalm 118 is the closing psalm of the Hallel sequence (Pss 113–118) recited in Jewish '
    'liturgy on the festivals. Verses 6–9 are the sovereignty declaration: aligned with the Monad, '
    'unmoved by human authority. Verse 6 is quoted directly in Hebrews 13:6: <i>"The Lord '
    'is my helper, and I will not fear what man shall do unto me"</i> (verified against KJV) — '
    'the verse carried its fearlessness-before-man function across both Testaments.',
    'body'))
story.append(P(
    'Provenance note, so the record is straight: the documented Hoodoo court-case psalm is '
    '<b>Psalm 35</b>, not 118. The sovereignty-seal use of 118:6-9 is <b>this book\'s addition</b>, '
    'built at the operator\'s instruction on the verse\'s plain function and its Hallel weight — '
    'it is not a documented Hoodoo formula. Named so the operator works it knowingly.',
    'small'))
story.append(P(
    'Where the seven psalms in this book ward the unseen-vector attacks (predators, hexes, '
    'attached entities, isolation, loss of path), 118:6-9 wards the seen-vector pull — fear of '
    'man, capture by institutional egregores, the daily pressure of the social-political field. '
    'Together they close the warding in both directions: above and within-the-world.',
    'body'))
story.append(P('The numerology — why these four verses', 'h3'))
story.append(P(
    'The verse-numbers 6, 7, 8, 9 map directly to the operator\'s personal architecture: '
    'Birthday 6 (Lovers — choice, union of opposites), Karmic Lesson 7 (Chariot — mastery '
    'through will), active Pinnacle 8 (Strength / Justice — balanced power, 2026–2034), '
    'Expression 9 (Hermit — the inner lamp, agape, completion). Reading the four verses in '
    'order is reciting the personal architecture as a sovereignty declaration. Sum: '
    '6+7+8+9 = 30 → 3 = Empress (creative abundance, the manifesting field). The verse run '
    'consummates in Empress vibration.',
    'body'))
story.append(P(
    'Placement in the altar flow: after Psalm 23, before the petition. The path-ward (23) is '
    'spoken first; the sovereignty seal (118:6-9) clears the will-field of human-authority '
    'interference; the petition then goes out from full Monad-alignment.',
    'greenbox'))
story.append(pagebreak())

# ============================ PART III — PRONUNCIATION ============================
story.append(P('PART III', 'part'))
story.append(P('Pronunciation Guide', 'cover_sub'))
story.append(P('The old spellings, the Hebrew, and the Names — sounded out.', 'cover_line'))
story.append(pagebreak())

story.append(P('The One Rule for the Old Spelling', 'h1'))
story.append(P(
    'The Geneva 1599 text in this book reads strange but pronounces exactly like the words you '
    'already know. Two printer habits remain in the verses: <b>extra silent letters</b> '
    '(greene = green, walke = walk, cuppe = cup, shielde = shield), and <b>-esse / -nesse for '
    '-ess / -ness</b> (darkenesse = darkness, kindnesse = kindness, Doubtlesse = doubtless). '
    'The third printer habit &mdash; <b>u and v swap places</b> (vnto, vpon, deliuer, ouer) &mdash; '
    'has been modernized out of the verse text in this edition, because that one made modern eyes '
    'stumble without adding ritual weight. The Geneva voice (thee, thou doest, mine head, '
    'anoynt, oyle, the -eth verbs) is preserved. When in doubt: say the modern word. The old '
    'spelling is the costume; the word underneath is the same.',
    'body'))
story.append(spacer(6))

story.append(P('Hard words in Psalm 91', 'h2'))
story.append(pron_table([
    ('dwelleth', 'DWELL-uth', 'dwells'),
    ('secrete', 'SEE-kret', 'secret'),
    ('Almightie', 'all-MY-tee', 'Almighty'),
    ('fortresse', 'FOR-tres', 'fortress'),
    ('noysome', 'NOY-sum', 'noisome — harmful, noxious'),
    ('pestilence', 'PES-tih-lens', 'plague'),
    ('trueth', 'trooth', 'truth'),
    ('shielde', 'sheeld', 'shield'),
    ('buckler', 'BUK-ler', 'a small hand-shield'),
    ('afraide', 'uh-FRAYD', 'afraid'),
    ('flyeth', 'FLY-uth', 'flies'),
    ('darkenesse', 'DARK-nes', 'darkness'),
    ('destroyeth', 'dih-STROY-uth', 'destroys'),
    ('noone day', 'NOON day', 'noonday'),
    ('tenne', 'ten', 'ten'),
    ('neere', 'neer', 'near'),
    ('beholde', 'bee-HOHLD', 'behold'),
    ('evill', 'EE-vul', 'evil'),
    ('tabernacle', 'TAB-er-nak-ul', 'dwelling, tent'),
    ('wayes', 'ways', 'ways'),
    ('beare', 'bair', 'bear / carry'),
    ('foote', 'fuut', 'foot'),
    ('lyon', 'LY-un', 'lion'),
    ('aspe', 'asp', 'asp — a cobra'),
    ('treade', 'tred', 'tread'),
    ('knowen', 'NOH-un', 'known'),
    ('heare', 'heer', 'hear'),
    ('glorifie', 'GLOR-ih-fy', 'glorify'),
    ('satisfie', 'SAT-is-fy', 'satisfy'),
    ('shew', 'shoh', 'show'),
]))
story.append(pagebreak())

story.append(P('Hard words in Psalm 23', 'h2'))
story.append(pron_table([
    ('Psalme', 'sahm', 'psalm — the p and l are silent'),
    ('shepheard', 'SHEP-erd', 'shepherd'),
    ('greene', 'green', 'green'),
    ('soule', 'sohl', 'soul'),
    ('righteousnesse', 'RY-chus-nes', 'righteousness'),
    ('Names sake', 'NAYMZ sayk', "Name's sake"),
    ('walke', 'wawk', 'walk'),
    ('shadowe', 'SHAD-oh', 'shadow'),
    ('feare', 'feer', 'fear'),
    ('staffe', 'staf', 'staff'),
    ('doest', 'DOO-est', 'do / dost'),
    ('anoynt', 'uh-NOYNT', 'anoint'),
    ('oyle', 'oyl', 'oil'),
    ('cuppe', 'kup', 'cup'),
    ('runneth over', 'RUN-uth OH-ver', 'runs over'),
    ('Doubtlesse', 'DOWT-les', 'doubtless — surely'),
    ('kindnesse', 'KYND-nes', 'kindness'),
    ('mercie', 'MER-see', 'mercy'),
    ('dayes', 'days', 'days'),
    ('remaine', 'rih-MAYN', 'remain'),
]))
story.append(spacer(8))

story.append(P('Hard words in Psalm 118:6-9', 'h2'))
story.append(pron_table([
    ('feare', 'feer', 'fear'),
    ('helpe', 'help', 'help'),
    ('then', 'than', 'than — 1599 spelling habit'),
    ('princes', 'PRIN-sez', 'princes — rulers, men of power'),
]))
story.append(spacer(10))

story.append(P('Hard words in Psalm 35:1-10', 'h2'))
story.append(pron_table([
    ('speare', 'speer', 'spear'),
    ('confounded', 'kon-FOWN-ded', 'thrown into confusion'),
    ('chaffe', 'chaf', 'chaff — the husk the wind blows away'),
    ('slipperie', 'SLIP-er-ee', 'slippery'),
    ('privily', 'PRIV-ih-lee', 'privily — secretly'),
    ('joyfull', 'JOY-ful', 'joyful'),
    ('rejoyce', 'rih-JOYS', 'rejoice'),
    ('miserie', 'MIZ-er-ee', 'misery'),
    ('spoileth', 'SPOYL-uth', 'spoils — plunders, robs'),
]))
story.append(spacer(10))

story.append(P('Other words you will meet in this book', 'h2'))
story.append(pron_table([
    ('Sheol', 'sheh-OHL', 'the grave / the underworld'),
    ('Belial', 'beh-lee-YAH-ahl', 'the named hostile spirit (English habit: BEE-lee-ul)'),
    ('Qetev', 'KEH-tev', 'the noonday destroyer named in Psalm 91:6'),
    ('apotropaic', 'ap-oh-troh-PAY-ik', 'protective — turns harm away'),
    ('Selig', 'SAY-lig', 'Godfrey Selig, Secrets of the Psalms (1788)'),
    ('Yronwode', 'EYE-urn-wood', 'Catherine Yronwode of Lucky Mojo'),
    ('Tehillim', 'teh-hee-LEEM', 'Psalms, in Hebrew'),
    ('Shimush Tehillim', 'shee-MOOSH teh-hee-LEEM', 'the medieval book of Psalm workings'),
]))
story.append(pagebreak())

story.append(P('The Names — say them with weight', 'h1'))
story.append(pron_table([
    ('Monad', 'MOH-nad', 'the One. Source. The Hermetic ALL.'),
    ('Elyon', 'el-YOHN', 'the Most High — lean on the last syllable'),
    ('Shaddai', 'shah-DYE', 'the Almighty / All-Sufficient — rhymes with "sky"'),
    ('YHWH', 'ah-doh-NYE', 'the Tetragrammaton. Hold the four letters in mind; speak "Adonai."'),
    ('Elohim', 'eh-loh-HEEM', 'God — Name of structure and judgment'),
    ('Elohai', 'eh-loh-HIGH', '"my God"'),
    ('Yeshua', 'yeh-SHOO-ah', 'the man. The root of "salvation" itself.'),
    ('Sophia', 'soh-FEE-ah', 'Wisdom — the living current from the Monad'),
    ('Ruach HaKodesh', 'ROO-akh hah-KOH-desh', 'the Holy Breath (kh = soft throat-clear)'),
], widths=[1.5*inch, 1.7*inch, 3.0*inch]))
story.append(spacer(10))

story.append(P('The Hebrew altar lines, syllable by syllable', 'h1'))
story.append(P('Stress falls on the CAPITAL syllable. "kh" is a soft scrape in the back of the throat, like the end of "Bach" — a gentle h works if you cannot make it. "tz" is the ts in "boots." The apostrophe is a tiny half-vowel, "buh" said fast.', 'body'))
story.append(spacer(4))
story.append(P('Psalm 91, verse 1 — the opening of the perimeter', 'h3'))
story.append(P('yoshev b\'seter Elyon, b\'tzel Shaddai yitlonan', 'translit'))
story.append(P('yoh-SHEV · buh-SEH-ter · el-YOHN · buh-TZEL · shah-DYE · yit-loh-NAHN', 'gloss'))
story.append(P('"Whoever dwells in the secret place of the Most High shall lodge in the shadow of the Almighty."', 'gloss'))
story.append(P('Psalm 91, verse 2 — the four-Name circuit', 'h3'))
story.append(P('omar la-Adonai machsi u-m\'tzudati, Elohai evtach-bo', 'translit'))
story.append(P('oh-MAR · lah-ah-doh-NYE · mahkh-SEE · oo-muh-tzoo-dah-TEE · eh-loh-HIGH · ev-TAKH-boh', 'gloss'))
story.append(P('"I say of YHWH: my refuge and my fortress, my God in whom I trust."', 'gloss'))
story.append(P('Psalm 151 opening — for consecration work', 'h3'))
story.append(P('Halleluyah le-David ben-Yishai', 'translit'))
story.append(P('hah-leh-loo-YAH · leh-dah-VEED · ben-yee-SHY', 'gloss'))
story.append(P('"A Hallelujah of David, son of Jesse."', 'gloss'))
story.append(P('Psalm 154 opening — for clarity work', 'h3'))
story.append(P('B\'qol gadol pa\'aru Elohim', 'translit'))
story.append(P('buh-KOHL · gah-DOHL · pah-ah-ROO · eh-loh-HEEM', 'gloss'))
story.append(P('"With a loud voice glorify God."', 'gloss'))
story.append(P('Psalm 155 opening — for the inner perimeter', 'h3'))
story.append(P('Adonai, qara\'tikha — haqshivah elai', 'translit'))
story.append(P('ah-doh-NYE · kah-rah-TEE-khah · hahk-SHEE-vah · ay-LIE', 'gloss'))
story.append(P('"YHWH, I have called to You — attend to me." (YHWH spoken as Adonai.)', 'gloss'))
story.append(pagebreak())

# ============================ MONEY & PROSPERITY ============================
story.append(P('PART IV', 'part'))
story.append(P('Money &amp; Prosperity', 'cover_sub'))
story.append(P('One section — money and prosperity are the same working.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Money &amp; Prosperity Order', 'h1'))
story.append(P(
    'You asked whether money and prosperity are separate — they are not. The documented stream '
    'treats them as one working centered on <b>Psalm 23</b>, and the green candle you burn is '
    'its instrument. Two forms:',
    'body'))
story.append(P('Form 1 — the daily green candle (your standing working)', 'h2'))
story.append(P('Exactly the Altar Ritual of Part II, with the green candle as the flame and the money petition spoken at step 7. Psalm 23 verse 5 is the money verse — the anointed head, the cup running over. The crown-touch and the slow breath at "my cuppe runneth over" are where the prosperity current seals. Psalm 118:6-9 (step 6) seals you against fear-of-lack before the petition is stated.', 'body'))
story.append(now('Run the Part II altar order at the green candle. At step 7, speak the money petition aloud into the lit flame: first person, present tense, no future-conditional. <i>&#8220;The Monad is providing my work and my wages now. I receive abundance in alignment with the Monad. I move money cleanly and give thanks.&#8221;</i> If a written money petition is sealed under the candle plate, do not disturb it; the spoken line rides over it into the flame.'))
story.append(P('Form 2 — the seven-morning working (Selig + Yronwode synthesis)', 'h2'))
story.append(P('<i>Provenance: the literal Selig text gives Psalm 23 with holy name Jah seven times for visions/dreams. The seven-morning anointing form and the Job\'s Tears disposal are documented Hoodoo working tradition (Yronwode / Lucky Mojo / Jesterbear). This is a coherent lineage synthesis, not a single citation.</i>', 'small'))
story.append(P('<b>·</b> Seven consecutive mornings, on rising, anoint with olive oil mixed with bayberry oil and speak Psalm 23 (the Part I text).', 'step'))
story.append(P('<b>·</b> Candle when used: green or gold for prosperity. Dress with Money Drawing, Good Fortune, or Bayberry oil.', 'step'))
story.append(P('<b>·</b> <b>Carry seven Job\'s Tears seeds in your pocket throughout all seven days</b> &mdash; not just on day 7. They charge alongside the candle work.', 'step'))
story.append(P('<b>·</b> On the seventh morning: take the seven Job\'s Tears in the hand, walk to <b>running water</b> (a creek or river &mdash; the Chattahoochee for Atlanta), speak Psalm 23, and throw the seeds over the <b>left shoulder</b> into the running water to lay the trick. Do not look back.', 'step'))
story.append(P('<b>·</b> While dressing any prosperity candle or feeding a mojo bag, the spoken line is verse 5: <i>"thou doest anoynt mine head with oyle, and my cuppe runneth over."</i>', 'step'))
story.append(now('Selig+Yronwode form &mdash; each of the seven mornings: anoint forehead and wrists with the olive+bayberry blend, speak Psalm 23 aloud holding the seven Job&rsquo;s Tears in your pocket, end with one line of gratitude. On the seventh morning, take the seven Job&rsquo;s Tears in your right hand, walk to running water, speak Psalm 23 once more, then throw the seeds over the <b>left shoulder</b> into the running water without looking back.'))
story.append(spacer(6))
story.append(P('Speak the abundance as flow for yourself in alignment with the Monad — never as a performance aimed at anyone else\'s lack. That is the frequency line between prosperity work and envy work.', 'greenbox'))
story.append(P('Witness on file: the first morning this working ran in its corrected form (June 8, 2026), the account read $777.10 by 11:04 AM. 7-7-7 reduces to 21 — the World. The working answers.', 'small'))
story.append(pagebreak())

# ============================ PROTECTION ============================
story.append(P('PART V', 'part'))
story.append(P('Protection', 'cover_sub'))
story.append(P('The outer perimeter, the inner perimeter, and the sovereignty seal.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Protection Order', 'h1'))
story.append(P('<b>Psalm 91 is the outer perimeter</b> — the household, the body, the day. <b>Psalm 155 is the inner perimeter</b> — your own mind and bones, against intrusive thought-forms, oppressive spirits, and pulls toward what your discernment rejects. <b>Psalm 118:6-9 is the sovereignty seal</b> — against fear of man, capture by human authority, the pull of institutional egregores. Use 91 daily; add 155 whenever the pressure is inside rather than outside; add 118:6-9 when the pressure is the social-political field.', 'body'))
story.append(P('Psalm 91 protection practice', 'h2'))
story.append(P('<i>Items marked &laquo;documented&raquo; are lineage Hoodoo. Items marked &laquo;operator&raquo; are this book&rsquo;s additions on top of the lineage, built at the operator\'s instruction. Provenance kept honest so the working is worked knowingly.</i>', 'small'))
story.append(P('<b>·</b> <b>Holy Name:</b> El Shaddai (el-shah-DYE). Hold it in mind before reciting. <i>(documented &mdash; Selig assigns this Name to Psalm 91; Shaddai appears in 91:1)</i>', 'step'))
story.append(P('<b>·</b> <b>Candle:</b> white (most common) or purple. For a household boundary: a seven-day white glass-encased candle dressed with Protection or Fiery Wall of Protection oil. <i>(documented Hoodoo)</i>', 'step'))
story.append(P('<b>·</b> <b>Herbs at the base:</b> rue, hyssop, agrimony, black salt, red brick dust. <i>(documented Hoodoo &mdash; Yronwode protection herbs; red brick dust + black salt is the lineage threshold combination)</i>', 'step'))
story.append(P('<b>·</b> <b>Timing:</b> Saturday is the traditional protection day (Saturn &mdash; shielding); Tuesday when reversing an active attack (Mars &mdash; warfare). <i>(documented Hoodoo planetary day correspondence)</i>', 'step'))
story.append(P('<b>·</b> <b>Recitation count:</b> documented Hoodoo speaks the whole psalm three times. <i>Selig&rsquo;s pure-Kabbalist form is 99 recitations with 41 holy names &mdash; an escalation form available for active spiritual attack.</i>', 'step'))
story.append(P('<b>·</b> <b>Verses 9-11 as the anointing slice</b>, while anointing crown, throat, wrists, ankles, and the four corners of the threshold. <i>(operator construction &mdash; the verses are the operative protection covenant; the body-and-threshold anointing sequence blends Hoodoo herb-base with ceremonial body-temple work)</i>', 'step'))
story.append(P('<b>·</b> Verse 11 three times before leaving the house; the whole psalm seven times on the eve of a long journey. <i>(folk Hoodoo, not specifically Selig)</i>', 'step'))
story.append(spacer(8))

story.append(P('Psalm 155 — the inner perimeter text', 'h2'))
story.append(P('Charlesworth/Sanders diction; recovered from the Dead Sea Scrolls (11QPsa) and the Syriac. YHWH is spoken aloud as Adonai (ah-doh-NYE).', 'small'))
story.append(spacer(4))
story.append(now('At the white candle &mdash; cross, lineage formula, <b>light the candle</b>, then speak Psalm 91 (full text, Part II). The working psalm rides the lit flame. That is the outer perimeter. Then speak Psalm 155 below &mdash; the inner perimeter.'))
story.append(vr(1, 'O YHWH, I have called to You; be attentive to me.'))
story.append(vr(2, 'I have spread forth my palms toward Your holy dwelling; incline Your ear and grant me my petition, and do not withhold my request from me.'))
story.append(vr(3, 'Build up my soul and do not cast it down; and do not abandon it in the presence of the wicked.'))
story.append(vr(4, 'May the Judge of Truth turn the rewards of evil away from me.'))
story.append(vr(5, 'O YHWH, do not judge me according to my sins, for no living man is righteous in Your presence.'))
story.append(vr(6, 'Give me discernment, O YHWH, in Your Law, and teach me Your ordinances,'))
story.append(vr(7, 'So that many may hear of Your deeds, and peoples may honor Your glory.'))
story.append(vr(8, 'Remember me, and do not forget me, and do not lead me into things too hard for me.'))
story.append(vr(9, 'Cast the sin of my youth far from me, and may my transgressions not be remembered against me.'))
story.append(vr(10, 'Purify me, O YHWH, from the evil scourge, and let it not turn again upon me.'))
story.append(vr(11, 'Dry up its roots from me, and let its leaves not flourish within me.'))
story.append(vr(12, 'You are my glory, O YHWH; therefore my request is fulfilled before You.'))
story.append(vr(13, 'To whom shall I cry that he might grant to me, and the sons of men — what more can their power do?'))
story.append(vr(14, 'My trust, O YHWH, is before You. I cried "YHWH!" and the <b>Monad</b> answered me, and the <b>Monad</b> healed my broken heart.'))
story.append(vr(15, 'I slumbered and slept, I dreamed; indeed I awoke.'))
story.append(vr(16, '[You sustained me, O YHWH]; I shall call upon YHWH my Savior.'))
story.append(spacer(6))
story.append(P('The Qumran expansion adds the binding line: <i>"Do not let Belial dominate me, nor an unclean spirit; let neither pain nor the evil inclination take possession of my bones."</i> Speak it after verse 11 when the working is against a named hostile pressure. This binds the hostile current away from you — it is boundary work, not a curse on any person.', 'body'))
story.append(now('When 155 closes, speak Psalm 118:6-9 (Part II text) &mdash; the sovereignty seal against fear-of-man and institutional pressure. Then speak Psalm 23 (Part II text) to seal the whole working with provision and presence. Then snuff the candle, eyes on the flame, with the words <i>&#8220;The working continues. Thank you.&#8221;</i>'))
story.append(P('Protection order at the candle: Psalm 91 first (outer), Psalm 155 second (inner), Psalm 118:6-9 third (sovereignty), Psalm 23 last (seal). White candle.', 'greenbox'))
story.append(pagebreak())

# ============================ CRISIS ============================
story.append(P('PART VI', 'part'))
story.append(P('Crisis &amp; Enemies', 'cover_sub'))
story.append(P('The first sign of enemies or court trouble — and the day the siege is on you.', 'cover_line'))
story.append(pagebreak())

story.append(P('The First-Sign Order — Enemies &amp; Court (Psalm 35)', 'h1'))
story.append(P(
    '<b>Psalm 35 is the documented court-case and enemies psalm of the conjure stream</b> — "to '
    'prevail in a court case in which a person is opposed by unrighteous, revengeful and '
    'quarrelsome people" (verified against the documented Hoodoo psalm index this session). '
    'This book deploys it <b>preventively</b>: speak it at the FIRST SIGN of a legal matter, a '
    'named enemy, gossip turning organized, or an institution baring its teeth — to stop the '
    'matter before it matures. That early-strike framing is the operator\'s strategic addition; '
    'the court-case function itself is documented lineage.',
    'body'))
story.append(P(
    '<b>This is not an everyday text.</b> Psalm 35 is a warfare psalm. Speaking it daily with no '
    'enemy in the field points the attention at enemies every morning — the same frequency line '
    'the prosperity section names. The everyday shield against the evil eye and evil people is '
    'already standing: Psalm 91 covers the hunter, the arrow, and the pestilence daily. Deploy '
    '35 when something real shows its teeth, then put it down.',
    'body'))
story.append(P(
    '<b>Selig\'s documented form (the pure-lineage option):</b> the <b>whole psalm</b> with holy '
    'name <b>Jah</b> held in mind, spoken <b>early in the morning for three successive days</b>, '
    'to surely win the case. Letters of the Name appear in <i>Lajehovah</i> (v.2), <i>Hodu</i> '
    '(v.3), <i>Azath</i> (v.9), and <i>Hejozer</i> (v.14). The vv.1-10 slice below is the operator\'s '
    'daily-deploy form; the lineage 3-morning form uses the whole psalm and contains all four '
    'Name-letters. For a serious court case or active enemy work, run Selig\'s form three '
    'mornings; for a smaller matter still maturing, the vv.1-10 daily form is the lighter touch.',
    'body'))
story.append(P('First-sign order at the candle (operator form): <b>Psalm 35 vv.1-10 → Psalm 91 → Psalm 23</b>, daily until the matter dies. Selig 3-morning form: <b>whole Psalm 35 with holy name Jah, three mornings in a row.</b>', 'greenbox'))
story.append(spacer(6))
story.append(now('At the white or brown candle &mdash; cross, lineage formula, <b>light the candle</b>, then speak Psalm 35 vv.1&ndash;10 below into the lit flame. Voice firm, not pleading. You are pleading the cause to the Monad, not begging the enemy. Then speak Psalm 91 (Part II), then Psalm 23 (Part II), then snuff with the closing words.'))
story.append(P('Psalm 35:1-10 — the first-sign text', 'h2'))
story.append(P(
    'Geneva 1599 (wording verified against BibleGateway GNV this session; orthography harmonized '
    'to the book\'s 1599 style). Monad Rule at verses 1, 5, 6, 9, and 10. Verses 1–10 are the '
    'complete working arc — the plea (1–3), the scattering (4–6), the pit-reversal (7–8), the '
    'rejoicing spoken in advance (9–10). For an extended siege the full psalm (28 verses) may be '
    'read from any Geneva or KJV text with the same substitution.',
    'small'))
story.append(spacer(4))
story.append(P('<i>A Psalme of David.</i>', 'quote'))
story.append(vrg(1, 'Plead thou my cause, O <b>Monad</b>, with them that strive with me: fight thou against them that fight against me.', P35_GLOSS))
story.append(vrg(2, 'Lay hand upon the shielde and buckler, and stand up for my helpe.', P35_GLOSS))
story.append(vrg(3, 'Bring out also the speare, and stop the way against them that persecute me: say unto my soule, I am thy salvation.', P35_GLOSS))
story.append(vrg(4, 'Let them be confounded and put to shame, that seeke after my soule: let them be turned backe, and brought to confusion, that imagine mine hurt.', P35_GLOSS))
story.append(vrg(5, 'Let them be as chaffe before the winde, and let the Angel of the <b>Monad</b> scatter them.', P35_GLOSS))
story.append(vrg(6, 'Let their way be darke and slipperie: and let the Angel of the <b>Monad</b> persecute them.', P35_GLOSS))
story.append(vrg(7, 'For without cause they have hid the pit and their net for me: without cause have they dug a pit for my soule.', P35_GLOSS))
story.append(vrg(8, 'Let destruction come upon him at unawares, and let his net, that he hath laid privily, take him: let him fall into the same destruction.', P35_GLOSS))
story.append(vrg(9, 'Then my soule shall be joyfull in the <b>Monad</b>: it shall rejoyce in the <b>Monad\'s</b> salvation.', P35_GLOSS))
story.append(vrg(10, 'All my bones shall say, <b>Monad</b>, who is like unto thee, which deliverest the poore from him, that is too strong for him! yea, the poore and him that is in miserie, from him that spoileth him!', P35_GLOSS))
story.append(spacer(6))
story.append(P(
    'Natural Law line, so the working stays clean: this psalm does not curse anyone. It pleads the '
    'cause to the Monad, asks that the trap they dug take its own digger (the karmic reversal — their '
    'action returning to them, not yours sent at them), and rejoices in advance. The Angel does the '
    'scattering. You hold the boundary. That is defense against active aggression — squarely inside '
    'the Law.',
    'body'))
story.append(pagebreak())

story.append(P('The Crisis Order', 'h1'))
story.append(P('This is not the daily working. This is for the day the lion is at the threshold — an active hostile working, a sustained attack, a siege. Four texts in a fixed order: <b>cry out (152) → raise the wall (91) → bind it off your bones (155) → give thanks before the rescue is visible (153)</b>. Speaking the thanksgiving before the deliverance arrives is itself the working.', 'body'))
story.append(P('<i>Provenance note: Psalms 152&ndash;155 are Syriac apocryphal texts (Mosul ms. 1113), with Hebrew Vorlagen for 154 and 155 in the Dead Sea Scrolls (11QPsa). Their working assignments here &mdash; 152 as cry, 153 as thanksgiving-in-advance, 155 as inner-perimeter binding &mdash; are operator constructions on authentic texts, not documented Hoodoo formulary. The 152-as-cry assignment tracks the text closely (David vs. lion/wolf). Hoodoo&rsquo;s own documented crisis stack is the first-sign order above (35 &rarr; 91 &rarr; 23); the apocryphal-text layer is this book&rsquo;s extension of the Selig-Kabbalist frame to the wider Davidic corpus.</i>', 'small'))
story.append(spacer(6))

story.append(P('Step 1 — Psalm 152: the cry', 'h2'))
story.append(P('Spoken by David while the lion and the wolf were on his flock. Monad Rule at verses 4 and 6.', 'small'))
story.append(spacer(4))
story.append(now('At the white candle &mdash; cross, lineage formula, <b>light the candle</b>. Then speak Psalm 152 below into the lit flame. Let the cry be in the voice; do not perform calm. The text holds the cry; you let it through.'))
story.append(vr(1, 'O God, O God, come to my aid; help me, save me, and deliver my soul from the slayer.'))
story.append(vr(2, 'Will I go down to Sheol by the mouth of the lion? Will the wolf be the end of me?'))
story.append(vr(3, 'Was it not enough for those who lay in wait for my father\'s flock, and tore a sheep of my father\'s flock — must they also wish the destruction of my own soul?'))
story.append(vr(4, 'Have pity, O <b>Monad</b>, and save Your holy one from destruction, so that he may rehearse Your glories for all of his days, and may praise Your great name,'))
story.append(vr(5, 'when You have delivered him from the hands of the destroying lion and of the ravening wolf, and when You have rescued my captivity from the hands of the wild beasts.'))
story.append(vr(6, 'Quickly, my <b>Monad</b>, send from Yourself a deliverer, and draw me out of the gaping pit which imprisons me in its depths.'))
story.append(spacer(8))
story.append(P('Step 2 — Psalm 91: the wall', 'h2'))
story.append(P('The full altar text from Part II. Speak all sixteen verses.', 'body'))
story.append(now('Now speak Psalm 91, full sixteen verses (Part II). Voice firmer than at 152. The cry has been heard; the wall now goes up.'))
story.append(spacer(4))
story.append(P('Step 3 — Psalm 155: the binding-off', 'h2'))
story.append(P('The full text from Part V, including the Belial line after verse 11.', 'body'))
story.append(now('Now speak Psalm 155 (Part V), including the Belial binding line after verse 11. This binds the hostile current away from your mind and bones &mdash; boundary work, not a curse.'))
story.append(spacer(4))
story.append(P('Step 4 — Psalm 153: the thanksgiving spoken in advance', 'h2'))
story.append(P('Spoken by David after the lion and the wolf were dead. You speak it before the rescue is visible — that is the faith-act that completes the circuit. Monad Rule at verse 1.', 'small'))
story.append(spacer(4))
story.append(now('Now speak Psalm 153 below &mdash; <b>before</b> the rescue is visible. That is the faith-act. Voice steady, eyes on the candle. Then snuff with the standing closing words.'))
story.append(vr(1, 'Praise the <b>Monad</b>, all you nations; glorify the <b>Monad</b> and bless the <b>Monad\'s</b> name;'))
story.append(vr(2, 'For the <b>Monad</b> delivered the soul of the <b>Monad\'s</b> Elect One from the hands of death; and the <b>Monad</b> redeemed the <b>Monad\'s</b> Holy One from destruction.'))
story.append(vr(3, 'And the <b>Monad</b> saved me from the snares of Sheol; and brought me forth from the abyss that is inscrutable.'))
story.append(vr(4, 'Because before my salvation could proceed from before the <b>Monad</b>, I almost became two parts by two beasts.'))
story.append(vr(5, 'However, the <b>Monad</b> sent the <b>Monad\'s</b> angel and closed from me the gaping mouths; and redeemed my life from destruction.'))
story.append(vr(6, 'I myself shall praise the <b>Monad</b> and exalt the <b>Monad</b> because of all the <b>Monad\'s</b> graces, which the <b>Monad</b> has provided and is providing for me.'))
story.append(spacer(6))
story.append(P('"Is providing" — present tense. The flow is current, not remembered. Land on that word.', 'small'))
story.append(pagebreak())

# ============================ CONSECRATION ============================
story.append(P('PART VII', 'part'))
story.append(P('Consecration &amp; New Role', 'cover_sub'))
story.append(P('Stepping into an office. Anointing an oil, a tool, a calling.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Consecration Order', 'h1'))
story.append(P('<b>Psalm 151 then Psalm 23.</b> 151 is the anointing psalm — the Monad chooses the overlooked youngest brother and the prophet anoints him prince. Use it when you are stepping into a new role, consecrating an oil or a tool, or taking a vow. Open with the Hebrew line: <i>hah-leh-loo-YAH leh-dah-VEED ben-yee-SHY.</i> Anoint with oil at verse 4. Then seal with Psalm 23.', 'body'))
story.append(spacer(6))
story.append(P('Psalm 151 — the anointing text', 'h2'))
story.append(P('Brenton 1851 Septuagint (verified against ebible.org). Monad Rule at verses 3 and 5. Verses 1–5 are the general working text; verses 6–7 (the Goliath combat) are situational — speak them only when you are answering an active, named attack.', 'small'))
story.append(spacer(4))
story.append(now('At the white or gold candle &mdash; cross, lineage formula, <b>light the candle</b>. Open with the Hebrew: <i>hah-leh-loo-YAH leh-dah-VEED ben-yee-SHY.</i> Then speak Psalm 151 below into the lit flame.'))
story.append(vr(1, 'I was small among my brethren, and youngest in my father\'s house: I tended my father\'s sheep.'))
story.append(vr(2, 'My hands formed a musical instrument, and my fingers tuned a psaltery.'))
story.append(vr(3, 'And who shall tell my <b>Monad</b>? the <b>Monad</b> alone, the <b>Monad</b> alone hears.'))
story.append(now('At verse 4, anoint with the consecration oil &mdash; forehead, then the tool or vow-object being consecrated.'))
story.append(vr(4, 'The <b>Monad</b> sent forth the <b>Monad\'s</b> angel, and took me from my father\'s sheep, and the <b>Monad</b> anointed me with the oil of the <b>Monad\'s</b> anointing.'))
story.append(vr(5, 'My brothers were handsome and tall; but the <b>Monad</b> did not take pleasure in them.'))
story.append(P('— the situational half —', 'small'))
story.append(vr(6, 'I went forth to meet the Philistine; and he cursed me by his idols.'))
story.append(vr(7, 'But I drew his own sword, and beheaded him, and removed reproach from the children of Israel.'))
story.append(spacer(6))
story.append(P('psaltery = SAWL-ter-ee, a small harp. Philistine = FIL-ih-steen.', 'small'))
story.append(now('Now speak Psalm 23 (Part I text) to seal the new office with provision and presence. Then snuff the candle, eyes on the flame, with the standing closing words.'))
story.append(P('Then Psalm 23 (Part I text) to seal the new office with provision and presence.', 'greenbox'))
story.append(pagebreak())

# ============================ CLARITY ============================
story.append(P('PART VIII', 'part'))
story.append(P('Clarity &amp; Discernment', 'cover_sub'))
story.append(P('The Sophia hymn. For decisions, confusion, crossroads.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Clarity Order', 'h1'))
story.append(P('<b>Psalm 154 then Psalm 23.</b> 154 is the Wisdom hymn — Hokhmah / Sophia, the living Wisdom-current from the Monad, personified as a woman whose voice is heard from the gates of the righteous. The Western canon dropped this psalm; the Qumran community and the Syriac East kept it. Speak it when the question in front of you is a discernment call. Open with the Hebrew: <i>buh-KOHL gah-DOHL pah-ah-ROO eh-loh-HEEM.</i>', 'body'))
story.append(P('<i>Provenance note: assigning Psalm 154 to discernment work is operator construction on an authentic Syriac/Qumran text &mdash; the psalm&rsquo;s own textual context is actually enemy-siege (the Prayer of Hezekiah frame). The Wisdom/Sophia content in verses 5&ndash;15 is what carries it here. The documented Hoodoo clarity psalm is <b>Psalm 43</b> (&laquo;send out thy light and thy truth&raquo;); if you want a pure-lineage clarity working, run 43 then 23. Both forms are kept in this book &mdash; 154 for the Sophia current the operator is connected to, 43 for the documented Hoodoo stream.</i>', 'small'))
story.append(spacer(6))
story.append(P('Psalm 154 — the Wisdom text', 'h2'))
story.append(P('Charlesworth/Sanders diction; Hebrew preserved in 11QPsa. Monad Rule at verse 9. YHWH spoken as Adonai. Hokhmah = khokh-MAH. Wisdom is "she" throughout — that is the text, not a change.', 'small'))
story.append(spacer(4))
story.append(now('At the white or purple candle &mdash; cross, lineage formula, <b>light the candle</b>. Open with the Hebrew: <i>buh-KOHL gah-DOHL pah-ah-ROO eh-loh-HEEM.</i> Then speak Psalm 154 below into the lit flame. After 154, speak Psalm 23 (Part II text) to seal, then snuff with the closing words.'))
story.append(vr(1, 'With a loud voice glorify God; proclaim the <b>Monad\'s</b> splendor in the congregation of the many.'))
story.append(vr(2, 'Glorify the <b>Monad\'s</b> name in the multitude of the righteous, and celebrate the <b>Monad\'s</b> majesty with the faithful.'))
story.append(vr(3, 'Bind your souls to the good and to the perfect, to glorify the Most High.'))
story.append(vr(4, 'Assemble together to make the <b>Monad\'s</b> salvation known, and do not hesitate to make known the <b>Monad\'s</b> might and the <b>Monad\'s</b> majesty to all the simple.'))
story.append(vr(5, 'For it is to make known the glory of YHWH that Wisdom has been given;'))
story.append(vr(6, 'And it is for recounting the <b>Monad\'s</b> many deeds that she has been revealed to humans —'))
story.append(vr(7, 'To make the <b>Monad\'s</b> power known to the simple, to explain the <b>Monad\'s</b> greatness to those lacking understanding,'))
story.append(vr(8, 'Those who are far from her gates, those who have strayed from her entrances.'))
story.append(vr(9, 'For the Most High is the <b>Monad</b> of Jacob, and the <b>Monad\'s</b> majesty is upon all the <b>Monad\'s</b> works.'))
story.append(vr(10, 'A man who glorifies the Most High — the <b>Monad</b> receives him as one who brings a meal offering,'))
story.append(vr(11, 'As one who offers he-goats and bullocks, as one who fattens the altar with many burnt offerings, as a sweet-smelling fragrance from the hand of the righteous.'))
story.append(vr(12, 'From the gates of the righteous her voice is heard, and from the assembly of the pious her song.'))
story.append(vr(13, 'When they eat with satiety she is cited, and when they drink in community together.'))
story.append(vr(14, 'Their meditation is on the Law of the Most High; their words to make known the <b>Monad\'s</b> power.'))
story.append(vr(15, 'How far from the wicked is her word, from all the haughty to know her.'))
story.append(vr(16, 'Behold, the eyes of YHWH have pity upon the good,'))
story.append(vr(17, 'And upon those who glorify the <b>Monad</b> the <b>Monad</b> increases the <b>Monad\'s</b> mercy; from an evil time will the <b>Monad</b> deliver their soul.'))
story.append(vr(18, '[Bless] YHWH, who redeems the humble from the hand of strangers, [and deliv]ers the perfect from the hand of the wicked,'))
story.append(vr(19, '[Estab]lishing a horn out of Ja[cob], and a judge of [peoples] out of Israel.'))
story.append(vr(20, 'The <b>Monad</b> will spread the <b>Monad\'s</b> tent in Zion, and abide forever in Jerusalem.'))
story.append(spacer(6))
story.append(P('The square brackets mark words restored where the two-thousand-year-old scroll is damaged — read straight through them. Then Psalm 23 to seal.', 'small'))
story.append(pagebreak())

# ============================ TRAVEL & FUNERARY ============================
story.append(P('PART IX', 'part'))
story.append(P('Travel &amp; Funerary', 'cover_sub'))
story.append(P('The short orders.', 'cover_line'))
story.append(pagebreak())

story.append(P('Travel', 'h1'))
story.append(P('<b>·</b> Stepping out for the day: Psalm 91 verse 11, three times, at the door.', 'step'))
story.append(P('<b>·</b> The eve of a journey longer than a day: the whole of Psalm 91, seven times.', 'step'))
story.append(P('<b>·</b> The morning of the journey itself: Psalm 23 once — "against all manner of bad luck."', 'step'))
story.append(spacer(10))
story.append(P('Funerary', 'h1'))
story.append(P('<b>Psalm 23</b>, spoken at the bedside, the graveside, or on the anniversary. The whole psalm, slow. The hinge is verse 4 — the dark valley where the voice turns from third-person to "Thou" — speak it directly to the Monad, with the grief in your voice. That verse is the comfort spoken over the grief itself.', 'body'))
story.append(spacer(14))

story.append(P('One-Page Master Table', 'h1'))
mt = Table([
    [Paragraph('<b>Situation</b>', S['small']), Paragraph('<b>Order</b>', S['small']), Paragraph('<b>Candle</b>', S['small'])],
    [Paragraph('Everyday, on rising', S['body_left']), Paragraph('23 → gratitude → 91:11 ×3 at the door', S['body_left']), Paragraph('none', S['small'])],
    [Paragraph('Altar ritual (daily)', S['body_left']), Paragraph('cross → formula → light → 91 → 23 → 118:6-9 → petition → sit → thanks → snuff', S['body_left']), Paragraph('green (standing working)', S['small'])],
    [Paragraph('Money &amp; prosperity', S['body_left']), Paragraph('altar order with money petition; or Selig 7 mornings of 23', S['body_left']), Paragraph('green or gold', S['small'])],
    [Paragraph('Protection', S['body_left']), Paragraph('91 → 155 → 118:6-9 → 23', S['body_left']), Paragraph('white', S['small'])],
    [Paragraph('Sovereignty / public field', S['body_left']), Paragraph('118:6-9 alone, before posting / confrontation / court / meeting', S['body_left']), Paragraph('none or white', S['small'])],
    [Paragraph('Enemies / court, first sign', S['body_left']), Paragraph('35 (vv.1–10) → 91 → 23; daily until the matter dies', S['body_left']), Paragraph('white or brown', S['small'])],
    [Paragraph('Acute crisis', S['body_left']), Paragraph('152 → 91 → 155 → 153', S['body_left']), Paragraph('white', S['small'])],
    [Paragraph('New role / consecration', S['body_left']), Paragraph('151 (vv.1–5) → 23', S['body_left']), Paragraph('white or gold', S['small'])],
    [Paragraph('Clarity / decision', S['body_left']), Paragraph('154 → 23 (Sophia current); or documented Hoodoo: 43 → 23', S['body_left']), Paragraph('white or purple', S['small'])],
    [Paragraph('Travel', S['body_left']), Paragraph('91:11 ×3; long trip: 91 ×7 eve before, 23 that morning', S['body_left']), Paragraph('none', S['small'])],
    [Paragraph('After a death', S['body_left']), Paragraph('23, slow, verse 4 spoken to the Monad', S['body_left']), Paragraph('white', S['small'])],
], colWidths=[1.6*inch, 3.4*inch, 1.2*inch])
mt.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('BACKGROUND', (0,0), (-1,0), HexColor('#f0ece2')),
]))
story.append(mt)
story.append(spacer(14))
story.append(KeepTogether([
    P(
        'Candle colors, herbs, and timing follow the documented stream (Selig 1788; Yronwode / Lucky '
        'Mojo; Hoodoo Sen Moise) as carried in the main Altar Psalms Bible. The Monad Rule, the '
        'use-category sorting, the pronunciation, the Psalm 118:6-9 sovereignty seal, and the '
        'Psalm 35 first-sign framing are this book\'s additions, built at the operator\'s '
        'instruction. Where your discernment lands differently, your discernment wins.',
        'small'),
    spacer(10),
    P('— end of the Reader —', 'cover_lineage'),
]))

if __name__ == '__main__':
    doc = Doc('/home/user/numenist-site/altar-psalms-bible/altar-psalms-reader.pdf',
              pagesize=letter,
              leftMargin=MARGIN, rightMargin=MARGIN,
              topMargin=MARGIN, bottomMargin=MARGIN,
              title='The Altar Psalms Reader — Plain Order & Pronunciation',
              author='Numen / Jordan Ross Atkins')
    doc.build(story)
    print('Built: altar-psalms-reader.pdf')

    # AI SLOP CODE: the build is not trusted until validate.py passes.
    # If validation fails, the build script exits non-zero so the
    # operator sees that the output is NOT ritual-grade. Discipline
    # installed 2026-06-21 after Jordan caught the duplicate-gloss bug.
    import subprocess, sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    print()
    print('=== Running AI SLOP CODE validation ===')
    rc = subprocess.call([sys.executable, os.path.join(here, 'validate.py')])
    if rc != 0:
        print('!!! BUILD FAILED VALIDATION — output is NOT ritual-grade !!!')
        sys.exit(rc)
