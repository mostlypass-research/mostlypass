# Mostly Pass: NFL Week 7 research, 2026-10-25

*Most games aren't bets.* Today's card: **0 BET · 7 LEAN · 6 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Broncos -4.5 -104 (lowvig): Pinnacle fair -101, model -147, would clear the BET bar at -130 or better
- Giants +10.5 -108 (lowvig): Pinnacle fair -105, model -151, would clear the BET bar at -133 or better
- Seahawks -3 +100 (draftkings): Pinnacle fair +103, model -124, would clear the BET bar at -109 or better
- Dolphins +4 -105 (lowvig): Pinnacle fair -106, model -129, would clear the BET bar at -114 or better
- Rams -3.5 +105 (pinnacle): Pinnacle fair +110, model -113, would clear the BET bar at +100 or better
- Browns -1.5 -110 (draftkings): Pinnacle fair -105, model -129, would clear the BET bar at -115 or better
- Packers +3.5 +100 (lowvig): Pinnacle fair +105, model -110, would clear the BET bar at +102 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Giants @ Texans | -10.5 | -7 | -3.5 | LEAN |
| Browns @ Titans | +1.5 | +3.7 | -2.2 | LEAN |
| Dolphins @ Jets | -4 | -1.9 | -2.1 | LEAN |
| Broncos @ Cardinals | +4.5 | +7.7 | -3.2 | LEAN |
| Packers @ Lions | -3.5 | -2.7 | -0.8 | LEAN |
| Rams @ Raiders | +3.5 | +4.5 | -1 | LEAN |
| Chiefs @ Seahawks | -3 | -4.8 | +1.8 | LEAN |
| Steelers @ Saints | +3 | +3.3 | -0.3 | PASS |
| Buccaneers @ Panthers | -2.5 | -4.4 | +1.9 | PASS |
| Bengals @ Ravens | +3 | -3.5 | +6.5 | PASS |
| 49ers @ Falcons | +2.5 | +6.7 | -4.2 | PASS |
| Colts @ Vikings | -7.5 | -10.5 | +3 | PASS |
| Cowboys @ Eagles | +4.5 | -4.6 | +9.1 | PASS |

## Why we're passing

Steelers @ Saints: Pinnacle has Saints +3; our model makes it +3.3. The best model edge on either side of the spread is 1.5%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Bengals @ Ravens: market +3, model -3.5 (gap +6.5 pts)
- 49ers @ Falcons: market +2.5, model +6.7 (gap -4.2 pts)
- Colts @ Vikings: market -7.5, model -10.5 (gap +3 pts)
- Cowboys @ Eagles: market +4.5, model -4.6 (gap +9.1 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.