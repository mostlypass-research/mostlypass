#!/usr/bin/env python3
"""One-time: turn this folder into the brand's GitHub repository, pseudonymously.
    .\\mp gitsetup <github-username> <noreply-email>
Sets a project-only identity ("Mostly Pass" + GitHub noreply address), verifies secrets are git-ignored,
commits, and pushes to https://github.com/<username>/mostlypass. Changes no global Git settings."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def git(*args, check=True, capture=False):
    r = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=capture)
    if check and r.returncode != 0:
        print(f"STOP: 'git {' '.join(args)}' failed." + (f"\n{r.stderr}" if capture else ""))
        sys.exit(1)
    return r


def main():
    if len(sys.argv) != 3 or "@users.noreply.github.com" not in sys.argv[2]:
        print("Usage: .\\mp gitsetup <github-username> <id+username@users.noreply.github.com>")
        return 1
    user, email = sys.argv[1].strip(), sys.argv[2].strip()
    repo = f"https://github.com/{user}/mostlypass.git"
    if not (ROOT / ".git").exists():
        git("init", "-q", "-b", "main")
    git("config", "user.name", "Mostly Pass")          # project-only (no --global)
    git("config", "user.email", email)
    git("config", "credential.https://github.com.username", user)
    # secrets and private data must be ignored before anything is staged
    for p in (".env", ".venv", "sandbox", "data/raw", "data/cache", "private"):
        if git("check-ignore", "-q", p, check=False).returncode != 0 and (ROOT / p).exists():
            print(f"STOP: {p} is not git-ignored. Nothing was committed. Tell Claude.")
            return 1
    git("add", "-A")
    staged = git("diff", "--cached", "--name-only", capture=True).stdout.split()
    leaks = [f for f in staged if f.startswith((".env", ".venv", "sandbox/", "data/raw", "data/cache", "private/")) or "keys" in f.lower()]
    if leaks:
        git("reset", "-q")
        print(f"STOP: refusing to commit private files: {leaks}")
        return 1
    if git("rev-parse", "--verify", "HEAD", check=False, capture=True).returncode != 0 or staged:
        git("commit", "-q", "-m", "Mostly Pass research machine: initial public commit")
    print(f"Identity on commits: Mostly Pass <{email}>  (your global Git settings are untouched)")
    print(f"Files committed: {len(staged)}. Secrets checked: .env and raw odds data are excluded.")
    remotes = git("remote", capture=True).stdout.split()
    if "origin" in remotes:
        git("remote", "set-url", "origin", repo)
    else:
        git("remote", "add", "origin", repo)
    print(f"Pushing to {repo} ... a browser window may open: sign in as {user} and click Authorize.")
    git("push", "-u", "origin", "main")
    print(f"\nSUCCESS: https://github.com/{user}/mostlypass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
