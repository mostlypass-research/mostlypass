"""Synthetic TEST payloads, built from the real upcoming nflverse week so team matching works.
Prices are derived from nflverse's posted spread with fixed, plausible vig. Event ids start with "fx" so
run_publish refuses them even if every other guard failed. Used only when MP_FIXTURE=1."""
from __future__ import annotations
import datetime as dt
import math
import pandas as pd
from mp.data.nflverse import ABBR_TO_NAME, load_games
from mp.pipeline.devig import prob_to_american

SHIFT = {"pinnacle": 0.0, "draftkings": 0.5, "fanduel": -0.5, "betmgm": 0.0}
VIG = {"pinnacle": 0.025, "draftkings": 0.045, "fanduel": 0.045, "betmgm": 0.05}


def _iso(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ml(p_home, vig):
    return prob_to_american(min(p_home * (1 + vig / 2), 0.97)), prob_to_american(min((1 - p_home) * (1 + vig / 2), 0.97))


def _phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def odds_payload(season: int) -> list[dict]:
    g = load_games()
    up = g[(g.season == season) & g.home_score.isna()].sort_values(["gameday", "gametime"])
    if up.empty:
        return []
    wk = up.week.iloc[0]
    up = up[up.week == wk]
    now = dt.datetime.now(dt.timezone.utc)
    out = []
    for i, r in enumerate(up.itertuples()):
        kick = pd.Timestamp(f"{r.gameday.date()} {r.gametime or '13:00'}", tz="America/New_York").tz_convert("UTC").to_pydatetime()
        if kick <= now + dt.timedelta(hours=2):
            kick = now + dt.timedelta(hours=24 + i)
        hs = -(float(r.spread_line) if pd.notna(r.spread_line) else 2.0)     # home spread (negative = favorite)
        tot = float(r.total_line) if pd.notna(r.total_line) else 44.5
        p_home = _phi(-hs / 13.5)
        books = []
        for bk in ("pinnacle", "draftkings", "fanduel", "betmgm"):
            h_ml, a_ml = _ml(p_home, VIG[bk])
            juice = -105 if bk == "pinnacle" else -110
            pt = hs + SHIFT[bk]
            books.append({"key": bk, "title": bk, "last_update": _iso(now), "markets": [
                {"key": "h2h", "outcomes": [{"name": ABBR_TO_NAME[r.home_team], "price": h_ml}, {"name": ABBR_TO_NAME[r.away_team], "price": a_ml}]},
                {"key": "spreads", "outcomes": [{"name": ABBR_TO_NAME[r.home_team], "price": juice, "point": pt},
                                                {"name": ABBR_TO_NAME[r.away_team], "price": juice, "point": -pt}]},
                {"key": "totals", "outcomes": [{"name": "Over", "price": juice, "point": tot}, {"name": "Under", "price": juice, "point": tot}]}]})
        out.append({"id": f"fx{r.game_id}", "sport_key": "americanfootball_nfl", "commence_time": _iso(kick),
                    "home_team": ABBR_TO_NAME[r.home_team], "away_team": ABBR_TO_NAME[r.away_team], "bookmakers": books})
    return out


def polymarket_payload(odds: list[dict]) -> list[dict]:
    out = []
    for e in odds[:3]:
        pin = next(b for b in e["bookmakers"] if b["key"] == "pinnacle")
        h = next(m for m in pin["markets"] if m["key"] == "h2h")["outcomes"]
        from mp.pipeline.devig import american_to_prob, devig_two_way
        ph, _ = devig_two_way(american_to_prob(h[0]["price"]), american_to_prob(h[1]["price"]))
        hn, an = e["home_team"].split()[-1], e["away_team"].split()[-1]
        out.append({"question": f"{an} vs. {hn}", "slug": f"fx-{an}-{hn}".lower(), "sportsMarketType": "moneyline",
                    "outcomes": f'["{an}","{hn}"]', "outcomePrices": f'["{1 - ph + 0.01:.3f}","{ph - 0.01:.3f}"]', "volumeNum": 1000})
    return out
