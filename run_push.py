#!/usr/bin/env python3
"""Ship code updates (.\\mp push). GitHub Actions is the source of truth for DATA, so local data
(database/, content/, models/) is reset to what GitHub has; only CODE is committed from this computer."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODE = ["mp", "config", ".github", "tests", "mp.cmd", "requirements.txt", "README.md", ".gitignore",
        ".gitattributes"] + [p.name for p in ROOT.glob("run_*.py")]
DATA = ["database", "content", "models"]


def git(*a, check=True):
    r = subprocess.run(["git", *a], cwd=ROOT, text=True, capture_output=True)
    if check and r.returncode != 0:
        print(f"STOP: git {' '.join(a)}\n{r.stdout}{r.stderr}")
        sys.exit(1)
    return r


def main():
    if not (ROOT / ".git").exists():
        print("This folder is not set up yet. Run .\\mp gitsetup first.")
        return 1
    git("fetch", "-q", "origin")
    git("checkout", "-q", "HEAD", "--", *[d for d in DATA if (ROOT / d).exists()])   # drop local data edits
    git("clean", "-fdq", "--", "database", "content")                               # drop local-only outputs
    git("add", "-A", "--", *[c for c in CODE if (ROOT / c).exists()])
    changed = git("diff", "--cached", "--name-only").stdout.split()
    if changed:
        git("commit", "-q", "-m", "code update: " + ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else ""))
    git("pull", "-q", "--rebase", "origin", "main")
    git("push", "-q", "origin", "main")
    print(f"Pushed {len(changed)} changed code file(s): {', '.join(changed) or 'none'}")
    print("Local data now matches GitHub (the automated runs are the source of truth).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
