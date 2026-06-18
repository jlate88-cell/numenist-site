# Numen Reading Enhancements — drop-in overlay

An **additive-only** layer that adds ten features to an existing Numen astrology
reading page **without removing, rewriting, or restyling a single line of the
reading that's already there.** Every selector is prefixed `.nx-` so it cannot
collide with the live page's CSS. No existing DOM node is deleted; the script
only *inserts* alongside what already renders.

## Drop it in (two lines + one call)

```html
<link rel="stylesheet" href="numen-enhancements.css">
<script src="numen-enhancements.js"></script>
<script>
  NumenEnhancements.init({
    sectionContainer: '.reading-section',   // wraps one section on your real page
    sectionTitle:     'h2',                 // the heading inside it
    pageContainer:    '.reading-page',      // outer wrap of the reading
    pageNumber:       2,
    user:  { name:'Maverick', dob:'1990-03-12', lifePath:11, expression:9 },
    chart: {
      sun:  { sign:'Pisces', deg:24.87, house:7 },
      moon: { sign:'Pisces', deg:20.12, house:7 },
      asc:  { sign:'Virgo',  deg:18.45 }
    }
  });
</script>
```

Open `demo.html` in a browser to see the whole thing rendered against a faithful
replica of a reading page. That file is the preview — it is **not** the product;
it exists so the overlay can be tested before it touches the live engine.

## The ten features

| # | Feature | Where it lands | Data it needs |
|---|---------|----------------|----------------|
| 1 | Light / Shadow polarity panel | end of each section | per-section copy (see below) |
| 2 | Hermetic principle badge | beside each section title | section→principle map (built in, tunable) |
| 3 | Tarot correspondence chips | under each section title | `chart` (sign + house) |
| 4 | Constellation panel ("your sky at first breath") | top of page | `chart` (sun/moon/asc) |
| 5 | The Working — boots on the ground | end of each section | per-section ritual copy |
| 6 | Personal Day banner (live, with Tarot) | top of page | `user.dob` + today |
| 7 | Natal chart wheel | top of page | `chart` |
| 8 | Audio "listen" bar | top of page | an audio source (see below) |
| 9 | Chaldean numerology chip | under each section title | `user.expression` |
| 10 | Resonance map (BaZi pillars ⟷ Western houses) | end of page | BaZi data (placeholder wired) |

## Config

| Key | Default | Meaning |
|-----|---------|---------|
| `sectionContainer` | `.reading-section, [data-section], section.reading` | CSS selector matching one section block |
| `sectionTitle` | `h2` | the heading element inside a section |
| `sectionBody` | `p` | the prose inside a section |
| `pageContainer` | `.reading-page, .page-content, main` | the outer wrap |
| `pageNumber` | `2` | which page (1–15) is current |
| `user` | placeholder | `{ name, dob:'YYYY-MM-DD', lifePath, expression }` |
| `chart` | placeholder | `{ sun, moon, asc }`, each `{ sign, deg, house }` |
| `today` | `new Date()` | override for testing Personal Day |

## What's real vs. what's scaffold — read this before going live

The overlay **renders and positions** all ten features correctly right now. What
it does **not** yet carry is the real *content* for three of them — these ship as
placeholders on purpose, so the engine (or you) drops in the true copy:

- **#1 Light / Shadow** — currently generic placeholder text. Production needs
  the real light-gift / shadow-trap copy *per section*. Pass it in or replace
  `POLARITY_DEFAULT` / wire a `polarity` array.
- **#5 The Working** — currently a generic candle scaffold. Production needs the
  real per-section ritual (color, verse, gesture) from the lineage.
- **#8 Audio** — the bar renders but has no audio source bound. Hook it to a real
  narration file or TTS stream.
- **#10 Resonance map** — the BaZi pillars and house links are illustrative
  placeholders until real BaZi pillars are computed for the native.

Everything else (#2, #3, #4, #6, #7, #9) is driven entirely by the `user` and
`chart` you pass in and is production-ready as soon as those carry real values.

## The one honest blocker

The live Numen 15-section reading **engine is not in this repository.** This
overlay is framework-agnostic precisely so it can attach to that engine wherever
it lives — but the final wire-up (matching `sectionContainer`/`sectionTitle` to
the engine's real markup, and feeding real per-section polarity + working copy)
has to happen against that engine. This module is the part that *can* be built
and verified without it. The rest waits on access to the engine or the copy.

## Guarantees

- **Additive only.** No existing text, heading, or markup is modified or removed.
- **No collisions.** Every class is `.nx-`-prefixed; every CSS var is `--nx-`.
- **Idempotent.** Re-running `init()` won't double-inject — each builder checks
  for its own node first.
- **Palette-matched.** Colors and fonts mirror the live Numen palette
  (`#06010f` ground, `#d4a857` gold, `#6a3d8e` plum, Cormorant Garamond / Inter).
