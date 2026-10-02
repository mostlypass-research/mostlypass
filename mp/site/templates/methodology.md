## Methodology

**What this is.** Daily quantitative research on NFL game markets. Every game on the slate gets a verdict: BET, LEAN or PASS. Most games are a PASS; that is the point.

**Where the numbers come from.**

1. **Prices.** A morning snapshot from The Odds API across eight books, including Pinnacle. A separate job checks the schedule every 10 minutes and captures Pinnacle's price shortly before each game kicks off. That capture is our closing line. 
2. **Fair market probability.** Pinnacle's two-way market with the vig removed (multiplicative devig). This is the benchmark the model has to beat.
3. **Model probability.** `elo_v0`: a margin-of-victory Elo rating fitted sequentially on nflverse game results (the last six seasons for live ratings; 2007 onward in the backtest), with home-field advantage and preseason regression. Spread = rating difference / 25; win probability from a normal margin distribution with a 13.5-point standard deviation. Parameters are versioned in git and printed with every row.
4. **Edge.** Model probability minus the implied probability of the best available price. **Threshold price** is the worst price at which edge still clears the BET bar.
5. **Verdict.** BET requires an edge of at least 3.0%, no data warnings, and a model that has passed the backtest gate. LEAN (a paper signal) means an edge of 1.5% or more, or a BET-sized edge from a model that has not passed the gate. Everything else is a PASS. Signals are issued only on the point spread, because that is the market the model was tested on; moneyline gaps are shown as research but never become signals. A model that disagrees with the vig-free market by more than 10 percentage points is presumed to be missing information, such as a quarterback change, and that game is forced to PASS.
6. **Grading.** Final scores come from nflverse, with The Odds API as a fallback. The closing price is our own last Pinnacle capture before kickoff. CLV is the closing implied probability minus the implied probability of the price we published. All of it is computed and appended, never edited.

**What the model is not.** It is not a claim of edge. The backtest below is shown whether it is flattering or not. If the model does not beat the close out of sample, it does not emit BETs; it emits research.

**Fail-safes.** Odds older than 3 hours, a missing Pinnacle market, a model error, a scores outage, or any generated number that does not match the database each block publication of a BET for that day.

**Rules of the record.** It is public, timestamped, append-only, auditable and automatically graded. It is our own automated database and has not been independently verified. Every signal is PAPER.
