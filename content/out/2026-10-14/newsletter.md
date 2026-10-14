# Mostly Pass: NFL Week 6 research, 2026-10-14

*Most games aren't bets.* Today's card: **0 BET · 7 LEAN · 7 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Bills -4.5 -105 (lowvig): Pinnacle fair -102, model -148, would clear the BET bar at -131 or better
- Jaguars -2.5 -110 (lowvig): Pinnacle fair -106, model -145, would clear the BET bar at -128 or better
- Colts -7 -103 (lowvig): Pinnacle fair +102, model -129, would clear the BET bar at -114 or better
- Falcons +3 -105 (fanduel): Pinnacle fair -108, model -127, would clear the BET bar at -112 or better
- Broncos +2.5 -101 (lowvig): Pinnacle fair +102, model -120, would clear the BET bar at -106 or better
- Cardinals +13.5 -115 (pinnacle): Pinnacle fair -108, model -134, would clear the BET bar at -119 or better
- Buccaneers +2.5 -105 (fanduel): Pinnacle fair -102, model -114, would clear the BET bar at -101 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Seahawks @ Broncos | +2.5 | +1 | +1.5 | LEAN |
| Texans @ Jaguars | -2.5 | -5.6 | +3.1 | LEAN |
| Steelers @ Buccaneers | +2.5 | +1.4 | +1.1 | LEAN |
| Bears @ Falcons | +3 | +1 | +2 | LEAN |
| Titans @ Colts | -7 | -9.2 | +2.2 | LEAN |
| Cardinals @ Rams | -13.5 | -11 | -2.5 | LEAN |
| Bills @ Raiders | +4.5 | +7.8 | -3.3 | LEAN |
| Jets @ Patriots | -7.5 | -11.6 | +4.1 | PASS |
| Saints @ Giants | +1 | -4.5 | +5.5 | PASS |
| Panthers @ Eagles | -1 | -4.9 | +3.9 | PASS |
| Ravens @ Browns | +4.5 | +4.2 | +0.3 | PASS |
| Chargers @ Chiefs | -8 | -8.1 | +0.1 | PASS |
| Cowboys @ Packers | -1 | -5.2 | +4.2 | PASS |
| Commanders @ 49ers | -7.5 | -11.5 | +4 | PASS |

## Why we're passing

Chargers @ Chiefs: Pinnacle has Chiefs -8; our model makes it -8.1. The best model edge on either side of the spread is -1.3%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Jets @ Patriots: market -7.5, model -11.6 (gap +4.1 pts)
- Saints @ Giants: market +1, model -4.5 (gap +5.5 pts)
- Panthers @ Eagles: market -1, model -4.9 (gap +3.9 pts)
- Cowboys @ Packers: market -1, model -5.2 (gap +4.2 pts)
- Commanders @ 49ers: market -7.5, model -11.5 (gap +4 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.