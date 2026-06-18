/* ============================================================
   NUMEN READING ENHANCEMENTS — additive-only injection
   v0.2 · drop-in script
   Adds 10 features to an existing astrology reading page
   WITHOUT modifying any existing text, headings, or markup.

   Quick start (see README.md for full reference):

     <link rel="stylesheet" href="fonts/fonts.css">
     <link rel="stylesheet" href="numen-enhancements.css">
     <script src="numen-enhancements.js"></script>
     <script>
       NumenEnhancements.init({
         sectionContainer: '.reading-section',
         sectionTitle:     'h2',
         pageContainer:    '.reading-page',
         mountTopAfter:    '.reading-masthead',  // chrome lands AFTER masthead
         pageNumber:       2,
         user:  { name:'Maverick', dob:'1990-03-12', lifePath:11, expression:9 },
         chart: {
           sun:  { sign:'Pisces', deg:24.87, house:7 },
           moon: { sign:'Pisces', deg:20.12, house:7 },
           asc:  { sign:'Virgo',  deg:18.45 }
         },
         sections: [
           { hermetic:{glyph:'☾︎',name:'Polarity'},
             light:'…', shadow:'…',
             working:{text:'…', glyphs:'☾︎ ✶ 🕯︎'} },
           // …one entry per reading section
         ]
       });
     </script>

   API surface:
     init(cfg)      → inject; idempotent
     destroy(cfg)   → cleanly removes every node init() injected
     util.reduce(n) → Pythagorean reduction (preserves 11/22/13/14/16/19)
     util.personalDay(dob, today) → Personal-Day calculation
     builders.*     → expose each feature builder for manual injection
     draw.*         → canvas drawers (constellation, wheel, resonance)

   No DOM is modified until init() is called. All inserted elements
   carry the .nx- prefix so they cannot collide with existing CSS.
   ============================================================ */

(function (global) {
  'use strict';

  // ------- defaults & data tables -------
  const TAROT = {
    Aries:'IV · The Emperor', Taurus:'V · The Hierophant', Gemini:'VI · The Lovers',
    Cancer:'VII · The Chariot', Leo:'VIII · Strength', Virgo:'IX · The Hermit',
    Libra:'XI · Justice', Scorpio:'XIII · Death', Sagittarius:'XIV · Temperance',
    Capricorn:'XV · The Devil', Aquarius:'XVII · The Star', Pisces:'XVIII · The Moon'
  };
  const HOUSE_TAROT = {
    1:'I · The Magician', 2:'II · The High Priestess', 3:'III · The Empress',
    4:'IV · The Emperor', 5:'V · The Hierophant', 6:'VI · The Lovers',
    7:'VII · The Chariot', 8:'VIII · Strength', 9:'IX · The Hermit',
    10:'X · Wheel of Fortune', 11:'XI · Justice', 12:'XII · The Hanged Man'
  };
  const COMPOUND_TAROT = {
    10:'Wheel of Fortune', 11:'Justice', 12:'Hanged Man', 13:'Death',
    14:'Temperance', 15:'Devil', 16:'Tower', 17:'Star', 18:'Moon',
    19:'Sun', 20:'Judgement', 21:'World', 22:'Fool/Master'
  };
  // U+FE0E forces monochrome text presentation of symbols that the OS would
  // otherwise render as color emoji (planets, signs, candle, etc.)
  const T = '︎';
  // Hermetic principle per section number (1..15) — operator-tunable mapping
  const HERMETIC_BY_SECTION = {
    1:{glyph:'∞',    name:'Correspondence'},
    2:{glyph:'☉'+T,  name:'Mentalism'},
    3:{glyph:'☾'+T,  name:'Vibration'},
    4:{glyph:'↑',    name:'Rhythm'},
    5:{glyph:'♀'+T,  name:'Gender'},
    6:{glyph:'♃'+T,  name:'Cause & Effect'},
    7:{glyph:'♅'+T,  name:'Polarity'},
    8:{glyph:'☊'+T,  name:'Vibration'},
    9:{glyph:'△',    name:'Correspondence'},
    10:{glyph:'⌛'+T, name:'Rhythm'},
    11:{glyph:'四',  name:'Correspondence'},
    12:{glyph:'日',  name:'Vibration'},
    13:{glyph:'紫',  name:'Mentalism'},
    14:{glyph:'運',  name:'Rhythm'},
    15:{glyph:'⊕',   name:'Polarity'}
  };
  // Default light/shadow placeholders — engine should replace with real per-section copy
  const POLARITY_DEFAULT = {
    light:'Add your light-side copy here — the gift, the trained expression, what this factor offers when integrated.',
    shadow:'Add your shadow-side copy here — the trap, the un-integrated pattern, what to watch for so the gift does not invert.'
  };
  // Working recommendation default scaffold — engine replaces with per-section ritual
  const WORKING_DEFAULT = {
    text:'Light a candle of the corresponding color. Speak the verse or invocation for this factor. Hold the breath for seven beats. The working seals when you snuff, not when you blow.',
    glyphs:'🕯'+T+' ✶ ☾'+T+' ♓'+T
  };

  const DEFAULTS = {
    sectionContainer: '.reading-section, [data-section], section.reading',
    sectionTitle:     'h2',
    sectionBody:      'p',
    pageContainer:    '.reading-page, .page-content, main',
    // CSS selector for the element AFTER which the top chrome (PD banner,
    // audio, constellation+wheel) is mounted. If null, mounts at top of page.
    mountTopAfter:    null,
    pageNumber:       2,
    user: { name:'Operator', dob:'1990-01-01', lifePath:11, expression:9 },
    chart: {
      sun: {sign:'Pisces', deg:24.87, house:7},
      moon:{sign:'Pisces', deg:20.12, house:7},
      asc: {sign:'Virgo',  deg:18.45}
    },
    today: new Date(),
    // Per-section overrides; sections[i] applies to the (i+1)th .reading-section
    // Each entry can carry any subset of: {hermetic, light, shadow, working, chips}
    //   hermetic: { glyph, name }
    //   light:    string (HTML allowed)
    //   shadow:   string (HTML allowed)
    //   working:  { text, glyphs }
    //   chips:    array of { glyph, name, k }   // overrides auto-generated chips
    // When a key is omitted, the default scaffold is used. This way a partial
    // sections array still works — engine can fill them in over time.
    sections: []
  };

  function sectionData(idx, cfg){
    const s = cfg.sections[idx] || {};
    return {
      hermetic: s.hermetic || HERMETIC_BY_SECTION[idx + 1] || {glyph:'✶', name:'Polarity'},
      light:    s.light    || POLARITY_DEFAULT.light,
      shadow:   s.shadow   || POLARITY_DEFAULT.shadow,
      working:  s.working  || WORKING_DEFAULT,
      chips:    s.chips // optional override; undefined means auto-generate
    };
  }

  // ------- helpers -------
  function el(tag, cls, txt){
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt !== undefined) e.textContent = txt;
    return e;
  }
  function html(tag, cls, h){
    const e = el(tag, cls);
    if (h) e.innerHTML = h;
    return e;
  }
  function reduce(n){
    while (n > 22 || (n > 9 && ![11,13,14,16,19,22].includes(n))) {
      n = String(n).split('').reduce((a,b)=>a+(+b),0);
    }
    return n;
  }
  function personalDay(dob, today){
    // PD = PersonalYear + month + day, all reduced
    const [yy,mm,dd] = dob.split('-').map(Number);
    const ty = today.getFullYear(), tm = today.getMonth()+1, td = today.getDate();
    const py = reduce(reduce(mm+dd) + reduce(ty));
    const pm = reduce(py + tm);
    const pd = reduce(pm + td);
    return pd;
  }

  // ------- feature builders -------
  function buildPersonalDayBanner(cfg){
    const pd = personalDay(cfg.user.dob, cfg.today);
    const tarot = COMPOUND_TAROT[pd] || (pd<=9 ? ['','Magician','High Priestess','Empress','Emperor','Hierophant','Lovers','Chariot','Strength','Hermit'][pd] : '');
    const banner = el('div','nx-pd-banner');
    banner.innerHTML = `
      <span class="nx-pd-glyph">☉</span>
      <span class="nx-pd-text">Today is your <b>Personal Day ${pd}${tarot?` / ${tarot}`:''}</b> — read the section whose number matches today\'s PD with extra attention.</span>
      <span class="nx-pd-tag">PD SYNC · live</span>`;
    return banner;
  }

  function buildAudioBar(){
    const a = el('div','nx-audio');
    a.innerHTML = `
      <button class="nx-play" aria-label="Play reading">▶</button>
      <div class="nx-wave">${Array.from({length:18}).map((_,i)=>`<span style="height:${30+Math.abs(Math.sin(i))*65}%"></span>`).join('')}</div>
      <span class="nx-lbl">Listen</span><span class="nx-time">7:42</span>`;
    return a;
  }

  function buildDuo(cfg){
    const duo = el('div','nx-duo');
    duo.innerHTML = `
      <div class="nx-panel"><div class="nx-panel-title">Your sky at first breath</div>
        <canvas class="nx-constellation" width="480" height="280" style="width:100%;height:auto"></canvas></div>
      <div class="nx-panel"><div class="nx-panel-title">Natal chart wheel</div>
        <canvas class="nx-wheel" width="300" height="300" style="width:100%;max-width:300px;height:auto"></canvas></div>`;
    return duo;
  }

  function buildHermBadge(data){
    const b = el('div','nx-herm-badge');
    b.innerHTML = `<div class="nx-herm-ring">${data.hermetic.glyph}</div><div class="nx-herm-lbl">${data.hermetic.name}</div>`;
    return b;
  }

  function buildChips(data, cfg){
    const wrap = el('div','nx-chips');
    let cards = data.chips;
    if (!cards) {
      cards = [];
      const sun = cfg.chart.sun;
      if (TAROT[sun.sign]) cards.push({glyph:TAROT[sun.sign].split(' ')[0], name:TAROT[sun.sign].split(' · ')[1], k:`${sun.sign} sign`});
      if (HOUSE_TAROT[sun.house]) cards.push({glyph:HOUSE_TAROT[sun.house].split(' ')[0], name:HOUSE_TAROT[sun.house].split(' · ')[1], k:`${sun.house}th house`});
    }
    cards.forEach(c=>{
      const chip = el('div','nx-chip');
      chip.innerHTML = `<div class="nx-chip-glyph">${c.glyph}</div><div class="nx-chip-meta"><div class="nx-chip-v">${c.name}</div><div class="nx-chip-k">${c.k}</div></div>`;
      wrap.appendChild(chip);
    });
    // Chaldean numerology chip — always appended for the operator
    const num = el('div','nx-chip nx-chip-num');
    num.innerHTML = `<div class="nx-chip-glyph">${cfg.user.expression}</div><div class="nx-chip-meta"><div class="nx-chip-v">Expression ${cfg.user.expression}</div><div class="nx-chip-k">Chaldean name</div></div>`;
    wrap.appendChild(num);
    return wrap;
  }

  function buildPolarity(data){
    const p = el('div','nx-polarity');
    p.innerHTML = `
      <div class="nx-pol nx-pol-light">
        <div class="nx-pol-h"><span class="nx-dot"></span>Light — the gift</div>
        <p>${data.light}</p>
      </div>
      <div class="nx-pol nx-pol-shadow">
        <div class="nx-pol-h"><span class="nx-dot"></span>Shadow — the trap</div>
        <p>${data.shadow}</p>
      </div>`;
    return p;
  }

  function buildWorking(data){
    const w = el('div','nx-working');
    w.innerHTML = `
      <div class="nx-working-h">The Working — boots on the ground</div>
      <p>${data.working.text}</p>
      <div class="nx-glyphs">${data.working.glyphs}</div>`;
    return w;
  }

  function buildResonance(){
    const r = el('div','nx-resonance');
    r.innerHTML = `
      <div class="nx-reso-title">Where East and West Meet</div>
      <div class="nx-reso-sub">BaZi pillars ⟷ Western houses · gold reinforces · rose crosses</div>
      <canvas class="nx-reso-canvas" width="1000" height="240" style="width:100%;height:auto"></canvas>`;
    return r;
  }

  // ------- canvas drawers -------
  // Approximate constellation stick-figures per zodiac sign.
  // Coordinates are normalized 0..1 across the panel.
  // Each point is [x, y, magnitude] where magnitude 1=brightest.
  // `lines` is a list of point-index pairs to connect.
  const CONSTELLATION = {
    Aries:      { stars:[[.30,.50,1],[.45,.45,1],[.60,.42,2],[.72,.55,2]],            lines:[[0,1],[1,2],[2,3]] },
    Taurus:     { stars:[[.20,.55,2],[.35,.45,1],[.50,.55,1],[.65,.65,2],[.65,.40,2],[.80,.30,2]], lines:[[1,0],[1,2],[2,3],[2,4],[4,5]] },
    Gemini:     { stars:[[.25,.30,1],[.35,.45,2],[.50,.60,2],[.60,.70,2],[.30,.30,1],[.45,.45,2],[.60,.60,2],[.70,.72,2]], lines:[[0,1],[1,2],[2,3],[4,5],[5,6],[6,7],[0,4]] },
    Cancer:     { stars:[[.40,.40,2],[.55,.50,2],[.50,.65,2],[.65,.55,2]],            lines:[[0,1],[1,2],[1,3]] },
    Leo:        { stars:[[.20,.55,2],[.30,.45,2],[.40,.40,1],[.50,.45,2],[.62,.55,1],[.72,.68,2],[.78,.60,2]],  lines:[[0,1],[1,2],[2,3],[3,4],[4,5],[4,6]] },
    Virgo:      { stars:[[.20,.45,2],[.35,.40,2],[.50,.45,1],[.60,.55,2],[.70,.65,1],[.55,.65,2]],  lines:[[0,1],[1,2],[2,3],[3,4],[3,5]] },
    Libra:      { stars:[[.30,.55,2],[.50,.40,1],[.70,.55,1],[.50,.70,2]],            lines:[[0,1],[1,2],[0,3],[2,3]] },
    Scorpio:    { stars:[[.20,.35,2],[.30,.40,1],[.40,.45,2],[.50,.55,1],[.60,.65,2],[.72,.70,2],[.78,.55,2]],  lines:[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]] },
    Sagittarius:{ stars:[[.20,.45,2],[.35,.40,1],[.50,.50,1],[.60,.45,2],[.50,.65,2],[.35,.60,2]],  lines:[[0,1],[1,2],[2,3],[2,4],[4,5],[5,0]] },
    Capricorn:  { stars:[[.20,.45,2],[.40,.40,1],[.60,.50,1],[.75,.60,2],[.55,.70,2]],  lines:[[0,1],[1,2],[2,3],[3,4],[4,0]] },
    Aquarius:   { stars:[[.20,.45,2],[.32,.55,2],[.45,.45,2],[.58,.55,1],[.70,.50,2],[.75,.65,2]], lines:[[0,1],[1,2],[2,3],[3,4],[4,5]] },
    // Pisces: the classical two-fish-tied-at-the-cord pattern.
    // Western fish (low/left), cord ascends across, eastern fish circles top/right.
    Pisces:     {
      stars:[
        [.12,.70,2],[.18,.62,2],[.24,.70,2],[.30,.62,2],[.24,.55,1],  // western fish + α-Psc area
        [.34,.50,2],[.42,.45,2],[.50,.42,2],[.58,.38,2],[.66,.34,2],  // cord
        [.72,.25,1],[.80,.18,2],[.86,.28,2],[.78,.32,2],[.78,.18,2]    // eastern fish circlet
      ],
      lines:[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12],[12,13],[13,10],[13,14]]
    }
  };

  function drawConstellation(canvas, cfg){
    const x = canvas.getContext('2d'); const W=canvas.width, H=canvas.height;
    x.clearRect(0,0,W,H);

    // Backdrop field — deterministic from sign so it's the same every render
    const sign = cfg.chart.sun.sign;
    let seed = sign.length * 7;
    const rnd = () => { seed = (seed * 9301 + 49297) % 233280; return seed/233280; };
    x.fillStyle = '#fff';
    for (let i=0;i<55;i++){
      const px=rnd()*W, py=rnd()*H, r=rnd()*1.0;
      x.globalAlpha=rnd()*.35+.10;
      x.beginPath(); x.arc(px,py,r,0,Math.PI*2); x.fill();
    }
    x.globalAlpha=1;

    // Constellation stick-figure for the sun-sign
    const con = CONSTELLATION[sign] || CONSTELLATION.Pisces;
    const px = i => con.stars[i][0]*W;
    const py = i => con.stars[i][1]*H;

    // connect lines first so stars sit on top
    x.strokeStyle='rgba(212,168,87,.45)'; x.lineWidth=1;
    con.lines.forEach(([a,b])=>{
      x.beginPath(); x.moveTo(px(a),py(a)); x.lineTo(px(b),py(b)); x.stroke();
    });

    // draw stars; magnitude→size mapping (1 brightest = 4.5, 2 = 3, 3+ = 2)
    con.stars.forEach((s,i)=>{
      const r = s[2] === 1 ? 4.2 : (s[2] === 2 ? 2.8 : 2);
      const cx = px(i), cy = py(i);
      const g = x.createRadialGradient(cx,cy,0,cx,cy,r*3.5);
      g.addColorStop(0,'#fff'); g.addColorStop(.35,'rgba(244,236,216,.6)'); g.addColorStop(1,'rgba(212,168,87,0)');
      x.fillStyle=g; x.beginPath(); x.arc(cx,cy,r*3.5,0,Math.PI*2); x.fill();
      x.fillStyle='#fff'; x.beginPath(); x.arc(cx,cy,r*.6,0,Math.PI*2); x.fill();
    });

    // Place Sun and Moon at their actual degree-within-sign positions.
    // Within this panel, treat the sign as spanning 30° from x=.15 to x=.85.
    const xForDeg = d => W * (0.15 + (Math.max(0, Math.min(30, d)) / 30) * 0.70);
    const sun = cfg.chart.sun, moon = cfg.chart.moon;

    const placeBody = (body, glyph, color, yFrac) => {
      const cx = xForDeg(body.deg || 0);
      const cy = H * yFrac;
      // big radial glow
      const g = x.createRadialGradient(cx,cy,0,cx,cy,22);
      g.addColorStop(0, color);
      g.addColorStop(.5,'rgba(212,168,87,.35)');
      g.addColorStop(1,'rgba(212,168,87,0)');
      x.fillStyle=g; x.beginPath(); x.arc(cx,cy,22,0,Math.PI*2); x.fill();
      // core
      x.fillStyle='#fff'; x.beginPath(); x.arc(cx,cy,3,0,Math.PI*2); x.fill();
      // label
      x.fillStyle='rgba(212,168,87,1)'; x.font='13px serif'; x.textAlign='left'; x.textBaseline='middle';
      x.fillText(glyph, cx+14, cy-8);
      x.fillStyle='rgba(201,191,168,.85)'; x.font='10px Inter, sans-serif';
      x.fillText(`${body.sign} ${body.deg.toFixed(1)}°`, cx+14, cy+6);
    };
    placeBody(sun,  '☉'+T, 'rgba(255,235,180,.85)', 0.28);
    placeBody(moon, '☾'+T, 'rgba(220,210,240,.85)', 0.70);

    // caption
    x.fillStyle='rgba(107,100,128,1)'; x.font='10px Inter, sans-serif'; x.textAlign='left';
    x.fillText(`Constellation: ${sign}`, 14, H - 12);
  }

  function drawWheel(canvas, cfg){
    const x = canvas.getContext('2d'); const W=canvas.width, H=canvas.height;
    const cx=W/2, cy=H/2;
    x.clearRect(0,0,W,H);

    // Real astrological wheel.
    //   Ascendant anchors at canvas LEFT (9 o'clock).
    //   Ecliptic longitude increases COUNTERCLOCKWISE in the wheel,
    //   which is DECREASING canvas angle (since y is down).
    //   canvas_angle(L) = π − (L − L_asc) · π/180
    const SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
                   'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
    // Append U+FE0E (text variation selector) so symbol fonts render the
    // monochrome glyph instead of the OS color-emoji presentation.
    const TX = '︎';
    const GLYPHS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'].map(g => g + TX);
    const PLANET_GLYPH = {
      sun:'☉'+TX, moon:'☾'+TX, mercury:'☿'+TX, venus:'♀'+TX, mars:'♂'+TX,
      jupiter:'♃'+TX, saturn:'♄'+TX, uranus:'♅'+TX, neptune:'♆'+TX, pluto:'♇'+TX
    };
    const signIdx = s => Math.max(0, SIGNS.indexOf(s));
    const lon     = body => signIdx(body.sign) * 30 + (body.deg || 0);
    const L_asc   = lon(cfg.chart.asc);
    const ang     = L => Math.PI - (L - L_asc) * Math.PI / 180;

    const rOuter = Math.min(cx,cy) - 8;
    const rSign  = rOuter - 20;     // inner edge of sign band
    const rHouse = rSign  - 18;     // outer edge of house band
    const rInner = rHouse - 60;     // inner ring (where planets sit)

    // outer ring
    x.strokeStyle='rgba(212,168,87,.55)'; x.lineWidth=1.2;
    [rOuter, rSign, rHouse, rInner].forEach(r=>{
      x.beginPath(); x.arc(cx,cy,r,0,Math.PI*2); x.stroke();
    });

    // 12 sign wedge dividers + glyphs at wedge midpoint
    x.fillStyle='#d4a857'; x.font='13px serif'; x.textAlign='center'; x.textBaseline='middle';
    for (let s=0; s<12; s++){
      const aStart = ang(s*30);
      // divider line from rSign to rOuter
      x.beginPath();
      x.moveTo(cx+Math.cos(aStart)*rSign, cy+Math.sin(aStart)*rSign);
      x.lineTo(cx+Math.cos(aStart)*rOuter, cy+Math.sin(aStart)*rOuter);
      x.stroke();
      // glyph at midpoint of wedge (15° into the sign)
      const aMid = ang(s*30 + 15);
      const rGlyph = (rSign + rOuter) / 2;
      x.fillText(GLYPHS[s], cx+Math.cos(aMid)*rGlyph, cy+Math.sin(aMid)*rGlyph);
    }

    // 12 house cusps (equal house from Ascendant)
    x.strokeStyle='rgba(212,168,87,.30)'; x.lineWidth=1;
    x.fillStyle='rgba(201,191,168,.65)'; x.font='10px Inter, sans-serif';
    for (let h=0; h<12; h++){
      const aCusp = ang(h*30); // 1st cusp at ASC longitude
      // angular cusps (1, 4, 7, 10) get stronger lines
      const angular = (h===0 || h===3 || h===6 || h===9);
      x.lineWidth = angular ? 1.5 : 0.8;
      x.strokeStyle = angular ? 'rgba(212,168,87,.65)' : 'rgba(212,168,87,.22)';
      x.beginPath();
      x.moveTo(cx, cy);
      x.lineTo(cx+Math.cos(aCusp)*rHouse, cy+Math.sin(aCusp)*rHouse);
      x.stroke();
      // house number sits inside the house wedge near the inner ring
      const aLbl = ang(h*30 + 15);
      const rLbl = rInner + 14;
      x.fillText(String(h+1), cx+Math.cos(aLbl)*rLbl, cy+Math.sin(aLbl)*rLbl);
    }

    // ASC, MC labels at angular cusps
    x.fillStyle='#d4a857'; x.font='bold 10px Inter, sans-serif';
    const aAsc = ang(L_asc), aMc = ang(L_asc + 90);
    x.fillText('ASC', cx+Math.cos(aAsc)*(rOuter+6) - 14, cy+Math.sin(aAsc)*(rOuter+6));
    x.fillText('IC',  cx+Math.cos(ang(L_asc+90))*(rOuter+6), cy+Math.sin(ang(L_asc+90))*(rOuter+6)+12);
    x.fillText('DSC', cx+Math.cos(ang(L_asc+180))*(rOuter+6) + 16, cy+Math.sin(ang(L_asc+180))*(rOuter+6));
    x.fillText('MC',  cx+Math.cos(ang(L_asc+270))*(rOuter+6), cy+Math.sin(ang(L_asc+270))*(rOuter+6)-8);

    // Plot planets from cfg.chart at their true ecliptic longitudes
    const bodies = Object.entries(cfg.chart)
      .filter(([k,v]) => v && v.sign && k !== 'asc')
      .map(([k,v]) => ({ key:k, glyph:PLANET_GLYPH[k] || '✶', L: lon(v) }));

    // simple anti-collision: nudge bodies within 8° of each other apart along the radial
    bodies.sort((a,b)=>a.L-b.L);
    const rPlanet = rHouse - 16;
    const placed = [];
    bodies.forEach(b=>{
      let r = rPlanet;
      while (placed.some(p => Math.abs((p.L - b.L + 540) % 360 - 180) < 8 && Math.abs(p.r - r) < 18)) {
        r -= 18;
      }
      placed.push({ ...b, r });
    });
    placed.forEach(p=>{
      const a = ang(p.L);
      const px = cx + Math.cos(a)*p.r, py = cy + Math.sin(a)*p.r;
      // glow
      const g = x.createRadialGradient(px, py, 0, px, py, 12);
      g.addColorStop(0,'rgba(212,168,87,.65)');
      g.addColorStop(.6,'rgba(212,168,87,.20)');
      g.addColorStop(1,'rgba(212,168,87,0)');
      x.fillStyle = g;
      x.beginPath(); x.arc(px, py, 12, 0, Math.PI*2); x.fill();
      // glyph
      x.fillStyle='#f4ecd8'; x.font='15px serif'; x.textAlign='center'; x.textBaseline='middle';
      x.fillText(p.glyph, px, py);
    });

    // Aspect lines between paired bodies if config provides cfg.aspects = [['sun','moon','conj']…]
    // Default: draw a conjunction line between sun and moon when both exist and within 8°
    const sun = cfg.chart.sun, moon = cfg.chart.moon;
    if (sun && moon) {
      const dL = Math.abs(((lon(sun) - lon(moon)) + 540) % 360 - 180);
      if (dL <= 8) {
        const a1 = ang(lon(sun)), a2 = ang(lon(moon));
        x.strokeStyle='rgba(212,168,87,.45)'; x.lineWidth=1;
        x.beginPath();
        x.moveTo(cx+Math.cos(a1)*(rHouse-14), cy+Math.sin(a1)*(rHouse-14));
        x.lineTo(cx+Math.cos(a2)*(rHouse-14), cy+Math.sin(a2)*(rHouse-14));
        x.stroke();
      }
    }
  }

  function drawResonance(canvas){
    const x = canvas.getContext('2d'); const W=canvas.width, H=canvas.height;
    x.clearRect(0,0,W,H);
    const pillars=['Year 庚','Month 己','Day 甲','Hour 丙'];
    const houses=['3rd · Mind','6th · Work','7th · Union','10th · Vocation','12th · Unseen'];
    const lx=140, rx=W-180;
    x.font='15px serif';
    pillars.forEach((p,i)=>{const y=40+i*52; x.fillStyle='#d4a857'; x.fillText(p,40,y+5); x.strokeStyle='rgba(212,168,87,.5)'; x.beginPath(); x.arc(lx,y,5,0,7); x.stroke();});
    houses.forEach((h,i)=>{const y=30+i*46; x.fillStyle='#c9bfa8'; x.fillText(h,rx+18,y+5); x.strokeStyle='rgba(212,168,87,.5)'; x.beginPath(); x.arc(rx,y,5,0,7); x.stroke();});
    const links=[[0,0,'g'],[1,1,'g'],[2,2,'g'],[2,3,'r'],[3,3,'g'],[0,4,'r'],[1,3,'r']];
    links.forEach(([a,b,col])=>{
      const y1=40+a*52, y2=30+b*46;
      x.strokeStyle = col==='g' ? 'rgba(212,168,87,.55)' : 'rgba(199,93,122,.55)';
      x.lineWidth = col==='g' ? 1.6 : 1.2;
      x.beginPath();
      x.moveTo(lx,y1);
      x.bezierCurveTo((lx+rx)/2,y1,(lx+rx)/2,y2,rx,y2);
      x.stroke();
    });
  }

  // ------- main init -------
  function init(userCfg){
    const cfg = Object.assign({}, DEFAULTS, userCfg || {});
    cfg.user  = Object.assign({}, DEFAULTS.user,  (userCfg && userCfg.user)  || {});
    cfg.chart = Object.assign({}, DEFAULTS.chart, (userCfg && userCfg.chart) || {});

    // 1. find the page container — fall back to body
    const page = document.querySelector(cfg.pageContainer) || document.body;

    // 2. inject page-level chrome: PD banner, audio bar, duo
    //    guard so a re-run of init() never double-injects the top chrome
    let top = page.querySelector(':scope > .nx-top');
    if (!top) {
      top = el('div','nx-host nx-top');
      top.appendChild(buildPersonalDayBanner(cfg));
      top.appendChild(buildAudioBar());
      top.appendChild(buildDuo(cfg));
      // mountTopAfter (if provided) inserts AFTER the selected element so the
      // existing masthead/header remains at the top of the reading
      const anchor = cfg.mountTopAfter ? page.querySelector(cfg.mountTopAfter) : null;
      if (anchor && anchor.nextSibling) page.insertBefore(top, anchor.nextSibling);
      else if (anchor) page.appendChild(top);
      else page.insertBefore(top, page.firstChild);

      // 3. animate canvases inside duo
      const constel = top.querySelector('.nx-constellation');
      if (constel) drawConstellation(constel, cfg);
      const wheel = top.querySelector('.nx-wheel');
      if (wheel) drawWheel(wheel, cfg);
    }

    // 4. find each section and inject features ADDITIVELY
    //    nothing existing is removed or rewritten
    const sections = document.querySelectorAll(cfg.sectionContainer);
    sections.forEach((sec, idx) => {
      const data = sectionData(idx, cfg);
      const title = sec.querySelector(cfg.sectionTitle);

      // 4a. Hermetic badge — place next to title without disturbing it
      if (title && !sec.querySelector('.nx-herm-badge')) {
        const row = el('div','nx-section-row');
        title.parentNode.insertBefore(row, title);
        row.appendChild(title);
        row.appendChild(buildHermBadge(data));
      }

      // 4b. Tarot + numerology chips — append after title row, BEFORE existing prose
      if (!sec.querySelector('.nx-chips')) {
        const chips = buildChips(data, cfg);
        const anchor = sec.querySelector('.nx-section-row') || title || sec.firstChild;
        if (anchor && anchor.nextSibling) sec.insertBefore(chips, anchor.nextSibling);
        else sec.appendChild(chips);
      }

      // 4c. Light/Shadow polarity — APPENDED to end of section
      if (!sec.querySelector('.nx-polarity')) sec.appendChild(buildPolarity(data));

      // 4d. The Working — APPENDED at the very end
      if (!sec.querySelector('.nx-working')) sec.appendChild(buildWorking(data));

      // tag the section with its index for the destroy() pass
      sec.classList.add('nx-touched');
    });

    // 5. Resonance map at end of page
    if (!page.querySelector('.nx-resonance')) {
      const reso = buildResonance();
      page.appendChild(reso);
      const c = reso.querySelector('.nx-reso-canvas');
      if (c) drawResonance(c);
    }

    return {
      sectionsEnhanced: sections.length,
      personalDay: personalDay(cfg.user.dob, cfg.today)
    };
  }

  // Cleanly remove every node this module injected. Lets the engine
  // re-init() with new data without a page reload.
  function destroy(cfg){
    cfg = cfg || {};
    const page = document.querySelector(cfg.pageContainer || DEFAULTS.pageContainer) || document.body;

    // Top chrome (PD banner + audio + duo)
    const top = page.querySelector(':scope > .nx-top');
    if (top) top.remove();

    // Per-section: chips, polarity, working
    document.querySelectorAll('.nx-chips, .nx-polarity, .nx-working').forEach(n=>n.remove());

    // Title rows: unwrap so original h2 returns to its native parent position
    document.querySelectorAll('.nx-section-row').forEach(row=>{
      const badge = row.querySelector('.nx-herm-badge');
      if (badge) badge.remove();
      while (row.firstChild) row.parentNode.insertBefore(row.firstChild, row);
      row.remove();
    });

    // Resonance map
    document.querySelectorAll('.nx-resonance').forEach(n=>n.remove());

    // remove our tag so re-init starts clean
    document.querySelectorAll('.nx-touched').forEach(n=>n.classList.remove('nx-touched'));
  }

  global.NumenEnhancements = {
    init,
    destroy,
    version: '0.2',
    // expose builders for manual injection or testing
    builders: {
      personalDayBanner: buildPersonalDayBanner,
      audioBar: buildAudioBar,
      duo: buildDuo,
      hermBadge: buildHermBadge,
      chips: buildChips,
      polarity: buildPolarity,
      working: buildWorking,
      resonance: buildResonance
    },
    draw: { constellation: drawConstellation, wheel: drawWheel, resonance: drawResonance },
    util: { reduce, personalDay }
  };
})(window);
