"""Walk-forward backtest of elo_v0 against nflverse closing lines (CC-BY-4.0).

The test every model must pass before it may emit a public BET:
  * sequential fit (no look-ahead), first N seasons are burn-in
  * benchmark = closing spread / moneyline from nflverse (book unknown, PFR-derived)
  * vig removed from closing moneylines before computing market probabilities
  * metrics: spread MAE vs close, ATS record when model disagrees with close by >= threshold,
    Brier score vs devigged close, calibration table, and a multiple-testing note
If model-vs-close ATS edge is not positive out of sample, qualify.py caps verdicts at LEAN.
"""
from __future__ import annotations
import json
import math
import pandas as pd
from mp.models.elo import Elo
from mp.pipeline.devig import american_to_prob, devig_two_way
from mp.config import MODEL_DIR


def run(games: pd.DataFrame, cfg: dict, burn_in: int = 3, start_season: int = 2010,
        end_season: int | None = None, thresholds=(1.0, 2.0, 3.0)) -> dict:
    elo = Elo.from_cfg(cfg)
    g = games.dropna(subset=["home_score", "away_score", "spread_line"]).copy()
    g = g[g["season"] >= start_season - burn_in]
    if end_season:
        g = g[g["season"] <= end_season]
    g = g.sort_values(["gameday", "game_id"])
    rows = []
    for r in g.itertuples(index=False):
        elo.new_season(int(r.season))
        neutral = getattr(r, "location", "Home") == "Neutral"
        if r.season >= start_season:
            model_spread = elo.expected_spread(r.home_team, r.away_team, neutral)  # home - away
            close_spread = float(r.spread_line)  # nflverse: positive = home favored by that many
            margin = float(r.home_score - r.away_score)
            p_model = elo.home_win_prob(r.home_team, r.away_team, neutral)
            p_close = None
            if pd.notna(getattr(r, "home_moneyline", None)) and pd.notna(getattr(r, "away_moneyline", None)):
                p_close, _ = devig_two_way(american_to_prob(r.home_moneyline), american_to_prob(r.away_moneyline))
            rows.append({"season": r.season, "week": r.week, "home": r.home_team, "away": r.away_team,
                         "model_spread": model_spread, "close_spread": close_spread, "margin": margin,
                         "p_model": p_model, "p_close": p_close,
                         "home_win": 1.0 if margin > 0 else (0.5 if margin == 0 else 0.0)})
        elo.update(r.home_team, r.away_team, float(r.home_score), float(r.away_score), neutral)
    df = pd.DataFrame(rows)
    out = {"model": elo.version, "seasons": [int(df.season.min()), int(df.season.max())], "n_games": len(df)}
    out["spread_mae_model"] = float((df.model_spread - df.margin).abs().mean())
    out["spread_mae_close"] = float((df.close_spread - df.margin).abs().mean())
    # ATS test: when model thinks home is better than close by >= t points, bet home ATS; else away
    ats = {}
    for t in thresholds:
        d = df[(df.model_spread - df.close_spread).abs() >= t].copy()
        side_home = d.model_spread > d.close_spread
        home_cover = (d.margin - d.close_spread) > 0
        push = (d.margin - d.close_spread) == 0
        win = (side_home & home_cover) | (~side_home & ~home_cover & ~push)
        n = int((~push).sum())
        w = int(win.sum())
        pct = w / n if n else float("nan")
        # 2-sided z test vs 50% (breakeven at -110 is 52.38%)
        z = (pct - 0.5) / math.sqrt(0.25 / n) if n else float("nan")
        ats[str(t)] = {"n": n, "wins": w, "pct": round(pct, 4) if n else None, "z_vs_50": round(z, 2) if n else None,
                       "roi_at_-110": round((w * (100 / 110) - (n - w)) / n, 4) if n else None}
    out["ats_by_threshold"] = ats
    dc = df.dropna(subset=["p_close"])
    out["brier_model"] = float(((dc.p_model - dc.home_win) ** 2).mean()) if len(dc) else None
    out["brier_close"] = float(((dc.p_close - dc.home_win) ** 2).mean()) if len(dc) else None
    # calibration deciles
    df["bin"] = (df.p_model * 10).clip(0, 9).astype(int)
    cal = df.groupby("bin").agg(n=("home_win", "size"), pred=("p_model", "mean"), actual=("home_win", "mean"))
    out["calibration"] = [{"bin": int(i), "n": int(r.n), "pred": round(float(r.pred), 3), "actual": round(float(r.actual), 3)}
                          for i, r in cal.iterrows()]
    out["multiple_testing_note"] = (f"{len(thresholds)} thresholds tested; Bonferroni alpha 0.05 -> per-test "
                                    f"alpha {0.05 / len(thresholds):.3f} (|z| >= {2.39 if len(thresholds)==3 else 2.0}).")
    # pass rule: best threshold must beat breakeven (52.38%) with |z| >= 2.39 AND positive ROI
    best = max((v for v in ats.values() if v["n"]), key=lambda v: v["roi_at_-110"] or -1, default=None)
    out["passes_bet_gate"] = bool(best and best["pct"] and best["pct"] > 0.5238 and best["z_vs_50"] >= 2.39)
    out["verdict"] = ("Model may emit BET-grade signals (edge vs close is statistically significant)."
                      if out["passes_bet_gate"] else
                      "Model does NOT beat the close out of sample: verdicts are capped at LEAN; publish as research.")
    (MODEL_DIR / "backtest_report.json").write_text(json.dumps(out, indent=1))
    df.to_csv(MODEL_DIR / "backtest_games.csv", index=False)
    return out
