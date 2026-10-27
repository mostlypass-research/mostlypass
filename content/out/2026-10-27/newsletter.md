# Mostly Pass: NFL Week 8 research, 2026-10-27

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 4 PASS** across 10 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Rams -7 +108 (pinnacle): Pinnacle fair +114, model -127, would clear the BET bar at -113 or better
- Steelers -4 +105 (pinnacle): Pinnacle fair +111, model -127, would clear the BET bar at -112 or better
- Bengals -10.5 +101 (pinnacle): Pinnacle fair +107, model -128, would clear the BET bar at -114 or better
- Packers -4 +102 (pinnacle): Pinnacle fair +108, model -119, would clear the BET bar at -106 or better
- Jaguars -7.5 -110 (fanduel): Pinnacle fair -105, model -130, would clear the BET bar at -115 or better
- Jets +1 -107 (lowvig): Pinnacle fair -107, model -118, would clear the BET bar at -104 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Panthers @ Packers | -4 | -5.5 | +1.5 | LEAN |
| Colts @ Jaguars | -7.5 | -9.7 | +2.2 | LEAN |
| Raiders @ Jets | +1 | -0.4 | +1.4 | LEAN |
| Titans @ Bengals | -10.5 | -12.6 | +2.1 | LEAN |
| Browns @ Steelers | -4 | -6 | +2 | LEAN |
| Chargers @ Rams | -7 | -9 | +2 | LEAN |
| Vikings @ Lions | -3 | +0.9 | -3.9 | PASS |
| Falcons @ Buccaneers | -2 | -1.5 | -0.5 | PASS |
| Patriots @ Dolphins | +7.5 | +6.8 | +0.7 | PASS |
| Bears @ Seahawks | -3.5 | -6 | +2.5 | PASS |

## Why we're passing

Falcons @ Buccaneers: Pinnacle has Buccaneers -2; our model makes it -1.5. The best model edge on either side of the spread is 0.6%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Vikings @ Lions: market -3, model +0.9 (gap -3.9 pts)
- Bears @ Seahawks: market -3.5, model -6 (gap +2.5 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.