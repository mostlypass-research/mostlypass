# Mostly Pass: NFL Week 8 research, 2026-10-29

*Most games aren't bets.* Today's card: **0 BET · 5 LEAN · 9 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Rams -7 +108 (pinnacle): Pinnacle fair +114, model -127, would clear the BET bar at -113 or better
- Steelers -3.5 -101 (pinnacle): Pinnacle fair +105, model -135, would clear the BET bar at -119 or better
- Bengals -10.5 +100 (lowvig): Pinnacle fair +103, model -128, would clear the BET bar at -114 or better
- Packers -4 +101 (pinnacle): Pinnacle fair +107, model -119, would clear the BET bar at -106 or better
- Falcons +2.5 -103 (pinnacle): Pinnacle fair +103, model -113, would clear the BET bar at -100 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Panthers @ Packers | -4 | -5.5 | +1.5 | LEAN |
| Falcons @ Buccaneers | -2.5 | -1.5 | -1 | LEAN |
| Titans @ Bengals | -10.5 | -12.6 | +2.1 | LEAN |
| Browns @ Steelers | -3.5 | -6 | +2.5 | LEAN |
| Chargers @ Rams | -7 | -9 | +2 | LEAN |
| Colts @ Jaguars | -10.5 | -9.7 | -0.8 | PASS |
| Vikings @ Lions | -3 | +0.9 | -3.9 | PASS |
| Cardinals @ Cowboys | -7.5 | -6 | -1.5 | PASS |
| Raiders @ Jets | -1 | -0.4 | -0.6 | PASS |
| Ravens @ Bills | -3.5 | -7.5 | +4 | PASS |
| Patriots @ Dolphins | +7 | +6.8 | +0.2 | PASS |
| Chiefs @ Broncos | +1.5 | -4.4 | +5.9 | PASS |
| Eagles @ Commanders | -5.5 | -0.1 | -5.4 | PASS |
| Bears @ Seahawks | -3.5 | -6 | +2.5 | PASS |

## Why we're passing

Patriots @ Dolphins: Pinnacle has Dolphins +7; our model makes it +6.8. The best model edge on either side of the spread is -0.7%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Vikings @ Lions: market -3, model +0.9 (gap -3.9 pts)
- Ravens @ Bills: market -3.5, model -7.5 (gap +4 pts)
- Chiefs @ Broncos: market +1.5, model -4.4 (gap +5.9 pts)
- Eagles @ Commanders: market -5.5, model -0.1 (gap -5.4 pts)
- Bears @ Seahawks: market -3.5, model -6 (gap +2.5 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.