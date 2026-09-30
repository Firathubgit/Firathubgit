"""
Project cards (one SVG per card so each can be wrapped in its own link on
GitHub).

    python scripts/make_cards_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, PANEL2, FRAME, INK, MUTED, BLUE, AMBER, GREEN, RED, PURPLE,  # noqa: E402
                   MONO, SANS, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

CARDS = [
    dict(slug="card-copilot", idx="01", accent=BLUE, status="ACTIVE", status_c=GREEN,
         title="Android Automotive AI Copilot",
         lines=["Kotlin + Compose cockpit, maps, driving-mode rules and a",
                "local voice agent (Qwen3 via Ollama) on a Linux edge node."],
         tags=["Kotlin", "AAOS", "COVESA VSS", "KUKSA", "Blender"]),
    dict(slug="card-volturiano", idx="02", accent=AMBER, status="STUDIO", status_c=AMBER,
         title="Volturiano Studios",
         lines=["Own company. 3D car configurator in React + Three.js, a",
                "Unity WebGL steering-wheel builder, and client apps."],
         tags=["React", "Three.js", "Unity WebGL", "Android"]),
    dict(slug="card-terrahutton", idx="03", accent=PURPLE, status="SHIPPED", status_c="#6e7681",
         title="Mining data → 3D / VR",
         lines=["At Terrahutton: drillholes, geophysics and magnetics",
                "turned into interactive 3D/VR scenes and dashboards."],
         tags=["Unity", "Python", "Supabase", "QGIS", "React"]),
    dict(slug="card-fighter", idx="04", accent=RED, status="SHIPPED", status_c="#6e7681",
         title="2.5D Fighting Game",
         lines=["Mortal Kombat-style brawler built over 8 months:",
                "selectable fighters, multiple stages, full combat loop."],
         tags=["Unity", "C#", "Game design", "Animation"]),
]

W, H = 490, 178


def card(c):
    tags = "  ·  ".join(c["tags"])
    status = c["status"].title()
    sw = 12 + len(status) * 7.2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c['title'])}">
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{PANEL}" stroke="{FRAME}"/>
  <g font-family="{SANS}">
    <text x="26" y="48" font-size="21" font-weight="600" fill="{INK}">{esc(c['title'])}</text>
    <circle cx="{W - 26 - sw}" cy="42" r="4" fill="{c['status_c']}"/>
    <text x="{W - 26}" y="47" text-anchor="end" font-size="13" fill="{MUTED}">{status}</text>
    <text x="26" y="84" font-size="14" fill="{MUTED}">{esc(c['lines'][0])}</text>
    <text x="26" y="105" font-size="14" fill="{MUTED}">{esc(c['lines'][1])}</text>
    <line x1="26" y1="128" x2="{W - 26}" y2="128" stroke="{FRAME}"/>
    <text x="26" y="154" font-size="13" fill="{INK}">{esc(tags)}</text>
  </g>
</svg>'''


for c in CARDS:
    p = os.path.join(ASSETS, c["slug"] + ".svg")
    open(p, "w", encoding="utf-8").write(card(c))
    print("wrote", p)
