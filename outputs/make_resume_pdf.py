#!/usr/bin/env python3
# Zero-dependency PDF resume generator (stdlib only). Core fonts, no embedding.
import zlib, textwrap

# Helvetica / Helvetica-Bold AFM widths (units/1000) for ASCII 32..126
HELV = [278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584]
HELVB = [278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584]

def cw(ch, bold):
    o = ord(ch)
    if 32 <= o <= 126:
        return (HELVB if bold else HELV)[o-32]
    return 556

def text_width(s, size, bold):
    return sum(cw(c, bold) for c in s) * size / 1000.0

def wrap(s, size, bold, maxw):
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = w if not cur else cur + ' ' + w
        if text_width(trial, size, bold) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

PAGE_W, PAGE_H = 612, 792           # US Letter pts
ML, MR, MT, MB = 46, 46, 40, 40
CONTENT_W = PAGE_W - ML - MR

pages, ops, y = [], [], PAGE_H - MT

def esc(s):
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')

def newpage():
    global ops, y
    if ops:
        pages.append(ops)
    ops = []
    y = PAGE_H - MT

def need(h):
    if y - h < MB:
        newpage()

def line(txt, size=9.7, bold=False, gap=1.0, indent=0, bullet=False):
    global y
    fnt = 'F2' if bold else 'F1'
    avail = CONTENT_W - indent - (12 if bullet else 0)
    for i, ln in enumerate(wrap(txt, size, bold, avail)):
        need(size + gap)
        x = ML + indent
        if bullet and i == 0:
            ops.append(f"BT /F1 {size} Tf {x} {y - size:.1f} Td (•) Tj ET".replace('•', '\\225'))
        bx = x + (12 if bullet else 0)
        ops.append(f"BT /{fnt} {size} Tf {bx:.1f} {y - size:.1f} Td ({esc(ln)}) Tj ET")
        y -= size + gap

def rule():
    global y
    need(5)
    ops.append(f"{ML} {y:.1f} m {PAGE_W-MR} {y:.1f} l 0.6 w S")
    y -= 5

def H(txt):
    global y
    need(22)
    y -= 4
    line(txt.upper(), size=10.5, bold=True, gap=2)
    rule()

def gap(h):
    global y
    y -= h

# ---------- CONTENT ----------
line("JORDAN ROSS ATKINS", size=20, bold=True, gap=3)
line("Atlanta, GA  -  678-300-5577  -  jlate88@gmail.com  -  [ADD: LinkedIn / portfolio URL]",
     size=9.5, gap=3)
gap(4)

H("Professional Summary")
line("Trained to read a scene before anyone else can. 17 years a filmmaker "
     "controlling composition, continuity, and pacing; now a Georgia blue-card "
     "armed agent making real-time threat assessments on private "
     "executive-protection details for national broadcast talent (Fox News, CNN); "
     "and self-taught builder of autonomous multi-agent AI, local-LLM robotics, "
     "and versioned LLM instruction architectures with verification protocols. "
     "One discipline across three arenas - spotting what is wrong, missing, or "
     "false before it ships. Seeking remote AI evaluation/training, AI "
     "video/commercial production, or technical support - measured on the "
     "assessment, not a transcript.")

H("Core Skills")
line("AI / ML: LLM output evaluation, prompt engineering, agentic systems design, "
     "multi-agent orchestration, AI behavior/instruction design, model-output review",
     bullet=True)
line("AI Media: end-to-end AI video & image generation - Higgsfield AI (full "
     "suite), Google Veo / Google Labs, Kling, Midjourney (advanced: scene "
     "construction, character consistency); hyper-realistic and animated "
     "commercial production", bullet=True)
line("Film & Post: cinematography, editing, color correction (DaVinci Resolve, "
     "CapCut), music editing & recording; composition, continuity, scene flow",
     bullet=True)
line("Automation: autonomous task pipelines, multi-session orchestration, "
     "cross-application automation bridges, custom event-hook pipelines", bullet=True)
line("Development: Python, Bash/Shell, HTML/CSS, Git, Linux system administration "
     "[CONFIRM/ADD: any other languages you use]", bullet=True)
line("AI Tooling: ChatGPT, Claude / LLM APIs, self-hosted/local LLM deployment, "
     "Raspberry Pi, terminal-driven development [CONFIRM/ADD: Agent SDK, n8n/Make]",
     bullet=True)

H("Selected Projects")
line("J-5 - Personal Robotics & Local-LLM Build  (2025)", bold=True, gap=2)
line("Self-built robotics project: Raspberry Pi hardware, camera vision ('eyes'), "
     "laptop-hosted local LLM ('brain'). Hand-coded via terminal to run a private "
     "self-hosted LLM ahead of mainstream adoption.")
line("Ultronos - Autonomous Multi-Agent System  (2025-Present)", bold=True, gap=2)
line("Multi-agent automation system that runs tasks independently and reports "
     "status across separate sessions.")
line("LLM System-Prompt & Instruction Architecture  (2026)", bold=True, gap=2)
line("Authored large-scale, versioned system-prompt and multi-agent instruction "
     "frameworks (10,000+ words) with built-in verification/audit protocols and "
     "version control - advanced prompt engineering and AI behavior design.")
line("AI Commercial & Video Production  (2025-Present)", bold=True, gap=2)
line("Trained under a mentor producing AI-driven commercial work. Direct Veo, "
     "Kling, Higgsfield, and Midjourney on a 17-year filmmaking foundation to "
     "produce hyper-realistic and animated commercials end to end - human taste, "
     "not the tool, is the deliverable; original animated short in development.")

H("Experience")
line("Executive Protection / Armed Security Agent - C2 Security Group, "
     "Atlanta, GA  (October 2023-Present)", bold=True, gap=2)
line("Close-protection details for national broadcast media personnel "
     "(Fox News, CNN), entertainment and music-industry talent, private and "
     "preschool campuses, and corporate/retail sites under managed-threat "
     "conditions", bullet=True)
line("Armed agent with a veteran-owned firm (BBB A+, Voted Best of Georgia 2025) "
     "contracted to the Jewish Federation of Greater Atlanta, the Secure "
     "Community Network, and the MJCCA - sustained high-threat-environment "
     "protection", bullet=True)
line("Georgia blue-card registered armed guard; real-time threat assessment, "
     "zero-margin judgment; self-trained in software and AI systems on duty",
     bullet=True)
gap(2)
line("Independent Filmmaker, Editor & Music Producer  (2008-Present)",
     bold=True, gap=2)
line("17 years shooting, editing, acting, and co-starring in short films; "
     "intricate music editing and recording", bullet=True)
line("Frame-level command of composition, symmetry, continuity, and emotional "
     "pacing - the craft eye AI generation lacks and the foundation that makes "
     "the AI film work credible", bullet=True)
gap(2)
line("Insurance Sales Closer - Legacy Health Insurance, Los Angeles, CA  "
     "(2018-2019)", bold=True, gap=2)
line("Ranked #1 closer five consecutive months; cold-call acquisition, needs "
     "analysis, objection handling, close; trained incoming sales staff",
     bullet=True)
gap(2)
line("Additional Experience  (2003-2018, GA / LA)", bold=True, gap=2)
line("Saucier - Cafe Del Rey (fine dining, LA);  Stone Restoration - F.D. Atkins "
     "& Associates;  Repossession Scout - Wilder Repo;  Auto Driver - Georgia's "
     "Elite Auto Sales;  Line Cook - Bones Restaurant, Atlanta", bullet=True)

H("Education")
line("High School Diploma - Alexander High School, Douglasville, GA")

newpage()

# ---------- ASSEMBLE PDF ----------
objs = []
def add(o):
    objs.append(o); return len(objs)

font1 = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
font2 = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

kids, page_objs = [], []
content_ids = []
for pg in pages:
    stream = ("\n".join(pg)).encode('latin-1', 'replace')
    comp = zlib.compress(stream)
    cid = add(b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(comp)
              + comp + b"\nendstream")
    content_ids.append(cid)

pages_parent_id = len(objs) + len(pages) + 1
for i, cid in enumerate(content_ids):
    pid = add(
        ("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] "
         "/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> "
         "/Contents %d 0 R >>" % (pages_parent_id, PAGE_W, PAGE_H,
                                  font1, font2, cid)).encode())
    page_objs.append(pid)

kids_str = " ".join("%d 0 R" % p for p in page_objs)
pages_id = add(("<< /Type /Pages /Count %d /Kids [%s] >>"
                % (len(page_objs), kids_str)).encode())
catalog_id = add(("<< /Type /Catalog /Pages %d 0 R >>" % pages_id).encode())

out = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
offsets = [0]
for i, body in enumerate(objs, 1):
    offsets.append(len(out))
    out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
xref_pos = len(out)
out += b"xref\n0 %d\n" % (len(objs)+1)
out += b"0000000000 65535 f \n"
for off in offsets[1:]:
    out += b"%010d 00000 n \n" % off
out += (b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF"
        % (len(objs)+1, catalog_id, xref_pos))

with open("/home/user/numenist-site/outputs/Jordan_Ross_Atkins_Resume_2026.pdf",
          "wb") as f:
    f.write(out)
print("PDF written: %d pages, %d bytes" % (len(pages), len(out)))
