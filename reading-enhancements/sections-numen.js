/* ============================================================
   NUMEN SECTIONS — production overlay data
   Keyed by the engine's actual section.id values, matching the
   schema stored in public.astrology_readings_cache.reading_json
   on Supabase project tuayjblcwswcmtuhoucv.

   Use:
     <script src="numen-enhancements.js"></script>
     <script src="sections-numen.js"></script>
     <script>
       NumenEnhancements.init({
         sectionContainer: '[data-section-id]',
         sectionTitle:     'h2',
         pageContainer:    '.reading-page',
         mountTopAfter:    '.reading-masthead',
         user:  { … },
         chart: { … },
         sections: window.NUMEN_SECTIONS  // <- this file's export
       });
     </script>

   Each entry is the OVERLAY only — the engine's existing per-section
   prose is left untouched. The Light/Shadow panel and the Working
   are APPENDED beneath the engine's paragraphs.

   Voice rules followed: warm, observant, grounded, precise. No
   sycophancy. No "I'd be careful". The lineage alive in the speaking.
   ============================================================ */

(function(global){
  const T = '︎';

  const NUMEN_SECTIONS = {

    'overview-combined': {
      hermetic: { glyph: '∞', name: 'Correspondence' },
      light:  'Treated as one reading, not nine systems stapled together. The Pythagorean number, the Hellenistic sect, the BaZi pillar, and the Zi Wei palace all describe the same soul through different instruments. When they converge, the convergence is the message. When they diverge, the divergence is the deeper message — each instrument reads the layer it is built for.',
      shadow: 'The temptation is to use the glance to feel finished. The hook is not the work; it is the doorway. Reading only the overview and skipping the sections below collapses a 15-instrument resonance into a tagline. Sit with each section in its own time.',
      working: {
        text:   'Read this page once at the start, then read it again at the end. The same words will land differently after the deeper sections have done their work. That difference IS the reading completing in you.',
        glyphs: '∞ ✶ ☉'+T+' ☾'+T
      }
    },

    'opening': {
      hermetic: { glyph: '⌖', name: 'Correspondence' },
      light:  'The sky at first breath is a contract that does not expire. Every transit you will ever live is the natal sky meeting the current sky, and the natal sky is the constant. Knowing it precisely — Pisces Sun in the 7th, Pisces Moon in the 7th, Virgo rising — turns every future weather report into a weather report ABOUT YOU.',
      shadow: 'Treating the natal chart as fixed fate is the trap. The chart names the instruments you were handed. What you play on them is the work. Read this section as inheritance, not sentence.',
      working: {
        text:   'Find a window facing the direction of your birth (for Flint, north-by-northwest from most US locations). Stand at it for three breaths at the time of day you were born. Speak the line: "I receive what I was given. I am the steward, not the script." That is the consecration of the chart.',
        glyphs: '✶ ☉'+T+' ☾'+T+' ↑'
      }
    },

    'sect-lights': {
      hermetic: { glyph: '☉'+T, name: 'Polarity' },
      light:  'A diurnal Pisces chart is rarer than it sounds. Pisces is the most lunar of the signs, and yours runs through a solar (day) chart — the receptive water given the active fire to move it. Jupiter sect-benefic blesses the larger pattern; Mars in-sect is sharper but still on your side; Saturn out-of-sect is the harder teacher whose lessons cost more but cut deeper.',
      shadow: 'Day-sect Pisces still carries the lunar reflex — wanting to dissolve, to merge, to let the boundary go soft. The sect calls for daylight clarity over the watery substrate. When you default to lunar-mode (withdrawing, absorbing, deflecting), you are running the chart backwards. The Sun is the chair of authority here, not a guest.',
      working: {
        text:   'At sunrise once a week, name aloud one thing your Sun (your will, your authority, the seat of the I) is responsible for today. Not your Moon (the felt-sense), not your Mercury (the explanation) — your Sun. Repeat for forty days. The chair learns to sit.',
        glyphs: '☉'+T+' ♓'+T+' ♃'+T+' ✶'
      }
    },

    'ascendant-lord': {
      hermetic: { glyph: '♍'+T, name: 'Cause & Effect' },
      light:  'Virgo rising at 18°27\' makes Mercury the steward of the whole life. The chart-ruler is your operating budget — wherever Mercury sits, that house\'s affairs lead. Virgo on the horizon also asks for precision as a way of love: the person who notices the small thing, names it, fixes it, and keeps going. That noticing is the rendering of service Virgo is built for.',
      shadow: 'Virgo rising can collapse into chronic self-correction — the inner editor that never stops marking up the draft. Service becomes performance, and the precision becomes a way of staying inside the cage of "not yet good enough." Mercury\'s rulership has to come HOME to the body, not run loops in the head.',
      working: {
        text:   'Once a day, do ONE small precise thing for its own sake — sharpen a knife, refold a stack, write one clean sentence — then walk away from it without inspecting the result. That is Virgo rising healing. The work is the offering, not the proof.',
        glyphs: '♍'+T+' ☿'+T+' ✶ 🕯'+T
      }
    },

    'personal-planets': {
      hermetic: { glyph: '☿'+T, name: 'Vibration' },
      light:  'Mercury in Aries 8th is a mind that thinks in initiating fire about hidden things — the chart-ruler placed in the house of death, sex, joint resource, depth. You think into what others avoid. Venus and Mars round out the personal instruments: how you love, how you go after. Each is a finger on the chord.',
      shadow: 'Aries Mercury can speak before it thinks; the 8th house emphasis means what you blurt has TEETH. Notice when the urgency to say it now is the 8th house wanting to be witnessed, not the truth wanting to be told.',
      working: {
        text:   'When the impulse to say a sharp thing arrives, hold the breath for three counts before opening the mouth. If the sentence still wants to come out at count three, it earns the right to be said. If it has dissolved, it was Mars firing through Mercury looking for a target.',
        glyphs: '☿'+T+' ♀'+T+' ♂'+T+' ✶'
      }
    },

    'social-planets': {
      hermetic: { glyph: '♃'+T, name: 'Rhythm' },
      light:  'Jupiter Leo 12th retrograde — your sect-benefic in the house of the unseen, the monastery, what dissolves the self. The expansion happens inwardly first, in solitude, in spirit-work, in the hour nobody sees. Saturn in the 6th house teaches through daily work, daily body, daily routine — and as day-sect malefic, it teaches more than it punishes.',
      shadow: 'A 12th house Jupiter retrograde can mean the gift hides from itself — you give to the unseen and forget to claim what is rightfully yours in the seen world. Saturn in the 6th can become chronic self-discipline that hardens into self-punishment. Both are the same trap: forgetting that the work serves YOU, not the other way around.',
      working: {
        text:   'Once a week, schedule one hour of UNWITNESSED practice — solo, no document, no record, no proof. Pray, draw, sing, walk, sit. The 12th house Jupiter eats this way. Then, separately, claim one specific Saturn boundary out loud (a stop time, a no, a rate). The two together feed each other.',
        glyphs: '♃'+T+' ♄'+T+' ✶ 🕯'+T
      }
    },

    'outer-planets': {
      hermetic: { glyph: '♅'+T, name: 'Vibration' },
      light:  'The outer planets carry a generation\'s signature. Yours sit where they sit — Uranus & Neptune in your 5th house of creativity, Pluto in your 3rd of the daily mind — and become personal where they touch your lights or angles. Read them as the assignment your cohort came in carrying that landed specifically on YOUR creative voice and YOUR thinking-speaking apparatus.',
      shadow: 'Outer-planet pressure on the 3rd and 5th can read as "my thinking is too weird, my creativity is too far out." That is the cohort\'s assignment, not your flaw. The trap is calling the assignment a defect and quieting it. The cohort needs the voice it was given.',
      working: {
        text:   'Once a month, make something for the cohort, not for the algorithm. A drawing, a verse, a recording — addressed to the people walking the same generational assignment. Send it to one person directly. That is how outer-planet generational signal becomes personal vocation.',
        glyphs: '♅'+T+' ♆'+T+' ♇'+T+' ✶'
      }
    },

    'nodes-chiron': {
      hermetic: { glyph: '☊', name: 'Cause & Effect' },
      light:  'The nodal axis names the soul\'s longitudinal arc — South Node Cancer 11th (the gift already mastered: protective community-tending), North Node Capricorn 5th (the growth-edge: structured creative authority, the throne in your own arena). Chiron names where the wound and the medicine sit in the same spot.',
      shadow: 'Falling back on the South Node — the Cancer 11th comfort of caring for the group, defending the tribe — feels safe but stops the soul\'s actual assignment. The North Node Capricorn 5th asks you to TAKE the chair of your own creative authority, not just protect the room others are creating in.',
      working: {
        text:   'Every Wednesday, do ONE Capricorn-5th move: claim authorship of something publicly. Sign the work. Set the price. Name the project as yours. The South Node will protest. Do it anyway. The protest is the muscle being asked to stretch.',
        glyphs: '☊ ☋ ⚷ ✶'
      }
    },

    'configurations': {
      hermetic: { glyph: '△', name: 'Correspondence' },
      light:  'Fire 21 · Earth 29 · Air 14 · Water 36, mostly Mutable. You are a water-dominant mutable chart — built to feel deeply and to translate across forms. The 14% Air is the assignment, not the deficiency: every year you build air is an upgrade to a system already strong in everything else.',
      shadow: 'Water-dominant means feeling first, naming later — sometimes much later. Low air means perspective and detachment do not arrive on their own; they must be practiced into. The trap is treating the air-deficiency as a personality fact instead of a trainable muscle.',
      working: {
        text:   'Three days a week: ten minutes of writing in third person about your own present situation. "Jordan is feeling X. The pattern is Y. The next move is Z." That is air being built. Do it for ninety days. The lift is real.',
        glyphs: '△ ▽ ◯ ✶'
      }
    },

    'timing': {
      hermetic: { glyph: '⌛'+T, name: 'Rhythm' },
      light:  'The 12th-house profection year activates dissolution, solitude, the unseen, and surrender — and the Lord of the Year is your natal Sun in Pisces 7th. The whole year speaks through the 7th-house relating field but the texture is 12th: hidden currents, withdrawal-as-practice, the partner you don\'t see clearly because the lens is the lens itself.',
      shadow: '12th-house years invite the false read that nothing is happening because nothing is visible. A great deal is happening, all of it submerged. The trap is measuring this year by visibility metrics. The proper measure is by depth of the unseen work — the dreams, the prayers, the silences, the quiet pulls.',
      working: {
        text:   'Keep a brief dream-log this year. One line on waking, no interpretation in the moment. Read the log monthly. The 12th-house Lord of the Year speaks loudest there — not in the meetings, not in the metrics, in the symbols that came when you were not steering.',
        glyphs: '⌛'+T+' ☉'+T+' ♓'+T+' ✶'
      }
    },

    'four-pillars': {
      hermetic: { glyph: '四', name: 'Correspondence' },
      light:  'Year 辛未 (Metal Goat) · Month 辛卯 (Metal Rabbit) · Day 甲申 (Yang Wood Monkey, your Day Master) · Hour 癸酉 (Yin Water Rooster). Jiǎ 甲 Yang Wood Day Master born in spring (卯 Rabbit month, Wood\'s seat) is a tree planted in its own season — naturally strong, naturally rising, designed to grow tall enough to carry weight.',
      shadow: 'Jiǎ Wood\'s shadow is rigidity disguised as principle — the tree that will not bend, that snaps in the storm rather than yield. Strong Day Masters trap themselves with their own straightness. The Useful God for your chart (resolved in the next section) is the medicine for exactly this stiffness.',
      working: {
        text:   'Once a week, do ONE thing the way someone else asked instead of the way your principle says. Not a moral compromise — a small structural yield. Eat at their preferred restaurant. Take their suggested route. Notice what the bending teaches. Jiǎ Wood with controlled flexibility is harder to break, not softer.',
        glyphs: '甲 申 ✶ 🕯'+T
      }
    },

    'day-master-ten-gods': {
      hermetic: { glyph: '日', name: 'Vibration' },
      light:  'Day Master strength assessment is the gate to BaZi. Once the Useful God is named, the chart becomes operational: you know which element to feed, which to drain, which to invoke under stress. This is the most actionable section in Eastern metaphysics — its conclusion changes daily life, color choices, direction-facing, and timing of moves.',
      shadow: 'The temptation is to nod along with the analysis and never APPLY it. A named Useful God that does not change the color you wear, the direction you sleep facing, the season you plan launches in — is theory pretending to be a working.',
      working: {
        text:   'Pick ONE concrete application from this section and implement it this week: a color in your daily clothing, a direction you face during morning practice, a kitchen object in the corresponding compass position. The body learns the element through repetition. The chart starts to operate.',
        glyphs: '✦ 木 ✶ 🕯'+T
      }
    },

    'zi-wei-stars': {
      hermetic: { glyph: '紫', name: 'Mentalism' },
      light:  'Zi Wei is the soul-level companion to BaZi\'s fate-mechanics. Where BaZi answers "what and when," Zi Wei answers "who is this soul." The 12-palace grid maps the architecture of identity, relationship, vocation, and fortune as STRUCTURE, not motion.',
      shadow: 'Zi Wei\'s richness can become a place to LIVE — palace-mapping every relationship until the maps replace the relationships. The chart is a doorway, not a dwelling. Read, integrate, return to people.',
      working: {
        text:   'Look at your Life Palace (命) and Body Palace (身) only this week. Sit with those two. Don\'t open the others until next week. Slow consumption of Zi Wei is how it lands; fast consumption is how it stays decorative.',
        glyphs: '紫 微 ✶ ☆'
      }
    },

    'da-yun-timing': {
      hermetic: { glyph: '運', name: 'Rhythm' },
      light:  'Da Yun (10-year Luck Pillars) and Liu Nian (annual pillar) are the BaZi answer to Hellenistic profections. They give you the seasonal weather. The cross-check — when Da Yun and profection point at the SAME themes — is gold-standard timing intelligence.',
      shadow: 'Timing techniques invite over-planning the future at the cost of being present to what is here. "When Da Yun changes, I\'ll —" is a sentence that can defer a decade. The pillars open doors; you have to walk through.',
      working: {
        text:   'At each Da Yun change-over, write a one-page letter to your future self for the new pillar — what you commit to enter into, what you commit to leave. Seal it. Read it the day after the pillar ends. That is the closing of the loop the system was designed for.',
        glyphs: '運 ✶ 🕯'+T+' ☆'
      }
    },

    'east-west-synthesis': {
      hermetic: { glyph: '⊕', name: 'Polarity' },
      light:  'Where Western Pisces-7th Sun and BaZi Jiǎ Wood Day Master AGREE: both speak of a soul whose work is consummated through encounter — the tree that grows visible to and through others. Where they DIFFER: Western reads the encounter as relational mirror (7th house), BaZi reads it as resource for growth (Jiǎ Wood absorbing what the surroundings provide). Both are true; they are reading different layers.',
      shadow: 'The synthesis can be over-quoted to feel like understanding without integrating. The point of the closing section is to NAME the through-line, then act on it. Without action it is decoration.',
      working: {
        text:   'Write one sentence — exactly one — that names the through-line of this whole reading in your own voice. Tape it where you brush your teeth. Read it twice daily for forty days. That is how a 15-section reading becomes a soul-operating-instruction.',
        glyphs: '⊕ ✶ ☉'+T+' 甲'
      }
    }
  };

  global.NUMEN_SECTIONS = NUMEN_SECTIONS;
})(window);
