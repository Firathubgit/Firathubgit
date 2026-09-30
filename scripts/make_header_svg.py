"""
Header: ASCII portrait, name, role. Static.

    python scripts/make_header_svg.py [out.svg]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import PANEL, FRAME, INK, MUTED, GREEN, SANS, MONO  # noqa: E402
from ascii_portrait import ascii_portrait  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "header.svg")

W = 1000
PX, PY = 40, 24
art, AW, AH = ascii_portrait(PX, PY, font_family=MONO)
H = int(AH + 2 * PY)
TX = int(PX + AW + 48)
CY = H // 2

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Firat Kaya — Computer Engineering student at University West, Game Developer Intern at Realdini, founder of Volturiano Studios">
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{FRAME}"/>
  {art}
  <g font-family="{SANS}">
    <text x="{TX}" y="{CY - 44}" font-size="56" font-weight="700" fill="{INK}">Firat Kaya</text>
    <text x="{TX}" y="{CY}" font-size="19" fill="{INK}">Computer Engineering student at University West</text>
    <text x="{TX}" y="{CY + 32}" font-size="17" fill="{MUTED}">Game Developer Intern at Realdini</text>
    <text x="{TX}" y="{CY + 58}" font-size="17" fill="{MUTED}">Founder of Volturiano Studios</text>
    <circle cx="{TX + 5}" cy="{CY + 91}" r="4.5" fill="{GREEN}"/>
    <text x="{TX + 18}" y="{CY + 96}" font-size="16" fill="{MUTED}">Göteborg, Sweden</text>
  </g>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, f"{W}x{H}", os.path.getsize(OUT) // 1024, "KB")
