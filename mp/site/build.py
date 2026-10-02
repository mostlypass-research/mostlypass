"""Static site generator: database -> SITE_DIR. No framework. Deployed by GitHub Actions to Cloudflare Pages.
In FIXTURE mode the output goes to sandbox/site/public and every page carries a TEST banner."""
from __future__ import annotations
import html
import json
import shutil
from pathlib import Path
import pandas as pd
import markdown
from mp.config import SITE_DIR, OUT_DIR, MODEL_DIR, DB_DIR, MODE
from mp.pipeline.grade import record_summary, merged
from mp.content.render import record_line

TPL = Path(__file__).parent / "templates"
CSS = """
:root{--ink:#111827;--muted:#6b7280;--accent:#1d4ed8;--bg:#fff;--line:#e5e7eb;--soft:#f8fafc}
@media(prefers-color-scheme:dark){:root{--ink:#e5e7eb;--muted:#9ca3af;--accent:#93c5fd;--bg:#0b1220;--line:#1f2937;--soft:#111a2e}}
*{box-sizing:border-box}body{font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg);margin:0}
main{max-width:880px;margin:0 auto;padding:20px 16px 48px}
nav{display:flex;flex-wrap:wrap;gap:14px;font-size:15px;margin-bottom:8px}nav a{color:var(--accent);text-decoration:none}
nav a.sub{background:var(--accent);color:#fff;padding:2px 10px;border-radius:6px}
.cta{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:10px 16px;border-radius:8px;font-weight:600;margin:4px 0 12px}
.brand{font-weight:700;font-size:22px;margin:18px 0 0}.tag{color:var(--muted);margin:2px 0 18px}
.hero{border:1px solid var(--line);background:var(--soft);border-radius:12px;padding:20px 20px 8px;margin:8px 0 24px}
.hero .kicker{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0}
.hero h2{font-size:28px;line-height:1.2;margin:6px 0 8px}.hero p{margin:6px 0 12px}
table{border-collapse:collapse;width:100%;font-size:14px;display:block;overflow-x:auto}td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;white-space:nowrap}
.kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:12px 0}
.kpi div{border:1px solid var(--line);border-radius:8px;padding:12px}.kpi b{font-size:20px;display:block}
.muted{color:var(--muted)}footer{margin-top:40px;font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:12px}
.test{background:#b91c1c;color:#fff;padding:10px 14px;font-weight:700;text-align:center}
.gate{position:fixed;inset:0;background:var(--bg);display:flex;align-items:center;justify-content:center;z-index:9;padding:16px}
.gate div{max-width:440px;padding:24px;border:1px solid var(--line);border-radius:12px}
button{background:var(--accent);color:#fff;border:0;padding:10px 16px;border-radius:8px;font-size:16px;cursor:pointer}
img{max-width:100%;height:auto}input{font-size:15px;padding:4px 6px}
"""
GATE = """<div class="gate" id="gate"><div><h2>21+ only</h2><p>This site publishes research on sports-betting markets for adults.
It is not betting advice, and it does not take or place bets. If you or someone you know has a gambling problem, call 1-800-GAMBLER.</p>
<button onclick="document.getElementById('gate').remove()">I am 21 or older</button></div></div>"""


def _page(cfg, title, body, gate=False):
    b = cfg["brand"]
    test = '<div class="test">TEST BUILD - FIXTURE DATA - NOT FOR PUBLICATION</div>' if MODE != "LIVE" else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · {html.escape(b['name'])}</title><meta name="description" content="{html.escape(b['description'])}">
{'<meta name="robots" content="noindex">' if MODE != "LIVE" else ''}<style>{CSS}</style></head><body>{test}{GATE if gate else ''}<main>
<nav><a href="/">Today</a><a href="/record/">Record</a><a href="/archive/">Archive</a><a href="/methodology/">Methodology</a><a href="/calculators/">Calculators</a><a href="/about/">About</a>{('<a class="sub" href="' + html.escape(b['newsletter_url']) + '">Subscribe free</a>') if b.get('newsletter_url') else ''}</nav>
<p class="brand">{html.escape(b['name'])}</p><p class="tag">{html.escape(b['tagline'])}</p>
{body}
<footer>Research on betting markets, not betting advice. All signals are PAPER unless marked otherwise. The record is our own automated database:
public, timestamped, append-only, auditable, automatically graded. It is not independently verified. 21+. Gambling problem? Call 1-800-GAMBLER.<br>
Data: nflverse (CC-BY 4.0), The Odds API, Polymarket public API. No affiliate links.</footer></main></body></html>"""


def _md(t):
    return markdown.markdown(t, extensions=["tables"])


def _hero(cfg):
    b = cfg["brand"]
    kicker = f'<p class="kicker">{html.escape(b["founder_line"])}</p>' if b.get("founder_line") else f'<p class="kicker">{html.escape(b["category"])}</p>'
    return f"""<section class="hero">{kicker}<h2>{html.escape(b['tagline'])}</h2><p>{html.escape(b['description'])}</p>
<p class="muted">No locks. No screenshots. No deleted losses. Every signal is PAPER until a model earns the right to call something a bet.</p>
{('<a class="cta" href="' + html.escape(b['newsletter_url']) + '">Get the daily research by email (free)</a>') if b.get('newsletter_url') else ''}</section>"""


def build(cfg: dict, today_md: str | None, date_str: str):
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    s = record_summary()
    arch = sorted([p.name for p in OUT_DIR.iterdir() if (p / "newsletter.md").exists() and (p / "PUBLISHED").exists()], reverse=True)
    latest = arch[0] if arch else None
    # Today
    body = _hero(cfg)
    if latest:
        if (OUT_DIR / latest / "card.png").exists():
            shutil.copy(OUT_DIR / latest / "card.png", SITE_DIR / "card.png")
            body += "<img src='/card.png' alt='Model vs Pinnacle spread for every game on the card'>"
        body += _md((OUT_DIR / latest / "newsletter.md").read_text())
    else:
        body += "<p>The first daily card publishes soon. Until then: <a href='/methodology/'>how this works</a>.</p>"
    (SITE_DIR / "index.html").write_text(_page(cfg, "Today", body, gate=True))
    # Archive
    (SITE_DIR / "archive").mkdir(exist_ok=True)
    links = "".join(f'<li><a href="/archive/{d}/">{d}</a></li>' for d in arch) or "<li>Nothing published yet.</li>"
    (SITE_DIR / "archive" / "index.html").write_text(_page(cfg, "Archive", f"<h2>Archive</h2><ul>{links}</ul>"))
    for d in arch:
        (SITE_DIR / "archive" / d).mkdir(exist_ok=True)
        (SITE_DIR / "archive" / d / "index.html").write_text(_page(cfg, d, _md((OUT_DIR / d / "newsletter.md").read_text())))
    # Record
    rec = SITE_DIR / "record"
    rec.mkdir(exist_ok=True)
    df = merged()
    pass_rate = ""
    ro = DB_DIR / "research_objects.jsonl"
    if ro.exists() and latest:
        objs = [json.loads(l) for l in ro.read_text().splitlines() if l.strip()]
        pub_dates = set(arch)
        gv = {}
        for o in objs:
            if o["created_ts"][:10] in pub_dates and o.get("mode") == "LIVE":
                k = (o["created_ts"][:10], o["event_id"])
                gv[k] = min(gv.get(k, "PASS"), o["verdict"], key={"BET": 0, "LEAN": 1, "PASS": 2}.get)
        if gv:
            pr = sum(1 for v in gv.values() if v == "PASS") / len(gv)
            pass_rate = f"<div><b>{pr * 100:.0f}%</b>of games graded PASS</div>"
    b, l = s["bet"], s["lean"]
    lclv = f"{l['clv_mean'] * 100:+.2f}%" if l.get("clv_mean") is not None else "n/a"
    lpos = f"{l['clv_pct_positive'] * 100:.0f}%" if l.get("clv_pct_positive") is not None else "n/a"
    kpis = f"""<div class="kpi"><div><b>{s['money']}</b>money type</div><div><b>{b['n']}</b>BET signals</div>
<div><b>{l['n']}</b>LEAN paper signals</div><div><b>{l['wins']}-{l['losses']}-{l['pushes']}</b>LEAN results</div>
<div><b>{lclv}</b>LEAN mean CLV (n={l['n_clv']})</div><div><b>{lpos}</b>LEAN CLV positive</div>{pass_rate}</div>"""
    table = "<p>No signals published yet.</p>"
    if len(df):
        df = df.sort_values("published_ts", ascending=False)
        df.to_csv(rec / "record.csv", index=False)
        cols = [c for c in ["published_ts", "money", "verdict", "selection", "market", "line", "price", "book",
                            "fair_market_price", "fair_price", "edge", "stake_units", "result", "pl_units", "close_price",
                            "close_line", "close_min_before", "clv_prob"] if c in df]
        table = df[cols].head(400).to_html(index=False, na_rep="", border=0)
    eq = "<img src='/record/equity.png' alt='Paper P/L'>" if (rec / "equity.png").exists() else ""
    rules = (TPL / "record_rules.md").read_text()
    (rec / "index.html").write_text(_page(cfg, "Record", f"<h2>Public research record</h2><p>{html.escape(record_line(s))}</p>{kpis}{eq}"
                                          f"{_md(rules)}<p><a href='/record/record.csv'>Download every row (CSV)</a></p>{table}"))
    # Methodology (with the live backtest, flattering or not)
    bt = json.loads((MODEL_DIR / "backtest_report.json").read_text()) if (MODEL_DIR / "backtest_report.json").exists() else None
    btxt = ""
    if bt:
        rows = "".join(f"<tr><td>{k} pts</td><td>{v['n']}</td><td>{v['pct'] * 100:.1f}%</td><td>{v['z_vs_50']}</td><td>{v['roi_at_-110'] * 100:+.1f}%</td></tr>"
                       for k, v in bt["ats_by_threshold"].items())
        btxt = (f"<h3>Backtest: {bt['model']} against NFL closing lines, {bt['seasons'][0]}–{bt['seasons'][1]} ({bt['n_games']:,} games)</h3>"
                f"<p>Average spread miss: model {bt['spread_mae_model']:.2f} points, closing line {bt['spread_mae_close']:.2f}. "
                f"Brier score: model {bt['brier_model']:.4f}, vig-free closing moneyline {bt['brier_close']:.4f} (lower is better).</p>"
                f"<table><tr><th>Model vs close gap</th><th>Games</th><th>Against the spread</th><th>z vs 50%</th><th>ROI at -110</th></tr>{rows}</table>"
                f"<p><b>{html.escape(bt['verdict'])}</b> {html.escape(bt['multiple_testing_note'])}</p>")
    (SITE_DIR / "methodology").mkdir(exist_ok=True)
    (SITE_DIR / "methodology" / "index.html").write_text(_page(cfg, "Methodology", _md((TPL / "methodology.md").read_text()) + btxt))
    (SITE_DIR / "calculators").mkdir(exist_ok=True)
    (SITE_DIR / "calculators" / "index.html").write_text(_page(cfg, "Calculators", (TPL / "calculators.html").read_text()))
    about = (TPL / "about.md").read_text().replace("{{FOUNDER}}", cfg["brand"].get("founder_line") or "")
    (SITE_DIR / "about").mkdir(exist_ok=True)
    (SITE_DIR / "about" / "index.html").write_text(_page(cfg, "About", _md(about)))
    (SITE_DIR / "_headers").write_text("/*\n  X-Robots-Tag: noindex\n" if MODE != "LIVE" else "/*\n  X-Content-Type-Options: nosniff\n")
    print(f"[site] {MODE}: built {len(arch)} published day(s) -> {SITE_DIR}")
