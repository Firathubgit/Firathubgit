"""
Header: ASCII portrait, name, current roles with logos. Static, set in Inter
(same as the CV).

    python scripts/make_header_svg.py [out.svg]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (PANEL, FRAME, INK, MUTED, INTER, MONO,  # noqa: E402
                   inter_css, text_width, data_uri)
from ascii_portrait import ascii_portrait  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ASSETS, "header.svg")

W = 1000
PX, PY = 44, 26
art, AW, AH = ascii_portrait(PX, PY, font_family=MONO)
H = int(AH + 2 * PY)
TX = int(PX + AW + 52)
CY = H // 2

LOGO_H = 20
LOGOS = {
    "uw": (os.path.join(ASSETS, "logos", "university-west.png"), 226 / 96),
    "realdini": (os.path.join(ASSETS, "logos", "realdini.png"), 119 / 96),
}


def role_line(y, lead, logo, name, size=18):
    """'<lead> [logo] <name>' on one baseline, logo sized to the cap height."""
    path, ratio = LOGOS[logo]
    lw = LOGO_H * ratio
    x1 = TX + text_width(lead, size) * 1.02 + 9
    x2 = x1 + lw + 8
    return (f'<text x="{TX}" y="{y}" font-size="{size}" fill="{MUTED}">{lead}</text>'
            f'<image x="{x1:.1f}" y="{y - LOGO_H + 3.5:.1f}" width="{lw:.1f}" height="{LOGO_H}" href="{data_uri(path, "image/png")}"/>'
            f'<text x="{x2:.1f}" y="{y}" font-size="{size}" font-weight="600" fill="{INK}">{name}</text>')


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Firat Kaya — Computer Engineering student at University West, Game Developer Intern at Realdini Studios. Göteborg, Sweden.">
  <style>
    {inter_css()}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{FRAME}"/>
  {art}
  <g font-family="{INTER}">
    <text x="{W - 32}" y="42" text-anchor="end" font-size="14" fill="{MUTED}">Göteborg, Sweden</text>
    <text x="{TX}" y="{CY - 6}" font-size="50" font-weight="700" fill="{INK}" letter-spacing="-0.5">Firat Kaya</text>
    {role_line(CY + 36, "Computer Engineering student at", "uw", "University West")}
    {role_line(CY + 70, "Game Developer Intern at", "realdini", "Realdini Studios")}
  </g>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, f"{W}x{H}", os.path.getsize(OUT) // 1024, "KB")
