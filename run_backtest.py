#!/usr/bin/env python3
"""Walk-forward backtest of the model against nflverse closing lines. Writes models/backtest_report.json.
The daily pipeline reads `passes_bet_gate` from that file; if False, no BETs are ever emitted."""
from __future__ import annotations
import json
import sys
from mp import config
from mp.data import nflverse
from mp.models import backtest


def main():
    cfg = config.load()
    games = nflverse.load_games()
    rep = backtest.run(games, cfg, start_season=2010, end_season=cfg["sport"]["season"] - 1)
    print(json.dumps({k: v for k, v in rep.items() if k != "calibration"}, indent=1))
    print("calibration:", rep["calibration"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
