#!/usr/bin/env python3
"""Builds assets/stats.svg and assets/languages.svg from the GitHub GraphQL API.

Runs daily in GitHub Actions with the built-in GITHUB_TOKEN; no third-party service.
Local preview with fake numbers:  python scripts/stats.py --demo
"""
import datetime as dt
import html
import json
import os
import sys
import urllib.request

LOGIN = os.environ.get("PROFILE_LOGIN", "Telle-dev")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
BG0, BG1 = "#1a1b27", "#24283b"
ACC, ACC2, GRN, TXT, SUB, MUT = "#7aa2f7", "#bb9af7", "#9ece6a", "#c0caf5", "#a9b1d6", "#565f89"
FONT = "'Segoe UI',Inter,Arial,sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    pullRequests { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": "bearer " + token, "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit("GraphQL error: %s" % data["errors"])
    return data["data"]["user"]


def demo():
    today = dt.date.today()
    days = [{"date": (today - dt.timedelta(days=i)).isoformat(), "contributionCount": (i * 7) % 5 if i % 9 else 0}
            for i in range(365)][::-1]
    return {
        "createdAt": "2023-03-01T00:00:00Z", "followers": {"totalCount": 12}, "pullRequests": {"totalCount": 9},
        "repositories": {"totalCount": 5, "nodes": [
            {"stargazerCount": 3, "languages": {"edges": [{"size": 90000, "node": {"name": "Java", "color": "#b07219"}}]}},
            {"stargazerCount": 1, "languages": {"edges": [{"size": 40000, "node": {"name": "Python", "color": "#3572A5"}},
                                                          {"size": 5000, "node": {"name": "Shell", "color": "#89e051"}}]}},
            {"stargazerCount": 0, "languages": {"edges": [{"size": 20000, "node": {"name": "JavaScript", "color": "#f1e05a"}},
                                                          {"size": 8000, "node": {"name": "TypeScript", "color": "#3178c6"}}]}},
        ]},
        "contributionsCollection": {"totalCommitContributions": 312, "restrictedContributionsCount": 140,
                                    "contributionCalendar": {"totalContributions": 488,
                                                             "weeks": [{"contributionDays": days}]}},
    }


def streaks(user):
    days = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"] > 0:
            current += 1
        elif i == 0:
            continue  # today not contributed yet: streak still alive
        else:
            break
    return current, longest


def frame(w, h, title, inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}">
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>
<linearGradient id="e" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC2}"/></linearGradient>
<clipPath id="k"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>
<style>.f{{font-family:{FONT}}}.in{{opacity:0;animation:in .6s ease forwards}}@keyframes in{{to{{opacity:1}}}}</style>
<g clip-path="url(#k)"><rect width="{w}" height="{h}" fill="url(#b)"/><rect width="{w}" height="3" fill="url(#e)"/></g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="#414868"/>
<text class="f" x="24" y="38" fill="{ACC}" font-size="17" font-weight="700">{html.escape(title)}</text>
{inner}
</svg>'''


def stats_svg(user):
    cc = user["contributionsCollection"]
    stars = sum(r["stargazerCount"] for r in user["repositories"]["nodes"])
    cur, longest = streaks(user)
    total = cc["contributionCalendar"]["totalContributions"]
    rows = [
        ("Contributions (last year)", "{:,}".format(total)),
        ("Commits (last year)", "{:,}".format(cc["totalCommitContributions"] + cc["restrictedContributionsCount"])),
        ("Current streak", "%d day%s" % (cur, "" if cur == 1 else "s")),
        ("Longest streak", "%d day%s" % (longest, "" if longest == 1 else "s")),
        ("Public repos", str(user["repositories"]["totalCount"])),
        ("Stars earned", str(stars)),
    ]
    out = []
    for i, (k, v) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 24 + col * 220, 72 + row * 52
        out.append('<g class="in" style="animation-delay:%.2fs"><text class="f" x="%d" y="%d" fill="%s" font-size="12.5">%s</text>'
                   '<text class="f" x="%d" y="%d" fill="%s" font-size="20" font-weight="700">%s</text></g>'
                   % (i * 0.08, x, y, MUT, html.escape(k), x, y + 22, TXT, html.escape(v)))
    upd = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    out.append('<text class="f" x="440" y="222" fill="%s" font-size="10.5" text-anchor="end">updated %s</text>' % (MUT, upd))
    return frame(464, 236, "GitHub Stats", "".join(out))


def langs_svg(user):
    sizes, colors = {}, {}
    for r in user["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            sizes[n] = sizes.get(n, 0) + e["size"]
            colors[n] = e["node"]["color"] or "#888"
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    total = float(sum(s for _, s in top)) or 1.0
    out, x = [], 24.0
    width = 416.0
    out.append('<clipPath id="bar"><rect x="24" y="58" width="%d" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">' % width)
    for n, s in top:
        w = width * s / total
        out.append('<rect x="%.2f" y="58" width="%.2f" height="10" fill="%s"/>' % (x, w + 0.5, colors[n]))
        x += w
    out.append("</g>")
    for i, (n, s) in enumerate(top):
        col, row = i % 2, i // 2
        cx, cy = 30 + col * 220, 100 + row * 36
        out.append('<g class="in" style="animation-delay:%.2fs"><circle cx="%d" cy="%d" r="6" fill="%s"/>'
                   '<text class="f" x="%d" y="%d" fill="%s" font-size="14">%s</text>'
                   '<text class="f" x="%d" y="%d" fill="%s" font-size="13">%.1f%%</text></g>'
                   % (i * 0.08, cx, cy, colors[n], cx + 14, cy + 5, SUB, html.escape(n), cx + 150, cy + 5, MUT, 100 * s / total))
    if not top:
        out.append('<text class="f" x="24" y="110" fill="%s" font-size="14">No public code yet</text>' % MUT)
    return frame(464, 236, "Most Used Languages", "".join(out))


def main():
    if "--demo" in sys.argv:
        user = demo()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise SystemExit("GITHUB_TOKEN missing")
        user = fetch(token)
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("stats.svg", stats_svg(user)), ("languages.svg", langs_svg(user))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print("wrote stats.svg and languages.svg")


if __name__ == "__main__":
    main()
