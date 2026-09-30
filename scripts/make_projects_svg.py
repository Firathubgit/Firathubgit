"""
Project cards, one full-width SVG per project (so each can link to its repo):
title, status, short description, four screenshots, tech line. Set in Inter.

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
         role="Software Developer · Android Automotive / AI", status=("Active", GREEN),
         text="AI-driven infotainment system for Android Automotive OS in Kotlin and Jetpack Compose. "
              "MapLibre navigation, a vehicle UI and a local voice assistant with Ollama/Qwen3, "
              "with vehicle data through COVESA VSS and the AAOS VHAL.",
         tags=["Kotlin", "Jetpack Compose", "Android Automotive OS", "AAOS VHAL", "COVESA VSS",
               "MapLibre", "Ollama/Qwen3", "Python"]),
    dict(slug="volturiano", title="Volturiano AI Website Builder",
         role="Fullstack Developer · AI agent system", status=("In development", AMBER),
         text="Agent-based website builder that generates and modifies React/Vite apps from "
              "natural-language instructions. Tool calling, isolated code execution in E2B sandboxes, "
              "real-time preview, Supabase, and publishing through GitHub and Vercel.",
         tags=["TypeScript", "React", "Node.js", "Supabase", "E2B", "GitHub", "Vercel", "AI agents"]),
    dict(slug="wacky-warriors", title="Wacky Warriors",
         role="Game Developer · Diploma project", status=("Shipped", "#6e7681"),
         text="2.5D fighting and arena game in Unity and C#, built over more than a year. Local "
              "multiplayer, character controllers, combat with hitboxes, health, animations and camera "
              "effects, plus multiple characters and stages.",
         tags=["Unity", "C#", "Unity Input System", "Cinemachine", "Local multiplayer", "Git"]),
]

W = 1000
PAD = 32
GAP = 12
TW = (W - 2 * PAD - 3 * GAP) / 4
TH = TW * 9 / 16


def card(p):
    y = 54
    o = [f'<text x="{PAD}" y="{y}" font-size="24" font-weight="700" fill="{INK}">{esc(p["title"])}</text>']
    label, col = p["status"]
    lx = W - PAD - text_width(label, 14) * 1.02
    o.append(f'<circle cx="{lx - 11:.1f}" cy="{y - 7}" r="4.5" fill="{col}"/>'
             f'<text x="{W - PAD}" y="{y - 2}" text-anchor="end" font-size="14" fill="{MUTED}">{label}</text>')
    y += 26
    o.append(f'<text x="{PAD}" y="{y}" font-size="14.5" fill="{MUTED}">{esc(p["role"])}</text>')
    y += 34
    for line in wrap(p["text"], 16, W - 2 * PAD - 20):
        o.append(f'<text x="{PAD}" y="{y}" font-size="16" fill="{INK}">{esc(line)}</text>')
        y += 25
    y += 8
    o.append("<defs>")
    for i in range(4):
        x = PAD + i * (TW + GAP)
        o.append(f'<clipPath id="t{i}"><rect x="{x:.1f}" y="{y:.1f}" width="{TW:.1f}" height="{TH:.1f}" rx="8"/></clipPath>')
    o.append("</defs>")
    for i in range(4):
        x = PAD + i * (TW + GAP)
        uri = data_uri(os.path.join(ASSETS, "projects", f'{p["slug"]}-{i + 1}.jpg'), "image/jpeg")
        o.append(f'<image x="{x:.1f}" y="{y:.1f}" width="{TW:.1f}" height="{TH:.1f}" clip-path="url(#t{i})" '
                 f'preserveAspectRatio="xMidYMid slice" href="{uri}"/>'
                 f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{TW - 1:.1f}" height="{TH - 1:.1f}" rx="8" fill="none" stroke="{FRAME}"/>')
    y += TH + 30
    o.append(f'<text x="{PAD}" y="{y:.1f}" font-size="14" fill="{MUTED}">{esc("  ·  ".join(p["tags"]))}</text>')
    H = int(y + 26)
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
