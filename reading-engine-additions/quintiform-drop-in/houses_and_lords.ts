/**
 * houses_and_lords.ts — deterministic composer for the new section
 *
 * TypeScript port of houses_and_lords.py for direct drop-in to the
 * Numen reading engine (Next.js, deployed via Vercel from
 * jlate88-cell/quintiform → numenist.com).
 *
 * Plug into the existing composer pipeline at the same point any other
 * section is composed. Returns ONE section object matching the engine
 * schema observed in public.astrology_readings_cache:
 *
 *   { id: string, heading: string, paragraphs: string[], blocks: Block[] }
 *
 * Where Block matches the engine's block shape:
 *   { type: 'paragraph', text: string }
 *
 * Insertion point in the section sequence:
 *   - 15-section combined-astrology product: insert after 'configurations',
 *     before 'timing'.
 *   - 17-section flagship Reading: insert after 'astrology', before
 *     'master-count'.
 */

// ---- Types matching the engine's existing schema ------------------------

export type Sign =
  | 'Aries' | 'Taurus' | 'Gemini' | 'Cancer' | 'Leo' | 'Virgo'
  | 'Libra' | 'Scorpio' | 'Sagittarius' | 'Capricorn' | 'Aquarius' | 'Pisces';

export type PlanetKey =
  | 'sun' | 'moon' | 'mercury' | 'venus' | 'mars'
  | 'jupiter' | 'saturn' | 'uranus' | 'neptune' | 'pluto';

export type ClassicalPlanetKey =
  | 'sun' | 'moon' | 'mercury' | 'venus' | 'mars' | 'jupiter' | 'saturn';

export interface Position {
  sign: Sign;
  deg: number;
  house?: number;
  retrograde?: boolean;
}

export interface Chart {
  asc: { sign: Sign; deg: number };
  sun?: Position;
  moon?: Position;
  mercury?: Position;
  venus?: Position;
  mars?: Position;
  jupiter?: Position;
  saturn?: Position;
  uranus?: Position;
  neptune?: Position;
  pluto?: Position;
}

export interface Block {
  type: 'paragraph';
  text: string;
}

export interface ReadingSection {
  id: string;
  heading: string;
  paragraphs: string[];
  blocks: Block[];
}

// ---- Hellenistic rulerships (no modern outers as house rulers) ----------
// Documented in Lilly, Christian Astrology (1647), and Hellenistic
// sources (Valens, Firmicus Maternus). Modern outer planets (Uranus,
// Neptune, Pluto) are NOT used as house rulers in this technique.

const SIGN_RULER: Record<Sign, ClassicalPlanetKey> = {
  Aries: 'mars',
  Taurus: 'venus',
  Gemini: 'mercury',
  Cancer: 'moon',
  Leo: 'sun',
  Virgo: 'mercury',
  Libra: 'venus',
  Scorpio: 'mars',
  Sagittarius: 'jupiter',
  Capricorn: 'saturn',
  Aquarius: 'saturn',
  Pisces: 'jupiter',
};

const SIGN_ORDER: Sign[] = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces',
];

// Essential dignity: sign → planet → label
const DIGNITY: Partial<Record<Sign, Partial<Record<ClassicalPlanetKey, string>>>> = {
  Aries:       { mars: 'domicile',           venus: 'detriment', sun: 'exaltation', saturn: 'fall' },
  Taurus:      { venus: 'domicile',          mars: 'detriment',  moon: 'exaltation' },
  Gemini:      { mercury: 'domicile',        jupiter: 'detriment' },
  Cancer:      { moon: 'domicile',           saturn: 'detriment', jupiter: 'exaltation', mars: 'fall' },
  Leo:         { sun: 'domicile',            saturn: 'detriment' },
  Virgo:       { mercury: 'domicile, exaltation', jupiter: 'detriment', venus: 'fall' },
  Libra:       { venus: 'domicile',          mars: 'detriment',  saturn: 'exaltation', sun: 'fall' },
  Scorpio:     { mars: 'domicile',           venus: 'detriment', moon: 'fall' },
  Sagittarius: { jupiter: 'domicile',        mercury: 'detriment' },
  Capricorn:   { saturn: 'domicile',         moon: 'detriment',  mars: 'exaltation',   jupiter: 'fall' },
  Aquarius:    { saturn: 'domicile',         sun: 'detriment' },
  Pisces:      { jupiter: 'domicile',        mercury: 'detriment, fall', venus: 'exaltation' },
};

const PLANET_GLYPH: Record<ClassicalPlanetKey, string> = {
  sun: '☉', moon: '☾', mercury: '☿', venus: '♀', mars: '♂',
  jupiter: '♃', saturn: '♄',
};

const PLANET_NAME: Record<ClassicalPlanetKey, string> = {
  sun: 'Sun', moon: 'Moon', mercury: 'Mercury', venus: 'Venus', mars: 'Mars',
  jupiter: 'Jupiter', saturn: 'Saturn',
};

const HOUSE_TOPIC: Record<number, string> = {
  1:  'self, body, and the way you meet the world',
  2:  'money, resources, and what you call valuable',
  3:  'daily mind, voice, siblings, and near travel',
  4:  'home, roots, ancestry, and the inner foundation',
  5:  'creative play, romance, children, and what you make',
  6:  'daily work, health, service, and the trained discipline',
  7:  'partnership, marriage, and the committed other',
  8:  'joint resources, intimacy, transformation, the hidden depths',
  9:  'higher mind, foreign ground, philosophy, the long journey',
  10: 'vocation, public reputation, the visible work in the world',
  11: 'friends, networks, hopes, the larger belonging',
  12: 'solitude, the unseen, what dissolves the self, surrender',
};

const HOUSE_AT: Record<number, string> = {
  1:  '1st house of self',
  2:  '2nd house of resources',
  3:  '3rd house of mind',
  4:  '4th house of root',
  5:  '5th house of creation',
  6:  '6th house of work and health',
  7:  '7th house of partnership',
  8:  '8th house of depth and shared resource',
  9:  '9th house of higher mind',
  10: '10th house of vocation',
  11: '11th house of network',
  12: '12th house of the unseen',
};

// ---- Helpers ---------------------------------------------------------------

function wholeSignHouses(ascSign: Sign): Record<number, Sign> {
  const start = SIGN_ORDER.indexOf(ascSign);
  const out: Record<number, Sign> = {};
  for (let h = 1; h <= 12; h++) {
    out[h] = SIGN_ORDER[(start + h - 1) % 12];
  }
  return out;
}

function dignityFor(planet: ClassicalPlanetKey, sign: Sign): string {
  return DIGNITY[sign]?.[planet] ?? 'peregrine';
}

function isAngular(h: number): boolean {
  return h === 1 || h === 4 || h === 7 || h === 10;
}
function isSuccedent(h: number): boolean {
  return h === 2 || h === 5 || h === 8 || h === 11;
}
function positionQuality(h: number): string {
  if (isAngular(h))   return "placed on the chart's load-bearing wall, loud and early";
  if (isSuccedent(h)) return 'placed in the middle distance, building and sustaining';
  return 'placed behind the scenes, working through learning and adjustment';
}

function qualityFor(dignity: string, retrograde: boolean): string {
  const bits: string[] = [];
  if (dignity.includes('domicile')) {
    bits.push("at home, working on its own terms, with full access to its tools");
  } else if (dignity.includes('exaltation')) {
    bits.push('exalted, lifted, working at its higher register');
  } else if (dignity.includes('detriment')) {
    bits.push(
      "in detriment, improvising tools that don't come standard, building hard-won competence"
    );
  } else if (dignity.includes('fall')) {
    bits.push(
      "in fall, running uphill against the sign's grain, the gift earned through the difficulty"
    );
  } else {
    bits.push(
      'peregrine, without strong essential dignity, shaped most by house and aspect rather than by the sign'
    );
  }
  if (retrograde) {
    bits.push(
      'retrograde, turned inward, asking to be integrated before it can be expressed outward'
    );
  }
  return bits.join('; ');
}

function ordSuffix(n: number): string {
  if (n >= 10 && n <= 20) return 'th';
  const r = n % 10;
  if (r === 1) return 'st';
  if (r === 2) return 'nd';
  if (r === 3) return 'rd';
  return 'th';
}

function formatPosition(pos: Position): string {
  const parts = [`${pos.sign} ${pos.deg.toFixed(2)}°`];
  if (pos.house !== undefined) {
    parts.push(`${pos.house}${ordSuffix(pos.house)} house`);
  }
  if (pos.retrograde) parts.push('retrograde');
  return parts.join(' · ');
}

function composeHouseParagraph(houseNum: number, chart: Chart): string {
  const cusps = wholeSignHouses(chart.asc.sign);
  const cuspSign = cusps[houseNum];
  const lord = SIGN_RULER[cuspSign];
  const pos = chart[lord];

  const topic = HOUSE_TOPIC[houseNum];
  const topicShort = topic.split(',')[0].trim();
  const lordGlyph = PLANET_GLYPH[lord];
  const lordName  = PLANET_NAME[lord];

  if (!pos) {
    return (
      `${houseNum}${ordSuffix(houseNum)} house — ${topic}. ` +
      `The sign on the cusp is ${cuspSign}; its lord is ${lordName} ${lordGlyph}. ` +
      `Position not provided for this lord; the dispositor read cannot be completed.`
    );
  }

  const lordHouse = pos.house;
  const dignity  = dignityFor(lord, pos.sign);
  const qual     = qualityFor(dignity, !!pos.retrograde);
  const angNote  = lordHouse !== undefined ? ` It is ${positionQuality(lordHouse)}.` : '';
  const whereTopic = lordHouse !== undefined ? (HOUSE_AT[lordHouse] ?? `${lordHouse}${ordSuffix(lordHouse)} house`) : '—';
  const whereShort = whereTopic.includes(' of ') ? whereTopic.split(' of ').slice(-1)[0] : whereTopic;

  return (
    `${houseNum}${ordSuffix(houseNum)} house — ${topic}. ` +
    `The sign on the cusp is ${cuspSign}; its lord is ${lordName} ${lordGlyph}, ` +
    `and it sits in your chart at ${formatPosition(pos)}. ` +
    `${lordName} is ${qual}.${angNote} ` +
    `Therefore the affairs of your ${houseNum}${ordSuffix(houseNum)} house ` +
    `are run through your ${whereTopic} — what feels like your ${topicShort} ` +
    `actually plays out wherever ${lordName} lives, not where the empty cusp sits. ` +
    `Watch ${whereShort} to see this house move.`
  );
}

// ---- Public API -----------------------------------------------------------

/**
 * Build the Twelve Doors section from a chart.
 * Insert into the engine's section sequence at the documented point.
 */
export function composeHousesAndLords(chart: Chart): ReadingSection {
  const intro =
    'Every house in the chart is run by the planet that rules the sign on its cusp. ' +
    'When a house is empty of planets, that does NOT mean it has no story; it means the ' +
    'story is happening wherever the cusp-lord lives. This section walks all twelve houses ' +
    'in turn, naming each cusp-lord and where it actually sits — so the affairs of every ' +
    'house become readable, not just the ones with bodies parked in them.';

  const paragraphs: string[] = [intro];
  for (let h = 1; h <= 12; h++) {
    paragraphs.push(composeHouseParagraph(h, chart));
  }

  const closing =
    'Held together, the twelve doors tell you which areas of your life move through which ' +
    'engines. Where a lord is angular and dignified, that house flows; where it is in ' +
    'detriment, retrograde, or cadent, the house asks for conscious work to come alive. ' +
    "When in doubt about an area of life, find its lord, see where it lives, and read the " +
    "affairs of the house through the affairs of the lord's house.";

  paragraphs.push(closing);

  const blocks: Block[] = paragraphs.map((text) => ({ type: 'paragraph', text }));

  return {
    id: 'houses-and-lords',
    heading: 'The Twelve Doors — Houses & Their Lords',
    paragraphs,
    blocks,
  };
}
