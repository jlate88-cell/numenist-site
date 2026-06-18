# Production Integration — Numen Reading Enhancements

Specific deployment instructions for the live Vercel + Next.js + Supabase
stack that serves the Numen astrology reading product (separate from this
landing-page repo).

## What this folder ships

| File | Purpose | Bytes |
|------|---------|-------|
| `numen-enhancements.css` | All `.nx-` styling | ~7 KB |
| `numen-enhancements.js` | Drop-in injection module | ~25 KB |
| `sections-numen.js` | Light/Shadow + Working overlay copy, **keyed by engine section IDs** | ~12 KB |
| `fonts/fonts.css` | Self-hosted font @font-face declarations | ~2 KB |
| `fonts/cormorant-garamond-latin.woff2` | Variable font, latin subset | ~37 KB |
| `fonts/inter-latin.woff2` | Variable font, latin subset | ~48 KB |

Total: ~131 KB (one-time, cached by the browser).

## The engine schema (verified from Supabase)

Each reading lives in `public.astrology_readings_cache.reading_json` and
is an object of shape:

```jsonc
{
  "phase": "...",
  "system": "combined",
  "westernTradition": "integrated",
  "composedBy": "deterministic" | "claude",
  "summary": "...",
  "sections": [
    {
      "id": "overview-combined",
      "heading": "Your Reading at a Glance",
      "paragraphs": ["...", "...", ...],
      "blocks": [{ "type": "paragraph", "text": "..." }, ...]
    },
    // ...15 entries, ids in order:
    //   overview-combined, opening, sect-lights, ascendant-lord,
    //   personal-planets, social-planets, outer-planets, nodes-chiron,
    //   configurations, timing, four-pillars, day-master-ten-gods,
    //   zi-wei-stars, da-yun-timing, east-west-synthesis
  ]
}
```

## What the integration needs in the Next.js reading page

In the React component that renders one section, give each rendered
section a `data-section-id` attribute matching the engine's `section.id`:

```tsx
{reading.sections.map((s) => (
  <section
    key={s.id}
    data-section-id={s.id}
    className="reading-section"
  >
    <h2>{s.heading}</h2>
    {s.paragraphs.map((p, i) => <p key={i}>{p}</p>)}
  </section>
))}
```

`data-section-id` is the seam the overlay reads to match per-section
copy by id.

## Adding the overlay to the Next.js page

```tsx
// app/reading/[id]/page.tsx (or wherever the reading renders)

// 1. Copy the six files in this folder to /public/numen-enhancements/
//    so they're served at /numen-enhancements/* by Next.js.

// 2. In the page component:

export default function ReadingPage({ params }) {
  // ... fetch reading from Supabase ...

  return (
    <>
      <link rel="stylesheet" href="/numen-enhancements/fonts/fonts.css" />
      <link rel="stylesheet" href="/numen-enhancements/numen-enhancements.css" />

      <div className="reading-page">
        <header className="reading-masthead">
          {/* ...existing masthead... */}
        </header>

        {reading.sections.map((s) => (
          <section
            key={s.id}
            data-section-id={s.id}
            className="reading-section"
          >
            <h2>{s.heading}</h2>
            {s.paragraphs.map((p, i) => <p key={i}>{p}</p>)}
          </section>
        ))}
      </div>

      <Script src="/numen-enhancements/numen-enhancements.js" strategy="afterInteractive" />
      <Script src="/numen-enhancements/sections-numen.js" strategy="afterInteractive" />
      <Script id="numen-init" strategy="afterInteractive">{`
        NumenEnhancements.init({
          sectionContainer: '[data-section-id]',
          sectionTitle:     'h2',
          pageContainer:    '.reading-page',
          mountTopAfter:    '.reading-masthead',
          user: {
            name:       ${JSON.stringify(chart.seekerName)},
            dob:        ${JSON.stringify(chart.dobIso)},     // 'YYYY-MM-DD'
            birthHour:  ${chart.birthHour ?? 'null'},
            lifePath:   ${chart.lifePath},
            expression: ${chart.expression}
          },
          chart: {
            sun:  { sign: ${JSON.stringify(chart.sun.sign)}, deg: ${chart.sun.deg}, house: ${chart.sun.house} },
            moon: { sign: ${JSON.stringify(chart.moon.sign)}, deg: ${chart.moon.deg}, house: ${chart.moon.house} },
            asc:  { sign: ${JSON.stringify(chart.asc.sign)}, deg: ${chart.asc.deg} }
          },
          sections: window.NUMEN_SECTIONS
        });
      `}</Script>
    </>
  );
}
```

## What the overlay adds, per the engine sections

| Engine section id | Overlay additions |
|-------------------|-------------------|
| `overview-combined` | Hermetic badge, Tarot chips, Light/Shadow, The Working |
| `opening` | …same shape… |
| `sect-lights` | …same shape, copy is diurnal/Pisces-7th aware… |
| `ascendant-lord` | …Virgo-rising/Mercury-chart-ruler aware… |
| `personal-planets` | … |
| `social-planets` | …Jupiter Leo 12th Rx, Saturn 6th aware… |
| `outer-planets` | … |
| `nodes-chiron` | …NN Capricorn 5th aware… |
| `configurations` | …Water 36 / Air 14 aware… |
| `timing` | …12th house profection / Sun Lord of Year aware… |
| `four-pillars` | …Jiǎ Wood Day Master / 甲申 day aware… |
| `day-master-ten-gods` | … |
| `zi-wei-stars` | … |
| `da-yun-timing` | … |
| `east-west-synthesis` | …closing through-line working… |

Per-page additions (independent of section): Personal Day banner (top),
audio bar (top, no source bound yet), constellation panel (top), natal
chart wheel (top), resonance map at the foot with real BaZi pillars
computed from the engine's `chart.bazi` if passed, or computed locally
from `user.dob` + `user.birthHour`.

## Verification before shipping

1. Deploy to a preview Vercel URL (not production).
2. Open one reading. Confirm:
   - Existing prose is byte-identical to before integration.
   - The `.nx-` enhancements appear around it.
   - Personal Day at the top matches today's date for the operator's DOB.
   - The natal wheel shows Sun & Moon in the correct house (Pisces 7th
     for Jordan's chart).
   - The four pillars at the foot read **辛未 · 辛卯 · 甲申 · 癸酉** for
     Jordan's chart, with Day Master 甲 highlighted.
3. Open the same page on mobile. The `nx-duo` grid collapses to a single
   column under 760px.
4. If anything looks wrong, call `NumenEnhancements.destroy({pageContainer:'.reading-page'})`
   in the console to revert cleanly.

## Source of truth for the per-section overlay copy

The `sections-numen.js` file is hand-written, lineage-aligned overlay
copy. It does NOT replace the engine's reading. It adds Light/Shadow
+ Working ABOVE the engine's existing per-section prose, so each section
gains an editorial frame without losing any of the deterministic /
Claude-composed content.

If the engine's section ids change (additions, removals, renames), the
overlay falls back to defaults for any unknown id — no crash, no missing
visual element, just generic scaffolding until the new id gets a real
entry added.
