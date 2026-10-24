# Mostly Pass: NFL Week 7 research, 2026-10-24

*Most games aren't bets.* Today's card: **0 BET · 8 LEAN · 5 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Giants +10.5 -108 (lowvig): Pinnacle fair -103, model -151, would clear the BET bar at -133 or better
- Broncos -4.5 -108 (fanduel): Pinnacle fair -102, model -147, would clear the BET bar at -130 or better
- Dolphins +4.5 -104 (fanduel): Pinnacle fair -102, model -137, would clear the BET bar at -121 or better
- Rams -3.5 +111 (pinnacle): Pinnacle fair +117, model -113, would clear the BET bar at +100 or better
- Seahawks -3 +101 (pinnacle): Pinnacle fair +107, model -124, would clear the BET bar at -109 or better
- Browns -1.5 -115 (pinnacle): Pinnacle fair -108, model -129, would clear the BET bar at -115 or better
- Packers +3.5 -102 (lowvig): Pinnacle fair -104, model -110, would clear the BET bar at +102 or better
- Panthers -2.5 -116 (pinnacle): Pinnacle fair -109, model -125, would clear the BET bar at -111 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Buccaneers @ Panthers | -2.5 | -4.4 | +1.9 | LEAN |
| Giants @ Texans | -10.5 | -7 | -3.5 | LEAN |
| Browns @ Titans | +1.5 | +3.7 | -2.2 | LEAN |
| Dolphins @ Jets | -4.5 | -1.9 | -2.6 | LEAN |
| Broncos @ Cardinals | +4.5 | +7.7 | -3.2 | LEAN |
| Packers @ Lions | -3.5 | -2.7 | -0.8 | LEAN |
| Rams @ Raiders | +3.5 | +4.5 | -1 | LEAN |
| Chiefs @ Seahawks | -3 | -4.8 | +1.8 | LEAN |
| Steelers @ Saints | +3 | +3.3 | -0.3 | PASS |
| Bengals @ Ravens | +1 | -3.5 | +4.5 | PASS |
| 49ers @ Falcons | +2.5 | +6.7 | -4.2 | PASS |
| Colts @ Vikings | -6.5 | -10.5 | +4 | PASS |
| Cowboys @ Eagles | +4.5 | -4.6 | +9.1 | PASS |

## Why we're passing

Steelers @ Saints: Pinnacle has Saints +3; our model makes it +3.3. The best model edge on either side of the spread is 0.0%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Bengals @ Ravens: market +1, model -3.5 (gap +4.5 pts)
- 49ers @ Falcons: market +2.5, model +6.7 (gap -4.2 pts)
- Colts @ Vikings: market -6.5, model -10.5 (gap +4 pts)
- Cowboys @ Eagles: market +4.5, model -4.6 (gap +9.1 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.