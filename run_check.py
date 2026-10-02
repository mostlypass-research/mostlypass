#!/usr/bin/env python3
"""One-command health check (.\\mp check). Runs everything that does not need an API key:
environment, unit tests, real nflverse data integrity, backtest reproduction + leakage sanity,
a full fixture run, and proof that fixture output cannot be published. Paste the CHECK SUMMARY to Claude."""
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
results = []


def step(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def run(args):
    env = dict(os.environ, PYTHONUTF8="1")
    env.pop("MP_FIXTURE", None)
    return subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)


def main():
    print("=== CHECK: environment ===")
    import pandas, numpy, matplotlib, requests, yaml, markdown, PIL  # noqa
    try:
        import tzdata  # noqa  (Windows needs this for time zones)
        tz = True
    except ImportError:
        tz = platform.system() != "Windows"
    step("python + packages", sys.version_info >= (3, 10) and tz,
         f"Python {platform.python_version()} on {platform.system()} {platform.release()}; pandas {pandas.__version__}")
    import shutil
    step("ffmpeg (optional, for Shorts)", True, "found" if shutil.which("ffmpeg") else "not installed - Shorts will be skipped locally (fine)")

    print("\n=== CHECK: unit tests ===")
    t = run(["tests/run.py"])
    print(t.stdout[-1500:])
    last = [l for l in t.stdout.splitlines() if "passed" in l]
    step("unit tests", t.returncode == 0, last[-1] if last else t.stderr[-300:])

    print("\n=== CHECK: nflverse real data ===")
    from mp import config
    cfg = config.load()
    from mp.data import nflverse
    games = nflverse.load_games()
    rep = nflverse.integrity_report(games, cfg["sport"]["season"])
    for k, v in rep.items():
        print(f"  {k}: {v}")
    ok = (rep["duplicate_game_ids"] == 0 and rep["teams_recent"] == 32 and not rep["teams_not_in_map"]
          and rep["future_games_with_scores"] == 0 and rep["team_same_day_duplicates"] == 0
          and rep["spread_line_coverage_played"] > 0.99)
    step("nflverse integrity", ok, f"{rep['rows']} games {rep['seasons']}; next: Week {rep.get('next_week')} ({rep.get('next_week_games')} games, {rep.get('next_week_dates')})")

    print("\n=== CHECK: backtest (walk-forward vs closing lines) ===")
    from mp.models import backtest
    bt = backtest.run(games, cfg, start_season=2010, end_season=cfg["sport"]["season"] - 1)
    for k, v in bt["ats_by_threshold"].items():
        print(f"  gap >= {k} pts: n={v['n']}  ATS {v['pct']:.1%}  z={v['z_vs_50']}  ROI@-110 {v['roi_at_-110']:+.1%}")
    print(f"  spread MAE model {bt['spread_mae_model']:.2f} vs close {bt['spread_mae_close']:.2f}; Brier model {bt['brier_model']:.4f} vs close {bt['brier_close']:.4f}")
    step("backtest reproduced", bt["n_games"] > 4000, f"{bt['n_games']} games {bt['seasons'][0]}-{bt['seasons'][1]}")
    step("no look-ahead signature", bt["spread_mae_model"] > bt["spread_mae_close"],
         "model is less accurate than the closing line, as an honest pre-game model should be")
    step("BET gate", True, "OPEN (model earned BETs)" if bt["passes_bet_gate"] else "CLOSED: model has not beaten the close, so no BETs")

    print("\n=== CHECK: fixture run (offline test data, sandboxed) ===")
    def prod_state():
        files = list((ROOT / "database").glob("*")) + list((ROOT / "content" / "out").glob("*/*")) + list((ROOT / "site" / "public").rglob("*"))
        return sorted((str(x), x.stat().st_mtime) for x in files if x.is_file())
    before = prod_state()
    f = run(["run_daily.py", "--fixture"])
    print(f.stdout[-2500:])
    sb = ROOT / "sandbox" / "content" / "out"
    made = sorted(sb.glob("*/APPROVAL.txt"))
    files = sorted(p.name for p in made[-1].parent.iterdir()) if made else []
    step("fixture pipeline", f.returncode == 0 and bool(made), ", ".join(files) if files else f.stderr[-400:])
    step("fixture output sandboxed", prod_state() == before, "written only to sandbox/; production folders unchanged")
    p = run(["run_publish.py", "--fixture"])
    step("fixture publication blocked", p.returncode == 2 and "REFUSED" in p.stdout, p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:])

    print("\n=== CHECK SUMMARY (paste everything from here down to Claude) ===")
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")
    bad = [r for r in results if not r[1]]
    print("RESULT:", "ALL CHECKS PASSED" if not bad else f"{len(bad)} CHECK(S) FAILED")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
