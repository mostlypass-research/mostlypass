# Mostly Pass: NFL Week 7 research, 2026-10-20

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 7 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Broncos -4 -110 (lowvig): Pinnacle fair -104, model -156, would clear the BET bar at -138 or better
- Dolphins +5.5 -115 (pinnacle): Pinnacle fair -109, model -154, would clear the BET bar at -136 or better
- Giants +10 -107 (pinnacle): Pinnacle fair -101, model -142, would clear the BET bar at -126 or better
- Seahawks -2.5 -108 (pinnacle): Pinnacle fair -102, model -131, would clear the BET bar at -116 or better
- Browns -1.5 -108 (fanduel): Pinnacle fair -102, model -129, would clear the BET bar at -115 or better
- Panthers -3 -109 (lowvig): Pinnacle fair -104, model -118, would clear the BET bar at -104 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Buccaneers @ Panthers | -3 | -4.4 | +1.4 | LEAN |
| Giants @ Texans | -10 | -7 | -3 | LEAN |
| Browns @ Titans | +1.5 | +3.7 | -2.2 | LEAN |
| Dolphins @ Jets | -5.5 | -1.9 | -3.6 | LEAN |
| Broncos @ Cardinals | +4 | +7.7 | -3.7 | LEAN |
| Chiefs @ Seahawks | -2.5 | -4.8 | +2.3 | LEAN |
| Patriots @ Bears | -3 | +0.5 | -3.5 | PASS |
| Steelers @ Saints | +3.5 | +3.3 | +0.2 | PASS |
| Bengals @ Ravens | -2.5 | -3.5 | +1 | PASS |
| Colts @ Vikings | -6.5 | -10.5 | +4 | PASS |
| Packers @ Lions | -3 | -2.7 | -0.3 | PASS |
| Rams @ Raiders | +4 | +4.5 | -0.5 | PASS |
| Cowboys @ Eagles | +4.5 | -4.6 | +9.1 | PASS |

## Why we're passing

Steelers @ Saints: Pinnacle has Saints +3.5; our model makes it +3.3. The best model edge on either side of the spread is 0.3%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Patriots @ Bears: market -3, model +0.5 (gap -3.5 pts)
- Colts @ Vikings: market -6.5, model -10.5 (gap +4 pts)
- Cowboys @ Eagles: market +4.5, model -4.6 (gap +9.1 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.