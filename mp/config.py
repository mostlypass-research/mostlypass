"""Central config. MODE is decided ONCE, at import, from the MP_FIXTURE env var.

LIVE    -> production folders (database/, content/out/, site/public/), publication allowed.
FIXTURE -> everything goes to sandbox/ (git-ignored), site carries a TEST banner,
           and run_publish.py refuses to run. Fixture data cannot reach production.
Run scripts set MP_FIXTURE from the --fixture flag before importing anything from mp.
"""
from __future__ import annotations
import os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "settings.yaml"


def _load_dotenv():
    """Read KEY=VALUE lines from ROOT/.env (created by `mp setkey`). Never overrides real env vars."""
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()
MODE = "FIXTURE" if os.getenv("MP_FIXTURE") == "1" else "LIVE"
BASE = ROOT / "sandbox" if MODE == "FIXTURE" else ROOT

DB_DIR = BASE / "database"
RAW_DIR = BASE / "data" / "raw"          # never committed (Odds API terms: no redistribution of raw data)
OUT_DIR = BASE / "content" / "out"
SITE_DIR = BASE / "site" / "public"
MODEL_DIR = ROOT / "models"              # backtest report is mode-independent (built from nflverse only)
FIXTURE_DIR = ROOT / "data" / "fixtures"
CACHE_DIR = ROOT / "data" / "cache"      # nflverse download cache, shared by both modes

for d in (DB_DIR, RAW_DIR, OUT_DIR, SITE_DIR, MODEL_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)


def load() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["mode"] = MODE
    cfg["secrets"] = {
        "odds_api_key": os.getenv("ODDS_API_KEY", "").strip(),
        "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
        "telegram_chat": os.getenv("TELEGRAM_CHAT_ID", "").strip(),
    }
    if MODE == "FIXTURE":
        cfg["odds"]["provider"] = "fixture"
    return cfg


def assert_live(action: str):
    """Hard stop for anything that publishes. Not configurable."""
    if MODE != "LIVE":
        import sys
        print(f"REFUSED: '{action}' is disabled in FIXTURE mode. Fixture/test data can never be published.")
        sys.exit(2)
