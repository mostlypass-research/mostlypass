"""Morning approval package. Delivered as a GitHub issue (free email + mobile push via the GitHub app).
Approve: comment exactly `approve` on the issue. Hold: do nothing. Nothing publishes without approval."""
from __future__ import annotations
import os
import requests
from mp.content.prose import fmt_price, label


def package_text(cfg, date_str, objs, counts, warnings, model_warnings, errors, credits, gate_open, n_posts, short_ok,
                 record_line) -> str:
    leans = sorted([o for o in objs if o["verdict"] in ("BET", "LEAN")], key=lambda o: (o["verdict"] != "BET", -o["edge"]))
    top = leans[0] if leans else (max(objs, key=lambda o: o["edge"]) if objs else None)
    wk = objs[0]["week"] if objs else "?"
    L = [f"MODE: {cfg['mode']}", f"DATE: {date_str}   NFL Week {wk}", "", "TODAY",
         f"BET: {counts['BET']}   LEAN: {counts['LEAN']}   PASS: {counts['PASS']}", ""]
    if top:
        L += [f"TOP SIGNAL ({top['verdict']}, {top['money']}):", f"  {label(top)} {fmt_price(top['market_price'])} at {top['market_book']}",
              f"MARKET: Pinnacle vig-free {fmt_price(top['fair_market_price'])} ({top['fair_market_prob']:.1%})",
              f"MODEL:  {fmt_price(top['fair_price'])} ({top['model_prob']:.1%})   edge {top['edge']:.1%}   BET bar at {fmt_price(top['threshold_price'])} or better",
              f"POLYMARKET: {top['exchange_prob']:.0%}" if top.get("exchange_prob") is not None else "POLYMARKET: n/a", ""]
    L += [f"BACKTEST GATE: {'OPEN' if gate_open else 'CLOSED (BET impossible)'}",
          "MODEL WARNINGS: " + ("None" if not model_warnings else "\n  - " + "\n  - ".join(model_warnings[:8])),
          "DATA WARNINGS: " + ("None" if not warnings else "\n  - " + "\n  - ".join(warnings[:8])),
          f"ODDS API CREDITS LEFT: {credits}",
          "VALIDATION: " + ("PASS" if not errors else "FAIL\n  - " + "\n  - ".join(errors[:8])),
          f"CONTENT: {'READY' if not errors else 'BLOCKED'} (newsletter, {n_posts} X posts, short: {'yes' if short_ok else 'skipped'})",
          f"RECORD: {record_line}"]
    repo = os.getenv("GITHUB_REPOSITORY")
    if short_ok and repo and cfg["mode"] == "LIVE":
        L.append(f"SHORT (review only, not posted anywhere): https://github.com/{repo}/raw/main/content/out/{date_str}/short.mp4")
    L.append("")
    if cfg["mode"] != "LIVE":
        L.append("STATUS: TEST RUN (fixture data). Publication is disabled in this mode.")
    elif errors:
        L.append("STATUS: BLOCKED. Validation failed, so nothing can be published today.")
    else:
        L.append("STATUS: AWAITING APPROVAL. Comment exactly  approve  on this issue to publish. Do nothing to hold.")
    return "\n".join(L)


def github_issue(title: str, body: str) -> str:
    tok, repo = os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPOSITORY")
    if not tok or not repo:
        return "no GitHub context (local run): package saved to APPROVAL.txt"
    r = requests.post(f"https://api.github.com/repos/{repo}/issues",
                      headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"},
                      json={"title": title, "body": f"```\n{body}\n```", "labels": ["approval"]}, timeout=20)
    return f"approval issue: HTTP {r.status_code}"
