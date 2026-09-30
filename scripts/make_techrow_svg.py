"""
CV-style tech line: small logo + name, centred, wrapping onto a second row
when needed. Transparent background, with a light-theme variant.

    python scripts/make_techrow_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import INK, INTER, inter_css, text_width, data_uri, esc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
TECH = os.path.join(ASSETS, "tech")

# Kotlin's own mark, drawn as a vector (the CV raster is cropped)
KOTLIN = ('<defs><linearGradient id="kt" x1="1" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#E44857"/><stop offset=".47" stop-color="#C711E1"/>'
          '<stop offset="1" stop-color="#7F52FF"/></linearGradient></defs>'
          '<path d="M24 24H0V0h24L12 12Z" fill="url(#kt)"/>')

ROWS = {
    "featured": [
        ("kotlin", "Kotlin"),
        ("jetpack-compose", "Jetpack Compose"),
        ("android-automotive", "Android Automotive OS"),
        ("aaos-vhal", "AAOS VHAL"),
        ("covesa-vss", "COVESA VSS"),
        ("maplibre", "MapLibre"),
        ("ollama", "Ollama / Qwen3"),
        ("python", "Python"),
    ],
}

W = 1000
ICON = 22
GAP_I = 8          # icon -> label
GAP = 26           # between items
ROW_H = 38
SIZE = 15.5


def icon(slug, x, y):
    if slug == "kotlin":
        s = ICON / 24 * 0.86
        o = ICON * 0.07
        return f'<g transform="translate({x + o:.1f},{y + o:.1f}) scale({s:.4f})">{KOTLIN}</g>'
    uri = data_uri(os.path.join(TECH, f"{slug}.png"), "image/png")
    return f'<image x="{x:.1f}" y="{y:.1f}" width="{ICON}" height="{ICON}" href="{uri}"/>'


def build(items, ink):
    widths = [ICON + GAP_I + text_width(lbl, SIZE, 600) * 1.02 for _, lbl in items]
    rows, cur, cw = [], [], 0
    for it, w in zip(items, widths):
        add = w + (GAP if cur else 0)
        if cur and cw + add > W - 40:
            rows.append((cur, cw)); cur, cw = [], 0
            add = w
        cur.append((it, w)); cw += add
    rows.append((cur, cw))
    H = len(rows) * ROW_H + 8
    o = []
    for r, (row, rw) in enumerate(rows):
        x = (W - rw) / 2
        cy = 4 + r * ROW_H + ROW_H / 2
        for (slug, lbl), w in row:
            o.append(icon(slug, x, cy - ICON / 2))
            o.append(f'<text x="{x + ICON + GAP_I:.1f}" y="{cy + 5.5:.1f}" font-size="{SIZE}" font-weight="600" fill="{ink}">{esc(lbl)}</text>')
            x += w + GAP
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(", ".join(l for _, l in items))}">
  <style>
    {inter_css((600,))}
  </style>
  <g font-family="{INTER}">
    {chr(10).join("    " + s for s in o).strip()}
  </g>
</svg>'''


if __name__ == "__main__":
    for name, items in ROWS.items():
        for suffix, ink in (("", INK), ("-light", "#1f2328")):
            out = os.path.join(ASSETS, f"tech-{name}{suffix}.svg")
            with open(out, "w", encoding="utf-8") as f:
                f.write(build(items, ink))
            print("wrote", out)
