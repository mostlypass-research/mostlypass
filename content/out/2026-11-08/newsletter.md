# Mostly Pass: NFL Week 9 research, 2026-11-08

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 7 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Eagles +3 -110 (draftkings): Pinnacle fair -116, model -158, would clear the BET bar at -140 or better
- Vikings +3 +101 (pinnacle): Pinnacle fair +107, model -137, would clear the BET bar at -122 or better
- Chargers +5.5 -108 (betrivers): Pinnacle fair -105, model -132, would clear the BET bar at -117 or better
- Chiefs -10 +104 (pinnacle): Pinnacle fair +109, model -114, would clear the BET bar at -101 or better
- 49ers -10 +106 (pinnacle): Pinnacle fair +111, model -111, would clear the BET bar at +102 or better
- Bears -6 -104 (lowvig): Pinnacle fair -101, model -112, would clear the BET bar at +100 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Jets @ Chiefs | -10 | -11.1 | +1.1 | LEAN |
| Giants @ Eagles | +3 | -0.9 | +3.9 | LEAN |
| Texans @ Chargers | +5.5 | +3.2 | +2.3 | LEAN |
| Raiders @ 49ers | -10 | -10.9 | +0.9 | LEAN |
| Buccaneers @ Bears | -6 | -7 | +1 | LEAN |
| Bills @ Vikings | +3 | +0.3 | +2.7 | LEAN |
| Browns @ Saints | -3.5 | -0.5 | -3 | PASS |
| Broncos @ Panthers | +3 | +6.8 | -3.8 | PASS |
| Cowboys @ Colts | +3.5 | PK | +3.5 | PASS |
| Lions @ Dolphins | +6.5 | +6.8 | -0.3 | PASS |
| Rams @ Commanders | +4.5 | +4.5 | PK | PASS |
| Cardinals @ Seahawks | -8.5 | -12.2 | +3.7 | PASS |
| Packers @ Patriots | -3 | -4.6 | +1.6 | PASS |

## Why we're passing

Rams @ Commanders: Pinnacle has Commanders +4.5; our model makes it +4.5. The best model edge on either side of the spread is 1.2%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Browns @ Saints: market -3.5, model -0.5 (gap -3 pts)
- Broncos @ Panthers: market +3, model +6.8 (gap -3.8 pts)
- Cowboys @ Colts: market +3.5, model PK (gap +3.5 pts)
- Cardinals @ Seahawks: market -8.5, model -12.2 (gap +3.7 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.