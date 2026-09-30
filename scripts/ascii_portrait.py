"""
ASCII portrait from assets/source-prepped.png (made by prep_photo.py).

Static: just the glyphs, no frame or animation. Bright pixels get dense
glyphs; three ink tones keep the face readable. Used by make_header_svg.py.
"""
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "source-prepped.png")

RAMP = " .'`,:;-~=+*ico%#&@"          # sparse -> dense (dark -> bright on a dark bg)
GAMMA = 0.85
MASK_T = 0.5
CROP = (70, 20, 632, 660)             # head + shoulders (l, t, r, b)
TONES = [(0.0, "#737d88"), (0.34, "#a8b1bb"), (0.62, "#f0f3f6")]
NBSP = " "                       # plain spaces collapse in SVG text


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ascii_portrait(x, y, cols=96, cell_w=4.0, cell_h=7.3, font_family="monospace"):
    """Return (svg_group, width, height) for the portrait placed at (x, y)."""
    im = Image.open(SRC).crop(CROP)
    w, h = im.size
    rows = int(round(cols * (h / w) * (cell_w / cell_h)))
    g = im.convert("L").filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
    a = im.split()[3]
    g = np.asarray(g.resize((cols, rows), Image.LANCZOS), dtype=np.float32) / 255.0
    a = np.asarray(a.resize((cols, rows), Image.LANCZOS), dtype=np.float32) / 255.0
    inside = a > MASK_T
    lo, hi = np.percentile(g[inside], 3), np.percentile(g[inside], 99.5)
    g = np.clip((g - lo) / (hi - lo), 0, 1) ** GAMMA

    font = cell_h * 0.93
    out = [f'<g font-family="{font_family}" font-size="{font:.1f}" style="white-space:pre">']
    for r in range(rows):
        glyph, band = [], []
        for c in range(cols):
            if a[r, c] <= MASK_T:
                glyph.append(" "); band.append(-1); continue
            v = float(g[r, c])
            glyph.append(RAMP[min(1 + int(v * (len(RAMP) - 2) + 0.5), len(RAMP) - 1)])
            band.append(max(i for i, (t, _) in enumerate(TONES) if v >= t))
        line = "".join(glyph)
        if not line.strip():
            continue
        first = len(line) - len(line.lstrip())
        last = len(line.rstrip())
        x0 = x + first * cell_w
        span = (last - first) * cell_w
        ty = y + r * cell_h + cell_h - 1.5
        for bi, (_, ink) in enumerate(TONES):
            s = "".join(glyph[c] if band[c] == bi else " " for c in range(first, last))
            if s.strip():
                out.append(f'<text x="{x0:.1f}" y="{ty:.1f}" fill="{ink}" textLength="{span:.1f}" '
                           f'lengthAdjust="spacingAndGlyphs">{_esc(s).replace(" ", NBSP)}</text>')
    out.append("</g>")
    return "\n".join(out), cols * cell_w, rows * cell_h
