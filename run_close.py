#!/usr/bin/env python3
"""Closing-line capture. Runs every 10 minutes (GitHub Actions). Reads the CURRENT schedule from The Odds API
/events endpoint (free), so Thursday, Saturday, international, holiday, flexed and rescheduled games are all
handled the same way: by their actual kickoff time.

Rule per game (minutes to kickoff = m):
  0 < m <= final_window  and no capture in the last min_gap minutes -> capture ("final")
  0 < m <= safety_window and no capture yet                          -> capture ("safety", in case the cron is late)
One Pinnacle-only call (3 credits) covers every game that needs it. Rows are appended, never overwritten.
Grading uses the LAST capture before kickoff and prints how many minutes before kickoff it was taken."""
import os
import sys
if "--fixture" in sys.argv:
    os.environ["MP_FIXTURE"] = "1"

import datetime as dt
import pandas as pd
from mp import config
from mp.data import oddsapi


def plan(events: list[dict], closes: pd.DataFrame, now: dt.datetime, c: dict) -> dict:
    need = {}
    for e in events:
        m = (oddsapi.parse(e["commence_time"]) - now).total_seconds() / 60
        if m <= 0 or m > c["safety_window_min"]:
            continue
        prev = closes[closes.event_id == e["id"]] if len(closes) else closes
        last = max((oddsapi.parse(t) for t in prev.snapshot_ts), default=None) if len(prev) else None
        if m <= c["final_window_min"]:
            if last is None or (now - last).total_seconds() / 60 >= c["min_gap_min"]:
                need[e["id"]] = "final"
        elif last is None:
            need[e["id"]] = "safety"
    return need


def main():
    cfg = config.load()
    events = oddsapi.fetch_events(cfg)
    closes = pd.read_csv(oddsapi.CLOSES) if oddsapi.CLOSES.exists() else pd.DataFrame(columns=["event_id", "snapshot_ts"])
    need = plan(events, closes, oddsapi.now_utc(), cfg["close"])
    if not need:
        print("[close] no game inside the capture window; 0 credits used")
        return 0
    n = oddsapi.capture_close(cfg, list(need), need)
    print(f"[close] captured {cfg['odds']['closing_book']} for {n} game(s): {need}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
