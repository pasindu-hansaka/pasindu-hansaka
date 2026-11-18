"""Render an animated contribution-activity SVG from a user's GitHub contribution calendar.

Usage: GITHUB_TOKEN=... python scripts/activity.py <username> <out.svg>
       python scripts/activity.py --sample <out.svg>   (random data, for previews)
Standard library only.
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
COLORS = ["#e6d7b6", "#cdb283", "#a8875a", "#76593a", "#3e2c1c"]


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "readme-activity-svg"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return [[(d["date"], d["contributionCount"], LEVEL[d["contributionLevel"]]) for d in w["contributionDays"]]
            for w in cal["weeks"]]


def sample():
    rnd = random.Random(7)
    end = dt.date.today()
    start = end - dt.timedelta(days=end.weekday() + 1 + 52 * 7)
    weeks, d = [], start
    while d <= end:
        week = []
        for _ in range(7):
            if d > end:
                break
            c = 0 if rnd.random() < 0.45 else rnd.choice([1, 1, 2, 3, 4, 6, 9, 14])
            week.append((d.isoformat(), c, 0 if c == 0 else min(4, 1 + c // 4)))
            d += dt.timedelta(days=1)
        weeks.append(week)
    return weeks


def streaks(days):
    cur = best = run = 0
    for _, c, _ in days:
        run = run + 1 if c else 0
        best = max(best, run)
    for i, (_, c, _) in enumerate(reversed(days)):
        if c:
            cur += 1
        elif i == 0:  # today may still be empty
            continue
        else:
            break
    return cur, best


def render(weeks):
    days = [d for w in weeks for d in w]
    total = sum(c for _, c, _ in days)
    cur, best = streaks(days)
    peak = max(days, key=lambda d: d[1])
    peak_label = dt.date.fromisoformat(peak[0]).strftime("%b %d")

    cell, gap = 12, 3
    gx, gy = 60, 150
    W, H = max(900, gx + len(weeks) * (cell + gap) + 40), 380
    out = []

    # month labels
    last_month = None
    for i, w in enumerate(weeks):
        m = dt.date.fromisoformat(w[0][0]).strftime("%b")
        if m != last_month and i < len(weeks) - 2:
            out.append(f'<text class="lbl" x="{gx + i * (cell + gap)}" y="{gy - 8}">{m}</text>')
            last_month = m
    for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text class="lbl" x="{gx - 8}" y="{gy + r * (cell + gap) + 10}" text-anchor="end">{name}</text>')

    # heatmap: one animated group per week column (cheap: ~53 animations, run once)
    for i, w in enumerate(weeks):
        x = gx + i * (cell + gap)
        cells = []
        for d in w:
            wd = (dt.date.fromisoformat(d[0]).weekday() + 1) % 7  # Sunday = 0
            fill = "#8e1b1b" if d is peak and d[1] else COLORS[d[2]]
            cells.append(f'<rect x="{x}" y="{gy + wd * (cell + gap)}" width="{cell}" height="{cell}" rx="3" fill="{fill}">'
                         f'<title>{d[1]} contributions on {d[0]}</title></rect>')
        out.append(f'<g class="col" style="animation-delay:{0.3 + i * 0.03:.2f}s">{"".join(cells)}</g>')
    hm_w = len(weeks) * (cell + gap)

    # last 30 days area chart
    last = days[-30:]
    cx, cy, cw, ch = 60, 300, W - 120, 50
    mx = max(1, max(c for _, c, _ in last))
    pts = [(cx + k * cw / (len(last) - 1), cy + ch - c / mx * ch) for k, (_, c, _) in enumerate(last)]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{cx + cw} {cy + ch} L{cx} {cy + ch}Z"

    stats = [(f"{total:,}", "CONTRIBUTIONS"), (f"{cur} days", "CURRENT STREAK"),
             (f"{best} days", "LONGEST STREAK"), (str(peak[1]), f"FINEST DAY · {peak_label.upper()}")]
    stat_svg = "".join(
        f'<g class="st" style="animation-delay:{0.1 + k * 0.15:.2f}s"><text class="num" x="{60 + k * (W - 120) // 4}" y="92">{v}</text>'
        f'<text class="lbl" x="{60 + k * (W - 120) // 4}" y="112">{label}</text></g>' for k, (v, label) in enumerate(stats))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{total} contributions in the last year, longest streak {best} days">
<defs>
<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="#f3e9d2" stop-opacity="0"/><stop offset=".5" stop-color="#f3e9d2" stop-opacity=".5"/><stop offset="1" stop-color="#f3e9d2" stop-opacity="0"/></linearGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e1b1b" stop-opacity=".18"/><stop offset="1" stop-color="#8e1b1b" stop-opacity="0"/></linearGradient>
<linearGradient id="stroke" x1="0" x2="1"><stop offset="0" stop-color="#2a1f14"/><stop offset="1" stop-color="#2a1f14"/></linearGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch" seed="3"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .09 0"/></filter>
<filter id="blot" x="-50%" y="-50%" width="200%" height="200%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .4  0 0 0 0 .2  0 0 0 .18 -.04"/></filter>
<radialGradient id="age" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#f3e9d2" stop-opacity="0"/><stop offset="1" stop-color="#e3cfa6"/></radialGradient>
<clipPath id="hm"><rect x="{gx}" y="{gy}" width="{hm_w}" height="{7 * (cell + gap)}"/></clipPath>
<style>
text{{font-family:'EB Garamond','Cormorant Garamond',Garamond,Baskerville,'Times New Roman',Georgia,serif;fill:#2a1f14}}
.ttl{{font-size:28px;font-style:italic;fill:#2a1f14}}
.num{{font-size:32px;font-weight:600;fill:#2a1f14}}
.lbl{{font-size:12px;letter-spacing:2px;fill:#6b5232}}
.col{{animation:pop .8s ease-out both;transform-box:fill-box;transform-origin:center}}
@keyframes pop{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
.st{{animation:up .7s ease-out both}}
@keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.line{{stroke-dasharray:2000;stroke-dashoffset:2000;animation:draw 2.4s 1.6s ease-out forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.area{{animation:fade 1s 3s both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.scan{{animation:sweep 3s 3s ease-in-out 1 both;opacity:0}}
@keyframes sweep{{0%{{transform:translateX(-160px);opacity:1}}100%{{transform:translateX({hm_w + 160}px);opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important;stroke-dashoffset:0!important}}}}
</style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="6" fill="#f3e9d2" stroke="#bfa77a"/>
<rect width="{W}" height="{H}" rx="4" filter="url(#blot)"/><rect width="{W}" height="{H}" rx="4" fill="url(#age)"/><rect width="{W}" height="{H}" rx="4" filter="url(#grain)"/>
<text class="ttl" x="60" y="50">The Contribution Ledger</text>
<text class="lbl" x="{W - 60}" y="46" text-anchor="end">TWELVE MONTHS</text>
{stat_svg}
{"".join(out)}
<rect class="scan" clip-path="url(#hm)" x="{gx}" y="{gy}" width="160" height="{7 * (cell + gap)}" fill="url(#scan)"/>
<text class="lbl" x="60" y="{cy - 10}">THE LAST THIRTY DAYS</text>
<path class="area" d="{area}" fill="url(#area)"/>
<path class="line" d="{line}" fill="none" stroke="url(#stroke)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
<circle r="4" fill="#8e1b1b" opacity="0"><animate attributeName="opacity" values="0;1" begin="4s" dur=".3s" fill="freeze"/><animateMotion begin="4s" dur="10s" repeatCount="1" fill="freeze" path="{line}"/></circle>
</svg>'''


if __name__ == "__main__":
    if sys.argv[1] == "--sample":
        data = sample()
    else:
        data = fetch(sys.argv[1], os.environ["GITHUB_TOKEN"])
    os.makedirs(os.path.dirname(sys.argv[2]) or ".", exist_ok=True)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(render(data))
