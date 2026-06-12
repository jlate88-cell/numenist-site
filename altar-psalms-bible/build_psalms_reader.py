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

Structure note (v2): Daily Reading moved to the front (Parts I and II);
Pronunciation Guide moved to Part III as reference. The operator opens
the book on the practice they actually do every day. Psalm 118:6-9
added to the Altar Ritual as the sovereignty seal between Psalm 23
and the petition — refuses fear-of-man and pull of human authority
before the petition is stated.

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
    PageTemplate, Frame
)
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
    'italic':        s('italic', fontName='SerifItalic', spaceAfter=6),
    'quote':         s('quote', leftIndent=20, rightIndent=10, fontName='SerifItalic', spaceAfter=6),
    'verse':         s('verse', leftIndent=14, fontSize=11.5, leading=16.5, spaceAfter=4),
    'speak':         s('speak', leftIndent=14, fontSize=12, leading=17, spaceAfter=5),
    'hebrew':        s('hebrew', fontSize=15, leading=22, alignment=TA_RIGHT, spaceAfter=3),
    'translit':      s('translit', fontName='SerifBoldItalic', fontSize=11, leading=15, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=3),
    'gloss':         s('gloss', fontSize=10, leading=13, alignment=TA_CENTER, textColor=SUB, spaceAfter=8),
    'step':          s('step', fontSize=11.5, leading=16, leftIndent=10, spaceAfter=6),
    'greenbox':      s('greenbox', fontSize=10, leading=13.5, textColor=GREEN, leftIndent=10, spaceAfter=4),
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
    '(lord/master). Hosea 2:16 itself records Source saying: <i>"You will call Me Ishi, and no '
    'more will you call Me Baali"</i> (verified against the Hebrew at Sefaria). Chaldean: '
    'LORD = 16/7 — the Tower, a karmic-debt number. MONAD = 21/3 — the World, the completion '
    'arcana, the same 21 carried by YESHUA and ELYON. The substitution moves the spoken text '
    'from the Tower vibration to the World vibration.',
    'body'))
story.append(P('Every substitution point in this book, so you can audit:', 'h3'))
story.append(P('· Psalm 91 — verses 2 and 9', 'body_left'))
story.append(P('· Psalm 23 — verses 1 and 6', 'body_left'))
story.append(P('· Psalm 118 — verses 6, 7, 8, and 9 (all four)', 'body_left'))
story.append(P('· Psalm 151 — verse 3 (twice) and verse 5', 'body_left'))
story.append(P('· Psalm 152 — verses 4 and 6', 'body_left'))
story.append(P('· Psalm 153 — verse 1', 'body_left'))
story.append(P('· Psalm 154 — verse 9', 'body_left'))
story.append(P(
    'Fifteen instances total. Every other word of the source texts is unchanged.',
    'small'))
story.append(pagebreak())

# ============================ PART I — EVERYDAY ============================
story.append(P('PART I', 'part'))
story.append(P('The Everyday Reading', 'cover_sub'))
story.append(P('On rising. No candle. Two to three minutes.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Everyday Order', 'h1'))
story.append(P(
    'This is for the morning you just want to say the Psalms and start the day right — no altar, '
    'no candle, no ritual. The documented on-rising practice (Selig) is <b>Psalm 23 spoken on '
    'waking</b>. The documented going-out practice is <b>Psalm 91 verse 11 spoken three times '
    'before stepping out of the house</b>. That is the whole everyday order:',
    'body'))
story.append(spacer(4))
story.append(P('<b>1.</b> Sit up. One slow breath in, one slow breath out.', 'step'))
story.append(P('<b>2.</b> Speak <b>Psalm 23</b> aloud (text below).', 'step'))
story.append(P('<b>3.</b> One line of gratitude in your own words. <i>"Thank you for this day."</i> Done.', 'step'))
story.append(P('<b>4.</b> At the door, before you leave: <b>Psalm 91 verse 11, three times</b> (text below).', 'step'))
story.append(spacer(8))

story.append(P('Psalm 23 — the everyday text', 'h2'))
story.append(P('Geneva 1599, with the Monad Rule at verses 1 and 6.', 'small'))
story.append(spacer(4))
story.append(P('<i>A Psalme of David.</i>', 'quote'))
story.append(vr(1, 'The <b>Monad</b> is my shepheard, I shall not want.'))
story.append(vr(2, 'He maketh me to rest in greene pasture, and leadeth me by the still waters.'))
story.append(vr(3, 'He restoreth my soule, and leadeth me in the paths of righteousnesse for his Names sake.'))
story.append(vr(4, 'Yea, though I should walke through the valley of the shadowe of death, I will feare no euill: for thou art with me: thy rod and thy staffe, they comfort me.'))
story.append(vr(5, 'Thou doest prepare a table before me in the sight of mine aduersaries: thou doest anoynt mine head with oyle, and my cuppe runneth ouer.'))
story.append(vr(6, 'Doubtlesse kindnesse and mercie shall follow me all the dayes of my life, and I shall remaine a long season in the house of the <b>Monad</b>.'))
story.append(spacer(6))
story.append(P('At verse 4 the voice shifts from "He" to "Thou" — let your voice meet it. In the everyday reading you do not need the crown-touch; that belongs to the altar.', 'small'))
story.append(spacer(8))

story.append(P('The door verse — Psalm 91:11, three times', 'h2'))
story.append(vr(11, 'For hee shall giue his Angels charge ouer thee to keepe thee in all thy wayes.'))
story.append(P('Say it three times, step out, go live the day.', 'small'))
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
story.append(P('<b>1. The Hermetic cross on the body.</b> Forehead → heart → right shoulder → left shoulder → back to heart. One slow breath through the whole gesture. Forehead is Source-above; heart is the body\'s altar; right is structure; left is flow; the return to heart seals it.', 'step'))
story.append(P('<b>2. The lineage formula, aloud:</b> <i>"In the name of the Father, the Son, and the Holy Spirit."</i> You are invoking the Source behind those words — the Monad — through the formula your ancestors carried.', 'step'))
story.append(P('<b>3. Psalm 91, aloud</b> — the perimeter (full text next page). If you want the Hebrew opening first: <i>yoh-SHEV buh-SEH-ter el-YOHN, buh-TZEL shah-DYE yit-loh-NAHN.</i>', 'step'))
story.append(P('<b>4. Psalm 23, aloud</b> — the seal of provision and path (text follows the Psalm 91 text). At verse 5, touch the crown of your head at "anoynt mine head with oyle." Let "my cuppe runneth ouer" be one slow breath.', 'step'))
story.append(P('<b>5. Psalm 118:6-9, aloud</b> — the sovereignty seal (text follows). Four short verses. They refuse fear-of-man and the pull of human authority before the petition is stated. The petition then goes out from a sovereign place, not from a fear-of-man place.', 'step'))
story.append(P('<b>6. The petition, aloud.</b> First person, present tense, brief. What you are drawing in.', 'step'))
story.append(P('<b>7. Light the candle</b> (or continue the standing burn).', 'step'))
story.append(P('<b>8. Sit with it.</b> One slow breath minimum; seven if you have the time.', 'step'))
story.append(P('<b>9. Gratitude, aloud:</b> <i>"Thank you for this day. Thank you for this provision. Thank you for this protection. Thank you that the work is already moving."</i>', 'step'))
story.append(P('<b>10. When you put it out — snuff, never blow.</b> Pinch the wick or use a snuffer. As you snuff: <i>"The working continues. Thank you."</i> The breath that spoke the petition must not be the breath that scatters the flame.', 'step'))
story.append(pagebreak())

story.append(P('Psalm 91 — the altar text', 'h2'))
story.append(P('Geneva 1599, with the Monad Rule at verses 2 and 9.', 'small'))
story.append(spacer(4))
story.append(vr(1, 'Who so dwelleth in the secrete of the most High, shall abide in the shadowe of the Almightie.'))
story.append(vr(2, 'I will say vnto the <b>Monad</b>, O mine hope, and my fortresse: he is my God, in him will I trust.'))
story.append(vr(3, 'Surely he will deliuer thee from the snare of the hunter, and from the noysome pestilence.'))
story.append(vr(4, 'Hee will couer thee vnder his winges, and thou shalt be sure vnder his feathers: his trueth shall be thy shielde and buckler.'))
story.append(vr(5, 'Thou shalt not be afraide of the feare of the night, nor of the arrowe that flyeth by day:'))
story.append(vr(6, 'Nor of the pestilence that walketh in the darkenesse: nor of the plague that destroyeth at noone day.'))
story.append(vr(7, 'A thousand shall fall at thy side, and tenne thousand at thy right hand, but it shall not come neere thee.'))
story.append(vr(8, 'Doubtlesse with thine eyes shalt thou beholde and see the reward of the wicked.'))
story.append(vr(9, 'For thou hast said, The <b>Monad</b> is mine hope: thou hast set the most High for thy refuge.'))
story.append(vr(10, 'There shall none euill come vnto thee, neither shall any plague come neere thy tabernacle.'))
story.append(vr(11, 'For hee shall giue his Angels charge ouer thee to keepe thee in all thy wayes.'))
story.append(vr(12, 'They shall beare thee in their handes, that thou hurt not thy foote against a stone.'))
story.append(vr(13, 'Thou shalt walke vpon the lyon and aspe: the yong lyon and the dragon shalt thou treade vnder feete.'))
story.append(vr(14, 'Because he hath loued me, therefore will I deliuer him: I will exalt him because hee hath knowen my Name.'))
story.append(vr(15, 'He shall call vpon me, and I wil heare him: I will be with him in trouble: I will deliuer him, and glorifie him.'))
story.append(vr(16, 'With long life wil I satisfie him, and shew him my saluation.'))
story.append(spacer(6))
story.append(P('The voice changes twice: verses 1–2 are you speaking; verses 3–13 are the blessing spoken over you; verses 14–16 are Source speaking back. Slow down at 14–16 — that is the seal.', 'small'))
story.append(pagebreak())

story.append(P('Psalm 23 — the altar seal of provision', 'h2'))
story.append(P('Same text as Part I (Everyday). Speak it after Psalm 91. At verse 5: touch the crown of your head at "anoynt mine head with oyle"; let "my cuppe runneth ouer" be the slow breath that meets the petition. Then move to Psalm 118:6-9 below before stating the petition.', 'body'))
story.append(spacer(10))

# ---- NEW: Psalm 118:6-9 — the sovereignty seal ----
story.append(P('Psalm 118:6-9 — the sovereignty seal', 'h2'))
story.append(P(
    'Geneva 1599 (verified against BibleGateway GNV this session; orthography harmonized to '
    'the book\'s 1599 style). The Monad Rule applies at all four verses. Speak after Psalm 23, '
    'before the petition.',
    'small'))
story.append(spacer(4))
story.append(vr(6, 'The <b>Monad</b> is with me: therefore I will not feare what man can do vnto me.'))
story.append(vr(7, 'The <b>Monad</b> is with me among them that helpe me: therefore shall I see my desire vpon mine enemies.'))
story.append(vr(8, 'It is better to trust in the <b>Monad</b>, then to haue confidence in man.'))
story.append(vr(9, 'It is better to trust in the <b>Monad</b>, then to haue confidence in princes.'))
story.append(spacer(6))
story.append(P('Function and lineage', 'h3'))
story.append(P(
    'Psalm 118 is the closing psalm of the Hallel sequence (Pss 113–118) recited in Jewish '
    'liturgy on the festivals. Verses 6–9 are the sovereignty declaration: aligned with Source, '
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
    'interference; the petition then goes out from full Source-alignment.',
    'greenbox'))
story.append(pagebreak())

# ============================ PART III — PRONUNCIATION ============================
story.append(P('PART III', 'part'))
story.append(P('Pronunciation Guide', 'cover_sub'))
story.append(P('The old spellings, the Hebrew, and the Names — sounded out.', 'cover_line'))
story.append(pagebreak())

story.append(P('The One Rule for the Old Spelling', 'h1'))
story.append(P(
    'The Geneva 1599 text looks strange but it is pronounced exactly like the words you already '
    'know. The old printers used three habits: <b>u and v swap places</b> (euill = evil, vnder = '
    'under, deliuer = deliver), <b>extra silent letters</b> (greene = green, walke = walk, cuppe = '
    'cup), and <b>-esse for -ess</b> (darkenesse = darkness). When in doubt: say the modern word. '
    'The old spelling is the costume; the word underneath is the same.',
    'body'))
story.append(spacer(6))

story.append(P('Hard words in Psalm 91', 'h2'))
story.append(pron_table([
    ('dwelleth', 'DWELL-uth', 'dwells'),
    ('secrete', 'SEE-kret', 'secret'),
    ('Almightie', 'all-MY-tee', 'Almighty'),
    ('vnto', 'UN-too', 'unto'),
    ('fortresse', 'FOR-tres', 'fortress'),
    ('deliuer', 'dih-LIV-er', 'deliver'),
    ('noysome', 'NOY-sum', 'noisome — harmful, noxious'),
    ('pestilence', 'PES-tih-lens', 'plague'),
    ('couer', 'KUV-er', 'cover'),
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
    ('euill', 'EE-vul', 'evil'),
    ('tabernacle', 'TAB-er-nak-ul', 'dwelling, tent'),
    ('giue', 'giv', 'give'),
    ('wayes', 'ways', 'ways'),
    ('beare', 'bair', 'bear / carry'),
    ('foote', 'fuut', 'foot'),
    ('lyon', 'LY-un', 'lion'),
    ('aspe', 'asp', 'asp — a cobra'),
    ('treade', 'tred', 'tread'),
    ('loued', 'luvd', 'loved'),
    ('knowen', 'NOH-un', 'known'),
    ('heare', 'heer', 'hear'),
    ('glorifie', 'GLOR-ih-fy', 'glorify'),
    ('satisfie', 'SAT-is-fy', 'satisfy'),
    ('shew', 'shoh', 'show'),
    ('saluation', 'sal-VAY-shun', 'salvation'),
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
    ('runneth ouer', 'RUN-uth OH-ver', 'runs over'),
    ('aduersaries', 'AD-ver-sair-eez', 'adversaries — enemies'),
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
    ('vnto', 'UN-too', 'unto'),
    ('helpe', 'help', 'help'),
    ('vpon', 'uh-PON', 'upon'),
    ('enemies', 'EN-uh-meez', 'enemies'),
    ('then', 'than', 'than — 1599 spelling habit'),
    ('haue', 'hav', 'have'),
    ('princes', 'PRIN-sez', 'princes — rulers, men of power'),
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
story.append(P('"He who dwells in the secret place of the Most High shall lodge in the shadow of the Almighty."', 'gloss'))
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
story.append(P('Exactly the Altar Ritual of Part II, with the green candle as the flame and the money petition spoken at step 6. Psalm 23 verse 5 is the money verse — the anointed head, the cup running over. The crown-touch and the slow breath at "my cuppe runneth ouer" are where the prosperity current seals. Psalm 118:6-9 (step 5) seals you against fear-of-lack before the petition is stated.', 'body'))
story.append(P('Form 2 — Selig\'s seven-morning working (documented, Secrets of the Psalms)', 'h2'))
story.append(P('<b>·</b> Seven consecutive mornings, on rising, anoint with olive oil mixed with bayberry oil and speak Psalm 23 (the Part I text).', 'step'))
story.append(P('<b>·</b> Candle when used: green or gold for prosperity. Dress with Money Drawing, Good Fortune, or Bayberry oil.', 'step'))
story.append(P('<b>·</b> On the seventh morning: hold seven Job\'s Tears seeds in the hand, walk to running water, speak Psalm 23, and throw the seeds over the <b>left shoulder</b> into the moving water to lay the trick.', 'step'))
story.append(P('<b>·</b> While dressing any prosperity candle or feeding a mojo bag, the spoken line is verse 5: <i>"thou doest anoynt mine head with oyle, and my cuppe runneth ouer."</i>', 'step'))
story.append(spacer(6))
story.append(P('Speak the abundance as flow for yourself in alignment with Source — never as a performance aimed at anyone else\'s lack. That is the frequency line between prosperity work and envy work.', 'greenbox'))
story.append(P('Witness on file: the first morning this working ran in its corrected form (June 8, 2026), the account read $777.10 by 11:04 AM. 7-7-7 reduces to 21 — the World. The working answers.', 'small'))
story.append(pagebreak())

# ============================ PROTECTION ============================
story.append(P('PART V', 'part'))
story.append(P('Protection', 'cover_sub'))
story.append(P('The outer perimeter, the inner perimeter, and the sovereignty seal.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Protection Order', 'h1'))
story.append(P('<b>Psalm 91 is the outer perimeter</b> — the household, the body, the day. <b>Psalm 155 is the inner perimeter</b> — your own mind and bones, against intrusive thought-forms, oppressive spirits, and pulls toward what your discernment rejects. <b>Psalm 118:6-9 is the sovereignty seal</b> — against fear of man, capture by human authority, the pull of institutional egregores. Use 91 daily; add 155 whenever the pressure is inside rather than outside; add 118:6-9 when the pressure is the social-political field.', 'body'))
story.append(P('Documented Psalm 91 protection practice', 'h2'))
story.append(P('<b>·</b> Holy Name: El Shaddai (el-shah-DYE). Hold it before reciting.', 'step'))
story.append(P('<b>·</b> Candle: white (most common) or purple. For a household boundary: a seven-day white glass-encased candle dressed with Protection or Fiery Wall of Protection oil.', 'step'))
story.append(P('<b>·</b> Herbs at the base: rue, hyssop, agrimony, black salt, red brick dust.', 'step'))
story.append(P('<b>·</b> Timing: Saturday is the traditional protection day; Tuesday when reversing an active attack.', 'step'))
story.append(P('<b>·</b> Verses 9–11 while anointing crown, throat, wrists, ankles, and the four corners of the threshold.', 'step'))
story.append(P('<b>·</b> Verse 11 three times before leaving the house; the whole psalm seven times on the eve of a long journey.', 'step'))
story.append(spacer(8))

story.append(P('Psalm 155 — the inner perimeter text', 'h2'))
story.append(P('Charlesworth/Sanders diction; recovered from the Dead Sea Scrolls (11QPsa) and the Syriac. YHWH is spoken aloud as Adonai (ah-doh-NYE).', 'small'))
story.append(spacer(4))
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
story.append(vr(14, 'My trust, O YHWH, is before You. I cried "YHWH!" and He answered me, and He healed my broken heart.'))
story.append(vr(15, 'I slumbered and slept, I dreamed; indeed I awoke.'))
story.append(vr(16, '[You sustained me, O YHWH]; I shall call upon YHWH my Savior.'))
story.append(spacer(6))
story.append(P('The Qumran expansion adds the binding line: <i>"Do not let Belial dominate me, nor an unclean spirit; let neither pain nor the evil inclination take possession of my bones."</i> Speak it after verse 11 when the working is against a named hostile pressure. This binds the hostile current away from you — it is boundary work, not a curse on any person.', 'body'))
story.append(P('Protection order at the candle: Psalm 91 first (outer), Psalm 155 second (inner), Psalm 118:6-9 third (sovereignty), Psalm 23 last (seal). White candle.', 'greenbox'))
story.append(pagebreak())

# ============================ CRISIS ============================
story.append(P('PART VI', 'part'))
story.append(P('Acute Crisis', 'cover_sub'))
story.append(P('When a hostile force is actively on you. Four psalms, this order.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Crisis Order', 'h1'))
story.append(P('This is not the daily working. This is for the day the lion is at the threshold — an active hostile working, a sustained attack, a siege. Four texts in a fixed order: <b>cry out (152) → raise the wall (91) → bind it off your bones (155) → give thanks before the rescue is visible (153)</b>. Speaking the thanksgiving before the deliverance arrives is itself the working.', 'body'))
story.append(spacer(6))

story.append(P('Step 1 — Psalm 152: the cry', 'h2'))
story.append(P('Spoken by David while the lion and the wolf were on his flock. Monad Rule at verses 4 and 6.', 'small'))
story.append(spacer(4))
story.append(vr(1, 'O God, O God, come to my aid; help me, save me, and deliver my soul from the slayer.'))
story.append(vr(2, 'Will I go down to Sheol by the mouth of the lion? Will the wolf be the end of me?'))
story.append(vr(3, 'Was it not enough for those who lay in wait for my father\'s flock, and tore a sheep of my father\'s flock — must they also wish the destruction of my own soul?'))
story.append(vr(4, 'Have pity, O <b>Monad</b>, and save Your holy one from destruction, so that he may rehearse Your glories for all of his days, and may praise Your great name,'))
story.append(vr(5, 'when You have delivered him from the hands of the destroying lion and of the ravening wolf, and when You have rescued my captivity from the hands of the wild beasts.'))
story.append(vr(6, 'Quickly, my <b>Monad</b>, send from Yourself a deliverer, and draw me out of the gaping pit which imprisons me in its depths.'))
story.append(spacer(8))
story.append(P('Step 2 — Psalm 91: the wall', 'h2'))
story.append(P('The full altar text from Part II. Speak all sixteen verses.', 'body'))
story.append(spacer(4))
story.append(P('Step 3 — Psalm 155: the binding-off', 'h2'))
story.append(P('The full text from Part V, including the Belial line after verse 11.', 'body'))
story.append(spacer(4))
story.append(P('Step 4 — Psalm 153: the thanksgiving spoken in advance', 'h2'))
story.append(P('Spoken by David after the lion and the wolf were dead. You speak it before the rescue is visible — that is the faith-act that completes the circuit. Monad Rule at verse 1.', 'small'))
story.append(spacer(4))
story.append(vr(1, 'Praise the <b>Monad</b>, all you nations; glorify Him and bless His name;'))
story.append(vr(2, 'For He delivered the soul of His Elect One from the hands of death; and He redeemed His Holy One from destruction.'))
story.append(vr(3, 'And He saved me from the snares of Sheol; and brought me forth from the abyss that is inscrutable.'))
story.append(vr(4, 'Because before my salvation could proceed from before Him, I almost became two parts by two beasts.'))
story.append(vr(5, 'However, He sent His angel and closed from me the gaping mouths; and redeemed my life from destruction.'))
story.append(vr(6, 'I myself shall praise Him and exalt Him because of all His graces, which He has provided and is providing for me.'))
story.append(spacer(6))
story.append(P('"Is providing" — present tense. The flow is current, not remembered. Land on that word.', 'small'))
story.append(pagebreak())

# ============================ CONSECRATION ============================
story.append(P('PART VII', 'part'))
story.append(P('Consecration &amp; New Role', 'cover_sub'))
story.append(P('Stepping into an office. Anointing an oil, a tool, a calling.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Consecration Order', 'h1'))
story.append(P('<b>Psalm 151 then Psalm 23.</b> 151 is the anointing psalm — Source chooses the overlooked youngest brother and the prophet anoints him prince. Use it when you are stepping into a new role, consecrating an oil or a tool, or taking a vow. Open with the Hebrew line: <i>hah-leh-loo-YAH leh-dah-VEED ben-yee-SHY.</i> Anoint with oil at verse 4. Then seal with Psalm 23.', 'body'))
story.append(spacer(6))
story.append(P('Psalm 151 — the anointing text', 'h2'))
story.append(P('Brenton 1851 Septuagint (verified against ebible.org). Monad Rule at verses 3 and 5. Verses 1–5 are the general working text; verses 6–7 (the Goliath combat) are situational — speak them only when you are answering an active, named attack.', 'small'))
story.append(spacer(4))
story.append(vr(1, 'I was small among my brethren, and youngest in my father\'s house: I tended my father\'s sheep.'))
story.append(vr(2, 'My hands formed a musical instrument, and my fingers tuned a psaltery.'))
story.append(vr(3, 'And who shall tell my <b>Monad</b>? the <b>Monad</b> himself, he himself hears.'))
story.append(vr(4, 'He sent forth his angel, and took me from my father\'s sheep, and he anointed me with the oil of his anointing.'))
story.append(vr(5, 'My brothers were handsome and tall; but the <b>Monad</b> did not take pleasure in them.'))
story.append(P('— the situational half —', 'small'))
story.append(vr(6, 'I went forth to meet the Philistine; and he cursed me by his idols.'))
story.append(vr(7, 'But I drew his own sword, and beheaded him, and removed reproach from the children of Israel.'))
story.append(spacer(6))
story.append(P('psaltery = SAWL-ter-ee, a small harp. Philistine = FIL-ih-steen.', 'small'))
story.append(P('Then Psalm 23 (Part I text) to seal the new office with provision and presence.', 'greenbox'))
story.append(pagebreak())

# ============================ CLARITY ============================
story.append(P('PART VIII', 'part'))
story.append(P('Clarity &amp; Discernment', 'cover_sub'))
story.append(P('The Sophia hymn. For decisions, confusion, crossroads.', 'cover_line'))
story.append(pagebreak())

story.append(P('The Clarity Order', 'h1'))
story.append(P('<b>Psalm 154 then Psalm 23.</b> 154 is the Wisdom hymn — Hokhmah / Sophia, the living Wisdom-current from the Monad, personified as a woman whose voice is heard from the gates of the righteous. The Western canon dropped this psalm; the Qumran community and the Syriac East kept it. Speak it when the question in front of you is a discernment call. Open with the Hebrew: <i>buh-KOHL gah-DOHL pah-ah-ROO eh-loh-HEEM.</i>', 'body'))
story.append(spacer(6))
story.append(P('Psalm 154 — the Wisdom text', 'h2'))
story.append(P('Charlesworth/Sanders diction; Hebrew preserved in 11QPsa. Monad Rule at verse 9. YHWH spoken as Adonai. Hokhmah = khokh-MAH. Wisdom is "she" throughout — that is the text, not a change.', 'small'))
story.append(spacer(4))
story.append(vr(1, 'With a loud voice glorify God; proclaim His splendor in the congregation of the many.'))
story.append(vr(2, 'Glorify His name in the multitude of the righteous, and celebrate His majesty with the faithful.'))
story.append(vr(3, 'Bind your souls to the good and to the perfect, to glorify the Most High.'))
story.append(vr(4, 'Assemble together to make His salvation known, and do not hesitate to make known His might and His majesty to all the simple.'))
story.append(vr(5, 'For it is to make known the glory of YHWH that Wisdom has been given;'))
story.append(vr(6, 'And it is for recounting His many deeds that she has been revealed to humans —'))
story.append(vr(7, 'To make His power known to the simple, to explain His greatness to those lacking understanding,'))
story.append(vr(8, 'Those who are far from her gates, those who have strayed from her entrances.'))
story.append(vr(9, 'For the Most High is the <b>Monad</b> of Jacob, and His majesty is upon all His works.'))
story.append(vr(10, 'A man who glorifies the Most High — He receives him as one who brings a meal offering,'))
story.append(vr(11, 'As one who offers he-goats and bullocks, as one who fattens the altar with many burnt offerings, as a sweet-smelling fragrance from the hand of the righteous.'))
story.append(vr(12, 'From the gates of the righteous her voice is heard, and from the assembly of the pious her song.'))
story.append(vr(13, 'When they eat with satiety she is cited, and when they drink in community together.'))
story.append(vr(14, 'Their meditation is on the Law of the Most High; their words to make known His power.'))
story.append(vr(15, 'How far from the wicked is her word, from all the haughty to know her.'))
story.append(vr(16, 'Behold, the eyes of YHWH have pity upon the good,'))
story.append(vr(17, 'And upon those who glorify Him He increases His mercy; from an evil time will He deliver their soul.'))
story.append(vr(18, '[Bless] YHWH, who redeems the humble from the hand of strangers, [and deliv]ers the perfect from the hand of the wicked,'))
story.append(vr(19, '[Estab]lishing a horn out of Ja[cob], and a judge of [peoples] out of Israel.'))
story.append(vr(20, 'He will spread His tent in Zion, and abide forever in Jerusalem.'))
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
story.append(P('<b>Psalm 23</b>, spoken at the bedside, the graveside, or on the anniversary. The whole psalm, slow. The hinge is verse 4 — the dark valley where the voice turns from "He" to "Thou" — speak it directly to Source, with the grief in your voice. That verse is the comfort spoken over the grief itself.', 'body'))
story.append(spacer(14))

story.append(P('One-Page Master Table', 'h1'))
mt = Table([
    [Paragraph('<b>Situation</b>', S['small']), Paragraph('<b>Order</b>', S['small']), Paragraph('<b>Candle</b>', S['small'])],
    [Paragraph('Everyday, on rising', S['body_left']), Paragraph('23 → gratitude → 91:11 ×3 at the door', S['body_left']), Paragraph('none', S['small'])],
    [Paragraph('Altar ritual (daily)', S['body_left']), Paragraph('cross → formula → 91 → 23 → 118:6-9 → petition → light → sit → thanks → snuff', S['body_left']), Paragraph('green (standing working)', S['small'])],
    [Paragraph('Money &amp; prosperity', S['body_left']), Paragraph('altar order with money petition; or Selig 7 mornings of 23', S['body_left']), Paragraph('green or gold', S['small'])],
    [Paragraph('Protection', S['body_left']), Paragraph('91 → 155 → 118:6-9 → 23', S['body_left']), Paragraph('white', S['small'])],
    [Paragraph('Sovereignty / public field', S['body_left']), Paragraph('118:6-9 alone, before posting / confrontation / court / meeting', S['body_left']), Paragraph('none or white', S['small'])],
    [Paragraph('Acute crisis', S['body_left']), Paragraph('152 → 91 → 155 → 153', S['body_left']), Paragraph('white', S['small'])],
    [Paragraph('New role / consecration', S['body_left']), Paragraph('151 (vv.1–5) → 23', S['body_left']), Paragraph('white or gold', S['small'])],
    [Paragraph('Clarity / decision', S['body_left']), Paragraph('154 → 23', S['body_left']), Paragraph('white or purple', S['small'])],
    [Paragraph('Travel', S['body_left']), Paragraph('91:11 ×3; long trip: 91 ×7 eve before, 23 that morning', S['body_left']), Paragraph('none', S['small'])],
    [Paragraph('After a death', S['body_left']), Paragraph('23, slow, verse 4 spoken to Source', S['body_left']), Paragraph('white', S['small'])],
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
story.append(P(
    'Candle colors, herbs, and timing follow the documented stream (Selig 1788; Yronwode / Lucky '
    'Mojo; Hoodoo Sen Moise) as carried in the main Altar Psalms Bible. The Monad Rule, the '
    'use-category sorting, the pronunciation, and the Psalm 118:6-9 sovereignty seal are this '
    'book\'s additions, built at the operator\'s instruction. Where your discernment lands '
    'differently, your discernment wins.',
    'small'))
story.append(spacer(10))
story.append(P('— end of the Reader —', 'cover_lineage'))

if __name__ == '__main__':
    doc = Doc('/home/user/numenist-site/altar-psalms-bible/altar-psalms-reader.pdf',
              pagesize=letter,
              leftMargin=MARGIN, rightMargin=MARGIN,
              topMargin=MARGIN, bottomMargin=MARGIN,
              title='The Altar Psalms Reader — Plain Order & Pronunciation',
              author='Numen / Jordan Ross Atkins')
    doc.build(story)
    print('Built: altar-psalms-reader.pdf')
