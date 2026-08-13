# Numen Reading Enhancements — drop-in overlay

An **additive-only** layer that adds ten features to an existing Numen
astrology reading page **without removing, rewriting, or restyling a single
line of the reading that's already there.** Every selector is prefixed `.nx-`
so it cannot collide with the live page's CSS. No existing DOM node is
deleted; the script only *inserts* alongside what already renders.

Self-contained: ships its own fonts (Cormorant Garamond + Inter), so no
external network calls and identical typography on every environment.

## Drop it in (two lines + one call)

```html
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="numen-enhancements.css">
<script src="numen-enhancements.js"></script>
<script>
  NumenEnhancements.init({
    sectionContainer: '.reading-section',   // selector for each section block
    sectionTitle:     'h2',                 // heading inside it
    pageContainer:    '.reading-page',      // outer wrap
    mountTopAfter:    '.reading-masthead',  // optional: chrome lands AFTER this
    pageNumber:       2,

    user:  { name:'Maverick', dob:'1990-03-12', lifePath:11, expression:9 },
    chart: {
      sun:  { sign:'Pisces', deg:24.87, house:7 },
      moon: { sign:'Pisces', deg:20.12, house:7 },
      asc:  { sign:'Virgo',  deg:18.45 }
    },

    // OPTIONAL: per-section copy. sections[i] applies to the (i+1)th section.
    sections: [
      {
        hermetic: { glyph:'☾︎', name:'Polarity' },
        light:    'real per-section light-gift copy',
        shadow:   'real per-section shadow-trap copy',
        working:  { text:'real ritual copy', glyphs:'☾︎ ✶ 🕯︎' }
      },
      // ...one entry per section the engine wants to fill
    ]
  });
</script>
```

Open `demo.html` in a browser to see the full integrated result. That file
is the preview — it is **not** the product; it exists so the overlay can be
tested against a faithful replica of a reading page before it touches the
live engine.

## The ten features

| # | Feature | Where it lands | Data it needs |
|---|---------|----------------|----------------|
| 1 | Light / Shadow polarity panel | end of each section | `sections[i].light/shadow` (else scaffold) |
| 2 | Hermetic principle badge | beside each section title | `sections[i].hermetic` (else built-in map) |
| 3 | Tarot correspondence chips | under each section title | `chart` (auto) or `sections[i].chips` override |
| 4 | Constellation panel ("your sky at first breath") | top of page | `chart` (sun/moon/asc) — real per-sign stick figures |
| 5 | The Working — boots on the ground | end of each section | `sections[i].working` (else scaffold) |
| 6 | Personal Day banner (live, with Tarot) | top of page | `user.dob` + today |
| 7 | Natal chart wheel | top of page | `chart` — real 12 signs, 12 houses, planets at true degrees |
| 8 | Audio "listen" bar | top of page | (UI only — bind a source separately) |
| 9 | Chaldean numerology chip | under each section title | `user.expression` |
| 10 | Resonance map (BaZi pillars ⟷ Western houses) | end of page | currently placeholder pillars |

## Config

| Key | Default | Meaning |
|-----|---------|---------|
| `sectionContainer` | `.reading-section, [data-section], section.reading` | selector for one section block |
| `sectionTitle` | `h2` | the heading element inside a section |
| `sectionBody` | `p` | the prose inside a section |
| `pageContainer` | `.reading-page, .page-content, main` | the outer wrap |
| `mountTopAfter` | `null` | if set, the top chrome (banner/audio/duo) is inserted AFTER this element instead of at the top of the page — use to keep your masthead first |
| `pageNumber` | `2` | which page (1–15) is current |
| `user` | placeholder | `{ name, dob:'YYYY-MM-DD', birthHour:0-23 (optional), lifePath, expression }` |
| `chart` | placeholder | `{ sun, moon, asc }`, each `{ sign, deg, house }` |
| `bazi` | auto-computed | optional pre-computed pillars — overrides the built-in BaZi calc |
| `resonanceHouses` | 5 default houses | which Western houses appear on the right column of the resonance map |
| `resonanceLinks` | element-affinity | optional `[[pillarIdx, houseIdx, 'g'|'r'], …]` to override the auto-drawn links |
| `sections` | `[]` | per-section overrides — see below |
| `today` | `new Date()` | override for testing Personal Day calc |

### Per-section overrides

Each entry of `sections` is `{ hermetic?, light?, shadow?, working?, chips? }`.
Any field omitted falls back to the default scaffold, so a partial array still
works — the engine can fill in sections progressively.

```js
sections: [
  {
    hermetic: { glyph:'☾︎', name:'Polarity' },   // optional badge override
    light:    'string (HTML allowed)',           // Light — the gift
    shadow:   'string (HTML allowed)',           // Shadow — the trap
    working:  { text:'string', glyphs:'☾︎ ✶ 🕯︎' },
    chips:    [ { glyph:'XVIII', name:'The Moon', k:'Pisces sign' }, … ]
  },
  // …
]
```

## API

| Call | Returns | Effect |
|------|---------|--------|
| `NumenEnhancements.init(cfg)` | `{ sectionsEnhanced, personalDay }` | Inject everything. Idempotent — safe to call again. |
| `NumenEnhancements.destroy(cfg)` | — | Cleanly removes every node the module injected. Original page returns to its pre-init state. Useful for re-init after data changes. |
| `NumenEnhancements.util.reduce(n)` | int | Pythagorean reduction with master-number preservation (11, 22) and karmic-debt preservation (13, 14, 16, 19). |
| `NumenEnhancements.util.personalDay(dob, today)` | int | Personal-Day calc (Personal Year + month + day, reduced). |
| `NumenEnhancements.util.bazi(dob, hour?)` | object | Real BaZi (Four Pillars) calculation. Returns `{ year, month, day, hour }`, each `{ stem, branch, element, animal, label }`. Hour is `null` if no birth hour passed. Year/month/day verified against reference dates (e.g. 2024-01-01 → 癸丑). |
| `NumenEnhancements.util.julianDay(y, m, d)` | int | Julian Day Number — exposed for any other calendar work the engine needs. |
| `NumenEnhancements.builders.*` | DOM node | Each individual feature exposed for manual injection or A/B testing. |
| `NumenEnhancements.draw.*` | — | Canvas drawers (`constellation`, `wheel`, `resonance`) exposed for re-rendering on resize. |

## What's real vs. what's scaffold — read this before going live

Everything **renders and positions** correctly out of the box. What ships as
real content vs. scaffold:

**Real now** (driven entirely by `user`/`chart` you pass in):
- Personal Day banner (calculation + Tarot correspondence)
- Natal chart wheel — 12 zodiac signs around the rim, 12 houses with angular
  cusps drawn stronger, planets placed at their true ecliptic longitudes,
  Sun-Moon conjunction line when within 8°
- Constellation panel — sign-specific stick figures (Pisces shows the
  two-fish cord, Leo the sickle, Scorpio the J-curve, etc.), Sun and Moon
  placed at their actual degree-within-sign positions
- Hermetic principle badge (default mapping; per-section override available)
- Tarot chips (sign + house Tarot from chart; per-section override available)
- Chaldean numerology chip

**Scaffold until the engine plugs real content** (via the `sections` array):
- Light / Shadow polarity copy — generic placeholder unless `sections[i].light`
  + `.shadow` are provided
- The Working ritual copy — generic placeholder unless `sections[i].working`
  is provided

**Not wired yet**:
- Audio bar renders but isn't bound to a narration source. Hook to a TTS
  stream or pre-rendered audio file when ready.
- Resonance map now uses **real** BaZi pillars computed from `user.dob` (+
  optional `user.birthHour`) via the built-in calculator. Engine can still
  override with `cfg.bazi` if it wants to use its own ephemeris-grade
  pillars. The pillar-to-house links default to an element-affinity
  heuristic; pass `cfg.resonanceLinks` to override.

## The one honest blocker

The live Numen 15-section reading **engine is not in this repository.** This
overlay is framework-agnostic precisely so it can attach to that engine
wherever it lives. The final wire-up — matching `sectionContainer` /
`sectionTitle` to the engine's real markup and feeding the `sections` array
with real per-section light/shadow/working copy — has to happen against that
engine. This module is the part that *can* be built and verified without it.

## Guarantees

- **Additive only.** No existing text, heading, or markup is modified or removed.
- **No collisions.** Every class is `.nx-` prefixed; every CSS var is `--nx-`.
- **Idempotent.** Re-running `init()` won't double-inject — each builder
  checks for its own node first.
- **Reversible.** `destroy()` cleanly undoes everything `init()` did.
- **Offline.** Self-hosts fonts; no external network calls at runtime.
- **Palette-matched.** Colors and fonts mirror the live Numen palette
  (`#06010f` ground, `#d4a857` gold, `#6a3d8e` plum, Cormorant Garamond / Inter).
