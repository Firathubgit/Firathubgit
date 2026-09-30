"""
Header banner: an EV cockpit boot screen.

- name draws in stroke-first, then fills
- a typewriter line cycles through what Firat is working on
- a speedometer-style gauge sweeps up on boot, then idles
- a perspective road with lane markings rushing toward the viewer

    python scripts/make_header_svg.py [out.svg]
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, PANEL, FRAME, INK, MUTED, CYAN, CYAN_DIM, AMBER, GREEN,  # noqa: E402
                   MONO, SANS, corners, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "header.svg")

W, H = 1000, 300

PHRASES = [
    "building Android Automotive cockpits with an AI copilot",
    "game developer intern @ Realdini",
    "founder of Volturiano Studios",
    "3D, Unity & data viz for real industry data",
    "computer engineering @ University West, class of '27",
]
CHAR = 0.045      # seconds per typed character
HOLD = 1.9        # seconds a finished line stays
ERASE = 0.35      # wipe-out time
BOOT = 1.8        # typewriter starts after the name lands

# -------------------------------------------------------------- typewriter
slots = []
t = 0.0
for p in PHRASES:
    d_type = len(p) * CHAR
    slots.append((t, d_type))
    t += d_type + HOLD + ERASE
CYCLE = t

TX, TY = 60, 196
CW = 8.4          # approx char advance at font-size 14 mono (clip only, never layout)
tw_parts = []
for i, (p, (s, d_type)) in enumerate(zip(PHRASES, slots)):
    full = len(p) * CW + 12
    k0 = s / CYCLE
    k1 = (s + d_type) / CYCLE
    k2 = (s + d_type + HOLD) / CYCLE
    k3 = (s + d_type + HOLD + ERASE) / CYCLE
    # steps: discrete-ish typing via many keyframes
    n = len(p)
    kt, vals = ["0"], ["0"]
    if k0 > 0:
        kt.append(f"{k0:.5f}"); vals.append("0")
    for j in range(1, n + 1):
        kt.append(f"{k0 + (k1 - k0) * j / n:.5f}"); vals.append(f"{j * CW:.1f}")
    kt += [f"{k2:.5f}", f"{k3:.5f}"]; vals += [f"{n * CW:.1f}", "0"]
    if k3 < 0.99999:
        kt.append("1"); vals.append("0")
    # de-duplicate identical key times (keep order)
    seen, KT, VV = set(), [], []
    for a, b in zip(kt, vals):
        if a in seen:
            continue
        seen.add(a); KT.append(a); VV.append(b)
    tw_parts.append(f'''
    <clipPath id="tw{i}"><rect x="{TX + 18}" y="{TY - 16}" width="0" height="24">
      <animate attributeName="width" values="{';'.join(VV)}" keyTimes="{';'.join(KT)}" dur="{CYCLE:.2f}s" begin="{BOOT}s" repeatCount="indefinite"/>
    </rect></clipPath>
    <text x="{TX + 18}" y="{TY}" clip-path="url(#tw{i})" font-family="{MONO}" font-size="14" fill="{INK}" style="white-space:pre">{esc(p)}</text>
    <rect x="{TX + 18}" y="{TY - 13}" width="8" height="16" fill="{CYAN}" opacity="0">
      <animate attributeName="x" values="{';'.join(f'{TX + 18 + float(v):.1f}' for v in VV)}" keyTimes="{';'.join(KT)}" dur="{CYCLE:.2f}s" begin="{BOOT}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{max(k0, 0.00001):.5f};{k3:.5f};{min(k3 + 0.00001, 1):.5f};1" dur="{CYCLE:.2f}s" begin="{BOOT}s" repeatCount="indefinite" calcMode="discrete"/>
    </rect>''')

# -------------------------------------------------------------- gauge
GX, GY, GR = 845, 150, 92
A0, A1 = 135, 405            # degrees, clockwise from +x (SVG coords)


def pol(a, r):
    rad = math.radians(a)
    return GX + r * math.cos(rad), GY + r * math.sin(rad)


ticks = []
for k in range(0, 41):
    a = A0 + (A1 - A0) * k / 40
    major = k % 5 == 0
    r1 = GR - (14 if major else 7)
    x1, y1 = pol(a, GR)
    x2, y2 = pol(a, r1)
    col = AMBER if k >= 34 else (CYAN if major else CYAN_DIM)
    ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{2 if major else 1}"/>')
    if major:
        lx, ly = pol(a, GR - 27)
        ticks.append(f'<text x="{lx:.1f}" y="{ly + 3.5:.1f}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTED}">{k // 5}</text>')

sx, sy = pol(A0, GR + 8)
ex, ey = pol(A1, GR + 8)
arc_len = math.radians(A1 - A0) * (GR + 8)
arc = f"M{sx:.1f},{sy:.1f} A{GR + 8},{GR + 8} 0 1 1 {ex:.1f},{ey:.1f}"
# needle idles around ~5 (years coding); rotate from A0
idle = A0 + (A1 - A0) * 5.2 / 8

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Firat Kaya — computer engineer, automotive UI and game developer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0a1420"/><stop offset=".55" stop-color="{BG}"/><stop offset="1" stop-color="#05080d"/>
    </linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#bff4ff"/><stop offset="1" stop-color="{CYAN}"/>
    </linearGradient>
    <linearGradient id="road" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath>
    <clipPath id="nameclip"><text x="56" y="140" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="2">FIRAT KAYA</text></clipPath>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#10202e"/></pattern>
  </defs>
  <style>
    .draw {{ stroke-dasharray: 900; stroke-dashoffset: 900; animation: draw 1.4s cubic-bezier(.6,0,.2,1) .2s forwards; }}
    .fill {{ opacity: 0; animation: fade .6s ease 1.2s forwards; }}
    .up {{ opacity: 0; transform: translateY(8px); animation: up .6s ease forwards; }}
    .needle {{ transform-origin: {GX}px {GY}px; transform: rotate(0deg); animation: sweep 1.6s cubic-bezier(.5,0,.2,1) .4s forwards, idle 3.2s ease-in-out 2s infinite alternate; }}
    .arc {{ stroke-dasharray: {arc_len:.1f}; stroke-dashoffset: {arc_len:.1f}; animation: arc 1.6s cubic-bezier(.5,0,.2,1) .4s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes up {{ to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes sweep {{ 0% {{ transform: rotate(0deg); }} 55% {{ transform: rotate({A1 - A0 - 6}deg); }} 100% {{ transform: rotate({idle - A0:.1f}deg); }} }}
    @keyframes idle {{ from {{ transform: rotate({idle - A0:.1f}deg); }} to {{ transform: rotate({idle - A0 + 7:.1f}deg); }} }}
    @keyframes arc {{ 0% {{ stroke-dashoffset: {arc_len:.1f}; }} 55% {{ stroke-dashoffset: 8; }} 100% {{ stroke-dashoffset: {arc_len * (1 - 5.2 / 8):.1f}; }} }}
  </style>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>

    <!-- road: horizon + lanes rushing in -->
    <g opacity=".9">
      <path d="M430,{H} L610,222 L650,222 L1000,{H - 10} L1000,{H} Z" fill="url(#road)" opacity=".25"/>
      <line x1="470" y1="{H}" x2="614" y2="222" stroke="{CYAN_DIM}" stroke-width="1.5"/>
      <line x1="960" y1="{H}" x2="646" y2="222" stroke="{CYAN_DIM}" stroke-width="1.5"/>
      <line x1="715" y1="{H}" x2="630" y2="222" stroke="{CYAN}" stroke-width="3" stroke-dasharray="14 18" opacity=".8">
        <animate attributeName="stroke-dashoffset" from="0" to="-64" dur=".55s" repeatCount="indefinite"/>
      </line>
      <line x1="0" y1="222.5" x2="{W}" y2="222.5" stroke="{FRAME}"/>
    </g>

    <!-- left: identity -->
    <text x="60" y="56" font-family="{MONO}" font-size="12" fill="{CYAN}" letter-spacing="3" class="up" style="animation-delay:.1s">// COMPUTER ENGINEER · AUTOMOTIVE UI · GAME DEV</text>
    <text x="56" y="140" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="2" fill="none" stroke="{CYAN}" stroke-width="1.2" class="draw">FIRAT KAYA</text>
    <text x="56" y="140" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="2" fill="url(#name)" class="fill">FIRAT KAYA</text>
    <g clip-path="url(#nameclip)">
      <rect x="-200" y="60" width="140" height="100" fill="url(#sheen)" transform="skewX(-20)">
        <animate attributeName="x" values="-200;900" dur="1.3s" begin="2.2s;sheen.end+5s" id="sheen"/>
      </rect>
    </g>
    <text x="{TX}" y="{TY}" font-family="{MONO}" font-size="14" fill="{GREEN}">❯</text>
    {"".join(tw_parts)}

    <g font-family="{MONO}" font-size="11" class="up" style="animation-delay:1.4s">
      <rect x="60" y="238" width="118" height="24" rx="12" fill="{PANEL}" stroke="{FRAME}"/>
      <circle cx="75" cy="250" r="3.5" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>
      <text x="85" y="254" fill="{INK}">now building</text>
      <rect x="186" y="238" width="160" height="24" rx="12" fill="{PANEL}" stroke="{FRAME}"/>
      <text x="200" y="254" fill="{MUTED}">📍 <tspan fill="{INK}">Göteborg, Sweden</tspan></text>
      <rect x="354" y="238" width="122" height="24" rx="12" fill="{PANEL}" stroke="{FRAME}"/>
      <text x="368" y="254" fill="{MUTED}">SV <tspan fill="{FRAME}">/</tspan> <tspan fill="{INK}">EN</tspan></text>
    </g>

    <!-- right: gauge -->
    <circle cx="{GX}" cy="{GY}" r="{GR + 30}" fill="url(#halo)"/>
    <circle cx="{GX}" cy="{GY}" r="{GR + 14}" fill="{PANEL}" stroke="{FRAME}"/>
    <path d="{arc}" fill="none" stroke="{FRAME}" stroke-width="4" stroke-linecap="round"/>
    <path d="{arc}" fill="none" stroke="{CYAN}" stroke-width="4" stroke-linecap="round" class="arc"/>
    {"".join(ticks)}
    <g class="needle">
      <line x1="{GX}" y1="{GY}" x2="{pol(A0, GR - 16)[0]:.1f}" y2="{pol(A0, GR - 16)[1]:.1f}" stroke="{AMBER}" stroke-width="3" stroke-linecap="round"/>
    </g>
    <circle cx="{GX}" cy="{GY}" r="9" fill="{BG}" stroke="{AMBER}" stroke-width="2"/>
    <text x="{GX}" y="{GY + 42}" text-anchor="middle" font-family="{SANS}" font-size="26" font-weight="700" fill="{INK}">5+</text>
    <text x="{GX}" y="{GY + 58}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTED}" letter-spacing="2">YEARS CODING</text>
    <text x="{GX - 64}" y="{H - 16}" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="1">DRIVE MODE</text>
    <text x="{GX + 16}" y="{H - 16}" font-family="{MONO}" font-size="10" fill="{GREEN}" letter-spacing="1">■ BUILD</text>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{FRAME}"/>
  {corners(10, 10, W - 20, H - 20, arm=16, opacity=.7)}
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
