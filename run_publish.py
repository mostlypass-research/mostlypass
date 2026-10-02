#!/usr/bin/env python3
"""After approval: append the public record, build the site, prepare the newsletter for paste.
Hard refusals (not configurable): FIXTURE mode; a package made in FIXTURE mode; any fixture event id;
validation errors; a package older than 8 hours. Signals whose game has already kicked off are never recorded."""
import os
import sys
if "--fixture" in sys.argv:
    os.environ["MP_FIXTURE"] = "1"

import argparse
import datetime as dt
import json
from zoneinfo import ZoneInfo
import markdown
from mp import config
from mp.config import OUT_DIR, MODE
from mp.data import oddsapi
from mp.pipeline import grade
from mp.site import build as site

MAX_AGE_H = 8


def refuse(msg):
    print("REFUSED: " + msg)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="")
    ap.add_argument("--fixture", action="store_true")
    ap.add_argument("--site-only", action="store_true", help="rebuild the site from already-published data")
    args = ap.parse_args()
    config.assert_live("publish")                       # 1. process mode
    cfg = config.load()
    if args.site_only:
        site.build(cfg, None, "")
        return 0
    date_str = args.date or dt.datetime.now(ZoneInfo(cfg["brand"]["timezone"])).strftime("%Y-%m-%d")
    out = OUT_DIR / date_str
    if not (out / "research_objects.json").exists():
        refuse(f"no package for {date_str}")
    if (out / "MODE").read_text().strip() != "LIVE":    # 2. package mode
        refuse("package was produced in FIXTURE mode")
    v = json.loads((out / "validation.json").read_text())
    if v.get("mode") != "LIVE":
        refuse("validation file is not from a LIVE run")
    if v["errors"]:                                     # 3. validator
        refuse("validation errors:\n - " + "\n - ".join(v["errors"]))
    age_h = (oddsapi.now_utc() - oddsapi.parse(v["created_utc"])).total_seconds() / 3600
    if age_h > MAX_AGE_H:                               # 4. stale prices
        refuse(f"package is {age_h:.1f} h old; prices are stale. Run the daily job again, then approve the new issue.")
    objs = json.loads((out / "research_objects.json").read_text())
    if any(o.get("mode") != "LIVE" or str(o["event_id"]).startswith("fx") for o in objs):
        refuse("package contains non-LIVE or fixture objects")   # 5. object-level check
    now = oddsapi.now_utc()
    live = [o for o in objs if oddsapi.parse(o["commence_time"]) > now]
    skipped = len({o["event_id"] for o in objs}) - len({o["event_id"] for o in live})
    if (out / "PUBLISHED").exists():
        print("already published; rebuilding site only")
    else:
        url = f"{cfg['brand']['site_url']}/archive/{date_str}/"
        n = grade.record_published(live, url)
        (out / "PUBLISHED").write_text(oddsapi.iso(now))
        print(f"[record] appended {n} paper signals (BET/LEAN) to database/signals.csv; {skipped} game(s) already started were excluded")
    site.build(cfg, None, date_str)
    nl = (out / "newsletter.md").read_text()
    (out / "newsletter.html").write_text(markdown.markdown(nl, extensions=["tables"]))
    print(f"[newsletter] ready to paste: {out / 'newsletter.html'} (or copy today's page from the website)")
    print(f"[x] posts: {out / 'x_posts.txt'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
