"""The Odds API client on the FREE Starter tier (500 credits/month).

Costs (docs, verified 1 Oct 2026): /odds = markets x regions, where <=10 named bookmakers = 1 region;
/events = free; /scores = 1 (2 with daysFrom). Every response's x-requests-remaining / x-requests-last
headers are logged to database/odds_credits.csv so usage is auditable.
Raw snapshots go to data/raw (never committed). Closing snapshots go to database/closes.csv (append-only).
"""
from __future__ import annotations
import csv
import json
import datetime as dt
import pandas as pd
import requests
from mp.config import RAW_DIR, FIXTURE_DIR, DB_DIR

BASE = "https://api.the-odds-api.com/v4"
SNAP = RAW_DIR / "odds_snapshots.csv"
SCORES = RAW_DIR / "scores.csv"
CLOSES = DB_DIR / "closes.csv"
CREDITS = DB_DIR / "odds_credits.csv"              # morning/grade calls
CREDITS_CLOSE = DB_DIR / "odds_credits_close.csv"  # closing-capture job (separate file: no git conflicts)


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t: dt.datetime) -> str:
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def _log_credits(endpoint: str, r: requests.Response):
    row = {"ts": iso(now_utc()), "endpoint": endpoint, "remaining": r.headers.get("x-requests-remaining"),
           "used": r.headers.get("x-requests-used"), "last": r.headers.get("x-requests-last")}
    path = CREDITS_CLOSE if endpoint in ("odds:close", "events") else CREDITS
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)
    return row


def credits_remaining() -> int | None:
    if not CREDITS.exists():
        return None
    df = pd.read_csv(CREDITS).dropna(subset=["remaining"])
    return int(float(df.remaining.iloc[-1])) if len(df) else None


def _get(cfg: dict, path: str, params: dict, endpoint: str):
    key = cfg["secrets"]["odds_api_key"]
    if not key:
        raise RuntimeError("ODDS_API_KEY is not set. Run:  .\\mp setkey")
    r = requests.get(f"{BASE}{path}", params={"apiKey": key, **params}, timeout=30)
    if r.status_code == 401:
        raise RuntimeError("The Odds API rejected the key (401). Re-run  .\\mp setkey  and paste it again.")
    if r.status_code == 429:
        raise RuntimeError("The Odds API quota is exhausted or rate-limited (429). No paid upgrade: wait for the monthly reset.")
    r.raise_for_status()
    info = _log_credits(endpoint, r)
    return r.json(), info


def _flatten(payload: list, label: str, ts: str) -> pd.DataFrame:
    rows = []
    for ev in payload:
        for bk in ev.get("bookmakers", []):
            for mk in bk.get("markets", []):
                for oc in mk.get("outcomes", []):
                    rows.append({"snapshot_ts": ts, "label": label, "event_id": ev["id"],
                                 "commence_time": ev["commence_time"], "home_team": ev["home_team"],
                                 "away_team": ev["away_team"], "book": bk["key"], "book_ts": bk.get("last_update"),
                                 "market": mk["key"], "name": oc["name"], "price": oc["price"], "point": oc.get("point")})
    return pd.DataFrame(rows)


def fetch_odds(cfg: dict, bookmakers: str, label: str) -> tuple[pd.DataFrame, dict]:
    """Pre-game odds only: events that have already started are dropped (live odds would pollute everything)."""
    if cfg["odds"]["provider"] == "fixture":
        from mp.data.fixture import odds_payload
        payload, info = odds_payload(cfg["sport"]["season"]), {"remaining": "fixture", "last": "0"}
    else:
        payload, info = _get(cfg, f"/sports/{cfg['sport']['key']}/odds",
                             {"bookmakers": bookmakers, "markets": cfg["odds"]["markets"], "oddsFormat": "american"},
                             f"odds:{label}")
    ts = iso(now_utc())
    df = _flatten(payload, label, ts)
    if not df.empty:
        df = df[df.commence_time.map(parse) > now_utc()]
        df.to_csv(SNAP, mode="a", header=not SNAP.exists(), index=False)
    print(f"[oddsapi] {label}: {df.event_id.nunique() if len(df) else 0} upcoming games, {len(df)} prices, "
          f"credits used by this call: {info.get('last')}, remaining: {info.get('remaining')}")
    return df, info


def fetch_events(cfg: dict) -> list[dict]:
    """Current schedule (FREE endpoint). Used by closing capture so flexed/rescheduled games are honored."""
    if cfg["odds"]["provider"] == "fixture":
        from mp.data.fixture import odds_payload
        return [{k: e[k] for k in ("id", "commence_time", "home_team", "away_team")} for e in odds_payload(cfg["sport"]["season"])]
    payload, _ = _get(cfg, f"/sports/{cfg['sport']['key']}/events", {}, "events")
    return payload


def capture_close(cfg: dict, event_ids: list[str], reason: dict) -> int:
    """One Pinnacle-only call (3 credits) for the whole slate; keep rows for the target games; append-only."""
    if cfg["odds"]["provider"] == "fixture":
        from mp.data.fixture import odds_payload
        payload = odds_payload(cfg["sport"]["season"])
    else:
        payload, _ = _get(cfg, f"/sports/{cfg['sport']['key']}/odds",
                          {"bookmakers": cfg["odds"]["closing_book"], "markets": cfg["odds"]["markets"],
                           "oddsFormat": "american"}, "odds:close")
    ts = now_utc()
    df = _flatten(payload, "close", iso(ts))
    if df.empty:
        return 0
    df = df[df.event_id.isin(event_ids) & (df.book == cfg["odds"]["closing_book"])].copy()
    if df.empty:
        return 0
    df["minutes_to_kickoff"] = df.commence_time.map(lambda c: round((parse(c) - ts).total_seconds() / 60, 1))
    df["book_age_min"] = df.book_ts.map(lambda b: round((ts - parse(b)).total_seconds() / 60, 1) if isinstance(b, str) else None)
    df["capture_reason"] = df.event_id.map(reason)
    df = df[df.minutes_to_kickoff > 0]            # never record a price taken after kickoff
    df.to_csv(CLOSES, mode="a", header=not CLOSES.exists(), index=False)
    return int(df.event_id.nunique())


def closing_price(event_id: str, market: str, name: str, point: float | None, commence_time: str):
    """Last captured benchmark price strictly before kickoff for this exact market/side.
    Returns dict(price, point, snapshot_ts, minutes_to_kickoff, book_age_min) or None. Never interpolates."""
    if not CLOSES.exists():
        return None
    df = pd.read_csv(CLOSES)
    df = df[(df.event_id == event_id) & (df.market == market) & (df.name == name)]
    df = df[df.snapshot_ts.map(parse) < parse(commence_time)]
    if df.empty:
        return None
    df = df[df.snapshot_ts == df.snapshot_ts.max()]
    if market in ("spreads", "totals") and point is not None and len(df) > 1:
        df = df.iloc[(df.point - float(point)).abs().argsort()[:1]]
    r = df.iloc[0]
    return {"price": float(r.price), "point": (float(r.point) if pd.notna(r.point) else None), "snapshot_ts": r.snapshot_ts,
            "minutes_to_kickoff": float(r.minutes_to_kickoff), "book_age_min": r.get("book_age_min")}


def fetch_scores(cfg: dict, days_from: int = 3) -> pd.DataFrame:
    if cfg["odds"]["provider"] == "fixture":
        payload = []
    else:
        payload, _ = _get(cfg, f"/sports/{cfg['sport']['key']}/scores", {"daysFrom": days_from}, "scores")
    rows = []
    for ev in payload:
        if not ev.get("completed"):
            continue
        sc = {s["name"]: float(s["score"]) for s in (ev.get("scores") or [])}
        rows.append({"event_id": ev["id"], "commence_time": ev["commence_time"], "home_team": ev["home_team"],
                     "away_team": ev["away_team"], "home_score": sc.get(ev["home_team"]),
                     "away_score": sc.get(ev["away_team"]), "fetched_ts": iso(now_utc())})
    return pd.DataFrame(rows)
