"""
Project cards, one full-width SVG per project (so each can link to its repo):
one screenshot beside title, status, short description and tech line. Set in Inter.

    python scripts/make_projects_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (PANEL, FRAME, INK, MUTED, GREEN, AMBER, INTER,  # noqa: E402
                   inter_css, wrap, text_width, data_uri, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

PROJECTS = [
    dict(slug="copilot", title="Android Automotive AI Infotainment",
         role="Android Automotive / AI", status=("Active", GREEN),
         text="AI-driven infotainment system for Android Automotive OS in Kotlin and Jetpack Compose. "
              "MapLibre navigation, a vehicle UI and a local voice assistant with Ollama/Qwen3, "
              "with vehicle data through COVESA VSS and the AAOS VHAL.",
         tags=["Kotlin", "Jetpack Compose", "Android Automotive OS", "AAOS VHAL", "COVESA VSS",
               "MapLibre", "Ollama/Qwen3", "Python"]),
    dict(slug="volturiano", title="Volturiano AI Website Builder",
         role="AI agent system", status=("In development", AMBER),
         text="Agent-based website builder that generates and modifies React/Vite apps from "
              "natural-language instructions. Tool calling, isolated code execution in E2B sandboxes, "
              "real-time preview, Supabase, and publishing through GitHub and Vercel.",
         tags=["TypeScript", "React", "Node.js", "Supabase", "E2B", "GitHub", "Vercel", "AI agents"]),
    dict(slug="wacky-warriors", title="Wacky Warriors",
         role="Diploma project", status=("Shipped", "#6e7681"),
         text="2.5D fighting and arena game in Unity and C#, built over more than a year. Local "
              "multiplayer, character controllers, combat with hitboxes, health, animations and camera "
              "effects, plus multiple characters and stages.",
         tags=["Unity", "C#", "Unity Input System", "Cinemachine", "Local multiplayer", "Git"]),
]

W = 1000
PAD = 28
IW = 400                       # screenshot width
IH = IW * 9 / 16
TX = PAD + IW + 32             # text column
TWID = W - TX - PAD


def card(p):
    o = []
    uri = data_uri(os.path.join(ASSETS, "projects", f'{p["slug"]}.jpg'), "image/jpeg")
    o.append(f'<defs><clipPath id="shot"><rect x="{PAD}" y="{PAD}" width="{IW}" height="{IH:.1f}" rx="10"/></clipPath></defs>')
    o.append(f'<image x="{PAD}" y="{PAD}" width="{IW}" height="{IH:.1f}" clip-path="url(#shot)" '
             f'preserveAspectRatio="xMidYMid slice" href="{uri}"/>'
             f'<rect x="{PAD + .5}" y="{PAD + .5}" width="{IW - 1}" height="{IH - 1:.1f}" rx="10" fill="none" stroke="{FRAME}"/>')

    y = PAD + 22
    o.append(f'<text x="{TX}" y="{y}" font-size="22" font-weight="700" fill="{INK}">{esc(p["title"])}</text>')
    y += 26
    label, col = p["status"]
    o.append(f'<circle cx="{TX + 4.5}" cy="{y - 5}" r="4.5" fill="{col}"/>'
             f'<text x="{TX + 16}" y="{y}" font-size="14" fill="{MUTED}">{label}  ·  {esc(p["role"])}</text>')
    y += 32
    for line in wrap(p["text"], 15, TWID):
        o.append(f'<text x="{TX}" y="{y}" font-size="15" fill="{INK}">{esc(line)}</text>')
        y += 23
    y += 12
    lines, cur = [], []
    for t in p["tags"]:                       # wrap between tags, never inside one
        if cur and text_width("  ·  ".join(cur + [t]), 13.5) > TWID:
            lines.append("  ·  ".join(cur)); cur = []
        cur.append(t)
    lines.append("  ·  ".join(cur))
    for line in lines:
        o.append(f'<text x="{TX}" y="{y}" font-size="13.5" fill="{MUTED}" style="white-space:pre">{esc(line)}</text>')
        y += 21
    H = int(max(PAD * 2 + IH, y + PAD - 12))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p['title'])}">
  <style>
    {inter_css((400, 700))}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{FRAME}"/>
  <g font-family="{INTER}">
    {chr(10).join("    " + s for s in o).strip()}
  </g>
</svg>'''


for p in PROJECTS:
    out = os.path.join(ASSETS, f'project-{p["slug"]}.svg')
    with open(out, "w", encoding="utf-8") as f:
        f.write(card(p))
    print("wrote", out, os.path.getsize(out) // 1024, "KB")
