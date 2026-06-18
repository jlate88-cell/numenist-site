/* ============================================================
   NUMEN READING ENHANCEMENTS — additive-only injection
   v0.1 · drop-in script
   Adds 10 features to an existing astrology reading page
   WITHOUT modifying any existing text, headings, or markup.

   Usage:
     <link rel="stylesheet" href="numen-enhancements.css">
     <script src="numen-enhancements.js"></script>
     <script>
       NumenEnhancements.init({
         // OPTIONAL: override default selectors to match your real markup
         sectionContainer: '.reading-section',   // wraps one section
         sectionTitle:     'h2',                 // the h2 inside it
         sectionBody:      '.reading-section .body, .reading-section p',
         pageContainer:    '.reading-page',      // outer wrap of each page
         pageNumber:       2,                    // which page number is current (1..15)
         user: {
           name: 'Maverick',
           dob:  '1990-03-12',
           lifePath: 11, expression: 9
         },
         chart: {
           sun:  { sign:'Pisces', deg:24.87, house:7 },
           moon: { sign:'Pisces', deg:20.12, house:7 },
           asc:  { sign:'Virgo',  deg:18.45 }
         }
       });
     </script>

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
  // Hermetic principle per section number (1..15) — operator-tunable mapping
  const HERMETIC_BY_SECTION = {
    1:{glyph:'∞', name:'Correspondence'},
    2:{glyph:'☉', name:'Mentalism'},
    3:{glyph:'☾', name:'Vibration'},
    4:{glyph:'↑', name:'Rhythm'},
    5:{glyph:'♀', name:'Gender'},
    6:{glyph:'♃', name:'Cause & Effect'},
    7:{glyph:'♅', name:'Polarity'},
    8:{glyph:'☊', name:'Vibration'},
    9:{glyph:'△', name:'Correspondence'},
    10:{glyph:'⌛', name:'Rhythm'},
    11:{glyph:'四', name:'Correspondence'},
    12:{glyph:'日', name:'Vibration'},
    13:{glyph:'紫', name:'Mentalism'},
    14:{glyph:'運', name:'Rhythm'},
    15:{glyph:'⊕', name:'Polarity'}
  };
  // Default light/shadow placeholders — engine should replace with real per-section copy
  const POLARITY_DEFAULT = {
    light:'Add your light-side copy here — the gift, the trained expression, what this factor offers when integrated.',
    shadow:'Add your shadow-side copy here — the trap, the un-integrated pattern, what to watch for so the gift does not invert.'
  };
  // Working recommendation default scaffold — engine replaces with per-section ritual
  const WORKING_DEFAULT = {
    text:'Light a candle of the corresponding color. Speak the verse or invocation for this factor. Hold the breath for seven beats. The working seals when you snuff, not when you blow.',
    glyphs:'🕯️ ✶ ☾ ♓'
  };

  const DEFAULTS = {
    sectionContainer: '.reading-section, [data-section], section.reading',
    sectionTitle:     'h2',
    sectionBody:      'p',
    pageContainer:    '.reading-page, .page-content, main',
    pageNumber:       2,
    user: { name:'Operator', dob:'1990-01-01', lifePath:11, expression:9 },
    chart: {
      sun: {sign:'Pisces', deg:24.87, house:7},
      moon:{sign:'Pisces', deg:20.12, house:7},
      asc: {sign:'Virgo',  deg:18.45}
    },
    today: new Date()
  };

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

  function buildHermBadge(secNum){
    const h = HERMETIC_BY_SECTION[secNum] || {glyph:'✶', name:'Polarity'};
    const b = el('div','nx-herm-badge');
    b.innerHTML = `<div class="nx-herm-ring">${h.glyph}</div><div class="nx-herm-lbl">${h.name}</div>`;
    return b;
  }

  function buildChips(secNum, cfg){
    const wrap = el('div','nx-chips');
    const sun = cfg.chart.sun;
    const cards = [];
    if (TAROT[sun.sign]) cards.push({glyph:TAROT[sun.sign].split(' ')[0], name:TAROT[sun.sign].split(' · ')[1], k:`${sun.sign} sign`});
    if (HOUSE_TAROT[sun.house]) cards.push({glyph:HOUSE_TAROT[sun.house].split(' ')[0], name:HOUSE_TAROT[sun.house].split(' · ')[1], k:`${sun.house}th house`});
    cards.forEach(c=>{
      const chip = el('div','nx-chip');
      chip.innerHTML = `<div class="nx-chip-glyph">${c.glyph}</div><div class="nx-chip-meta"><div class="nx-chip-v">${c.name}</div><div class="nx-chip-k">${c.k}</div></div>`;
      wrap.appendChild(chip);
    });
    // Numerology chip
    const num = el('div','nx-chip nx-chip-num');
    num.innerHTML = `<div class="nx-chip-glyph">${cfg.user.expression}</div><div class="nx-chip-meta"><div class="nx-chip-v">Expression ${cfg.user.expression}</div><div class="nx-chip-k">Chaldean name</div></div>`;
    wrap.appendChild(num);
    return wrap;
  }

  function buildPolarity(){
    const p = el('div','nx-polarity');
    p.innerHTML = `
      <div class="nx-pol nx-pol-light">
        <div class="nx-pol-h"><span class="nx-dot"></span>Light — the gift</div>
        <p>${POLARITY_DEFAULT.light}</p>
      </div>
      <div class="nx-pol nx-pol-shadow">
        <div class="nx-pol-h"><span class="nx-dot"></span>Shadow — the trap</div>
        <p>${POLARITY_DEFAULT.shadow}</p>
      </div>`;
    return p;
  }

  function buildWorking(){
    const w = el('div','nx-working');
    w.innerHTML = `
      <div class="nx-working-h">The Working — boots on the ground</div>
      <p>${WORKING_DEFAULT.text}</p>
      <div class="nx-glyphs">${WORKING_DEFAULT.glyphs}</div>`;
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
  function drawConstellation(canvas, cfg){
    const x = canvas.getContext('2d'); const W=canvas.width, H=canvas.height;
    x.clearRect(0,0,W,H);
    // backdrop stars
    x.fillStyle = '#fff';
    for (let i=0;i<70;i++){
      const px=Math.random()*W, py=Math.random()*H, r=Math.random()*1.2;
      x.globalAlpha=Math.random()*.5+.15; x.beginPath(); x.arc(px,py,r,0,7); x.fill();
    }
    x.globalAlpha=1;
    // named points — Sun, Moon, Asc
    const pts = [
      {label:`☉ ${cfg.chart.sun.sign}`, x:W*0.62, y:H*0.30, big:true},
      {label:`☾ ${cfg.chart.moon.sign}`, x:W*0.74, y:H*0.22, big:true},
      {label:`↑ ${cfg.chart.asc.sign} ASC`, x:W*0.20, y:H*0.66, big:true},
      {label:'', x:W*0.40, y:H*0.42}, {label:'', x:W*0.50, y:H*0.55},
      {label:'', x:W*0.30, y:H*0.30}, {label:'', x:W*0.85, y:H*0.50}
    ];
    // connect a few
    x.strokeStyle='rgba(212,168,87,.4)'; x.lineWidth=1;
    x.beginPath(); x.moveTo(pts[0].x,pts[0].y);
    [3,4,1,6].forEach(i=>x.lineTo(pts[i].x,pts[i].y));
    x.stroke();
    x.beginPath(); x.moveTo(pts[2].x,pts[2].y); x.lineTo(pts[4].x,pts[4].y); x.stroke();
    // glow points
    pts.forEach(p=>{
      const r = p.big ? 4 : 2;
      const g = x.createRadialGradient(p.x,p.y,0,p.x,p.y,r*3.5);
      g.addColorStop(0,'#fff'); g.addColorStop(.4,'#d4a857'); g.addColorStop(1,'rgba(212,168,87,0)');
      x.fillStyle=g; x.beginPath(); x.arc(p.x,p.y,r*3.5,0,7); x.fill();
      x.fillStyle='#fff'; x.beginPath(); x.arc(p.x,p.y,r*.7,0,7); x.fill();
    });
    x.fillStyle='rgba(201,191,168,.8)'; x.font='11px Inter, sans-serif';
    pts.filter(p=>p.label).forEach(p=>x.fillText(p.label, p.x+10, p.y+4));
  }

  function drawWheel(canvas, cfg){
    const x = canvas.getContext('2d'); const W=canvas.width, H=canvas.height;
    const cx=W/2, cy=H/2;
    x.clearRect(0,0,W,H);
    x.strokeStyle='rgba(212,168,87,.5)'; x.lineWidth=1.2;
    [140,108,60].forEach(r=>{x.beginPath();x.arc(cx,cy,r,0,7);x.stroke();});
    for (let i=0;i<12;i++){
      const a=i*Math.PI/6;
      x.beginPath();
      x.moveTo(cx+Math.cos(a)*108, cy+Math.sin(a)*108);
      x.lineTo(cx+Math.cos(a)*140, cy+Math.sin(a)*140);
      x.stroke();
    }
    const glyphs=['☉','☾','☿','♀','♂','♃','♄','♅','♆','♇'];
    const angles=[20,25,200,210,300,140,250,95,98,70];
    x.fillStyle='#d4a857'; x.font='15px serif';
    angles.forEach((d,i)=>{
      const a=(d-90)*Math.PI/180, r=124;
      x.fillText(glyphs[i], cx+Math.cos(a)*r-7, cy+Math.sin(a)*r+5);
    });
    x.strokeStyle='rgba(199,93,122,.6)';
    x.beginPath();
    x.moveTo(cx+Math.cos(-1.2)*60, cy+Math.sin(-1.2)*60);
    x.lineTo(cx+Math.cos(2.0)*60, cy+Math.sin(2.0)*60);
    x.stroke();
    x.strokeStyle='rgba(106,61,142,.6)';
    x.beginPath();
    x.moveTo(cx+Math.cos(.5)*60, cy+Math.sin(.5)*60);
    x.lineTo(cx+Math.cos(3.3)*60, cy+Math.sin(3.3)*60);
    x.stroke();
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

    // 2. inject page-level chrome at the top: PD banner, audio bar, duo
    //    guard so a re-run of init() never double-injects the top chrome
    let top = page.querySelector(':scope > .nx-top');
    if (!top) {
      top = el('div','nx-host nx-top');
      top.appendChild(buildPersonalDayBanner(cfg));
      top.appendChild(buildAudioBar());
      top.appendChild(buildDuo(cfg));
      page.insertBefore(top, page.firstChild);

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
      const secNum = idx + 1;
      const title = sec.querySelector(cfg.sectionTitle);

      // 4a. Hermetic badge — place next to title without disturbing it
      if (title && !sec.querySelector('.nx-herm-badge')) {
        const row = el('div','nx-section-row');
        // wrap title in row so badge can sit beside it; original title element is reused, not replaced
        title.parentNode.insertBefore(row, title);
        row.appendChild(title);
        row.appendChild(buildHermBadge(secNum));
      }

      // 4b. Tarot + numerology chips — append after title row, BEFORE existing prose
      if (!sec.querySelector('.nx-chips')) {
        const chips = buildChips(secNum, cfg);
        // place after the title-row if it exists, else after title, else at top
        const anchor = sec.querySelector('.nx-section-row') || title || sec.firstChild;
        if (anchor && anchor.nextSibling) sec.insertBefore(chips, anchor.nextSibling);
        else sec.appendChild(chips);
      }

      // 4c. Light/Shadow — APPENDED to end of section, ADDS to existing content
      if (!sec.querySelector('.nx-polarity')) sec.appendChild(buildPolarity());

      // 4d. Working — APPENDED at the very end
      if (!sec.querySelector('.nx-working')) sec.appendChild(buildWorking());
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

  global.NumenEnhancements = {
    init,
    version: '0.1',
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
