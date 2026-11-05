# Mostly Pass: NFL Week 9 research, 2026-11-05

*Most games aren't bets.* Today's card: **0 BET · 7 LEAN · 8 PASS** across 15 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Vikings +3 +102 (pinnacle): Pinnacle fair +108, model -137, would clear the BET bar at -122 or better
- Browns +3 -101 (lowvig): Pinnacle fair +101, model -135, would clear the BET bar at -119 or better
- Chargers +4.5 +101 (pinnacle): Pinnacle fair +107, model -117, would clear the BET bar at -104 or better
- Chiefs -10 -102 (lowvig): Pinnacle fair +103, model -114, would clear the BET bar at -101 or better
- Bears -6.5 +104 (pinnacle): Pinnacle fair +110, model -106, would clear the BET bar at +106 or better
- 49ers -10 -101 (pinnacle): Pinnacle fair +105, model -111, would clear the BET bar at +102 or better
- Patriots -3 -110 (fanduel): Pinnacle fair -107, model -120, would clear the BET bar at -107 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Jets @ Chiefs | -10 | -11.1 | +1.1 | LEAN |
| Browns @ Saints | -3 | -0.5 | -2.5 | LEAN |
| Texans @ Chargers | +4.5 | +3.2 | +1.3 | LEAN |
| Raiders @ 49ers | -10 | -10.9 | +0.9 | LEAN |
| Packers @ Patriots | -3 | -4.6 | +1.6 | LEAN |
| Buccaneers @ Bears | -6.5 | -7 | +0.5 | LEAN |
| Bills @ Vikings | +3 | +0.3 | +2.7 | LEAN |
| Jaguars @ Ravens | +10.5 | +2.8 | +7.7 | PASS |
| Bengals @ Falcons | +3 | +2.6 | +0.4 | PASS |
| Broncos @ Panthers | +3 | +6.8 | -3.8 | PASS |
| Cowboys @ Colts | +5.5 | PK | +5.5 | PASS |
| Lions @ Dolphins | +7.5 | +6.8 | +0.7 | PASS |
| Rams @ Commanders | +5.5 | +4.5 | +1 | PASS |
| Giants @ Eagles | +3 | -0.9 | +3.9 | PASS |
| Cardinals @ Seahawks | -8.5 | -12.2 | +3.7 | PASS |

## Why we're passing

Bengals @ Falcons: Pinnacle has Falcons +3; our model makes it +2.6. The best model edge on either side of the spread is 1.5%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Jaguars @ Ravens: market +10.5, model +2.8 (gap +7.7 pts)
- Broncos @ Panthers: market +3, model +6.8 (gap -3.8 pts)
- Cowboys @ Colts: market +5.5, model PK (gap +5.5 pts)
- Giants @ Eagles: market +3, model -0.9 (gap +3.9 pts)
- Cardinals @ Seahawks: market -8.5, model -12.2 (gap +3.7 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.