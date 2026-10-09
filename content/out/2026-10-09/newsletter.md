# Mostly Pass: NFL Week 5 research, 2026-10-09

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 8 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Bills +3 +104 (lowvig): Pinnacle fair +107, model -138, would clear the BET bar at -122 or better
- Giants +4 -105 (lowvig): Pinnacle fair -101, model -151, would clear the BET bar at -134 or better
- Eagles +7.5 -102 (lowvig): Pinnacle fair +102, model -132, would clear the BET bar at -117 or better
- Seahawks -3.5 +104 (pinnacle): Pinnacle fair +110, model -109, would clear the BET bar at +104 or better
- Cardinals +5.5 -103 (lowvig): Pinnacle fair +101, model -116, would clear the BET bar at -102 or better
- Broncos -3.5 +100 (pinnacle): Pinnacle fair +106, model -110, would clear the BET bar at +102 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Eagles @ Jaguars | -7.5 | -5.2 | -2.3 | LEAN |
| Giants @ Commanders | -4 | -0.5 | -3.5 | LEAN |
| Broncos @ Chargers | +3.5 | +4.3 | -0.8 | LEAN |
| 49ers @ Seahawks | -3.5 | -4.2 | +0.7 | LEAN |
| Lions @ Cardinals | +5.5 | +4.3 | +1.2 | LEAN |
| Bills @ Rams | -3 | -0.3 | -2.7 | LEAN |
| Bears @ Packers | +1 | +1.5 | -0.5 | PASS |
| Vikings @ Saints | +2 | +6.9 | -4.9 | PASS |
| Colts @ Steelers | -2.5 | -3.2 | +0.7 | PASS |
| Raiders @ Patriots | -4 | -8.7 | +4.7 | PASS |
| Browns @ Jets | -2.5 | +1.9 | -4.4 | PASS |
| Bengals @ Dolphins | +6.5 | +3 | +3.5 | PASS |
| Texans @ Titans | +7.5 | +7.1 | +0.4 | PASS |
| Ravens @ Falcons | -3.5 | +1.1 | -4.6 | PASS |

## Why we're passing

Texans @ Titans: Pinnacle has Titans +7.5; our model makes it +7.1. The best model edge on either side of the spread is -0.1%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Vikings @ Saints: market +2, model +6.9 (gap -4.9 pts)
- Raiders @ Patriots: market -4, model -8.7 (gap +4.7 pts)
- Browns @ Jets: market -2.5, model +1.9 (gap -4.4 pts)
- Bengals @ Dolphins: market +6.5, model +3 (gap +3.5 pts)
- Ravens @ Falcons: market -3.5, model +1.1 (gap -4.6 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.