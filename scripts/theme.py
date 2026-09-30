"""Shared palette + helpers for every SVG in this profile.

Direction: an EV cockpit / HUD. Near-black glass, one cyan signal colour,
amber for warnings/highlights, soft white ink. Everything animates with
SMIL or CSS keyframes only -- GitHub renders SVG inside <img>, so no JS.
"""

BG = "#070b12"        # outer glass
PANEL = "#0b111b"     # panel fill
PANEL2 = "#0e1622"
FRAME = "#1b2838"     # hairline borders
GRID = "#122030"
INK = "#d6e2ee"       # primary text
MUTED = "#6b7f95"     # secondary text
CYAN = "#37e1ff"      # signal
CYAN_DIM = "#1b6f86"
AMBER = "#ffb547"
GREEN = "#3dffa8"
RED = "#ff5470"

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def corners(x, y, w, h, arm=14, color=CYAN, width=2, opacity=0.9):
    """HUD corner brackets around a rectangle."""
    p = []
    for cx, cy, dx, dy in [(x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)]:
        p.append(f"M{cx + dx * arm},{cy} L{cx},{cy} L{cx},{cy + dy * arm}")
    return (f'<path d="{" ".join(p)}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="square" opacity="{opacity}"/>')


def titlebar(w, title, right="", h=30):
    """Window chrome: three lights, a centred title, optional right label."""
    return f"""
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h}" rx="10" fill="{PANEL2}"/>
  <rect x="0.5" y="{h - 10}" width="{w - 1}" height="10.5" fill="{PANEL2}"/>
  <line x1="0" y1="{h + 0.5}" x2="{w}" y2="{h + 0.5}" stroke="{FRAME}"/>
  <circle cx="18" cy="{h / 2}" r="5" fill="{RED}" opacity=".85"/>
  <circle cx="36" cy="{h / 2}" r="5" fill="{AMBER}" opacity=".85"/>
  <circle cx="54" cy="{h / 2}" r="5" fill="{GREEN}" opacity=".85"/>
  <text x="{w / 2}" y="{h / 2 + 4}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(title)}</text>
  <text x="{w - 16}" y="{h / 2 + 4}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{CYAN_DIM}">{esc(right)}</text>"""
