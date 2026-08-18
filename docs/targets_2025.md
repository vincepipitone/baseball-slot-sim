# 2025 target cards (as of end of 2025 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Andrew Saalfrank | ARI | 27 | RP | 29 | 47° | 0.46 | supinator | 87 | 98 | 100 | 89 | SL (106, 0.85, 0.10) | +2.6 | 0.27 | 2 | 43 |  | 90 | +2.2 | +0.04 | +0.3 |
| 2 | Scott Blewett | - - - | 29 | RP | 44 | 47° | 0.84 | supinator | 85 | 100 | 107 | 97 | SI (92, 0.47, 0.21) | +1.0 | 0.26 | 3 | 358 |  | 86 | +0.9 | +0.02 | +0.1 |
| 3 | Alek Jacob | SDP | 27 | RP | 33 | 2° | 0.88 | supinator | 90 | 95 | 100 | 89 | FC (101, 0.20, 0.01) | +1.5 | 0.01 | 1 | 16 |  | 91 | +1.3 | +0.02 | +0.2 |
| 4 | José Ureña | - - - | 33 | RP | 55 | 28° | 0.99 | pronator | 87 | 100 | 101 | 92 | CU (105, 0.20, 0.01) | +2.5 | 0.06 | 2 | 386 | Y | 90 | +2.1 | +0.05 | +0.4 |
| 5 | Chase Lee | DET | 26 | RP | 37 | -4° | 0.38 | supinator | 91 | 97 | 105 | 96 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 16 |  | 91 | +0.0 | +0.00 | +0.0 |
| 6 | Alexis Díaz | - - - | 28 | RP | 17 | 16° | 0.85 | supinator | 94 | 101 | 93 | 89 | CU (114, 0.30, 0.01) | +2.8 | 0.07 | 3 | 62 |  | 97 | +2.4 | +0.04 | +0.3 |
| 7 | Grant Holman | ATH | 25 | RP | 23 | 41° | 0.97 | pronator | 92 | 101 | 97 | 93 | SI (97, 0.23, 0.05) | +0.8 | 0.04 | 3 | 580 | Y | 92 | +0.7 | +0.01 | +0.1 |
| 8 | Jalen Beeks | ARI | 31 | RP | 57 | 49° | 0.94 | hybrid | 92 | 97 | 95 | 91 | SL (109, 0.75, 0.16) | +2.4 | 0.48 | 3 | 219 |  | 94 | +2.0 | +0.05 | +0.4 |
| 9 | Dane Dunning | - - - | 30 | RP | 20 | 38° | nan | unknown | 81 | 97 | 104 | 89 | CU (100, 0.23, 0.01) | +2.5 | 0.06 | 2 | 543 |  | 84 | +2.1 | +0.04 | +0.3 |
| 10 | Corbin Martin | BAL | 29 | RP | 18 | 43° | 0.83 | supinator | 97 | 100 | 96 | 95 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 732 |  | 97 | +0.0 | +0.00 | +0.0 |
| 11 | Andrew Alvarez | WSN | 26 | SP | 23 | 48° | 0.71 | supinator | 89 | 99 | 106 | 101 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 108 |  | 89 | +0.0 | +0.00 | +0.0 |
| 12 | Carlos Carrasco | - - - | 38 | SP | 45 | 35° | 0.76 | supinator | 80 | 99 | 101 | 88 | FC (88, 0.45, 0.03) | +1.0 | 0.04 | 1 | 109 |  | 81 | +0.9 | +0.03 | +0.2 |
| 13 | Germán Márquez | COL | 30 | SP | 126 | 40° | 0.96 | lean_supinator | 86 | 98 | 98 | 85 | FC (102, 0.28, 0.03) | +2.2 | 0.07 | 1 | 498 | Y | 88 | +1.9 | +0.13 | +1.0 |
| 14 | Matthew Liberatore | STL | 25 | SP | 151 | 48° | 0.97 | pronator | 95 | 98 | 102 | 97 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 143 |  | nan | +nan | +nan | +nan |
| 15 | Félix Bautista | BAL | 30 | RP | 34 | 69° | nan | unknown | 100 | 105 | 100 | 106 | KC (117, 0.23, 0.00) | +2.4 | 0.05 | 3 | 14 |  | 102 | +2.0 | +0.03 | +0.3 |
| 16 | Anthony Molina | COL | 23 | RP | 34 | 50° | 0.99 | pronator | 94 | 97 | 111 | 104 | FC (102, 0.23, 0.37) | +1.2 | 0.46 | 2 | 459 | Y | 95 | +1.0 | +0.02 | +0.1 |
| 17 | Tomoyuki Sugano | BAL | 35 | SP | 157 | 40° | 0.87 | supinator | 88 | 100 | 107 | 99 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 697 |  | nan | +nan | +nan | +nan |
| 18 | Luis Morales | ATH | 22 | SP | 48 | 39° | 0.86 | supinator | 98 | 102 | 107 | 105 | CU (108, 0.23, 0.03) | +1.5 | 0.36 | 3 | 664 |  | 99 | +1.3 | +0.04 | +0.3 |
| 19 | Jake Eder | LAA | 26 | RP | 18 | 37° | 0.94 | lean_pronator | 89 | 98 | 95 | 85 | SI (103, 0.55, 0.43) | +1.9 | 0.83 | 2 | 235 | Y | 91 | +1.6 | +0.03 | +0.2 |
| 20 | Connor Gillispie | MIA | 27 | SP | 26 | 46° | 0.94 | hybrid | 89 | 99 | 97 | 87 | CU (96, 0.20, 0.01) | +1.0 | 0.01 | 1 | 535 |  | 90 | +0.9 | +0.03 | +0.2 |
| 21 | Casey Mize | DET | 28 | SP | 149 | 48° | 0.98 | pronator | 95 | 101 | 107 | 103 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 542 |  | 95 | +0.0 | +0.00 | +0.0 |
| 22 | Nabil Crismatt | ARI | 30 | SP | 34 | 37° | 0.90 | supinator | 79 | 99 | 108 | 92 | FC (91, 0.47, 0.08) | +1.6 | 0.13 | 1 | 675 |  | 80 | +1.4 | +0.05 | +0.4 |
| 23 | Yusei Kikuchi | LAA | 34 | SP | 178 | 34° | 0.91 | lean_supinator | 98 | 99 | 105 | 105 | SI (106, 0.68, 0.21) | +1.1 | 0.23 | 1 | 126 |  | 99 | +0.9 | +0.09 | +0.7 |
| 24 | Andrew Heaney | - - - | 34 | SP | 122 | 26° | 0.99 | pronator | 90 | 100 | 104 | 93 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 90 | Y | 90 | +0.0 | +0.00 | +0.0 |
| 25 | Jose Quintana | MIL | 36 | SP | 131 | 42° | 0.87 | supinator | 86 | 99 | 104 | 91 | FC (98, 0.30, 0.07) | +1.7 | 0.12 | 1 | 216 |  | 88 | +1.5 | +0.10 | +0.8 |
| 26 | Carson Palmquist | COL | 24 | SP | 34 | 16° | 0.93 | lean_supinator | 93 | 97 | 91 | 85 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 33 |  | 93 | +0.0 | +0.00 | +0.0 |
| 27 | Sam Bachman | LAA | 25 | RP | 20 | 35° | nan | unknown | 100 | 102 | 101 | 101 | FF (104, 0.82, 0.04) | +0.6 | 0.02 | 2 | 295 |  | 100 | +0.5 | +0.01 | +0.1 |
| 28 | Scott McGough | - - - | 35 | RP | 16 | 45° | 0.95 | lean_pronator | 89 | 100 | 99 | 89 | FC (96, 0.50, 0.03) | +1.1 | 0.04 | 2 | 659 |  | 90 | +0.9 | +0.01 | +0.1 |
| 29 | Chase Dollander | COL | 23 | SP | 98 | 25° | 0.94 | lean_supinator | 97 | 100 | 98 | 95 | SL (114, 0.90, 0.42) | +2.4 | 0.98 | 1 | 271 |  | 100 | +2.0 | +0.11 | +0.9 |
| 30 | Antonio Senzatela | COL | 30 | SP | 130 | 42° | 0.84 | supinator | 85 | 98 | 106 | 93 | FC (101, 0.28, 0.21) | +2.2 | 0.47 | 1 | 373 |  | 88 | +1.9 | +0.13 | +1.1 |
| 31 | Zach Agnos | COL | 24 | RP | 31 | 39° | 0.97 | pronator | 89 | 99 | 96 | 90 | CU (96, 0.28, 0.01) | +1.1 | 0.04 | 2 | 773 | Y | 90 | +0.9 | +0.02 | +0.1 |
| 32 | Martín Pérez | CHW | 34 | SP | 56 | 47° | 0.97 | pronator | 86 | 97 | 101 | 90 | SL (103, 0.55, 0.01) | +2.4 | 0.03 | 1 | 266 |  | 88 | +2.1 | +0.07 | +0.5 |
| 33 | Zack Littell | - - - | 29 | SP | 186 | 41° | 0.96 | pronator | 88 | 97 | 101 | 92 | FC (90, 0.23, 0.04) | +0.4 | 0.01 | 1 | 483 |  | 88 | +0.3 | +0.03 | +0.3 |
| 34 | Roki Sasaki | LAD | 23 | SP | 36 | 42° | 0.96 | pronator | 91 | 98 | 91 | 84 | SI (101, 0.33, 0.08) | +1.4 | 0.13 | 2 | 558 | Y | 92 | +1.2 | +0.04 | +0.3 |
| 35 | Sean Reynolds | SDP | 27 | RP | 27 | 43° | 0.97 | pronator | 94 | 100 | 96 | 91 | CU (108, 0.35, 0.03) | +1.9 | 0.09 | 2 | 282 |  | 96 | +1.6 | +0.03 | +0.2 |
| 36 | Chris Stratton | - - - | 34 | RP | 21 | 36° | 0.81 | supinator | 87 | 99 | 93 | 84 | FC (96, 0.65, 0.13) | +1.2 | 0.16 | 1 | 536 |  | 88 | +1.1 | +0.02 | +0.1 |
| 37 | Taijuan Walker | PHI | 32 | SP | 123 | 40° | 0.97 | pronator | 86 | 99 | 102 | 92 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 438 |  | nan | +nan | +nan | +nan |
| 38 | Erick Fedde | - - - | 32 | SP | 141 | 39° | nan | unknown | 89 | 100 | 103 | 95 | CU (98, 0.25, 0.01) | +1.3 | 0.02 | 2 | 698 |  | 90 | +1.1 | +0.09 | +0.7 |
| 39 | Carson Whisenhunt | SFG | 24 | SP | 23 | 51° | 0.99 | pronator | 91 | 95 | 87 | 77 | CU (105, 0.25, 0.01) | +1.9 | 0.04 | 2 | 194 |  | 93 | +1.6 | +0.05 | +0.4 |
| 40 | Victor Vodnik | COL | 25 | RP | 50 | 43° | 0.89 | supinator | 98 | 101 | 101 | 105 | SI (111, 0.53, 0.28) | +1.9 | 0.57 | 2 | 436 |  | 100 | +1.6 | +0.03 | +0.3 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emerson Hancock | SEA | SP | 16° | hybrid | 90 | CU | 116 | 0.20 | 0.01 | +3.6 | 94 | +0.15 |
| 2 | Tayler Scott | - - - | RP | 15° | pronator | 91 | CU | 115 | 0.23 | 0.01 | +3.4 | 94 | +0.05 |
| 3 | Tristan Beck | SFG | RP | 41° | pronator | 93 | FS | 115 | 0.25 | 0.01 | +3.1 | 96 | +0.06 |
| 4 | Trevor Williams | WSN | SP | 17° | supinator | 90 | CU | 111 | 0.35 | 0.02 | +2.9 | 93 | +0.11 |
| 5 | Alexis Díaz | - - - | RP | 16° | supinator | 94 | CU | 114 | 0.30 | 0.01 | +2.8 | 97 | +0.04 |
| 6 | Lyon Richardson | CIN | RP | 30° | lean_supinator | 93 | SL | 112 | 0.93 | 0.32 | +2.7 | 96 | +0.04 |
| 7 | Jesus Tinoco | MIA | RP | 21° | hybrid | 97 | CU | 117 | 0.20 | 0.01 | +2.7 | 100 | +0.04 |
| 8 | Michael Tonkin | MIN | RP | 14° | lean_supinator | 93 | CU | 113 | 0.38 | 0.01 | +2.7 | 96 | +0.04 |
| 9 | Andrew Saalfrank | ARI | RP | 47° | supinator | 87 | SL | 106 | 0.85 | 0.10 | +2.6 | 90 | +0.04 |
| 10 | Angel Chivilli | COL | RP | 34° | pronator | 94 | CU | 113 | 0.23 | 0.01 | +2.6 | 97 | +0.05 |
| 11 | Cole Sands | MIN | RP | 24° | supinator | 96 | SL | 114 | 0.75 | 0.12 | +2.5 | 99 | +0.06 |
| 12 | Dane Dunning | - - - | RP | 38° | unknown | 81 | CU | 100 | 0.23 | 0.01 | +2.5 | 84 | +0.04 |
| 13 | Jason Alexander | - - - | SP | 19° | hybrid | 93 | CU | 111 | 0.28 | 0.01 | +2.5 | 95 | +0.09 |
| 14 | Konnor Pilkington | WSN | RP | 30° | pronator | 97 | CU | 115 | 0.23 | 0.01 | +2.5 | 100 | +0.03 |
| 15 | Brady Singer | CIN | SP | 24° | supinator | 95 | CU | 113 | 0.35 | 0.01 | +2.5 | 98 | +0.19 |
| 16 | José Ureña | - - - | RP | 28° | pronator | 87 | CU | 105 | 0.20 | 0.01 | +2.5 | 90 | +0.05 |
| 17 | Martín Pérez | CHW | SP | 47° | pronator | 86 | SL | 103 | 0.55 | 0.01 | +2.4 | 88 | +0.07 |
| 18 | Tanner Houck | BOS | SP | 21° | supinator | 96 | CU | 113 | 0.33 | 0.02 | +2.4 | 98 | +0.07 |
| 19 | Félix Bautista | BAL | RP | 69° | unknown | 100 | KC | 117 | 0.23 | 0.00 | +2.4 | 102 | +0.03 |
| 20 | Chase Dollander | COL | SP | 25° | lean_supinator | 97 | SL | 114 | 0.90 | 0.42 | +2.4 | 100 | +0.11 |
| 21 | Jalen Beeks | ARI | RP | 49° | hybrid | 92 | SL | 109 | 0.75 | 0.16 | +2.4 | 94 | +0.05 |
| 22 | Victor Mederos | LAA | SP | 23° | unknown | 98 | CU | 115 | 0.20 | 0.01 | +2.4 | 100 | +0.07 |
| 23 | Luke Weaver | NYY | RP | 48° | pronator | 97 | SL | 114 | 0.88 | 0.13 | +2.3 | 99 | +0.05 |
| 24 | Germán Márquez | COL | SP | 40° | lean_supinator | 86 | FC | 102 | 0.28 | 0.03 | +2.2 | 88 | +0.13 |
| 25 | Antonio Senzatela | COL | SP | 42° | supinator | 85 | FC | 101 | 0.28 | 0.21 | +2.2 | 88 | +0.13 |

## Named checks

- **Carson Palmquist** (COL, SP): slot 16°, eff4 0.93, lean_supinator; Stuff+ 93 (own 97), Loc+ 91; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=33, drop-recipe N → proj Stf+ 93, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 16°, eff4 0.90, hybrid; Stuff+ 90 (own 99), Loc+ 100; reachable 1, best add CU (prec Stf+ 116, share 0.20, P 0.01), gain +3.6, ΣEV 0.04, pool n=75, drop-recipe N → proj Stf+ 94, ΔWAR +0.15