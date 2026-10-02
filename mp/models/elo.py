"""elo_v0: a transparent margin-of-victory Elo for NFL.

Deterministic. No LLM touches a number. Fit sequentially so there is no look-ahead:
ratings used to price a game depend only on games completed before it.
Spread (home - away points) = (home_elo + HFA - away_elo) / elo_to_points.
Win prob = Phi(spread / spread_sd) (normal margin approximation).
"""
from __future__ import annotations
import json
import math
from dataclasses import dataclass, field
import pandas as pd
from mp.config import MODEL_DIR


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass
class Elo:
    k: float = 20.0
    hfa: float = 48.0
    elo_to_points: float = 25.0
    spread_sd: float = 13.5
    regress: float = 0.33
    mov: bool = True
    ratings: dict = field(default_factory=dict)
    last_season: int | None = None
    version: str = "elo_v0"

    def rating(self, team: str) -> float:
        return self.ratings.get(team, 1500.0)

    def new_season(self, season: int):
        if self.last_season is not None and season != self.last_season:
            for t in self.ratings:
                self.ratings[t] = 1500.0 + (self.ratings[t] - 1500.0) * (1 - self.regress)
        self.last_season = season

    def expected_spread(self, home: str, away: str, neutral: bool = False) -> float:
        diff = self.rating(home) - self.rating(away) + (0 if neutral else self.hfa)
        return diff / self.elo_to_points

    def home_win_prob(self, home: str, away: str, neutral: bool = False) -> float:
        return norm_cdf(self.expected_spread(home, away, neutral) / self.spread_sd)

    def cover_prob(self, home: str, away: str, line_home: float, neutral: bool = False) -> float:
        """P(home margin + line_home > 0). line_home is the home spread (e.g. -3.5)."""
        mu = self.expected_spread(home, away, neutral)
        return 1.0 - norm_cdf((-line_home - mu) / self.spread_sd)

    def update(self, home: str, away: str, home_score: float, away_score: float, neutral: bool = False):
        p_home = self.home_win_prob(home, away, neutral)
        margin = home_score - away_score
        s_home = 1.0 if margin > 0 else (0.5 if margin == 0 else 0.0)
        mult = 1.0
        if self.mov:
            elo_diff = self.rating(home) - self.rating(away) + (0 if neutral else self.hfa)
            if margin < 0:
                elo_diff = -elo_diff
            mult = math.log(abs(margin) + 1) * (2.2 / (elo_diff * 0.001 + 2.2))
        delta = self.k * mult * (s_home - p_home)
        self.ratings[home] = self.rating(home) + delta
        self.ratings[away] = self.rating(away) - delta

    def fit(self, games: pd.DataFrame):
        """games: completed games sorted by date with season, home_team, away_team, scores, location."""
        g = games.dropna(subset=["home_score", "away_score"]).sort_values(["gameday", "game_id"])
        for r in g.itertuples(index=False):
            self.new_season(int(r.season))
            self.update(r.home_team, r.away_team, float(r.home_score), float(r.away_score),
                        neutral=(getattr(r, "location", "Home") == "Neutral"))

    def save(self, path=None):
        path = path or MODEL_DIR / "elo_ratings.json"
        path.write_text(json.dumps({"version": self.version, "last_season": self.last_season,
                                    "params": {"k": self.k, "hfa": self.hfa, "elo_to_points": self.elo_to_points,
                                               "spread_sd": self.spread_sd, "regress": self.regress},
                                    "ratings": self.ratings}, indent=1))

    @classmethod
    def from_cfg(cls, cfg: dict) -> "Elo":
        m = cfg["model"]
        return cls(k=m["k"], hfa=m["home_field_elo"], elo_to_points=m["elo_to_points"],
                   spread_sd=m["spread_sd"], regress=m["regress_preseason"], mov=m["mov_multiplier"],
                   version=m["name"])
