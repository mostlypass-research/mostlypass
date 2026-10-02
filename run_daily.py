#!/usr/bin/env python3
"""Morning pipeline: data -> odds -> model -> verdicts -> content -> validation -> approval package.
    .\\mp daily        live (needs ODDS_API_KEY)
    .\\mp fixture      offline test data, written to sandbox/, can never be published
Nothing is published here. Exit code 0 = package produced (READY or BLOCKED); 1 = crash/no data."""
import os
import sys
if "--fixture" in sys.argv:
    os.environ["MP_FIXTURE"] = "1"

import argparse
import datetime as dt
import json
from zoneinfo import ZoneInfo
import pandas as pd
from mp import config
from mp.config import MODEL_DIR, OUT_DIR, MODE
from mp.data import nflverse, oddsapi, polymarket
from mp.models.elo import Elo
from mp.pipeline import research, validate, grade
from mp.content import render, charts, video
from mp import notify


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", action="store_true")
    ap.add_argument("--llm", action="store_true", help="polish prose with the local `claude` CLI (validator still applies)")
    ap.add_argument("--no-video", action="store_true")
    args = ap.parse_args()
    cfg = config.load()
    date_str = dt.datetime.now(ZoneInfo(cfg["brand"]["timezone"])).strftime("%Y-%m-%d")
    warnings: list[str] = []
    print(f"=== {cfg['brand']['name']} daily run · MODE={MODE} · {date_str} ===")

    games = nflverse.load_games()
    snap, info = oddsapi.fetch_odds(cfg, cfg["odds"]["morning_bookmakers"], "morning")
    if snap.empty:
        print("No upcoming NFL games with prices. Nothing to do.")
        return 1
    bench = cfg["odds"]["closing_book"]
    pin = snap[snap.book == bench]
    if pin.empty:
        print(f"STOP: {bench} returned no prices. The benchmark is load-bearing; no verdicts will be produced and no "
              "other book is substituted. Re-run later; if it persists, tell Claude.")
        return 1
    age = (oddsapi.now_utc() - oddsapi.parse(pin.book_ts.max())).total_seconds() / 60
    if age > cfg["odds"]["stale_minutes"]:
        warnings.append(f"{bench} prices are {age:.0f} min old")
    credits = info.get("remaining")
    if credits not in (None, "fixture") and int(float(credits)) < cfg["odds"]["min_credits_warning"]:
        warnings.append(f"Odds API credits low: {credits}")

    ev = snap[["event_id", "home_team", "away_team", "commence_time"]].drop_duplicates("event_id")
    matched = nflverse.match_events(games, ev, cfg["sport"]["season"])
    for r in matched[matched.game_id.isna()].itertuples():
        warnings.append(f"event {r.event_id} not found in nflverse schedule; excluded")

    poly = None
    if cfg["exchange"]["polymarket_enabled"]:
        try:
            poly = polymarket.fetch_nfl_moneylines(cfg)
        except Exception as e:
            print(f"[polymarket] skipped ({e}); display-only, card unaffected")

    elo = Elo.from_cfg(cfg)
    played = games[(games.season > cfg["sport"]["season"] - cfg["model"]["fit_seasons"]) & games.home_score.notna()]
    elo.fit(played)
    elo.save()
    bt_path = MODEL_DIR / "backtest_report.json"
    gate_open = bool(json.loads(bt_path.read_text())["passes_bet_gate"]) if bt_path.exists() else False

    objs, model_warnings = research.build(cfg, snap, matched, elo, poly, warnings, gate_open)
    if not objs:
        print("No research objects could be built:", warnings + model_warnings)
        return 1
    research.append(objs)

    summary = grade.record_summary()
    g = grade.merged()
    recent = pd.DataFrame()
    if len(g) and "graded_ts" in g:
        gg = g.dropna(subset=["graded_ts"])
        recent = gg[gg.graded_ts.map(lambda t: (oddsapi.now_utc() - oddsapi.parse(t)).total_seconds() < 26 * 3600)]
    paths = render.write_all(cfg, objs, summary, render.recap_md(recent, summary), date_str, use_llm=args.llm)
    out = paths["dir"]
    chart = charts.card_chart(objs, out / "card.png", f"NFL Week {objs[0]['week']}: model vs Pinnacle, home spread",
                              test=(MODE != "LIVE"))
    short_ok = False
    if cfg["content"]["short_video"] and not args.no_video:
        sh = paths["short"]
        short_ok = video.build_short(chart, sh["captions"], cfg["brand"]["name"], out / "short.mp4", out / "frames",
                                     test=(MODE != "LIVE")) is not None

    # validation: every number in every publishable artifact must exist in the data
    cnt = render.counts(objs)
    bt = json.loads(bt_path.read_text()) if bt_path.exists() else None
    allowed = validate.allowed_from(objs, summary, cfg, bt)
    sh = paths["short"]
    errors = []
    for name, text in (("newsletter.md", (out / "newsletter.md").read_text()), ("x_posts.txt", (out / "x_posts.txt").read_text()),
                       ("short.json", " ".join([sh["title"], sh["description"]] + sh["captions"]))):
        errors += [f"{name}: {e}" for e in validate.check(text, allowed, cnt)]
    (out / "validation.json").write_text(json.dumps({"mode": MODE, "created_utc": oddsapi.iso(oddsapi.now_utc()),
                                                     "errors": errors, "warnings": warnings,
                                                     "model_warnings": model_warnings}, indent=1))
    pkg = notify.package_text(cfg, date_str, objs, cnt, warnings, model_warnings, errors, credits, gate_open,
                              len(paths["x_posts"]), short_ok, render.record_line(summary))
    (out / "APPROVAL.txt").write_text(pkg)
    print("\n" + pkg + "\n")
    if MODE == "LIVE":
        print(notify.github_issue(f"Approve {date_str} research (Week {objs[0]['week']})", pkg))
    print(f"Package folder: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
