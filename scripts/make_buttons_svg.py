"""
Contact links: one small SVG per link (so each can be wrapped in its own
<a> on GitHub). Icon + label in Inter on a transparent background, so they
read as links, not as part of the header card.

    python scripts/make_buttons_svg.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import INK, INTER, inter_css, text_width, data_uri, esc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
ICONS = os.path.join(ASSETS, "icons")

H = 44
ICON = 18
PADX = 4
GAP = 10


def linkedin_icon(x, y, ink=None):
    d = re.search(r' d="([^"]+)"', open(os.path.join(ICONS, "linkedin.svg")).read()).group(1)
    s = ICON / 512
    ox = x + (ICON - 448 * s) / 2
    # white behind the cut-out "in", blue square on top -> the usual LinkedIn mark
    return (f'<rect x="{ox + 1:.2f}" y="{y + 2:.2f}" width="{448 * s - 2:.2f}" height="{ICON - 4:.2f}" rx="2" fill="#fff"/>'
            f'<g transform="translate({ox:.2f},{y:.2f}) scale({s:.5f})"><path fill="#0a66c2" d="{d}"/></g>')


def mail_icon(x, y, ink="#e6edf3"):
    s = ICON / 24
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.4f})" fill="none" stroke="{ink}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/><rect x="2" y="4" width="20" height="16" rx="2"/></g>')


def portfolio_icon(x, y, ink=None):
    name = "portfolio-light.png" if ink in (None, INK) else "portfolio-dark.png"
    uri = data_uri(os.path.join(ICONS, name), "image/png")
    return f'<image x="{x:.2f}" y="{y:.2f}" width="{ICON}" height="{ICON}" href="{uri}"/>'


BUTTONS = [
    ("portfolio", "Portfolio", portfolio_icon),
    ("linkedin", "LinkedIn", linkedin_icon),
    ("email", "firat05_@hotmail.com", mail_icon),
]


def button(label, icon, ink=INK):
    tw = text_width(label, 15, 600) * 1.02
    W = int(PADX * 2 + ICON + GAP + tw + 2)
    ix, iy = PADX, (H - ICON) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
  <style>
    {inter_css((600,))}
  </style>
  {icon(ix, iy, ink)}
  <text x="{ix + ICON + GAP}" y="{H / 2 + 5.3:.1f}" font-family="{INTER}" font-size="15" font-weight="600" fill="{ink}">{esc(label)}</text>
</svg>'''


if __name__ == "__main__":
    from PIL import Image
    src = Image.open(os.path.join(ICONS, "portfolio.png")).convert("RGBA")
    light = Image.new("RGBA", src.size, (230, 237, 243, 255))
    light.putalpha(src.split()[3])
    light.save(os.path.join(ICONS, "portfolio-light.png"))
    dark = Image.new("RGBA", src.size, (31, 35, 40, 255))
    dark.putalpha(src.split()[3])
    dark.save(os.path.join(ICONS, "portfolio-dark.png"))
    # "-light" files are for GitHub's light theme (dark ink)
    for slug, label, icon in BUTTONS:
        for suffix, ink in (("", INK), ("-light", "#1f2328")):
            out = os.path.join(ASSETS, f"btn-{slug}{suffix}.svg")
            with open(out, "w", encoding="utf-8") as f:
                f.write(button(label, icon, ink))
            print("wrote", out)
