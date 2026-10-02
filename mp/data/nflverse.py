"""nflverse data (CC-BY-4.0): schedule, scores, closing spread/total 1999+, moneylines 2006+.
Source: https://github.com/nflverse/nflverse-data/releases/tag/schedules
"""
from __future__ import annotations
import time
import datetime as dt
from pathlib import Path
import pandas as pd
import requests
from mp.config import CACHE_DIR

GAMES_URL = "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv"

TEAM_MAP = {
    "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR", "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
    "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
    "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS",
}
ABBR_TO_NAME = {v: k for k, v in TEAM_MAP.items()}
LEGACY = {"OAK": "LV", "SD": "LAC", "STL": "LA"}   # franchise moves, so ratings carry across


def load_games(refresh: bool = True, max_age_hours: float = 6) -> pd.DataFrame:
    dest = CACHE_DIR / "nflverse_games.csv"
    fresh = dest.exists() and (time.time() - dest.stat().st_mtime) < max_age_hours * 3600
    if refresh and not fresh:
        try:
            r = requests.get(GAMES_URL, timeout=60)
            r.raise_for_status()
            dest.write_bytes(r.content)
        except Exception as e:
            if not dest.exists():
                raise RuntimeError(f"nflverse download failed and no cached copy: {e}")
            print(f"[nflverse] download failed, using cached copy: {e}")
    df = pd.read_csv(dest, low_memory=False)
    for col in ("home_team", "away_team"):
        df[col] = df[col].replace(LEGACY)
    df["gameday"] = pd.to_datetime(df["gameday"])
    return df


def match_events(games: pd.DataFrame, events: pd.DataFrame, season: int) -> pd.DataFrame:
    """Attach nflverse game_id and week to each Odds API event: same home/away teams, kickoff date within 1 day.
    Unmatched events are returned with game_id = None (caller warns and excludes them)."""
    s = games[games.season == season]
    out = []
    for ev in events.drop_duplicates("event_id").itertuples(index=False):
        h, a = TEAM_MAP.get(ev.home_team), TEAM_MAP.get(ev.away_team)
        kick_et = pd.Timestamp(ev.commence_time).tz_convert("America/New_York").tz_localize(None).normalize()
        m = s[(s.home_team == h) & (s.away_team == a) & ((s.gameday - kick_et).abs() <= pd.Timedelta(days=1))]
        out.append({"event_id": ev.event_id, "game_id": m.game_id.iloc[0] if len(m) == 1 else None,
                    "week": int(m.week.iloc[0]) if len(m) == 1 else None, "home_abbr": h, "away_abbr": a})
    return pd.DataFrame(out)


def integrity_report(df: pd.DataFrame, season: int) -> dict:
    """Checks the user asked for: schedule, scores, lines, teams, dates, duplicates, playoffs."""
    rep = {"rows": len(df), "seasons": f"{int(df.season.min())}-{int(df.season.max())}",
           "duplicate_game_ids": int(df.game_id.duplicated().sum())}
    recent = df[df.season >= season - 6]
    teams = set(recent.home_team) | set(recent.away_team)
    rep["teams_recent"] = len(teams)
    rep["teams_not_in_map"] = sorted(t for t in teams if t not in ABBR_TO_NAME)
    rep["game_types"] = df.game_type.value_counts().to_dict()
    rep["neutral_site_games"] = int((df.location == "Neutral").sum())
    played = df.dropna(subset=["home_score", "away_score"])
    rep["spread_line_coverage_played"] = round(float(played.spread_line.notna().mean()), 4)
    rep["moneyline_coverage_2010plus"] = round(float(played[played.season >= 2010].home_moneyline.notna().mean()), 4)
    cur = df[df.season == season]
    rep["current_season_games"] = len(cur)
    rep["current_season_played"] = int(cur.home_score.notna().sum())
    up = cur[cur.home_score.isna()].sort_values(["gameday", "gametime"])
    if len(up):
        wk = int(up.week.iloc[0])
        nxt = up[up.week == wk]
        rep["next_week"] = wk
        rep["next_week_games"] = len(nxt)
        rep["next_week_dates"] = f"{nxt.gameday.min().date()} to {nxt.gameday.max().date()}"
    # scores present only for past dates (no future scores = no data leak in the file)
    today = pd.Timestamp(dt.date.today())
    rep["future_games_with_scores"] = int(df[(df.gameday > today) & df.home_score.notna()].shape[0])
    # chronology: within each team, game dates strictly increase (no duplicated/overlapping rows)
    long = pd.concat([df[["season", "gameday", "home_team"]].rename(columns={"home_team": "team"}),
                      df[["season", "gameday", "away_team"]].rename(columns={"away_team": "team"})])
    rep["team_same_day_duplicates"] = int(long.duplicated(["team", "gameday"]).sum())
    return rep
