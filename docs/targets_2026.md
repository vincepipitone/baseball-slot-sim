# 2026 target cards (through 2026-08-16) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Albert Suárez | BAL | 36 | RP | 51 | 46° | 0.91 | hybrid | 85 | 98 | 104 | 91 | SL (105, 0.82, 0.41) | +2.8 | 1.54 | 2 | 319 |  | 87 | +2.4 | +0.05 | +0.4 |
| 2 | Simeon Woods Richardson | - - - | 25 | SP | 63 | 50° | 0.96 | pronator | 87 | 99 | 93 | 85 | CH (103, 0.50, 0.04) | +2.2 | 0.96 | 6 | 252 |  | 90 | +1.8 | +0.06 | +0.5 |
| 3 | Eduardo Rodriguez | ARI | 33 | SP | 149 | 42° | 0.86 | supinator | 92 | 100 | 110 | 103 | SL (111, 0.82, 0.28) | +2.7 | 0.77 | 1 | 307 |  | 94 | +2.3 | +0.19 | +1.5 |
| 4 | Jalen Beeks | TEX | 32 | RP | 26 | 47° | 0.92 | hybrid | 89 | 97 | 101 | 91 | SL (107, 0.78, 0.18) | +2.5 | 0.68 | 3 | 303 |  | 91 | +2.1 | +0.03 | +0.3 |
| 5 | Dean Kremer | - - - | 30 | SP | 53 | 44° | 0.98 | pronator | 90 | 98 | 95 | 89 | SL (107, 0.75, 0.24) | +2.3 | 0.61 | 2 | 750 |  | 93 | +1.9 | +0.06 | +0.5 |
| 6 | Jared Jones | PIT | 24 | SP | 64 | 41° | 0.90 | supinator | 101 | 102 | 107 | 110 | SI (115, 0.38, 0.24) | +2.1 | 0.60 | 2 | 456 |  | 103 | +1.8 | +0.06 | +0.5 |
| 7 | Kirby Yates | - - - | 39 | RP | 35 | 19° | 0.94 | lean_pronator | 88 | 99 | 101 | 88 | SL (108, 0.85, 0.18) | +2.7 | 0.57 | 4 | 132 |  | 91 | +2.3 | +0.04 | +0.3 |
| 8 | Walbert Ureña | LAA | 22 | SP | 107 | 41° | 0.88 | supinator | 99 | 101 | 103 | 105 | CU (113, 0.23, 0.03) | +1.9 | 0.56 | 3 | 397 |  | 101 | +1.6 | +0.09 | +0.7 |
| 9 | Adam Macko | TOR | 25 | RP | 22 | 46° | 0.89 | supinator | 98 | 99 | 96 | 92 | FC (110, 0.38, 0.22) | +1.7 | 0.53 | 3 | 249 |  | 100 | +1.4 | +0.02 | +0.2 |
| 10 | Will Klein | LAD | 26 | RP | 41 | 45° | 0.98 | pronator | 95 | 102 | 104 | 101 | SI (112, 0.28, 0.18) | +2.4 | 0.51 | 2 | 588 |  | 97 | +2.1 | +0.03 | +0.3 |
| 11 | Eric Lauer | - - - | 31 | SP | 98 | 38° | 0.94 | hybrid | 89 | 97 | 103 | 89 | SI (98, 0.65, 0.36) | +1.3 | 0.46 | 1 | 182 | Y | 90 | +1.1 | +0.06 | +0.5 |
| 12 | Seranthony Domínguez | - - - | 31 | RP | 43 | 28° | 0.80 | supinator | 110 | 100 | 89 | 98 | SL (116, 0.97, 0.46) | +0.9 | 0.42 | 3 | 332 |  | 111 | +0.8 | +0.01 | +0.1 |
| 13 | Tyler Schweitzer | CHW | 25 | RP | 24 | 46° | 0.77 | supinator | 98 | 102 | 103 | 103 | SI (109, 0.25, 0.15) | +1.5 | 0.41 | 3 | 299 |  | 100 | +1.3 | +0.02 | +0.2 |
| 14 | Brennan Bernardino | COL | 34 | RP | 50 | 16° | 0.75 | supinator | 91 | 98 | 105 | 94 | SL (110, 0.80, 0.15) | +2.6 | 0.39 | 1 | 54 |  | 94 | +2.2 | +0.04 | +0.4 |
| 15 | Matthew Boyd | CHC | 35 | SP | 85 | 24° | 0.93 | hybrid | 96 | 99 | 108 | 101 | SI (104, 0.72, 0.35) | +1.1 | 0.38 | 1 | 106 |  | 97 | +0.9 | +0.04 | +0.3 |
| 16 | Julian Garcia | CIN | 31 | RP | 26 | 56° | 0.76 | supinator | 86 | 99 | 103 | 90 | CU (103, 0.50, 0.02) | +2.4 | 0.32 | 4 | 263 |  | 89 | +2.0 | +0.03 | +0.3 |
| 17 | Mark Leiter Jr. | ATH | 35 | RP | 33 | 44° | 0.97 | pronator | 92 | 98 | 99 | 94 | SL (98, 0.88, 0.35) | +0.9 | 0.32 | 2 | 772 |  | 93 | +0.8 | +0.01 | +0.1 |
| 18 | Yusei Kikuchi | LAA | 35 | SP | 31 | 46° | 0.91 | hybrid | 98 | 99 | 103 | 103 | SI (103, 0.25, 0.40) | +0.8 | 0.30 | 1 | 217 |  | 99 | +0.6 | +0.02 | +0.2 |
| 19 | Shane Baz | BAL | 27 | SP | 139 | 37° | 0.96 | pronator | 98 | 100 | 103 | 103 | SL (109, 0.65, 0.16) | +1.5 | 0.29 | 3 | 853 |  | 100 | +1.3 | +0.10 | +0.8 |
| 20 | Drew Anderson | DET | 32 | RP | 76 | 41° | 0.86 | supinator | 99 | 101 | 100 | 101 | SI (106, 0.57, 0.29) | +1.0 | 0.28 | 2 | 857 |  | 100 | +0.8 | +0.03 | +0.2 |
| 21 | Ben Brown | CHC | 26 | RP | 68 | 39° | 0.94 | lean_supinator | 102 | 100 | 99 | 99 | SL (113, 0.82, 0.17) | +1.6 | 0.27 | 3 | 552 |  | 103 | +1.3 | +0.04 | +0.3 |
| 22 | José Suarez | - - - | 28 | RP | 58 | 40° | 0.88 | supinator | 96 | 98 | 98 | 95 | FC (104, 0.23, 0.19) | +1.2 | 0.25 | 2 | 293 |  | 97 | +1.0 | +0.02 | +0.2 |
| 23 | Elmer Rodríguez | NYY | 22 | SP | 17 | 27° | 0.93 | lean_supinator | 94 | 96 | 81 | 75 | FC (99, 0.23, 0.29) | +0.8 | 0.22 | 1 | 352 |  | 94 | +0.7 | +0.02 | +0.2 |
| 24 | Osvaldo Bido | - - - | 30 | RP | 18 | 31° | 0.86 | supinator | 99 | 99 | 89 | 86 | CU (109, 0.30, 0.05) | +1.4 | 0.22 | 2 | 486 |  | 100 | +1.2 | +0.02 | +0.2 |
| 25 | Kohl Drake | ARI | 25 | SP | 16 | 39° | 0.97 | pronator | 93 | 98 | 94 | 87 | SI (101, 0.20, 0.19) | +1.1 | 0.20 | 1 | 287 |  | 94 | +0.9 | +0.03 | +0.2 |
| 26 | Bryan Abreu | HOU | 29 | RP | 45 | 41° | 0.89 | supinator | 99 | 99 | 84 | 86 | SI (104, 0.65, 0.28) | +0.7 | 0.20 | 4 | 810 |  | 100 | +0.6 | +0.01 | +0.1 |
| 27 | Luke Weaver | - - - | 32 | RP | 47 | 48° | 0.95 | pronator | 102 | 104 | 107 | 110 | SL (113, 0.88, 0.12) | +1.6 | 0.19 | 1 | 304 |  | 103 | +1.4 | +0.03 | +0.2 |
| 28 | Zac Gallen | ARI | 30 | SP | 98 | 46° | 0.81 | supinator | 87 | 100 | 109 | 100 | FC (92, 0.38, 0.23) | +0.7 | 0.18 | 2 | 660 |  | 88 | +0.6 | +0.03 | +0.3 |
| 29 | Sam Aldegheri | LAA | 24 | SP | 33 | 44° | 0.93 | hybrid | 90 | 96 | 96 | 87 | SI (96, 0.45, 0.20) | +0.9 | 0.18 | 1 | 241 |  | 91 | +0.8 | +0.02 | +0.2 |
| 30 | Huascar Brazobán | - - - | 36 | RP | 59 | 37° | 0.93 | lean_pronator | 96 | 99 | 100 | 97 | SL (111, 0.75, 0.06) | +2.1 | 0.17 | 2 | 757 | Y | 98 | +1.8 | +0.04 | +0.3 |
| 31 | Peyton Pallette | CLE | 25 | RP | 20 | 39° | 0.99 | pronator | 92 | 100 | 96 | 86 | CH (98, 0.55, 0.04) | +0.9 | 0.16 | 2 | 863 |  | 93 | +0.7 | +0.01 | +0.1 |
| 32 | Randy Dobnak | KCR | 31 | SP | 41 | 20° | 0.87 | supinator | 82 | 99 | 109 | 91 | CU (116, 0.33, 0.01) | +4.8 | 0.15 | 2 | 47 |  | 86 | +4.1 | +0.13 | +1.1 |
| 33 | Landen Roupp | SFG | 27 | SP | 129 | 22° | 0.83 | supinator | 99 | 102 | 105 | 104 | SL (107, 0.80, 0.13) | +1.2 | 0.15 | 1 | 183 |  | 100 | +1.0 | +0.07 | +0.6 |
| 34 | Craig Yoho | - - - | 26 | RP | 25 | 20° | 0.99 | pronator | 95 | 100 | 97 | 96 | SL (108, 0.70, 0.08) | +1.8 | 0.15 | 1 | 162 |  | 97 | +1.5 | +0.03 | +0.2 |
| 35 | Chris Murphy | CHW | 28 | RP | 30 | 41° | 0.90 | lean_supinator | 108 | 100 | 90 | 97 | FC (118, 0.23, 0.11) | +1.4 | 0.15 | 1 | 137 |  | 109 | +1.1 | +0.02 | +0.2 |
| 36 | Shaun Anderson | LAA | 31 | RP | 20 | 46° | 0.70 | supinator | 86 | 99 | 96 | 88 | CU (102, 0.53, 0.02) | +2.2 | 0.13 | 2 | 617 |  | 89 | +1.9 | +0.03 | +0.2 |
| 37 | Rhett Lowder | CIN | 24 | SP | 101 | 26° | 0.89 | supinator | 86 | 100 | 104 | 93 | CU (111, 0.35, 0.02) | +3.5 | 0.12 | 2 | 300 |  | 90 | +3.0 | +0.16 | +1.3 |
| 38 | Ethan Roberts | CHC | 28 | RP | 25 | 37° | nan | unknown | 96 | 102 | 95 | 95 | CU (120, 0.25, 0.01) | +3.3 | 0.12 | 3 | 36 |  | 100 | +2.8 | +0.05 | +0.4 |
| 39 | Cal Quantrill | TEX | 31 | RP | 70 | 43° | 0.97 | pronator | 89 | 98 | 106 | 95 | SL (98, 0.65, 0.07) | +1.2 | 0.12 | 2 | 259 |  | 90 | +1.0 | +0.03 | +0.2 |
| 40 | Jacob Waguespack | DET | 32 | RP | 27 | 71° | 0.97 | pronator | 93 | 99 | 92 | 83 | SL (102, 0.65, 0.10) | +1.2 | 0.12 | 1 | 9 |  | 95 | +1.0 | +0.02 | +0.1 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Randy Dobnak | KCR | SP | 20° | supinator | 82 | CU | 116 | 0.33 | 0.01 | +4.8 | 86 | +0.13 |
| 2 | Rhett Lowder | CIN | SP | 26° | supinator | 86 | CU | 111 | 0.35 | 0.02 | +3.5 | 90 | +0.16 |
| 3 | Ethan Roberts | CHC | RP | 37° | unknown | 96 | CU | 120 | 0.25 | 0.01 | +3.3 | 100 | +0.05 |
| 4 | Adrian Houser | SFG | SP | 37° | hybrid | 90 | FS | 113 | 0.20 | 0.01 | +3.2 | 93 | +0.15 |
| 5 | Germán Márquez | SDP | SP | 39° | pronator | 87 | CU | 110 | 0.30 | 0.01 | +3.2 | 90 | +0.09 |
| 6 | Jake Woodford | - - - | RP | 26° | unknown | 98 | KC | 120 | 0.23 | 0.01 | +3.0 | 101 | +0.04 |
| 7 | Albert Suárez | BAL | RP | 46° | hybrid | 85 | SL | 105 | 0.82 | 0.41 | +2.8 | 87 | +0.05 |
| 8 | Eduardo Rodriguez | ARI | SP | 42° | supinator | 92 | SL | 111 | 0.82 | 0.28 | +2.7 | 94 | +0.19 |
| 9 | Kirby Yates | - - - | RP | 19° | lean_pronator | 88 | SL | 108 | 0.85 | 0.18 | +2.7 | 91 | +0.04 |
| 10 | Zack Littell | - - - | SP | 43° | hybrid | 83 | CU | 102 | 0.33 | 0.01 | +2.6 | 86 | +0.15 |
| 11 | Brennan Bernardino | COL | RP | 16° | supinator | 91 | SL | 110 | 0.80 | 0.15 | +2.6 | 94 | +0.04 |
| 12 | Jalen Beeks | TEX | RP | 47° | hybrid | 89 | SL | 107 | 0.78 | 0.18 | +2.5 | 91 | +0.03 |
| 13 | Brady Singer | CIN | SP | 22° | supinator | 92 | CU | 110 | 0.30 | 0.02 | +2.5 | 95 | +0.14 |
| 14 | Luis Castillo | - - - | SP | 19° | supinator | 97 | CU | 114 | 0.28 | 0.03 | +2.5 | 99 | +0.13 |
| 15 | Will Klein | LAD | RP | 45° | pronator | 95 | SI | 112 | 0.28 | 0.18 | +2.4 | 97 | +0.03 |
| 16 | Julian Garcia | CIN | RP | 56° | supinator | 86 | CU | 103 | 0.50 | 0.02 | +2.4 | 89 | +0.03 |
| 17 | Dennis Santana | - - - | RP | 31° | hybrid | 92 | CU | 108 | 0.20 | 0.03 | +2.3 | 94 | +0.03 |
| 18 | Ronel Blanco | HOU | SP | 48° | pronator | 93 | FS | 110 | 0.23 | 0.01 | +2.3 | 96 | +0.06 |
| 19 | Tanner Gordon | COL | RP | 45° | pronator | 86 | FS | 103 | 0.30 | 0.02 | +2.3 | 88 | +0.06 |
| 20 | Dean Kremer | - - - | SP | 44° | pronator | 90 | SL | 107 | 0.75 | 0.24 | +2.3 | 93 | +0.06 |
| 21 | Raisel Iglesias | ATL | RP | 29° | supinator | 96 | CU | 112 | 0.20 | 0.02 | +2.3 | 98 | +0.04 |
| 22 | Taylor Clarke | ARI | RP | 45° | unknown | 92 | CU | 108 | 0.38 | 0.03 | +2.2 | 94 | +0.04 |
| 23 | Tim Mayza | PHI | RP | 43° | lean_supinator | 97 | CU | 113 | 0.20 | 0.02 | +2.2 | 100 | +0.04 |
| 24 | Shaun Anderson | LAA | RP | 46° | supinator | 86 | CU | 102 | 0.53 | 0.02 | +2.2 | 89 | +0.03 |
| 25 | Tyler Mahle | - - - | SP | 43° | pronator | 88 | CH | 103 | 0.50 | 0.04 | +2.2 | 90 | +0.11 |

## Named checks

- **Trey Yesavage** (TOR, SP): slot 66°, eff4 0.98, pronator; Stuff+ 108 (own 101), Loc+ 90; reachable 3, best add CH (prec Stf+ 112, share 0.45, P 0.02), gain +0.5, ΣEV 0.02, pool n=16, drop-recipe N → proj Stf+ 108, ΔWAR +0.02
- **Carson Palmquist** (WSN, SP): slot 12°, eff4 0.90, lean_supinator; Stuff+ 107 (own 99), Loc+ 93; reachable 1, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=30, drop-recipe N → proj Stf+ 107, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 11°, eff4 0.82, supinator; Stuff+ 101 (own 100), Loc+ 106; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=36, drop-recipe N → proj Stf+ 101, ΔWAR +0.00