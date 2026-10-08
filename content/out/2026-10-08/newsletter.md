# Mostly Pass: NFL Week 5 research, 2026-10-08

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 9 PASS** across 15 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Giants +3.5 +100 (lowvig): Pinnacle fair +104, model -143, would clear the BET bar at -126 or better
- Bills +3 +102 (lowvig): Pinnacle fair +108, model -138, would clear the BET bar at -122 or better
- Dolphins +7 -115 (pinnacle): Pinnacle fair -108, model -160, would clear the BET bar at -141 or better
- Eagles +7.5 -105 (lowvig): Pinnacle fair -100, model -132, would clear the BET bar at -117 or better
- Broncos -3.5 +105 (lowvig): Pinnacle fair +109, model -110, would clear the BET bar at +102 or better
- Cardinals +5.5 -103 (lowvig): Pinnacle fair +103, model -116, would clear the BET bar at -102 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Eagles @ Jaguars | -7.5 | -5.2 | -2.3 | LEAN |
| Bengals @ Dolphins | +7 | +3 | +4 | LEAN |
| Giants @ Commanders | -3.5 | -0.5 | -3 | LEAN |
| Broncos @ Chargers | +3.5 | +4.3 | -0.8 | LEAN |
| Lions @ Cardinals | +5.5 | +4.3 | +1.2 | LEAN |
| Bills @ Rams | -3 | -0.3 | -2.7 | LEAN |
| Buccaneers @ Cowboys | -8 | -4.2 | -3.8 | PASS |
| Bears @ Packers | +2.5 | +1.5 | +1 | PASS |
| Vikings @ Saints | +2 | +6.9 | -4.9 | PASS |
| Colts @ Steelers | -2.5 | -3.2 | +0.7 | PASS |
| Raiders @ Patriots | -4 | -8.7 | +4.7 | PASS |
| Browns @ Jets | -1.5 | +1.9 | -3.4 | PASS |
| Texans @ Titans | +7.5 | +7.1 | +0.4 | PASS |
| 49ers @ Seahawks | -3 | -4.2 | +1.2 | PASS |
| Ravens @ Falcons | -3.5 | +1.1 | -4.6 | PASS |

## Why we're passing

Texans @ Titans: Pinnacle has Titans +7.5; our model makes it +7.1. The best model edge on either side of the spread is -0.1%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Buccaneers @ Cowboys: market -8, model -4.2 (gap -3.8 pts)
- Vikings @ Saints: market +2, model +6.9 (gap -4.9 pts)
- Raiders @ Patriots: market -4, model -8.7 (gap +4.7 pts)
- Browns @ Jets: market -1.5, model +1.9 (gap -3.4 pts)
- Ravens @ Falcons: market -3.5, model +1.1 (gap -4.6 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.