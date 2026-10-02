"""Odds math. Pure functions, unit-tested."""
from __future__ import annotations
import math


def american_to_prob(odds: float) -> float:
    odds = float(odds)
    return 100.0 / (odds + 100.0) if odds > 0 else (-odds) / (-odds + 100.0)


def prob_to_american(p: float) -> int:
    p = min(max(float(p), 1e-6), 1 - 1e-6)
    if p >= 0.5:
        return int(round(-100.0 * p / (1 - p)))
    return int(round(100.0 * (1 - p) / p))


def american_to_decimal(odds: float) -> float:
    odds = float(odds)
    return 1 + odds / 100.0 if odds > 0 else 1 + 100.0 / (-odds)


def devig_two_way(p1: float, p2: float, method: str = "multiplicative") -> tuple[float, float]:
    """Remove vig from a two-outcome market. 'power' solves p1^k + p2^k = 1 (favorite-longshot aware)."""
    if method == "multiplicative":
        s = p1 + p2
        return p1 / s, p2 / s
    # power method: bisection on k
    lo, hi = 0.5, 3.0
    for _ in range(60):
        k = (lo + hi) / 2
        f = p1 ** k + p2 ** k - 1
        if f > 0:
            lo = k
        else:
            hi = k
    k = (lo + hi) / 2
    return p1 ** k, p2 ** k


def hold(p1: float, p2: float) -> float:
    return p1 + p2 - 1.0


def edge(model_p: float, price_american: float) -> float:
    """Probability edge: model prob minus implied prob at the price offered (vig included)."""
    return model_p - american_to_prob(price_american)


def ev_per_unit(model_p: float, price_american: float) -> float:
    d = american_to_decimal(price_american)
    return model_p * (d - 1) - (1 - model_p)


def kelly(model_p: float, price_american: float, fraction: float = 0.25, cap: float = 1.0) -> float:
    b = american_to_decimal(price_american) - 1
    f = (model_p * b - (1 - model_p)) / b
    return float(min(max(f * fraction, 0.0), cap))


def threshold_price(model_p: float, min_edge: float) -> int:
    """Worst price at which edge is still >= min_edge."""
    p_needed = model_p - min_edge
    return prob_to_american(p_needed)


def clv(bet_price: float, close_price: float) -> float:
    """CLV as implied-probability difference: close implied - bet implied (positive = beat the close)."""
    return american_to_prob(close_price) - american_to_prob(bet_price)


def spread_clv_points(bet_line: float, close_line: float) -> float:
    """Points of CLV on a spread. Both lines are from the bet side's own perspective
    (e.g. we took +3, it closed +2.5 => +0.5; we took -3, it closed -3.5 => +0.5)."""
    return bet_line - close_line
