# Mostly Pass: NFL Week 10 research, 2026-11-10

*Most games aren't bets.* Today's card: **0 BET · 9 LEAN · 5 PASS** across 14 games. All signals are PAPER, timestamped before kickoff, and graded automatically against the Pinnacle close.

## Bets

None. Our model has not beaten NFL closing lines out of sample, so it is not allowed to call anything a bet. What follows is research.

## Where the model disagrees on the spread (paper signals)

- Vikings +5.5 -117 (pinnacle): Pinnacle fair -110, model -163, would clear the BET bar at -144 or better
- Jaguars -10.5 -105 (fanduel): Pinnacle fair -104, model -127, would clear the BET bar at -113 or better
- Browns +5 -108 (pinnacle): Pinnacle fair -102, model -131, would clear the BET bar at -116 or better
- Cardinals +9.5 -107 (lowvig): Pinnacle fair -103, model -126, would clear the BET bar at -112 or better
- Giants -2.5 -105 (pinnacle): Pinnacle fair +101, model -120, would clear the BET bar at -106 or better
- Ravens -5 -105 (lowvig): Pinnacle fair -100, model -117, would clear the BET bar at -104 or better
- 49ers -4 -105 (lowvig): Pinnacle fair +101, model -115, would clear the BET bar at -102 or better
- Steelers +3.5 -105 (lowvig): Pinnacle fair -102, model -114, would clear the BET bar at -101 or better

## Every game: market vs model

| Game | Pinnacle spread (home) | Model spread (home) | Gap (pts) | Verdict |
| --- | --- | --- | --- | --- |
| Commanders @ Giants | -2.5 | -4 | +1.5 | LEAN |
| Jaguars @ Titans | +10.5 | +12.5 | -2 | LEAN |
| Chiefs @ Falcons | +3.5 | +3.5 | PK | LEAN |
| Vikings @ Packers | -5.5 | -1.4 | -4.1 | LEAN |
| Texans @ Browns | +5 | +2.7 | +2.3 | LEAN |
| Rams @ Cardinals | +9.5 | +7.5 | +2 | LEAN |
| 49ers @ Cowboys | +4 | +5.2 | -1.2 | LEAN |
| Steelers @ Bengals | -3.5 | -2.4 | -1.1 | LEAN |
| Chargers @ Ravens | -5 | -6.3 | +1.3 | LEAN |
| Patriots @ Lions | -2.5 | -3.2 | +0.7 | PASS |
| Bills @ Jets | +7.5 | +13.7 | -6.2 | PASS |
| Dolphins @ Colts | -2.5 | -2.9 | +0.4 | PASS |
| Panthers @ Saints | -1 | -1.6 | +0.6 | PASS |
| Seahawks @ Raiders | +4.5 | +8.3 | -3.8 | PASS |

## Why we're passing

Dolphins @ Colts: Pinnacle has Colts -2.5; our model makes it -2.9. The best model edge on either side of the spread is -0.7%, under the 1.5% bar for even a paper signal. The price is fair, so not betting is the default.

## When the model is probably wrong

A big gap between our model and the sharp market usually means the model is missing information, such as a quarterback change or an injury, not that we found a mispricing. These games are automatic passes:

- Bills @ Jets: market +7.5, model +13.7 (gap -6.2 pts)
- Seahawks @ Raiders: market +4.5, model +8.3 (gap -3.8 pts)

## The record

BET: none (the model has not earned BETs) · LEAN paper signals: 3-1-0, mean CLV n/a (n=0)

---
How this works: https://mostlypass.pages.dev/methodology/ · Every row: https://mostlypass.pages.dev/record/record.csv
Research, not betting advice. Paper signals only. 21+. Gambling problem? Call 1-800-GAMBLER.