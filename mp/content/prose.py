"""Rationale text from templates. Every figure is formatted here from the research object.

Optional --llm: pipes the finished text through the local `claude` CLI (your subscription, $0) with an
instruction not to touch any number; the validator still checks the result, so a changed digit blocks it.
"""
from __future__ import annotations
import shutil
import subprocess


def fmt_price(p) -> str:
    p = int(p)
    return f"+{p}" if p > 0 else str(p)


def fmt_line(x) -> str:
    if x is None:
        return "ML"
    x = float(x)
    return "PK" if x == 0 else (f"+{x:g}" if x > 0 else f"{x:g}")


def nick(team: str) -> str:
    return team.split()[-1]


def label(o: dict) -> str:
    return f"{nick(o['selection'])} {fmt_line(o['line'])}" if o["market"] == "spreads" else f"{nick(o['selection'])} ML"


def rationale(o: dict) -> str:
    s = (f"{label(o)} is {fmt_price(o['market_price'])} at {o['market_book']}. Pinnacle, vig removed: "
         f"{fmt_price(o['fair_market_price'])}. Model: {fmt_price(o['fair_price'])}. "
         f"Model edge at the offered price: {round(o['edge'] * 100, 1)}%. ")
    if o["verdict"] == "BET":
        s += f"Paper BET {o['stake_units']:g}u; stop at {fmt_price(o['threshold_price'])}."
    elif o["verdict"] == "LEAN":
        s += ("LEAN (paper signal): the model has not beaten closing lines in testing, so this is a disagreement "
              f"to track, not a bet. It would need {fmt_price(o['threshold_price'])} or better.")
    else:
        s += "PASS: model and market agree within noise."
    if o.get("exchange_prob") is not None:
        s += f" Polymarket: {round(o['exchange_prob'] * 100)}%."
    return s


def polish(text: str, use_llm: bool = False) -> str:
    exe = shutil.which("claude") if use_llm else None
    if not exe:
        return text
    prompt = ("Rewrite this sports-betting research note in plain, dry, analytical English. Do not add, remove or "
              "change ANY number, sign, price, team, book or verdict word. Return only the rewritten text.\n\n" + text)
    try:
        out = subprocess.run([exe, "-p", prompt], capture_output=True, text=True, timeout=180, encoding="utf-8")
        return out.stdout.strip() or text
    except Exception:
        return text
