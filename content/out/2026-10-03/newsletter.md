# Mostly Pass: NFL Week 4 research, 2026-10-03

*Most games aren't bets.* Today's card: **0 BET · 6 LEAN · 9 PASS** across 15 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Texans -3 +100 (pinnacle): Pinnacle fair +106, model -134, would clear the BET bar at -119 or better
- Buccaneers +3.5 -115 (fanduel): Pinnacle fair -112, model -152, would clear the BET bar at -134 or better
- Raiders +4.5 -105 (draftkings): Pinnacle fair -100, model -118, would clear the BET bar at -104 or better
- Vikings -10 -101 (lowvig): Pinnacle fair +103, model -112, would clear the BET bar at +101 or better
- Patriots +7 -113 (lowvig): Pinnacle fair -107, model -123, would clear the BET bar at -109 or better
- Broncos +2.5 +103 (lowvig): Pinnacle fair +105, model -104, would clear the BET bar at +108 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Patriots @ Bills | -7 | -5.2 | -1.8 | LEAN |
| Packers @ Buccaneers | +3.5 | PK | +3.5 | LEAN |
| Cowboys @ Texans | -3 | -5.5 | +2.5 | LEAN |
| Dolphins @ Vikings | -10 | -10.9 | +0.9 | LEAN |
| Broncos @ 49ers | -2.5 | -2.1 | -0.4 | LEAN |
| Chiefs @ Raiders | +4.5 | +3.1 | +1.4 | LEAN |
| Colts @ Commanders | +4.5 | -1.9 | +6.4 | PASS |
| Jets @ Bears | -3.5 | -10.1 | +6.6 | PASS |
| Rams @ Eagles | +3.5 | -0.7 | +4.2 | PASS |
| Jaguars @ Bengals | -2.5 | +1.2 | -3.7 | PASS |
| Cardinals @ Giants | +2.5 | -3.1 | +5.6 | PASS |
| Titans @ Ravens | -11.5 | -12.3 | +0.8 | PASS |
| Chargers @ Seahawks | -7.5 | -11.8 | +4.3 | PASS |
| Lions @ Panthers | +4 | +3.4 | +0.6 | PASS |
| Falcons @ Saints | -2 | -1.1 | -0.9 | PASS |

## Why we're passing

Lions @ Panthers: Pinnacle has Panthers +4; our model makes it +3.4. The best model edge on either side of the spread is -0.4%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Colts @ Commanders: market +4.5, model -1.9 (gap +6.4 pts)
- Jets @ Bears: market -3.5, model -10.1 (gap +6.6 pts)
- Rams @ Eagles: market +3.5, model -0.7 (gap +4.2 pts)
- Jaguars @ Bengals: market -2.5, model +1.2 (gap -3.7 pts)
- Cardinals @ Giants: market +2.5, model -3.1 (gap +5.6 pts)
- Chargers @ Seahawks: market -7.5, model -11.8 (gap +4.3 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals published: 4, none graded yet

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.