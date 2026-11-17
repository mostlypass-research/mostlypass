# Mostly Pass: NFL Week 11 research, 2026-11-17

*Most games aren't bets.* Today's card: **0 BET · 5 LEAN · 8 PASS** across 13 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Broncos -10 -108 (lowvig): Pinnacle fair -102, model -140, would clear the BET bar at -124 or better
- Ravens +2.5 +102 (lowvig): Pinnacle fair +104, model -122, would clear the BET bar at -108 or better
- Commanders +6.5 -105 (lowvig): Pinnacle fair -102, model -120, would clear the BET bar at -106 or better
- Lions -6.5 -102 (pinnacle): Pinnacle fair +104, model -115, would clear the BET bar at -102 or better
- Chargers -3 -116 (lowvig): Pinnacle fair -110, model -129, would clear the BET bar at -114 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Buccaneers @ Lions | -6.5 | -7.7 | +1.2 | LEAN |
| Ravens @ Panthers | -2.5 | -0.8 | -1.7 | LEAN |
| Jets @ Chargers | -3 | -5.1 | +2.1 | LEAN |
| Raiders @ Broncos | -10 | -12.8 | +2.8 | LEAN |
| Bengals @ Commanders | +6.5 | +5 | +1.5 | LEAN |
| Colts @ Texans | -13 | -7.5 | -5.5 | PASS |
| Saints @ Bears | -11.5 | -11.4 | -0.1 | PASS |
| Cardinals @ Chiefs | -16 | -11.4 | -4.6 | PASS |
| Dolphins @ Bills | -17 | -16.7 | -0.3 | PASS |
| Titans @ Cowboys | -8 | -8.7 | +0.7 | PASS |
| Steelers @ Eagles | +4.5 | +4 | +0.5 | PASS |
| Jaguars @ Giants | +6 | +6.1 | -0.1 | PASS |
| Vikings @ 49ers | -3 | -2.8 | -0.2 | PASS |

## Why we're passing

Saints @ Bears: Pinnacle has Bears -11.5; our model makes it -11.4. The best model edge on either side of the spread is -0.9%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Colts @ Texans: market -13, model -7.5 (gap -5.5 pts)
- Cardinals @ Chiefs: market -16, model -11.4 (gap -4.6 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.