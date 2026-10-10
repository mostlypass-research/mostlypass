# Mostly Pass: NFL Week 5 research, 2026-10-10

*Most games aren't bets.* Today's card: **0 BET · 5 LEAN · 9 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Giants +3.5 -108 (fanduel): Pinnacle fair -108, model -143, would clear the BET bar at -126 or better
- Eagles +7.5 -102 (pinnacle): Pinnacle fair +104, model -132, would clear the BET bar at -117 or better
- Seahawks -3.5 +108 (pinnacle): Pinnacle fair +114, model -109, would clear the BET bar at +104 or better
- Cardinals +5.5 -105 (lowvig): Pinnacle fair -104, model -116, would clear the BET bar at -102 or better
- Texans -7.5 +112 (pinnacle): Pinnacle fair +118, model +105, would clear the BET bar at +118 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Eagles @ Jaguars | -7.5 | -5.2 | -2.3 | LEAN |
| Texans @ Titans | +7.5 | +7.1 | +0.4 | LEAN |
| Giants @ Commanders | -3.5 | -0.5 | -3 | LEAN |
| 49ers @ Seahawks | -3.5 | -4.2 | +0.7 | LEAN |
| Lions @ Cardinals | +5.5 | +4.3 | +1.2 | LEAN |
| Bears @ Packers | +1 | +1.5 | -0.5 | PASS |
| Vikings @ Saints | +2 | +6.9 | -4.9 | PASS |
| Colts @ Steelers | -3 | -3.2 | +0.2 | PASS |
| Raiders @ Patriots | -3.5 | -8.7 | +5.2 | PASS |
| Browns @ Jets | -2.5 | +1.9 | -4.4 | PASS |
| Bengals @ Dolphins | +6.5 | +3 | +3.5 | PASS |
| Broncos @ Chargers | +3.5 | +4.3 | -0.8 | PASS |
| Ravens @ Falcons | -3.5 | +1.1 | -4.6 | PASS |
| Bills @ Rams | -3 | -0.3 | -2.7 | PASS |

## Why we're passing

Colts @ Steelers: Pinnacle has Steelers -3; our model makes it -3.2. The best model edge on either side of the spread is 1.4%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Vikings @ Saints: market +2, model +6.9 (gap -4.9 pts)
- Raiders @ Patriots: market -3.5, model -8.7 (gap +5.2 pts)
- Browns @ Jets: market -2.5, model +1.9 (gap -4.4 pts)
- Bengals @ Dolphins: market +6.5, model +3 (gap +3.5 pts)
- Ravens @ Falcons: market -3.5, model +1.1 (gap -4.6 pts)
- Bills @ Rams: market -3, model -0.3 (gap -2.7 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.