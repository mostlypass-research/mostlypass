# Mostly Pass: NFL Week 9 research, 2026-11-07

*Most games aren't bets.* Today's card: **0 BET · 8 LEAN · 6 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Vikings +3 -101 (pinnacle): Pinnacle fair +105, model -137, would clear the BET bar at -122 or better
- Chargers +6 -106 (pinnacle): Pinnacle fair -100, model -140, would clear the BET bar at -124 or better
- Browns +3.5 -112 (draftkings): Pinnacle fair -106, model -143, would clear the BET bar at -126 or better
- Chiefs -10 +111 (pinnacle): Pinnacle fair +117, model -114, would clear the BET bar at -101 or better
- 49ers -10 +103 (lowvig): Pinnacle fair +109, model -111, would clear the BET bar at +102 or better
- Falcons +3 +105 (pinnacle): Pinnacle fair +111, model -105, would clear the BET bar at +107 or better
- Bears -6.5 +104 (pinnacle): Pinnacle fair +110, model -106, would clear the BET bar at +106 or better
- Patriots -3 -110 (fanduel): Pinnacle fair -108, model -120, would clear the BET bar at -107 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Bengals @ Falcons | +3 | +2.6 | +0.4 | LEAN |
| Jets @ Chiefs | -10 | -11.1 | +1.1 | LEAN |
| Browns @ Saints | -3.5 | -0.5 | -3 | LEAN |
| Texans @ Chargers | +6 | +3.2 | +2.8 | LEAN |
| Raiders @ 49ers | -10 | -10.9 | +0.9 | LEAN |
| Packers @ Patriots | -3 | -4.6 | +1.6 | LEAN |
| Buccaneers @ Bears | -6.5 | -7 | +0.5 | LEAN |
| Bills @ Vikings | +3 | +0.3 | +2.7 | LEAN |
| Broncos @ Panthers | +2.5 | +6.8 | -4.3 | PASS |
| Cowboys @ Colts | +5.5 | PK | +5.5 | PASS |
| Lions @ Dolphins | +6.5 | +6.8 | -0.3 | PASS |
| Rams @ Commanders | +4.5 | +4.5 | PK | PASS |
| Giants @ Eagles | +3 | -0.9 | +3.9 | PASS |
| Cardinals @ Seahawks | -8.5 | -12.2 | +3.7 | PASS |

## Why we're passing

Rams @ Commanders: Pinnacle has Commanders +4.5; our model makes it +4.5. The best model edge on either side of the spread is -0.4%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Broncos @ Panthers: market +2.5, model +6.8 (gap -4.3 pts)
- Cowboys @ Colts: market +5.5, model PK (gap +5.5 pts)
- Giants @ Eagles: market +3, model -0.9 (gap +3.9 pts)
- Cardinals @ Seahawks: market -8.5, model -12.2 (gap +3.7 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.