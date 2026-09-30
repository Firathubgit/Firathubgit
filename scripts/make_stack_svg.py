"""
Stack section laid out like the CV: category label on the left, then the
CV's own logos + names flowing to the right. Inter, transparent background,
dark and light variants.

    python scripts/make_stack_svg.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import INK, MUTED, INTER, inter_css, text_width, data_uri, esc  # noqa: E402
from make_techrow_svg import KOTLIN  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
TECH = os.path.join(ASSETS, "tech")

# (label, [(icon, name), ...]); None starts a new line after a small gap,
# mirroring the split between languages and frameworks on the CV.
GROUPS = [
    ("Operating Systems", [("windows", "Windows"), ("macos", "MacOS"), ("debian", "Debian"), ("arch", "Arch")]),
    ("Programming", [("python", "Python"), ("sql", "SQL"), ("typescript", "TypeScript"),
                     ("javascript", "JavaScript"), ("cpp", "C++"), ("csharp", "C#"), ("kotlin", "Kotlin"),
                     ("android", "Android"), ("jetpack-compose", "Jetpack Compose"), ("html", "HTML"),
                     ("css", "CSS"), ("linux", "Linux"), ("rest-api", "REST API"), None,
                     ("react", "React"), ("nodejs", "Node.js"), ("supabase", "Supabase"),
                     ("nextjs", "Next.js"), ("threejs", "Three.js")]),
    ("Tools", [("git", "Git"), ("docker", "Docker"), ("figma", "Figma"), ("vscode", "VS Code"),
               ("visual-studio", "Visual Studio"), ("neovim", "Vim/Neovim"), ("youtrack", "YouTrack"),
               ("unity", "Unity"), ("unreal", "Unreal"), ("godot", "Godot"), ("fusion360", "Fusion 360")]),
    ("Certifications", [("cisco", "CCNA 1"), ("cisco", "Linux Unhatched")]),
    ("Languages", ["Swedish — Fluent", "English — Fluent", "Turkish — Fluent"]),
]
ON_DARK = {"unity", "unreal", "threejs"}     # black logos get a light version on dark

W = 1000
LX = 8                 # category label x
IX = 190               # items start
RIGHT = W - 8
ICON = 20
SIZE = 15
ROW = 34
GAP_I = 8
GAP = 22


def icon_svg(slug, x, y, dark):
    if slug == "kotlin":
        s = ICON / 24 * 0.86
        o = ICON * 0.07
        return f'<g transform="translate({x + o:.1f},{y + o:.1f}) scale({s:.4f})">{KOTLIN}</g>'
    name = f"{slug}-ondark" if dark and slug in ON_DARK else slug
    uri = data_uri(os.path.join(TECH, f"{name}.png"), "image/png")
    return f'<image x="{x:.1f}" y="{y:.1f}" width="{ICON}" height="{ICON}" href="{uri}"/>'


def build(dark):
    ink = INK if dark else "#1f2328"
    muted = MUTED if dark else "#59636e"
    rule = "#30363d" if dark else "#d1d9e0"
    o = []
    y = 6
    for gi, (label, items) in enumerate(GROUPS):
        if gi:
            y += 18                              # groups are separated by space only
        top = y
        cy = y + ROW / 2
        o.append(f'<text x="{LX}" y="{cy + 5:.1f}" font-size="14" fill="{muted}">{esc(label)}</text>')
        x = IX
        for it in items:
            if it is None:                       # CV-style divider inside a group
                y += ROW
                y += 6
                cy = y + ROW / 2
                x = IX
                continue
            if isinstance(it, str):              # spoken languages: pill, like the CV
                w = text_width(it, 14) + 24
                if x + w > RIGHT:
                    y += ROW; cy = y + ROW / 2; x = IX
                o.append(f'<rect x="{x:.1f}" y="{cy - 13:.1f}" width="{w:.1f}" height="26" rx="13" fill="none" stroke="{rule}"/>'
                         f'<text x="{x + 12:.1f}" y="{cy + 5:.1f}" font-size="14" fill="{ink}">{esc(it)}</text>')
                x += w + 10
                continue
            slug, name = it
            w = ICON + GAP_I + text_width(name, SIZE)
            if x + w > RIGHT:
                y += ROW; cy = y + ROW / 2; x = IX
            o.append(icon_svg(slug, x, cy - ICON / 2, dark))
            o.append(f'<text x="{x + ICON + GAP_I:.1f}" y="{cy + 5.2:.1f}" font-size="{SIZE}" fill="{ink}">{esc(name)}</text>')
            x += w + GAP
        y += ROW
    H = int(y + 6)
    body = "\n    ".join(o)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack: operating systems, programming, tools, certifications, languages">
  <style>
    {inter_css((400,))}
  </style>
  <g font-family="{INTER}">
    {body}
  </g>
</svg>'''


if __name__ == "__main__":
    for suffix, dark in (("", True), ("-light", False)):
        out = os.path.join(ASSETS, f"stack{suffix}.svg")
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(dark))
        print("wrote", out, os.path.getsize(out) // 1024, "KB")
