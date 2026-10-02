#!/usr/bin/env python3
"""Nightly: grade finished games (nflverse scores, Odds API fallback), CLV vs our own pre-kickoff close,
equity chart (BET rows only), rebuild the site."""
import os
import sys
if "--fixture" in sys.argv:
    os.environ["MP_FIXTURE"] = "1"

from mp import config
from mp.config import SITE_DIR
from mp.data import nflverse
from mp.pipeline import grade
from mp.content import charts, render
from mp.site import build as site


def main():
    cfg = config.load()
    try:
        games = nflverse.load_games()
    except Exception as e:
        print(f"[grade] nflverse unavailable ({e}); Odds API scores only")
        games = None
    graded = grade.grade(cfg, games)
    s = grade.record_summary()
    (SITE_DIR / "record").mkdir(parents=True, exist_ok=True)
    charts.equity_curve(grade.merged(), SITE_DIR / "record" / "equity.png", "Paper BET P/L, cumulative units")
    print(render.record_line(s))
    site.build(cfg, None, "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
