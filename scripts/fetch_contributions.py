#!/usr/bin/env python3
"""
Fetch the last year of daily contribution counts and derived stats into
data/contributions.json.

Source 1: GitHub's public contributions fragment (what the profile page uses).
Source 2 (fallback): github-contributions-api.jogruber.de.
No token needed. Run daily by .github/workflows/update-profile.yml.
"""
import datetime
import json
import os
import re
import sys
from collections import defaultdict

import requests

USER = os.environ.get("GH_PROFILE_USER", "Firathubgit")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "contributions.json")
UA = {"User-Agent": "firathubgit-profile-bot/1.0"}


def from_github():
    from bs4 import BeautifulSoup
    r = requests.get(f"https://github.com/users/{USER}/contributions", headers=UA, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("no calendar cells -- markup changed?")
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        text = tips.get(td.get("id"), "")
        m = re.match(r"(\d+)", text.replace(",", ""))
        days.append({"date": date, "count": int(m.group(1)) if m else 0})
    return days


def from_jogruber():
    r = requests.get(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last", headers=UA, timeout=30)
    r.raise_for_status()
    return [{"date": d["date"], "count": d["count"]} for d in r.json()["contributions"]]


def stats(days):
    today = datetime.date.today().isoformat()
    days = [d for d in days if d["date"] <= today]
    # current streak (today may still be empty -- don't break on it)
    i = len(days) - 1
    if i >= 0 and days[i]["count"] == 0:
        i -= 1
    cur = 0
    while i >= 0 and days[i]["count"] > 0:
        cur += 1
        i -= 1
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    best = max(days, key=lambda d: d["count"]) if days else {"date": today, "count": 0}
    months = defaultdict(int)
    for d in days:
        months[d["date"][:7]] += d["count"]
    return days, {
        "total": sum(d["count"] for d in days),
        "active_days": sum(1 for d in days if d["count"] > 0),
        "current_streak": cur,
        "longest_streak": longest,
        "best_day": best,
        "months": dict(months),
    }


def main():
    days = None
    for fn in (from_github, from_jogruber):
        try:
            days = fn()
            print(f"{fn.__name__}: {len(days)} days")
            break
        except Exception as e:  # noqa: BLE001
            print(f"{fn.__name__} failed: {e}", file=sys.stderr)
    if not days:
        sys.exit("no contribution source reachable")
    days.sort(key=lambda d: d["date"])
    days, s = stats(days)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"user": USER, "generated": datetime.datetime.utcnow().isoformat() + "Z",
                   "stats": s, "days": days}, f, indent=1)
    print("total", s["total"], "streak", s["current_streak"], "longest", s["longest_streak"])


if __name__ == "__main__":
    main()
