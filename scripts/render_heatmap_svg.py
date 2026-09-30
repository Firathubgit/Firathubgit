#!/usr/bin/env python3
"""
Render data/contributions.json as an animated HUD contribution heatmap.

- cells pop in on a diagonal sweep (CSS, plays once then holds)
- a radar-style scan bar keeps sliding across the year (SMIL loop)
- best day gets a pulsing amber ring, today blinks
- stats row: total, current streak, longest streak, best day

    python scripts/render_heatmap_svg.py [data.json] [out.svg]
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL2, FRAME, INK, MUTED, CYAN, CYAN_DIM, AMBER, GREEN,  # noqa: E402
                   MONO, SANS, corners, titlebar, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
IN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "heatmap.svg")

PAL = ["#101a25", "#0a3b4b", "#0d6a84", "#1ba6c6", "#37e1ff"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

W = 1000
CELL, GAP = 13, 3
STEP = CELL + GAP
TB = 30

try:
    data = json.load(open(IN))
    days, st = data["days"], data["stats"]
except (OSError, ValueError, KeyError):
    today = datetime.date.today()
    days = [{"date": (today - datetime.timedelta(days=i)).isoformat(), "count": 0} for i in range(364, -1, -1)]
    st = {"total": 0, "current_streak": 0, "longest_streak": 0, "active_days": 0,
          "best_day": {"date": today.isoformat(), "count": 0}}

# align to weeks starting Sunday, like GitHub
first = datetime.date.fromisoformat(days[0]["date"])
pad = (first.weekday() + 1) % 7                # Sunday -> 0
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
GY = TB + 58
GH = 7 * STEP - GAP
H = GY + GH + 40 + 96 + 24

today_s = datetime.date.today().isoformat()
best = st["best_day"]

o = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution heatmap for the last year: {st['total']} contributions">
  <defs>
    <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".8" stop-color="{CYAN}" stop-opacity=".10"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#0e1926" stroke-width="1"/>
    </pattern>
    <clipPath id="gclip"><rect x="{GX - 4}" y="{GY - 4}" width="{GW + 8}" height="{GH + 8}"/></clipPath>
  </defs>
  <style>
    .c {{ opacity: 0; transform-box: fill-box; transform-origin: center; transform: scale(.2); animation: pop .45s cubic-bezier(.3,1.6,.5,1) forwards; }}
    @keyframes pop {{ to {{ opacity: 1; transform: scale(1); }} }}
    .up {{ opacity: 0; animation: up .6s ease forwards; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{FRAME}"/>
  <rect x="1" y="{TB + 1}" width="{W - 2}" height="{H - TB - 2}" fill="url(#grid)" opacity=".6"/>
  {titlebar(W, "telemetry://contributions — last 12 months", "updated " + today_s)}
  <g font-family="{MONO}" font-size="10" fill="{MUTED}">''']

last_m = None
labels = []
for wk in range(NW):
    d = cells[wk * 7] if wk * 7 < len(cells) and cells[wk * 7] else None
    if d is None:
        d = next((c for c in cells[wk * 7: wk * 7 + 7] if c), None)
    if not d:
        continue
    m = int(d["date"][5:7])
    if m != last_m and wk < NW - 1:
        labels.append((wk, MONTHS[m - 1]))
        last_m = m
# drop a label that would collide with the next one (e.g. a partial first month)
for j, (wk, name) in enumerate(labels):
    if j + 1 < len(labels) and labels[j + 1][0] - wk < 3:
        continue
    o.append(f'    <text x="{GX + wk * STEP}" y="{GY - 10}">{name}</text>')
for name, r in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
    o.append(f'    <text x="{GX - 34}" y="{GY + r * STEP + CELL - 3}">{name}</text>')
o.append('  </g>\n  <g>')

REVEAL = 2.2
maxo = (NW - 1) + 6 * 1.4
for i, d in enumerate(cells):
    if d is None:
        continue
    wk, row = divmod(i, 7)
    x, y = GX + wk * STEP, GY + row * STEP
    lv = level(d["count"])
    delay = 0.3 + (wk + row * 1.4) / maxo * REVEAL
    title = f'{d["count"]} contribution{"s" if d["count"] != 1 else ""} on {d["date"]}'
    o.append(f'    <rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{PAL[lv]}" '
             f'style="animation-delay:{delay:.2f}s"><title>{title}</title></rect>')
    if d["date"] == best["date"] and best["count"] > 0:
        o.append(f'    <rect x="{x - 2.5}" y="{y - 2.5}" width="{CELL + 5}" height="{CELL + 5}" rx="4.5" fill="none" stroke="{AMBER}" stroke-width="1.5">'
                 f'<animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/></rect>')
    if d["date"] == today_s:
        o.append(f'    <rect x="{x - 2}" y="{y - 2}" width="{CELL + 4}" height="{CELL + 4}" rx="4" fill="none" stroke="{CYAN}" stroke-width="1.2">'
                 f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect>')

END = 0.3 + REVEAL + 0.5
o.append(f'''  </g>
  <g clip-path="url(#gclip)">
    <rect x="{GX - 120}" y="{GY - 4}" width="120" height="{GH + 8}" fill="url(#scan)" opacity="0">
      <animate attributeName="opacity" to="1" begin="{END:.1f}s" dur=".01s" fill="freeze"/>
      <animate attributeName="x" values="{GX - 120};{GX + GW + 8}" begin="{END:.1f}s" dur="6s" repeatCount="indefinite"/>
    </rect>
  </g>''')

# legend
ly = GY + GH + 24
lx = GX + GW - 5 * (CELL + 4) - 70
o.append(f'  <g font-family="{MONO}" font-size="10" fill="{MUTED}">')
o.append(f'    <text x="{GX}" y="{ly + 10}">{st.get("active_days", 0)} active days · <tspan fill="{AMBER}">◻</tspan> best day · <tspan fill="{CYAN}">◻</tspan> today</text>')
o.append(f'    <text x="{lx - 8}" y="{ly + 10}" text-anchor="end">less</text>')
for i, c in enumerate(PAL):
    o.append(f'    <rect x="{lx + i * (CELL + 4)}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
o.append(f'    <text x="{lx + 5 * (CELL + 4) + 4}" y="{ly + 10}">more</text>\n  </g>')

# stats tiles
ty = ly + 36
tiles = [
    ("CONTRIBUTIONS", f'{st["total"]:,}', "last 12 months", CYAN),
    ("CURRENT STREAK", f'{st["current_streak"]}', "days in a row", GREEN),
    ("LONGEST STREAK", f'{st["longest_streak"]}', "days", INK),
    ("BEST DAY", f'{best["count"]}', datetime.date.fromisoformat(best["date"]).strftime("%d %b %Y"), AMBER),
]
TW = (W - 2 * 40 - 3 * 16) / 4
for i, (lab, val, sub, col) in enumerate(tiles):
    x = 40 + i * (TW + 16)
    o.append(f'''  <g class="up" style="animation-delay:{END - 0.3 + i * 0.12:.2f}s">
    <rect x="{x:.1f}" y="{ty}" width="{TW:.1f}" height="76" rx="8" fill="{PANEL}" stroke="{FRAME}"/>
    <rect x="{x:.1f}" y="{ty + 14}" width="3" height="48" fill="{col}"/>
    <text x="{x + 18:.1f}" y="{ty + 24}" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="2">{lab}</text>
    <text x="{x + 18:.1f}" y="{ty + 54}" font-family="{SANS}" font-size="26" font-weight="700" fill="{col}">{esc(val)}</text>
    <text x="{x + TW - 14:.1f}" y="{ty + 54}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}">{esc(sub)}</text>
  </g>''')

o.append(f'  {corners(10, TB + 10, W - 20, H - TB - 20, arm=14, opacity=.5)}\n</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT, f"{W}x{H}", os.path.getsize(OUT) // 1024, "KB")
