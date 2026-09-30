#!/usr/bin/env python3
"""
Render data/contributions.json as a GitHub-style contribution graph with a
short reveal animation and a simple stats row.

    python scripts/render_heatmap_svg.py [data.json] [out.svg]
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import BG, FRAME, INK, MUTED, SANS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
IN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "heatmap.svg")

PAL = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]   # GitHub dark-mode greens
EMPTY_STROKE = "#1f242c"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

W = 1000
CELL, GAP = 13, 3
STEP = CELL + GAP

try:
    data = json.load(open(IN))
    days, st = data["days"], data["stats"]
except (OSError, ValueError, KeyError):
    today = datetime.date.today()
    days = [{"date": (today - datetime.timedelta(days=i)).isoformat(), "count": 0} for i in range(364, -1, -1)]
    st = {"total": 0, "current_streak": 0, "longest_streak": 0,
          "best_day": {"date": today.isoformat(), "count": 0}}

first = datetime.date.fromisoformat(days[0]["date"])
pad = (first.weekday() + 1) % 7                # weeks start on Sunday, like GitHub
cells = [None] * pad + days
NW = (len(cells) + 6) // 7

nz = sorted(d["count"] for d in days if d["count"] > 0)


def level(c):
    if c <= 0 or not nz:
        return 0
    q = [nz[int(len(nz) * f)] for f in (0.25, 0.5, 0.75)]
    return 1 + sum(c > t for t in q)


GW = NW * STEP - GAP
GX = (W - GW) // 2 + 14
GY = 92
GH = 7 * STEP - GAP
LY = GY + GH + 22
SY = LY + 44
H = SY + 82

best = st["best_day"]
o = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{st['total']} contributions in the last year">
  <style>
    .c {{ opacity: 0; animation: in .5s ease forwards; }}
    @keyframes in {{ to {{ opacity: 1; }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{FRAME}"/>
  <text x="{GX - 34}" y="46" font-family="{SANS}" font-size="18" font-weight="600" fill="{INK}">{st['total']:,} contributions in the last year</text>
  <g font-family="{SANS}" font-size="11" fill="{MUTED}">''']

labels, last_m = [], None
for wk in range(NW):
    d = next((c for c in cells[wk * 7: wk * 7 + 7] if c), None)
    if not d:
        continue
    m = int(d["date"][5:7])
    if m != last_m and wk < NW - 1:
        labels.append((wk, MONTHS[m - 1]))
        last_m = m
for j, (wk, name) in enumerate(labels):
    if j + 1 < len(labels) and labels[j + 1][0] - wk < 3:
        continue                                   # skip a squeezed partial month
    o.append(f'    <text x="{GX + wk * STEP}" y="{GY - 10}">{name}</text>')
for name, r in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
    o.append(f'    <text x="{GX - 34}" y="{GY + r * STEP + CELL - 3}">{name}</text>')
o.append('  </g>\n  <g>')

for i, d in enumerate(cells):
    if d is None:
        continue
    wk, row = divmod(i, 7)
    lv = level(d["count"])
    delay = 0.1 + wk * 0.018
    stroke = f' stroke="{EMPTY_STROKE}"' if lv == 0 else ""
    title = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} on {d["date"]}'
    o.append(f'    <rect class="c" x="{GX + wk * STEP}" y="{GY + row * STEP}" width="{CELL}" height="{CELL}" rx="2.5" '
             f'fill="{PAL[lv]}"{stroke} style="animation-delay:{delay:.2f}s"><title>{title}</title></rect>')
o.append('  </g>')

lx = GX + GW - 5 * (CELL + 4) - 36
o.append(f'  <g font-family="{SANS}" font-size="11" fill="{MUTED}">')
o.append(f'    <text x="{lx - 8}" y="{LY + 10}" text-anchor="end">Less</text>')
for i, c in enumerate(PAL):
    o.append(f'    <rect x="{lx + i * (CELL + 4)}" y="{LY}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}" stroke="{EMPTY_STROKE}"/>')
o.append(f'    <text x="{lx + 5 * (CELL + 4) + 4}" y="{LY + 10}">More</text>\n  </g>')

o.append(f'  <line x1="30" y1="{SY - 14}" x2="{W - 30}" y2="{SY - 14}" stroke="{FRAME}"/>')
stats = [
    (f'{st["total"]:,}', "Total contributions"),
    (f'{st["current_streak"]}', "Current streak (days)"),
    (f'{st["longest_streak"]}', "Longest streak (days)"),
    (f'{best["count"]}', "Best day · " + datetime.date.fromisoformat(best["date"]).strftime("%d %b %Y")),
]
cw = (W - 60) / 4
for i, (val, lab) in enumerate(stats):
    cx = 30 + cw * i + cw / 2
    o.append(f'  <text x="{cx:.1f}" y="{SY + 26}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="600" fill="{INK}">{val}</text>')
    o.append(f'  <text x="{cx:.1f}" y="{SY + 50}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTED}">{lab}</text>')
    if i:
        o.append(f'  <line x1="{30 + cw * i:.1f}" y1="{SY + 2}" x2="{30 + cw * i:.1f}" y2="{SY + 54}" stroke="{FRAME}"/>')
o.append('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT, f"{W}x{H}", os.path.getsize(OUT) // 1024, "KB")
