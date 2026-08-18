# 2025 target cards (as of end of 2025 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Lyon Richardson | CIN | 25 | RP | 37 | 30° | 0.93 | lean_supinator | 93 | 97 | 95 | 88 | SL (112, 0.93, 0.41) | +2.7 | 1.17 | 2 | 466 | Y | 96 | +2.3 | +0.04 | +0.3 |
| 2 | Chase Dollander | COL | 23 | SP | 98 | 25° | 0.94 | lean_supinator | 97 | 100 | 98 | 95 | SL (114, 0.90, 0.38) | +2.4 | 0.90 | 1 | 271 |  | 100 | +2.0 | +0.11 | +0.9 |
| 3 | Griffin Canning | NYM | 29 | SP | 76 | 44° | 0.94 | lean_pronator | 90 | 99 | 99 | 92 | FS (99, 0.20, 0.04) | +1.2 | 0.64 | 2 | 698 |  | 91 | +1.0 | +0.04 | +0.3 |
| 4 | Jake Eder | LAA | 26 | RP | 18 | 37° | 0.94 | lean_pronator | 89 | 98 | 95 | 85 | SI (103, 0.55, 0.30) | +1.9 | 0.59 | 2 | 236 | Y | 91 | +1.6 | +0.03 | +0.2 |
| 5 | Victor Vodnik | COL | 25 | RP | 50 | 43° | 0.89 | supinator | 98 | 101 | 101 | 105 | SI (111, 0.53, 0.25) | +1.9 | 0.52 | 2 | 436 |  | 100 | +1.6 | +0.03 | +0.3 |
| 6 | Tommy Kahnle | DET | 35 | RP | 63 | 43° | 0.93 | hybrid | 92 | 97 | 97 | 93 | SL (104, 0.65, 0.28) | +1.7 | 0.50 | 4 | 738 |  | 93 | +1.4 | +0.04 | +0.3 |
| 7 | Antonio Senzatela | COL | 30 | SP | 130 | 42° | 0.84 | supinator | 85 | 98 | 106 | 93 | FC (101, 0.28, 0.22) | +2.2 | 0.48 | 1 | 374 |  | 88 | +1.9 | +0.13 | +1.1 |
| 8 | Jalen Beeks | ARI | 31 | RP | 57 | 49° | 0.94 | hybrid | 92 | 97 | 95 | 91 | SL (109, 0.75, 0.14) | +2.4 | 0.41 | 3 | 219 |  | 94 | +2.0 | +0.05 | +0.4 |
| 9 | Ranger Suarez | PHI | 29 | SP | 157 | 38° | 0.80 | supinator | 97 | 102 | 111 | 107 | SL (106, 0.70, 0.20) | +1.2 | 0.39 | 5 | 240 |  | 98 | +1.0 | +0.09 | +0.7 |
| 10 | Luke Jackson | - - - | 33 | RP | 51 | 53° | 0.94 | lean_supinator | 93 | 103 | 102 | 99 | CH (106, 0.40, 0.03) | +1.9 | 0.37 | 3 | 322 |  | 94 | +1.6 | +0.03 | +0.3 |
| 11 | Cole Sands | MIN | 27 | RP | 72 | 24° | 0.86 | supinator | 96 | 100 | 105 | 100 | SL (114, 0.75, 0.12) | +2.5 | 0.31 | 2 | 237 |  | 99 | +2.2 | +0.06 | +0.5 |
| 12 | Mason Englert | TBR | 25 | RP | 44 | 41° | 0.92 | lean_supinator | 95 | 101 | 108 | 102 | SL (106, 0.80, 0.19) | +1.6 | 0.31 | 1 | 750 |  | 96 | +1.4 | +0.02 | +0.2 |
| 13 | Luke Weaver | NYY | 31 | RP | 64 | 48° | 0.96 | pronator | 97 | 101 | 102 | 101 | SL (114, 0.88, 0.13) | +2.3 | 0.31 | 1 | 254 |  | 99 | +2.0 | +0.05 | +0.4 |
| 14 | Anthony Molina | COL | 23 | RP | 34 | 50° | 0.99 | pronator | 94 | 97 | 111 | 104 | FC (102, 0.23, 0.25) | +1.2 | 0.31 | 2 | 460 | Y | 95 | +1.0 | +0.02 | +0.1 |
| 15 | Ian Gibaut | CIN | 31 | RP | 25 | 51° | 0.96 | pronator | 89 | 100 | 106 | 97 | SI (99, 0.23, 0.20) | +1.4 | 0.30 | 2 | 437 |  | 91 | +1.2 | +0.02 | +0.2 |
| 16 | José Ruiz | - - - | 30 | RP | 16 | 47° | 0.93 | lean_supinator | 98 | 100 | 106 | 104 | SL (110, 0.88, 0.17) | +1.8 | 0.30 | 2 | 526 |  | 99 | +1.5 | +0.02 | +0.2 |
| 17 | Andrew Saalfrank | ARI | 27 | RP | 29 | 47° | 0.46 | supinator | 87 | 98 | 100 | 89 | SL (106, 0.85, 0.11) | +2.6 | 0.29 | 2 | 43 |  | 90 | +2.2 | +0.04 | +0.3 |
| 18 | Max Lazar | PHI | 26 | RP | 41 | 53° | 0.82 | supinator | 93 | 101 | 101 | 95 | SL (103, 0.75, 0.20) | +1.4 | 0.28 | 2 | 374 |  | 94 | +1.2 | +0.02 | +0.2 |
| 19 | Luis Peralta | COL | 24 | RP | 19 | 28° | 0.98 | pronator | 98 | 98 | 92 | 86 | SL (113, 0.70, 0.11) | +2.1 | 0.26 | 2 | 76 | Y | 100 | +1.8 | +0.03 | +0.2 |
| 20 | Dean Kremer | BAL | 29 | SP | 171 | 42° | 0.98 | pronator | 96 | 99 | 101 | 96 | SL (107, 0.78, 0.15) | +1.6 | 0.25 | 2 | 685 |  | 98 | +1.3 | +0.12 | +1.0 |
| 21 | Yusei Kikuchi | LAA | 34 | SP | 178 | 34° | 0.91 | lean_supinator | 98 | 99 | 105 | 105 | SI (106, 0.68, 0.23) | +1.1 | 0.25 | 1 | 126 |  | 99 | +0.9 | +0.09 | +0.7 |
| 22 | Kyle Harrison | - - - | 23 | SP | 35 | 29° | 0.98 | pronator | 104 | 100 | 108 | 108 | SI (108, 0.55, 0.35) | +0.6 | 0.23 | 2 | 55 | Y | 104 | +0.5 | +0.02 | +0.1 |
| 23 | Luis Morales | ATH | 22 | SP | 48 | 39° | 0.86 | supinator | 98 | 102 | 107 | 105 | CU (108, 0.23, 0.02) | +1.5 | 0.21 | 3 | 664 |  | 99 | +1.3 | +0.04 | +0.3 |
| 24 | Scott Blewett | - - - | 29 | RP | 44 | 47° | 0.84 | supinator | 85 | 100 | 107 | 97 | SI (92, 0.47, 0.18) | +1.0 | 0.21 | 4 | 359 |  | 86 | +0.9 | +0.02 | +0.1 |
| 25 | Fraser Ellard | CHW | 27 | RP | 17 | 28° | 0.85 | supinator | 102 | 98 | 87 | 89 | FC (112, 0.23, 0.13) | +1.4 | 0.20 | 2 | 121 |  | 103 | +1.2 | +0.02 | +0.2 |
| 26 | Landen Roupp | SFG | 26 | SP | 106 | 21° | nan | unknown | 97 | 102 | 106 | 102 | SL (113, 0.90, 0.09) | +2.1 | 0.19 | 2 | 115 |  | 99 | +1.8 | +0.11 | +0.8 |
| 27 | Joey Wentz | - - - | 27 | RP | 98 | 51° | 0.92 | lean_supinator | 91 | 99 | 104 | 95 | SI (97, 0.30, 0.22) | +0.8 | 0.19 | 1 | 182 |  | 91 | +0.7 | +0.02 | +0.2 |
| 28 | John Curtiss | ARI | 32 | RP | 36 | 44° | 0.97 | pronator | 95 | 100 | 105 | 98 | CU (107, 0.42, 0.09) | +1.6 | 0.18 | 2 | 471 |  | 97 | +1.4 | +0.02 | +0.2 |
| 29 | Jack Perkins | ATH | 25 | RP | 38 | 31° | 0.96 | pronator | 100 | 101 | 96 | 96 | SI (103, 0.50, 0.44) | +0.4 | 0.18 | 1 | 444 | Y | 101 | +0.3 | +0.01 | +0.0 |
| 30 | Nathan Eovaldi | TEX | 35 | SP | 130 | 30° | 0.94 | lean_supinator | 100 | 101 | 104 | 105 | SI (103, 1.00, 0.25) | +0.4 | 0.17 | 3 | 451 | Y | 100 | +0.4 | +0.03 | +0.2 |
| 31 | Zach Brzykcy | WSN | 25 | RP | 23 | 55° | 0.98 | pronator | 91 | 100 | 91 | 84 | SL (100, 0.80, 0.12) | +1.2 | 0.16 | 2 | 225 |  | 93 | +1.1 | +0.02 | +0.1 |
| 32 | Sean Reynolds | SDP | 27 | RP | 27 | 43° | 0.97 | pronator | 94 | 100 | 96 | 91 | CU (108, 0.35, 0.05) | +1.9 | 0.16 | 2 | 283 |  | 96 | +1.6 | +0.03 | +0.2 |
| 33 | Chris Stratton | - - - | 34 | RP | 21 | 36° | 0.81 | supinator | 87 | 99 | 93 | 84 | FC (96, 0.65, 0.12) | +1.2 | 0.15 | 1 | 536 |  | 88 | +1.1 | +0.02 | +0.1 |
| 34 | Brooks Kriske | - - - | 31 | RP | 18 | 43° | 0.95 | pronator | 99 | 97 | 87 | 89 | SL (108, 0.78, 0.12) | +1.2 | 0.15 | 4 | 715 |  | 101 | +1.1 | +0.02 | +0.1 |
| 35 | Taylor Rashi | ARI | 29 | RP | 16 | 73° | 0.88 | supinator | 85 | 97 | 104 | 91 | SI (97, 0.20, 0.05) | +1.8 | 0.15 | 3 | 7 |  | 86 | +1.5 | +0.02 | +0.2 |
| 36 | Roki Sasaki | LAD | 23 | SP | 36 | 42° | 0.96 | pronator | 91 | 98 | 91 | 84 | SI (101, 0.33, 0.08) | +1.4 | 0.14 | 3 | 559 | Y | 92 | +1.2 | +0.04 | +0.3 |
| 37 | Génesis Cabrera | - - - | 28 | RP | 42 | 41° | 0.94 | lean_supinator | 103 | 99 | 102 | 104 | SL (112, 0.55, 0.11) | +1.4 | 0.14 | 2 | 189 |  | 104 | +1.2 | +0.02 | +0.2 |
| 38 | Zach Agnos | COL | 24 | RP | 31 | 39° | 0.97 | pronator | 89 | 99 | 96 | 90 | CH (96, 0.38, 0.03) | +1.1 | 0.14 | 3 | 773 | Y | 90 | +0.9 | +0.02 | +0.1 |
| 39 | Mitch Farris | LAA | 24 | SP | 24 | 46° | 0.99 | pronator | 88 | 96 | 91 | 79 | CU (97, 0.40, 0.03) | +1.4 | 0.14 | 3 | 215 |  | 89 | +1.2 | +0.04 | +0.3 |
| 40 | Paxton Schultz | TOR | 27 | RP | 24 | 37° | 0.91 | hybrid | 93 | 99 | 97 | 90 | CU (100, 0.45, 0.01) | +1.0 | 0.14 | 3 | 719 |  | 94 | +0.9 | +0.01 | +0.1 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emerson Hancock | SEA | SP | 16° | hybrid | 90 | CU | 116 | 0.20 | 0.02 | +3.6 | 94 | +0.15 |
| 2 | Tayler Scott | - - - | RP | 15° | pronator | 91 | CU | 115 | 0.23 | 0.01 | +3.4 | 94 | +0.05 |
| 3 | Sam Aldegheri | LAA | SP | 41° | supinator | 91 | KC | 115 | 0.20 | 0.01 | +3.3 | 95 | +0.09 |
| 4 | Tristan Beck | SFG | RP | 41° | pronator | 93 | FS | 115 | 0.25 | 0.01 | +3.1 | 96 | +0.06 |
| 5 | Caden Dana | LAA | SP | 45° | pronator | 90 | FS | 112 | 0.20 | 0.02 | +3.1 | 94 | +0.09 |
| 6 | Chris Paddack | - - - | SP | 50° | pronator | 91 | FS | 113 | 0.20 | 0.02 | +3.1 | 94 | +0.22 |
| 7 | Trevor Williams | WSN | SP | 17° | supinator | 90 | CU | 111 | 0.35 | 0.01 | +2.9 | 93 | +0.11 |
| 8 | Alexis Díaz | - - - | RP | 16° | supinator | 94 | CU | 114 | 0.30 | 0.01 | +2.8 | 97 | +0.04 |
| 9 | Germán Márquez | COL | SP | 40° | lean_supinator | 86 | CU | 105 | 0.20 | 0.01 | +2.8 | 88 | +0.16 |
| 10 | Lyon Richardson | CIN | RP | 30° | lean_supinator | 93 | SL | 112 | 0.93 | 0.41 | +2.7 | 96 | +0.04 |
| 11 | Jesus Tinoco | MIA | RP | 21° | hybrid | 97 | CU | 117 | 0.20 | 0.01 | +2.7 | 100 | +0.04 |
| 12 | Michael Tonkin | MIN | RP | 14° | lean_supinator | 93 | CU | 113 | 0.38 | 0.01 | +2.7 | 96 | +0.04 |
| 13 | Andrew Saalfrank | ARI | RP | 47° | supinator | 87 | SL | 106 | 0.85 | 0.11 | +2.6 | 90 | +0.04 |
| 14 | Bradley Blalock | COL | SP | 65° | pronator | 91 | CH | 110 | 0.50 | 0.04 | +2.6 | 94 | +0.07 |
| 15 | Angel Chivilli | COL | RP | 34° | pronator | 94 | CU | 113 | 0.23 | 0.01 | +2.6 | 97 | +0.05 |
| 16 | Cole Sands | MIN | RP | 24° | supinator | 96 | SL | 114 | 0.75 | 0.12 | +2.5 | 99 | +0.06 |
| 17 | Félix Bautista | BAL | RP | 69° | unknown | 100 | CH | 118 | 0.23 | 0.01 | +2.5 | 102 | +0.04 |
| 18 | Dane Dunning | - - - | RP | 38° | unknown | 81 | CU | 100 | 0.23 | 0.01 | +2.5 | 84 | +0.04 |
| 19 | Jason Alexander | - - - | SP | 19° | hybrid | 93 | CU | 111 | 0.28 | 0.01 | +2.5 | 95 | +0.09 |
| 20 | Konnor Pilkington | WSN | RP | 30° | pronator | 97 | CU | 115 | 0.23 | 0.01 | +2.5 | 100 | +0.03 |
| 21 | Brady Singer | CIN | SP | 24° | supinator | 95 | CU | 113 | 0.35 | 0.01 | +2.5 | 98 | +0.19 |
| 22 | José Ureña | - - - | RP | 28° | pronator | 87 | CU | 105 | 0.20 | 0.01 | +2.5 | 90 | +0.05 |
| 23 | Tanner Houck | BOS | SP | 21° | supinator | 96 | CU | 113 | 0.33 | 0.01 | +2.4 | 98 | +0.07 |
| 24 | Chase Dollander | COL | SP | 25° | lean_supinator | 97 | SL | 114 | 0.90 | 0.38 | +2.4 | 100 | +0.11 |
| 25 | Jalen Beeks | ARI | RP | 49° | hybrid | 92 | SL | 109 | 0.75 | 0.14 | +2.4 | 94 | +0.05 |

## Named checks

- **Carson Palmquist** (COL, SP): slot 16°, eff4 0.93, lean_supinator; Stuff+ 93 (own 97), Loc+ 91; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=33, drop-recipe N → proj Stf+ 93, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 16°, eff4 0.90, hybrid; Stuff+ 90 (own 99), Loc+ 100; reachable 1, best add CU (prec Stf+ 116, share 0.20, P 0.02), gain +3.6, ΣEV 0.06, pool n=75, drop-recipe N → proj Stf+ 94, ΔWAR +0.15