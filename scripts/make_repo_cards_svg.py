"""
Project cards drawn like GitHub's own pinned-repository cards: repo icon,
blue repo name, visibility pill, short description, language dot. Dark and
light variants so they match either GitHub theme.

    python scripts/make_repo_cards_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import esc, INTER, inter_css, text_width, wrap  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# Inter is embedded so the layout (pill position, line wraps) is exact everywhere
FONT = INTER

THEMES = {
    "": dict(bg="#0d1117", border="#3d444d", name="#4493f8", text="#9198a1", pill="#3d444d"),
    "-light": dict(bg="#ffffff", border="#d1d9e0", name="#0969da", text="#59636e", pill="#d1d9e0"),
}

REPOS = [
    dict(slug="copilot", name="android-automotive-ai-copliot-infotainment", vis="Public",
         desc=["AI-driven infotainment for Android Automotive OS in Kotlin and",
               "Jetpack Compose, with MapLibre navigation and a local",
               "Ollama/Qwen3 voice assistant."],
         lang=("Kotlin", "#A97BFF")),
    dict(slug="volturiano", name="volturiano", vis="Private",
         desc=["Agent-based website builder that generates and edits React/Vite",
               "apps from natural language, with E2B sandboxes and publishing",
               "through GitHub and Vercel."],
         lang=("TypeScript", "#3178c6")),
    dict(slug="wacky-warriors", name="FiratsGymnasieArbete", vis="Public",
         desc=["Wacky Warriors: a 2.5D fighting and arena game in Unity and C#",
               "with local multiplayer, multiple characters and stages.",
               "Diploma project."],
         lang=("C#", "#178600")),
    dict(slug="formula-driverless", name="Formula-Driverless-Path-Predictor", vis="Public",
         desc=["A C++20 and Qt 6 racing simulator that shows why a driverless car brakes,",
               "accelerates or changes line. Real tire physics, a minimum-curvature racing",
               "line and MPCC, all backed by tests."],
         lang=("C++", "#f34b7d")),
]

W, H = 480, 150
# GitHub's octicon "repo" (16px)
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z")


def text_len(s, size, bold=False):
    return text_width(s, size, 600 if bold else 400)


def card(r, t):
    nx = 16 + 16 + 8
    px = nx + text_len(r["name"], 14, True) + 8
    pw = text_len(r["vis"], 12) + 16
    lines = "\n    ".join(
        f'<text x="16" y="{64 + i * 19}" font-size="12.5" fill="{t["text"]}">{esc(l)}</text>'
        for i, l in enumerate(wrap(" ".join(r["desc"]), 12.5, W - 36)[:3]))
    lang, col = r["lang"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(r['name'])}">
  <style>
    {inter_css((400, 600))}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{t['bg']}" stroke="{t['border']}"/>
  <g font-family="{FONT}">
    <path transform="translate(16,20)" fill="{t['text']}" d="{REPO_ICON}"/>
    <text x="{nx}" y="33" font-size="14" font-weight="600" fill="{t['name']}">{esc(r['name'])}</text>
    <rect x="{px:.1f}" y="19.5" width="{pw:.1f}" height="19" rx="9.5" fill="none" stroke="{t['pill']}"/>
    <text x="{px + pw / 2:.1f}" y="33" font-size="12" text-anchor="middle" fill="{t['text']}">{r['vis']}</text>
    {lines}
    <circle cx="22" cy="{H - 22}" r="6" fill="{col}"/>
    <text x="34" y="{H - 18}" font-size="12" fill="{t['text']}">{esc(lang)}</text>
  </g>
</svg>'''


if __name__ == "__main__":
    for r in REPOS:
        for suffix, t in THEMES.items():
            out = os.path.join(ASSETS, f'repo-{r["slug"]}{suffix}.svg')
            with open(out, "w", encoding="utf-8") as f:
                f.write(card(r, t))
            print("wrote", out)
