"""
neofetch-style info card that sits beside the ASCII portrait.

Lines print in one by one; the degree-progress bar is computed from today's
date, so the daily workflow keeps it current.

    python scripts/make_info_svg.py [out.svg]
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL2, FRAME, INK, MUTED, CYAN, CYAN_DIM, AMBER, GREEN, RED,  # noqa: E402
                   MONO, corners, titlebar, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "info-card.svg")

W, H = 602, 734          # same box as portrait.svg so the two read as a pair
TB = 30

ROWS = [
    ("Role", "Game Developer Intern @ Realdini"),
    ("Company", "Founder · Volturiano Studios"),
    ("Study", "Computer Engineering · Datateknik 180 hp"),
    ("Uni", "University West · Högskolan Väst"),
    ("Previous", "Fullstack & 3D data viz @ Terrahutton"),
    ("Focus", "Android Automotive · SDV · AI copilots"),
    ("Code", "Kotlin · C# · C++ · Python · TS/JS · x86"),
    ("3D / UI", "Unity · Three.js · React · Blender · Figma"),
    ("Data", "Supabase · QGIS · Ollama · Node.js"),
    ("Uptime", "5+ years shipping code"),
    ("Langs", "Svenska · English"),
    ("Web", "firatportfolio.com"),
]

START = datetime.date(2024, 9, 1)
END = datetime.date(2027, 6, 15)
today = datetime.date.today()
pct = max(0.0, min(1.0, (today - START).days / (END - START).days))

X = 34
Y0 = TB + 50
LH = 31
STEP = 0.16       # seconds between printed lines
T0 = 0.4

o = []
o.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Firat Kaya — role, studies, stack">
  <defs>
    <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN_DIM}"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#0e1926" stroke-width="1"/>
    </pattern>
  </defs>
  <style>
    .ln {{ opacity: 0; animation: pr .35s steps(4, end) forwards; }}
    @keyframes pr {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: translateX(0); }} }}
    .fill {{ transform-box: fill-box; transform-origin: left center; transform: scaleX(0); animation: grow 1.4s cubic-bezier(.5,0,.2,1) forwards; }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    .blink {{ animation: bl 1s steps(1) infinite; }}
    @keyframes bl {{ 50% {{ opacity: 0; }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{FRAME}"/>
  <rect x="1" y="{TB + 1}" width="{W - 2}" height="{H - TB - 2}" fill="url(#grid)" opacity=".7"/>
  {titlebar(W, "firat@goteborg: ~ $ fastfetch", "zsh")}
  <g font-family="{MONO}" font-size="15">''')

t = T0
o.append(f'    <text x="{X}" y="{Y0}" class="ln" style="animation-delay:{t:.2f}s"><tspan fill="{CYAN}" font-weight="700">firat</tspan><tspan fill="{MUTED}">@</tspan><tspan fill="{CYAN}" font-weight="700">goteborg</tspan></text>')
t += STEP
o.append(f'    <text x="{X}" y="{Y0 + 18}" fill="{FRAME}" class="ln" style="animation-delay:{t:.2f}s">{"─" * 46}</text>')
y = Y0 + 18
for k, v in ROWS:
    t += STEP
    y += LH
    o.append(
        f'    <text x="{X}" y="{y}" class="ln" style="animation-delay:{t:.2f}s">'
        f'<tspan fill="{AMBER}">{esc(k)}</tspan><tspan x="{X + 104}" fill="{INK}">{esc(v)}</tspan></text>'
    )

# degree progress
t += STEP * 2
y += 44
BW = W - 2 * X
o.append(f'''    <g class="ln" style="animation-delay:{t:.2f}s">
      <text x="{X}" y="{y}" fill="{MUTED}" font-size="12">DEGREE PROGRESS <tspan fill="{FRAME}">·</tspan> SEP 2024 → JUN 2027</text>
      <text x="{W - X}" y="{y}" fill="{CYAN}" font-size="12" text-anchor="end">{pct * 100:.0f}%</text>
      <rect x="{X}" y="{y + 10}" width="{BW}" height="10" rx="5" fill="{PANEL2}" stroke="{FRAME}"/>
      <rect x="{X}" y="{y + 10}" width="{BW * pct:.1f}" height="10" rx="5" fill="url(#bar)" class="fill" style="animation-delay:{t + .2:.2f}s"/>''')
for q in range(1, 6):
    xq = X + BW * q / 6
    o.append(f'      <line x1="{xq:.1f}" y1="{y + 10}" x2="{xq:.1f}" y2="{y + 20}" stroke="{BG}" stroke-width="2"/>')
o.append('    </g>')

# now building
t += STEP * 2
y += 58
o.append(f'''    <g class="ln" style="animation-delay:{t:.2f}s">
      <rect x="{X}" y="{y - 20}" width="{BW}" height="62" rx="8" fill="{PANEL}" stroke="{FRAME}"/>
      <circle cx="{X + 18}" cy="{y - 1}" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>
      <text x="{X + 32}" y="{y + 3}" fill="{GREEN}" font-size="12" letter-spacing="1">NOW BUILDING</text>
      <text x="{X + 18}" y="{y + 27}" fill="{INK}" font-size="13">Android Automotive AI Copilot <tspan fill="{MUTED}">· Kotlin · VSS · Ollama</tspan></text>
    </g>''')

# prompt + palette
t += STEP * 2
y += 76
o.append(f'    <text x="{X}" y="{y}" class="ln" style="animation-delay:{t:.2f}s"><tspan fill="{GREEN}">❯</tspan><tspan fill="{INK}"> </tspan><tspan class="blink" fill="{CYAN}">█</tspan></text>')
t += STEP
sw = [BG, RED, GREEN, AMBER, CYAN_DIM, "#b58cff", CYAN, INK]
for i, c in enumerate(sw):
    o.append(f'    <rect x="{X + i * 28}" y="{H - 44}" width="24" height="14" rx="2" fill="{c}" stroke="{FRAME}" class="ln" style="animation-delay:{t + i * 0.05:.2f}s"/>')
o.append(f'''  </g>
  {corners(12, TB + 12, W - 24, H - TB - 24, arm=14, opacity=.5)}
</svg>''')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT, f"progress {pct:.0%}", os.path.getsize(OUT) // 1024, "KB")
