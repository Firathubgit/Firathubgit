"""Shared palette for the profile SVGs: GitHub's own dark-mode colours, so
everything sits naturally on the profile page."""

BG = "#0d1117"
PANEL = "#161b22"
PANEL2 = "#1c2128"
FRAME = "#30363d"
INK = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
AMBER = "#d29922"
GREEN = "#3fb950"
RED = "#f85149"
PURPLE = "#a371f7"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------------------------------------------------------------- Inter
# The CV is set in Inter. GitHub shows these SVGs through <img>, which cannot
# load web fonts, so the (subset) font files are embedded as data URIs.
import base64 as _b64
import os as _os

_ASSETS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "assets")
INTER = "Inter, " + SANS


def data_uri(path, mime):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + _b64.b64encode(f.read()).decode()


def inter_css(weights=(400, 600, 700)):
    faces = []
    for w in weights:
        uri = data_uri(_os.path.join(_ASSETS, "fonts", f"inter-{w}.woff2"), "font/woff2")
        faces.append(f"@font-face {{ font-family: Inter; font-weight: {w}; src: url({uri}) format('woff2'); }}")
    return "\n    ".join(faces)


_metrics = {}


def text_width(s, size, weight=400):
    """Advance width of s in Inter at the given size (px), for layout."""
    if weight not in _metrics:
        from fontTools.ttLib import TTFont
        f = TTFont(_os.path.join(_ASSETS, "fonts", f"inter-{weight}.woff2"))
        _metrics[weight] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    cmap, hmtx, upm = _metrics[weight]
    total = 0
    for ch in s:
        g = cmap.get(ord(ch))
        total += hmtx[g][0] if g else upm * 0.55
    return total * size / upm


def wrap(s, size, width, weight=400):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if cur and text_width(t, size, weight) > width:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines
