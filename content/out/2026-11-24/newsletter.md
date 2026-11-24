# Mostly Pass: NFL Week 12 research, 2026-11-24

*Most games aren't bets.* Today's card: **0 BET · 7 LEAN · 9 PASS** across 16 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Vikings -7 +106 (lowvig): Pinnacle fair +105, model -134, would clear the BET bar at -118 or better
- Bills -2.5 -114 (lowvig): Pinnacle fair -108, model -161, would clear the BET bar at -142 or better
- Rams -2.5 -104 (pinnacle): Pinnacle fair +102, model -137, would clear the BET bar at -121 or better
- Jaguars -14.5 -104 (draftkings): Pinnacle fair -100, model -129, would clear the BET bar at -114 or better
- Ravens +6.5 +101 (pinnacle): Pinnacle fair +107, model -108, would clear the BET bar at +104 or better
- Seahawks +3 +105 (lowvig): Pinnacle fair +109, model -102, would clear the BET bar at +111 or better
- Bengals -10 +100 (lowvig): Pinnacle fair +104, model -106, would clear the BET bar at +106 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Packers @ Rams | -2.5 | -5.1 | +2.6 | LEAN |
| Chiefs @ Bills | -2.5 | -6.5 | +4 | LEAN |
| Ravens @ Texans | -6.5 | -5.8 | -0.7 | LEAN |
| Falcons @ Vikings | -7 | -9.4 | +2.4 | LEAN |
| Titans @ Jaguars | -14.5 | -16.6 | +2.1 | LEAN |
| Saints @ Bengals | -10 | -10.5 | +0.5 | LEAN |
| Seahawks @ 49ers | -3 | -2.8 | -0.2 | LEAN |
| Bears @ Lions | +2.5 | -2.2 | +4.7 | PASS |
| Eagles @ Cowboys | -8.5 | -3.6 | -4.9 | PASS |
| Broncos @ Steelers | +2.5 | +3.3 | -0.8 | PASS |
| Jets @ Dolphins | +3.5 | -2.5 | +6 | PASS |
| Giants @ Colts | +6.5 | +2.5 | +4 | PASS |
| Patriots @ Chargers | -1 | +4.9 | -5.9 | PASS |
| Commanders @ Cardinals | +7.5 | +2.5 | +5 | PASS |
| Raiders @ Browns | -4.5 | -4.8 | +0.3 | PASS |
| Panthers @ Buccaneers | -3 | -3.2 | +0.2 | PASS |

## Why we're passing

Panthers @ Buccaneers: Pinnacle has Buccaneers -3; our model makes it -3.2. The best model edge on either side of the spread is 0.7%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Bears @ Lions: market +2.5, model -2.2 (gap +4.7 pts)
- Eagles @ Cowboys: market -8.5, model -3.6 (gap -4.9 pts)
- Jets @ Dolphins: market +3.5, model -2.5 (gap +6 pts)
- Giants @ Colts: market +6.5, model +2.5 (gap +4 pts)
- Patriots @ Chargers: market -1, model +4.9 (gap -5.9 pts)
- Commanders @ Cardinals: market +7.5, model +2.5 (gap +5 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.