"""One research object per game-market-side, built only from data + deterministic math. Append-only store.

Verdict rules (in order; any failure can only LOWER a verdict, never raise it):
  edge >= bet threshold -> BET; >= lean threshold -> LEAN; else PASS
  model vs Pinnacle-fair gap > sanity bound -> PASS + model warning (model is likely missing information)
  any data warning, or backtest gate closed -> BET becomes LEAN
  more than max_bets_per_day BETs -> lowest-edge extras become LEAN
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import pandas as pd
from mp.config import DB_DIR, MODE
from mp.pipeline.devig import (american_to_prob, devig_two_way, prob_to_american, edge, ev_per_unit,
                               kelly, threshold_price)
from mp.models.elo import Elo
from mp.data.polymarket import match_team_prob

RO_PATH = DB_DIR / "research_objects.jsonl"


def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _oid(*parts):
    return hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12]


def benchmark_fair(ev: pd.DataFrame, market: str, book: str):
    """Devigged two-way probabilities from the benchmark book's main line for one event/market."""
    d = ev[(ev.market == market) & (ev.book == book)]
    if d.empty:
        return None
    if market == "h2h":
        probs = {r.name: american_to_prob(r.price) for r in d.itertuples()}
        if len(probs) != 2:
            return None
        k = list(probs)
        q = devig_two_way(probs[k[0]], probs[k[1]])
        return {"lines": {k[0]: None, k[1]: None}, "fair": {k[0]: q[0], k[1]: q[1]}, "book_ts": d.book_ts.max()}
    d = d.assign(abs_point=d.point.abs())
    best = None
    for ap, dd in d.groupby("abs_point"):
        if len(dd) != 2 or dd.name.nunique() != 2:
            continue
        probs = {r.name: american_to_prob(r.price) for r in dd.itertuples()}
        k = list(probs)
        q = devig_two_way(probs[k[0]], probs[k[1]])
        cand = {"lines": {r.name: float(r.point) for r in dd.itertuples()}, "fair": {k[0]: q[0], k[1]: q[1]},
                "book_ts": dd.book_ts.max()}
        if best is None or abs(q[0] - 0.5) < abs(list(best["fair"].values())[0] - 0.5):
            best = cand
    return best


def best_price(ev, market, sel, line, books):
    d = ev[(ev.market == market) & (ev.name == sel) & ev.book.isin(books)]
    if line is not None:
        d = d[d.point == line]
    if d.empty:
        return None, None
    r = d.sort_values("price", ascending=False).iloc[0]   # higher American price = better for the bettor
    return float(r.price), r.book


def build(cfg: dict, snap: pd.DataFrame, matched: pd.DataFrame, elo: Elo, poly, warnings: list[str],
          backtest_pass: bool) -> tuple[list[dict], list[str]]:
    q, o = cfg["qualify"], cfg["odds"]
    bench = o["closing_book"]
    ts = _now()
    model_warnings: list[str] = []
    mm = matched.dropna(subset=["game_id"])
    if mm.empty:
        return [], ["no Odds API events matched the nflverse schedule"]
    week = int(mm.week.min())
    keep = mm[mm.week == week].set_index("event_id")
    objs = []
    for event_id, ev in snap[snap.event_id.isin(keep.index)].groupby("event_id"):
        info = keep.loc[event_id]
        home, away = ev.home_team.iloc[0], ev.away_team.iloc[0]
        h, a = info.home_abbr, info.away_abbr
        commence = ev.commence_time.iloc[0]
        mu = elo.expected_spread(h, a)
        p_home = elo.home_win_prob(h, a)
        for market in ("h2h", "spreads"):
            fair = benchmark_fair(ev, market, bench)
            if not fair:
                warnings.append(f"{away} @ {home}: no {bench} {market} line")
                continue
            for sel in (home, away):
                line = fair["lines"].get(sel)
                if market == "h2h":
                    p_model = p_home if sel == home else 1 - p_home
                else:
                    p_model = elo.cover_prob(h, a, line) if sel == home else 1 - elo.cover_prob(h, a, -line)
                price, book = best_price(ev, market, sel, line, o["best_price_books"])
                if price is None:
                    continue
                fair_p = fair["fair"][sel]
                e = edge(p_model, price)
                verdict = "BET" if e >= q["edge_threshold_bet"] else ("LEAN" if e >= q["edge_threshold_lean"] else "PASS")
                flags = []
                if abs(p_model - fair_p) > q["sanity_max_gap"]:
                    if verdict != "PASS" and market == "spreads":
                        model_warnings.append(f"{sel} {line:+g}: model {p_model:.0%} vs market {fair_p:.0%}; gap too large, likely missing info (QB/injury); forced PASS")
                    verdict, flags = "PASS", ["sanity_gap"]
                if market not in q.get("signal_markets", ["spreads"]) and verdict != "PASS":
                    # The model was backtested against the SPREAD only. Its moneyline conversion is untested,
                    # so moneyline disagreements are displayed as research but never become signals.
                    verdict, flags = "PASS", flags + ["market_not_validated"]
                if verdict == "BET" and (warnings or (q["require_backtest_pass"] and not backtest_pass)):
                    verdict = "LEAN"
                home_line = fair["lines"].get(home)
                objs.append({
                    "id": _oid(event_id, market, sel, ts), "created_ts": ts, "mode": MODE, "money": q["money"],
                    "sport": cfg["sport"]["short"], "season": cfg["sport"]["season"], "week": week,
                    "game_id": info.game_id, "event_id": event_id, "commence_time": commence,
                    "home": home, "away": away, "market": market, "selection": sel, "line": line,
                    "market_price": int(price), "market_book": book,
                    "market_implied_prob": round(american_to_prob(price), 4),
                    "benchmark_book": bench, "benchmark_ts": fair["book_ts"],
                    "fair_market_prob": round(fair_p, 4), "fair_market_price": prob_to_american(fair_p),
                    "model_prob": round(p_model, 4), "fair_price": prob_to_american(p_model),
                    "model_spread_home": round(mu, 1),
                    "gap_points": round(home_line + mu, 1) if (market == "spreads" and home_line is not None) else None,
                    "edge": round(e, 4), "ev_per_unit": round(ev_per_unit(p_model, price), 4),
                    "threshold_price": threshold_price(p_model, q["edge_threshold_bet"]),
                    "verdict": verdict, "stake_units": 0.0, "exchange_prob": None, "flags": flags,
                    "model_version": elo.version, "backtest_gate": "open" if backtest_pass else "closed",
                })
                if market == "h2h":
                    objs[-1]["exchange_prob"] = match_team_prob(poly, sel, away if sel == home else home, fair_p,
                                                                cfg["exchange"]["max_gap_vs_pinnacle"])
    bets = sorted([x for x in objs if x["verdict"] == "BET"], key=lambda x: -x["edge"])
    for x in bets[q["max_bets_per_day"]:]:
        x["verdict"] = "LEAN"
    for x in objs:
        if x["verdict"] == "BET":
            x["stake_units"] = round(kelly(x["model_prob"], x["market_price"], q["kelly_fraction"], q["max_stake_units"]), 2)
    return objs, model_warnings


def append(objs: list[dict]):
    with open(RO_PATH, "a", encoding="utf-8") as f:
        for o in objs:
            f.write(json.dumps(o, default=str) + "\n")
