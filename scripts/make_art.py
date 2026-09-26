#!/usr/bin/env python3
"""Generates the static profile art (header banner + project cards). Run once; output is committed."""
import html
import os
import textwrap

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.makedirs("assets/cards", exist_ok=True)

BG0, BG1 = "#1a1b27", "#24283b"
ACC, ACC2, GRN, TXT, MUT = "#7aa2f7", "#bb9af7", "#9ece6a", "#c0caf5", "#565f89"

# ---------------------------------------------------------------- header banner
roles = ["Discord Bot Developer", "Paper / Spigot Plugin Developer", "Building canidelete", "Java · Python · TypeScript"]
n, per = len(roles), 3.0
total = n * per
css = [
    ".t{font-family:Inter,'Segoe UI',Arial,sans-serif;font-weight:800}",
    ".m{font-family:'JetBrains Mono',Consolas,'Courier New',monospace}",
    ".r{opacity:0}",
    ".blob{animation:float 8s ease-in-out infinite}.b2{animation-delay:-4s}",
    "@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(18px,-12px)}}",
    ".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}",
]
body = []
for i, r in enumerate(roles):
    a, b = i / n * 100, (i + 1) / n * 100
    css.append(".r%d{animation:r%d %ss infinite}" % (i, i, total))
    css.append("@keyframes r%d{0%%{opacity:0}%.2f%%{opacity:0;transform:translateY(8px)}%.2f%%{opacity:1;transform:translateY(0)}"
               "%.2f%%{opacity:1;transform:translateY(0)}%.2f%%{opacity:0;transform:translateY(-8px)}100%%{opacity:0}}"
               % (i, a, a + 3, b - 3, b))
    body.append('<text class="m r r%d" x="60" y="178" fill="%s" font-size="22">&gt; %s</text>' % (i, GRN, html.escape(r)))

header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="240" viewBox="0 0 1000 240" role="img" aria-label="Tellegram: Discord bot and Minecraft plugin developer">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient>
<radialGradient id="g1"><stop offset="0" stop-color="{ACC}" stop-opacity=".45"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2"><stop offset="0" stop-color="{ACC2}" stop-opacity=".4"/><stop offset="1" stop-color="{ACC2}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#ffffff" stroke-opacity=".04"/></pattern>
<clipPath id="c"><rect width="1000" height="240" rx="16"/></clipPath>
</defs>
<style>{"".join(css)}</style>
<g clip-path="url(#c)">
<rect width="1000" height="240" fill="url(#bg)"/><rect width="1000" height="240" fill="url(#grid)"/>
<circle class="blob" cx="830" cy="60" r="170" fill="url(#g1)"/><circle class="blob b2" cx="690" cy="220" r="150" fill="url(#g2)"/>
<text class="m" x="60" y="70" fill="{MUT}" font-size="16">// hey there, I'm</text>
<text class="t" x="56" y="132" fill="url(#tx)" font-size="64">Tellegram</text>
{"".join(body)}
<text class="m" x="60" y="214" fill="{MUT}" font-size="14">Germany  ·  he/him  ·  github.com/Telle-dev</text>
<g transform="translate(790,72)">
<rect width="160" height="104" rx="12" fill="#16161e" stroke="{ACC}" stroke-opacity=".35"/>
<circle cx="18" cy="16" r="4" fill="#f7768e"/><circle cx="32" cy="16" r="4" fill="#e0af68"/><circle cx="46" cy="16" r="4" fill="{GRN}"/>
<text class="m" x="16" y="46" font-size="13"><tspan fill="{ACC2}">public class</tspan></text>
<text class="m" x="16" y="66" fill="{TXT}" font-size="13">Tellegram {{</text>
<text class="m" x="16" y="86" fill="{GRN}" font-size="13">  build();<tspan class="cur" fill="{TXT}">▌</tspan></text>
</g>
</g></svg>'''
with open("assets/header.svg", "w", encoding="utf-8") as f:
    f.write(header)

# ---------------------------------------------------------------- project cards
BOOK = ("M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 010-1.5h1.75v-2h-8a1 1 0 00-.714 "
        "1.7.75.75 0 11-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8V1.5zM5 12.25v3.25a.25.25 "
        "0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z")
FONT = "'Segoe UI',Inter,Arial,sans-serif"
cards = [
    ("canidelete", "Finds the workarounds in your code you can finally delete: closed upstream issues, upgraded deps, passed deadlines.",
     "Python", "#3572A5", "CLI · GitHub Action"),
    ("Auto-Message", "Lightweight plugin that sends automatic chat messages with clickable links, commands and sounds.",
     "Java", "#b07219", "Paper · Spigot 1.13–1.21+"),
    ("Anti-Item-Explosions", "Protects whitelisted blocks and dropped items from explosions, fire and lava.",
     "Java", "#b07219", "Paper · Spigot plugin"),
    ("ItemBlocker", "Blocks crafting, using, dropping, placing and picking up configured items. Cleans inventories, even nested shulkers.",
     "Java", "#b07219", "Paper · Purpur 1.20–1.21"),
]
for name, desc, lang, lcol, tag in cards:
    lines = textwrap.wrap(desc, 54)[:3]
    text = "".join('<text x="24" y="%d" fill="#a9b1d6" font-size="13.5" font-family="%s">%s</text>'
                   % (82 + 20 * i, FONT, html.escape(l)) for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="170" viewBox="0 0 440 170" role="img" aria-label="{html.escape(name)}">
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="e" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient>
<clipPath id="k"><rect width="440" height="170" rx="14"/></clipPath></defs>
<g clip-path="url(#k)"><rect width="440" height="170" fill="url(#b)"/><rect width="440" height="3" fill="url(#e)"/></g>
<rect x=".5" y=".5" width="439" height="169" rx="14" fill="none" stroke="#414868"/>
<path transform="translate(24,25) scale(1.1)" fill="{ACC}" d="{BOOK}"/>
<text x="50" y="40" fill="{TXT}" font-size="19" font-weight="700" font-family="{FONT}">{html.escape(name)}</text>
{text}
<circle cx="30" cy="146" r="6" fill="{lcol}"/>
<text x="42" y="151" fill="#a9b1d6" font-size="13" font-family="{FONT}">{lang}</text>
<text x="416" y="151" fill="{MUT}" font-size="12.5" text-anchor="end" font-family="{FONT}">{html.escape(tag)}</text>
</svg>'''
    with open("assets/cards/%s.svg" % name, "w", encoding="utf-8") as f:
        f.write(svg)
print("art written")
