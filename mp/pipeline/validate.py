"""Validator: every number in publishable text must come from structured data. Unexplained number => FAIL.

Allowed sources: research objects, the record summary, config thresholds, the backtest report.
Ignored as non-claims: ISO dates, times, URLs, 12-char ids, the helpline, "21+", week numbers.
A failure is never fixed by loosening this file; it is fixed by putting the number in the data.
"""
from __future__ import annotations
import re

PRICE_RE = re.compile(r"(?<![\w.])([+-]\d{3,4})(?![\d%.])")
PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s?%")
UNITS_RE = re.compile(r"([+-]?\d+(?:\.\d+)?)\s?u\b")
LINE_RE = re.compile(r"(?<![\w$.])([+-]\d{1,2}(?:\.\d)?)(?![\d%.u])")
RECORD_RE = re.compile(r"(?<![\w-])(\d+)-(\d+)(?:-(\d+))?(?![\w-])")


UNIT_KEYS = {"units", "staked", "max_drawdown_units", "stake_units"}
PCT_KEYS = {"clv_mean", "clv_pct_positive", "roi", "pct", "roi_at_-110", "edge_threshold_bet", "edge_threshold_lean",
            "sanity_max_gap"}
INT_KEYS = {"n", "graded", "wins", "losses", "pushes", "n_clv", "n_games"}
DEC_KEYS = {"spread_mae_model", "spread_mae_close", "z_vs_50"}


def _walk(d, out: list, key=""):
    if isinstance(d, dict):
        for k, v in d.items():
            _walk(v, out, str(k))
    elif isinstance(d, (list, tuple)):
        for v in d:
            _walk(v, out, key)
    elif isinstance(d, (int, float)) and not isinstance(d, bool) and d is not None:
        out.append((key, float(d)))


def allowed_from(objs: list[dict], summary: dict | None = None, cfg: dict | None = None,
                 backtest: dict | None = None) -> dict:
    prices, pcts, units, lines, ints = set(), set(), set(), set(), set()

    def pct(v):
        pcts.add(round(abs(v) * 100, 1)); pcts.add(float(round(abs(v) * 100)))

    for o in objs:
        for k in ("market_price", "fair_price", "fair_market_price", "threshold_price"):
            if o.get(k) is not None:
                prices.add(int(o[k]))
        for k in ("edge", "model_prob", "market_implied_prob", "fair_market_prob", "ev_per_unit", "exchange_prob"):
            if o.get(k) is not None:
                pct(float(o[k]))
        for k in ("line", "gap_points", "model_spread_home"):
            if o.get(k) is not None:
                lines.add(float(o[k])); lines.add(-float(o[k]))
        if o.get("stake_units"):
            units.add(float(o["stake_units"]))
    pairs: list = []
    for src in (summary, backtest):
        if src:
            _walk(src, pairs)
    if cfg:
        _walk(cfg.get("qualify", {}), pairs)
    for k, v in pairs:
        if k in UNIT_KEYS:
            units.add(round(abs(v), 2))
        elif k in PCT_KEYS:
            pct(v)
        elif k in INT_KEYS and float(v).is_integer():
            ints.add(int(v))
        elif k in DEC_KEYS:
            pcts.add(round(abs(v), 2))
    return {"prices": prices, "pcts": pcts, "units": units, "lines": lines, "ints": ints}


def _scrub(text: str) -> str:
    text = re.sub(r"\d{4}-\d{2}-\d{2}(?:T[\d:]+Z?)?", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"1-800-GAMBLER", " ", text)
    text = re.sub(r"\b[0-9a-f]{12}\b", " ", text)
    text = re.sub(r"\b\d{1,2}:\d{2}\s?(?:[AaPp][Mm])?(?:\s?ET)?\b", " ", text)
    text = re.sub(r"\b21\+", " ", text)
    text = re.sub(r"\b[Ww]eek \d+\b", " ", text)
    return text


def check(text: str, allowed: dict, counts: dict | None = None) -> list[str]:
    errors = []
    text = _scrub(text)
    ok_ints = set(allowed["ints"]) | set((counts or {}).values())
    for m in PRICE_RE.finditer(text):
        v = int(m.group(1))
        if v not in allowed["prices"]:
            errors.append(f"price {m.group(1)} not in data")
    for m in PCT_RE.finditer(text):
        v = float(m.group(1))
        if round(v, 1) not in allowed["pcts"] and float(round(v)) not in allowed["pcts"]:
            errors.append(f"percentage {m.group(1)}% not in data")
    for m in UNITS_RE.finditer(text):
        v = abs(float(m.group(1)))
        if v != 0 and round(v, 2) not in allowed["units"]:
            errors.append(f"units {m.group(1)}u not in data")
    for m in LINE_RE.finditer(text):
        v = float(m.group(1))
        if v not in allowed["lines"] and round(abs(v), 1) not in allowed["pcts"]:
            errors.append(f"line {m.group(1)} not in data")
    for m in RECORD_RE.finditer(text):
        nums = [int(x) for x in m.groups() if x is not None]
        if any(n not in ok_ints for n in nums):
            errors.append(f"record {m.group(0)} not in data")
    return errors
