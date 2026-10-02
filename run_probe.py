#!/usr/bin/env python3
"""Live odds probe (.\\mp odds): one morning-style call (expected cost 3 credits). Verifies the slate, the books,
Pinnacle on every market, timestamps and credits. Paste the PROBE SUMMARY to Claude."""
import sys
from zoneinfo import ZoneInfo
import pandas as pd
from mp import config
from mp.data import oddsapi, nflverse


def main():
    cfg = config.load()
    if cfg["mode"] != "LIVE":
        print("probe runs in LIVE mode only"); return 1
    snap, info = oddsapi.fetch_odds(cfg, cfg["odds"]["morning_bookmakers"], "probe")
    if snap.empty:
        print("PROBE: no upcoming games returned"); return 1
    games = nflverse.load_games()
    ev = snap[["event_id", "home_team", "away_team", "commence_time"]].drop_duplicates("event_id")
    m = nflverse.match_events(games, ev, cfg["sport"]["season"]).set_index("event_id")
    et = ZoneInfo("America/New_York")
    bench = cfg["odds"]["closing_book"]
    print(f"\n{'kickoff (ET)':<17}{'game':<28}{'wk':>3} {'books':>5}  pinnacle: ML / spread / total   (age min)")
    full, full_cur, cur_n = 0, 0, 0
    cur_wk = int(m.week.dropna().min()) if m.week.notna().any() else None
    for e in ev.sort_values("commence_time").itertuples():
        d = snap[snap.event_id == e.event_id]
        p = d[d.book == bench]
        has = {mk: (mk in set(p.market)) for mk in ("h2h", "spreads", "totals")}
        full += all(has.values())
        if e.event_id in m.index and m.loc[e.event_id].week == cur_wk:
            cur_n += 1
            full_cur += all(has.values())
        def g(mk, nm):
            r = p[(p.market == mk) & (p.name == nm)]
            if r.empty:
                return "--"
            r = r.iloc[0]
            return (f"{r.point:+g} {int(r.price):+d}" if mk == "spreads" else f"{r.point:g} {int(r.price):+d}") if mk != "h2h" else f"{int(r.price):+d}"
        age = (oddsapi.now_utc() - oddsapi.parse(p.book_ts.max())).total_seconds() / 60 if len(p) else float("nan")
        k = oddsapi.parse(e.commence_time).astimezone(et).strftime("%a %m-%d %H:%M")
        wk = m.loc[e.event_id].week if e.event_id in m.index and pd.notna(m.loc[e.event_id].week) else "?"
        name = f"{e.away_team.split()[-1]} @ {e.home_team.split()[-1]}"
        print(f"{k:<17}{name:<28}{str(wk):>3} {d.book.nunique():>5}  {g('h2h', e.home_team):>6} / {g('spreads', e.home_team):>11} / {g('totals', 'Over'):>11}   ({age:.0f})")
    books = sorted(snap.book.unique())
    n = ev.shape[0]
    print("\n=== PROBE SUMMARY (paste from here down to Claude) ===")
    print(f"upcoming games: {n}; nflverse matched: {int(m.game_id.notna().sum())}/{n}")
    print(f"books returned ({len(books)}): {', '.join(books)}")
    print(f"pinnacle present with ML+spread+total: {full}/{n} games")
    print(f"markets: {', '.join(sorted(snap.market.unique()))}")
    print(f"credits used by this call: {info.get('last')}; credits remaining: {info.get('remaining')}")
    print(f"current week (Week {cur_wk}): pinnacle complete on {full_cur}/{cur_n} games; later weeks are look-ahead lines and do not affect the card")
    print("PINNACLE BENCHMARK (current week):", "VERIFIED" if cur_n and full_cur == cur_n else ("PARTIAL - send to Claude" if full_cur else "MISSING - STOP"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
