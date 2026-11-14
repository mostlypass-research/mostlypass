# Mostly Pass: NFL Week 10 research, 2026-11-14

*Most games aren't bets.* Today's card: **0 BET · 9 LEAN · 4 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Ravens -4.5 -103 (lowvig): Pinnacle fair +103, model -124, would clear the BET bar at -110 or better
- Cardinals +9.5 -106 (lowvig): Pinnacle fair -101, model -126, would clear the BET bar at -112 or better
- Jaguars -10.5 -110 (fanduel): Pinnacle fair -104, model -127, would clear the BET bar at -113 or better
- Seahawks -6.5 -109 (lowvig): Pinnacle fair -103, model -124, would clear the BET bar at -110 or better
- Chiefs -3.5 +113 (pinnacle): Pinnacle fair +119, model -100, would clear the BET bar at +112 or better
- Dolphins +4 -101 (pinnacle): Pinnacle fair +105, model -114, would clear the BET bar at -101 or better
- Browns +5 -116 (pinnacle): Pinnacle fair -109, model -131, would clear the BET bar at -116 or better
- 49ers -4 -103 (pinnacle): Pinnacle fair +103, model -115, would clear the BET bar at -102 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Jaguars @ Titans | +10.5 | +12.5 | -2 | LEAN |
| Chiefs @ Falcons | +3.5 | +3.5 | PK | LEAN |
| Vikings @ Packers | -3 | -1.4 | -1.6 | LEAN |
| Dolphins @ Colts | -4 | -2.9 | -1.1 | LEAN |
| Texans @ Browns | +5 | +2.7 | +2.3 | LEAN |
| Seahawks @ Raiders | +6.5 | +8.3 | -1.8 | LEAN |
| Rams @ Cardinals | +9.5 | +7.5 | +2 | LEAN |
| 49ers @ Cowboys | +4 | +5.2 | -1.2 | LEAN |
| Chargers @ Ravens | -4.5 | -6.3 | +1.8 | LEAN |
| Patriots @ Lions | -2.5 | -3.2 | +0.7 | PASS |
| Bills @ Jets | +8.5 | +13.7 | -5.2 | PASS |
| Panthers @ Saints | -2.5 | -1.6 | -0.9 | PASS |
| Steelers @ Bengals | -3.5 | -2.4 | -1.1 | PASS |

## Why we're passing

Patriots @ Lions: Pinnacle has Lions -2.5; our model makes it -3.2. The best model edge on either side of the spread is -1.1%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Bills @ Jets: market +8.5, model +13.7 (gap -5.2 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.