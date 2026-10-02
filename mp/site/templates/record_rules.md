### How this record works

- **Every signal is PAPER.** No real money is wagered or claimed. If that ever changes, each row will say so in the `money` column.
- **BET, LEAN, PASS.** A BET requires a model that has beaten closing lines out of sample; ours has not, so there are no BETs. A LEAN is a paper signal: the model disagrees with the market by more than a set threshold. It is tracked at zero stake for research, so it never adds units or ROI. A PASS is everything else.
- **Timestamped and append-only.** Each signal is written at publication with a UTC timestamp and the page it was published on. Rows are never edited or deleted. Corrections are new rows. The full history lives in a public git repository, so any change would be visible.
- **Graded automatically.** Final scores come from nflverse, with The Odds API as fallback. If the two sources disagree, the signal is not graded and stays listed as pending.
- **Closing line.** The close is our own last Pinnacle capture before kickoff, taken by a job that checks every 10 minutes. Each row shows how many minutes before kickoff that capture was taken. If there is no capture, CLV is left blank, never estimated.
- **What this is not.** This is our own automated database. It is public and auditable, but no third party has verified it.
