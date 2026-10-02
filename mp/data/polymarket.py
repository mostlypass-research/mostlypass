"""Polymarket public API (no key). DISPLAY ONLY: never used in verdicts, never linked.

Gamma: https://gamma-api.polymarket.com. A price is shown only if (a) the market is a game moneyline,
(b) both team names match exactly one market, and (c) it is within `max_gap_vs_pinnacle` of
Pinnacle's devigged probability. Anything else is dropped (fail-soft: the card never depends on it).
"""
from __future__ import annotations
import json
import datetime as dt
import pandas as pd
import requests
from mp.config import RAW_DIR, FIXTURE_DIR

GAMMA = "https://gamma-api.polymarket.com"
OUT = RAW_DIR / "polymarket_snapshots.csv"
_NOT_ML = ("spread", "o/u", "over", "under", "total", "1h", "first half", "quarter", "points", "yards", "mvp", "win the")


def fetch_nfl_moneylines(cfg: dict) -> pd.DataFrame:
    if cfg["odds"]["provider"] == "fixture":
        from mp.data.fixture import odds_payload, polymarket_payload
        payload = polymarket_payload(odds_payload(cfg["sport"]["season"]))
    else:
        r = requests.get(f"{GAMMA}/events", params={"closed": "false", "active": "true", "limit": 200,
                                                     "tag_slug": "nfl"}, timeout=30)
        r.raise_for_status()
        payload = [m for ev in r.json() for m in ev.get("markets", [])]
    rows, ts = [], dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    for m in payload:
        q = (m.get("question") or "")
        mtype = (m.get("sportsMarketType") or "").lower()
        if mtype and mtype != "moneyline":
            continue
        if not mtype and any(w in q.lower() for w in _NOT_ML):
            continue
        outcomes, prices = m.get("outcomes"), m.get("outcomePrices")
        outcomes = json.loads(outcomes) if isinstance(outcomes, str) else outcomes
        prices = json.loads(prices) if isinstance(prices, str) else prices
        if not outcomes or not prices or len(outcomes) != 2 or len(prices) != 2:
            continue
        for name, p in zip(outcomes, prices):
            rows.append({"snapshot_ts": ts, "question": q, "slug": m.get("slug"), "outcome": name, "prob": float(p),
                         "volume": m.get("volumeNum") or m.get("volume")})
    df = pd.DataFrame(rows)
    if not df.empty:
        df.to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
    print(f"[polymarket] {df.slug.nunique() if len(df) else 0} NFL moneyline markets")
    return df


def match_team_prob(df: pd.DataFrame | None, team: str, opp: str, pinnacle_fair: float, max_gap: float) -> float | None:
    if df is None or df.empty:
        return None
    t, o = team.split()[-1], opp.split()[-1]          # nickname: "49ers", "Chiefs"
    m = df[df.question.str.contains(t, regex=False) & df.question.str.contains(o, regex=False)]
    if m.slug.nunique() != 1:
        return None                                    # zero or ambiguous: show nothing rather than guess
    row = m[m.outcome.str.contains(t, regex=False)]
    if len(row) != 1:
        return None
    p = float(row.prob.iloc[0])
    if not (0.02 <= p <= 0.98) or abs(p - pinnacle_fair) > max_gap:
        return None
    return p
