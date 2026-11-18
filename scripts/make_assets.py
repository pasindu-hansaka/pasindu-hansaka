# Generates the README artwork in assets/. Run: python scripts/make_assets.py && THEME=dark python scripts/make_assets.py
import os
import textwrap
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SERIF = "'EB Garamond','Cormorant Garamond',Garamond,Baskerville,'Times New Roman',Georgia,serif"
SCRIPT = "'Snell Roundhand','Apple Chancery','Segoe Script','Brush Script MT','URW Chancery L',cursive"
import os
DARK = os.environ.get("THEME") == "dark"
SUF = "-dark" if DARK else ""
if DARK:
    PAGE, INK, SEPIA, FAINT, WAX = "#0d1117", "#e6edf3", "#9198a1", "#3d444d", "#e5736b"
else:
    PAGE, INK, SEPIA, FAINT, WAX = "#ffffff", "#1f2328", "#59636e", "#d1d9e0", "#9a2a2a"
PAPER = PAGE
RM = "@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}}"

def paper_defs(W, H):
    return ""
    return f'''<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch" seed="3"/>
<feColorMatrix values="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .09 0"/></filter>
<filter id="blot" x="-50%" y="-50%" width="200%" height="200%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .4  0 0 0 0 .2  0 0 0 .18 -.04"/></filter>
<radialGradient id="age" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="{PAPER}" stop-opacity="0"/><stop offset="1" stop-color="{PAPER2}"/></radialGradient>'''

def paper(W, H, border=False):
    return (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{FAINT}"/>' if border else "")
    return (f'<rect width="{W}" height="{H}" rx="4" fill="{PAPER}"/>'
            f'<rect width="{W}" height="{H}" rx="4" filter="url(#blot)"/>'
            f'<rect width="{W}" height="{H}" rx="4" fill="url(#age)"/>'
            f'<rect width="{W}" height="{H}" rx="4" filter="url(#grain)"/>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="4" fill="none" stroke="{FAINT}"/>')

BASE_CSS = f'''text{{font-family:{SERIF};fill:{INK}}}
.in{{animation:in 1.4s ease-out both}}@keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.fade{{animation:fade 1.6s ease-out both}}@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.stamp{{animation:stamp .6s cubic-bezier(.2,1.4,.4,1) both;transform-box:fill-box;transform-origin:center}}
@keyframes stamp{{0%{{opacity:0;transform:scale(1.8) rotate(-8deg)}}100%{{opacity:1;transform:none}}}}
.ink{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 2.2s ease-in-out forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}
{RM}'''

def pen(i, x, y, h, w, begin, dur):
    """clipPath that reveals text left-to-right like a pen stroke"""
    return (f'<clipPath id="p{i}"><rect x="{x}" y="{y}" height="{h}" width="0">'
            f'<animate attributeName="width" values="0;{w}" begin="{begin}s" dur="{dur}s" calcMode="spline" keyTimes="0;1" keySplines=".45 0 .55 1" fill="freeze"/></rect></clipPath>')

def seal(cx, cy, r, delay, text="PH"):
    pts = []
    import math
    for k in range(28):
        a = k / 28 * 2 * math.pi
        rr = r + (3 if k % 2 else -1)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return (f'<g class="stamp" style="animation-delay:{delay}s"><polygon points="{" ".join(pts)}" fill="#8e1b1b"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="#5e0f0f" stroke-width="2"/>'
            f'<circle cx="{cx-r*.35}" cy="{cy-r*.4}" r="{r*.22}" fill="#fff" fill-opacity=".12"/>'
            f'<text x="{cx}" y="{cy+r*.28}" text-anchor="middle" font-size="{r*.8:.0f}" font-style="italic" style="fill:#f1d9c0;font-family:{SERIF}">{text}</text></g>')

def write(n, s): open(f"{A}/{n[:-4]}{SUF}.svg", "w").write(s)

# ---------------- hero: letterhead ----------------
W, H = 1200, 320
write("letterhead.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Pasindu Hansaka - Python, AI agents and control systems">
<defs>{paper_defs(W,H)}{pen(0, 80, 90, 110, 900, .3, 2.4)}<style>{BASE_CSS}</style></defs>
{paper(W,H)}
<text class="fade" x="100" y="70" font-size="14" letter-spacing="5" style="fill:{SEPIA}">FROM THE DESK OF</text>
<text x="96" y="168" font-size="84" font-weight="500" clip-path="url(#p0)">Pasindu Hansaka</text>
<path class="ink" d="M100 196 C300 186 520 204 760 192" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" style="animation-delay:2.4s"/>
<text class="in" x="100" y="240" font-size="21" letter-spacing="5" style="fill:{SEPIA};animation-delay:2.8s">PYTHON  ·  AI AGENTS  ·  CONTROL SYSTEMS</text>
<text class="in" x="100" y="276" font-size="17" font-style="italic" style="fill:{SEPIA};animation-delay:3.2s">Correspondence on code, machines and curiosity — est. MMXXV</text>
{seal(1040, 160, 62, 3.6)}
</svg>''')

# ---------------- divider: ink flourish ----------------
write("divider.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 40" width="1200" height="40" role="img" aria-label="divider">
<style>{BASE_CSS}</style>
<path class="ink" d="M300 20 C400 20 470 8 540 20 S585 32 600 20 S615 8 660 20 S800 20 900 20" fill="none" stroke="{SEPIA}" stroke-width="1.4" stroke-linecap="round"/>
<circle class="fade" cx="600" cy="20" r="3" fill="{SEPIA}" style="animation-delay:1.6s"/>
</svg>''')

# ---------------- toolbox: one compact row of stamps ----------------
items = ["Python", "C++", "Jupyter", "MATLAB", "Simulink", "Git", "GitHub"]
import random; rnd = random.Random(4)
widths = [30 + len(it) * 10 for it in items]; gap = 12
W = sum(widths) + gap * (len(items) - 1) + 80; H = 130; out = []; x = 40; y = 92
for k, (it, w) in enumerate(zip(items, widths)):
    rot = rnd.uniform(-3, 3)
    out.append(f'<g transform="rotate({rot:.1f} {x+w/2:.0f} {y})"><g class="stamp" style="animation-delay:{0.5+k*0.2:.2f}s">'
               f'<rect x="{x}" y="{y-17}" width="{w}" height="30" rx="3" fill="none" stroke="{WAX}" stroke-width="1.8" stroke-opacity=".85"/>'
               f'<rect x="{x+3}" y="{y-14}" width="{w-6}" height="24" rx="2" fill="none" stroke="{WAX}" stroke-opacity=".4"/>'
               f'<text x="{x+w/2:.0f}" y="{y+5}" text-anchor="middle" font-size="16" letter-spacing="1" style="fill:{WAX}">{it.upper()}</text></g></g>')
    x += w + gap
write("toolbox.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack: {", ".join(items)}">
<defs>{paper_defs(W,H)}{pen(0, 0, 18, 40, W, .1, 1)}<style>{BASE_CSS}</style></defs>
{paper(W,H)}
<text x="40" y="46" font-size="22" font-style="italic" clip-path="url(#p0)">Instruments of the Trade</text>
<path class="ink" d="M40 56 H230" stroke="{FAINT}" style="animation-delay:.6s"/>
{"".join(out)}
</svg>''')

# ---------------- project cards: postcards ----------------
projects = [("PSB-Chatbot", "An AI-powered academic assistant for PSB students.", "Python", "ai", "I"),
            ("file-organizer", "A Python CLI that sorts files into type-based folders: images, documents, videos and more.", "Python", "cli", "II"),
            ("self-balancing-unicycle", "A MATLAB/Simulink model of a self-balancing unicycle with a PID controller.", "MATLAB", "sim", "III"),
            ("pasindu-hansaka.github.io", "My personal portfolio website.", "HTML", "web", "IV")]
for i, (name, desc, lang, slug, num) in enumerate(projects):
    W, H = 440, 220
    lines = textwrap.wrap(desc, 34)[:3]
    dt = "".join(f'<text x="30" y="{112+j*24}" font-size="17" font-style="italic" style="fill:{SEPIA}">{l}</text>' for j, l in enumerate(lines))
    sx, sy = W-92, 24  # postage stamp
    perf = "".join(f'<circle cx="{sx+k*8}" cy="{sy}" r="2.4" fill="{PAPER}"/><circle cx="{sx+k*8}" cy="{sy+74}" r="2.4" fill="{PAPER}"/>' for k in range(9)) + \
           "".join(f'<circle cx="{sx}" cy="{sy+k*8+5}" r="2.4" fill="{PAPER}"/><circle cx="{sx+64}" cy="{sy+k*8+5}" r="2.4" fill="{PAPER}"/>' for k in range(9))
    d0 = 0.2
    write(f"project-{slug}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{name}: {desc}">
<defs>{paper_defs(W,H)}{pen(0, 20, 34, 40, 320, d0+.3, 1.2)}<style>{BASE_CSS}</style></defs>
{paper(W,H,True)}
<g class="stamp" style="animation-delay:{d0+1.4:.1f}s"><rect x="{sx}" y="{sy}" width="64" height="74" fill="#8e1b1b"/>{perf}
<rect x="{sx+7}" y="{sy+8}" width="50" height="58" fill="none" stroke="#f6efe4" stroke-opacity=".7"/>
<text x="{sx+32}" y="{sy+48}" text-anchor="middle" font-size="22" font-style="italic" style="fill:#f6efe4">{num}</text></g>
<g class="fade" style="animation-delay:{d0+1.8:.1f}s" fill="none" stroke="{INK}" stroke-opacity=".35"><circle cx="{sx-14}" cy="{sy+56}" r="24"/><path d="M{sx+6} {sy+46} q12 -6 24 0 t24 0 M{sx+6} {sy+56} q12 -6 24 0 t24 0 M{sx+6} {sy+66} q12 -6 24 0 t24 0"/></g>
<text x="30" y="66" font-size="{26 if len(name) < 18 else 22}" font-weight="600" clip-path="url(#p0)">{name}</text>
<path class="ink" d="M30 80 H220" stroke="{FAINT}" style="animation-delay:{d0+1.3:.1f}s"/>
<g class="fade" style="animation-delay:{d0+1.1:.1f}s">{dt}</g>
<text class="fade" x="30" y="{H-24}" font-size="13" letter-spacing="3" style="fill:{SEPIA};animation-delay:{d0+2:.1f}s">{lang.upper()}</text>
<text class="fade" x="{W-30}" y="{H-24}" text-anchor="end" font-size="13" letter-spacing="3" style="fill:{WAX};animation-delay:{d0+2:.1f}s">READ MORE ›</text>
</svg>''')
print("ok")

# ---------------- workbench: a unicycle sketched in ink, then balancing ----------------
import math
def gear(cx, cy, r, teeth, depth=7):
    pts = []
    for k in range(teeth * 4):
        a = k / (teeth * 4) * 2 * math.pi
        rr = r + (depth if k % 4 in (1, 2) else 0)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}"/><circle cx="{cx}" cy="{cy}" r="{r*.35:.1f}"/><circle cx="{cx}" cy="{cy}" r="3"/>'

W, H = 1000, 300
wx, wy, wr = 190, 205, 55   # wheel
spokes = "".join(f'<path d="M{wx} {wy} L{wx+wr*math.cos(k*math.pi/4):.1f} {wy+wr*math.sin(k*math.pi/4):.1f}"/>' for k in range(8))
fx, fy, fr = 190, 70, 34    # flywheel (reaction wheel)
fspokes = "".join(f'<path d="M{fx} {fy} L{fx+fr*math.cos(k*math.pi/3):.1f} {fy+fr*math.sin(k*math.pi/3):.1f}"/>' for k in range(6))
notes = [("AI &amp; ML research at Hochschule München", "Research intern · Python"),
         ("Controllers that keep things upright", "MATLAB/Simulink"),
         ("Driverless planning and SLAM", "ROS · Formula Student")]
note_svg = []
for i, (t, tag) in enumerate(notes):
    y = 128 + i * 46; d = 2.6 + i * 0.7
    note_svg.append(pen(10 + i, 560, y - 26, 40, 400, d, 0.9))
    note_svg.append(f'<text x="566" y="{y}" font-size="21" clip-path="url(#p{10+i})">{t}</text>')
    note_svg.append(f'<text class="fade" x="568" y="{y+20}" font-size="12" letter-spacing="3" style="fill:{WAX};animation-delay:{d+0.6:.1f}s">{tag.upper()}</text>')
write("workbench.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="On the workbench: an ink sketch of a self-balancing unicycle being drawn, with turning gears. AI and machine learning research at Hochschule München, controllers in MATLAB/Simulink and driverless planning and SLAM for Formula Student.">
<defs>{paper_defs(W,H)}{pen(9, 560, 36, 50, 400, 2.0, 1)}<style>{BASE_CSS}
.sk{{fill:none;stroke:{INK};stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.thin{{stroke-width:1.1;stroke-opacity:.7}}
.d1{{stroke-dasharray:400;stroke-dashoffset:400;animation:draw 1.4s ease-in-out forwards}}
.bal{{transform-origin:{wx}px {wy+wr}px;animation:bal 3.2s 2.6s ease-in-out infinite alternate}}
@keyframes bal{{from{{transform:rotate(-3.5deg)}}to{{transform:rotate(3.5deg)}}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 2.4s 2.6s linear infinite}}
.spinr{{animation-direction:reverse;animation-duration:1.6s}}
.slow{{animation-duration:6s}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.dim{{stroke-dasharray:4 4;animation:fade 1s 2.2s both}}
</style></defs>
{paper(W,H)}
<!-- ground -->
<path class="sk thin d1" d="M60 {wy+wr} H340"/>
{"".join(f'<path class="sk thin fade" d="M{x} {wy+wr} l-10 10" style="animation-delay:.6s"/>' for x in range(75, 340, 18))}
<!-- the unicycle, balancing -->
<g class="bal">
  <g class="sk">
    <circle class="d1" cx="{wx}" cy="{wy}" r="{wr}" style="animation-delay:.2s"/>
    <g class="spin slow"><g class="thin fade" style="animation-delay:1s">{spokes}</g></g>
    <circle cx="{wx}" cy="{wy}" r="5" class="fade" style="animation-delay:.9s"/>
    <path class="d1" d="M{wx-7} {wy} V{fy+fr+14} M{wx+7} {wy} V{fy+fr+14} M{wx-16} {fy+fr+14} H{wx+16} M{wx} {fy+fr+14} V{fy}" style="animation-delay:.8s"/>
    <circle class="d1" cx="{fx}" cy="{fy}" r="{fr}" style="animation-delay:1.3s"/>
    <g class="spin"><g class="thin fade" style="animation-delay:1.9s">{fspokes}</g></g>
    <circle cx="{fx}" cy="{fy}" r="4" class="fade" style="animation-delay:1.8s"/>
  </g>
</g>
<!-- dimension line + annotation -->
<g class="sk thin" style="stroke:{WAX}"><path class="dim" d="M{wx+wr+40} {fy} V{wy+wr}"/><path class="dim" d="M{wx+wr+32} {fy} h16 M{wx+wr+32} {wy+wr} h16"/></g>
<text class="fade" x="{wx+wr+52}" y="{(fy+wy+wr)//2}" font-size="13" font-style="italic" style="fill:{WAX};animation-delay:2.3s">θ → 0</text>
<!-- gears -->
<g style="fill:none;stroke:{INK};stroke-width:1.6" class="fade" >
  <g class="spin" style="animation-duration:8s">{gear(420, 120, 36, 12)}</g>
  <g class="spin spinr" style="animation-duration:5.4s">{gear(470, 182, 22, 8, 6)}</g>
</g>
<!-- notes -->
<text x="560" y="74" font-size="30" font-style="italic" clip-path="url(#p9)">Currently building</text>
<path class="ink" d="M562 88 H760" stroke="{FAINT}" style="animation-delay:2.4s"/>
{"".join(note_svg)}
</svg>''')
