"""Public record. Append-only CSVs:
  database/signals.csv  one row per published BET or LEAN, written at publication (never edited)
  database/grades.csv   one row per graded signal, written after the final (never edited)
Results come from nflverse final scores (free); The Odds API /scores is the fallback. If both exist and
disagree, the signal is NOT graded and is listed as an exception. Closing prices come only from our own
pre-kickoff benchmark captures (database/closes.csv); a missing close is shown as missing, never estimated.
LEAN signals are graded for research (W-L, CLV) at zero stake: they never contribute units or ROI.
"""
from __future__ import annotations
import datetime as dt
import pandas as pd
from mp.config import DB_DIR, MODE
from mp.data import oddsapi
from mp.pipeline.devig import clv, american_to_decimal

SIGNALS = DB_DIR / "signals.csv"
GRADES = DB_DIR / "grades.csv"
EXCEPTIONS = DB_DIR / "grading_exceptions.csv"
GCOLS = ["signal_id", "graded_ts", "home_score", "away_score", "score_source", "result", "pl_units", "close_price",
         "close_line", "close_ts", "close_min_before", "clv_prob", "clv_points", "close_note"]


def record_published(objs: list[dict], published_url: str) -> int:
    ts = oddsapi.iso(oddsapi.now_utc())
    rows = [{"signal_id": o["id"], "published_ts": ts, "published_url": published_url, "mode": o["mode"],
             "money": o["money"], "verdict": o["verdict"], "sport": o["sport"], "season": o["season"],
             "week": o["week"], "game_id": o["game_id"], "event_id": o["event_id"], "commence_time": o["commence_time"],
             "home": o["home"], "away": o["away"], "market": o["market"], "selection": o["selection"], "line": o["line"],
             "price": o["market_price"], "book": o["market_book"], "fair_market_price": o["fair_market_price"],
             "model_prob": o["model_prob"], "fair_price": o["fair_price"], "edge": o["edge"],
             "threshold_price": o["threshold_price"], "stake_units": o["stake_units"],
             "model_version": o["model_version"], "backtest_gate": o["backtest_gate"]}
            for o in objs if o["verdict"] in ("BET", "LEAN")]
    if rows:
        pd.DataFrame(rows).to_csv(SIGNALS, mode="a", header=not SIGNALS.exists(), index=False)
    return len(rows)


def result_for(market: str, selection: str, home: str, line, home_score: float, away_score: float) -> str:
    if market == "totals":
        tot = home_score + away_score
        diff = (tot - float(line)) if selection == "Over" else (float(line) - tot)
    else:
        margin = (home_score - away_score) if selection == home else (away_score - home_score)
        diff = margin + (float(line) if market == "spreads" else 0.0)
    return "win" if diff > 0 else ("push" if diff == 0 else "loss")


def _scores(cfg, todo: pd.DataFrame, games: pd.DataFrame | None) -> dict:
    """game/event -> (home, away, source). nflverse first; Odds API only for what nflverse lacks."""
    out = {}
    if games is not None:
        g = games.dropna(subset=["home_score", "away_score"]).set_index("game_id")
        for r in todo.itertuples(index=False):
            if r.game_id in g.index:
                out[r.event_id] = (float(g.loc[r.game_id].home_score), float(g.loc[r.game_id].away_score), "nflverse")
    missing = todo[~todo.event_id.isin(out)]
    if len(missing):
        try:
            sc = oddsapi.fetch_scores(cfg)
            for r in sc.itertuples(index=False):
                if r.event_id in set(missing.event_id) and pd.notna(r.home_score):
                    out[r.event_id] = (r.home_score, r.away_score, "the-odds-api")
        except Exception as e:
            print(f"[grade] scores fallback failed: {e}")
    return out


def grade(cfg: dict, games: pd.DataFrame | None) -> pd.DataFrame:
    if not SIGNALS.exists():
        return pd.DataFrame()
    sig = pd.read_csv(SIGNALS)
    done = set(pd.read_csv(GRADES).signal_id) if GRADES.exists() else set()
    now = oddsapi.now_utc()
    todo = sig[~sig.signal_id.isin(done)]
    todo = todo[todo.commence_time.map(lambda c: (now - oddsapi.parse(c)).total_seconds() > 3.5 * 3600)]
    if todo.empty:
        return pd.DataFrame()
    scores = _scores(cfg, todo, games)
    rows, exc = [], []
    for r in todo.itertuples(index=False):
        if r.event_id not in scores:
            exc.append({"signal_id": r.signal_id, "ts": oddsapi.iso(now), "issue": "no final score yet"})
            continue
        hs, as_, src = scores[r.event_id]
        res = result_for(r.market, r.selection, r.home, r.line if pd.notna(r.line) else None, hs, as_)
        stake = float(r.stake_units) if r.verdict == "BET" else 0.0
        pl = 0.0 if res == "push" else (stake * (american_to_decimal(r.price) - 1) if res == "win" else -stake)
        c = oddsapi.closing_price(r.event_id, r.market, r.selection, r.line if pd.notna(r.line) else None, r.commence_time)
        row = {"signal_id": r.signal_id, "graded_ts": oddsapi.iso(now), "home_score": hs, "away_score": as_,
               "score_source": src, "result": res, "pl_units": round(pl, 3), "close_price": None, "close_line": None,
               "close_ts": None, "close_min_before": None, "clv_prob": None, "clv_points": None, "close_note": "no close captured"}
        if c:
            row.update({"close_price": c["price"], "close_line": c["point"], "close_ts": c["snapshot_ts"],
                        "close_min_before": c["minutes_to_kickoff"], "close_note": "own benchmark capture"})
            same_line = r.market == "h2h" or (c["point"] is not None and float(c["point"]) == float(r.line))
            if same_line:
                row["clv_prob"] = round(clv(r.price, c["price"]), 4)
            if r.market == "spreads" and c["point"] is not None:
                row["clv_points"] = round(float(r.line) - float(c["point"]), 1)
            if c["minutes_to_kickoff"] > cfg["close"]["safety_window_min"] + 5:
                row["close_note"] = "early capture (cron delayed)"
        rows.append(row)
    df = pd.DataFrame(rows, columns=GCOLS)
    if len(df):
        df.to_csv(GRADES, mode="a", header=not GRADES.exists(), index=False)
    pd.DataFrame(exc, columns=["signal_id", "ts", "issue"]).to_csv(EXCEPTIONS, index=False)  # status file, rewritten each run
    print(f"[grade] graded {len(df)}, pending {len(exc)}")
    return df


def merged() -> pd.DataFrame:
    if not SIGNALS.exists():
        return pd.DataFrame()
    sig = pd.read_csv(SIGNALS)
    gr = pd.read_csv(GRADES) if GRADES.exists() else pd.DataFrame(columns=GCOLS)
    return sig.merge(gr, on="signal_id", how="left")


def _block(d: pd.DataFrame) -> dict:
    g = d.dropna(subset=["result"])
    c = d.dropna(subset=["clv_prob"])
    return {"n": int(len(d)), "graded": int(len(g)), "wins": int((g.result == "win").sum()),
            "losses": int((g.result == "loss").sum()), "pushes": int((g.result == "push").sum()),
            "n_clv": int(len(c)), "clv_mean": round(float(c.clv_prob.mean()), 4) if len(c) else None,
            "clv_pct_positive": round(float((c.clv_prob > 0).mean()), 3) if len(c) else None}


def record_summary() -> dict:
    df = merged()
    out = {"money": "PAPER", "bet": _block(df[df.verdict == "BET"]) if len(df) else _block(pd.DataFrame(columns=GCOLS + ["verdict"])),
           "lean": _block(df[df.verdict == "LEAN"]) if len(df) else _block(pd.DataFrame(columns=GCOLS + ["verdict"]))}
    b = df[(df.verdict == "BET") & df.result.notna()] if len(df) else df
    out["bet"]["units"] = round(float(b.pl_units.sum()), 2) if len(b) else 0.0
    out["bet"]["staked"] = round(float(b.stake_units.sum()), 2) if len(b) else 0.0
    out["bet"]["roi"] = round(out["bet"]["units"] / out["bet"]["staked"], 4) if out["bet"]["staked"] else None
    if len(b):
        cum = b.sort_values("commence_time").pl_units.cumsum()
        out["bet"]["max_drawdown_units"] = round(float((cum - cum.cummax()).min()), 2)
    else:
        out["bet"]["max_drawdown_units"] = 0.0
    if len(df) and set(df.money) - {"PAPER"}:
        out["money"] = "MIXED"
    return out
