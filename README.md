# Research machine: Phase 0 ($0)

Daily NFL betting-market research with a public, timestamped, append-only PAPER record.
You never need to edit code. Everything runs through one Windows command, `.\mp`, or automatically on GitHub Actions.

## Commands (PowerShell, inside this folder)

| Command | What it does | Credits |
| --- | --- | --- |
| `.\mp check` | One-time setup + tests + nflverse integrity + backtest + fixture run + proof that fixture output cannot be published | 0 |
| `.\mp setkey` | Saves your Odds API key to `.env` on this computer (never committed) | 0 |
| `.\mp odds` | Live probe: slate, books, Pinnacle on every market, timestamps, credits | ~3 |
| `.\mp daily` | Live morning pipeline -> `content\out\<date>\APPROVAL.txt` | ~3 |
| `.\mp fixture` | Same pipeline on TEST data, written to `sandbox\`, publication impossible | 0 |
| `.\mp preview` | Opens the generated website at http://localhost:8000 | 0 |
| `.\mp grade` / `.\mp close` | Grading / closing-line capture (normally automatic) | 0-3 |

## Automatic schedule (GitHub Actions, free on a public repo)

| Workflow | When (ET) | Does |
| --- | --- | --- |
| 1-daily-research | 08:15 daily | Odds + model + verdicts + content + validation; opens an approval issue |
| 2-closing-line-capture | every 10 min, 09:00-01:00 | Captures Pinnacle 5-15 min before each kickoff (safety capture at 35-45 min) |
| 3-grade-and-site | 07:00 daily | Grades finished games, CLV, record, redeploys site |
| 4-publish-on-approve | when you comment `approve` | Appends record, deploys site, closes the issue |

## Safety rules built into the code

- FIXTURE mode writes only to `sandbox/`, and every publish path refuses it. Three separate checks catch it: the process mode, the package mode and the event IDs.
- There are no BETs unless `models/backtest_report.json` shows the model beat closing lines out of sample. The gate is currently CLOSED.
- If Pinnacle is missing, there are no verdicts and no substitute book. A stale benchmark means no BET. A model-vs-market gap over 10 points forces a PASS.
- Every number in every publishable file must exist in the data, or the package is BLOCKED.
- Packages older than 8 hours cannot be published, and games that have already kicked off are never recorded.
- Record rows are only ever appended, never edited. CLV comes only from our own pre-kickoff captures; if one is missing, the CLV stays blank.

## Secrets (GitHub > Settings > Secrets and variables > Actions)

`ODDS_API_KEY`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`. Nothing else is needed.

Data sources: nflverse (CC-BY 4.0); The Odds API (free tier; raw snapshots are never committed); the Polymarket public API (display only).
