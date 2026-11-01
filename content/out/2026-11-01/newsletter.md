# Mostly Pass: NFL Week 8 research, 2026-11-01

*Most games aren't bets.* Today's card: **0 BET · 4 LEAN · 9 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Seahawks -3 -106 (pinnacle): Pinnacle fair -100, model -143, would clear the BET bar at -126 or better
- Steelers -3.5 -101 (lowvig): Pinnacle fair +103, model -135, would clear the BET bar at -119 or better
- Rams -6.5 -105 (lowvig): Pinnacle fair -103, model -135, would clear the BET bar at -120 or better
- Raiders +1 +104 (lowvig): Pinnacle fair +109, model -108, would clear the BET bar at +105 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Raiders @ Jets | -1 | -0.4 | -0.6 | LEAN |
| Browns @ Steelers | -3.5 | -6 | +2.5 | LEAN |
| Chargers @ Rams | -6.5 | -9 | +2.5 | LEAN |
| Bears @ Seahawks | -3 | -6 | +3 | LEAN |
| Colts @ Jaguars | -10.5 | -9.7 | -0.8 | PASS |
| Vikings @ Lions | -3.5 | +0.9 | -4.4 | PASS |
| Falcons @ Buccaneers | -2.5 | -1.5 | -1 | PASS |
| Cardinals @ Cowboys | -7.5 | -6 | -1.5 | PASS |
| Titans @ Bengals | -13 | -12.6 | -0.4 | PASS |
| Ravens @ Bills | -3.5 | -7.5 | +4 | PASS |
| Patriots @ Dolphins | +7 | +6.8 | +0.2 | PASS |
| Chiefs @ Broncos | +1 | -4.4 | +5.4 | PASS |
| Eagles @ Commanders | -6 | -0.1 | -5.9 | PASS |

## Why we're passing

Patriots @ Dolphins: Pinnacle has Dolphins +7; our model makes it +6.8. The best model edge on either side of the spread is -0.7%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Vikings @ Lions: market -3.5, model +0.9 (gap -4.4 pts)
- Ravens @ Bills: market -3.5, model -7.5 (gap +4 pts)
- Chiefs @ Broncos: market +1, model -4.4 (gap +5.4 pts)
- Eagles @ Commanders: market -6, model -0.1 (gap -5.9 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.