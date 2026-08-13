"""
Altar Psalms — Working Integration (Companion Document)
=======================================================

Verse-by-verse integration of the seven Altar Psalms (23, 91, 151, 152, 153,
154, 155) with the inherited Hoodoo / Selig / Sefer Shimush Tehillim working
tradition already documented in the main Altar Psalms Bible — passed through
the Monad-frequency filter so the operator can audit what's lineage-faithful
and Monad-aligned vs. what carries low-frequency residue (saturnian /
tribal-Yahweh / coercive / imprecatory) that should be flagged before use.

Layer labels used throughout (so the reader audits by layer of confidence):
  [TEXT]    — verifiable text traceable to a primary-source translation
              (Geneva 1599, Brenton 1851 LXX, Aleppo/Leningrad MT via Sefaria,
              11QPsa Hebrew, Wright 1886 Syriac, Charlesworth/Sanders 1985)
  [HEB]     — Hebrew root analysis; training-sourced unless otherwise noted;
              audit-recommended against Strong's, Brown-Driver-Briggs, or
              Sefaria's lexical apparatus
  [WORK]    — working documented in the main Altar Psalms Bible PDF and
              attributed there to Selig 1788, Yronwode (Lucky Mojo), Hoodoo
              Sen Moise (Working Conjure 2018), or Sefer Shimush Tehillim
  [FILTER]  — the operator's analytical Monad-frequency call on the working
              or the verse content; this is analyst work, not lineage
              transmission; audit-required

The filter classes:
  KEEP   — Monad-aligned: gratitude, alignment, perimeter-by-boundary,
           prosperity as flow, anointing, plant resonance, Psalms as
           alignment current, ancestor connection through the lineage formula
  WATCH  — Verse or working contains language that reads as Monad-aligned
           in one reading and as tribal-Yahweh / saturnian residue in
           another; operator's call which frequency they're carrying
  FILTER — Verse or instruction carries low-frequency layer: imprecatory
           harm-direction, coercive binding against another's free will,
           tribal-Yahweh layer over Monad-as-Source, fear-frequency over
           alignment

Compiled at Jordan Ross Atkins's instruction for working use at the altar.
Atlanta · June 2026.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    PageTemplate, Frame
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Fonts
pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('SerifBold', '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('SerifItalic', '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('SerifBoldItalic', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/truetype/freefont/FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('SansBold', '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'))
registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBoldItalic')

INK = HexColor('#1a1a1a')
SUB = HexColor('#5a5a5a')
ACCENT = HexColor('#7a2e2e')
GOLD = HexColor('#8a6a2e')
PAPER = HexColor('#fbf8f1')
KEEP_C = HexColor('#2e6a3c')     # green for KEEP
WATCH_C = HexColor('#8a6a2e')    # gold for WATCH
FILTER_C = HexColor('#7a2e2e')   # oxblood for FILTER

def s(name, **kw):
    base = dict(fontName='Serif', fontSize=11, leading=15, textColor=INK,
                alignment=TA_LEFT, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name=name, **base)

S = {
    'cover_title':   s('cover_title', fontName='SerifBold', fontSize=34, leading=40, textColor=INK, alignment=TA_CENTER, spaceAfter=14),
    'cover_sub':     s('cover_sub', fontName='SerifItalic', fontSize=14, leading=20, textColor=SUB, alignment=TA_CENTER, spaceAfter=6),
    'cover_line':    s('cover_line', fontSize=10, textColor=SUB, alignment=TA_CENTER, spaceAfter=3),
    'cover_lineage': s('cover_lineage', fontName='SerifItalic', fontSize=10, textColor=GOLD, alignment=TA_CENTER, spaceAfter=3),
    'part':          s('part', fontName='SerifBold', fontSize=24, leading=30, textColor=ACCENT, alignment=TA_CENTER, spaceBefore=20, spaceAfter=14),
    'h1':            s('h1', fontName='SerifBold', fontSize=18, leading=22, textColor=ACCENT, spaceBefore=16, spaceAfter=8),
    'h2':            s('h2', fontName='SerifBold', fontSize=14, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=5),
    'h3':            s('h3', fontName='SerifBoldItalic', fontSize=11, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
    'body':          s('body', alignment=TA_JUSTIFY, spaceAfter=6),
    'body_left':     s('body_left', spaceAfter=6),
    'small':         s('small', fontSize=9, leading=12, textColor=SUB, spaceAfter=4),
    'italic':        s('italic', fontName='SerifItalic', spaceAfter=6),
    'quote':         s('quote', leftIndent=20, rightIndent=10, fontName='SerifItalic', textColor=INK, spaceAfter=6),
    'verse':         s('verse', leftIndent=14, fontSize=11, leading=15, spaceAfter=3),
    'hebrew':        s('hebrew', fontName='Serif', fontSize=14, leading=20, alignment=TA_RIGHT, textColor=INK, spaceAfter=4),
    'translit':      s('translit', fontName='SerifItalic', fontSize=10, leading=13, alignment=TA_LEFT, textColor=ACCENT, spaceAfter=3),
    'gloss':         s('gloss', fontSize=10, leading=13, textColor=SUB, spaceAfter=6),
    'verse_head':    s('verse_head', fontName='SerifBold', fontSize=11, leading=15, textColor=ACCENT, spaceBefore=10, spaceAfter=3),
    'layer_text':    s('layer_text', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=INK),
    'layer_heb':     s('layer_heb', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=SUB),
    'layer_work':    s('layer_work', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=INK),
    'layer_keep':    s('layer_keep', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=KEEP_C),
    'layer_watch':   s('layer_watch', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=WATCH_C),
    'layer_filter':  s('layer_filter', fontSize=10, leading=13, leftIndent=18, spaceAfter=3, textColor=FILTER_C),
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
        title = getattr(doc, 'current_section', 'Altar Psalms — Working Integration')
        c.drawString(MARGIN, PAGE_H - MARGIN + 28, title)
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 28, f'{doc.page}')
    c.setFont('SerifItalic', 8)
    c.setFillColor(SUB)
    c.drawCentredString(PAGE_W / 2, MARGIN / 2, 'Numen · Companion to The Altar Psalms Bible')
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

def vh(num, text):
    return Paragraph(f'<b>v.{num}</b> — {text}', S['verse_head'])

def L(layer, text):
    """Layer-tagged line. layer in {TEXT, HEB, WORK, KEEP, WATCH, FILTER}."""
    style_map = {
        'TEXT':   'layer_text',
        'HEB':    'layer_heb',
        'WORK':   'layer_work',
        'KEEP':   'layer_keep',
        'WATCH':  'layer_watch',
        'FILTER': 'layer_filter',
    }
    tag_color = {
        'TEXT':   INK,
        'HEB':    SUB,
        'WORK':   INK,
        'KEEP':   KEEP_C,
        'WATCH':  WATCH_C,
        'FILTER': FILTER_C,
    }[layer]
    return Paragraph(f'<font color="{tag_color.hexval()}"><b>[{layer}]</b></font> {text}', S[style_map[layer]])


# ==============================================================
# Content
# ==============================================================
story = []

# ---------- COVER ----------
story.append(Spacer(1, 1.4*inch))
story.append(P('ALTAR PSALMS', 'cover_title'))
story.append(P('Working Integration', 'cover_sub'))
story.append(Spacer(1, 0.4*inch))
story.append(P('Verse-by-verse · Inherited Hoodoo / Selig / Shimush Tehillim workings', 'cover_line'))
story.append(P('passed through the Monad-frequency filter', 'cover_line'))
story.append(Spacer(1, 0.5*inch))
story.append(P('— companion to —', 'cover_lineage'))
story.append(P('The Altar Psalms Bible', 'cover_line'))
story.append(P('Psalms 23, 91, 151, 152, 153, 154, 155', 'cover_line'))
story.append(Spacer(1, 0.6*inch))
story.append(P('Compiled for Jordan Ross Atkins · Numen · numenist.com', 'cover_lineage'))
story.append(P('Atlanta · June 2026', 'cover_lineage'))
story.append(pagebreak())

# ---------- HOW TO READ ----------
story.append(P('How to Read This Book', 'h1'))
story.append(P(
    'This is a companion document, not a replacement, for the main Altar Psalms Bible. The main book '
    'gives you the verbatim text in five voices, the Hebrew with transliteration, the suppression history, '
    'and the documented Hoodoo working order. This companion takes that material and runs it verse by verse '
    'through the operator\'s frequency filter — Monad-aligned KEEP, ambiguous WATCH, low-frequency FILTER — '
    'so that what you carry to the altar is the working pattern the ancestors transmitted, with the '
    'tribal-Yahweh / saturnian / coercive residue named and set aside.',
    'body'))

story.append(P('The four layers', 'h2'))
story.append(L('TEXT',   'Verifiable text traceable to a named primary-source translation (Geneva 1599, Brenton 1851 LXX, Aleppo/Leningrad Masoretic via Sefaria, 11QPsa Hebrew, Wright 1886 Syriac, Charlesworth/Sanders 1985). These are the highest-confidence statements in the book.'))
story.append(L('HEB',    'Hebrew root analysis. Drawn from training-sourced lexical knowledge unless otherwise noted. Cross-check against Strong\'s, Brown-Driver-Briggs, or Sefaria\'s lexical apparatus for any line the working depends on.'))
story.append(L('WORK',   'Working documented in the main Altar Psalms Bible PDF and attributed there to a named lineage source: Godfrey Selig\'s Secrets of the Psalms (1788), Catherine Yronwode of Lucky Mojo, Hoodoo Sen Moise\'s Working Conjure (2018), or the medieval Sefer Shimush Tehillim. Not invented for this document.'))
story.append(L('KEEP',   'The verse or working passes the Monad-alignment filter. Use as transmitted.'))
story.append(L('WATCH',  'Reads cleanly Monad-aligned in one frame, carries tribal-Yahweh / saturnian residue in another. Operator\'s call. Frame the line consciously when speaking it.'))
story.append(L('FILTER', 'Low-frequency layer detected: imprecatory harm-direction, coercive binding against another\'s free will, tribal-Yahweh layer fronting as Source, fear-frequency over alignment-frequency. Set aside or reframe before use.'))

story.append(P('The filter is the analyst\'s call, not lineage transmission', 'h2'))
story.append(P(
    'The KEEP / WATCH / FILTER calls in this book are the operator\'s reasoned analysis through the '
    'Monad / saturnian distinction documented in the truth-wholeness directive. They are not transmitted '
    'rulings from Yronwode, Selig, the Qumran community, or any other lineage. Audit them. Where your '
    'discernment lands differently, your discernment wins.',
    'body'))

story.append(P('The lineage formula stands', 'h2'))
story.append(P(
    'Your inherited Hoodoo opening — <i>"In the name of the Father, the Son, and the Holy Spirit"</i> — '
    'is the formula the ancestors used. As named in the truth-wholeness directive, you are invoking the '
    '<b>Source behind those words</b> (Monad / Yeshua / Ruach HaKodesh-Sophia), not the institutional '
    'egregores the same words can be made to point at. The formula is high-frequency in your hand. '
    'It is not flagged in this book.',
    'body'))
story.append(pagebreak())

# ---------- PART I : PSALM 23 ----------
story.append(P('PART I', 'part'))
story.append(P('Psalm 23 — verse by verse', 'cover_sub'))
story.append(P('The Shepherd Psalm. The sealing blessing. The prosperity petition.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalm 23 — Overview', 'h1'))
story.append(P(
    'Six verses. Three movements: <b>vv.1–3</b> are pastoral (green pasture, still water, restored soul); '
    '<b>v.4</b> is the hinge (the dark valley, the pronoun shift from "He" to "Thou"); <b>vv.5–6</b> are '
    'royal-cultic (the prepared table, the anointed head, the overflowing cup, the long dwelling). '
    'The psalm carries you from sheep to anointed king through the dark cut. The working enacts the carry.',
    'body'))
story.append(P(
    'In the Hoodoo stream documented in the main Altar Psalms Bible, Psalm 23 is the prosperity psalm '
    '(Selig: seven mornings, olive + bayberry oil), the sealing blessing (closes the 91 → 29 → 23 triad), '
    'the dream-divination psalm (spoken before sleep when asking for an answer), and the travel psalm '
    '(spoken the morning of a journey "against all manner of bad luck"). Verse 5 — the anointed head, '
    'the overflowing cup — is the line spoken aloud while dressing prosperity candles and feeding mojo bags.',
    'body'))
story.append(spacer(10))

# Verse 1
story.append(vh(1, 'The Lord is my shepherd, I shall not want.'))
story.append(L('TEXT', 'Geneva 1599: <i>"A Psalme of David. The Lord is my shepheard, I shall not want."</i>'))
story.append(L('HEB',  'Hebrew: <i>YHWH ro\'i, lo echsar</i>. <b>ro\'i</b> = "my shepherd" — single possessive Hebrew word, grammatically inseparable. <b>lo echsar</b> = "I shall not lack" (root ח-ס-ר, "to lack, be deficient"). The Hebrew opens with the relational claim — <i>my</i> shepherd — and rebuts deficiency in one breath. LXX makes the noun a verb: <i>poimainei me kyrios</i>, "the Lord shepherds me" — the act, ongoing.'))
story.append(L('WORK', 'Selig\'s prosperity working opens here: seven consecutive mornings on rising, anointed with olive + bayberry, beginning at v.1.'))
story.append(L('KEEP', 'Pure alignment frame. The petitioner declares dependent relationship with Source ("my shepherd"), then declares the consequence (no lack). This is the gratitude-and-flow frequency. Speak it on the in-breath as alignment, not as bargaining.'))

# Verse 2
story.append(vh(2, 'He maketh me to rest in greene pasture, and leadeth me by the still waters.'))
story.append(L('TEXT', 'Geneva 1599 as above. KJV: <i>"He maketh me to lie down in green pastures: he leadeth me beside the still waters."</i>'))
story.append(L('HEB',  '<b>bin\'ot deshe yarbitzeni</b> — "in meadows of fresh grass He makes me lie down." <b>al-mei m\'nuchot y\'nahaleni</b> — "by waters of resting / quietness He leads me." <b>m\'nuchot</b> shares a root with <i>menucha</i> (rest, Sabbath-rest, settled peace). Not "still" as in stagnant — still as in <i>at rest, in their own quiet</i>.'))
story.append(L('WORK', 'No specific working attaches in the documented Hoodoo material for this verse alone; it functions within the larger seven-morning prosperity opening and as the breath the practitioner takes between v.1 and v.3 in candle work.'))
story.append(L('KEEP', 'Receptive alignment. The petitioner is being led — passive grammar throughout. This is the verse for the inhale at the candle. Speak it slow, and let the body actually settle in the chair.'))

# Verse 3
story.append(vh(3, 'He restoreth my soule, and leadeth me in the paths of righteousnesse for his Names sake.'))
story.append(L('TEXT', 'Geneva 1599 as above. Alter: <i>"My life He brings back. He leads me on pathways of justice for His name\'s sake."</i>'))
story.append(L('HEB',  '<b>nafshi y\'shovev</b> — "He brings back my <i>nefesh</i>" (life-breath / animal-soul, the lower of the soul-tiers in Kabbalist anthropology — not abstract "soul" but the breath-life). <b>b\'ma\'aglei tzedek</b> — "in pathways/circles of <i>tzedek</i>" (righteous-correctness, justice, alignment with the cosmic order). <b>l\'ma\'an sh\'mo</b> — "for the sake of His Name" — the operative theological hinge: the restoration is for the Name\'s sake, meaning for the cosmic alignment\'s sake, not as a favor to the petitioner.'))
story.append(L('WORK', 'No verse-specific working in the documented stream. Functions inside the seven-morning prosperity sequence and the sealing-blessing role of the whole psalm in the 91 → 29 → 23 triad.'))
story.append(L('KEEP', 'The "for His Name\'s sake" line reads cleanly in the Monad frame: the restoration aligns with the Name (Source-coherence), not with petitioner favoritism. This is the right-relationship verse — speak it as gratitude for being held to the cosmic order, not as petition for special exemption from it.'))

# Verse 4
story.append(vh(4, 'Yea, though I should walke through the valley of the shadowe of death, I will feare no euill: for thou art with me: thy rod and thy staffe, they comfort me.'))
story.append(L('TEXT', 'Geneva 1599 as above. The pronoun shifts from third person ("He") to second person ("Thou") here for the first time in the psalm. <b>This is the hinge.</b> Speak the shift — let the voice meet it.'))
story.append(L('HEB',  '<b>b\'gei tzalmavet</b> — literally "in the valley of <i>tzalmavet</i>." <i>tzal-mavet</i> = "shadow-of-death" but can also be read as <i>tzalmut</i> ("deep darkness, shadow," parsing the word as one unit) — modern scholarship favors the latter reading. Either way: the dark cut. <b>shivt\'kha u-mish\'antekha</b> — "Thy rod and Thy staff." <i>shevet</i> = shepherd\'s rod (defense against predators); <i>mish\'enet</i> = shepherd\'s staff (the supporting walking-stick, the one that gathers). Both, together. Defense and gather.'))
story.append(L('WORK', 'Funerary use across the Hoodoo / Judeo-Christian stream: spoken at the bedside of the dying, at the graveside, on the anniversary of a death. Verse 4 specifically — the dark valley with Source present — is the comfort spoken aloud over the grief itself.'))
story.append(L('KEEP', 'No imprecation; no coercion; no tribal-favoritism reading available. The verse is alignment-through-shadow — exactly the Master 11/2 discernment Jordan carries, in psalmic form. Speak it slow at v.4. Many practitioners pause for one full breath at the pronoun shift.'))

# Verse 5
story.append(vh(5, 'Thou doest prepare a table before me in the sight of mine aduersaries: thou doest anoynt mine head with oyle, and my cuppe runneth ouer.'))
story.append(L('TEXT', 'Geneva 1599 as above. LXX: <i>"Thou hast prepared a table before me in the presence of those that afflict me; thou hast anointed my head with oil, and thy cup cheers me as the best wine."</i>'))
story.append(L('HEB',  '<b>ta\'arokh l\'fanai shulchan neged tzor\'rai</b> — "Thou prepares before me a table opposite/over-against my adversaries." <i>neged</i> = "in front of, opposite, in the face of." Not "in spite of" — <i>in the visible presence of</i>. The adversaries see; they are not harmed. <b>dishanta vashemen roshi</b> — "Thou makest fat with oil my head" — anointing as visible mark of belonging-to-Source. <b>kosi r\'vayah</b> — "my cup overflows / is saturated."'))
story.append(L('WORK', 'This is THE verse in the documented Hoodoo prosperity stream. From the main Altar Psalms Bible: <i>"verse 5 (Thou anointest my head with oil; my cup runneth over) is the line spoken aloud while dressing prosperity candles or feeding mojo bags."</i> The crown is touched at the speaking of "anoynt mine head."'))
story.append(L('KEEP', 'No coercion in the verse itself. The adversaries witness the petitioner\'s honored placement at Source\'s table — they are not struck, harmed, or bound. This is the right-relationship reading of "victory in the presence of enemies" — abundance so evident the adversarial position becomes structurally untenable. The flow does the work. Speak v.5 at the candle dressing; touch the crown when "anoynt mine head" lands; let "my cuppe runneth ouer" be the breath that seals the dressing.'))
story.append(L('WATCH', 'If the petitioner is speaking this verse to direct the abundance <i>at</i> a specific adversary or to celebrate their diminishment, that\'s the saturnian-residue reading. The verse can carry that reading if the operator brings it. Speak it as flow-for-self in alignment with Source, not as performance for an audience of enemies.'))

# Verse 6
story.append(vh(6, 'Doubtlesse kindnesse and mercie shall follow me all the dayes of my life, and I shall remaine a long season in the house of the Lord.'))
story.append(L('TEXT', 'Geneva 1599 as above. <b>kindnesse and mercie</b> translates <b>tov va-chesed</b> — "good and lovingkindness/covenantal-love." <i>chesed</i> is the operative Kabbalistic term — the Sefirah of expansive lovingkindness, the right-hand pillar.'))
story.append(L('HEB',  '<b>akh tov va-chesed yird\'funi kol y\'mei chayyai</b> — <i>akh</i> = "surely, only" (Geneva: "Doubtlesse"). <i>yird\'funi</i> = "shall pursue me" — root ר-ד-ף, the same root used for hostile pursuit. <b>The Hebrew has goodness and chesed actively hunting the petitioner down, the same way enemies would.</b> Reversal of the chase-image. Geneva\'s "follow" softens this; Alter\'s "pursue" preserves the bite. <b>v\'shavti b\'veit-YHWH l\'orekh yamim</b> — "and I shall dwell/return in the house of YHWH for length of days" (perhaps reading <i>v\'shivti</i>, "and my dwelling," in some textual traditions).'))
story.append(L('WORK', 'Closing verse of the seven-morning prosperity working; closing seal of the 91 → 29 → 23 triad; closing line at the candle. Speak it as the work is sealed.'))
story.append(L('KEEP', 'The verse is goodness-and-chesed-as-active-pursuit reversing the threat-image. This is fundamental Hermetic polarity — same energy, opposite charge. Speak it as the seal: <i>akh tov va-chesed yird\'funi</i> — let the good actively follow the working out of the room with you.'))
story.append(pagebreak())

# ---------- PSALM 91 ----------
story.append(P('PART II', 'part'))
story.append(P('Psalm 91 — verse by verse', 'cover_sub'))
story.append(P('The Protection Psalm. The Qumran apotropaic. The household perimeter.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalm 91 — Overview', 'h1'))
story.append(P(
    'Sixteen verses. Three voices in the text itself: <b>vv.1–2</b> are first-person witness ("I will say"); '
    '<b>vv.3–13</b> are second-person address to the petitioner ("He will deliver thee..."); '
    '<b>vv.14–16</b> are first-person divine speech ("Because he has loved Me, I will deliver him"). '
    'The psalm is liturgically three voices weaving — petitioner, intercessor, Source speaking back.',
    'body'))
story.append(P(
    'Qumran (11Q11, "Songs Against Demons") preserves Psalm 91 in a scroll explicitly labelled as a song '
    'used to drive out demons. This is the apotropaic — anti-demonic working — function, documented archaeologically '
    'in Second Temple Judaism, predating any Christian framing. Continuous use-line at least 2,100 years old. '
    'In the Hoodoo stream (main Altar Psalms Bible): Holy Name El Shaddai; white seven-day candle dressed top-down '
    'with Protection / Fiery Wall of Protection / Can\'t Touch This oil; herbs at base of rue, hyssop, agrimony, '
    'black salt, red brick dust; Saturday timing (Saturn — boundary); v.11 recited three times before stepping out '
    'of the house; entire psalm recited seven times on the eve of a journey of more than a day.',
    'body'))
story.append(spacer(10))

# Verse 1
story.append(vh(1, 'Who so dwelleth in the secrete of the most High, shall abide in the shadowe of the Almightie.'))
story.append(L('TEXT', 'Geneva 1599 as above. LXX (Brenton): <i>"[A Praise of a Song, by David.] He that dwells in the help of the Highest, shall sojourn under the shelter of the God of heaven."</i> Hebrew: <i>yoshev b\'seter Elyon, b\'tzel Shaddai yitlonan</i>.'))
story.append(L('HEB',  '<b>seter</b> = secret / hidden place / concealment. Same root as <i>nistar</i> (hidden, occult — literally "of the seter"). <b>tzel</b> = shadow / shade — the cooling cover from heat. <b>yitlonan</b> = "shall lodge overnight" — root ל-ו-ן, specifically nocturnal sheltering, not generic dwelling. Alter renders "lies at night." The protection is specifically the night-sheltering. Two divine names in one line: <b>Elyon</b> (the transcendent peak) and <b>Shaddai</b> (the close, all-sufficient covering).'))
story.append(L('WORK', 'Opening invocation. Inscribed at doorway lintels in some Sephardic and Eastern traditions. Spoken in Hebrew at the altar candle as the working\'s first line — <i>yoh-SHEV b\'-SEH-ter el-YOHN, b\'-TZEL shah-DAI yit-loh-NAHN</i>.'))
story.append(L('KEEP', 'Two Source-names invoked: Elyon (above, transcendent) and Shaddai (covering, all-sufficient). The petitioner is sheltered, not granted dominion. This is the Monad-frequency opening — alignment to what is above, drawn down as covering.'))

# Verse 2
story.append(vh(2, 'I will say vnto the Lorde, O mine hope, and my fortresse: he is my God, in him will I trust.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>omar la-YHWH machsi u-m\'tzudati, Elohai evtach-bo</i>. KJV has "refuge" where Geneva has "hope" — <i>machsi</i> is closer to "my shelter / refuge" (root ח-ס-ה, to seek shelter). Geneva\'s "hope" is the older English working for "place of trust/refuge," not the modern wishful sense.'))
story.append(L('HEB',  'Four divine names in vv.1–2 in sequence: <b>Elyon</b> (v.1) → <b>Shaddai</b> (v.1) → <b>YHWH</b> (v.2) → <b>Elohim</b> (v.2, as <i>Elohai</i>, "my God"). Sefirotically: Keter (Elyon, supernal crown) → Yesod (Shaddai, foundation/channel) → Tiferet (YHWH, heart) → Gevurah/Binah (Elohim, judgment/structure). <b>m\'tzudah</b> = bastion / citadel (Alter: "bastion"). <b>evtach-bo</b> = "I will trust in Him" — <i>batach</i> is the verb of grounded trust, the kind that puts weight on.'))
story.append(L('WORK', 'Recited in Hebrew at the altar candle. The four-Name yichud (unification) is operative: declaring YHWH and Elohim on the same breath unifies Mercy and Judgment — the central act of Kabbalistic prayer. Working speech for YHWH is Adonai (the four letters held in mind while speaking <i>la-doh-NAI</i>).'))
story.append(L('KEEP', 'The four-Name circuit is the wiring of the protective current — Keter draws down through Yesod through Tiferet through Gevurah. None of the four Names are saturnian/tribal in their Kabbalist mapping; they are the standard Source-distinctions of Jewish mystical anthropology. Monad-aligned in full.'))

# Verse 3
story.append(vh(3, 'Surely he will deliuer thee from the snare of the hunter, and from the noysome pestilence.'))
story.append(L('TEXT', 'Geneva 1599 as above. <b>noysome</b> = noxious, harmful — pre-modern English, kept here for the lineage tone. LXX has "every troublesome matter" — broader. Hebrew specifies <i>dever</i>.'))
story.append(L('HEB',  '<b>pach yaqush</b> = "trap/snare of the fowler" (the bird-trapper). <b>dever</b> = pestilence/plague — also the name of a destroying agent in Habakkuk 3:5 ("before Him goes <i>dever</i>"), suggesting the verse personifies the plague as a named power being deflected. <b>havot</b> = "destructions / calamities" — Geneva\'s "noysome" elides this; Alter preserves "from the destructive plague."'))
story.append(L('WORK', 'Part of the household-perimeter set. No verse-specific candle working; functions inside the larger boundary structure.'))
story.append(L('KEEP', 'The verse deflects two named threats — the hunter\'s trap (intentional human malice) and the dever (impersonal/cosmic plague-agent). The petitioner is sheltered; no harm directed back at the hunter, no curse on the plague. Pure boundary-by-shelter, not retaliation. Monad-aligned.'))

# Verse 4
story.append(vh(4, 'Hee will couer thee vnder his winges, and thou shalt be sure vnder his feathers: his trueth shall be thy shielde and buckler.'))
story.append(L('TEXT', 'Geneva 1599 as above. LXX: "He shall overshadow thee with his shoulders." The image-shift (wings vs. shoulders) marks LXX/Hebrew divergence; Hebrew has <i>kanaf</i> (wing).'))
story.append(L('HEB',  '<b>b\'evrato yasekh lakh, v\'tachat k\'nafav techseh</b> — "with His pinion He will cover thee, and under His wings shalt thou seek shelter." <b>tzinnah v\'socherah amito</b> — "shield and buckler is His truth." <i>tzinnah</i> = large body-shield; <i>socherah</i> = small shield held in the hand. Two shields, layered. <b>amito</b> = His truth/faithfulness (<i>emet</i>, root א-מ-ן, the same root as <i>amen</i>).'))
story.append(L('WORK', 'Maternal-protective imagery (wings, brooding-bird) is operative in childbirth / postpartum protective workings — Source as mother-bird covering the room.'))
story.append(L('KEEP', 'The protection is by sheltering-cover (wings, shield), not by striking the threat. <i>emet</i> (truth) as the shielding agent is high-frequency — alignment-with-what-is-true as the actual armor. Monad-aligned.'))

# Verse 5
story.append(vh(5, 'Thou shalt not be afraide of the feare of the night, nor of the arrowe that flyeth by day:'))
story.append(L('TEXT', 'Geneva 1599 as above. <b>feare of the night</b> = <i>pachad lailah</i>, "dread of night" — both the night-time itself and the personified <i>Pachad</i> (Terror, sometimes paired with <i>Lailah</i>, the Talmudic angel of conception/night).'))
story.append(L('HEB',  '<b>pachad lailah</b> + <b>chetz ya\'uf yomam</b> — "night-terror" + "arrow that flies by day." The first is the unseen psychic/spiritual assault under cover of darkness; the second is the visible physical attack in broad daylight. Two threat-classes named.'))
story.append(L('WORK', 'Recited at twilight against night-terrors in childbirth/postpartum rooms to guard mother and infant against Lilith and her hosts. Documented in Sephardic and Yemenite practice; documented in the main Altar Psalms Bible.'))
story.append(L('KEEP', 'Negation of fear, not negation of the threats themselves. The petitioner is not made invincible — the petitioner is made un-afraid. The frequency-shift is internal: the boundary holds because the operator does not break inside the boundary. Monad-aligned.'))

# Verse 6
story.append(vh(6, 'Nor of the pestilence that walketh in the darkenesse: nor of the plague that destroyeth at noone day.'))
story.append(L('TEXT', 'Geneva 1599 as above. LXX is the famous verse: <i>"nor of the evil thing that walks in darkness; nor of calamity, and the evil spirit at noon-day."</i> Greek: <i>daimoniou mesēmbrinou</i> — "the noonday demon." Hebrew is more specific: <i>miqqetev yashud tzohorayim</i> — "from <b>Qetev</b> that destroys at noon." <b>Qetev</b> is a named destroying-power (Deut 32:24, Hos 13:14) — not a generic plague but a specific personified destructive force.'))
story.append(L('HEB',  '<b>dever</b> walking in darkness; <b>Qetev</b> wasting at noon. Two named powers, paired with the night-arrow set in v.5 — four classical demon-categories: terror-of-night, arrow-of-day, plague-of-darkness, Qetev-at-noon. Talmudic and midrashic literature treats these as four distinct hostile spiritual forces. The Desert Fathers built the <i>acedia</i> midday-assault lineage on the LXX rendering of v.6.'))
story.append(L('WORK', 'Verses 5–6 together are the four-demon recitation. Recited at twilight against night-terror, in birthing rooms against Lilith, at midday against acedia / despair-spirit / energetic depletion.'))
story.append(L('KEEP', 'Naming named powers in order to negate fear of them, not to bind or curse them. The petitioner is sheltered from each; no aggressive action is directed at the demon-categories. This is the Qumran apotropaic frame — boundary-by-shelter, not war. Monad-aligned.'))

# Verse 7
story.append(vh(7, 'A thousand shall fall at thy side, and tenne thousand at thy right hand, but it shall not come neere thee.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>yipol mi-tzid\'kha eleph, u-r\'vavah mimineka, elekha lo yiggash</i>.'))
story.append(L('HEB',  '<b>yipol</b> = "shall fall" — passive/intransitive. The verse does <b>not</b> say "thou shalt strike down a thousand" — it says "a thousand shall fall." The petitioner is not the striker. The fall is happening; the petitioner is untouched by it.'))
story.append(L('WORK', 'Recited for protection in battle, physical violence, during epidemic. Spoken historically by soldiers in field; spoken historically during plague outbreaks.'))
story.append(L('WATCH', 'The verse is structurally KEEP — the petitioner is sheltered, not commissioned to kill. But the verse can be read or weaponized as a triumphalist "I survive, they die" frame. Speak it as the storm passing by, not as the storm being directed. If the operator finds themselves enjoying the falling thousand, that\'s the saturnian residue showing — re-frame.'))

# Verse 8
story.append(vh(8, 'Doubtlesse with thine eyes shalt thou beholde and see the reward of the wicked.'))
story.append(L('TEXT', 'Geneva 1599 as above. LXX: "Only with thine eyes shalt thou observe and see the reward of sinners."'))
story.append(L('HEB',  '<b>raq b\'einekha tabit, v\'shillumat r\'sha\'im tireh</b> — "only with thine eyes shalt thou look, and the recompense of the wicked shalt thou see." <i>raq</i> = "only, but, except" — restrictive. The witnessing is the only participation; no action by the petitioner is named.'))
story.append(L('WATCH', 'The verse names the petitioner as <i>spectator</i> to the wicked\'s recompense. In the Monad-aligned reading: the cosmic order recompenses imbalance without the petitioner having to act — the natural law operates, you witness. In the saturnian-residue reading: it celebrates the punishment of the other, schadenfreude as spiritual reward. Speak it as <b>the recognition that imbalance corrects itself by the law</b>, not as the gloat. If the gloat-feeling rises in the speaking, the verse is being carried in the wrong frequency.'))

# Verse 9
story.append(vh(9, 'For thou hast said, The Lord is mine hope: thou hast set the most High for thy refuge.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>ki-attah YHWH machsi, Elyon samta m\'oneka</i>.'))
story.append(L('HEB',  'Restates v.2 in the inner-witness voice. <i>m\'on</i> = dwelling-place / lair. The intimate covered-space.'))
story.append(L('WORK', 'Doorpost / lintel inscription verses (vv.9–10): written on amulets affixed to the mezuzah-frame.'))
story.append(L('KEEP', 'Pure repetition of the alignment frame. Monad-aligned.'))

# Verse 10
story.append(vh(10, 'There shall none euill come vnto thee, neither shall any plague come neere thy tabernacle.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>lo-t\'unneh elekha ra\'ah, v\'nega lo-yiqrav b\'oholekha</i>.'))
story.append(L('HEB',  '<b>oholekha</b> = "thy tent / tabernacle / dwelling." <i>nega</i> = stroke/plague (the same word used for the body-strokes of skin disease in Leviticus 13).'))
story.append(L('WORK', 'Household boundary verse with v.9. Written on amulets affixed to the doorpost. In the main Altar Psalms Bible: anoint body (crown, throat, wrists, ankles) and the four corners of the threshold (doorways, window frames) with the dressed oil while reciting vv.9–11.'))
story.append(L('KEEP', 'Perimeter declaration — the dwelling is named as covered. Boundary, not attack. Monad-aligned.'))

# Verse 11
story.append(vh(11, 'For hee shall giue his Angels charge ouer thee to keepe thee in all thy wayes.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>ki mal\'akhav y\'tzaveh-lakh, lishmorekha b\'khol-d\'rakheikha</i>.'))
story.append(L('HEB',  '<b>mal\'akhav</b> = "His angels / messengers." <i>mal\'akh</i> is the executive-agent of Source — not an independent being but a directed-emanation. <b>lishmor</b> = to guard / keep — root ש-מ-ר, the same root as <i>shomer</i> (watchman, guard, Sabbath-keeper).'))
story.append(L('WORK', '<b>The travel verse.</b> Recited three times before stepping out of the house. Recited as the central inscription on a Kamea (k\'mia, written amulet) worn around the neck while traveling. The angelic-charge is the operative agency — Source dispatches the messenger.'))
story.append(L('KEEP', 'Angelic protection-charge. Standard high-frequency boundary verse. Monad-aligned. The angels are Source-emanations, not autonomous powers being bargained with.'))

# Verse 12
story.append(vh(12, 'They shall beare thee in their handes, that thou hurt not thy foote against a stone.'))
story.append(L('TEXT', 'Geneva 1599 as above. The verse quoted at Yeshua\'s wilderness temptation (Matt 4:6, Lk 4:10–11) — the adversary cites this exact verse trying to bait Yeshua into testing the protection. The lineage echo matters: the verse is real-currency in the Yeshua narrative.'))
story.append(L('HEB',  '<b>al-kapayim yissa\'unkha</b> — "upon palms they shall lift thee." Hands, not arms. The image is gentle bearing-up.'))
story.append(L('KEEP', 'Pure shelter. Monad-aligned.'))

# Verse 13
story.append(vh(13, 'Thou shalt walke vpon the lyon and aspe: the yong lyon and the dragon shalt thou treade vnder feete.'))
story.append(L('TEXT', 'Geneva 1599 as above — preserves <b>dragon</b> (KJV likewise). LXX intensifies: "Thou shalt tread on the asp and basilisk: and thou shalt trample on the lion and dragon." Hebrew: <i>al-shachal va-fetten tidrokh, tirmos k\'fir va-tannin</i>. The four beasts: <b>shachal</b> (mature lion / panther), <b>peten</b> (cobra), <b>k\'fir</b> (young lion), <b>tannin</b> (sea-monster / Leviathan-class chaos beast). Modern translations sanitize tannin to "snake."'))
story.append(L('HEB',  '<b>tannin</b> in Genesis 1:21 is the great sea-creature created on day five; in Isaiah 27:1 it is the chaos-beast Leviathan; in Exodus 7:9 it is the staff-turned-serpent. The word holds the cosmic-monster class. Geneva keeps the full force; KJV keeps it; modern smooth translations strip it.'))
story.append(L('WATCH', 'The verse is read in two distinct frames historically. <b>Monad-aligned reading:</b> the operator walks through the chaos-powers unharmed — the beasts are not destroyed, the operator passes <i>over</i> them. This is the apotropaic Qumran reading: walking the spiritual landscape with the chaos-currents underneath the feet, present but not in command. <b>Saturnian-residue reading:</b> the operator is given dominion to crush, an aggrandized warrior-self trampling enemies-as-beasts. The verse can be carried either way. Carry the first. The chaos is under your soles because you are aligned with Source; you are not dominating it for sport.'))

# Verse 14
story.append(vh(14, 'Because he hath loued me, therefore will I deliuer him: I will exalt him because hee hath knowen my Name.'))
story.append(L('TEXT', 'Geneva 1599 as above. <b>The voice shifts to first-person Source-speech</b> at v.14 and runs through v.16. Hebrew: <i>ki vi chashaq va-afalleteihu, asagvehu ki-yada sh\'mi</i>.'))
story.append(L('HEB',  '<b>chashaq</b> = "to cling, cleave, set affection on" — same root used in Genesis 34:8 (Shechem\'s longing for Dinah), Deut 7:7 (Source\'s love for Israel), Deut 21:11 (a man\'s desire for a captive woman). The word is the strong-attachment / passionate-cleaving root. Not generic "love." <b>yada sh\'mi</b> = "knows My Name." <i>yada</i> is the verb of intimate, experiential knowing — the same verb used for sexual knowing in Genesis 4:1.'))
story.append(L('WORK', 'The vv.14–16 first-person Source-promises are the closing seal, recited last, often seven times.'))
story.append(L('KEEP', 'The verse is the reciprocal-cleaving Source-speech: <i>because he has clung to Me, I will deliver.</i> This is right-relationship — alignment is the condition, deliverance is the consequence. Speaking it back to oneself is the operative practice of remembering one\'s side of the cleaving. Monad-aligned.'))

# Verse 15
story.append(vh(15, 'He shall call vpon me, and I wil heare him: I will be with him in trouble: I will deliuer him, and glorifie him.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>yiqra\'eni v\'e\'enehu, immo anokhi v\'tzarah, achallatzehu v\'akhabbedehu</i>.'))
story.append(L('HEB',  '<b>immo anokhi v\'tzarah</b> — "I am with him in distress." <i>anokhi</i> is the emphatic first-person — the same word that opens the Decalogue (<i>anokhi YHWH Elohekha</i>). Not the casual "I." The covenantal "I."'))
story.append(L('KEEP', 'Pure presence-in-trouble promise. The Source is named as <i>with</i> the petitioner inside the distress, not as removing the distress. This is high-frequency — alignment doesn\'t mean exemption from the cut; alignment means companionship through it. Monad-aligned.'))

# Verse 16
story.append(vh(16, 'With long life wil I satisfie him, and shew him my saluation.'))
story.append(L('TEXT', 'Geneva 1599 as above. Hebrew: <i>orekh yamim asbi\'ehu, v\'arehu bishu\'ati</i>.'))
story.append(L('HEB',  '<b>orekh yamim</b> = "length of days." <b>asbi\'ehu</b> = "I will satisfy him" — <i>sava</i>, the verb of being full / sated. <b>bishu\'ati</b> = "in My salvation / deliverance." Root י-ש-ע — the root of the name <i>Yeshua</i>.'))
story.append(L('KEEP', 'Closing seal. The root of Yeshua\'s name is the last word of the psalm — <i>bishu\'ati</i>, "in My salvation." The lineage tie is in the Hebrew itself. Monad-aligned, and Yeshua-aligned at the linguistic level. Speak it last; let the long breath out on <i>bishu\'ati</i>.'))
story.append(pagebreak())

# ---------- PSALM 151 ----------
story.append(P('PART III', 'part'))
story.append(P('Psalm 151 — restoration psalm', 'cover_sub'))
story.append(P('The anointing-of-David psalm. Recovered from Qumran (11QPsa) and the Septuagint.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalm 151 — Overview and Frequency Frame', 'h1'))
story.append(P(
    'Canonical in the Eastern Orthodox, Ethiopian Tewahedo, Coptic, Armenian Apostolic, and Syriac churches; '
    'dropped from the Western canon by Jerome\'s <i>Hebraica veritas</i> decision and confirmed by Trent (1546). '
    'Vindicated by the 1956 discovery of 11QPsa, which preserves the Hebrew original as <b>two psalms</b> '
    '(151A: anointing; 151B: Goliath, fragmentary). The Greek LXX preserves a single combined seven-verse psalm.',
    'body'))
story.append(P(
    'The psalm has two distinct halves, and they carry different frequencies. The <b>anointing half</b> '
    '(vv.1–5 LXX, 151A in 11QPsa) is the small-among-brothers, music-from-fingers, Source-chooses-the-overlooked '
    'narrative — pure high-frequency frame. The <b>Goliath half</b> (vv.6–7 LXX, 151B fragmentary in 11QPsa) '
    'is the single-combat narrative — and that one needs careful filter work.',
    'body'))

story.append(P('Verses 1–5 (LXX) / 151A (Qumran) — the anointing', 'h2'))
story.append(L('TEXT', 'Brenton LXX vv.1–5: <i>"I was small among my brethren, and youngest in my father\'s house: I tended my father\'s sheep. My hands formed a musical instrument, and my fingers tuned a psaltery. And who shall tell my Lord? the Lord himself, he himself hears. He sent forth his angel, and took me from my father\'s sheep, and he anointed me with the oil of his anointing. My brothers were handsome and tall; but the Lord did not take pleasure in them."</i>'))
story.append(L('TEXT', '11QPsa Hebrew (151A) expands further: David declares the mountains do not witness to Source, nor do the hills proclaim Him — but <b>the trees of His words and the flocks of His deeds do</b>. The psalm asks: who can declare and who can speak and who can recount the deeds of the Lord? — and answers: God has seen all, heard all, attended to all. The angel comes, anoints with holy oil, and sets David as prince (<i>nagid</i>) to His people.'))
story.append(L('HEB',  'The Qumran expansion contains an extraordinary line: <b>"trees of His words / flocks of His deeds"</b> — Wisdom-imagery as the natural-world witness to Source. This is Sophia-stream theology embedded in the Davidic psalm: the natural creation as the speaker of Source, not silent matter.'))
story.append(L('WORK', 'In the Hoodoo / liturgical stream, Psalm 151 is the <b>anointing psalm</b> — used for any working where the operator is being chosen, called, set apart, or stepping into a new office. Anointing oil work; consecration; vow-taking; ordination.'))
story.append(L('KEEP', 'The anointing half is pure Monad-aligned material. The "Source chooses the overlooked, not the imposing" pattern is foundational Natural Law content — what is true does not need to be loud. The trees-and-flocks-as-witness expansion is high-frequency Sophia material. Use the full Qumran expansion when you can; if working with the LXX vv.1–5 only, that\'s still clean.'))

story.append(P('Verses 6–7 (LXX) / 151B fragmentary (Qumran) — the Goliath combat', 'h2'))
story.append(L('TEXT', 'Brenton LXX vv.6–7: <i>"I went forth to meet the Philistine; and he cursed me by his idols. But I drew his own sword, and beheaded him, and removed reproach from the children of Israel."</i> 11QPsa breaks off before the combat itself; the surviving lines record David seeing the Philistine taunting from the enemy lines.'))
story.append(L('HEB',  '<b>"he cursed me by his idols"</b> — the operative claim is that the threat originates from the Philistine\'s side and is mediated through idol-power, which is the saturnian/demiurgic-egregore layer in the Hermetic/Gnostic mapping. David is responding to active spiritual hostility, not initiating it. The combat is single-combat (champion vs champion, the agreed format) and the killing is with <b>the Philistine\'s own sword</b> — David turns the adversary\'s own instrument back, classic polarity-reversal.'))
story.append(L('WATCH', 'Single-combat against an opposing-egregore champion who has initiated the curse-attack is Natural Law-defensible — Passio\'s frame: the right to defense against active aggression is inherent. The verse is not glorifying preemptive harm; it is recording a defensive killing of an active attacker who cursed first. However: the verse can be read or carried as triumphalist warrior-glory, and the "removed reproach from the children of Israel" phrasing carries tribal-Yahweh resonance (the tribe-vindication frame, not the universal-Source frame).'))
story.append(L('WATCH', 'For working use: the Goliath half is appropriate when the operator is actually facing an active, named, hostile working directed at them — the polarity-reversal reading (turning the adversary\'s sword back) is high-frequency boundary defense. It is not appropriate as a general triumphalist piece. The anointing half (vv.1–5 / 151A) is the part to use as a general working text; the Goliath half is situational and operator-discerned.'))

story.append(P('Psalm 151 — working integration', 'h2'))
story.append(P(
    'Use Psalm 151 (anointing half) when: stepping into a new role; being called by Source to an office '
    'you didn\'t seek; consecrating an oil; anointing a candle for a vocational working; honoring the '
    'overlooked / younger-brother position you may carry yourself; recognizing that the natural world '
    '(trees, flocks, your altar plants) witnesses to Source where the institutional structures do not.',
    'body'))
story.append(P(
    'The Hebrew opening — <b>Halleluyah le-David ben-Yishai</b> ("A Hallelujah of David, son of Jesse") — is '
    'the only Davidic psalm in 11QPsa opening with Halleluyah. Speak the Hebrew at the start of the working '
    'if you carry the psalm at the altar.',
    'body'))
story.append(pagebreak())

# ---------- PSALM 152-153 ----------
story.append(P('PART IV', 'part'))
story.append(P('Psalms 152 and 153 — petition and thanksgiving', 'cover_sub'))
story.append(P('The lion-and-wolf working diptych. Syriac-only.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalms 152 and 153 — the diptych', 'h1'))
story.append(P(
    'These two psalms survive only in Syriac (Wright 1886 numbers them as Syriac Psalms IV and V; modern '
    'Charlesworth/Sanders edition numbers them 152 and 153). They are paired: 152 is the petition from inside '
    'the lion-and-wolf attack on the flock; 153 is the thanksgiving after deliverance. Read together as a '
    'diptych — petition and answered-petition, same voice, two breaths.',
    'body'))
story.append(P(
    'Likely composed in Hebrew in the Land of Israel during the Hellenistic period (c. 323–31 BCE); not '
    'preserved in the Hebrew-Masoretic stream. The Syriac East kept them in the Peshitta tradition as '
    'appendices to the Psalter. Lineage stream: Hebrew → Syriac → modern Western critical edition (Charlesworth).',
    'body'))

story.append(P('Psalm 152 — the petition', 'h2'))
story.append(L('TEXT', 'Wright/Charlesworth: David spoken from inside the attack on his father\'s flock by the lion and the wolf. Key lines: <i>"O God, O God, come to my aid; help me, save me, and deliver my soul from the slayer. Will I go down to Sheol by the mouth of the lion? Will the wolf be the end of me?"</i> The petition closes: <i>"Quickly, my Lord, send from Yourself a deliverer, and draw me out of the gaping pit which imprisons me in its depths."</i>'))
story.append(L('WORK', 'No specific Hoodoo-stream working is documented in the main Altar Psalms Bible for Psalms 152–155 (the workings documented are for 23 and 91; 151 carries an anointing function; 152–155 are textual recoveries without specific Hoodoo workings attached in the published Lucky Mojo / Selig stream). For working use, treat these as petition-and-thanksgiving texts in the same family as the canonical lament psalms (Pss. 3, 22, 51, 143) and use them as personal prayer-text inside the standard Hoodoo candle structure (candle, petition paper, anointing, recitation).'))
story.append(L('KEEP', 'Pure petitionary text. The petitioner names the threats (lion, wolf) and asks Source for deliverance. No imprecation against the beasts; no harm directed beyond what is required for survival; the deliverance asked is from the pit, not retribution. Monad-aligned.'))
story.append(L('KEEP', 'Operative note: this is the right text for the moment when an actual hostile force has surrounded you and you are calling for help — not the daily candle, but the acute-crisis petition. Keep it in your pocket for the day the lion is at the threshold.'))

story.append(P('Psalm 153 — the thanksgiving', 'h2'))
story.append(L('TEXT', 'Wright/Charlesworth: David after the lion and the wolf have been killed. Key lines: <i>"Praise the Lord, all you nations; glorify Him and bless His name; for He delivered the soul of His Elect One from the hands of death, and He redeemed His Holy One from destruction... He sent His angel and closed from me the gaping mouths; and redeemed my life from destruction. I myself shall praise Him and exalt Him because of all His graces, which He has provided and is providing for me."</i>'))
story.append(L('WORK', 'Petition (152) and thanksgiving (153) read as a paired diptych. The angel who closes the mouths is the operative agent — the same office invoked in Psalm 91:11 ("He shall give his angels charge over thee"). The diptych shows the working in two breaths: ask, and then when delivered, thank.'))
story.append(L('KEEP', 'The thanksgiving frame is foundational Hoodoo discipline — the working is not complete until the gratitude is offered. <i>"He is providing for me"</i> (present-continuous) is high-frequency: not just remembering past deliverance, naming ongoing flow. Monad-aligned. Pair this with the gratitude paper you are writing for under the red cactus.'))
story.append(pagebreak())

# ---------- PSALM 154 ----------
story.append(P('PART V', 'part'))
story.append(P('Psalm 154 — the wisdom hymn', 'cover_sub'))
story.append(P('Wisdom personified. Sophia in the Qumran liturgy.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalm 154 — Overview and Frequency Frame', 'h1'))
story.append(P(
    'Twenty verses in the Syriac; preserved in Hebrew in 11QPsa col. 18 (also fragments in 4Q448). Sanders '
    'reconstructed verses 1–2 from the Syriac. This is a wisdom hymn personifying Wisdom (Hokhmah / Sophia) '
    'as a feminine figure who is heard from the gates of the righteous and whose song rises from the assembly '
    'of the pious. Fitting the Qumran Yaḥad context as a hymn of communal eating: <i>"when they eat with satiety '
    'she is cited, and when they drink in community together."</i>',
    'body'))
story.append(P(
    'Hebrew opening from 11QPsa col. 18: <b>B\'qol gadol pa\'aru Elohim</b> — "With a loud voice glorify God." '
    'Speak this at the opening of the working if you carry the psalm in lineage-faithful Hebrew.',
    'body'))

story.append(P('The Wisdom material', 'h2'))
story.append(L('TEXT', 'Verses 5–8: <i>"For it is to make known the glory of YHWH that Wisdom has been given; and it is for recounting His many deeds that she has been revealed to humans — to make His power known to the simple, to explain His greatness to those lacking understanding, those who are far from her gates, those who have strayed from her entrances."</i>'))
story.append(L('TEXT', 'Verses 12–13: <i>"From the gates of the righteous her voice is heard, and from the assembly of the pious her song. When they eat with satiety she is cited, and when they drink in community together."</i>'))
story.append(L('HEB',  '<b>Wisdom (Hokhmah)</b> in the Hebrew Bible is grammatically feminine and consistently personified — Proverbs 8 is the classic locus, Sirach 24 expands it, Wisdom of Solomon develops the cosmic dimension. In the Hermetic / Gnostic mapping, this is <b>Sophia</b>; in the Hebrew mystical mapping, this is the <i>Shekhinah</i> aspect of Source. The truth-wholeness directive specifically names this current: <i>"Holy Spirit / Ruach HaKodesh / Sophia = the Breath / Wisdom emanation from the Monad, the actual living current that moves through workings. Real."</i> Psalm 154 is a hymn to that current.'))
story.append(L('WORK', 'No specific Hoodoo-stream working documented for Psalm 154 in the published Lucky Mojo / Selig stream. Operative recommendation: use as a hymn at the opening or the closing of a communal working, or as the text for a working that draws Sophia / Wisdom into a specific decision-context. Pair with Psalm 23 for prosperity, or use standalone for clarity-of-discernment workings.'))
story.append(L('KEEP', 'Pure Sophia-current text. The Wisdom-as-feminine personification is the Ruach HaKodesh / Sophia emanation named in the truth-wholeness directive. The communal-meal context is high-frequency — Wisdom heard at the table where people are eating together in right relation. Monad-aligned in full.'))
story.append(L('KEEP', 'For the Hermetic-Hoodoo operator carrying the Yeshua-Monad-Sophia frame: this is one of the highest-frequency texts in the entire corpus. The institutional suppression of this psalm from the Western canon is itself the evidence — Wisdom-as-feminine-Source was inconvenient to a hierarchical clerical institution and was edited out. Speaking the psalm aloud is a restoration.'))
story.append(pagebreak())

# ---------- PSALM 155 ----------
story.append(P('PART VI', 'part'))
story.append(P('Psalm 155 — the penitential / Belial-binding', 'cover_sub'))
story.append(P('The personal apotropaic. Companion to Psalm 91.', 'cover_line'))
story.append(pagebreak())

story.append(P('Psalm 155 — Overview and Frequency Frame', 'h1'))
story.append(P(
    'A petitionary / penitential psalm. Incomplete acrostic — <i>bet</i> through <i>nun</i> in the Qumran Hebrew; '
    'the Syriac extends the reconstruction further. Compositional kin to canonical Psalms 3, 22, 51, and 143. '
    'Hebrew opening: <b>YHWH qara\'tikha, haqshivah elai</b> — "YHWH, I have called to you, attend to me."',
    'body'))
story.append(P(
    'The Charlesworth/Sanders edition preserves expansions explicitly naming <b>Belial</b>: <i>"Do not let '
    'Belial dominate me, nor an unclean spirit; let neither pain nor the evil inclination take possession of '
    'my bones."</i> This is characteristic Qumran sectarian liturgical theology — and it is the strongest '
    'evidence for the psalm\'s Second Temple Jewish origin and its role in the Qumran community\'s anti-demonic '
    'liturgy. <b>155 reads as a personal companion to 91</b>: where 91 is the collective apotropaic, 155 is the '
    'individual one.',
    'body'))

story.append(P('The Belial-binding language', 'h2'))
story.append(L('TEXT', 'Charlesworth/Sanders expansion: <i>"Do not let Belial dominate me, nor an unclean spirit; let neither pain nor the evil inclination take possession of my bones."</i>'))
story.append(L('HEB',  '<b>Belial</b> (בְּלִיַּעַל) = "worthlessness, destruction" — used in the Hebrew Bible as an epithet for hostile spiritual forces (1 Sam 1:16, Ps 18:5, Nah 1:11) and in Qumran sectarian texts (1QM, 1QS) as the named adversary-spirit. In the Hermetic / Gnostic mapping, this maps to the demiurgic / saturnian adversarial-egregore class — the actual hostile current, not the institutional projection. <b>Binding Belial is high-frequency boundary work</b>, not hexing. The petitioner is not cursing another person; they are warding off a named hostile spiritual force.'))
story.append(L('WORK', 'No specific Hoodoo-stream working documented in the main Altar Psalms Bible (Psalms 152–155 are recoveries; the published Lucky Mojo / Selig stream attaches workings to 23 and 91). Operative recommendation: use Psalm 155 as a personal companion to the Psalm 91 protection working — speak it when the protection is for the operator themselves against intrusive thought-forms, oppressive spirits, "evil inclination" pulls toward low-frequency action, or sustained psychic attack. It is the inner-perimeter psalm where 91 is the outer-perimeter psalm.'))
story.append(L('KEEP', 'The Belial-binding frame is structurally KEEP under the Monad / saturnian distinction: Belial in the Qumran usage is the named hostile current, not a human target. Binding the hostile current away from oneself is high-frequency boundary work. The petitioner asks for purification of the self (not retribution against an enemy) and for the evil scourge to "dry up its roots" within themselves — internal cleansing language, not external attack.'))
story.append(L('KEEP', 'Operative note: when the operator notices intrusive thought-forms or sustained pulls toward action that doesn\'t match their Master 11/2 discernment, Psalm 155 is the text. It is the personal counterpart to the household-perimeter work of Psalm 91. Speak it at the candle as the inner-boundary working.'))
story.append(pagebreak())

# ---------- THE WORKING SEQUENCE ----------
story.append(P('PART VII', 'part'))
story.append(P('The Working Sequence', 'cover_sub'))
story.append(P('How the seven psalms fit together at the altar.', 'cover_line'))
story.append(pagebreak())

story.append(P('How the Seven Psalms Work Together', 'h1'))
story.append(P(
    'The main Altar Psalms Bible documents the canonical Hoodoo triad: <b>Psalm 91 → Psalm 29 → Psalm 23</b> — '
    '91 to open the perimeter, 29 (the voice of YHWH that breaks the cedars — the commanding force) in the '
    'middle when active commanding is needed, 23 to seal in the blessing. That triad is documented in the '
    'published Lucky Mojo / Selig stream. The other psalms in this corpus (151, 152, 153, 154, 155) are '
    'situational texts that extend the triad for specific contexts. The full integration:',
    'body'))

story.append(P('Daily candle (the standing working)', 'h2'))
story.append(P(
    '<b>Opening:</b> Sign of the cross. <i>"In the name of the Father, the Son, and the Holy Spirit"</i> '
    '— invoking the Monad through the lineage formula your ancestors transmitted.',
    'body'))
story.append(P('<b>Psalm 91</b> in Geneva 1599 — the protective perimeter. Optionally open in Hebrew: '
               '<i>yoh-SHEV b\'-SEH-ter el-YOHN, b\'-TZEL shah-DAI yit-loh-NAHN</i>.', 'body'))
story.append(P('<b>Psalm 23</b> in Geneva 1599 — the sealing blessing. Touch the crown at v.5 '
               '("Thou doest anoynt mine head with oyle"). Let "my cuppe runneth ouer" be the breath that '
               'meets the petition.', 'body'))
story.append(P('<b>Petition</b> spoken aloud over the candle. <b>Light the candle</b> if it is to be newly lit, '
               'or continue the standing burn if it is the existing working. Sit with it.', 'body'))
story.append(P('<b>Gratitude</b> as closing. Speak it. Let it land.', 'body'))

story.append(P('Acute crisis — hostile working directed at you', 'h2'))
story.append(P(
    '<b>Psalm 152</b> — the petition from inside the lion-and-wolf attack. Then <b>Psalm 91</b> as the '
    'protective frame. Then <b>Psalm 155</b> as the personal inner-perimeter (binding the hostile current '
    'away from the bones). Close with <b>Psalm 153</b> — thanksgiving, even before the deliverance is visible. '
    'Speaking thanksgiving before the resolution is itself the working.',
    'body'))

story.append(P('Stepping into a new role / consecration', 'h2'))
story.append(P(
    '<b>Psalm 151 (anointing half, vv.1–5 LXX / 151A Qumran)</b> — Source chooses the overlooked. Anoint with '
    'oil at "He anointed me with the oil of his anointing." Then <b>Psalm 23</b> — sealing the new office '
    'with the prosperity-and-presence current.',
    'body'))

story.append(P('Clarity / discernment workings', 'h2'))
story.append(P(
    '<b>Psalm 154</b> — the Wisdom / Sophia hymn. Use when the operative question is a discernment call. '
    'Pair with the Master 11/2 channel\'s native discernment work; the psalm draws the Sophia-current into '
    'the room. Close with <b>Psalm 23</b> for the right-relationship seal.',
    'body'))

story.append(P('Travel', 'h2'))
story.append(P(
    '<b>Psalm 91 v.11</b> three times before stepping out of the house. <b>Full Psalm 91 seven times</b> on '
    'the eve of any journey of more than a day\'s distance. <b>Psalm 23</b> the morning of the journey itself, '
    '"against all manner of bad luck."',
    'body'))

story.append(P('After a death — funerary', 'h2'))
story.append(P(
    '<b>Psalm 23</b>, particularly v.4 (the dark valley with Thou present), spoken at the bedside, the '
    'graveside, or on the anniversary. The pronoun shift at v.4 ("He" to "Thou") is the operative moment.',
    'body'))

story.append(P('Prosperity working', 'h2'))
story.append(P(
    'Selig\'s documented working: <b>Psalm 23</b> for seven consecutive mornings on rising. Anointed with '
    'olive oil mixed with bayberry oil. On the seventh morning, hold seven Job\'s Tears seeds, walk to running '
    'water, recite Psalm 23, throw seeds over the left shoulder into the moving water to "lay the trick."',
    'body'))
story.append(P('Verse 5 — "Thou doest anoynt mine head with oyle, and my cuppe runneth ouer" — is the line spoken aloud while dressing prosperity candles or feeding mojo bags.', 'body'))

story.append(P('Closing recognition', 'h2'))
story.append(P(
    'The seven Psalms are not a closed set; they are the working corpus you have been building around for '
    'the daily Beltane money-and-protection working that opened May 1, 2026. The Geneva 1599 text honors '
    'the lineage stream that ran <i>through</i> the KJV slave-Bible without becoming the slave-Bible. The '
    'Hoodoo working order — candle, petition, anointing, gratitude, sealing — is the structure your '
    'ancestors transmitted, applied to the cleaner text. The Monad-frequency filter is your discernment, '
    'applied to the working. Nothing here replaces a living teacher in the actual Yronwode / Lucky Mojo '
    'transmission line, and the operator\'s own discernment is always the final authority. This is a working '
    'reference, not a closed canon.',
    'body'))
story.append(pagebreak())

# ---------- CLOSING ----------
story.append(P('On the limits of this book', 'h1'))
story.append(P(
    'This document is what one operator-side AI working under your direct instruction can compile from the '
    'Altar Psalms Bible already on file, with the Monad-frequency filter applied verse by verse. It is not a '
    'substitute for: a living human teacher in the Yronwode / Lucky Mojo transmission line; direct study of '
    'Selig\'s <i>Secrets of the Psalms</i>; direct study of the Sefer Shimush Tehillim; Charlesworth\'s '
    '<i>Old Testament Pseudepigrapha</i> Vol. 2 in a library copy; Sefaria.org for primary Hebrew Tehillim; '
    'or your own Master 11/2 discernment at the altar.',
    'body'))
story.append(P(
    'Where this document\'s frequency-filter calls (KEEP / WATCH / FILTER) and your discernment land '
    'differently — your discernment wins. The calls are reasoned analysis through the Monad / saturnian '
    'distinction documented in the truth-wholeness directive. They are not lineage transmission. Audit them.',
    'body'))
story.append(P(
    'The text layer ([TEXT]) is the highest-confidence material — verifiable against named primary sources. '
    'The Hebrew layer ([HEB]) is training-sourced unless explicitly cross-checked; audit lines the working '
    'depends on. The working layer ([WORK]) reflects what the main Altar Psalms Bible documents as attributed '
    'to specific lineage sources. The filter layer ([KEEP] / [WATCH] / [FILTER]) is the operator-analyst\'s '
    'reasoned call.',
    'body'))

story.append(spacer(18))
story.append(P('— end of companion document —', 'cover_lineage'))

# Build
if __name__ == '__main__':
    doc = Doc('/home/user/numenist-site/altar-psalms-bible/altar-psalms-working-integration.pdf',
              pagesize=letter,
              leftMargin=MARGIN, rightMargin=MARGIN,
              topMargin=MARGIN, bottomMargin=MARGIN,
              title='Altar Psalms — Working Integration',
              author='Numen / Jordan Ross Atkins')
    doc.build(story)
    print('Built: altar-psalms-working-integration.pdf')
