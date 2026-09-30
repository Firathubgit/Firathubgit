"""
Project cards (one SVG per card so each can be wrapped in its own link on
GitHub) + the footer strip.

    python scripts/make_cards_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL2, FRAME, INK, MUTED, CYAN, CYAN_DIM, AMBER, GREEN,  # noqa: E402
                   MONO, SANS, corners, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

CARDS = [
    dict(slug="card-copilot", idx="01", accent=CYAN, status="ACTIVE", status_c=GREEN,
         title="Android Automotive AI Copilot",
         lines=["Kotlin + Compose cockpit, maps, driving-mode rules and a",
                "local voice agent (Qwen3 via Ollama) on a Linux edge node."],
         tags=["Kotlin", "AAOS", "COVESA VSS", "KUKSA", "Blender"]),
    dict(slug="card-volturiano", idx="02", accent=AMBER, status="STUDIO", status_c=AMBER,
         title="Volturiano Studios",
         lines=["Own company. 3D car configurator in React + Three.js, a",
                "Unity WebGL steering-wheel builder, and client apps."],
         tags=["React", "Three.js", "Unity WebGL", "Android"]),
    dict(slug="card-terrahutton", idx="03", accent="#b58cff", status="SHIPPED", status_c=CYAN,
         title="Mining data → 3D / VR",
         lines=["At Terrahutton: drillholes, geophysics and magnetics",
                "turned into interactive 3D/VR scenes and dashboards."],
         tags=["Unity", "Python", "Supabase", "QGIS", "React"]),
    dict(slug="card-fighter", idx="04", accent="#ff5470", status="SHIPPED", status_c=CYAN,
         title="2.5D Fighting Game",
         lines=["Mortal Kombat-style brawler built over 8 months:",
                "selectable fighters, multiple stages, full combat loop."],
         tags=["Unity", "C#", "Game design", "Animation"]),
]

W, H = 490, 206


def card(c):
    chips = []
    x = 26
    for t in c["tags"]:
        w = 14 + len(t) * 7.0
        chips.append(f'<rect x="{x}" y="160" width="{w:.0f}" height="22" rx="11" fill="{PANEL2}" stroke="{FRAME}"/>'
                     f'<text x="{x + w / 2:.1f}" y="175" text-anchor="middle" fill="{INK}">{esc(t)}</text>')
        x += w + 7
    acc = c["accent"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c['title'])}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{acc}" stop-opacity=".13"/><stop offset=".5" stop-color="{PANEL}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sw" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{acc}" stop-opacity="0"/><stop offset=".5" stop-color="{acc}"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="{BG}"/>
    <rect width="{W}" height="{H}" fill="url(#g)"/>
    <rect x="0" y="0" width="4" height="{H}" fill="{acc}"/>
    <rect x="-160" y="0" width="160" height="2" fill="url(#sw)">
      <animate attributeName="x" values="-160;{W}" dur="3.2s" repeatCount="indefinite"/>
    </rect>
    <text x="{W - 22}" y="{H - 18}" text-anchor="end" font-family="{SANS}" font-size="84" font-weight="800" fill="{acc}" opacity=".07">{c['idx']}</text>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{FRAME}"/>
  <g font-family="{MONO}" font-size="11">
    <text x="26" y="36" fill="{acc}" letter-spacing="2">{c['idx']} <tspan fill="{FRAME}">/</tspan> <tspan fill="{MUTED}">PROJECT</tspan></text>
    <circle cx="{W - 94}" cy="32" r="3.5" fill="{c['status_c']}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="{W - 84}" y="36" fill="{c['status_c']}" letter-spacing="2">{c['status']}</text>
  </g>
  <text x="26" y="74" font-family="{SANS}" font-size="22" font-weight="700" fill="{INK}">{esc(c['title'])}</text>
  <g font-family="{SANS}" font-size="13.5" fill="{MUTED}">
    <text x="26" y="106">{esc(c['lines'][0])}</text>
    <text x="26" y="126">{esc(c['lines'][1])}</text>
  </g>
  <g font-family="{MONO}" font-size="11">{"".join(chips)}</g>
  {corners(8, 8, W - 16, H - 16, arm=10, color=acc, width=1.5, opacity=.55)}
</svg>'''


def footer():
    FW, FH = 1000, 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{FW}" height="{FH}" viewBox="0 0 {FW} {FH}" role="img" aria-label="Thanks for visiting">
  <defs>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="road" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".25"/>
    </linearGradient>
    <clipPath id="c"><rect x="1" y="1" width="{FW - 2}" height="{FH - 2}" rx="12"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{FW}" height="{FH}" fill="{BG}"/>
    <path d="M300,{FH} L490,40 L510,40 L700,{FH} Z" fill="url(#road)"/>
    <line x1="330" y1="{FH}" x2="494" y2="40" stroke="{CYAN_DIM}"/>
    <line x1="670" y1="{FH}" x2="506" y2="40" stroke="{CYAN_DIM}"/>
    <line x1="500" y1="{FH}" x2="500" y2="40" stroke="{CYAN}" stroke-width="2.5" stroke-dasharray="10 14" opacity=".8">
      <animate attributeName="stroke-dashoffset" from="0" to="48" dur=".6s" repeatCount="indefinite"/>
    </line>
    <rect x="0" y="40" width="{FW}" height="1" fill="url(#fade)"/>
    <circle cx="500" cy="40" r="3" fill="{AMBER}"><animate attributeName="r" values="2;5;2" dur="2s" repeatCount="indefinite"/></circle>
  </g>
  <rect x="0.5" y="0.5" width="{FW - 1}" height="{FH - 1}" rx="12" fill="none" stroke="{FRAME}"/>
  <g font-family="{MONO}" font-size="12" letter-spacing="2">
    <text x="40" y="76" fill="{MUTED}">END OF ROUTE</text>
    <text x="40" y="96" fill="{INK}">thanks for driving by</text>
    <text x="{FW - 40}" y="76" text-anchor="end" fill="{MUTED}">NEXT STOP</text>
    <text x="{FW - 40}" y="96" text-anchor="end" fill="{CYAN}">let's build something ▸</text>
  </g>
</svg>'''


for c in CARDS:
    p = os.path.join(ASSETS, c["slug"] + ".svg")
    open(p, "w", encoding="utf-8").write(card(c))
    print("wrote", p)
p = os.path.join(ASSETS, "footer.svg")
open(p, "w", encoding="utf-8").write(footer())
print("wrote", p)
