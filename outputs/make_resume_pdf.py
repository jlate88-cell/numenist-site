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
            ops.append(f"BT /F1 {size} Tf {x} {y - size:.1f} Td (-) Tj ET")
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
line("Atlanta, GA  |  678-300-5577  |  jlate88@gmail.com",
     size=9.5, gap=3)
gap(4)

H("Summary")
line("Armed executive protection agent and self-taught AI builder. I run "
     "close-protection details for on-air talent at Fox News and CNN, plus "
     "entertainment and high-threat institutional clients, through a licensed, "
     "veteran-owned Atlanta firm. On post downtime over the last few years I "
     "taught myself to code from the terminal and built real systems: a robot "
     "running a local language model offline before that was common, an "
     "autonomous AI content and automation factory that routes work across "
     "multiple media providers and publishes finished products on its own, and a "
     "shipped numerology product. Seventeen years making and editing films before "
     "any of this, which is the eye behind the AI video work. I am looking for "
     "remote work in AI evaluation and training, AI content and video production, "
     "automation engineering, or technical support.")

H("Core Skills")
line("AI / ML: LLM output evaluation and audit, prompt engineering, agent "
     "systems and orchestration, AI behavior and instruction design, building "
     "structured verification frameworks", bullet=True)
line("AI media: image, video, and audio generation across Higgsfield AI, "
     "Google Veo, Kling, and Midjourney; multi-provider routing; hyper-real and "
     "animated commercial work start to finish", bullet=True)
line("Film and post: shooting, editing, color grading (DaVinci Resolve, "
     "CapCut), music editing and recording; seventeen years hands-on", bullet=True)
line("Code and systems: Python, Bash, HTML/CSS, Git, Linux. Self-hosted and "
     "local LLMs, Raspberry Pi hardware, terminal-driven builds, automation "
     "pipelines", bullet=True)

H("Projects")
line("Ultronos, AI content and automation factory  (2025 to now)", bold=True, gap=2)
line("End-to-end pipeline that takes a content job, routes each step to the "
     "right model across multiple image, video, and audio AI providers, then "
     "runs the result through an autonomous audit gate that checks quality "
     "before anything is released. Approved products auto-publish to Etsy and "
     "Gumroad with no manual step. It runs on its own.", bullet=True)
line("Numen / Quintiform, numerology product  (2025 to now)", bold=True, gap=2)
line("Designed and shipped a numerology product built on a structured "
     "calculation engine that turns birth data into full personalized written "
     "readings. Packaged and sold as a paid digital product.", bullet=True)
line("J-5, personal robot and local LLM  (2025)", bold=True, gap=2)
line("Built a robot from a Raspberry Pi with a camera for vision and my laptop "
     "running a local language model as the brain. Hand-coded the whole thing "
     "through the terminal, learning as I went, to get a private model running "
     "fully offline before that was common or easy.", bullet=True)
line("LLM instruction systems  (2026)", bold=True, gap=2)
line("Wrote large, versioned instruction frameworks for language models, over "
     "10,000 words each, with my own verification and audit checks, version "
     "control, and behavior rules built in. Deep prompt engineering and AI "
     "behavior design.", bullet=True)
line("AI commercial production  (2025 to now)", bold=True, gap=2)
line("Trained under a mentor who produces AI commercial work. I direct Veo, "
     "Kling, Higgsfield, and Midjourney off a real filmmaking background, which "
     "is why the output reads like film instead of generated clips. Hyper-real "
     "and animated. An original animated short is in progress.", bullet=True)

H("Experience")
line("Executive Protection / Armed Agent. C2 Security Group, Atlanta, GA. "
     "October 2023 to present.", bold=True, gap=2)
line("Close-protection and advance details for on-air talent at Fox News and "
     "CNN, entertainment and music clients, private and preschool campuses, and "
     "corporate and retail sites", bullet=True)
line("Real-time threat assessment and protective coverage with no margin for "
     "error; armed post and detail work across high-profile and high-sensitivity "
     "clients", bullet=True)
line("C2 is veteran-owned, BBB A+, and Voted Best of Georgia 2025, contracted "
     "to the Jewish Federation of Greater Atlanta, the Secure Community Network, "
     "and the MJCCA", bullet=True)
line("Georgia blue-card armed guard. Taught myself software and AI on post "
     "between assignments and shipped the systems above while working full duty",
     bullet=True)
gap(2)
line("Filmmaker, Editor, and Music Producer. 2008 to present.", bold=True, gap=2)
line("Seventeen years shooting, editing, acting, and co-starring in short "
     "films, plus music editing and recording", bullet=True)
line("Hands-on command of framing, continuity, color, and timing; this is the "
     "craft eye that makes the AI video work hold up", bullet=True)
gap(2)
line("Insurance Sales Closer. Legacy Health Insurance, Los Angeles, CA. "
     "2018 to 2019.", bold=True, gap=2)
line("Number one closer five months running. Cold-call acquisition, needs "
     "analysis, and closing. Trained new reps", bullet=True)
gap(2)
line("Earlier work  (2003 to 2018)", bold=True, gap=2)
line("Saucier at Cafe Del Rey (fine dining, LA). Stone restoration with F.D. "
     "Atkins. Repossession scout at Wilder. Auto driver at Georgia's Elite. Line "
     "cook at Bones, Atlanta.", bullet=True)

H("Education")
line("High School Diploma. Alexander High School, Douglasville, GA.")

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
