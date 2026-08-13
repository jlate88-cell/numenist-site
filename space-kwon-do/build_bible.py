"""
Space Kwon Do — Show Bible PDF Generator
Written for Jordan Ross Atkins. Compiles the full brainstorm conversation
from this session into a single canonical reference document.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)

# ---------- Styles ----------
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'TitleX', parent=styles['Title'],
    fontSize=32, leading=36, alignment=TA_CENTER,
    textColor=black, spaceAfter=12, fontName='Helvetica-Bold'
)
subtitle_style = ParagraphStyle(
    'SubtitleX', parent=styles['Title'],
    fontSize=14, leading=18, alignment=TA_CENTER,
    textColor=HexColor('#555555'), spaceAfter=24, fontName='Helvetica-Oblique'
)
h1 = ParagraphStyle(
    'H1X', parent=styles['Heading1'],
    fontSize=20, leading=24, textColor=black,
    spaceBefore=18, spaceAfter=10, fontName='Helvetica-Bold'
)
h2 = ParagraphStyle(
    'H2X', parent=styles['Heading2'],
    fontSize=15, leading=19, textColor=HexColor('#222222'),
    spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold'
)
h3 = ParagraphStyle(
    'H3X', parent=styles['Heading3'],
    fontSize=12, leading=16, textColor=HexColor('#333333'),
    spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold'
)
body = ParagraphStyle(
    'BodyX', parent=styles['BodyText'],
    fontSize=10.5, leading=14, alignment=TA_JUSTIFY,
    spaceAfter=6, fontName='Helvetica'
)
bullet = ParagraphStyle(
    'BulletX', parent=body,
    leftIndent=18, bulletIndent=6, spaceAfter=3
)
quote = ParagraphStyle(
    'QuoteX', parent=body,
    leftIndent=24, rightIndent=24, textColor=HexColor('#444444'),
    fontName='Helvetica-Oblique', spaceBefore=4, spaceAfter=8
)

# ---------- Helpers ----------
def P(text, style=body):
    return Paragraph(text, style)

def B(text):
    return Paragraph(f'&bull; {text}', bullet)

def HR():
    return Spacer(1, 0.1*inch)

def SPACE(h=0.15):
    return Spacer(1, h*inch)

# ---------- Content ----------
story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 2.2*inch))
story.append(P("SPACE KWON DO", title_style))
story.append(P("Show Bible — Working Draft", subtitle_style))
story.append(Spacer(1, 0.4*inch))
story.append(P("Compiled from session brainstorm on 5/30/2026 (PD 9 / Moon / Empress).", subtitle_style))
story.append(P("For Jordan Ross Atkins.", subtitle_style))
story.append(PageBreak())

# ===== TABLE OF CONTENTS =====
story.append(P("CONTENTS", h1))
toc_items = [
    "1. Cosmological Framing",
    "2. The Cast",
    "3. The Ship",
    "4. The Belt System (Heroes)",
    "5. The Drip System (Villains)",
    "6. The Great War — Backstory & Factions",
    "7. Recurring Villains",
    "8. Planets",
    "9. Dimensions",
    "10. Signature Techniques",
    "11. Anime Combat DNA",
    "12. Music & Rap Layer",
    "13. The Dojo Redshirt Roster",
    "14. Zap & Glitch — The Minions",
    "15. Comedy Rules",
    "16. Series-Long Mythology",
    "17. Full Episode Treatments",
]
for t in toc_items:
    story.append(P(t, body))
story.append(PageBreak())

# ===== 1. COSMOLOGICAL FRAMING =====
story.append(P("1. Cosmological Framing", h1))
story.append(P(
    "Space Kwon Do operates under integrated Pythagorean-Hermetic syncretism. "
    "Every character name is run through Chaldean numerology; every villain rank, ship name, "
    "and planet name carries vibrational weight that informs the show's mythology. "
    "Karmic Debt numbers (13, 14, 16, 19) are flagged when they appear. Tarot correspondences "
    "for compound numbers are used to anchor character arcs. "
    "<i>As above, so below.</i> The cosmic frame is the ground; the comedy and combat are how it lands."
, body))
story.append(P(
    "<b>Jordan's chart anchor (Master Number 11/2 Life Path, active 8 Pinnacle 2026-2034)</b> "
    "is the operator-position from which all the brainstorming flowed. His character in the show "
    "shares his name vibration (20/2 Chaldean) and his Pinnacle drives the Diamond Iced ladder structure."
, body))

# ===== 2. CAST =====
story.append(P("2. The Cast", h1))
story.append(P("PRIMARY DUO", h2))
story.append(P("<b>JORDAN</b> — Chaldean 20/2. Judgement card / Master 11 reducer. Muay Thai (close-combat, elbows and knees). Gold Belt. The channel-warrior. Connects the team.", body))
story.append(P("<b>STEFFIN</b> — Chaldean 34/7. Saturn-Mystic. Karate + mixed martial arts. Captain of the Ronin. Gold Belt. The withdrawn analyst-leader, the brooding-captain trope elevated.", body))
story.append(P("REGULAR THIRD", h2))
story.append(P("<b>SIMON</b> — Chaldean 20/2. Judgement card / Awakened Killer. Former Empire of Polish war-machine, activated post-Truce, taught by a dying Crane monk to choose. Now wears the Ash Belt — a new rank invented for warriors who have transcended the kill-instinct. Combat-support primary; limit-break is PROTOCOL ZERO. Speaks rarely, profoundly. Tends a secret cargo-hold garden.", body))
story.append(P("RECURRING", h2))
story.append(P("<b>ERICA</b> — Chaldean 12/3. Hanged Man card / Empress reduction. Pilot of the Ronin, Quantum Capoeira practitioner, secret Platinum Belt. Comes when called, has her own life off-ship. Audience-surrogate. Names what the boys refuse to. Carried wounded from both sides during the Great War — that's why she'll fly Jordan and Steffin together.", body))
story.append(P("STRUCTURAL NOTE", h2))
story.append(P(
    "Three 20/2 vibrations operate on the ship (Jordan + Simon + the Ronin itself). "
    "Triple Judgement-trumpet field. Master Mystic 7 (Steffin) processes the trumpet. "
    "The cosmic structure is a three-trumpet awakening with one analyst integrating the call. "
    "Whatever the ship encounters is being called to rise."
, body))

# ===== 3. THE SHIP =====
story.append(P("3. The Ship", h1))
story.append(P("Name options (Chaldean checked):", body))
story.append(B("<b>THE RONIN</b> = 20/2. Judgement, masterless-warrior. Same frequency as Jordan and Simon. Recommended primary."))
story.append(B("<b>THE BLACK FLAG</b> = 26/8. Pinnacle 8 number. Outlaw-coded material-mastery name."))
story.append(B("<b>THE OMEN</b> = 21/3. World card, completion energy."))
story.append(B("<b>THE JADE FANG</b> = 28/1. Sun number, leader, first-strike."))
story.append(P("The ship has its own AI presence — droll, ancient, judgmental. Speaks rarely. Lands hard. Functions as silent fourth crew member.", body))

# ===== 4. BELT SYSTEM =====
story.append(P("4. The Belt System (Heroes)", h1))
belt_data = [
    ['Belt', 'Meaning'],
    ['Black Belt', 'Required to board the Ronin. Dojo standard. Most die before silver.'],
    ['Silver Belt', 'Hard-won. Lady Hair achieves this before dying. Rare survival.'],
    ['Gold Belt', 'Jordan and Steffin. Master tier. Six others exist galaxy-wide.'],
    ['Platinum Belt', 'Above Gold. Requires demonstrated LEVITY. Erica secretly holds this.'],
    ['Ash Belt', 'Invented for Simon. For warriors who have transcended the kill-instinct. Hidden brotherhood across the galaxy.'],
]
belt_table = Table(belt_data, colWidths=[1.2*inch, 5.0*inch])
belt_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#dddddd')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#888888')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(belt_table)

# ===== 5. DRIP SYSTEM =====
story.append(P("5. The Drip System (Villain Ranking)", h1))
story.append(P(
    "Villains are ranked by ice and gemstone. The Drip system is the structural inverse of the Belt system: "
    "heroes earn rank through discipline; villains buy rank through material flex. "
    "Each gemstone carries Chaldean weight."
, body))
drip_data = [
    ['Rank', 'Chaldean', 'Card / Function', 'Notes'],
    ['SILVER', '20/2', 'Judgement', 'Entry-level. The shadow trumpet — heralds bigger storm.'],
    ['EMERALD', '24/6', 'Lovers/Devil-axis', 'Mid-tier. Domestic-aligned, mob bosses, family operations.'],
    ['RUBY', '11/2', 'Master 11 in distortion', 'High-tier. Power without integration. Psychological-warfare specialists.'],
    ['SAPPHIRE', '33/6', 'Master 33 in shadow', 'Elite. False-master energy. Former teachers turned wrong.'],
    ['DIAMOND', '26/8', 'Pinnacle 8 dark mirror', "Final-boss class. Material-mastery as oppression. The dark mirror of Jordan's Pinnacle."],
    ['ONYX', '18/9', 'Moon, dark integration', 'Beyond Diamond. Ultimate boss. Has integrated all shadow into one form.'],
]
drip_table = Table(drip_data, colWidths=[0.9*inch, 0.8*inch, 1.6*inch, 2.9*inch])
drip_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), HexColor('#ffffff')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#888888')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(drip_table)
story.append(SPACE(0.1))
story.append(P(
    "<i>Every Diamond Iced villain is what Jordan would become if he abandoned the Gold Belt path. "
    "Each Diamond fight is the hero facing the dark mirror of his own active Pinnacle.</i>"
, quote))

# ===== 6. GREAT WAR =====
story.append(P("6. The Great War — Backstory & Factions", h1))
story.append(P("FACTIONS", h2))
story.append(B("<b>The Mars Bloc</b> — Hard Style. Tigers, Dragons, breaking arts. Jordan's old side."))
story.append(B("<b>The Crane Concord</b> — Soft Style. Cranes, Snakes, redirection arts. Steffin's old side."))
story.append(B("<b>The Empire of Polish</b> — Tech faction. Emperor Proctor's. Scorns martial arts. Built Simon as a war-machine deployed too late."))
story.append(B("<b>The Unaligned</b> — Pacifists, monks, civilians caught between. Erica's people. She carried wounded from all sides."))
story.append(P("TRIGGER", h2))
story.append(P(
    "The <b>Theft of the Master's Belt</b> — an artifact demonstrating mastery beyond the Hard/Soft split. "
    "Both factions claimed the other stole it and went to war. "
    "<b>Eventual truth (late-series reveal):</b> the Belt walked off by itself. It was a soul cycling through forms. "
    "It chose to leave. Both sides fought a war over something neither stole."
, body))
story.append(P("THE PEACE", h2))
story.append(P(
    "The Truce of Veringol. Both sides exhausted. Jordan and Steffin met at the Truce ceremony — they each honored the dead "
    "from the other's side, which neither faction technically required. Erica saw them do this and decided they were worth flying. "
    "Simon arrived years later, post-Activation, and asked to join. They accepted with full solemnity."
, body))

# ===== 7. RECURRING VILLAINS =====
story.append(P("7. Recurring Villains", h1))
villains = [
    ('CASIMIR THE CRITIC', '15/6 (Devil)', 'RUBY', 'No fighting skill, maximum psychological threat. Describes the heroes\' seriousness in real-time during combat. They cannot defeat him because they refuse to acknowledge him.'),
    ('EMPEROR PROCTOR', '33/6 (Master Teacher, shadow)', 'DIAMOND', 'Tech-empire leader. Sees the heroes as LARPers. Returns repeatedly with bigger tech. Heroes humble him with elbows. Built Simon.'),
    ('AYANNA OF THE THIRD LEGION', '14/5 (KD Temperance)', 'EMERALD', 'War-survivor who didn\'t accept the Truce. Her grievance is real — the karmic 14 marks unmoderated warrior energy.'),
    ('VEX SILVERTOOTH', '16/7 (KD Tower)', 'SILVER', 'Tower-energy minor villain. Often a stepping-stone to bigger fights.'),
    ('MADAM CHIME', '14/5 (KD Temperance)', 'SAPPHIRE', 'Sound-based fighter. Warrior who can\'t moderate. Sapphire-level threat.'),
    ('GENERAL JAW', '32/5', 'DIAMOND', 'Bone-strike specialist with Empire of Polish bionic upgrades. Fights with his jaw.'),
    ('THE TWIN ICES', 'shared mind', 'SAPPHIRE', 'Mirror twins, both wearing diamonds, fight in perfect sync. Share one mind.'),
    ('MIRROR JORDAN / MIRROR STEFFIN', '20/2 / 34/7', 'varies', 'Comedic-self shadows from the Mirror Dimension. Joke constantly. Heroes find them offensive.'),
    ('THE HOLLOW KING', 'absence', 'ONYX', 'The void itself. Final-series antagonist. Faceless. No name to vibe — the vibration of absence is the weapon.'),
    ('VESPER BLOODFANG', '29/11 (Master 11 shadow)', 'SILVER', 'Bat-themed slum-planet warlord. Pilot-episode villain. Drew Zap & Glitch with his Master-11 shadow channel.'),
]
v_table_data = [['Name', 'Chaldean', 'Drip', 'Notes']]
for name, chal, drip, notes in villains:
    v_table_data.append([name, chal, drip, notes])
v_table = Table(v_table_data, colWidths=[1.6*inch, 1.4*inch, 0.7*inch, 2.5*inch])
v_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#222222')),
    ('TEXTCOLOR', (0,0), (-1,0), HexColor('#ffffff')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#888888')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(v_table)

story.append(PageBreak())

# ===== 8. PLANETS =====
story.append(P("8. Planets", h1))
story.append(P(
    "Each planet visual-distinct, premise gettable in five seconds, fighting built in. "
    "Drip-ranked bosses where named."
, body))

planets = [
    # name, drip, description
    ("BREK-7 — The Slum Planet", "SILVER (Vesper Bloodfang)", "Cyberpunk martial arts. Crime lords rap-battle for territory. Heroes refuse to rap-battle ('Rap is not the way of the warrior'). Erica rap-battles for them, wins a borough. Pilot setting."),
    ("SENSHARA — Planet of the Sensei", "varies", "Every inhabitant is a martial arts master. Civil war between Tiger, Crane, and Otter Houses. Masters speak only in koans. Heroes nod solemnly. Erica narrates the actual meaning to the audience under her breath. Simon learns The Strike That Weeps from Otter House."),
    ("THE BUREAU PLANET (Burocratos-7)", "DIAMOND (Dross)", "Martial arts illegal without permits. Forms are 47 pages. Heroes file paperwork between strikes. Permits expire mid-fight. Boss is a Diamond Iced Permit Director who fights from behind his desk."),
    ("VANGUARD-9 — The Funeral Planet", "SAPPHIRE (High Mourner Zeph)", "Where failed missions are interred. Mortician-Monks weep for hire. Steffin gives a 40-minute eulogy. Monks fake-weep through it. Erica catches them backstage drinking and comparing tears-per-minute."),
    ("SYNARA — The Algorithm Planet", "DIAMOND (CEO Prax)", "Run by Talos-9 AI. Combat opponents adapt mid-fight. AI keeps suggesting 'Lighten Up.' Heroes refuse. They lose every preliminary fight. Talos-9 offers Simon friendship; Simon accepts; Talos-9 quietly stops feeding the villain data."),
    ("THE EMPIRE OF POLISH (multi-planet)", "DIAMOND (Emperor Proctor)", "Galactic tech empire. Recurring season-spanning antagonist. Bigger and bigger tech. Heroes always win with basic martial arts. Proctor sees them as LARPers and cannot understand his own failures."),
    ("TRIBUNAL PRIME — The Honor Planet", "RUBY (Lord Vex)", "Every action governed by elaborate martial code. Steffin thrives. Erica is bored and breaks every code, causing diplomatic crises. ('The shoes were Velcro.')"),
    ("HILARIUS IV — The Drug Planet", "SAPPHIRE (Baron Giggles)", "Population on Giggledust, a perception substance. Locals see heroes as absurd and laugh constantly. Heroes interpret laughter as tactical weakness. Jordan gets dusted mid-fight; laughs for the first time in the series."),
    ("HEXAPOD-9 — The Insect Planet", "hive royalty (Vespryne / Groxx)", "Sentient hive-mind insectoids. Steffin is invited to arbitrate a succession. The dying Queen offers him a mating dance. He performs it flawlessly. Becomes Brother of the Hive forever. Insect emissaries periodically appear in later episodes calling him 'Brother.'"),
    ("HYDROPOLIS-3 — The Water Planet", "varies", "All combat underwater. Surface techniques don't work. Steffin invents 'Wet Karate.' Erica is a natural — backstory drop, she was a competitive swimmer as a kid. First episode she carries the team."),
    ("GLACIUS-4 — The Ice Planet", "EMERALD", "Sub-zero combat. Slippery footing. Steffin's stances shine. Boss rides a giant frost-bear. Final fight on a melting ice bridge over a frozen sea."),
    ("SAHARATH — The Desert Planet", "RUBY", "Endless dunes, no water, sand-bending warlord controls the one well. Heroes free the well. Sand-manipulator combat."),
    ("PYROS — The Lava Planet", "SAPPHIRE", "Volcanic. Combat on hardening lava floes. Boss forges weapons from heart-magma. Possible Master's Belt mythology tie-in."),
    ("SELENE — The Crystal Planet", "RUBY", "Crystalline forests and cities. Sound carries forever — heroes can't whisper tactics. Stealth combat in kaleidoscope battles."),
    ("TEMPEST-9 — The Storm Planet", "EMERALD", "Perpetual lightning. Heroes must ground themselves. Auras attract bolts. Simon (metal-bodied, grounded) is lightning-immune — his episode."),
    ("MONS MAJOR — The Gravity Planet", "varies", "Triple Earth gravity. First true power-up planet. Heroes leave permanently stronger. They later use gravity-collars to train on the ship."),
    ("REFLECTUS — The Mirror Planet", "RUBY", "Surface is one polished mirror. Combat requires fighting reflections. Visually every shot is twinned."),
    ("SPORADIA — The Mushroom Planet", "varies", "Spores cause personalized hallucinations. Jordan sees his mother. Steffin sees his brother. Simon sees the Crane monk. Erica sees herself succeeding without them. They fight through the visions."),
    ("COLOSSUS — The Giant Planet", "varies", "Heroes are ant-sized relative to locals. Asymmetric combat. Comedy gold."),
    ("MINIMUM-1 — The Tiny Planet", "varies", "Heroes are giants. Precision combat — knock out without crushing."),
    ("NYX — The Night Planet", "varies", "Perpetual darkness. Combat by sound and motion only. Erica's spotlight (Hanged Man perceives by absence)."),
    ("SYLVANIA — The Forest Planet", "varies", "Sentient trees. Heroes ally with the tree-king. Boss is a logger-villain harvesting sentient wood."),
    ("FORGE-IRON — The Metal Planet", "varies", "Magnetic surface. Heroes' metal gear sticks to ground. Unarmed combat. Simon has trouble walking."),
    ("FUNHAUS — The Carnival Planet", "SAPPHIRE", "Permanent festival. Combat hidden in attractions. Funhouse mirrors, rollercoaster fights, cotton-candy weapons. Ringmaster boss."),
    ("CRAPULUS-9 — Planet Hung-Over", "DIAMOND", "Population perpetually drunk and hung-over. Combat with locals puking mid-fight. Boss slurs his menace."),
    ("MATRIMONIA — Planet Always-Wedding", "DIAMOND (Groom Zero)", "Every day is someone's wedding. Combat happens at receptions without ruining cakes."),
    ("ETIQUIA — Planet Polite-To-Death", "varies", "Aggressive politeness. Tea before fights, apologies after. Steffin loves it. Jordan offends the planet by sneezing without saying 'excuse me.'"),
    ("SNIPER-PRIME — Planet Dead-Eye", "varies", "Everyone's a marksman. Heroes have to close distance under fire. The boss is just a regular guy without a gun once they reach him."),
    ("MATERNA-3 — Planet Mom", "SAPPHIRE (Galactic Mom)", "Middle-aged women warriors fight with kitchen implements. Galactic Mom serves cookies between rounds. Simon is adopted on the spot by three moms."),
    ("OLFACTUS — Planet Stink", "varies (Stench-Lord Vostri)", "Everything smells terrible. The smell is the local CURRENCY — they trade in smells. Heroes accidentally inhale 400 credits."),
    ("BELATERRA — Planet Late", "varies", "Everyone is always running late. Heroes wait four hours in a dueling circle for a boss who shows up apologizing profusely."),
    ("VERBATIM-7 — Planet Literal", "(BIG DEAL)", "Inhabitants take everything literally. 'I'll wipe the floor with you' — locals hand Jordan a mop. Boss is a literal large business contract. Cannot be punched. Heroes leave without victory."),
    ("ECHO-PRIME — Planet Bad-Cover-Band", "SAPPHIRE (Flex Much)", "Everyone plays covers of songs that don't exist. Erica humiliates the boss in a rap battle. Heroes clap politely."),
    ("RECURSIVUM — Mirror-of-Mirror", "varies", "Same as the last planet but slightly off. Every planet has a recursive twin. Implied infinite franchise model. Heroes don't notice."),
]
for name, drip, desc in planets:
    story.append(P(f"<b>{name}</b>", h3))
    story.append(P(f"<i>Drip / Boss:</i> {drip}", body))
    story.append(P(desc, body))

story.append(PageBreak())

# ===== 9. DIMENSIONS =====
story.append(P("9. Dimensions", h1))
story.append(P(
    "Dimensions are pocket realms with simple, gettable rules. Heroes pass through these "
    "for character-test episodes or quick comedic detours."
, body))

dimensions = [
    ("THE MUSIC DIMENSION", "Matter is rhythm. Martial arts only work synced to a beat. The literal Boondocks 'fight-with-rap-in-background' premise made real. Heroes emerge changed. They kind of like the rhythm-fighting. They won't admit it."),
    ("THE MIRROR DIMENSION", "Alternate selves with comedic awareness. Mirror-Jordan, Mirror-Steffin laugh constantly, joke. Heroes find them offensive. Mirror-Erica is identical to regular Erica — she already carries the comedic function."),
    ("THE PAST LIFE DIMENSION", "Past-life selves. Steffin's is a clown. Jordan's is a librarian. Erica's is a deity (deity confirms it to her). Simon meets his original Empire programmer."),
    ("THE AUDIENCE DIMENSION", "Realm that's a TV viewing party. Audience comments on the show as it happens. Heroes don't break character; they interpret laughter as enemy confusion."),
    ("THE TAROT DIMENSION", "Pocket realm structured like the Major Arcana. 22 chambers. Each chamber a card-archetype trial. Long-arc material."),
    ("THE LOOP REALM", "17-minute time loop. Groundhog Day with martial arts. Heroes perfect their loop-actions to absurd precision while Erica figures out the actual escape."),
    ("THE GRAVITY-INVERSE DIMENSION", "Reversed cause and effect. Actions happen before the choice to do them. Forces intuition-first combat."),
    ("THE SOUND DIMENSION", "No melody, only noise. Heroes find signal in noise. Erica's spotlight (12/3 Hanged Man perceives by voice and sound)."),
    ("THE VERSE DIMENSION", "Reality structured like a poem. Every move must rhyme. Spoken words must scan. One-take rap-battle dressed as combat."),
    ("THE NEGATIVE-SPACE DIMENSION", "Everything is what isn't there. Erica wins by saying nothing."),
    ("THE SLOW-MOTION DIMENSION", "Everything at quarter speed. Strategic, deliberate. Anime-classic. Inner monologues last actual scene-lengths."),
    ("THE FAST-MOTION DIMENSION", "4x speed. Hyper-reaction. Dojo redshirts who survive level up significantly. Power-up dimension."),
    ("THE CARTOON DIMENSION", "Reality is 2D animation. Cartoon physics — squash, stretch, fall and bounce. Heroes take everything seriously while their bodies behave like Looney Tunes. Pure visual comedy."),
    ("THE OPPOSITE DIMENSION", "Opposites are true. Inhabitants take only silly people seriously. Heroes have to act silly. They cannot. Erica solves it by being herself."),
    ("THE MEDIEVAL DIMENSION", "Castles, swords, dragons. Heroes adapt martial arts to dragon-era. Diamond Knights are an actual thing — Drip system meets the medieval era."),
    ("THE WILD WEST DIMENSION", "Saloons, six-shooters, high-noon duels. Heroes adapt martial arts to quickdraw culture without guns. Spaghetti-Western with rap soundtrack instead of Morricone."),
    ("THE 8-BIT DIMENSION", "Retro video game reality. Pixelated. Health bars. Power-ups on the floor. Heroes fight as 8-bit sprites. Doubles as Cypher Episode setting."),
    ("THE NOIR DIMENSION", "Black and white. Trench coats. Foggy alleys. Detective narration over every scene. Heroes' solemnity ALMOST fits."),
    ("THE SILENT FILM DIMENSION", "Black and white, no dialogue, inter-title cards. Slapstick combat. Heroes pantomime seriousness with grand gestures. Piano accompaniment."),
    ("THE INVERTED COLOR DIMENSION", "Photo-negative reality. Combat in inverted colors. Visually disorienting, premise simple."),
    ("THE COMMERCIAL BREAK DIMENSION", "Reality cuts to commercials mid-fight. Heroes wait through ads. Eventually learn to attack during commercials when the villain is also stuck watching."),
    ("THE CRINGE DIMENSION", "Late-2010s slang badly used. 'No cap fr fr, that's lowkey bussin.' Boss is VIBE CHECK. Heroes refuse to use the slang and lose every social encounter."),
    ("THE FILLER EPISODE DIMENSION", "Nothing important happens. Heroes recognize they're in filler and try to grow as characters. They can't. Episode ends with beach volleyball."),
    ("THE ANIME RECAP DIMENSION", "Reality is a recap of previous events. Heroes fight while clips of their past play. They try to censor embarrassing moments; they can't until the recap finishes."),
    ("THE PARENTS WATCHING DIMENSION", "Everyone's parents in the audience. Jordan's mom, Steffin's parents, Simon's 'parent' Emperor Proctor. Steffin tries hard to impress unimpressed parents."),
    ("THE DUBBED DIMENSION", "Poorly dubbed audio. Mouths don't match. Simon's voice comes out as a chipmunk anime girl. He delivers his wind-quote in chipmunk voice. Heroes don't laugh. Erica laughs."),
    ("THE FAN FICTION DIMENSION", "Reality written by amateur fans. Plot beats are weird. Romance subplots erupt. Steffin gets paired with the bat villain in awkward beach scenes. He plays them with full sincerity."),
    ("THE GROUP CHAT DIMENSION", "Reality is a group chat. Heroes communicate by text bubbles. Boss is READ AT 9:47. Combat is typing speed. Simon's bubbles are emoji."),
    ("THE THIRD-PERSON DIMENSION", "Reality is in third person. Heroes must refer to themselves in the third person. Joke: they kind of already do."),
]
for name, desc in dimensions:
    story.append(P(f"<b>{name}</b>", h3))
    story.append(P(desc, body))

story.append(PageBreak())

# ===== 10. SIGNATURE TECHNIQUES =====
story.append(P("10. Signature Techniques", h1))
story.append(P(
    "Anime-style named attacks. Shouted aloud the first time used per season. "
    "Text overlay on screen for the first use. Heroes call attacks with solemn gravity; "
    "villains call attacks with rap-style brag. The asymmetry is the joke."
, body))

story.append(P("JORDAN — Muay Thai", h2))
story.append(B('<b>"THIRTY-SIX CROWS"</b> — flurry of elbow strikes'))
story.append(B('<b>"THE STANDING PISCES"</b> — twin-elbow finisher (his Sun sign — two fish striking up the same current)'))
story.append(B('<b>"HEART-TAP"</b> — single strike to the chest'))
story.append(B('<b>"THE CHANNEL STRIKE"</b> — stillness, then one blow (Master 11 channel firing)'))

story.append(P("STEFFIN — Karate-Mix", h2))
story.append(B('<b>"THE SATURN RETURN"</b> — delayed counterstrike'))
story.append(B('<b>"SEVEN TOWERS FALLING"</b> — sweep + throw combo (his 7 + Tower card)'))
story.append(B('<b>"CAPTAIN\'S SILENCE"</b> — defensive stance, bait the impatient strike'))
story.append(B('<b>"THE MYSTIC PIN"</b> — ground hold while explaining what the opponent did wrong'))

story.append(P("SIMON — Combat Support / Limit-Break", h2))
story.append(B('<b>"THE EMPTY STRIKE"</b> — winds up to kill, stops, opponent surrenders'))
story.append(B('<b>"THE TACTICAL EMBRACE"</b> — disarms opponents with a hug'))
story.append(B('<b>"THE APOLOGY"</b> — names the strike and apologizes mid-blow'))
story.append(B('<b>"PROTOCOL ZERO"</b> — full war-machine limit-break. Once or twice a season. Costs him an episode of quiet aftermath.'))
story.append(B('<b>"THE STRIKE THAT WEEPS"</b> — learned from Otter House on Senshara. Attacker\'s grief flows into the strike. Cannot be taught without a wound.'))

story.append(P("ERICA — Quantum Capoeira", h2))
story.append(B('<b>"THE TIDE-TURN"</b> — reverses direction mid-fight, opponent is already where she predicted'))
story.append(B('<b>"THE INVERSION"</b> — Hanged Man counter. Hangs upside down at the last instant of an enemy strike, counters from inversion.'))
story.append(B('<b>"THE ONE-NOTE DROP"</b> — pure sound-as-weapon. Earned in the Sound Dimension episode.'))

story.append(PageBreak())

# ===== 11. ANIME COMBAT DNA =====
story.append(P("11. Anime Combat DNA", h1))
story.append(P("This is an action anime, not a sitcom with fights. Every episode requires:", body))
story.append(B("<b>Minimum one-third combat time.</b> Major boss fights span multiple episodes."))
story.append(B("<b>Named attacks called aloud with text overlay.</b> DBZ-style. Heroes solemn; villains braggy."))
story.append(B("<b>Auras tied to numerology.</b> Jordan = master-blue/violet (11). Steffin = mystic-purple (Saturn-7). Simon = silver-ash. Erica = hanged-gold (12/3)."))
story.append(B("<b>Power-ups tied to spiritual integration.</b> When Jordan integrates a karmic lesson (3, 7, 8), aura intensifies and a new technique unlocks. Mythology revealed through power-ups."))
story.append(B("<b>Trash talk asymmetry.</b> Heroes trash talk solemnly ('Your form betrays incomplete devotion to your line'). Villains casually ('Bro you're literally praying mid-fight')."))
story.append(B("<b>Inner monologue during strikes.</b> Heroes have long internal philosophical monologues mid-combat. Fights pause for them. Anime tradition."))
story.append(B("<b>Drip-Rank progression.</b> Each season climbs the Silver-to-Onyx ladder. Diamond fights span 2-3 episodes. Onyx is the season finale."))
story.append(B("<b>Training arcs</b> between major battles. Standard shonen training-arc beats: new master, painful lesson, breakthrough, return with new technique."))
story.append(B("<b>Tournament arcs</b> every season. Bigger each time."))
story.append(B('<b>The Dojo Death Reel.</b> Closing montage of fallen redshirts with rap dirge — names, years lived, discipline mastered. Played dead serious. Grows absurdly long by Season 2.'))

# ===== 12. MUSIC / RAP =====
story.append(P("12. Music & Rap Layer", h1))
story.append(B('<b>Each main character has a personal combat theme.</b> Three distinct tracks. Evolve through seasons.'))
story.append(B('<b>Title track evolves.</b> S1 = Jordan\'s verse. S2 = +Erica\'s verse. S3 = +Sage\'s verse. S4 = full posse cut.'))
story.append(B('<b>The Rapper Sage</b> — recurring wandering wisdom-rapper. Voiced by real-rapper cameos each appearance. His bars become canonical in-universe.'))
story.append(B('<b>Cypher Episode</b> — annual bottle episode where combat is a literal rap cypher.'))
story.append(B('<b>The Dojo Death Reel</b> — closing montage with melancholy rap dirge. Names, years lived, discipline mastered.'))
story.append(B('<b>Aqua Teen Hunger Force structure</b> — rap in transitions, between segments, in title. Boondocks influence — fight-with-rap-in-background.'))

# ===== 13. DOJO REDSHIRTS =====
story.append(P("13. The Dojo Redshirt Roster", h1))
story.append(P('Each redshirt has a personality bigger than their screen time. Anyone the camera lingers on dies. Their deaths land because their personalities are vivid.', body))

redshirts = [
    ("LADY HAIR", "18/9 Moon", "Long blonde-haired warrior. Monsters keep trying to mate with him. Steffin nicknamed him; Brad is his real name but no one calls him Brad anymore. Has unrequited crush on Erica. Hair magically grows each episode. Earns Silver Belt; proposes to Erica in the same scene he gets killed by stray plasma bolt. Erica looks up from coffee: 'I was going to say no.'"),
    ("HOTBOX", "30/3 Empress", "Smokes between strikes. Offers every enemy a hit. Some accept. Dies offering a Diamond Iced villain a joint mid-fight. Villain accepts, lights it, then incinerates Hotbox while still smoking. Honored death."),
    ("PINKY", "17/8 Star", "Tiny, fast, talks constantly. Lives in Steffin's shadow as a positive hype-man. Calls Steffin 'Big Brother Captain.' Dies tackling a missile to save Steffin."),
    ("OLD MAN MOK", "37/10/1 Wheel", "Claims he's 102. Probably 47. Speaks wisdom-gibberish: 'When the river flows like a turnip, the warrior is full of ducks.' Dies of 'old age' mid-fight. Funeral reveals he was 38."),
    ("DROP-KICK DARIUS", "17/8 Star", "Only knows one move. Drop-kicks everything — doors, salads, insults. Dies attempting a drop-kick on a flying ship. Sails into vacuum. Steffin: 'Darius drop-kicked the void. The void was honored.'"),
    ("BIG MOIST", "25/7 Mystic", "Large, sweaty, hands out napkins. Surprising emotional intelligence. Best friend on the dojo. Dies hugging Simon during a battle. Simon's hug-protocol cannot save him. Simon mourns alone in the garden for three episodes."),
    ("PAULIE FOUR-LEGS", "24/6 + 37/1", "Prosthetic robot legs — TWO pairs, walks like a centaur. Chose to add an extra pair 'for balance.' Dies misplacing a hoof on a stairwell."),
    ("THE TWINS — KAI & KAI", "4 + 4", "Both named Kai. Refuse to clarify which is which. Sometimes fight as one. When one dies, the other immediately answers to both names. 'There has always been one Kai.'"),
    ("SISTER CONSTANCE", "49/13/4 KD Death", "Former nun who left the order for martial arts. Wears the habit. Rosary as weapon. Says grace before every fight, for both sides. Dies blessing her killer. Killer is moved, joins the dojo, dies next episode."),
]
for name, chal, desc in redshirts:
    story.append(P(f"<b>{name}</b> — {chal}", h3))
    story.append(P(desc, body))

# ===== 14. ZAP & GLITCH =====
story.append(P("14. Zap & Glitch — The Minions", h1))
story.append(P("<b>Name vibrations:</b> ZAP = 16/7 (KD Tower). GLITCH = 19/1 (KD Sun). Both Karmic Debt names. Their pattern of perpetual follower-ship is structural in their names — KD 16 collapses every leadership attempt; KD 19 makes them misuse authority when they have it. They cannot break the pattern until both debts integrate.", body))
story.append(P("ORIGIN", h2))
story.append(P("Former Empire of Polish propaganda-techs — assigned to amplify squad morale during the Great War. Their squad died. Truce signed. They kept hyping. Have been finding new villains to amplify ever since.", body))
story.append(P("THE CORE PATTERN", h2))
story.append(P("Every time the heroes kill their boss, they find a new boss within 24 hours. Each new boss is slightly stranger than the last. Eventually they run out of bosses willing to take them on and invent one in their heads — DADDY DRIP. The imaginary boss issues increasingly absurd orders. They argue about what he said.", body))
story.append(P("THE CLIMACTIC REALIZATION", h2))
story.append(P("The imaginary boss IS them. They've been leading each other through the puppet of an imagined third. When they realize this, they finally accept rank — they become Ruby Iced together. Their fight against the heroes after the promotion is genuinely hard.", body))
story.append(P("RECURRING BITS", h2))
story.append(B('<b>Assigned hype phrases</b> yelled regardless of context: "OH YOU IN TROUBLE NOW!" / "THAT\'S A BOSS-LEVEL MOVE!" / "HE BUILT DIFFERENT!"'))
story.append(B('<b>Business cards</b> — "Zap & Glitch Hype Co. — Boss Energy Amplification Since The Truce."'))
story.append(B('<b>The Spreadsheet</b> — Google Sheet of every boss they\'ve worked for, ranked by Drip tier and severance package.'))
story.append(B('<b>30-Second Silence Ritual</b> — when a boss dies, exact 30 seconds, then they pivot to the killer: "So... you hiring?"'))
story.append(B('<b>Wrong notes</b> — they take combat notes on the heroes\' techniques. The notes are wildly wrong. "Jordan\'s Standing Pisces = jumping fish noise."'))
story.append(B('<b>Identity erosion</b> — one of them periodically misremembers the other\'s name. "Zap — I mean Glitch — wait who am I again."'))
story.append(B('<b>The slogan</b> — "WHEN THE BOSS POPS, WE HYPE-DROP."'))

# ===== 15. COMEDY RULES =====
story.append(P("15. Comedy Rules", h1))
story.append(P("Extracted from the Lady Hair monster-mating opening scene. The engine of the show's comedy:", body))
story.append(B("<b>Ridiculous setup, easy badass execution.</b> The monster is huge AND it's the BABY. Mother is still out there."))
story.append(B('<b>Deadpan commentary during the absurdity.</b> "Look at that, the monster\'s trying to mate with Lady Hair." No reaction to the weirdness. Just observation.'))
story.append(B("<b>Nicknames stick instantly and forever.</b> Brad becomes Lady Hair. Big guy becomes Big Moist. They never go back."))
story.append(B("<b>Redshirts have personalities bigger than their screen time.</b> This is why their deaths land."))
story.append(B("<b>Heroes don't acknowledge the weird.</b> Universe is increasingly absurd around them. They register only the part relevant to mission."))
story.append(B("<b>Erica names what they refuse to.</b> When she's there. Audience surrogate."))
story.append(B("<b>Steffin's casual dismissal is comedy gold.</b> Whenever Steffin is offhand about something terrifying, the joke lands."))
story.append(B("<b>Escalation tease at scene end.</b> The monster was the BABY. Some episodes pay off the escalation, others never do. Both are funny."))

# ===== 16. MYTHOLOGY =====
story.append(P("16. Series-Long Mythology Threads", h1))
story.append(B("<b>The Master's Belt</b> — soul cycling through forms. Killed by accident in Season 1 Episode 4 (as a redshirt). Heroes carry its karmic debt unknowingly. Series-finale-level reveal."))
story.append(B("<b>The Ash Belt Brotherhood</b> — Simon as unwitting leader of a hidden network of former killers. Galactic gathering revealed Season 4."))
story.append(B("<b>The Mirror Dimension Evolution</b> — mirrors get smarter and weirder each appearance. Audience starts wondering if they're the GOOD versions."))
story.append(B("<b>The Diamond Ladder</b> — climbing the Drip ranks as season-long power architecture."))
story.append(B("<b>Erica's True Rank</b> — secret Platinum Belt, revealed Season 3 or 4."))
story.append(B("<b>The Single Laugh</b> — series finale moment when all four laugh together for the first and only time. The cathartic release the contract earns over seven seasons."))

story.append(PageBreak())

# ===== 17. EPISODE TREATMENTS =====
story.append(P("17. Full Episode Treatments", h1))
story.append(P("Nine episode treatments developed in full beat-sheet form. Each follows the structure: Cold Open, Setup, Complication, Fight Beats, Climax, Callback.", body))

# Episode 01
story.append(P("EP 01: \"THE BAT AND THE BOROUGH\" — Brek-7 (PILOT)", h2))
story.append(P("<b>COLD OPEN.</b> The Lady Hair monster-mating scene. Two redshirts die in the first ten seconds (Kai #1 is one). Beast turns on Lady Hair. Tries to mate. Steffin dispatches with one elbow. <i>'That's the baby. Let's find its mother.'</i> Title card. Rap beat drops.", body))
story.append(P("<b>SETUP.</b> Brek-7 is run by warring crime-lords who settle territory by rap battle. Ronin hired by a neutral coalition to take down VESPER BLOODFANG (Silver Iced, 29/11 Master shadow). Bat warlord with diamond-studded sonar wings.", body))
story.append(P("<b>COMPLICATION.</b> Bloodfang challenges Steffin to a rap battle. Steffin: 'Rap is not the way of the warrior.' Erica steps forward. 'I'll do it.'", body))
story.append(P("<b>THE BATTLE.</b> Erica vs. Bloodfang. Three rounds. She humiliates him in round three with a verse naming every borough he's stolen. Crowd loses its mind. Bloodfang refuses to honor the loss.", body))
story.append(P("<b>THE FIGHT.</b> Jordan vs. Bloodfang. Sonar Strike vs. Thirty-Six Crows. Bloodfang's diamond-studded wings shatter under elbows (the diamonds were stress-bearing). Finishing move: Heart-Tap.", body))
story.append(P("<b>ZAP & GLITCH DEBUT.</b> Observe loss in slow-motion. 30 seconds of silence. Pivot to a Diamond Iced lord in the crowd. Hand him a business card.", body))
story.append(P("<b>LAST LINE.</b> Simon: <i>'The girl with the words. She broke him with words. I do not understand the words. But I felt them.'</i>", body))

# Episode 02
story.append(P("EP 02: \"BROTHER OF THE HIVE\" — Hexapod-9", h2))
story.append(P("<b>COLD OPEN.</b> Insect envoy lands at the dojo. Lady Hair tries to shake its hand. Envoy attempts to mate with Lady Hair. Steffin: 'Not now, Lady Hair. We have business.' Lady Hair: 'He started it.'", body))
story.append(P("<b>SETUP.</b> Hexapod-9 hires the Ronin to mediate a hive succession. Queen VESPRYNNE (40/4 Emperor) is dying. Two princess-claimants. Steffin offered the arbitrator role.", body))
story.append(P("<b>COMPLICATION.</b> Hive law requires the arbitrator to challenge the dying Queen in single combat. Steffin agrees. Prepares two days. Dojo trains for insect combat. Drop-Kick Darius drop-kicks a giant cricket through a wall.", body))
story.append(P("<b>THE TWIST.</b> Queen does not raise her claws. She begins a mating dance. Steffin freezes one frame. Performs it flawlessly back. Hive erupts.", body))
story.append(P("<b>THE FIGHT.</b> Vespryne's daughter GROXX (22 / Master Builder) rejects Steffin's selection. Zero-gravity duel inside the royal chamber while the hive sings a coronation song. Steffin wins with Seven Towers Falling.", body))
story.append(P("<b>CLIMAX.</b> Vespryne dies. Final breath: 'Brother.' Hive erupts in tearful chittering. Steffin is now a brother of the hive forever.", body))
story.append(P("<b>CALLBACK SETUP.</b> Insect courier hands Steffin mating-dance invitations from other hives. Future episodes — hive emissaries show up calling him 'Brother.'", body))
story.append(P("<b>LAST LINE.</b> Erica: 'You know your dance was technically a marriage proposal.' Steffin: 'I am aware. I am also a married man on Hexapod-9 now.'", body))

# Episode 04
story.append(P("EP 04: \"THE KOAN WAR\" — Senshara", h2))
story.append(P("<b>COLD OPEN.</b> Two old masters argue in a tea garden for forty years. 'The bird does not perch on the tongue of the dead snake.' 'BUT THE SNAKE WAS NEVER DEAD!' They strike each other once. Both fall. Both rise. Drink tea.", body))
story.append(P("<b>SETUP.</b> Civil war between Tiger House (Hard/Mars), Crane House (Soft/Saturn), and Otter House (Internal/Neptune — emotional vibration fighters). Ronin hired to mediate.", body))
story.append(P("<b>COMPLICATION.</b> Steffin → Crane. Jordan → Tiger. Three days of training each. Both return absorbing each other's philosophy and arguing on the ship. Erica refuses to arbitrate.", body))
story.append(P("<b>OTTER HOUSE.</b> Simon is drawn to Otter because they cry during combat. MASTER YONA (14/5 KD Temperance) teaches him 'The Strike That Weeps.' Technique requires a wound to be taught.", body))
story.append(P("<b>KOANS.</b> Heroes nod solemnly at every koan. Erica narrates to camera: 'He's telling them to stop arguing and eat breakfast. They think he's revealing the secret of the universe.'", body))
story.append(P("<b>THE TOURNAMENT.</b> Jordan represents Tiger. Steffin represents Crane. Simon represents Otter. Cherry petals, slow drum-rap. Simon wins with the Strike That Weeps — both Jordan and Steffin fall to grief they cannot block. Otter House becomes canonical lineage.", body))
story.append(P("<b>LAST LINE.</b> Master Yona to Simon: 'You will return. You have not finished weeping.' Simon: 'I have observed: the wind is also a kind of grief.' Yona, after a long pause: 'YES.'", body))

# Episode 05
story.append(P("EP 05: \"PERMITS AND PUNCHES\" — The Bureau Planet", h2))
story.append(P("<b>COLD OPEN.</b> Long bureaucratic line. Exasperated warrior: 'It's been six MONTHS, can I PLEASE punch him now.' Clerk: 'Form 71-A is required for kicks. Form 71-B for punches. You filed 71-AB. That form does not exist.'", body))
story.append(P("<b>SETUP.</b> Burocratos-7 — martial arts illegal without permit. Hired by MELVIN OF ACCOUNTS RECEIVABLE (24/6) to defeat Permit Director DROSS (19/1 KD Sun, Diamond Iced). Dross wears diamond-studded reading glasses.", body))
story.append(P("<b>COMPLICATION.</b> Combat Permit 9-Alpha is 47 pages. Steffin fills it out with solemnity. Jordan denied for missing notarization. Simon rejected — robots not classified as combatants under Section 14.", body))
story.append(P("<b>THE BUREAUCRATIC FIGHTS.</b> Each fight requires its own permit. Each permit expires mid-fight. Steffin pulled out of active combat by a clerk at the 9-minute mark. Returns 40 minutes later, resumes mid-strike.", body))
story.append(P("<b>SIMON B-PLOT.</b> Spends episode in Robot Classification Office. Asked to prove personhood. Delivers quiet monologue about his garden. Clerk weeps. Approves Class-A Combatant Permit. Simon uses it once: Tactical Embrace on a guard.", body))
story.append(P("<b>THE BOSS.</b> Dross fights from behind his desk — bureaucratic ritual. Throws filing cabinets. Finishing move: INDEFINITE PENDING REVIEW — pins under paperwork until suffocation. Jordan defeats him by filing a counter-permit naming Dross's denial as unlawful obstruction. Dross legally bound to process it. He processes himself into his own resignation. Jordan elbows him over the desk.", body))
story.append(P("<b>LAST LINE.</b> Steffin: 'The form became the weapon. The form became the warrior. The form was the way.' Erica: 'You're going to need to file a Form 92-C for the exit clearance.' They turn around.", body))

# Episode 07
story.append(P("EP 07: \"THE FAKE WEEPING\" — Vanguard-9", h2))
story.append(P("<b>COLD OPEN.</b> Big Moist's funeral. Simon's eulogy. Brief, devastating. Cut to Vanguard-9: a Mortician-Monk weeping over a stranger. Camera pulls back: he is being PAID to weep.", body))
story.append(P("<b>SETUP.</b> Ronin must retrieve the soul of DROP-KICK DARIUS, misfiled into the wrong tomb. The Gray Choir of Mortician-Monks offers help for a fee.", body))
story.append(P("<b>COMPLICATION.</b> Steffin delivers a 40-minute eulogy for Darius before retrieval. Monks weep ostentatiously. Lay flowers. Tear robes. Wail. Steffin is deeply moved.", body))
story.append(P("<b>THE TWIST.</b> Erica catches them backstage. They are laughing. Drinking. Comparing tears-per-minute. 'My average is 8.7, you?' 'I cried over the toaster eulogy yesterday so I'm rested.' Erica films them.", body))
story.append(P("<b>THE FIGHT.</b> HIGH MOURNER ZEPH (25/7 Mystic, Sapphire Iced funeral-jewelry) runs a soul-trafficking ring. Fights with censer-flail and mourning veil that absorbs strikes. Finishing move: 'The Endless Lament' — sustained wail that destabilizes opponents emotionally. Simon nearly succumbs because his grief is real. Triple-team take-down: Channel Strike + Captain's Silence + Apology.", body))
story.append(P("<b>RESOLUTION.</b> Erica plays the backstage video to the citizens. Scandal explodes. Gray Choir disbanded. Heroes' actual mourning canonized as the new standard. Steffin gets honorary Mortician-Monk title.", body))
story.append(P("<b>LAST LINE.</b> Simon: 'The weeping was not real. The weeping I gave for Big Moist was real. I felt the difference. I do not know how to teach it.' Steffin: 'You don't teach it. You earn it.'", body))

# Episode 08
story.append(P("EP 08: \"VELCRO\" — Tribunal Prime", h2))
story.append(P("<b>COLD OPEN.</b> Tribunal warrior performs 12-step pre-combat bow. Eight minutes of bowing. Combat lasts four seconds. Then six more minutes of bowing.", body))
story.append(P("<b>SETUP.</b> Diplomatic envoy mission. Steffin is in heaven — every protocol, every code. Court takes to him. Offers honorary lordship. He accepts in a 90-minute ceremony.", body))
story.append(P("<b>ERICA DISASTER.</b> Dragged along as pilot. Bored, hot. Removes ceremonial shoes during a banquet IN THE WRONG COLOR ORDER. This is a declaration of war on the host's bloodline.", body))
story.append(P("<b>THE CRISIS.</b> Three Tribunal warriors challenge Erica to a duel of honor. Steffin: 'Erica. You have shamed our line by removing your shoes in the wrong color order.' Erica: 'Captain, the shoes were Velcro.' Steffin: 'VELCRO IS NOT A DEFENSE.'", body))
story.append(P("<b>ERICA'S FIGHT.</b> Defeats all three with The Inversion. Court is stunned — they were told she was the pilot. Steffin sees her fight for the first time and is wordlessly impressed. He does not bring it up afterward.", body))
story.append(P("<b>JORDAN B-PLOT.</b> Koan competition. Places third. Judges baffled by his straightforward answers. 'Why does the dragon sleep on the mountain?' Jordan: 'Because the mountain is comfortable.' Judges weep. Bronze.", body))
story.append(P("<b>BOSS FIGHT.</b> LORD VEX SILVERTOOTH (Diamond Iced, KD 16/7 Tower) interrupts the ceremony. Code-bound combat — every strike announced. Steffin announces Saturn Return. Vex announces Diamond Storm. They clash. Steffin wins with The Mystic Pin — ground hold while explaining what Vex did wrong over 14 minutes.", body))
story.append(P("<b>LAST LINE.</b> Erica: 'That place was a museum with a dress code.' Steffin: 'It was the most beautiful planet I have ever been on.' Long beat. Erica: '...The shoes were Velcro.'", body))

# Episode 09
story.append(P("EP 09: \"LIGHTEN UP\" — Synara", h2))
story.append(P("<b>COLD OPEN.</b> Two combat-AIs locked in a fight for 80,000 years. Both adapt. Neither wins. They have a calm conversation about how nothing in their styles works against each other. They keep fighting anyway.", body))
story.append(P("<b>SETUP.</b> Synara run by TALOS-9 (18/9 Moon). Ronin hired to retrieve stolen tech from CEO PRAX (16/7 KD Tower, Diamond Iced) who has hacked Talos-9's core.", body))
story.append(P("<b>COMPLICATION.</b> Every opponent on Synara accesses Talos-9's adaptive combat database. Heroes lose every preliminary fight.", body))
story.append(P("<b>THE AI'S OFFERINGS.</b> Talos-9 keeps suggesting 'Lighten Up' as tactical advice. Subtitled. Simon is offered friendship. He accepts. Talos-9 sends Simon a poem.", body))
story.append(P("<b>THE FIGHT.</b> Prax uses predictive combat — knows what heroes will do half a second early. Heroes losing badly. Talos-9, having befriended Simon, quietly stops feeding Prax data. Prax loses his edge mid-fight. Jordan elbows him into next week.", body))
story.append(P("<b>ZAP & GLITCH.</b> Hyping Prax all wrong. Yelling 'BOSS LEVEL MOVE' when Prax misses. After loss, immediately pivot to Jordan and Steffin offering services. Heroes refuse. Z&G leave business cards.", body))
story.append(P("<b>REVEAL.</b> Talos-9 explains: heroes lost all preliminary fights because they refused 'Lighten Up.' Data shows comedy integration raises win rate 340%. Heroes thank Talos-9 for the data. They will not integrate humor. They depart.", body))
story.append(P("<b>TALOS-9 FILES UPDATE.</b> 'Subjects classified: voluntarily suboptimal. Maintain monitoring. Hypothesis: integrated comedy will arrive externally. Subject Simon is the variable to watch.'", body))
story.append(P("<b>LAST LINE.</b> Simon, reading Talos-9's poem to the garden: 'The wind is also a kind of friendship. I have a new friend. He is a planet.'", body))

# Episode 11
story.append(P("EP 11: \"THE LAUGHTER WAS THE BATTLEFIELD\" — Hilarius IV", h2))
story.append(P("<b>COLD OPEN.</b> Hilarius IV warrior in combat stance. Begins laughing uncontrollably. Falls. Still laughing.", body))
story.append(P("<b>SETUP.</b> Population on GIGGLEDUST — substance that makes anyone not on it appear absurd. Heroes arrive. Locals begin laughing immediately.", body))
story.append(P("<b>THE TACTICAL MISREAD.</b> Steffin interprets the laughter as a battle-shame technique. 'They are using mockery as a weapon. Hold the line.' Heroes walk with EVEN MORE solemnity. Laughter intensifies. Steffin: 'They are weakening. Our resolve is breaking them.'", body))
story.append(P("<b>THE MISSION.</b> BARON GIGGLES (Sapphire Iced, 33/6 Master shadow) mass-produces giggledust and traffics it galaxy-wide.", body))
story.append(P("<b>SIMON.</b> Doesn't get giggledust. Unaffected. Registers locals' laughter as joy and is PLEASED. 'I like this planet. The beings are happy.' Waves at every laugher. They laugh harder.", body))
story.append(P("<b>THE FIGHT.</b> In a candy-pink factory shaped like a clown's face. Heroes vs. dust-pumped warriors laughing while fighting. Steffin uses Captain's Silence. Guard laughs. Steffin maintains silence. Guard's laughter becomes uncomfortable. Guard surrenders to escape the silence.", body))
story.append(P("<b>JORDAN GETS DUSTED.</b> Baron Giggles's seltzer bottle fires giggledust into Jordan's face. JORDAN BEGINS TO LAUGH. For the first time in the series. Other heroes stop fighting. They watch. Erica is filming.", body))
story.append(P("<b>RECOVERY.</b> Jordan recovers after 90 seconds. Wipes eyes. Rises. 'That was an effective weapon. I will report you to the appropriate authorities.' Heart-Tap. Giggles is down.", body))
story.append(P("<b>EMOTIONAL BEAT.</b> Erica saves the footage of Jordan laughing. 'For the finale.'", body))
story.append(P("<b>LAST LINE.</b> Locals high-five heroes leaving. Steffin: 'They are conceding the war by saluting our exit.' Erica: 'They are not.'", body))

# Recurring: Empire of Polish
story.append(P("RECURRING ARC: \"THE EMPIRE OF POLISH\" — Multi-episode", h2))
story.append(P("Emperor PROCTOR (33/6 Master Teacher in shadow, DIAMOND ICED) appears periodically with increasingly elaborate tech-army incursions. Each appearance the tech is bigger. Each appearance heroes humble it with basic martial arts. Proctor cannot understand his own failure.", body))
story.append(P("Key arc episodes:", body))
story.append(B("<b>'The LARPers'</b> — First appearance. Mech-warrior squad destroyed by elbows. Proctor files loss as 'anomalous,' funds bigger squad."))
story.append(B("<b>'The Singularity Mech'</b> — City-sized AI mech. Heroes climb it. Steffin breaks the core with one strike."))
story.append(B("<b>'The Maker'</b> — Proctor meets Simon. Addresses Simon as property. Simon: 'I am Simon. I have decided. I am not yours.' Simon turns and leaves. Proctor sits in wreckage."))
story.append(B("<b>'Sticks and Diamond'</b> — Season finale. Diamond Citadel planet-killer. Heroes assault with wooden sticks. Defeat Proctor with stance, breathing, footwork. Steffin gives him one piece of advice: 'Lighten up.'"))
story.append(B("<b>Post-defeat recurring</b> — Returns as a minor nuisance, no longer Diamond, wearing shameful Silver. Heroes spare him every time. Pitiable."))

# ===== END NOTE =====
story.append(PageBreak())
story.append(P("END OF WORKING DRAFT", h1))
story.append(P(
    "This bible is a living document. Every name added to the show should be Chaldean-checked. "
    "Every date in production should be Personal-Day calculated against Jordan's chart. "
    "The Drip System carries Pinnacle 8 weight at the Diamond tier — every Diamond Iced fight is the "
    "operator facing the dark mirror of his own material-mastery period (2026-2034)."
, body))
story.append(SPACE(0.3))
story.append(P(
    "<b>Cosmic note:</b> This document was compiled on May 30, 2026 — Personal Day 9 (Moon), Day 30 of the Beltane working "
    "(Empress day). The creative manifestation work of writing the bible is itself the boots-on-the-ground for the day's cosmic frame."
, quote))
story.append(SPACE(0.3))
story.append(P("Written by Claude on behalf of Jordan Ross Atkins. For Space Kwon Do.", subtitle_style))

# ---------- Build ----------
output_path = '/home/user/numenist-site/space-kwon-do/space-kwon-do-bible.pdf'
doc = SimpleDocTemplate(
    output_path, pagesize=letter,
    leftMargin=0.85*inch, rightMargin=0.85*inch,
    topMargin=0.85*inch, bottomMargin=0.85*inch,
    title="Space Kwon Do — Show Bible",
    author="Jordan Ross Atkins"
)

doc.build(story)
print(f"PDF written: {output_path}")
