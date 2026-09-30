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
