#!/usr/bin/env python3
"""Store the Odds API key in a local .env file (never committed, never sent anywhere but The Odds API)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
env = ROOT / ".env"
print("Paste your Odds API key (right-click or Ctrl+V), then press Enter:")
key = input("> ").strip().strip('"').strip("'")
if not re.fullmatch(r"[0-9a-fA-F]{32}", key):
    print(f"That does not look like an Odds API key (expected 32 letters/numbers, got {len(key)} characters). Nothing saved.")
    sys.exit(1)
lines = [l for l in (env.read_text(encoding="utf-8").splitlines() if env.exists() else []) if not l.startswith("ODDS_API_KEY=")]
lines.append(f"ODDS_API_KEY={key}")
env.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Saved. Key ends in ...{key[-4:]}. It is stored only in {env.name} on this computer (git ignores it).")
