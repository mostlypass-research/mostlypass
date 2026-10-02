"""Launch guarantees: fixture can't publish, close capture timing, grading incl. totals, validator, UTF-8."""
import datetime as dt
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_mode_cannot_publish():
    env = dict(os.environ, MP_FIXTURE="1")
    r = subprocess.run([sys.executable, "run_publish.py", "--fixture"], cwd=ROOT, capture_output=True, text=True, env=env)
    assert r.returncode == 2 and "REFUSED" in r.stdout


def test_assert_live_raises_in_fixture():
    code = "import os; os.environ['MP_FIXTURE']='1'\nfrom mp import config\ntry:\n config.assert_live('x')\nexcept SystemExit as e:\n print('BLOCKED', e)"
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    assert "BLOCKED" in r.stdout


def test_close_capture_plan():
    sys.path.insert(0, str(ROOT))
    import run_close
    cfg = {"final_window_min": 15, "safety_window_min": 45, "min_gap_min": 12}
    now = dt.datetime(2026, 10, 4, 16, 50, tzinfo=dt.timezone.utc)
    ev = [{"id": "a", "commence_time": "2026-10-04T17:00:00Z"},   # 10 min out -> final
          {"id": "b", "commence_time": "2026-10-04T17:25:00Z"},   # 35 min out, none yet -> safety
          {"id": "c", "commence_time": "2026-10-04T20:05:00Z"},   # far -> nothing
          {"id": "d", "commence_time": "2026-10-04T16:40:00Z"}]   # already started -> never
    empty = pd.DataFrame(columns=["event_id", "snapshot_ts"])
    assert run_close.plan(ev, empty, now, cfg) == {"a": "final", "b": "safety"}
    prior = pd.DataFrame([{"event_id": "a", "snapshot_ts": "2026-10-04T16:45:00Z"},
                          {"event_id": "b", "snapshot_ts": "2026-10-04T16:40:00Z"}])
    assert run_close.plan(ev, prior, now, cfg) == {}          # a captured 5 min ago; b has its safety capture


def test_result_logic_incl_totals():
    from mp.pipeline.grade import result_for
    assert result_for("h2h", "KC", "KC", None, 27, 17) == "win"
    assert result_for("spreads", "KC", "KC", -7.5, 27, 17) == "win"
    assert result_for("spreads", "LV", "KC", 7.5, 27, 17) == "loss"
    assert result_for("spreads", "KC", "KC", -10, 27, 17) == "push"
    assert result_for("totals", "Over", "KC", 43.5, 27, 17) == "win"
    assert result_for("totals", "Under", "KC", 44, 27, 17) == "push"


def test_validator_nested_summary_and_thresholds():
    from mp.pipeline import validate
    objs = [{"market_price": 135, "fair_price": -122, "fair_market_price": -110, "threshold_price": 101, "edge": 0.031,
             "model_prob": 0.55, "market_implied_prob": 0.4255, "fair_market_prob": 0.5238, "ev_per_unit": 0.29,
             "line": None, "model_spread_home": 1.7, "gap_points": None, "stake_units": 0.0, "exchange_prob": None}]
    summ = {"money": "PAPER", "bet": {"n": 0, "graded": 0, "wins": 0, "losses": 0, "pushes": 0, "units": 0.0},
            "lean": {"n": 7, "graded": 5, "wins": 3, "losses": 2, "pushes": 0, "n_clv": 5, "clv_mean": 0.012}}
    cfg = {"qualify": {"edge_threshold_bet": 0.03, "edge_threshold_lean": 0.015}}
    a = validate.allowed_from(objs, summ, cfg)
    assert validate.check("Bears ML +135, fair -122, edge 3.1%, LEAN 3-2-0, CLV +1.2%, bar 1.5%. 2026-10-04 21+", a) == []
    assert validate.check("Bears ML +140", a)
    assert validate.check("record 4-1-0", a)


def test_utf8_write_default():
    import mp  # noqa: installs the UTF-8 guard
    p = Path(tempfile.mkdtemp()) / "x.txt"
    p.write_text("— · ≥")
    assert p.read_bytes().decode("utf-8") == "— · ≥"


def test_grading_end_to_end_with_own_close():
    """Signal -> score (nflverse) -> close (own capture, last before kickoff) -> CLV; LEAN carries zero units."""
    from mp.pipeline import grade
    from mp.data import oddsapi
    d = Path(tempfile.mkdtemp())
    grade.SIGNALS, grade.GRADES, grade.EXCEPTIONS, oddsapi.CLOSES = d / "s.csv", d / "g.csv", d / "e.csv", d / "c.csv"
    kick = "2025-10-05T17:00:00Z"
    base = {"published_ts": "2025-10-05T13:00:00Z", "published_url": "u", "mode": "LIVE", "money": "PAPER", "sport": "NFL",
            "season": 2025, "week": 5, "game_id": "2025_05_LV_KC", "event_id": "e1", "commence_time": kick,
            "home": "Kansas City Chiefs", "away": "Las Vegas Raiders", "book": "draftkings", "fair_market_price": -110,
            "model_prob": 0.55, "fair_price": -122, "edge": 0.03, "threshold_price": -108, "model_version": "elo_v0",
            "backtest_gate": "closed"}
    rows = [dict(base, signal_id="s1", verdict="LEAN", market="spreads", selection="Kansas City Chiefs", line=-7.5, price=-110, stake_units=0.0),
            dict(base, signal_id="s2", verdict="BET", market="h2h", selection="Las Vegas Raiders", line=None, price=250, stake_units=0.5)]
    pd.DataFrame(rows).to_csv(grade.SIGNALS, index=False)
    closes = [  # two captures; the later one (5 min before) must win; one AFTER kickoff must be ignored
        {"snapshot_ts": "2025-10-05T16:20:00Z", "event_id": "e1", "commence_time": kick, "book": "pinnacle", "market": "spreads", "name": "Kansas City Chiefs", "price": -105, "point": -7.5, "minutes_to_kickoff": 40, "book_age_min": 1},
        {"snapshot_ts": "2025-10-05T16:55:00Z", "event_id": "e1", "commence_time": kick, "book": "pinnacle", "market": "spreads", "name": "Kansas City Chiefs", "price": -115, "point": -7.5, "minutes_to_kickoff": 5, "book_age_min": 1},
        {"snapshot_ts": "2025-10-05T16:55:00Z", "event_id": "e1", "commence_time": kick, "book": "pinnacle", "market": "h2h", "name": "Las Vegas Raiders", "price": 240, "point": None, "minutes_to_kickoff": 5, "book_age_min": 1},
        {"snapshot_ts": "2025-10-05T17:10:00Z", "event_id": "e1", "commence_time": kick, "book": "pinnacle", "market": "spreads", "name": "Kansas City Chiefs", "price": -300, "point": -3.5, "minutes_to_kickoff": -10, "book_age_min": 1}]
    pd.DataFrame(closes).to_csv(oddsapi.CLOSES, index=False)
    games = pd.DataFrame([{"game_id": "2025_05_LV_KC", "home_score": 27.0, "away_score": 17.0}])
    g = grade.grade({"close": {"safety_window_min": 45}, "odds": {"provider": "fixture"}}, games).set_index("signal_id")
    assert g.loc["s1", "result"] == "win" and g.loc["s1", "pl_units"] == 0.0          # LEAN: zero units
    assert g.loc["s1", "close_price"] == -115 and g.loc["s1", "close_min_before"] == 5
    assert abs(g.loc["s1", "clv_prob"] - (115 / 215 - 110 / 210)) < 1e-3              # beat the close
    assert g.loc["s2", "result"] == "loss" and g.loc["s2", "pl_units"] == -0.5
    assert g.loc["s2", "clv_prob"] > 0                                                 # took +250, closed +240
    s = grade.record_summary()
    assert s["money"] == "PAPER" and s["bet"]["units"] == -0.5 and s["lean"]["wins"] == 1
    assert grade.grade({"close": {"safety_window_min": 45}, "odds": {"provider": "fixture"}}, games).empty  # idempotent
