import math
from mp.pipeline.devig import (american_to_prob, prob_to_american, devig_two_way, hold, edge, kelly,
                               threshold_price, clv, spread_clv_points, ev_per_unit)
from mp.pipeline import validate
from mp.models.elo import Elo


def test_american_roundtrip():
    assert abs(american_to_prob(-110) - 0.5238) < 1e-3
    assert abs(american_to_prob(+150) - 0.4) < 1e-9
    assert prob_to_american(0.5238) in (-110, -109, -111)
    assert prob_to_american(0.4) == 150


def test_devig_and_hold():
    p1, p2 = american_to_prob(-110), american_to_prob(-110)
    assert abs(hold(p1, p2) - 0.0476) < 1e-3
    q1, q2 = devig_two_way(p1, p2)
    assert abs(q1 - 0.5) < 1e-9 and abs(q1 + q2 - 1) < 1e-9
    a, b = devig_two_way(american_to_prob(-320), american_to_prob(275), "power")
    assert abs(a + b - 1) < 1e-6 and a > 0.7


def test_edge_kelly_threshold():
    assert abs(edge(0.55, -110) - (0.55 - 0.5238)) < 1e-3
    assert kelly(0.55, -110, 1.0) > 0 and kelly(0.50, -110) == 0.0
    assert ev_per_unit(0.5238, -110) < 1e-6
    t = threshold_price(0.55, 0.03)  # need implied <= 0.52 => about -108
    assert -110 < t <= -107


def test_clv():
    assert clv(+115, +103) > 0
    assert clv(-110, -115) > 0  # closed shorter than our price: we beat the close
    assert clv(-110, -105) < 0
    assert spread_clv_points(+3.0, +2.5) == 0.5
    assert spread_clv_points(-3.0, -3.5) == 0.5


def test_elo_basic():
    e = Elo()
    assert abs(e.home_win_prob("A", "B") - 0.556) < 0.01  # HFA only
    e.update("A", "B", 30, 10)
    assert e.rating("A") > 1500 > e.rating("B")
    assert e.cover_prob("A", "B", -3.0) < e.home_win_prob("A", "B")


def test_validator_blocks_invented_numbers():
    objs = [{"market_price": 115, "fair_price": 103, "fair_market_price": 108, "threshold_price": 108,
             "edge": 0.026, "model_prob": 0.493, "market_implied_prob": 0.465, "fair_market_prob": 0.48,
             "ev_per_unit": 0.05, "line": None, "model_spread_home": -1.5, "stake_units": 0.5}]
    allowed = validate.allowed_from(objs, {"bet": {"n": 2, "wins": 1, "losses": 1, "pushes": 0, "units": 0.95}})
    ok = "ATL +115, fair +103, threshold +108, edge 2.6%, stake 0.5u. Record 1-1-0."
    bad = "ATL +110, fair -103, edge 4.1%, stake 2u."
    assert validate.check(ok, allowed, {"BET": 2, "LEAN": 4, "PASS": 9}) == []
    errs = validate.check(bad, allowed, {"BET": 2, "LEAN": 4, "PASS": 9})
    assert any("110" in e for e in errs) and any("4.1" in e for e in errs) and any("2u" in e for e in errs)
