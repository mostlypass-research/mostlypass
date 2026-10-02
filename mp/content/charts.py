"""Charts with matplotlib (free). Brand style: grey first, one accent."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ACCENT = "#2563eb"
GREY = "#9ca3af"
INK = "#111827"


def _style(ax, title):
    ax.set_title(title, loc="left", fontsize=13, color=INK, pad=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e5e7eb", linewidth=0.8)
    ax.tick_params(colors="#4b5563")


def line_history(snaps: pd.DataFrame, event_id: str, book: str, selection: str, model_line: float | None,
                 out: Path, title: str) -> Path | None:
    d = snaps[(snaps.event_id == event_id) & (snaps.book == book) & (snaps.market == "spreads") & (snaps.name == selection)]
    if d.empty:
        return None
    d = d.sort_values("snapshot_ts")
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
    ax.plot(pd.to_datetime(d.snapshot_ts), d.point, color=ACCENT, linewidth=2.2, marker="o")
    if model_line is not None:
        ax.axhline(model_line, color=GREY, linestyle="--", linewidth=1.5)
        ax.text(ax.get_xlim()[1], model_line, f"  model {model_line:+.1f}", va="center", color="#4b5563", fontsize=9)
    _style(ax, title)
    ax.set_ylabel("spread")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def equity_curve(df: pd.DataFrame, out: Path, title: str) -> Path | None:
    """Cumulative paper units for BET rows only. LEAN rows carry zero stake and never appear here."""
    if df is None or df.empty or "pl_units" not in df:
        return None
    d = df[(df.verdict == "BET")].dropna(subset=["pl_units"]).sort_values("commence_time")
    if d.empty:
        return None
    cum = d.pl_units.cumsum().values
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
    ax.plot(range(1, len(cum) + 1), cum, color=ACCENT, linewidth=2.2)
    ax.axhline(0, color=GREY, linewidth=1)
    _style(ax, title)
    ax.set_xlabel("paper bets")
    ax.set_ylabel("units (paper)")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def card_chart(objs: list[dict], out: Path, title: str, test: bool = False) -> Path:
    """Model spread vs Pinnacle spread for every game on the card (home perspective)."""
    rows, lean_games = {}, {o["event_id"] for o in objs if o["market"] == "spreads" and o["verdict"] in ("LEAN", "BET")}
    for o in sorted(objs, key=lambda o: o["commence_time"]):
        if o["market"] == "spreads" and o["selection"] == o["home"]:
            rows[f"{o['away'].split()[-1]} @ {o['home'].split()[-1]}"] = (o["line"], -o["model_spread_home"],
                                                                           "LEAN" if o["event_id"] in lean_games else "PASS")
    labels = list(rows)
    fig, ax = plt.subplots(figsize=(9, 0.45 * max(len(labels), 4) + 1.5), dpi=150)
    for i, k in enumerate(labels):
        mk, md, v = rows[k]
        ax.plot([mk, md], [i, i], color="#d1d5db", linewidth=2, zorder=1)
        ax.scatter([mk], [i], color=GREY, zorder=2, s=36)
        ax.scatter([md], [i], color=ACCENT if v != "PASS" else "#6b7280", zorder=3, s=46)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color="#e5e7eb")
    ax.invert_yaxis()
    _style(ax, title)
    ax.set_xlabel("home spread: light grey = Pinnacle (vig-free market) · dark = model · blue = paper signal (LEAN)")
    if test:
        fig.text(0.5, 0.5, "TEST DATA", fontsize=60, color="red", alpha=0.25, ha="center", va="center", rotation=20)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out
