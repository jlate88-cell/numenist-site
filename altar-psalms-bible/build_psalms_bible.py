"""
Altar Psalms Bible — build script
Compiled from 10-agent deep research deployment for Jordan Ross Atkins / Numen.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, PageTemplate, Frame
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ---- Fonts: FreeSerif covers Hebrew glyphs ----
pdfmetrics.registerFont(TTFont('Serif', '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'))
pdfmetrics.registerFont(TTFont('SerifBold', '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'))
pdfmetrics.registerFont(TTFont('SerifItalic', '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'))
pdfmetrics.registerFont(TTFont('SerifBoldItalic', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/truetype/freefont/FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('SansBold', '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'))

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBoldItalic')

# Colors
INK = HexColor('#1a1a1a')
SUB = HexColor('#5a5a5a')
ACCENT = HexColor('#7a2e2e')   # deep oxblood
GOLD = HexColor('#8a6a2e')
PAPER = HexColor('#fbf8f1')    # parchment off-white

# Styles
def s(name, parent=None, **kw):
    base = dict(
        fontName='Serif', fontSize=11, leading=15, textColor=INK,
        alignment=TA_LEFT, spaceAfter=6,
    )
    base.update(kw)
    return ParagraphStyle(name=name, **base)

S = {
    'cover_title':   s('cover_title', fontName='SerifBold', fontSize=42, leading=46, textColor=INK, alignment=TA_CENTER, spaceAfter=18),
    'cover_sub':     s('cover_sub', fontName='SerifItalic', fontSize=16, leading=22, textColor=SUB, alignment=TA_CENTER, spaceAfter=8),
    'cover_line':    s('cover_line', fontSize=11, textColor=SUB, alignment=TA_CENTER, spaceAfter=4),
    'cover_lineage': s('cover_lineage', fontName='SerifItalic', fontSize=10, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4),

    'part':          s('part', fontName='SerifBold', fontSize=26, leading=32, textColor=ACCENT, alignment=TA_CENTER, spaceBefore=24, spaceAfter=16),
    'h1':            s('h1', fontName='SerifBold', fontSize=20, leading=24, textColor=ACCENT, spaceBefore=18, spaceAfter=10),
    'h2':            s('h2', fontName='SerifBold', fontSize=15, leading=19, textColor=ACCENT, spaceBefore=14, spaceAfter=6),
    'h3':            s('h3', fontName='SerifBoldItalic', fontSize=12, leading=16, textColor=INK, spaceBefore=10, spaceAfter=4),

    'body':          s('body', alignment=TA_JUSTIFY, spaceAfter=8),
    'body_left':     s('body_left', spaceAfter=8),
    'small':         s('small', fontSize=9, leading=12, textColor=SUB, spaceAfter=4),
    'italic':        s('italic', fontName='SerifItalic', spaceAfter=6),
    'quote':         s('quote', leftIndent=24, rightIndent=12, fontName='SerifItalic', textColor=INK, alignment=TA_LEFT, spaceAfter=8),
    'verse':         s('verse', leftIndent=18, fontSize=11, leading=16, alignment=TA_LEFT, spaceAfter=4),
    'hebrew_big':    s('hebrew_big', fontName='Serif', fontSize=18, leading=26, alignment=TA_RIGHT, textColor=INK, spaceAfter=4),
    'hebrew':        s('hebrew', fontName='Serif', fontSize=14, leading=22, alignment=TA_RIGHT, textColor=INK, spaceAfter=4),
    'translit':      s('translit', fontName='SerifItalic', fontSize=11, leading=15, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=4),
    'gloss':         s('gloss', fontSize=11, leading=14, alignment=TA_CENTER, textColor=SUB, spaceAfter=10),
    'toc':           s('toc', fontSize=11, leading=18, spaceAfter=2),
    'caption':       s('caption', fontName='SerifItalic', fontSize=9, leading=12, textColor=SUB, alignment=TA_CENTER, spaceAfter=10),
    'source':        s('source', fontSize=8, leading=11, textColor=SUB, leftIndent=12, spaceAfter=2),
}

# Page templates with running header / footer
PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Background — subtle parchment
    canvas_obj.setFillColor(PAPER)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Header rule
    if doc.page > 1:
        canvas_obj.setStrokeColor(GOLD)
        canvas_obj.setLineWidth(0.4)
        canvas_obj.line(MARGIN, PAGE_H - MARGIN + 22, PAGE_W - MARGIN, PAGE_H - MARGIN + 22)
        canvas_obj.setFont('SerifItalic', 9)
        canvas_obj.setFillColor(SUB)
        title = getattr(doc, 'current_section', 'The Altar Psalms Bible')
        canvas_obj.drawString(MARGIN, PAGE_H - MARGIN + 28, title)
        canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 28, f'{doc.page}')
    # Footer
    canvas_obj.setFont('SerifItalic', 8)
    canvas_obj.setFillColor(SUB)
    canvas_obj.drawCentredString(PAGE_W / 2, MARGIN / 2, 'Numen · numenist.com')
    canvas_obj.restoreState()


class PsalmsDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(MARGIN, MARGIN, PAGE_W - 2*MARGIN, PAGE_H - 2*MARGIN, id='main',
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=12)
        self.addPageTemplates([PageTemplate(id='cover', frames=frame, onPage=header_footer),
                               PageTemplate(id='body', frames=frame, onPage=header_footer)])
        self.current_section = ''

    def afterFlowable(self, flowable):
        # Update running section title from H1/Part headings
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            if sn in ('part', 'h1'):
                txt = flowable.getPlainText()
                self.current_section = txt


# ---- Helper builders ----
def P(text, style='body'):
    return Paragraph(text, S[style])

def hebrew_line(text, big=False):
    return Paragraph(text, S['hebrew_big' if big else 'hebrew'])

def spacer(h=8):
    return Spacer(1, h)

def pagebreak():
    return PageBreak()

def verse_row(num, txt):
    return Paragraph(f'<b>{num}.</b> {txt}', S['verse'])

def translation_table(rows, col_widths=None):
    """rows: list of (source, text) tuples."""
    if col_widths is None:
        col_widths = [1.4*inch, 4.6*inch]
    data = []
    for src, txt in rows:
        data.append([Paragraph(f'<b>{src}</b>', S['small']),
                     Paragraph(txt, S['body_left'])])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-2), 0.3, HexColor('#d8d0c0')),
        ('BACKGROUND', (0,0), (0,-1), HexColor('#f0ece2')),
    ]))
    return t


# ==============================================================
# Content
# ==============================================================
story = []

# ---------- COVER ----------
story.append(Spacer(1, 1.4*inch))
story.append(P('THE ALTAR PSALMS BIBLE', 'cover_title'))
story.append(P('A working reference for the Hermetic-Hoodoo practitioner', 'cover_sub'))
story.append(Spacer(1, 0.5*inch))
story.append(P('Psalms 23, 91, 151, 152, 153, 154, 155', 'cover_line'))
story.append(P('In Hebrew, Greek (Septuagint), Latin, Geneva, JPS, KJV, Alter', 'cover_line'))
story.append(P('with Syriac and Qumran sources for the suppressed Five', 'cover_line'))
story.append(Spacer(1, 0.45*inch))
story.append(P('— including —', 'cover_lineage'))
story.append(P('Hebrew pronunciation · Kabbalistic divine names · sefirotic mapping', 'cover_line'))
story.append(P('Hoodoo working order · Sefer Shimush Tehillim · 72 Names', 'cover_line'))
story.append(P('Vulgate vs LXX transmission · Coptic and Ethiopian retention', 'cover_line'))
story.append(P('The YHVH discernment', 'cover_line'))
story.append(Spacer(1, 0.6*inch))
story.append(P('Compiled from a ten-agent deep research deployment', 'cover_lineage'))
story.append(P('for Jordan Ross Atkins · Numen · numenist.com', 'cover_lineage'))
story.append(P('Atlanta · June 2026', 'cover_lineage'))
story.append(pagebreak())

# ---------- TABLE OF CONTENTS ----------
story.append(P('Contents', 'h1'))
story.append(spacer(8))
toc_entries = [
    ('Foreword — On Who You Are Calling To', ''),
    ('', ''),
    ('PART I  —  THE OPERATIVE PSALMS', ''),
    ('Psalm 23  ·  The Shepherd Psalm in Five Voices', ''),
    ('Psalm 91  ·  The Protection Psalm in Five Voices', ''),
    ('Psalm 151  ·  Restored from Greek and Qumran', ''),
    ('Psalm 152  ·  The Petition (Syriac)', ''),
    ('Psalm 153  ·  The Thanksgiving (Syriac)', ''),
    ('Psalm 154  ·  The Wisdom Hymn (Qumran + Syriac)', ''),
    ('Psalm 155  ·  The Penitential / Belial-Binding (Qumran + Syriac)', ''),
    ('', ''),
    ('PART II  —  THE WORKING MATERIALS', ''),
    ('Hebrew Pronunciation — Psalm 91, Verses 1–2', ''),
    ('The Four Divine Names of Psalm 91', ''),
    ('Chaldean Vibrations of the Names', ''),
    ('Hoodoo Working Order  ·  Psalms 23, 29, 91', ''),
    ('Sefer Shimush Tehillim and the 72 Names', ''),
    ('Sefirotic Mapping of the Psalm 91 Names', ''),
    ('Three Operative Contexts — Sleep, Funeral, Journey', ''),
    ('', ''),
    ('PART III  —  TRANSMISSION AND SUPPRESSION', ''),
    ('The Latin Layer — Vulgate vs Septuagint Psalter', ''),
    ('The African Psalter — Coptic, Ethiopian, Beta Israel', ''),
    ('How the Suppression Happened', ''),
    ('', ''),
    ('PART IV  —  THE FULL ALTAR ORDER', ''),
    ('A Working Liturgy', ''),
    ('Sources and Bibliography', ''),
]
for label, _ in toc_entries:
    if not label:
        story.append(spacer(4))
    elif label.startswith('PART'):
        story.append(Paragraph(f'<font color="#7a2e2e"><b>{label}</b></font>', S['toc']))
    else:
        story.append(P(label, 'toc'))
story.append(pagebreak())

# ---------- FOREWORD ----------
story.append(P('Foreword', 'h1'))
story.append(P('On Who You Are Calling To', 'h2'))

story.append(P(
    'This book exists because the operator asked for the whole truth, not the approved version of it. '
    'What follows is the Psalter as it was used before the canon was fixed against the lineage — '
    'the texts the Qumran community held, the texts the Ethiopian Church never stopped copying, '
    'the texts the Syriac East preserved when Rome and the Reformers dropped them. '
    'It is also the Psalter the Hoodoo doctors of the African diaspora carried inside the Christian wrapper '
    'their ancestors were handed, and it is the operative Hebrew the Kabbalists never lost.',
    'body'))

story.append(P('A note on the Source you are addressing', 'h3'))
story.append(P(
    'The operator works in the language his Hoodoo ancestors used — '
    '<i>"In the name of the Father, the Son, and the Holy Ghost"</i> — '
    'and this book honours that formula. It also honours the discernment that knows the formula is a wrapper, '
    'not an ID badge.',
    'body'))
story.append(P('YHWH — the storm-god egregore (ancient)', 'h3'))
story.append(P(
    'The archaeological record is clear: <b>YHWH</b> first appears in Egyptian topographical lists from '
    'about 1400 BCE — Soleb and Amara West — as "Yhw of the Shasu land," a regional storm-and-warrior deity '
    'of the Edomite-Midianite-Kenite south. The oldest biblical theophanies (Deuteronomy 33:2, Judges 5:4-5, '
    'Habakkuk 3:3, Psalm 68:7-8) all describe YHWH coming from <i>Seir / Sinai / Teman / Paran</i> '
    'in storm-god grammar — earth quaking, heavens dropping rain, mountains melting. '
    'This is not the unconditioned Source. This is a powerful regional egregore later editorially fused with '
    '<b>El</b>, the Canaanite high god of the divine council at Ugarit, and elevated to sole-god status '
    'by the seventh-century Deuteronomistic editors under Josiah. Ancient, real, operative — '
    'but not the Monad.',
    'body'))

story.append(P('Jehovah — the medieval Christian fabrication (not even ancient)', 'h3'))
story.append(P(
    '<b>"Jehovah" is not a divine name at all.</b> It is a 13th-century Christian Hebraist construction. '
    'The Tetragrammaton YHWH was never vocalized in Jewish tradition — the Masoretes inserted the vowels '
    'of <i>Adonai</i> ("my Lord") into the consonantal text as a <i>qere</i>, a reading instruction telling '
    'the reader to say "Adonai" instead of attempting the unutterable Name. Medieval Christian Hebraists '
    'misread this scribal apparatus as the actual vocalization and produced the hybrid <i>Yehowah</i> '
    '(YHWH consonants + Adonai vowels).',
    'body'))
story.append(P(
    'The Spanish Dominican friar <b>Raymundus Martini</b> introduced this form into Christian writing in his '
    '<i>Pugio Fidei</i>, <b>1270 CE</b> — originally as <i>Yohoua</i>. The spelling <i>Jehova</i> appeared '
    'only when <b>Joseph Voisin edited Martini\'s work in the 17th century</b>. The letter <b>J</b> itself '
    'did not exist as a distinct character until <b>Gian Giorgio Trissino proposed it in 1524</b>; before '
    'that, medieval Latin used a lengthened "I" for both vowel and consonant. The 1611 KJV still printed '
    '<i>Iehouah</i>; the modern English "Jehovah" with the J only stabilized in the mid-17th century.',
    'body'))
story.append(P(
    '<b>So "Jehovah" is barely 400 years old in its modern form, and the underlying concept</b> — combining '
    'Adonai\'s vowels with YHWH\'s consonants — <b>is itself a 750-year-old Christian misreading of a '
    'Jewish scribal mark.</b> No continuous lineage. No ancient referent. The Jehovah\'s Witness movement '
    'and the entire Anglo-Protestant invocation of "Jehovah God" is a Christian-Hebraist artifact treated '
    'as if it were a primordial Name. It is a manufactured egregore on top of an already-manufactured '
    'composite of YHWH (storm god) and El (high god). Two layers of construction, one called "Jehovah."',
    'body'))

story.append(P('The Source — actual names, with lineage', 'h3'))
story.append(P(
    'The <b>Monad</b> — the Hermetic <i>All</i>, the Gnostic Pleroma\'s source, the unconditioned ground — '
    'is the actual Source address. <b>Elyon</b> ("Most High"), the name Melchizedek used in Genesis 14 to bless '
    'Abraham <i>before</i> the later editorial fusion of Elyon with YHWH, names that address. '
    'So does <b>Yeshua</b> ("YHWH saves") — when he taught his disciples to '
    'pray, he taught them to say <i>Abba</i>, not <i>YHWH</i> and not <i>Jehovah</i>. So does <b>Ein Sof</b> '
    'in Kabbalah, the Source beyond every name and every sefirah of the Tree.',
    'body'))

story.append(P('Chaldean check on the names — by category, not by digit', 'h3'))
story.append(P(
    'Grouping by category surfaces the distinction. Reducing digits alone makes coincidences '
    'look like equivalences — but a Source-name and an egregore-name that both reduce to the same final '
    'digit do not share an address. The compound number and its Tarot correspondence carry the actual signal.',
    'body'))

# Source names — grouped at top
story.append(P('<b>Source-names</b> (continuous lineage to the unconditioned ground):', 'body'))
src_table = Table([
    ['Name', 'Letters', 'Compound', 'Reduced', 'Tarot'],
    ['ELYON', 'E(5)+L(3)+Y(1)+O(7)+N(5)', '21', '3', 'The World'],
    ['MONAD', 'M(4)+O(7)+N(5)+A(1)+D(4)', '21', '3', 'The World'],
    ['YESHUA', 'Y(1)+E(5)+S(3)+H(5)+U(6)+A(1)', '21', '3', 'The World'],
], colWidths=[0.9*inch, 2.4*inch, 0.75*inch, 0.7*inch, 1.0*inch])
src_table.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (-1,-1), 'Serif', 10),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('BACKGROUND', (0,1), (-1,-1), HexColor('#f5f1e4')),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(src_table)
story.append(P(
    'All three hit <b>21 / The World</b> at the compound — the completion card, the dancer in the wreath, '
    'the four kerubim at the corners, the fully integrated cosmos. Same vibrational address. '
    'Same Source through three name-faces.',
    'small'))
story.append(spacer(8))

# Egregore names — grouped separately, with provenance notes
story.append(P('<b>Egregore-names</b> (powerful but not the Source — different addresses entirely):', 'body'))
egr_table = Table([
    ['Name', 'Letters', 'Compound', 'Reduced', 'Tarot / Note'],
    ['YHWH', 'Y(1)+H(5)+W(6)+H(5)', '17', '8', 'The Star (ancient storm-god name, ~1400 BCE)'],
    ['JEHOVAH', 'J(1)+E(5)+H(5)+O(7)+V(6)+A(1)+H(5)', '30', '3', 'No Tarot Major — name fabricated 1270 CE; J letter 1524 CE'],
], colWidths=[0.9*inch, 2.4*inch, 0.75*inch, 0.7*inch, 2.7*inch])
egr_table.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (-1,-1), 'Serif', 9.5),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('BACKGROUND', (0,1), (-1,-1), HexColor('#f1e8e0')),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(egr_table)
story.append(P(
    '<b>JEHOVAH\'s 30/3 reduction does <i>not</i> share an address with the Source-names\' 21/3.</b> '
    'The reduction-to-3 by digit-sum is a coincidence of arithmetic; the compound number is what carries the '
    'signal, and 30 (no major-arcana correspondence in the standard Chaldean-Tarot keying) is qualitatively '
    'different from 21 (The World). Jehovah\'s additional disqualification: <b>it has no continuous lineage '
    'at all.</b> Where YHWH at least anchors to an ancient regional storm-god name with 3,400 years of '
    'historical use, Jehovah is a medieval Christian Hebraist artifact, a misreading of a scribal mark '
    'rendered in a letter that did not yet exist. Two layers of fabrication. Operationally: '
    '<b>do not invoke "Jehovah" thinking you are addressing the Source.</b> You are addressing a '
    '750-year-old Christian-Hebraist construct.',
    'small'))

story.append(P('How to use the formula', 'h3'))
story.append(P(
    'The Hoodoo formula keeps its operative power when the operator names the Source explicitly at the front of '
    'the invocation, so the routing is unambiguous. Working options:',
    'body'))
story.append(P(
    '<i>"In the name of the Most High <b>Elyon</b>, of <b>Yeshua</b> the Anointed, '
    'and of the <b>Ruach HaKodesh</b> — the Holy Breath, Sophia — '
    'the living current that moves through this working."</i>',
    'quote'))
story.append(P(
    '<i>Or simpler: "In the name of the <b>Monad</b>, the <b>All</b>, and the <b>Holy Breath</b>."</i>',
    'quote'))
story.append(P(
    'For Psalm 91 specifically, the four divine names in v.1–2 (<b>Elyon, Shaddai, YHWH, Elohim</b>) '
    'should be held as <i>Elyon and Shaddai</i> first — the load-bearing protective names — '
    'with YHWH and Elohim read as the wider divine-council layer underneath. '
    'The Qumran community used this psalm as a song against demons (11Q11). They knew what they were addressing.',
    'body'))

story.append(P('On lineage', 'h3'))
story.append(P(
    'The transmission line of the Psalter you hold runs through Africa first, Rome second. '
    'Hebrew Second-Temple liturgy → Alexandrian Greek Septuagint (produced by Jews in Africa) → '
    'Coptic Sahidic and Bohairic Psalters → Ge\'ez Mäzmurä Dawit and the unbroken Tewahedo chain → '
    'the Christian text that arrived in West Africa by multiple vectors → '
    'the Bible the enslaved received in the Americas and re-coded as operative spellwork. '
    'The candle on the altar in Atlanta in June 2026 is the local instance of that line, not its imitation.',
    'body'))
story.append(P(
    '<i>Rome inherited. Africa transmitted. The working continues.</i>',
    'italic'))
story.append(pagebreak())

# =========================================================
# PART I — THE OPERATIVE PSALMS
# =========================================================
story.append(Spacer(1, 1.2*inch))
story.append(P('PART I', 'part'))
story.append(P('The Operative Psalms', 'cover_sub'))
story.append(Spacer(1, 0.4*inch))
story.append(P(
    'The texts themselves, in five voices where available — '
    'Hebrew with transliteration, Geneva 1599 (lineage-faithful for the Hoodoo working), '
    'JPS (closest pre-Christianized English), Septuagint (Brenton), and Robert Alter (the operative Hebrew read).',
    'italic'))
story.append(pagebreak())

# ---------- PSALM 23 ----------
story.append(P('Psalm 23', 'h1'))
story.append(P('The Shepherd Psalm', 'h2'))

story.append(P('Hebrew — Verses 1–2 (Masoretic)', 'h3'))
story.append(hebrew_line('מִזְמ֥וֹר לְדָוִ֑ד יְהוָ֥ה רֹ֝עִ֗י לֹ֣א אֶחְסָֽר׃', big=True))
story.append(P('Mizmor le-David. YHWH ro\'i, lo echsar.', 'translit'))
story.append(P('"A psalm of David. YHWH is my shepherd; I shall not lack."', 'gloss'))
story.append(spacer(4))
story.append(hebrew_line('בִּנְא֣וֹת דֶּ֭שֶׁא יַרְבִּיצֵ֑נִי עַל־מֵ֖י מְנֻח֣וֹת יְנַהֲלֵֽנִי׃', big=True))
story.append(P('Bin\'ot deshe yarbitzeini; al-mei menuchot yenahaleini.', 'translit'))
story.append(P('"In meadows of fresh grass He makes me lie down; beside waters of restfulness He leads me."', 'gloss'))
story.append(spacer(8))
story.append(P(
    'The relational claim is grammatically inseparable from the naming: <i>ro\'i</i> is a single Hebrew word, '
    'possessive — "my shepherd." <i>Lo echsar</i> (root ח-ס-ר, "to lack, be deficient") is one terse rebuttal of want.',
    'body'))
story.append(pagebreak())

story.append(P('Psalm 23 — Five Voices', 'h2'))

# Verse 1
story.append(P('Verse 1 — The LORD is my shepherd', 'h3'))
story.append(translation_table([
    ('Alter (2007)', '"A David psalm. The LORD is my shepherd, I shall not want."'),
    ('Geneva 1599', '"A Psalme of David. The Lord is my shepheard, I shall not want."'),
    ('JPS 1985', '"The LORD is my shepherd; I lack nothing."'),
    ('LXX (Brenton)', '"The Lord tends me as a shepherd, and I shall want nothing."'),
    ('KJV 1611', '"The LORD is my shepherd; I shall not want."'),
]))
story.append(P(
    'The Greek <i>poimainei me kyrios</i> verbalizes the noun: not "the Shepherd who is mine" but '
    '"the One who is shepherding me — now, in the act."',
    'small'))

# Verse 2
story.append(P('Verse 2 — Green pastures, still waters', 'h3'))
story.append(translation_table([
    ('Alter', '"In grass meadows He makes me lie down, by quiet waters guides me."'),
    ('Geneva 1599', '"He maketh me to rest in greene pasture, and leadeth me by the still waters."'),
    ('JPS 1985', '"He makes me lie down in green pastures; He leads me to water in places of repose."'),
    ('LXX (Brenton)', '"In a place of green grass, there he has made me dwell: he has nourished me by the water of rest."'),
    ('KJV', '"He maketh me to lie downe in green pastures: he leadeth me beside the still waters."'),
]))

# Verse 3
story.append(P('Verse 3 — The pivot', 'h3'))
story.append(translation_table([
    ('Alter', '"My life He brings back. He leads me on pathways of justice for His name\'s sake."'),
    ('Geneva 1599', '"He restoreth my soule, and leadeth me in the paths of righteousnesse for his Names sake."'),
    ('JPS 1985', '"He renews my life; He guides me in right paths as befits His name."'),
    ('LXX (Brenton)', '"He has restored my soul: he has guided me into the paths of righteousness, for his name\'s sake."'),
]))
story.append(P(
    '<b>Critical word:</b> נֶפֶשׁ (<i>nefesh</i>). Alter refuses "soul" — the Hebrew has no Platonic '
    'body/soul split. <i>Nefesh</i> is throat, breath, life-force, the living animal self. '
    '"<b>My life He brings back</b>" preserves the somatic charge the Christianized "restoreth my soule" '
    'laundered out. For working purposes: nefesh is the living breath, not a disembodied soul — '
    'this matters when the psalm is being used to call something back into a body.',
    'body'))

# Verse 4
story.append(P('Verse 4 — The valley (the load-bearing verse)', 'h3'))
story.append(translation_table([
    ('Alter', '"Though I walk in the vale of death\'s shadow, I fear no harm, for You are with me. Your rod and Your staff — it is they that console me."'),
    ('Geneva 1599', '"Yea, though I should walke through the valley of the shadowe of death, I will feare no euill: for thou art with me: thy rod and thy staffe, they comfort me."'),
    ('JPS 1985', '"Though I walk through a valley of deepest darkness, I fear no harm, for You are with me; Your rod and Your staff — they comfort me."'),
    ('LXX (Brenton)', '"Yea, even if I should walk in the midst of the shadow of death, I will not be afraid of evils: for thou art with me; thy rod and thy staff, these have comforted me."'),
    ('KJV', '"Yea, though I walke through the valley of the shadow of death, I will feare no euill: for thou art with me, thy rod and thy staffe, they comfort me."'),
]))

# Verse 5
story.append(P('Verse 5 — Table, anointing, cup', 'h3'))
story.append(translation_table([
    ('Alter', '"You set out a table before me in the face of my foes. You moisten my head with oil, my cup overflows."'),
    ('Geneva 1599', '"Thou doest prepare a table before me in the sight of mine aduersaries: thou doest anoynt mine head with oyle, and my cuppe runneth ouer."'),
    ('JPS 1985', '"You spread a table for me in full view of my enemies; You anoint my head with oil; my drink is abundant."'),
    ('LXX (Brenton)', '"Thou hast prepared a table before me in presence of them that afflict me: thou hast thoroughly anointed my head with oil; and thy cup cheers me like the best wine."'),
]))
story.append(P(
    'The LXX adds the inebriating cup — <b>μεθύσκον</b> (<i>methyskon</i>), "intoxicating" — a sacramental '
    'drunkenness that the Masoretic merely calls "overflowing" (<i>revayah</i>, "saturation"). '
    'For a Hoodoo anointing, the LXX reading sanctions the cup as actively transformative.',
    'small'))

# Verse 6
story.append(P('Verse 6 — The dwelling', 'h3'))
story.append(translation_table([
    ('Alter', '"Let but goodness and kindness pursue me all the days of my life. And I shall dwell in the house of the LORD for many long days."'),
    ('Geneva 1599', '"Doubtlesse kindnesse and mercie shall follow me all the dayes of my life, and I shall remaine a long season in the house of the Lord."'),
    ('JPS 1985', '"Only goodness and steadfast love shall pursue me all the days of my life, and I shall dwell in the house of the LORD for many long years."'),
    ('LXX (Brenton)', '"Thy mercy also shall follow me all the days of my life: and my dwelling shall be in the house of the Lord for a very long time."'),
    ('KJV', '"Surely goodnesse and mercie shall follow me all the dayes of my life: and I will dwell in the house of the LORD for euer."'),
]))
story.append(P(
    'The Hebrew verb is יִרְדְּפוּנִי (<i>yirdefuni</i>) — to <b>pursue, chase, hunt down</b>. '
    'Goodness and chesed are not strolling behind — they are running you down like hounds. '
    'Alter and JPS preserve this. Geneva and KJV soften to "follow." The hunt is operatively important: '
    'not passive grace, <i>grace as predator</i>. And the Hebrew never says "for ever" — it says '
    '<i>le-orekh yamim</i>, "for length of days." The KJV\'s "for euer" is a Christianized eternalization the '
    'Hebrew does not warrant.',
    'body'))

story.append(pagebreak())

story.append(P('On <i>tzalmavet</i> — what the Hebrew actually says', 'h2'))
story.append(P(
    'The pivot of the psalm is גֵּיא צַלְמָוֶת (<i>gei tzalmavet</i>) in verse 4.',
    'body'))
story.append(P(
    '<b>gei</b> (גֵּיא) — a deep ravine, gorge, gully. Same word as <i>Gei Hinnom</i> (Gehenna), the burning '
    'ravine outside Jerusalem.',
    'body_left'))
story.append(P(
    '<b>tzalmavet</b> (צַלְמָוֶת) — two readings, both ancient, both operative: '
    '(1) <b>compound:</b> <i>tzel</i> (shadow) + <i>mavet</i> (death) → "shadow-of-death"; '
    '(2) <b>re-pointing:</b> <i>tzalmut</i> — densest possible darkness, the place where light fails entirely. '
    'The word appears 17–18 times in the Tanakh, concentrated in Job, almost always paired with imagery of pure dark.',
    'body_left'))
story.append(P(
    '<b>What the Hebrew literally says:</b> "the gorge of death-shadow" or "the gorge of deepest dark." '
    'Not a metaphor for dying. A geographic and ontological location — <b>the place where light cannot reach.</b> '
    'This is the only place in all Hebrew scripture where someone <i>walks through</i> tzalmavet and is not '
    'destroyed by it. That is the operative claim of the psalm: passage through annihilating dark with the '
    'named One present.',
    'body'))

story.append(P('The pronoun shift', 'h3'))
story.append(P(
    'The psalm opens in <b>third person</b> — He makes me lie down, He leads me, He restores. '
    'At v.4, where the speaker enters the death-ravine, it shifts to <b>second person</b> — '
    'You are with me, Your rod, Your staff, You prepare, You anoint. The shift happens precisely at the '
    'moment of greatest darkness. The grammar enacts what the words describe: '
    '<i>in the bright pastures one talks about the Shepherd; in the dark gorge one talks to Him.</i> '
    'The vocative is born in the dark. All five translations preserve the shift but none flag it. '
    'It must be read aloud to be felt.',
    'body'))
story.append(P('Dual structure', 'h3'))
story.append(P(
    'Verses 1–3 are pastoral — green meadows, still waters, restored breath. '
    'Verses 5–6 are royal/cultic — table, anointing, oil, cup, house. <b>Verse 4 is the hinge.</b> '
    'The psalm is shaped as a passage from shepherd\'s pasture, through the dark cut, to the king\'s hall. '
    'Sheep at the start, anointed guest at the end. <b>The transformation happens in the dark.</b>',
    'body'))
story.append(P(
    '<b>For working purposes</b> — Geneva 1599 is closest in time to the candle-and-petition lineage as it '
    'would have been practiced by English-speaking root workers <i>before</i> the KJV displaced it. '
    'Pre-Jacobean, untouched by the political theology that shaped the KJV under James I. '
    'For the operative Hebrew read where <i>nefesh</i> is breath not soul, <i>gei tzalmavet</i> is the '
    'lightless ravine, <i>yirdefuni</i> is the hunt of grace, and <i>le-orekh yamim</i> is the length of '
    'days rather than abstract eternity — Alter and JPS together give the cleanest pre-Christianized English.',
    'body'))
story.append(pagebreak())

# ---------- PSALM 91 ----------
story.append(P('Psalm 91', 'h1'))
story.append(P('The Protection Psalm — Yoshev B\'seter Elyon', 'h2'))

story.append(P(
    'In the Hebrew Masoretic Text and modern English Bibles this is Psalm 91. In the Septuagint and the Latin '
    'Vulgate it is <b>Psalm 90</b>, because the LXX merges what the MT counts as Psalms 9 and 10. '
    'Orthodox, Catholic, and Greek sources citing "Psalm 90" mean this psalm.',
    'body'))

story.append(P('Hebrew — Verses 1–2 (the operative opening)', 'h3'))
story.append(hebrew_line('יֹשֵׁב בְּסֵתֶר עֶלְיוֹן, בְּצֵל שַׁדַּי יִתְלוֹנָן', big=True))
story.append(P('Yoshev b\'seter Elyon, b\'tzel Shaddai yitlonan.', 'translit'))
story.append(P('"He who dwells in the secret place of Elyon shall lodge in the shadow of Shaddai."', 'gloss'))
story.append(spacer(4))
story.append(hebrew_line('אֹמַר לַיהוָה מַחְסִי וּמְצוּדָתִי, אֱלֹהַי אֶבְטַח־בּוֹ', big=True))
story.append(P('Omar la-YHWH machsi u\'m\'tzudati, Elohai evtach-bo.', 'translit'))
story.append(P('"I will say of YHWH: my refuge and my fortress; my Elohim, in whom I trust."', 'gloss'))
story.append(spacer(8))
story.append(P(
    'Four distinct divine names — <b>Elyon, Shaddai, YHWH, Elohim</b> — named in sequence in the first two '
    'verses. Every English translation that renders all four as "the Lord / the Almighty / God" flattens the '
    'working. The protective architecture depends on all four being voiced.',
    'body'))
story.append(pagebreak())

story.append(P('JPS 1917 — Full Text', 'h2'))
for i, v in enumerate([
    'O thou that dwellest in the covert of the Most High, And abidest in the shadow of the Almighty;',
    'I will say of the LORD, who is my refuge and my fortress, My God, in whom I trust,',
    'That He will deliver thee from the snare of the fowler, And from the noisome pestilence.',
    'He will cover thee with His pinions, And under His wings shalt thou take refuge; His truth is a shield and a buckler.',
    'Thou shalt not be afraid of the terror by night, Nor of the arrow that flieth by day;',
    'Of the pestilence that walketh in darkness, Nor of the destruction that wasteth at noonday.',
    'A thousand may fall at thy side, And ten thousand at thy right hand; It shall not come nigh thee.',
    'Only with thine eyes shalt thou behold, And see the recompense of the wicked.',
    'For thou hast made the LORD who is my refuge, Even the Most High, thy habitation.',
    'There shall no evil befall thee, Neither shall any plague come nigh thy tent.',
    'For He will give His angels charge over thee, To keep thee in all thy ways.',
    'They shall bear thee upon their hands, Lest thou dash thy foot against a stone.',
    'Thou shalt tread upon the lion and asp; The young lion and the serpent shalt thou trample under feet.',
    '\'Because he hath set his love upon Me, therefore will I deliver him; I will set him on high, because he hath known My name.',
    'He shall call upon Me, and I will answer him; I will be with him in trouble; I will rescue him, and bring him to honour.',
    'With long life will I satisfy him, And make him to behold My salvation.\'',
], start=1):
    story.append(verse_row(i, v))
story.append(spacer(6))
story.append(P(
    'The 1985 JPS transliterates <b>Shaddai</b> rather than rendering it "Almighty" — '
    'a deliberate move toward the Hebrew that the working benefits from.',
    'small'))
story.append(pagebreak())

story.append(P('Geneva Bible 1599 — Full Text', 'h2'))
story.append(P('The Bible the Puritans and most pre-KJV English-speaking esotericists actually used. Pre-Jacobean. Lineage-faithful for Hoodoo working.', 'small'))
story.append(spacer(4))
for i, v in enumerate([
    'Who so dwelleth in the secret of the most High, shall abide in the shadow of the Almighty.',
    'I will say unto the Lord, O my hope, and my fortress: he is my God, in him will I trust.',
    'Surely he will deliver thee from the snare of the hunter, and from the noisome pestilence.',
    'He will cover thee under his wings, and thou shalt be sure under his feathers: his truth shall be thy shield and buckler.',
    'Thou shalt not be afraid of the fear of the night: nor of the arrow that flieth by day:',
    'Nor of the pestilence that walketh in the darkness: nor of the plague that destroyeth at noon day.',
    'A thousand shall fall at thy side, and ten thousand at thy right hand, but it shall not come near thee.',
    'Doubtless with thine eyes shalt thou behold and see the reward of the wicked.',
    'For thou hast said, The Lord is mine hope: thou hast set the most High for thy refuge.',
    'There shall none evil come unto thee, neither shall any plague come near thy tabernacle.',
    'For he shall give his Angels charge over thee to keep thee in all thy ways.',
    'They shall bear thee in their hands, that thou hurt not thy foot against a stone.',
    'Thou shalt walk upon the lion and asp: the young lion, and the <b>dragon</b> shalt thou tread under feet.',
    'Because he hath loved me, therefore will I deliver him: I will exalt him because he hath known my Name.',
    'He shall call upon me, and I will hear him: I will be with him in trouble: I will deliver him, and glorify him.',
    'With long life will I satisfy him, and show him my salvation.',
], start=1):
    story.append(verse_row(i, v))
story.append(spacer(6))
story.append(P(
    'Geneva keeps <b>dragon</b> at v.13 (תַּנִּין, <i>tannin</i> — the Leviathan-class chaos beast of Genesis 1:21 '
    'and Isaiah 27:1). KJV preserves it; most modern translations sanitize to "serpent" or "snake," '
    'losing the cosmic-monster resonance.',
    'small'))
story.append(pagebreak())

story.append(P('Septuagint — Psalm 90, Brenton', 'h2'))
for i, v in enumerate([
    'He that dwells in the help of the Highest, shall sojourn under the shelter of the God of heaven.',
    'He shall say to the Lord, Thou art my helper and my refuge: my God; I will hope in him.',
    'For he shall deliver thee from the snare of the hunters, from every troublesome matter.',
    'He shall overshadow thee with his shoulders, and thou shalt trust under his wings: his truth shall cover thee with a shield.',
    'Thou shalt not be afraid of terror by night; nor of the arrow flying by day;',
    'nor of the evil thing that walks in darkness; nor of calamity, and <b>the demon of noonday</b>.',
    'A thousand shall fall at thy side, and ten thousand at thy right hand; but it shall not come nigh thee.',
    'Only with thine eyes shalt thou observe and see the reward of sinners.',
    'For thou, O Lord, art my hope: thou, my soul, hast made the Most High thy refuge.',
    'No evils shall come upon thee, and no scourge shall draw nigh to thy dwelling.',
    'For he shall give his angels charge concerning thee, to keep thee in all thy ways.',
    'They shall bear thee up on their hands, lest at any time thou dash thy foot against a stone.',
    'Thou shalt tread on the <b>asp and basilisk</b>: and thou shalt trample on the <b>lion and dragon</b>.',
    'For he has hoped in me, and I will deliver him: I will protect him, because he has known my name.',
    'He shall call upon me, and I will hearken to him: I am with him in affliction; and I will deliver him, and glorify him.',
    'I will satisfy him with length of days, and shew him my salvation.',
], start=1):
    story.append(verse_row(i, v))
story.append(spacer(6))
story.append(P(
    'The Greek at v.6 — ἀπὸ συμπτώματος καὶ δαιμονίου μεσημβρινοῦ, "from mishap and the noonday demon" — '
    'is the verse the Desert Fathers built the <i>acedia</i> / midday spiritual-assault lineage on. '
    'The LXX intensifies v.13\'s menagerie into mythological creatures (basilisk, dragon) '
    'where the MT names cobra and tannin.',
    'small'))
story.append(pagebreak())

story.append(P('Robert Alter — Key Verses', 'h2'))
story.append(P('Alter preserves <b>Shaddai</b> untranslated, renders <i>m\'tzudah</i> as <b>"bastion"</b> '
               '(military-precise — a citadel, not a generic fortress), and renders <i>yitlonan</i> as '
               '<b>"lies at night"</b> — preserving the Hebrew root meaning of overnight lodging. '
               'For working purposes: the protection is specifically <i>nocturnal sheltering</i>, '
               'not generic dwelling.', 'body'))
story.append(P('Verses 1–2:', 'h3'))
story.append(P('"He who dwells in the Most High\'s shelter, in the shadow of Shaddai lies at night. '
               'I say of the Lord, \'My refuge and bastion, my God in whom I trust.\'"', 'quote'))
story.append(P('Verse 3:', 'h3'))
story.append(P('"…He will save you from the fowler\'s trap, from the destructive plague."', 'quote'))
story.append(P('Verses 5–6:', 'h3'))
story.append(P('"…the plague that stalks in the darkness, or the scourge that ravages at noon."', 'quote'))
story.append(pagebreak())

story.append(P('Word-choice divergences that affect the working', 'h2'))

t91 = [
    ['Verse', 'Hebrew', 'Smoothed', 'Closer-to-Hebrew'],
    ['1a', 'עֶלְיוֹן Elyon', '"the Most High"', 'Elyon — distinct name; El Elyon of Genesis 14 / Melchizedek'],
    ['1b', 'שַׁדַּי Shaddai', '"the Almighty"', 'Shaddai — "of the mountain," "the breasted/nurturing one," "the destroyer"; JPS 1985 and Alter transliterate'],
    ['2',  'יְהוָה YHWH', '"the LORD"', 'YHWH — the actual proper name; "LORD" in small caps marks suppression'],
    ['2',  'מַחְסִי וּמְצוּדָתִי', '"refuge and fortress"', 'Alter: "refuge and bastion" — m\'tzudah is a citadel'],
    ['3',  'מִדֶּבֶר הַוּוֹת', '"noisome pestilence"', '"the plague of destructions/calamities" — the doubling intensifies'],
    ['6',  'מִקֶּטֶב יָשׁוּד צָהֳרָיִם', '"destruction at noonday"', 'LXX: "the noonday demon." MT preserves Qeteb, a named destroying power (Deut 32:24, Hos 13:14)'],
    ['13', 'שַׁחַל וָפֶתֶן... כְּפִיר וְתַנִּין', '"lion / serpent"', 'Geneva, KJV, LXX preserve dragon for tannin — the chaos-beast'],
    ['14', 'חָשַׁק chashaq', '"set his love on me"', '"cleaved/clung passionately" — same root used for sexual longing'],
]
t = Table(t91, colWidths=[0.5*inch, 1.4*inch, 1.4*inch, 3.2*inch])
t.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 9.5),
    ('FONT', (0,1), (-1,-1), 'Serif', 9),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t)

story.append(P('The Qumran evidence', 'h3'))
story.append(P(
    '<b>11Q11</b> (Cave 11 at Qumran, "Songs Against Demons" / Apocryphal Psalms) preserves Psalm 91 in a '
    'scroll <b>explicitly labelled</b> with three other compositions as "songs of the wise" used to drive '
    'out demons. This is documentary archaeological proof that the psalm functioned as a <i>working</i> — '
    'an apotropaic ritual against demonic assault — in Second Temple Judaism, predating any Christian framing. '
    'When you light a white candle to Psalm 91, you are inside a continuous use-line at least 2,100 years old.',
    'body'))

story.append(P('Operative recommendation', 'h3'))
story.append(P(
    'Speak the Hebrew v.1–2 aloud — <i>Yoshev b\'seter Elyon, b\'tzel Shaddai yitlonan; omar la-YHWH machsi '
    'u\'m\'tzudati, Elohai evtach-bo</i> — naming the four divine names in sequence. Then proceed in '
    '<b>Geneva 1599</b> or <b>Alter</b> for the English working — both preserve the dragon at v.13 and the '
    'named entities the smoother translations strip out. Avoid modern translations that flatten Qeteb to '
    '"destruction" and tannin to "snake."',
    'body'))

story.append(pagebreak())

# ---------- PSALM 151 ----------
story.append(P('Psalm 151', 'h1'))
story.append(P('Restored from the Greek and the Dead Sea Scrolls', 'h2'))

story.append(P(
    'Canonical in the Eastern Orthodox, Ethiopian Tewahedo, Coptic, Armenian Apostolic, and Syriac churches. '
    'Dropped from the Western canon by Jerome\'s Hebraica veritas decision, confirmed by Trent (1546), '
    'reinforced by the Protestant Reformers. Vindicated by the 1956 Qumran discovery of 11QPsa, which '
    'preserves the Hebrew original as <b>two psalms</b> (151A: anointing; 151B: Goliath, fragmentary).',
    'body'))

story.append(P('Septuagint (Brenton 1851, public domain)', 'h2'))
story.append(P('Superscription: <i>"This Psalm is a genuine one of David, though supernumerary, '
               'composed when he fought in single combat with Goliad."</i>', 'small'))
story.append(spacer(4))
for i, v in enumerate([
    'I was small among my brethren, and youngest in my father\'s house: I tended my father\'s sheep.',
    'My hands formed a musical instrument, and my fingers tuned a psaltery.',
    'And who shall tell my Lord? the Lord himself, he himself hears.',
    'He sent forth his angel, and took me from my father\'s sheep, and he anointed me with the oil of his anointing.',
    'My brothers were handsome and tall; but the Lord did not take pleasure in them.',
    'I went forth to meet the Philistine; and he cursed me by his idols.',
    'But I drew his own sword, and beheaded him, and removed reproach from the children of Israel.',
], start=1):
    story.append(verse_row(i, v))

story.append(P('Hebrew Superscription (11QPsa)', 'h2'))
story.append(hebrew_line('הללויה לדויד בן ישי', big=True))
story.append(P('Halleluyah le-David ben-Yishai', 'translit'))
story.append(P('"A Hallelujah of David, son of Jesse."', 'gloss'))
story.append(P(
    'This is the only Davidic psalm in 11QPsa that opens with <i>Halleluyah</i> rather than <i>le-David</i> '
    'alone — a deliberate liturgical framing, marking the psalm as praise rather than petition.',
    'body'))

story.append(P('Psalm 151A — the Hebrew expansion (Qumran)', 'h2'))
story.append(P(
    'The 11QPsa Hebrew Psalm 151A is roughly twice the length of LXX verses 1–5 and contains material the '
    'Greek translator excised. David declares he was smaller than his brothers, the youngest son of his '
    'father, made shepherd over his father\'s flock and ruler over his father\'s young goats. He fashioned '
    'a pipe with his hands and a lyre with his fingers, and so rendered glory to YHWH. Then — the section '
    'the Greek removes — David says within himself that <b>the mountains do not witness to Him, nor do '
    'the hills proclaim Him; the trees of His words, and the flocks of His deeds, do.</b> The psalm asks: '
    '<i>who can declare and who can speak and who can recount the deeds of the Lord?</i> God has seen all, '
    'heard all, attended to all. He sent His prophet to anoint him; Samuel came to elevate him. His brothers '
    'went out to meet Samuel — fine of form, fine of appearance: the tall of stature, the handsome of hair — '
    'yet the Lord God did not choose them. Rather, He sent and took David from behind the flock, anointed him '
    'with holy oil, and set him as prince (<i>nagid</i>) to His people and ruler among the sons of His covenant.',
    'body'))

story.append(P('Psalm 151B — the Goliath fragment (Qumran)', 'h2'))
story.append(P(
    'The bottom of column XXVIII is damaged and only the opening lines survive. The superscription reads '
    'something like <i>"At the beginning of David\'s power, after the prophet of God had anointed him,"</i> '
    'and the surviving lines record David seeing the Philistine taunting from the enemy lines — the text '
    'breaks off before the combat itself. The DSS therefore preserve <b>two psalms</b> (anointing + Goliath) '
    'where the LXX preserves <b>one combined seven-verse psalm</b>.',
    'body'))
story.append(pagebreak())

# ---------- PSALMS 152-155 ----------
story.append(P('The Suppressed Five', 'h1'))
story.append(P('Psalms 152, 153, 154, 155', 'h2'))
story.append(P(
    'Four Davidic / Solomonic psalms preserved in the <b>Syriac Peshitta tradition</b> as appendices to the '
    '150-psalm Psalter and partially in the <b>Dead Sea Scrolls</b> (11QPsa, 11Q5). '
    'Two (154 and 155) survive in Hebrew from Qumran; two (152 and 153) survive only in Syriac. '
    'First identified in Western scholarship by Giuseppe Simone Assemani in 1759; standard scholarly '
    'references are James H. Charlesworth\'s <i>Old Testament Pseudepigrapha</i>, Vol. 2 (Doubleday, 1985), '
    'pp. 609–624, W. Wright\'s 1886 Syriac translation (Cambridge MS), and Geza Vermes\'s <i>The Complete '
    'Dead Sea Scrolls in English</i> (Penguin, 7th ed.).',
    'body'))
story.append(P(
    'The "suppression" is most accurately described as <b>non-preservation in the dominant Hebrew-Masoretic '
    'and Greek-Septuagint streams</b>, with continuous transmission only in the <b>Syriac East</b> and in '
    'the <b>buried Qumran library</b> that resurfaced in 1947–1956. The Qumran community — the Essenes, '
    'the lineage closest to John the Baptist and arguably the formative milieu of Yeshua\'s own movement — '
    'kept these as Psalms of David. They were inside the working Psalter of the desert sect when Yeshua '
    'was alive.',
    'body'))
story.append(pagebreak())

# Psalm 152
story.append(P('Psalm 152', 'h1'))
story.append(P('Spoken by David when he was contending with the lion and the wolf which took a sheep from his flock', 'small'))
story.append(spacer(8))
for i, v in enumerate([
    'O God, O God, come to my aid; help me, save me, and deliver my soul from the slayer.',
    'Will I go down to Sheol by the mouth of the lion? Will the wolf be the end of me?',
    'Was it not enough for those who lay in wait for my father\'s flock, and tore a sheep of my father\'s flock — must they also wish the destruction of my own soul?',
    'Have pity, O LORD, and save Your holy one from destruction, so that he may rehearse Your glories for all of his days, and may praise Your great name,',
    'when You have delivered him from the hands of the destroying lion and of the ravening wolf, and when You have rescued my captivity from the hands of the wild beasts.',
    'Quickly, my Lord, send from Yourself a deliverer, and draw me out of the gaping pit which imprisons me in its depths.',
], start=1):
    story.append(verse_row(i, v))
story.append(P('Survives only in Syriac. Likely composed in Hebrew, in the Land of Israel, during the Hellenistic period (c. 323–31 BCE).', 'small'))
story.append(pagebreak())

# Psalm 153
story.append(P('Psalm 153', 'h1'))
story.append(P('Spoken by David when returning thanks to God, who had delivered him from the lion and the wolf and he had slain both of them', 'small'))
story.append(spacer(8))
for i, v in enumerate([
    'Praise the Lord, all you nations; glorify Him and bless His name;',
    'For He delivered the soul of His Elect One from the hands of death; and He redeemed His Holy One from destruction.',
    'And He saved me from the snares of Sheol; and brought me forth from the abyss that is inscrutable.',
    'Because before my salvation could proceed from before Him, I almost became two parts by two beasts.',
    'However, He sent His angel and closed from me the gaping mouths; and redeemed my life from destruction.',
    'I myself shall praise Him and exalt Him because of all His graces, which He has provided and is providing for me.',
], start=1):
    story.append(verse_row(i, v))
story.append(P('Petition (152) and thanksgiving (153) read as a paired diptych. The angel who closes the mouths is the operative agent — the same office invoked in Psalm 91:11.', 'small'))
story.append(pagebreak())

# Psalm 154
story.append(P('Psalm 154', 'h1'))
story.append(P('A wisdom hymn personifying Wisdom as a woman — fitting the Qumran Yaḥad context as a hymn of communal eating', 'small'))
story.append(spacer(6))
story.append(P('Hebrew opening (11QPsa col. 18):', 'h3'))
story.append(hebrew_line('בקול גדול פארו אלוהים', big=True))
story.append(P('B\'qol gadol pa\'aru Elohim', 'translit'))
story.append(P('"With a loud voice glorify God"', 'gloss'))
story.append(spacer(8))
for i, v in enumerate([
    'With a loud voice glorify God; proclaim His splendor in the congregation of the many.',
    'Glorify His name in the multitude of the righteous, and celebrate His majesty with the faithful.',
    'Bind your souls to the good and to the perfect, to glorify the Most High.',
    'Assemble together to make His salvation known, and do not hesitate to make known His might and His majesty to all the simple.',
    'For it is to make known the glory of YHWH that Wisdom has been given;',
    'And it is for recounting His many deeds that she has been revealed to humans —',
    'To make His power known to the simple, to explain His greatness to those lacking understanding,',
    'Those who are far from her gates, those who have strayed from her entrances.',
    'For the Most High is the Lord of Jacob, and His majesty is upon all His works.',
    'A man who glorifies the Most High — He receives him as one who brings a meal offering,',
    'As one who offers he-goats and bullocks, as one who fattens the altar with many burnt offerings, as a sweet-smelling fragrance from the hand of the righteous.',
    'From the gates of the righteous her voice is heard, and from the assembly of the pious her song.',
    'When they eat with satiety she is cited, and when they drink in community together.',
    'Their meditation is on the Law of the Most High; their words to make known His power.',
    'How far from the wicked is her word, from all the haughty to know her.',
    'Behold, the eyes of YHWH have pity upon the good,',
    'And upon those who glorify Him He increases His mercy; from an evil time will He deliver their soul.',
    '[Bless] YHWH, who redeems the humble from the hand of strangers, [and deliv]ers the perfect from the hand of the wicked,',
    '[Estab]lishing a horn out of Ja[cob], and a judge of [peoples] out of Israel.',
    'He will spread His tent in Zion, and abide forever in Jerusalem.',
], start=1):
    story.append(verse_row(i, v))
story.append(P('Twenty verses in the Syriac. Verses 3–19 preserved in Hebrew in 11QPsa col. 18 (also fragments in 4Q448). Sanders reconstructed verses 1–2 from the Syriac.', 'small'))
story.append(pagebreak())

# Psalm 155
story.append(P('Psalm 155', 'h1'))
story.append(P('A petitionary / penitential psalm. An incomplete acrostic — bet through nun in the Qumran Hebrew; the Syriac extends the reconstruction further. Compositional kin to Psalms 3, 22, 51, and 143.', 'small'))
story.append(spacer(6))
story.append(P('Hebrew opening (11QPsa col. 24):', 'h3'))
story.append(hebrew_line('יהוה קראתיך הקשיבה אלי', big=True))
story.append(P('YHWH qara\'tikha, haqshivah elai', 'translit'))
story.append(P('"YHWH, I have called to you, attend to me"', 'gloss'))
story.append(spacer(8))
for i, v in enumerate([
    'O YHWH, I have called to You; be attentive to me.',
    'I have spread forth my palms toward Your holy dwelling; incline Your ear and grant me my petition, and do not withhold my request from me.',
    'Build up my soul and do not cast it down; and do not abandon it in the presence of the wicked.',
    'May the Judge of Truth turn the rewards of evil away from me.',
    'O YHWH, do not judge me according to my sins, for no living man is righteous in Your presence.',
    'Give me discernment, O YHWH, in Your Law, and teach me Your ordinances,',
    'So that many may hear of Your deeds, and peoples may honor Your glory.',
    'Remember me, and do not forget me, and do not lead me into things too hard for me.',
    'Cast the sin of my youth far from me, and may my transgressions not be remembered against me.',
    'Purify me, O YHWH, from the evil scourge, and let it not turn again upon me.',
    'Dry up its roots from me, and let its leaves not flourish within me.',
    'You are my glory, O YHWH; therefore my request is fulfilled before You.',
    'To whom shall I cry that he might grant to me, and the sons of men — what more can their power do?',
    'My trust, O YHWH, is before You. I cried "YHWH!" and He answered me, and He healed my broken heart.',
    'I slumbered and slept, I dreamed; indeed I awoke.',
    '[You sustained me, O YHWH]; I shall call upon YHWH my Savior.',
], start=1):
    story.append(verse_row(i, v))
story.append(P(
    'The Charlesworth/Sanders edition contains expansions with an explicit reference to <b>Belial</b>: '
    '<i>"Do not let Belial dominate me, nor an unclean spirit; let neither pain nor the evil inclination take '
    'possession of my bones"</i> — phrasing characteristic of Qumran sectarian theology, strong evidence for '
    'the psalm\'s Second Temple Jewish origin and its place in the Qumran community\'s anti-demonic liturgy. '
    '<b>155 reads as a companion to 91 in this respect</b> — a personal apotropaic, where 91 is the collective form.',
    'small'))
story.append(pagebreak())

# =========================================================
# PART II — THE WORKING MATERIALS
# =========================================================
story.append(Spacer(1, 1.2*inch))
story.append(P('PART II', 'part'))
story.append(P('The Working Materials', 'cover_sub'))
story.append(Spacer(1, 0.4*inch))
story.append(P(
    'Hebrew pronunciation for altar speech. The four divine names of Psalm 91 with their sefirotic mapping. '
    'Hoodoo working order — candles, herbs, timing. Sefer Shimush Tehillim and the 72 Names. '
    'The three operative contexts: sleep, after-funeral, journey.',
    'italic'))
story.append(pagebreak())

# Hebrew pronunciation guide
story.append(P('Hebrew Pronunciation', 'h1'))
story.append(P('Psalm 91, Verses 1–2 — for altar speech', 'h2'))

story.append(P('Verse 1', 'h3'))
story.append(hebrew_line('יֹשֵׁב בְּסֵתֶר עֶלְיוֹן בְּצֵל שַׁדַּי יִתְלוֹנָן', big=True))
story.append(P('yoh-SHEV b\'-SEH-ter el-YOHN, b\'-TZEL shah-DAI yit-loh-NAHN', 'translit'))
story.append(P('"He who dwells in the secret place of the Most High shall lodge in the shadow of the Almighty."', 'gloss'))
story.append(spacer(6))

t1 = Table([
    ['Hebrew', 'Pronounce', 'Meaning'],
    ['יֹשֵׁב', 'yoh-SHEV', 'dwelling / sitting'],
    ['בְּסֵתֶר', 'b\'-SEH-ter', 'in the secret / hidden place'],
    ['עֶלְיוֹן', 'el-YOHN', 'the Most High (divine name)'],
    ['בְּצֵל', 'b\'-TZEL', 'in the shadow (tz = ts in "cats")'],
    ['שַׁדַּי', 'shah-DAI', 'the Almighty / All-Sufficient (rhymes with "shy")'],
    ['יִתְלוֹנָן', 'yit-loh-NAHN', 'shall lodge / abide overnight'],
], colWidths=[1.2*inch, 1.5*inch, 3.5*inch])
t1.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (0,-1), 'Serif', 14),
    ('FONT', (1,1), (1,-1), 'SerifItalic', 11),
    ('FONT', (2,1), (2,-1), 'Serif', 10),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t1)

story.append(P('Verse 2', 'h3'))
story.append(hebrew_line('אֹמַר לַיהוָה מַחְסִי וּמְצוּדָתִי אֱלֹהַי אֶבְטַח־בּוֹ', big=True))
story.append(P('oh-MAR la-doh-NAI mahkh-SEE u-m\'-tzu-da-TEE, eh-loh-HAI ev-TAKH-bo', 'translit'))
story.append(P('"I will say of the LORD, my refuge and my fortress; my God, in Him I trust."', 'gloss'))
story.append(spacer(6))

t2 = Table([
    ['Hebrew', 'Pronounce', 'Meaning'],
    ['אֹמַר', 'oh-MAR', 'I will say'],
    ['לַיהוָה', 'la-doh-NAI', 'to the LORD (יהוה is spoken as Adonai)'],
    ['מַחְסִי', 'mahkh-SEE', 'my refuge (kh = soft throat-clear, like Bach)'],
    ['וּמְצוּדָתִי', 'u-m\'-tzu-da-TEE', 'and my fortress'],
    ['אֱלֹהַי', 'eh-loh-HAI', 'my God (ai = "eye")'],
    ['אֶבְטַח־בּוֹ', 'ev-TAKH-bo', 'I trust in Him'],
], colWidths=[1.2*inch, 1.5*inch, 3.5*inch])
t2.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (0,-1), 'Serif', 14),
    ('FONT', (1,1), (1,-1), 'SerifItalic', 11),
    ('FONT', (2,1), (2,-1), 'Serif', 10),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t2)

story.append(P('Pronunciation notes for an English speaker', 'h3'))
story.append(P('<b>Stress</b> in Hebrew usually falls on the <b>last syllable</b> of a word — the CAPS in the transliteration show where to lean.', 'body_left'))
story.append(P('<b>kh</b> = a soft scrape in the back of the throat, like clearing a hair. Not a hard k. If you can\'t make it, a gentle h substitutes acceptably.', 'body_left'))
story.append(P('<b>tz</b> = the "ts" sound in <i>boots</i>. One consonant cluster.', 'body_left'))
story.append(P('<b>\'</b> (apostrophe) = the sh\'va, a near-silent half-vowel — "b\'SEH-ter" is "buh-SEH-ter" said fast.', 'body_left'))
story.append(pagebreak())

# Divine Names
story.append(P('The Four Divine Names of Psalm 91', 'h1'))
story.append(P('Each carries a distinct working signature', 'small'))

tdn = Table([
    ['Name', 'Hebrew', 'Speak it', 'Working signature'],
    ['YHWH', 'יהוה', 'Adonai (ah-doh-NAI)',
     'The unutterable Name. Substitute Adonai in working speech. Visualize the four letters while speaking Adonai. Tiferet — heart of the Tree.'],
    ['Elohim', 'אֱלֹהִים', 'eh-loh-HEEM',
     'Plural of majesty; Name of judgment, structure, law. Gevurah / Binah — measured power. (In v.2: Elohai = "my God.")'],
    ['Elyon', 'עֶלְיוֹן', 'el-YOHN',
     'The Most High — the transcendent peak, that which is above. Keter (the supernal crown) or Arikh Anpin (the patient unmanifest). The shelter (seter) of Elyon is the concealed crown.'],
    ['Shaddai', 'שַׁדַּי', 'shah-DAI',
     'The Almighty / All-Sufficient. The Name on the mezuzah. Yesod — foundation, the channel through which the upper worlds enter the lower. Acronym: Shomer Daltot Yisrael — "Guardian of the Doors of Israel."'],
], colWidths=[0.7*inch, 0.9*inch, 1.4*inch, 3.5*inch])
tdn.setStyle(TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (0,-1), 'SerifBold', 10),
    ('FONT', (1,1), (1,-1), 'Serif', 16),
    ('FONT', (2,1), (2,-1), 'SerifItalic', 10),
    ('FONT', (3,1), (3,-1), 'Serif', 9.5),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(tdn)
story.append(spacer(8))

story.append(P('Why verse 2 is operationally exceptional', 'h3'))
story.append(P(
    '<i>"I will say of YHWH: He is my refuge and my fortress, my Elohim in whom I trust"</i> — '
    'the practitioner declares <b>YHWH (mercy / Tiferet)</b> and <b>Elohim (judgment / Gevurah)</b> '
    'as one name on the same breath. This is the <b>yichud</b> — the unification of Mercy and Judgment — '
    'the central act of Kabbalistic prayer.',
    'body'))
story.append(P(
    'The four Names in verses 1–2 traverse the Tree from Keter (Elyon) down through Tiferet (YHWH), '
    'Gevurah (Elohim), and Yesod (Shaddai) — <b>a complete vertical descent of the protective current.</b> '
    'The reciter is not naming God four times; the reciter is <i>wiring a circuit</i>.',
    'body'))

story.append(P('The Simple Chant for the Altar', 'h3'))
story.append(P('Repeat at the candle, three or seven times, on the slow exhale:', 'body'))
story.append(P(
    '<b>yoh-SHEV b\'-SEH-ter el-YOHN<br/>'
    'b\'-TZEL shah-DAI yit-loh-NAHN</b>',
    'quote'))
story.append(P('Two long breaths. First: "yoh-SHEV b\'SEH-ter el-YOHN" — let the el-YOHN rise. '
               'Second: "b\'TZEL shah-DAI yit-loh-NAHN" — let the yit-loh-NAHN settle.', 'body'))

story.append(P('Shorter seed-phrase (for under the breath while dressing the candle):', 'h3'))
story.append(P('<b>el-YOHN... shah-DAI...</b>', 'quote'))
story.append(P('Above, and around. The Most High calls down; the Almighty closes the circle.', 'body'))
story.append(pagebreak())

# Hoodoo working order
story.append(P('Hoodoo Working Order', 'h1'))
story.append(P('Psalms 23 + 29 + 91 in active practice', 'h2'))

story.append(P('The Canonical Triad', 'h3'))
story.append(P(
    'The documented Hoodoo pairing is actually a <b>triad</b>: <b>Psalm 91 + Psalm 29 + Psalm 23</b>, '
    'recited together to quiet a tumultuous or disorderly ghost or to drive an oppressive spirit from the house. '
    'Functional logic of the pairing:',
    'body'))
story.append(P('<b>Psalm 91</b> — the wall, the boundary, the active protection', 'body_left'))
story.append(P('<b>Psalm 23</b> — the blessing within the wall, peace and provision in the protected space', 'body_left'))
story.append(P('<b>Psalm 29</b> — the voice of the Lord that breaks the cedars — the active commanding force', 'body_left'))
story.append(P(
    'Common practitioner deployment: read <b>Psalm 91 first</b> to establish protection, then '
    '<b>Psalm 23 last</b> as the sealing blessing. Many rootworkers use this opening-and-closing structure '
    'around any working: 91 to open the perimeter, 23 to seal in the blessing.',
    'body'))

story.append(P('Psalm 91 — Documented Working Structure', 'h2'))
story.append(P(
    '<b>Holy Name (Selig):</b> El Shaddai. Pronounce or hold in mind before reciting.',
    'body_left'))
story.append(P(
    '<b>Candle:</b> White most common; purple secondary; for active household boundary, '
    'a seven-day white glass-encased candle, dressed top-down (toward you, for drawing protection in) with '
    'Protection, Fiery Wall of Protection, or "Can\'t Touch This" condition oil.',
    'body_left'))
story.append(P(
    '<b>Dressing herbs at base:</b> crushed rue, hyssop, agrimony, black salt, red brick dust '
    '(boundary and reversal). Hyssop is the canonical Biblical purification herb (Psalm 51:7).',
    'body_left'))
story.append(P(
    '<b>Petition:</b> names of household members written on brown paper, crossed by the text of '
    'Psalm 91 written crosswise over the names.',
    'body_left'))
story.append(P(
    '<b>Timing:</b> recite three times at the lighting, then once daily until the candle finishes. '
    '<b>Saturday</b> (Saturn — boundary, restriction, walls) is the traditional protection day; '
    '<b>Tuesday</b> (Mars) when the work is reversal of an active enemy attack.',
    'body_left'))
story.append(P(
    '<b>Application:</b> anoint body (crown, throat, wrists, ankles) and the four corners of the threshold '
    '(doorways, window frames) with the dressed oil while reciting verses 9–11.',
    'body_left'))

story.append(P('Psalm 91 — Verse-Specific Protections (Talmudic, Midrashic, Shimush)', 'h2'))
story.append(P('<b>vv. 1–2</b> — opening invocation, recited as entry into the protected dwelling. Inscribed at doorway lintels in some Sephardic and Eastern traditions.', 'body_left'))
story.append(P('<b>vv. 5–6</b> — the four classical demon categories (terror of night, arrow by day, deber, qetev). Recited at twilight against night-terrors and in childbirth/postpartum rooms to guard mother and infant against Lilith and her hosts.', 'body_left'))
story.append(P('<b>v. 7</b> — recited for protection in battle, physical violence, and during epidemic.', 'body_left'))
story.append(P('<b>vv. 9–10</b> — household boundary verses; written on amulets affixed to the doorpost.', 'body_left'))
story.append(P('<b>v. 11</b> — the travel-protection verse, recited before journeys. Used as the central inscription on a Kamea (k\'mia) worn around the neck while traveling.', 'body_left'))
story.append(P('<b>vv. 14–16</b> — the divine first-person promises, closing seal; recited last, often seven times.', 'body_left'))
story.append(P(
    'Widespread practice: recite verse 11 <b>three times</b> before stepping out of the house, '
    'and recite the entire Psalm <b>seven times</b> on the eve of any journey of more than a day\'s distance.',
    'body'))
story.append(pagebreak())

story.append(P('Psalm 23 — Documented Working Structure', 'h2'))
story.append(P('<b>Prosperity working:</b> anoint with olive oil mixed with bayberry oil, recite Psalm 23 for seven consecutive mornings upon rising (from Selig).', 'body_left'))
story.append(P('<b>Candle:</b> green or gold for prosperity; white for blessing/peace; light blue for marital harmony. Dress with Money Drawing, Good Fortune, or Bayberry oil.', 'body_left'))
story.append(P('<b>Job\'s Tears working (yronwode):</b> on the seventh morning, hold seven Job\'s Tears seeds in the hand, walk to running water, recite Psalm 23, and throw the seeds over the <b>left shoulder</b> into the moving water to "lay the trick."', 'body_left'))
story.append(P('<b>Dream divination:</b> recite Psalm 23 immediately before sleep, asking that the answer be given in dream.', 'body_left'))
story.append(P('<b>Travel:</b> recite Psalm 23 the morning of a journey, "against all manner of bad luck."', 'body_left'))
story.append(P('<b>Cup runneth over:</b> verse 5 ("Thou anointest my head with oil; my cup runneth over") is the line spoken aloud while dressing prosperity candles or feeding mojo bags.', 'body_left'))

story.append(P('Lineage transmission', 'h2'))
story.append(P(
    'The principal Jewish-Kabbalistic transmission line into African American conjure is '
    '<b>Godfrey Selig\'s <i>Secrets of the Psalms: A Fragment of the Practical Kabala</i></b> '
    '(Roman-Hebrew, German original 1788; English in the U.S. by Dorene Publishing late 1930s–40s). '
    'Catherine Yronwode of Lucky Mojo documents Selig as the principal line; Hoodoo Sen Moise '
    '(<i>Working Conjure</i>, Weiser 2018) emphasises the Psalms as the verbal armature of the work itself. '
    'Beneath Selig lies the medieval <b>Sefer Shimush Tehillim</b>, which assigns each Psalm a divine Name, '
    'a magical purpose, and an instruction.',
    'body'))
story.append(pagebreak())

# Shimush Tehillim
story.append(P('Sefer Shimush Tehillim and the 72 Names', 'h1'))

story.append(P(
    'The <b>Sefer Shimush Tehillim</b> ("On the Magical Uses of the Psalms") is a medieval Hebrew text '
    '(printed Italy 1551, circulating in manuscript centuries earlier — commonly dated to the Geonic period, '
    '10th–11th century, possibly earlier). Its operative principle: '
    '<i>"The entire Torah is composed of the names of God, and in consequence it has the property of saving '
    'and protecting man."</i> Each Psalm is a structured emission of the Name. The working consists of '
    'pronouncing it with intention, paired with a specific divine name and a material substrate '
    '(water, oil, parchment).',
    'body'))

story.append(P('Psalm 91 in Shimush prescription', 'h3'))
story.append(P('<b>Master psalm for:</b>', 'body_left'))
story.append(P('Protection from harmful spirits, demons (<i>mazikin</i>), and the evil eye — recited over the threshold, on amulets (<i>kameot</i>), worn on the body.', 'body_left'))
story.append(P('Protection of travelers — recited before a journey, especially at night.', 'body_left'))
story.append(P('Exorcism and the lifting of plague — paired with the names Shaddai and Elyon. <b>Dead Sea Scroll 11Q11</b> classifies Psalm 91 among the "Four Psalms Against Demons" used by the Qumran community for exorcism — placing operational use back to at least the 1st century BCE.', 'body_left'))
story.append(P('Protection of the newborn and the dying — written on parchment, placed under the pillow.', 'body_left'))
story.append(P(
    'Associated divine names: <b>Shaddai</b> (the name on the mezuzah, the protective shield-name) and '
    '<b>YHWH</b> in its full vocalization, with the angelic guardians of v.11 — '
    '<i>Michael, Gabriel, Uriel, Raphael</i> — invoked at the four cardinal points around the operator.',
    'body'))

story.append(P('The 72 Names (Shem HaMephorash)', 'h3'))
story.append(P(
    'The <b>72-letter Name</b> is constructed boustrophedonically from <b>Exodus 14:19–21</b> — three verses '
    'of exactly 72 letters each, read right-left-right, producing 72 three-letter triads. The Name Moses used '
    'to part the Red Sea. In practical Kabbalah, several triads pair with Psalm 91:',
    'body'))
story.append(P('<b>ל·ל·ה (Lelahel)</b> — name #6, healing and protection from spiritual sickness.', 'body_left'))
story.append(P('<b>כ·ל·י (Kaliel)</b> — name #19, judgment and protection from false accusation.', 'body_left'))
story.append(P('<b>מ·ל·ה (Mileh)</b> — protection in danger.', 'body_left'))
story.append(P('<b>ה·ה·ה (Hahahel)</b> — protection of the spiritual mission.', 'body_left'))
story.append(P(
    'Aryeh Kaplan treats the 72 Names as <i>meditative gateways</i> rather than incantations: '
    'the practitioner enters the Name rather than wielding it. Paired with Psalm 91, '
    'the Name is held in the mind while the Psalm is voiced — '
    'the Psalm provides the protective vessel, the Name provides the charge.',
    'body'))

story.append(P('Encoded structure: the doubled final verse', 'h3'))
story.append(P(
    'Per <i>Machzor Vitry</i> (11th c., school of Rashi), verse 16 — '
    '<i>Orech yamim asbi\'ehu, v\'arehu bishu\'ati</i> ("With length of days I will satisfy him, '
    'and show him My salvation") — is recited <b>twice</b> at the close, in Pesukei DeZimra of Shabbat and '
    'in the bedtime liturgy. The reason given: <b>the doubling completes the spelling of a Name of God.</b> '
    'The two recitations together yield the letters that finish a divine name initiated earlier — '
    'making the Psalm itself a graphic sigil that only resolves when spoken twice.',
    'body'))

story.append(P('Shir shel Pega\'im / Shir shel Nega\'im', 'h3'))
story.append(P(
    'Talmud <b>Shevu\'ot 15b</b> records Rabbi Yehoshua ben Levi calling Psalm 91 by two near-identical titles: '
    '<i>shir shel pega\'im</i> (song against demonic strikes) and <i>shir shel nega\'im</i> '
    '(song against plagues). A one-letter change (<i>pe</i> → <i>nun</i>) flips the operative field from '
    'spirits to disease — the same psalm operates on both registers because the structure underneath is identical. '
    'R. Yehoshua ben Levi would not recite it as an incantation in public, '
    '<i>lest one rely on the verse and not on God</i>, but recited it privately every night before sleep.',
    'body'))
story.append(pagebreak())

# Three operative contexts
story.append(P('Three Operative Contexts', 'h1'))
story.append(P('Sleep · After-Funeral · Journey', 'h2'))

story.append(P('Before Sleep', 'h3'))
story.append(P(
    'Sleep is, in Kabbalistic anthropology, a 1/60th experience of death — the upper soul '
    '(<i>neshamah</i>) ascends and the lower soul (<i>nefesh</i>) remains in the body, exposed. '
    'Rabbi Yehoshua ben Levi\'s nightly recitation of Psalm 91 is the source of the practice. '
    'In <b>Kriyat Shema al ha-Mitah</b> (the Bedtime Shema), Psalm 91 is the protective canopy over the '
    'sleeping body — the <i>seter Elyon</i> literally becomes the bedroom.',
    'body'))

story.append(P('After a Funeral / Accompanying the Casket', 'h3'))
story.append(P(
    'The psalm is recited <b>seven times</b> while accompanying the casket from the hearse to the grave. '
    'The seven recitations correspond to the seven <i>sefirot</i> of construction '
    '(<i>Chesed</i> through <i>Malkhut</i>) — the soul being escorted, name by name, through the seven '
    'gates of release. The Hoodoo parallel — graveyard dirt as a substance of crossing-over — sits in the '
    'same register: Psalm 91 marks the boundary between the worlds and bonds the spirit to safe passage.',
    'body'))

story.append(P('On a Journey', 'h3'))
story.append(P(
    '<i>Tefillat HaDerekh</i> (the wayfarer\'s prayer) is paired with or substituted by Psalm 91. '
    'The "way" in Kabbalistic reading is always two ways at once — the geographic road and the soul\'s road. '
    'Reciting <i>Yoshev B\'seter</i> before leaving the threshold seals the <i>seter</i> (concealed shelter) '
    'around the traveler so the road cannot reach them through the senses while they are vulnerable in motion.',
    'body'))

story.append(P('Authorship', 'h3'))
story.append(P(
    '<i>Midrash Tehillim</i> and the <i>Zohar</i> attribute Psalm 91 to <b>Moses</b>, composed either on '
    'the day he completed the Tabernacle or <b>while ascending Sinai through the cloud of the angels of '
    'destruction</b> — the protective utterance Moses voiced to pass through the wrathful host and reach the '
    'Throne. David later compiled it into the Psalter. This authorship matters operationally: the Psalm is '
    'in the lineage of the <i>one who crossed the threshold and returned</i>, which is why it is the '
    'threshold-text for sleep, death, and travel.',
    'body'))
story.append(pagebreak())

# =========================================================
# PART III — TRANSMISSION AND SUPPRESSION
# =========================================================
story.append(Spacer(1, 1.2*inch))
story.append(P('PART III', 'part'))
story.append(P('Transmission and Suppression', 'cover_sub'))
story.append(Spacer(1, 0.4*inch))
story.append(P(
    'How the texts moved Hebrew → Greek → Latin → English, what was edited at each step, '
    'and why the African and Syriac transmission lines preserved what Rome and the Reformers dropped.',
    'italic'))
story.append(pagebreak())

# Vulgate vs LXX
story.append(P('The Latin Layer', 'h1'))
story.append(P('Vulgate vs Septuagint Psalter', 'h2'))

story.append(P(
    'The single most important fact about the Western Psalter: <b>the Church did not adopt Jerome\'s '
    'translation from the Hebrew</b>. Jerome made one (the <i>Psalterium iuxta Hebraeos</i>, c. 392) — '
    'technically the most accurate Latin Psalter ever produced. The Church refused to put it in the liturgy. '
    'Instead, the Catholic West chanted, prayed, memorized, and exorcised in the <b>Psalterium Gallicanum</b> — '
    'Jerome\'s earlier revision of a Greek translation of the Hebrew, made from Origen\'s Hexaplaric '
    'Septuagint around 386 CE. The Hebrew-direct Psalter survived in a handful of Spanish manuscripts '
    'and as a scholar\'s curiosity. The Greek-mediated Psalter became the bones of Western Christendom.',
    'body'))

story.append(P('Jerome\'s three Psalters', 'h3'))
story.append(P(
    '<b>Psalterium Romanum (c. 384 CE).</b> Traditionally identified as Jerome\'s first revision of the Old '
    'Latin against the LXX. More recent scholarship holds that what we call the "Roman" Psalter is one of '
    'several mid-4th-century Old Latin recensions Jerome encountered rather than produced. It became the '
    'liturgical text of Rome itself and survived in St Peter\'s Basilica into the 20th century.',
    'body_left'))
story.append(P(
    '<b>Psalterium Gallicanum (c. 386–389 CE).</b> Jerome\'s revision of the Old Latin against Origen\'s '
    'Hexapla. A Septuagint-based text, not a Hebrew translation. Promoted by Alcuin under Charlemagne and '
    'spread through Gaul from the 9th c. <b>This is the Psalter of the Vulgate.</b>',
    'body_left'))
story.append(P(
    '<b>Psalterium iuxta Hebraeos (c. 392 CE).</b> Jerome\'s direct translation from the Hebrew. '
    'Stylistically the most precise of the three. <b>Never used liturgically.</b> Spanish manuscripts '
    'preserved it longer than the rest of the West; Alcuin\'s Carolingian standardization wiped it elsewhere.',
    'body_left'))

story.append(P('Why the Gallicanum won', 'h3'))
story.append(P('<b>1. Liturgical inertia.</b> Monks and clergy had the LXX-flavored text memorized in chant. Replacing the Psalter is replacing the prayer-bones of the daily Office. By Trent (1546) the Gallicanum had been the liturgical Psalter for seven centuries.', 'body_left'))
story.append(P('<b>2. Apostolic argument.</b> The New Testament writers quoted the Septuagint. To prefer a fresh Hebrew translation over the LXX was to imply the apostles had been quoting an inferior text. The LXX was held to be inspired translation, not mere translation.', 'body_left'))
story.append(P('<b>3. Anti-Jewish polemic disguised as method.</b> A Hebrew-direct Psalter implicitly conceded that contemporary Jewish text-tradition had something the Church lacked. Augustine\'s anxiety in Letter 71 is partly about congregational disturbance and partly about ceding interpretive ground to "the Jews."', 'body_left'))
story.append(pagebreak())

story.append(P('Augustine\'s Letter 71 — the Jonah\'s Gourd incident', 'h2'))
story.append(P(
    'Augustine, writing from Hippo in 403 CE, refused Jerome\'s Hebrew turn. He narrates: a bishop at Oea '
    '(modern Tripoli) introduced Jerome\'s new translation of Jonah. At Jonah 4:6 Jerome had rendered the '
    'Hebrew <i>qiqayon</i> as <i>hedera</i> (ivy) rather than the traditional Old Latin <i>cucurbita</i> '
    '(gourd) following the LXX. Augustine reports:',
    'body'))
story.append(P(
    '<i>"Arose such a tumult in the congregation, especially among the Greeks, correcting what had been '
    'read, and denouncing the translation as false, that the bishop was compelled to ask the testimony of '
    'the Jewish residents (it was in the town of Oea). These... gave their testimony that it was correctly '
    'rendered in the Greek Septuagint version, and in the Latin one taken from it. What further need I say? '
    'The man was compelled to correct your version in that passage as if it had been falsely translated, '
    'as he desired not to be left without a congregation."</i>',
    'quote'))
story.append(P(
    'Augustine\'s argument is not philological. It is pastoral and political: a Hebrew-based Psalter will '
    '(a) split the Latin churches from the Greek churches whose Septuagint is the apostolic text, '
    '(b) leave bishops unable to defend their lectionary against challenges they cannot evaluate, and '
    '(c) implicitly elevate contemporary Jewish reading over apostolic Greek reading.',
    'body'))
story.append(P(
    'Underneath the gourd is the structural anxiety: <b>if the Hebrew can correct the Greek at one point, '
    'it can correct it anywhere</b> — including at the Christologically loaded points the LXX had stabilized. '
    'Augustine sees this. Jerome sees this. Augustine chooses unity; Jerome chooses source. The Church chose Augustine.',
    'body'))
story.append(pagebreak())

story.append(P('Three Christologically Loaded Divergences', 'h2'))

story.append(P('Psalm 22:16 (Vulgate 21:17) — pierced vs. lion', 'h3'))
story.append(Table([
    ['Tradition', 'Text', 'English'],
    ['Hebrew (MT)', 'כָּאֲרִי יָדַי וְרַגְלָי (ka\'ari)', '"like a lion my hands and my feet"'],
    ['Hebrew (Nahal Hever DSS)', 'כארו (ka\'aru)', '"they pierced/dug"'],
    ['Greek (LXX 21:17)', 'ὤρυξαν χεῖράς μου καὶ πόδας', '"they dug my hands and feet"'],
    ['Latin Vulgate', 'foderunt manus meas et pedes meos', '"they pierced my hands and my feet"'],
], colWidths=[1.6*inch, 2.4*inch, 2.5*inch], style=TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 9.5),
    ('FONT', (0,1), (-1,-1), 'Serif', 9.5),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
])))
story.append(P(
    'The Masoretic <i>ka\'ari</i> ("like a lion") makes no grammatical sense — there is no verb. '
    'The Nahal Hever Psalms scroll (1st c. CE) reads <i>ka\'aru</i>, third-person plural perfect of '
    '<i>karah</i> ("to dig, bore through"). The LXX translators were reading a Hebrew text close to the '
    'Nahal Hever; Jerome inherited the LXX rendering through the Hexapla and passed it into the Gallicanum '
    'as <i>foderunt</i>. <b>The crucifixion-prophecy reading of Psalm 22 stands or falls on this one '
    'consonant — yod vs. waw, two strokes.</b>',
    'small'))

story.append(P('Psalm 16:10 (Vulgate 15:10) — pit vs. corruption', 'h3'))
story.append(Table([
    ['Tradition', 'Text', 'English'],
    ['Hebrew (MT)', 'לִרְאוֹת שָׁחַת (shachat)', '"to see the pit / grave"'],
    ['Greek (LXX 15:10)', 'ἰδεῖν διαφθοράν (diaphthora)', '"to see corruption"'],
    ['Latin Vulgate', 'videre corruptionem', '"to see corruption"'],
], colWidths=[1.6*inch, 2.4*inch, 2.5*inch], style=TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 9.5),
    ('FONT', (0,1), (-1,-1), 'Serif', 9.5),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
])))
story.append(P(
    'The Hebrew <i>shachat</i> means "pit, grave" — a place. The LXX translators read the same consonants '
    'as <i>shichat</i> ("destruction, corruption"). <b>Peter\'s Pentecost sermon (Acts 2:27) quotes the LXX '
    'exactly</b>, and the apostolic argument for the resurrection — David\'s body decayed, therefore the '
    'psalm cannot refer to him, therefore it must refer to the Messiah whose body did not decay — is built '
    'on the LXX reading. The Hebrew says "pit." Without the LXX reading, the apostolic proof-text dissolves. '
    'This is what Augustine was protecting when he told Jerome to leave the LXX alone.',
    'small'))

story.append(P('Psalm 110:3 — the dew vs. the begotten', 'h3'))
story.append(Table([
    ['Tradition', 'Text', 'English'],
    ['Hebrew (MT)', 'מֵרֶחֶם מִשְׁחָר לְךָ טַל יַלְדֻתֶיךָ', '"from the womb of the dawn, the dew of your youth is yours"'],
    ['Greek (LXX 109:3)', 'ἐκ γαστρὸς πρὸ ἑωσφόρου ἐξεγέννησά σε', '"from the womb before the morning-star I begot you"'],
    ['Latin Vulgate', 'ex utero ante luciferum genui te', '"from the womb before the day-star I begot you"'],
], colWidths=[1.6*inch, 2.4*inch, 2.5*inch], style=TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 9.5),
    ('FONT', (0,1), (-1,-1), 'Serif', 9.5),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
])))
story.append(P(
    'The Hebrew is a difficult royal image: the king\'s young troops gather like dewdrops at first light. '
    'The LXX restructures the consonants and reads first-person divine generation. The Vulgate hardens this '
    'into <i>genui te</i> — the same verb the Nicene Creed uses for the eternal generation of the Son. '
    'The verse the West chants as a Christmas Vespers responsory <b>is not what the Hebrew says</b>. '
    'The trinitarian metaphysics rides on the Greek-Latin reading.',
    'small'))
story.append(pagebreak())

story.append(P('Psalm Numbering — Three Streams', 'h2'))
story.append(Table([
    ['Masoretic (Hebrew)', 'Septuagint / Vulgate'],
    ['1–8', '1–8'],
    ['9–10 (two acrostics)', '9 (kept together)'],
    ['11–113', '10–112'],
    ['114–115', '113 (merged)'],
    ['116', '114 + 115 (split)'],
    ['117–146', '116–145'],
    ['147', '146 + 147 (split)'],
    ['148–150', '148–150'],
], colWidths=[2.6*inch, 2.6*inch], style=TableStyle([
    ('FONT', (0,0), (-1,0), 'SerifBold', 10),
    ('FONT', (0,1), (-1,-1), 'Serif', 10),
    ('TEXTCOLOR', (0,0), (-1,0), ACCENT),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('LINEBELOW', (0,0), (-1,0), 0.6, ACCENT),
    ('LINEBELOW', (0,1), (-1,-2), 0.2, HexColor('#d8d0c0')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
])))
story.append(spacer(8))
story.append(P(
    '<b>Eastern Orthodox</b> retains LXX numbering. When an Orthodox monk says "Psalm 50," he means the '
    '<i>Miserere</i> (MT 51). <b>Roman Catholicism</b> used Vulgate/LXX numbering in liturgical books until '
    'Vatican II; modern Catholic Bibles use Hebrew numbering with Vulgate in parentheses. '
    '<b>Protestantism</b> inherited Hebrew numbering through the Reformation return to the Masoretic text. '
    '<b>Anglicanism</b> is the hybrid: Hebrew numbering, Vulgate-derived text (Coverdale, from the Vulgate via Luther). '
    'The number is Reformed; the verse is medieval.',
    'body'))

story.append(P('Coverdale, Cranmer, and the Anglican Hybrid', 'h2'))
story.append(P(
    'Miles Coverdale\'s 1535 Psalter — the first complete printed English Bible — was not made from Hebrew. '
    'Coverdale could not read Hebrew. He worked from Luther\'s German, the Zürich Bible, the <b>Latin Vulgate</b>, '
    'and Pagninus\' Latin. Each psalm in Coverdale carries a Latin incipit drawn straight from the Vulgate. '
    'The text is materially Vulgate-flavored.',
    'body'))
story.append(P(
    'When the KJV appeared in 1611 with a fresh translation from the Hebrew, the Church of England declined '
    'to switch. The 1662 Book of Common Prayer kept Coverdale. The Episcopal Church kept Coverdale until 1979. '
    'Anglo-Catholic and traditionalist Anglican parishes still chant it. Cranmer\'s reasoning was '
    '<b>liturgical, not philological. The Coverdale Psalter sings.</b> '
    'Handel\'s <i>Messiah</i> uses Coverdale BCP, not KJV, in several places — the liturgical-musical body '
    'of Anglicanism is Vulgate-derived flesh on a Reformed skeleton.',
    'body'))

story.append(P('The Anglican-Hoodoo pipeline', 'h3'))
story.append(P(
    'The transmission into African-American Hoodoo passes through Protestant Bible culture in the American '
    'South. The working text of Southern Hoodoo is predominantly the <b>King James Version</b>, not Coverdale, '
    'not Douay-Rheims. Two routes shape practice:',
    'body'))
story.append(P(
    '<b>1. Direct KJV use</b> — especially for set-piece psalms (23 for blessing, 35 for legal cases, 37 for '
    'patience, 91 for protection, 23+91 stacked for road-opening). The KJV Psalms are a Hebrew-direct '
    'translation, but they were made in a Church-of-England matrix that had been chanting Coverdale '
    '(Vulgate-flavored) for seven decades, so the rhythm and theology are Latinate even where the lexicon is Hebrew.',
    'body_left'))
story.append(P(
    '<b>2. Selig\'s <i>Secrets of the Psalms</i></b> — Lutheran-Pietist Christian-Kabbalistic manual that '
    'prescribes specific Psalms for specific operations — recited over oil, over water, over candles. '
    'It runs the Reuchlin-Christian-Kabbalah pipeline into African-American conjure practice. '
    'Hoodoo Psalm work in Memphis, New Orleans, and the Sea Islands shows clear Selig influence by the 1940s.',
    'body_left'))
story.append(pagebreak())

# African Psalter
story.append(P('The African Psalter', 'h1'))
story.append(P('The Lineage Rome Did Not Inherit', 'h2'))

story.append(P('The Ethiopian Tewahedo Canon — 81 Books', 'h3'))
story.append(P(
    'The Ethiopian Orthodox Tewahedo Church holds the broadest biblical canon of any historically continuous '
    'Christian communion: <b>46 books in the Old Testament and 35 in the New, totaling 81.</b> '
    'Not a "Catholic Bible plus extras." A parallel transmission that never passed through Rome.',
    'body'))
story.append(P('<b>1 Enoch (Mäṣḥäfä Henok)</b> — in full, in Ge\'ez. The book Jude quotes by name (Jude 1:14-15) survived complete <i>only</i> in Ethiopian transmission. James Bruce carried three Ge\'ez manuscripts out in 1773; the Aramaic Dead Sea Scroll fragments confirmed the Ethiopian text was faithful to something the Mediterranean church had been blind to since late antiquity.', 'body_left'))
story.append(P('<b>Jubilees (Mäṣḥäfä Kufale)</b> — the 49-year-cycle retelling of Genesis–Exodus, with the alternative solar calendar.', 'body_left'))
story.append(P('<b>The three books of Mäqabyan</b> — <i>not</i> the Greek 1-2 Maccabees of the Septuagint. Entirely distinct Ethiopian compositions, narrating different figures and themes. Same name, different books.', 'body_left'))
story.append(P('<b>Mäs\'hafä Kidan (Book of the Covenant / Testamentum Domini)</b> — Christ\'s post-resurrection teaching on church order; canonical NT in Ethiopia, unknown to Rome.', 'body_left'))
story.append(P('<b>Senodos · Didascalia · Two Books of Clement</b> — collected apostolic canons and letters.', 'body_left'))

story.append(P('The Coptic Psalter', 'h3'))
story.append(P(
    'Two parallel Psalter traditions in two Coptic dialects: <b>Sahidic</b> (Upper Egypt) and <b>Bohairic</b> '
    '(Lower Egypt, still the liturgical language of the Coptic Orthodox Church). Both translated from the '
    'Septuagint — the Greek Alexandrian recension. The Coptic Psalter carries the Alexandrian text-tradition '
    'the Jewish diaspora of Egypt itself had produced.',
    'body'))
story.append(P(
    '<b>The Mudil Codex</b> (Coptic Museum Cairo, cat. 6614) is the load-bearing artifact. Discovered in '
    '1984 in a Coptic cemetery at al-Mudil, ~45 km from ancient Oxyrhynchus, placed as a <b>pillow</b> '
    'beneath the head of an adolescent girl in her grave. 498 parchment folios. Late 4th / early 5th '
    'century. <b>The oldest complete Coptic Psalter known.</b> Uniquely valuable: it descends from Greek '
    'manuscripts that <b>predate Origen\'s Hexapla</b> and the recensional corrections that reshaped the '
    'Greek text under Roman editorial pressure later. A window on what the Psalter looked like in Alexandria '
    'before the centralizing edits.',
    'body'))

story.append(P('The Ge\'ez Psalter — Mäzmurä Dawit', 'h3'))
story.append(P(
    'Densest single book in the Tewahedo liturgical life. Memorized whole by <i>dabtaras</i> and clergy:',
    'body'))
story.append(P('<b>151 Psalms</b> as canonical proper — Psalm 151 sits as canon, not as appendix. Emperor Haile Selassie I opened his first address to the Council of State by reciting Psalm 151 in full.', 'body_left'))
story.append(P('<b>15 Biblical Canticles</b> (Moses, Miriam, Hannah, Habakkuk, the Magnificat, the Benedictus, the Nunc Dimittis, etc.)', 'body_left'))
story.append(P('<b>Mahaleyä Mahalay (Song of Songs)</b>', 'body_left'))
story.append(P('<b>Wedasse Maryam (Praise of Mary)</b> — a Marian psalter organized by the seven days of the week.', 'body_left'))
story.append(P('<b>Anqäṣä Berhan (Gate of Light)</b> — a second appended Marian psalter.', 'body_left'))
story.append(pagebreak())

story.append(P('The North African Fathers', 'h3'))
story.append(P(
    'The systematizers of Christian doctrine were African before they were anything else:',
    'body'))
story.append(P('<b>Origen</b> (Alexandria, c. 185–253) — first systematic Christian theologian; the Hexapla, the De Principiis.', 'body_left'))
story.append(P('<b>Clement of Alexandria</b> (c. 150–215) — Stromateis; synthesis with Hellenistic philosophy.', 'body_left'))
story.append(P('<b>Athanasius</b> (Alexandria, c. 296–373) — Nicene Christology, and the 39th Festal Letter of 367 CE: the earliest document anywhere listing the 27 books of the New Testament as we now have them. <b>An Egyptian Coptic bishop. Not a Roman pope.</b>', 'body_left'))
story.append(P('<b>Cyril of Alexandria</b> (c. 376–444) — Christology that gave us the Theotokos formula at Ephesus.', 'body_left'))
story.append(P('<b>Tertullian</b> (Carthage, c. 155–220) — first major Latin Christian writer; coined the Latin word <i>trinitas</i>. <b>Latin Christian theology begins in Africa.</b>', 'body_left'))
story.append(P('<b>Cyprian</b> (Carthage, c. 200–258) — ecclesiology, episcopal unity.', 'body_left'))
story.append(P('<b>Augustine</b> (Hippo Regius, modern Algeria, 354–430) — the most influential theologian in Western Christianity, full stop. African.', 'body_left'))

story.append(P('The Garima Gospels — Africa\'s Documentary Receipt', 'h3'))
story.append(P(
    'Two Ge\'ez gospel codices preserved at the Abba Garima monastery in Tigray, northern Ethiopia. '
    '<b>Radiocarbon dating at Oxford placed Garima 2 at approximately 390–570 CE and Garima 1 at '
    'approximately 530–660 CE.</b> Before this testing, Western scholars assumed they were medieval (~900 '
    'years old). The actual dates make them <b>contemporary with or older than Codex Sinaiticus and Codex '
    'Vaticanus.</b> Garima 2 is a candidate for the <b>earliest surviving complete illuminated Christian '
    'manuscript on earth</b> — with evangelist portraits, canon tables, decorated headpieces. African '
    'Christians were producing fully illustrated bound Gospel books before the Lindisfarne Gospels were '
    'conceived — by at least 200 years.',
    'body'))

story.append(P('Beta Israel — The Ethiopian Jewish Psalter', 'h3'))
story.append(P(
    'The <b>Beta Israel</b> ("House of Israel") are the Jewish community of northern Ethiopia. Their tradition '
    'traces lineage to the Solomonic line through Menelik I, son of the Queen of Sheba — a continuous Jewish '
    'identity in the Horn of Africa <b>that did not pass through the rabbinic Mishnaic synthesis</b> of the '
    'Mediterranean diaspora. No Talmud. A pre-rabbinic, Second-Temple-era Judaism. Sacred text: the <b>Orit</b> — '
    'an Octateuch (Torah + Joshua, Judges, Ruth) — read liturgically in Ge\'ez, not Hebrew. The community '
    'preserves practices including <i>seged</i>, ritual purity, and the use of sacred recitation for '
    'protection. <b>The protective use of Psalm 91 and the road-opening function of Psalm 23 in Black '
    'diaspora rootwork has a structural cousin in the Ethiopian Jewish protective psalter tradition</b> — '
    'both inherit from a Second-Temple Semitic stratum where psalms were operative, not merely devotional.',
    'body'))

story.append(P('Implications for the Practitioner', 'h3'))
story.append(P(
    'When a Black diaspora rootworker opens to Psalm 23 for road-opening, or Psalm 91 for shielding, '
    'the textual lineage of that Psalter runs: Hebrew Second-Temple liturgy → Alexandrian Greek Septuagint '
    '(produced by Jews <b>in Africa</b>) → Coptic Sahidic/Bohairic Psalter (Africans translating the Africans) '
    '→ Ge\'ez Mäzmurä Dawit and the unbroken Tewahedo chain → the Christian textual stream that arrived in '
    'West Africa centuries before the Atlantic slave trade → the Bible the enslaved received in the Americas '
    'and re-coded as operative spellwork. The KJV in plantation contexts is the <b>latest</b> link in that '
    'chain, not the source.',
    'body'))
story.append(P(
    '<b>Ethiopian retention of 1 Enoch</b> matters for any practitioner working with the Watchers, angelic '
    'taxonomy, the cosmology of the Sons of God and the Daughters of Men. The text Jude trusted as Scripture '
    'survived only because African monks copied it for a thousand years while Europe forgot. The angelological '
    'substrate of grimoiric Hermetism is downstream of Ethiopian preservation.',
    'body'))
story.append(P(
    '<b>The Coptic preservation of the Nag Hammadi library</b> (1945, Upper Egypt — Coptic codices buried by '
    'monks of Pachomius\'s monastic federation around the time of Athanasius\'s 39th Festal Letter): the '
    'entire Western recovery of Sethian, Valentinian, and Thomasine Christianity was made possible because '
    'Egyptian Christians refused to burn what their bishop told them to burn. The Hermetic corpus you draw '
    'on for the <i>as above, so below</i> axiom survived in the same Coptic monastic ecology that preserved '
    'the Sahidic Psalter.',
    'body'))
story.append(P(
    '<i>Rome inherited. Africa transmitted. The working continues.</i>',
    'italic'))
story.append(pagebreak())

# =========================================================
# PART IV — THE FULL ALTAR ORDER
# =========================================================
story.append(Spacer(1, 1.2*inch))
story.append(P('PART IV', 'part'))
story.append(P('The Full Altar Order', 'cover_sub'))
story.append(Spacer(1, 0.4*inch))
story.append(P('A working liturgy drawing the whole stack together — Hebrew opening, English body, '
               'sealing close. Operator names the Source. The candle burns.', 'italic'))
story.append(pagebreak())

story.append(P('A Working Liturgy', 'h1'))
story.append(P('For the lighting of a white candle for protection, with Psalm 91 as the working text', 'h2'))

story.append(P('1. Threshold', 'h3'))
story.append(P('Wash the hands. Light the candle. Stand or sit facing the altar.', 'body'))

story.append(P('2. Naming the Source', 'h3'))
story.append(P(
    '<i>"In the name of the Most High <b>Elyon</b>, of <b>Yeshua</b> the Anointed, '
    'and of the <b>Ruach HaKodesh</b> — the Holy Breath, Sophia — the living current that moves through '
    'this working."</i>',
    'quote'))

story.append(P('3. The Hebrew Opening — Psalm 91, verses 1–2', 'h3'))
story.append(hebrew_line('יֹשֵׁב בְּסֵתֶר עֶלְיוֹן בְּצֵל שַׁדַּי יִתְלוֹנָן', big=True))
story.append(P('yoh-SHEV b\'-SEH-ter el-YOHN, b\'-TZEL shah-DAI yit-loh-NAHN', 'translit'))
story.append(spacer(2))
story.append(hebrew_line('אֹמַר לַיהוָה מַחְסִי וּמְצוּדָתִי אֱלֹהַי אֶבְטַח־בּוֹ', big=True))
story.append(P('oh-MAR la-doh-NAI mahkh-SEE u-m\'-tzu-da-TEE, eh-loh-HAI ev-TAKH-bo', 'translit'))
story.append(P('Two long breaths. Four names spoken: Elyon, Shaddai, YHWH (as Adonai), Elohai.', 'small'))

story.append(P('4. The English Body — Psalm 91, Geneva 1599', 'h3'))
story.append(P('Read aloud, slowly. Hand on the petition paper at v.7. Anoint the four corners at v.11.', 'body'))

story.append(P('5. The Petition', 'h3'))
story.append(P(
    'Speak the working sentence aloud, naming the persons, the household, the boundary, the outcome. '
    'Match the wording to the work — protection, road-opening, sustenance, banishing.',
    'body'))

story.append(P('6. The Sealing Blessing — Psalm 23, Geneva 1599', 'h3'))
story.append(P('Read aloud. At v.4 the pronoun shifts from "He" to "You" — let the voice meet it. '
               'At v.5 ("Thou doest anoynt mine head with oyle"), anoint the crown.', 'body'))

story.append(P('7. The Doubled Close — Psalm 91, verse 16', 'h3'))
story.append(P(
    '<i>"With long life will I satisfy him, and show him my salvation."</i> '
    'Speak it <b>twice</b>. Per Machzor Vitry, the doubling completes a hidden Name of God.',
    'quote'))

story.append(P('8. Release', 'h3'))
story.append(P('Bow the head. Let the candle burn. Step away. Trust the working.', 'body'))

story.append(spacer(16))
story.append(P('Variants', 'h2'))
story.append(P('<b>For the triad working</b> (quieting a disorderly spirit): add Psalm 29 between Psalm 91 and Psalm 23 — the voice of the Lord that breaks the cedars, the commanding force.', 'body_left'))
story.append(P('<b>For a journey:</b> recite Psalm 91 v.11 three times before stepping out the door; recite the entire Psalm seven times on the eve of a journey of more than a day\'s distance.', 'body_left'))
story.append(P('<b>For sleep:</b> recite Psalm 91 once at the bedside before the Bedtime Shema. The Kabbalists teach the seter Elyon literally becomes the bedroom.', 'body_left'))
story.append(P('<b>For accompanying the dead:</b> recite Psalm 91 seven times, one for each sefirah of construction (Chesed through Malkhut), escorting the spirit through the gates of release.', 'body_left'))
story.append(P('<b>For a Belial-binding</b> (active spiritual assault): use Psalm 155 with the Charlesworth/Sanders expansions, in addition to Psalm 91. The Qumran community paired them.', 'body_left'))
story.append(pagebreak())

# Sources / Bibliography
story.append(P('Sources and Bibliography', 'h1'))

story.append(P('Primary texts and editions', 'h2'))
story.append(P('Robert Alter, <i>The Hebrew Bible: A Translation with Commentary</i> (W. W. Norton, 2018–19). Standalone <i>Book of Psalms</i> (Norton, 2007).', 'source'))
story.append(P('JPS Tanakh 1985 (Jewish Publication Society); JPS 1917 (public domain).', 'source'))
story.append(P('The Geneva Bible 1599 (pre-Jacobean English; available facsimile via Internet Archive).', 'source'))
story.append(P('Brenton\'s Septuagint (1851, public domain) — ebible.org/eng-Brenton/.', 'source'))
story.append(P('NETS — A New English Translation of the Septuagint (Pietersma & Wright, Oxford 2007/2009) — ccat.sas.upenn.edu/nets/.', 'source'))
story.append(P('Authorized King James Version 1611.', 'source'))
story.append(P('Latin Vulgate (Clementine and Stuttgartensia editions); Coverdale Psalter (1535, Book of Common Prayer).', 'source'))

story.append(P('Hebrew sources', 'h2'))
story.append(P('Chabad.org — Tehillim Chapter 91 (Hebrew with niqqud + English). chabad.org/library/bible_cdo/aid/16312/', 'source'))
story.append(P('Sefaria — Psalms 91, 23, 154, etc. (Hebrew + multiple English translations, Rashi, Ibn Ezra, Radak, Targum). sefaria.org/Psalms.91', 'source'))
story.append(P('Mechon-Mamre — Psalms 91, Hebrew/English. mechon-mamre.org/p/pt/pt2691.htm', 'source'))
story.append(P('Bible Hub — Hebrew interlinear with Strong\'s and lexical analysis.', 'source'))

story.append(P('Dead Sea Scrolls', 'h2'))
story.append(P('Leon Levy Dead Sea Scrolls Digital Library (Israel Antiquities Authority). deadseascrolls.org.il', 'source'))
story.append(P('James A. Sanders, <i>The Psalms Scroll of Qumrân Cave 11 (11QPsa)</i> — DJD IV (Oxford: Clarendon, 1965).', 'source'))
story.append(P('Geza Vermes, <i>The Complete Dead Sea Scrolls in English</i> (Penguin Classics, 7th ed.).', 'source'))
story.append(P('James H. Charlesworth (ed.), <i>The Old Testament Pseudepigrapha</i>, Vol. 2 (Doubleday, 1985), pp. 609–624 — Charlesworth & Sanders, "More Psalms of David."', 'source'))
story.append(P('11Q11 (Apocryphal Psalms) — the "Four Songs Against Demons" scroll including Psalm 91. dssenglishbible.com/scroll11Q11.htm', 'source'))

story.append(P('Syriac apocryphal Psalms (152–155)', 'h2'))
story.append(P('W. Wright, <i>Some Apocryphal Psalms in Syriac</i> (1886), Proceedings of the Society of Biblical Archaeology vol. 9.', 'source'))
story.append(P('Gorgias Encyclopedic Dictionary of the Syriac Heritage — Psalms, Syriac Apocryphal. gedsh.bethmardutho.org', 'source'))

story.append(P('Kabbalistic and Hoodoo lineage', 'h2'))
story.append(P('Sefer Shimush Tehillim — Mohr Siebeck critical edition (Rebiger).', 'source'))
story.append(P('Godfrey Selig, <i>Secrets of the Psalms</i> (German 1788; English Dorene 1930s-40s). Full text scan: archive.org/details/godfrey-selig-secrets-of-the-psalms', 'source'))
story.append(P('Catherine Yronwode, <i>"Secrets of the Psalms": The Kabbalist Influence on Hoodoo</i>. luckymojo.com/secretspsalms.html', 'source'))
story.append(P('Catherine Yronwode and Mikhail Strabo, <i>The Art of Hoodoo Candle Magic</i>. luckymojo.com/theartofhoodoocandlemagic.html', 'source'))
story.append(P('Hoodoo Sen Moise, <i>Working Conjure: A Guide to Hoodoo Folk Magic</i> (Weiser, 2018).', 'source'))
story.append(P('Aryeh Kaplan, <i>Meditation and Kabbalah</i> (1982). archive.org/details/meditationkabbal0000kapl', 'source'))
story.append(P('Joshua Trachtenberg, <i>Jewish Magic and Superstition</i> (1939). sacred-texts.com/jud/jms/', 'source'))
story.append(P('Daniel C. Matt (tr.), <i>The Zohar: Pritzker Edition</i> (Stanford UP).', 'source'))

story.append(P('Translation politics and history', 'h2'))
story.append(P('Adam Kamesar, <i>Jerome, Greek Scholarship, and the Hebrew Bible</i> (Oxford: Clarendon, 1993).', 'source'))
story.append(P('Megan Hale Williams, <i>The Monk and the Book: Jerome and the Making of Christian Scholarship</i> (Chicago, 2006).', 'source'))
story.append(P('Mogens Müller, <i>The First Bible of the Church: A Plea for the Septuagint</i> (Sheffield, 1996).', 'source'))
story.append(P('Pierre-Maurice Bogaert — manuscript-history work on the Vulgate (<i>Revue Bénédictine</i> studies).', 'source'))
story.append(P('Augustine, <i>Letter 71</i> and <i>Letter 75</i> (to Jerome). newadvent.org/fathers/1102071.htm', 'source'))

story.append(P('African and Ethiopian sources', 'h2'))
story.append(P('Ethiopian Orthodox Tewahedo Church official canon. ethiopianorthodox.org/english/canonical/books.html', 'source'))
story.append(P('Anke Wanger, <i>The Biblical Canon of the EOTC</i> (EUCLID, scholarly survey).', 'source'))
story.append(P('Thomas C. Oden, <i>How Africa Shaped the Christian Mind</i> (IVP, 2007).', 'source'))
story.append(P('John S. Mbiti, <i>African Religions and Philosophy</i> (Heinemann, 1969).', 'source'))
story.append(P('Brent Nongbri, "The Mudil Psalter" (2024). brentnongbri.com/2024/03/31/the-mudil-psalter/', 'source'))
story.append(P('Coptic Old Testament Project, Göttingen Academy.', 'source'))
story.append(P('Ethiopian Heritage Fund — Garima Gospels project. ethiopianheritagefund.org', 'source'))
story.append(P('Athanasius, <i>39th Festal Letter</i> (367 CE). newadvent.org/fathers/2806039.htm', 'source'))

story.append(P('Talmudic, Midrashic, and lineage-Jewish', 'h2'))
story.append(P('Talmud, Shevu\'ot 15b — Shir shel Pega\'im / Nega\'im.', 'source'))
story.append(P('Midrash Tehillim 91. sefaria.org/Midrash_Tehillim.91', 'source'))
story.append(P('Rashi on Psalms 91. sefaria.org/Rashi_on_Psalms.91.1', 'source'))
story.append(P('Targum to Psalms.', 'source'))
story.append(P('Yeshivat Har Etzion, <i>Tehillim 91 — A Song of Afflictions</i>. etzion.org.il', 'source'))

story.append(P('Hoodoo Psalm working references', 'h2'))
story.append(P('Jesterbear — <i>Psalms and Verses in Hoodoo</i>. jesterbear.com/Hoodoo/PsalmsVerses.html', 'source'))
story.append(P('Living Talismans — <i>Shimmush Tehillim: The Jewish Magical Use of the Psalms</i>. livingtalismans.com/shimmush-tehillim-the-jewish-magical-use-of-the-psalms/', 'source'))
story.append(P('Rich Bitch Conjure — <i>The Power of Psalms in Hoodoo</i>. richbitchconjure.com', 'source'))
story.append(P('Original Botanica — <i>Hoodoo in the Psalms</i>. originalbotanica.com/hoodoo-in-the-psalms', 'source'))
story.append(spacer(20))

story.append(P('Colophon', 'h2'))
story.append(P(
    'Compiled from a ten-agent deep research deployment for Jordan Ross Atkins / Numen, Atlanta GA, '
    'in the first days of June 2026 — the month of Mercury\'s shadow, the year of Saturn-Neptune-conjunct '
    'in Aries, Personal Year 1 for the operator, with the active 8 Pinnacle just opened. '
    'Typeset in FreeSerif. Layout in ReportLab. Released to the working.',
    'small'))
story.append(P(
    '<i>The truth was here all along, scattered through the lineage. '
    'What was needed was the discernment to gather it without distortion.</i>',
    'italic'))

# ---- Build ----
import os
out = '/home/user/numenist-site/altar-psalms-bible/altar-psalms-bible.pdf'
os.makedirs(os.path.dirname(out), exist_ok=True)
doc = PsalmsDoc(out, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                topMargin=MARGIN, bottomMargin=MARGIN, title='The Altar Psalms Bible',
                author='Jordan Ross Atkins / Numen')
doc.build(story)
print(f'Built: {out}')
print(f'Size: {os.path.getsize(out)} bytes')
