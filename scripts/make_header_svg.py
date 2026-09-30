"""
Header: photo, name, role. Clean and static apart from a short fade-in.

    python scripts/make_header_svg.py [out.svg]
"""
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import PANEL, FRAME, INK, MUTED, GREEN, SANS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "header.svg")
AVATAR = os.path.join(HERE, "..", "assets", "avatar.jpg")

W, H = 1000, 230
R = 76                     # photo radius
CX, CY = 56 + R, H // 2
TX = CX + R + 44

photo = base64.b64encode(open(AVATAR, "rb").read()).decode()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Firat Kaya — Computer Engineering student, Game Developer Intern at Realdini, founder of Volturiano Studios">
  <defs>
    <clipPath id="avatar"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>
  </defs>
  <style>
    .in {{ opacity: 0; animation: in .7s ease forwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{FRAME}"/>
  <g class="in">
    <image x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" clip-path="url(#avatar)" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{photo}" xlink:href="data:image/jpeg;base64,{photo}"/>
    <circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{FRAME}" stroke-width="2"/>
  </g>
  <g font-family="{SANS}">
    <text x="{TX}" y="{CY - 22}" font-size="52" font-weight="700" fill="{INK}" class="in" style="animation-delay:.1s">Firat Kaya</text>
    <text x="{TX}" y="{CY + 18}" font-size="19" fill="{INK}" class="in" style="animation-delay:.25s">Computer Engineering student at University West</text>
    <text x="{TX}" y="{CY + 46}" font-size="16" fill="{MUTED}" class="in" style="animation-delay:.4s">Game Developer Intern at Realdini  ·  Founder of Volturiano Studios</text>
    <g class="in" style="animation-delay:.55s">
      <circle cx="{TX + 5}" cy="{CY + 71}" r="4.5" fill="{GREEN}"/>
      <text x="{TX + 18}" y="{CY + 76}" font-size="15" fill="{MUTED}">Göteborg, Sweden</text>
    </g>
  </g>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
