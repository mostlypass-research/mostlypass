"""One set of research objects -> every channel. Templates only format numbers that already exist in the data."""
from __future__ import annotations
import json
from mp.config import OUT_DIR, MODE
from mp.content.prose import rationale, fmt_price, fmt_line, label, nick, polish

RANK = {"BET": 0, "LEAN": 1, "PASS": 2}


def games(objs):
    g = {}
    for o in objs:
        x = g.setdefault(o["event_id"], {"home": o["home"], "away": o["away"], "commence": o["commence_time"],
                                         "mu": o["model_spread_home"], "items": []})
        x["items"].append(o)
    for x in g.values():
        x["verdict"] = min((i["verdict"] for i in x["items"]), key=RANK.get)
        x["top"] = min(x["items"], key=lambda i: (RANK[i["verdict"]], -i["edge"]))
        x["sp"] = next((i for i in x["items"] if i["market"] == "spreads" and i["selection"] == x["home"]), None)
        x["name"] = f"{nick(x['away'])} @ {nick(x['home'])}"
        spreads = [i for i in x["items"] if i["market"] == "spreads"]
        x["spread_best_edge"] = max((i["edge"] for i in spreads), default=None)
        x["flagged"] = any("sanity_gap" in (i.get("flags") or []) for i in spreads)
        x["clean_pass"] = x["verdict"] == "PASS" and not x["flagged"] and x["sp"] is not None
    return sorted(g.values(), key=lambda x: (RANK[x["verdict"]], x["commence"]))


def counts(objs):
    gs = games(objs)
    return {k: sum(1 for x in gs if x["verdict"] == k) for k in ("BET", "LEAN", "PASS")}


def record_line(s: dict) -> str:
    if not s:
        return "No signals graded yet."
    b, l = s["bet"], s["lean"]
    parts = []
    if b["graded"]:
        roi = f"{b['roi'] * 100:+.1f}%" if b.get("roi") is not None else "n/a"
        parts.append(f"BET (paper): {b['wins']}-{b['losses']}-{b['pushes']}, {b['units']:+.2f}u, ROI {roi}, "
                     f"max drawdown {b['max_drawdown_units']:.2f}u")
    else:
        parts.append("BET: none (the model has not earned BETs)")
    if l["graded"]:
        clv = f"{l['clv_mean'] * 100:+.1f}%" if l.get("clv_mean") is not None else "n/a"
        parts.append(f"LEAN paper signals: {l['wins']}-{l['losses']}-{l['pushes']}, mean CLV {clv} (n={l['n_clv']})")
    else:
        parts.append(f"LEAN paper signals published: {l['n']}, none graded yet")
    return " · ".join(parts)


def newsletter_md(cfg, objs, summary, date_str, recap="", use_llm=False) -> str:
    b, gs, c = cfg["brand"], games(objs), counts(objs)
    wk = objs[0]["week"] if objs else ""
    L = [f"# {b['name']}: NFL Week {wk} research, {date_str}", ""]
    if MODE != "LIVE":
        L += ["**TEST BUILD: FIXTURE DATA. NOT FOR PUBLICATION.**", ""]
    L += [f"*{b['tagline']}* Today's card: **{c['BET']} BET · {c['LEAN']} LEAN · {c['PASS']} PASS** across {len(gs)} games. "
          "All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.", ""]
    bets = [o for o in objs if o["verdict"] == "BET"]
    leans = sorted([o for o in objs if o["verdict"] == "LEAN"], key=lambda o: -o["edge"])
    L += ["## Bets", ""]
    if bets:
        L += [f"- **{label(o)} {fmt_price(o['market_price'])}**: {polish(rationale(o), use_llm)}" for o in bets]
    else:
        L += ["None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. "
              "What follows is research."]
    if leans:
        L += ["", "## Where the model disagrees on the spread (paper signals)", ""]
        L += [f"- {label(o)} {fmt_price(o['market_price'])} ({o['market_book']}): Pinnacle fair {fmt_price(o['fair_market_price'])}, "
              f"model {fmt_price(o['fair_price'])}, would clear the BET bar at {fmt_price(o['threshold_price'])} or better" for o in leans[:8]]
    L += ["", "## Every game: market vs model", "",
          "| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |", "| --- | --- | --- | --- | --- |"]
    for x in gs:
        sp = x["sp"]
        L.append(f"| {x['name']} | {fmt_line(sp['line']) if sp else 'n/a'} | {fmt_line(-x['mu'])} | "
                 f"{fmt_line(sp['gap_points']) if sp and sp.get('gap_points') is not None else 'n/a'} | {x['verdict']} |")
    clean = sorted([x for x in gs if x["clean_pass"]], key=lambda x: abs(x["sp"]["gap_points"]))
    if clean:
        x = clean[0]
        L += ["", "## Why we're passing", "",
              f"{x['name']}: Pinnacle has {nick(x['home'])} {fmt_line(x['sp']['line'])}; our model makes it {fmt_line(-x['mu'])}. "
              f"The best model edge on either side of the spread is {round(x['spread_best_edge'] * 100, 1)}%, under the "
              f"{round(cfg['qualify']['edge_threshold_lean'] * 100, 1)}% bar for even a paper signal. The price is fair, so not betting is the default."]
    flagged = [x for x in gs if x["flagged"]]
    if flagged:
        L += ["", "## When the model is probably wrong", "",
              "A big gap between our model and the sharp market usually means the model is missing information, "
              "such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:", ""]
        L += [f"- {x['name']}: market {fmt_line(x['sp']['line'])}, model {fmt_line(-x['mu'])} (gap {fmt_line(x['sp']['gap_points'])} pts)" for x in flagged]
    ex = [o for o in objs if o.get("exchange_prob") is not None]
    if ex:
        o = ex[0]
        L += ["", "## Two markets, one game", "",
              f"{nick(o['selection'])} to win: sportsbook price {fmt_price(o['market_price'])} implies "
              f"{round(o['market_implied_prob'] * 100)}% with vig; Pinnacle without vig {round(o['fair_market_prob'] * 100)}%; "
              f"Polymarket {round(o['exchange_prob'] * 100)}%."]
    if recap:
        L += ["", "## Results", "", recap]
    L += ["", "## The record", "", record_line(summary), "", "---",
          f"How this works: {b['site_url']}/methodology/ · Every row: {b['site_url']}/record/record.csv",
          "Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER."]
    return "\n".join(L)


def x_posts(cfg, objs, summary, date_str) -> list[str]:
    b, gs, c = cfg["brand"], games(objs), counts(objs)
    wk = objs[0]["week"] if objs else ""
    posts = [f"NFL Week {wk} card, {date_str}.\n{len(gs)} games priced. {c['BET']} bets, {c['LEAN']} paper signals, {c['PASS']} passes.\n\n"
             f"{b['tagline']}\nEvery line, every disagreement, every result: link in reply."]
    clean = sorted([x for x in gs if x["clean_pass"]], key=lambda x: abs(x["sp"]["gap_points"]))
    if clean:
        x = clean[0]
        posts.append(f"Why we're passing on {x['name']}:\nPinnacle {fmt_line(x['sp']['line'])}. Our model {fmt_line(-x['mu'])}.\n"
                     f"Best edge on either side of the spread: {round(x['spread_best_edge'] * 100, 1)}%.\n"
                     "That's noise, not an edge. The price is fair.")
    flagged = sorted([x for x in gs if x["flagged"]], key=lambda x: -abs(x["sp"]["gap_points"]))
    if flagged:
        x = flagged[0]
        posts.append(f"This looks like an edge. It isn't.\n{x['name']}: market {fmt_line(x['sp']['line'])}, our model {fmt_line(-x['mu'])}.\n"
                     "A gap that big usually means the model is missing something (a QB change, an injury), not that the sharp market is wrong.\nAutomatic pass.")
    leans = sorted([o for o in objs if o["verdict"] == "LEAN"], key=lambda o: -o["edge"])
    if leans:
        o = leans[0]
        posts.append(f"Biggest model disagreement today (paper, not a bet):\n{label(o)} {fmt_price(o['market_price'])}\n"
                     f"Pinnacle fair {fmt_price(o['fair_market_price'])} · model {fmt_price(o['fair_price'])}\n"
                     "Our model hasn't beaten closing lines yet, so we track it instead of betting it.")
    ex = [o for o in objs if o.get("exchange_prob") is not None]
    if ex:
        o = ex[0]
        posts.append(f"Same game, three prices. {nick(o['selection'])} to win:\nSportsbook {fmt_price(o['market_price'])} = "
                     f"{round(o['market_implied_prob'] * 100)}% (vig included)\nPinnacle, vig removed: {round(o['fair_market_prob'] * 100)}%\n"
                     f"Polymarket: {round(o['exchange_prob'] * 100)}%")
    posts.append(f"Record ({summary.get('money', 'PAPER')}): {record_line(summary)}\nPublic, timestamped, append-only.")
    return posts


def short_script(cfg, objs, date_str) -> dict:
    gs, c = games(objs), counts(objs)
    wk = objs[0]["week"] if objs else ""
    clean = sorted([g for g in gs if g["clean_pass"]], key=lambda g: abs(g["sp"]["gap_points"]))
    x = clean[0] if clean else next((g for g in gs if g["sp"]), gs[0])
    focus = (f"{x['name']}. Pinnacle {fmt_line(x['sp']['line']) if x['sp'] else 'n/a'}. Model {fmt_line(-x['mu'])}. "
             + ("Inside the noise. We pass." if x.get("clean_pass") else "A disagreement. Tracked on paper, not bet."))
    caps = [f"NFL Week {wk}", f"{len(gs)} games. {c['BET']} bets. {c['PASS']} passes.", focus,
            cfg["brand"]["tagline"], "Every signal timestamped. Every result published."]
    return {"title": f"Why we're passing on {x['name']}" if x.get("clean_pass") else f"NFL Week {wk}: market vs model",
            "captions": caps,
            "description": f"{focus}\n\nPublic, timestamped, append-only paper record: {cfg['brand']['site_url']}/record/\n"
                           "Research, not betting advice. 21+."}


def recap_md(graded, summary) -> str:
    if graded is None or len(graded) == 0:
        return ""
    return f"{len(graded)} signals graded since the last issue. " + record_line(summary)


def write_all(cfg, objs, summary, recap, date_str, use_llm=False) -> dict:
    d = OUT_DIR / date_str
    d.mkdir(parents=True, exist_ok=True)
    nl = newsletter_md(cfg, objs, summary, date_str, recap, use_llm)
    posts = x_posts(cfg, objs, summary, date_str)
    short = short_script(cfg, objs, date_str)
    (d / "newsletter.md").write_text(nl)
    (d / "x_posts.txt").write_text("\n\n=====\n\n".join(posts))
    (d / "short.json").write_text(json.dumps(short, indent=1))
    (d / "research_objects.json").write_text(json.dumps(objs, indent=1, default=str))
    (d / "MODE").write_text(MODE)
    return {"dir": d, "newsletter": nl, "x_posts": posts, "short": short}
