#!/usr/bin/env python3
"""PRIVATE ledger for your own systems' picks. Never published, never committed (private/ is git-ignored).

  .\\mp mypick NFL Patriots +7 -110 [system] [book]      log a pick (must be before kickoff)
  .\\mp mypick NCAAF "Ohio State" -14 -110 [system]
  .\\mp mypick NFL Texans ML +120 [system]               moneyline
  .\\mp mypicks                                          grade finished games + show the record

Every pick is stamped with the time you logged it; a pick logged after kickoff is refused.
Results: NFL from nflverse (free); NCAAF from The Odds API scores (2 credits, only when something needs grading,
and only finds games from the last 3 days, so run `.\\mp mypicks` at least every couple of days).
Closing line (NFL only): our own Pinnacle capture (read from the public repo); if missing, the nflverse consensus
close, labelled as such. NCAAF has no closing capture, so no CLV. Files are append-only.
"""
from __future__ import annotations
import hashlib
import io
import subprocess
import sys
import pandas as pd
import requests
from mp import config
from mp.config import ROOT
from mp.data import oddsapi, nflverse
from mp.pipeline.grade import result_for
from mp.pipeline.devig import clv, american_to_decimal

PRIV = ROOT / "private"
PICKS = PRIV / "my_picks.csv"
GRADES = PRIV / "my_grades.csv"
SPORTS = {"NFL": "americanfootball_nfl", "NCAAF": "americanfootball_ncaaf"}


def _private_ok():
    PRIV.mkdir(exist_ok=True)
    r = subprocess.run(["git", "check-ignore", "-q", "private/my_picks.csv"], cwd=ROOT, capture_output=True)
    if (ROOT / ".git").exists() and r.returncode != 0:
        print("STOP: private/ is not git-ignored, so your picks could be committed. Nothing was saved. Tell Claude.")
        sys.exit(1)


def _num(s: str) -> float:
    return float(s.replace("+", ""))


def add(argv):
    if len(argv) < 4:
        print(__doc__)
        return 1
    league, team, line_s, price_s = argv[0].upper(), argv[1], argv[2], argv[3]
    system = argv[4] if len(argv) > 4 else "default"
    book = argv[5] if len(argv) > 5 else ""
    if league not in SPORTS:
        print(f"League must be NFL or NCAAF (got {league}).")
        return 1
    try:
        price = _num(price_s)
        market, line = ("h2h", None) if line_s.upper() == "ML" else ("spreads", _num(line_s))
    except ValueError:
        print("Line must look like +7, -2.5 or ML; price like -110 or +120.")
        return 1
    if not (price <= -100 or price >= 100):
        print("Price must be American odds, e.g. -110 or +120.")
        return 1
    _private_ok()
    cfg = config.load()
    cfg["sport"]["key"] = SPORTS[league]
    now = oddsapi.now_utc()
    evs = [e for e in oddsapi.fetch_events(cfg) if oddsapi.parse(e["commence_time"]) > now]   # free endpoint
    t = team.lower()
    hits = [(e, side) for e in evs for side in (e["home_team"], e["away_team"])
            if t == side.lower() or side.lower().startswith(t + " ") or side.lower().endswith(" " + t)]
    if not hits:
        print(f"STOP: no upcoming {league} game found for '{team}' (games already started cannot be logged).")
        return 1
    first = min(oddsapi.parse(e["commence_time"]) for e, _ in hits)
    hits = [(e, s) for e, s in hits if oddsapi.parse(e["commence_time"]) == first]
    if len({s for _, s in hits}) > 1:
        print(f"STOP: '{team}' matches more than one team: {sorted({s for _, s in hits})}. Use the full name in quotes.")
        return 1
    ev, sel = hits[0]
    row = {"pick_id": "", "logged_ts": oddsapi.iso(now), "system": system, "league": league, "event_id": ev["id"],
           "commence_time": ev["commence_time"], "home": ev["home_team"], "away": ev["away_team"], "selection": sel,
           "market": market, "line": line, "price": price, "book": book, "stake_units": 1.0}
    row["pick_id"] = hashlib.sha1(f"{system}|{ev['id']}|{sel}|{market}".encode()).hexdigest()[:10]
    if PICKS.exists() and row["pick_id"] in set(pd.read_csv(PICKS).pick_id):
        print("Already logged (same system, game and side). Nothing added.")
        return 0
    pd.DataFrame([row]).to_csv(PICKS, mode="a", header=not PICKS.exists(), index=False)
    hrs = (oddsapi.parse(ev["commence_time"]) - now).total_seconds() / 3600
    ln = "ML" if line is None else f"{line:+g}"
    print(f"LOGGED (private): {sel} {ln} {price:+g}  [{system}]  {ev['away_team']} @ {ev['home_team']}, "
          f"kickoff {ev['commence_time']} ({hrs:.1f}h from now). Logged at {row['logged_ts']}.")
    return 0


def _repo_closes() -> pd.DataFrame | None:
    """Our public Pinnacle closing captures, read straight from GitHub (always current)."""
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        slug = url.split("github.com/")[1].removesuffix(".git")
        r = requests.get(f"https://raw.githubusercontent.com/{slug}/main/database/closes.csv", timeout=30)
        r.raise_for_status()
        return pd.read_csv(io.StringIO(r.text))
    except Exception as e:
        print(f"[mypicks] could not read our closing captures ({e}); CLV falls back to nflverse.")
        return None


def _our_close(closes, p):
    if closes is None:
        return None
    d = closes[(closes.event_id == p.event_id) & (closes.market == p.market) & (closes.name == p.selection)]
    d = d[d.snapshot_ts.map(oddsapi.parse) < oddsapi.parse(p.commence_time)]
    if d.empty:
        return None
    d = d[d.snapshot_ts == d.snapshot_ts.max()].iloc[0]
    return {"price": float(d.price), "point": float(d.point) if pd.notna(d.point) else None, "ts": d.snapshot_ts}


def grade():
    if not PICKS.exists():
        return
    picks = pd.read_csv(PICKS)
    done = set(pd.read_csv(GRADES).pick_id) if GRADES.exists() else set()
    now = oddsapi.now_utc()
    todo = picks[~picks.pick_id.isin(done)]
    todo = todo[todo.commence_time.map(lambda c: (now - oddsapi.parse(c)).total_seconds() > 3.5 * 3600)]
    if todo.empty:
        return
    cfg = config.load()
    scores, closes, games = {}, None, None
    nfl = todo[todo.league == "NFL"]
    if len(nfl):
        games = nflverse.load_games()
        closes = _repo_closes()
        m = nflverse.match_events(games, nfl.rename(columns={"home": "home_team", "away": "away_team"}), cfg["sport"]["season"])
        g = games.set_index("game_id")
        for r in m.itertuples(index=False):
            if r.game_id and r.game_id in g.index and pd.notna(g.loc[r.game_id].home_score):
                gg = g.loc[r.game_id]
                scores[r.event_id] = (float(gg.home_score), float(gg.away_score), "nflverse", gg.spread_line)
    if len(todo[todo.league == "NCAAF"]):
        cfg["sport"]["key"] = SPORTS["NCAAF"]
        try:
            for r in oddsapi.fetch_scores(cfg).itertuples(index=False):
                if pd.notna(r.home_score):
                    scores[r.event_id] = (r.home_score, r.away_score, "the-odds-api", None)
        except Exception as e:
            print(f"[mypicks] NCAAF scores unavailable: {e}")
    rows = []
    for p in todo.itertuples(index=False):
        if p.event_id not in scores:
            print(f"  pending: {p.selection} ({p.league}) - no final score found yet")
            continue
        hs, as_, src, nfl_close_home = scores[p.event_id]
        line = p.line if pd.notna(p.line) else None
        res = result_for(p.market, p.selection, p.home, line, hs, as_)
        pl = 0.0 if res == "push" else (american_to_decimal(p.price) - 1 if res == "win" else -1.0)
        row = {"pick_id": p.pick_id, "graded_ts": oddsapi.iso(now), "home_score": hs, "away_score": as_,
               "score_source": src, "result": res, "pl_units": round(pl, 3), "close_line": None, "close_price": None,
               "clv_points": None, "clv_prob": None, "close_source": "none (no capture for this league)"}
        c = _our_close(closes, p) if p.league == "NFL" else None
        if c:
            row.update(close_line=c["point"], close_price=c["price"], close_source="Mostly Pass Pinnacle capture")
            if p.market == "h2h" or (line is not None and c["point"] == float(line)):
                row["clv_prob"] = round(clv(p.price, c["price"]), 4)
            if p.market == "spreads" and c["point"] is not None:
                row["clv_points"] = round(float(line) - c["point"], 1)
        elif p.league == "NFL" and p.market == "spreads" and pd.notna(nfl_close_home):
            close_sel = -float(nfl_close_home) if p.selection == p.home else float(nfl_close_home)   # nflverse: + = home favored
            row.update(close_line=close_sel, close_source="nflverse consensus close (fallback)",
                       clv_points=round(float(line) - close_sel, 1))
        rows.append(row)
    if rows:
        pd.DataFrame(rows).to_csv(GRADES, mode="a", header=not GRADES.exists(), index=False)


def report():
    if not PICKS.exists():
        print("No private picks logged yet.  Example:  .\\mp mypick NFL Patriots +7 -110")
        return 0
    d = pd.read_csv(PICKS)
    if GRADES.exists():
        d = d.merge(pd.read_csv(GRADES), on="pick_id", how="left")
    else:
        d["result"] = None
    print("\nPRIVATE LEDGER (not published; 1 unit flat per pick)\n")
    for p in d.sort_values("commence_time").itertuples(index=False):
        ln = "ML" if pd.isna(p.line) else f"{p.line:+g}"
        res = p.result if isinstance(p.result, str) else "pending"
        extra = ""
        if isinstance(p.result, str):
            extra = f"  {p.pl_units:+.2f}u"
            if pd.notna(p.clv_points):
                extra += f"  CLV {p.clv_points:+.1f} pts"
            if pd.notna(getattr(p, "clv_prob", None)):
                extra += f" / {p.clv_prob * 100:+.1f}% prob"
        print(f"  [{p.system}] {p.league} {p.selection} {ln} {p.price:+g}  ->  {res}{extra}")
    g = d[d.result.notna()] if "result" in d else d.iloc[0:0]
    print("\nBY SYSTEM")
    for sysname, s in d.groupby("system"):
        gs = g[g.system == sysname]
        w, l, pu = (gs.result == "win").sum(), (gs.result == "loss").sum(), (gs.result == "push").sum()
        units = gs.pl_units.sum() if len(gs) else 0.0
        clvp = gs.clv_points.dropna() if len(gs) else pd.Series(dtype=float)
        line = f"  {sysname}: {len(s)} logged, {w}-{l}-{pu}, {units:+.2f}u"
        if len(gs):
            line += f", ROI {units / len(gs) * 100:+.1f}%"
        if len(clvp):
            line += f", beat the close on {int((clvp > 0).sum())} of {len(clvp)} (mean {clvp.mean():+.2f} pts)"
        print(line)
    print("\nSmall samples mean nothing. Closing-line value says more than wins early on; "
          "a few hundred picks are needed before the W-L means much.")
    return 0


def main():
    args = [a for a in sys.argv[1:] if a]
    if args and args[0] == "add":
        return add(args[1:])
    grade()
    return report()


if __name__ == "__main__":
    sys.exit(main())
