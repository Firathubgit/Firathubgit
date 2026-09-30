"""
Turn assets/source-prepped.png into an animated ASCII portrait SVG.

Light ink on dark glass: bright pixels get dense glyphs, the cut-out
background becomes blank. Glyphs are split into three tone layers (dim /
mid / bright ink) so the face reads clearly instead of as one flat colour.
Each row is revealed by a left->right clip wipe with a cyan block cursor
riding the edge (a terminal "printing" the face), then a faint HUD scan-line
sweeps down on a loop. SMIL only -> animates on GitHub.

    python scripts/make_ascii_svg.py [prepped.png] [out.svg]
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, FRAME, INK, MUTED, CYAN, AMBER, GREEN, MONO,  # noqa: E402
                   corners, titlebar, esc)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "portrait.svg")

COLS = 118
CELL_W = 4.8
CELL_H = 8.8
FONT = 8.2
RAMP = " .'`,:;-~=+*ico%#&@"     # sparse -> dense (dark -> bright on a dark bg)
GAMMA = 0.85                     # <1 lifts skin tones into the dense glyphs
MASK_T = 0.5                     # alpha below this -> blank
CROP = (70, 20, 632, 660)        # head + shoulders (l, t, r, b)
TONES = [(0.0, "#566b82"), (0.34, "#a3b8cc"), (0.62, "#f0f8ff")]  # (from level, ink)

PAD = 18
TB = 30
SB = 34

NBSP = "\u00a0"  # real spaces collapse in SVG text; nbsp keeps the grid

ROW_DUR = 0.055
T0 = 0.35                        # delay before printing starts

im = Image.open(SRC).crop(CROP)
w, h = im.size
ROWS = int(round(COLS * (h / w) * (CELL_W / CELL_H)))
g = im.convert("L").filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
a = im.split()[3]
g = np.asarray(g.resize((COLS, ROWS), Image.LANCZOS), dtype=np.float32) / 255.0
a = np.asarray(a.resize((COLS, ROWS), Image.LANCZOS), dtype=np.float32) / 255.0

# normalise luminance inside the subject only, so the ramp is fully used
inside = a > MASK_T
lo, hi = np.percentile(g[inside], 3), np.percentile(g[inside], 99.5)
g = np.clip((g - lo) / (hi - lo), 0, 1) ** GAMMA

# per cell: glyph + tone band
grid = [[" "] * COLS for _ in range(ROWS)]
band = [[-1] * COLS for _ in range(ROWS)]
for r in range(ROWS):
    for c in range(COLS):
        if a[r, c] <= MASK_T:
            continue
        v = float(g[r, c])
        idx = 1 + int(v * (len(RAMP) - 2) + 0.5)          # never blank inside the mask
        grid[r][c] = RAMP[min(idx, len(RAMP) - 1)]
        band[r][c] = max(i for i, (t, _) in enumerate(TONES) if v >= t)

ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
W = int(ART_W + PAD * 2)
H = int(TB + PAD + ART_H + 10 + SB)
AX, AY = PAD, TB + PAD
END = T0 + ROWS * ROW_DUR

out = []
out.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="ASCII portrait of Firat Kaya">
  <defs>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset=".9" stop-color="{CYAN}" stop-opacity=".06"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".38" r=".55">
      <stop offset="0" stop-color="{CYAN}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="#0e1926" stroke-width="1"/>
    </pattern>
    <clipPath id="art"><rect x="{AX}" y="{AY}" width="{ART_W}" height="{ART_H}"/></clipPath>
  </defs>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{FRAME}"/>
  <rect x="1" y="{TB + 1}" width="{W - 2}" height="{H - TB - SB - 1}" fill="url(#grid)"/>
  <rect x="1" y="{TB + 1}" width="{W - 2}" height="{H - TB - SB - 1}" fill="url(#glow)"/>
  {titlebar(W, "firat@goteborg: ~/portrait --ascii", "tty0")}
  {corners(AX - 7, AY - 7, ART_W + 14, ART_H + 14, arm=18, opacity=.85)}
  <g font-family="{MONO}" font-size="{FONT}" style="white-space:pre">''')

for r in range(ROWS):
    line = "".join(grid[r])
    if not line.strip():
        continue
    y = AY + r * CELL_H
    begin = round(T0 + r * ROW_DUR, 3)
    first = len(line) - len(line.lstrip())
    last = len(line.rstrip())
    x0 = AX + first * CELL_W
    span = (last - first) * CELL_W
    out.append(
        f'    <clipPath id="r{r}"><rect x="{x0:.1f}" y="{y:.1f}" width="0" height="{CELL_H}">'
        f'<animate attributeName="width" from="0" to="{span:.1f}" begin="{begin}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
    out.append(f'    <g clip-path="url(#r{r})">')
    for bi, (_, ink) in enumerate(TONES):
        s = "".join(grid[r][c] if band[r][c] == bi else " " for c in range(first, last))
        if not s.strip():
            continue
        out.append(
            f'      <text x="{x0:.1f}" y="{y + CELL_H - 2:.1f}" fill="{ink}" textLength="{span:.1f}" '
            f'lengthAdjust="spacingAndGlyphs">{esc(s).replace(chr(32), NBSP)}</text>'
        )
    out.append('    </g>')
    out.append(
        f'    <rect x="{x0:.1f}" y="{y + 0.5:.1f}" width="{CELL_W + 1:.1f}" height="{CELL_H - 1}" fill="{CYAN}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{begin}s" dur="{ROW_DUR}s"/>'
        f'<animate attributeName="x" from="{x0:.1f}" to="{x0 + span:.1f}" begin="{begin}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'</rect>'
    )

sy = H - SB
out.append(f'''  </g>
  <g clip-path="url(#art)">
    <rect x="{AX}" y="{AY - 70}" width="{ART_W}" height="70" fill="url(#scan)" opacity="0">
      <animate attributeName="opacity" to="1" begin="{END:.2f}s" dur="0.01s" fill="freeze"/>
      <animate attributeName="y" values="{AY - 70};{AY + ART_H}" begin="{END:.2f}s" dur="5s" repeatCount="indefinite"/>
    </rect>
  </g>
  <line x1="1" y1="{sy + 0.5}" x2="{W - 1}" y2="{sy + 0.5}" stroke="{FRAME}"/>
  <g font-family="{MONO}" font-size="11">
    <circle cx="20" cy="{sy + SB / 2}" r="4" fill="{GREEN}">
      <animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="32" y="{sy + SB / 2 + 4}" fill="{MUTED}">ONLINE <tspan fill="{FRAME}">|</tspan> <tspan fill="{INK}">GÖTEBORG</tspan> 57.71°N 11.97°E</text>
    <text x="{W - 18}" y="{sy + SB / 2 + 4}" text-anchor="end" fill="{MUTED}">render <tspan fill="{CYAN}">{COLS}x{ROWS}</tspan> <tspan fill="{AMBER}">■</tspan></text>
  </g>
</svg>''')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("wrote", OUT, f"{W}x{H}", f"{ROWS} rows", os.path.getsize(OUT) // 1024, "KB")
