# 2026 target cards (as of end of 2026 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Albert Suárez | BAL | 36 | RP | 51 | 46° | 0.91 | hybrid | 85 | 98 | 104 | 91 | SL (104, 0.90, 0.34) | +2.8 | 1.20 | 2 | 317 |  | 87 | +2.3 | +0.05 | +0.4 |
| 2 | Randy Dobnak | KCR | 31 | SP | 41 | 20° | 0.87 | supinator | 82 | 99 | 109 | 91 | CU (116, 0.33, 0.02) | +4.8 | 0.20 | 2 | 47 |  | 86 | +4.1 | +0.13 | +1.1 |
| 3 | Will Klein | LAD | 26 | RP | 41 | 45° | 0.98 | pronator | 95 | 102 | 104 | 101 | SI (112, 0.28, 0.19) | +2.4 | 0.67 | 2 | 587 |  | 97 | +2.1 | +0.03 | +0.3 |
| 4 | Brandon Eisert | - - - | 28 | RP | 34 | 34° | 0.90 | supinator | 83 | 96 | 106 | 95 | CU (96, 0.33, 0.01) | +1.8 | 0.06 | 2 | 172 |  | 85 | +1.5 | +0.03 | +0.2 |
| 5 | Yusei Kikuchi | LAA | 35 | SP | 31 | 46° | 0.91 | hybrid | 98 | 99 | 103 | 103 | SI (103, 0.25, 0.46) | +0.8 | 0.34 | 1 | 217 |  | 99 | +0.6 | +0.02 | +0.2 |
| 6 | Sean Sullivan | COL | 23 | SP | 22 | 31° | 0.96 | pronator | 81 | 98 | 100 | 81 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 136 | Y | 81 | +0.0 | +0.00 | +0.0 |
| 7 | Julian Garcia | CIN | 31 | RP | 26 | 56° | 0.76 | supinator | 86 | 99 | 103 | 90 | CU (103, 0.50, 0.02) | +2.4 | 0.19 | 4 | 263 |  | 89 | +2.0 | +0.03 | +0.3 |
| 8 | Tomoyuki Sugano | COL | 36 | SP | 118 | 40° | 0.88 | supinator | 82 | 99 | 103 | 88 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 652 |  | nan | +nan | +nan | +nan |
| 9 | Eduardo Rodriguez | ARI | 33 | SP | 149 | 42° | 0.86 | supinator | 92 | 100 | 110 | 103 | SL (111, 0.82, 0.32) | +2.7 | 0.88 | 1 | 306 |  | 94 | +2.3 | +0.19 | +1.5 |
| 10 | Jalen Beeks | TEX | 32 | RP | 26 | 47° | 0.92 | hybrid | 89 | 97 | 101 | 91 | SL (107, 0.78, 0.15) | +2.5 | 0.62 | 3 | 303 |  | 91 | +2.1 | +0.03 | +0.3 |
| 11 | Zack Littell | - - - | 30 | SP | 120 | 43° | 0.95 | hybrid | 83 | 97 | 101 | 86 | CU (102, 0.33, 0.02) | +2.6 | 0.13 | 2 | 483 |  | 86 | +2.2 | +0.15 | +1.2 |
| 12 | Dean Kremer | - - - | 30 | SP | 53 | 44° | 0.98 | pronator | 90 | 98 | 95 | 89 | SL (107, 0.75, 0.20) | +2.3 | 0.46 | 1 | 748 |  | 93 | +1.9 | +0.06 | +0.5 |
| 13 | Brennan Bernardino | COL | 34 | RP | 50 | 16° | 0.75 | supinator | 91 | 98 | 105 | 94 | SL (110, 0.80, 0.14) | +2.6 | 0.36 | 1 | 54 |  | 94 | +2.2 | +0.04 | +0.4 |
| 14 | Shaun Anderson | LAA | 31 | RP | 20 | 46° | 0.70 | supinator | 86 | 99 | 96 | 88 | CU (102, 0.53, 0.04) | +2.2 | 0.17 | 2 | 613 |  | 89 | +1.9 | +0.03 | +0.2 |
| 15 | Casey Mize | - - - | 29 | SP | 102 | 47° | 0.99 | pronator | 89 | 99 | 107 | 98 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 700 |  | 89 | +0.0 | +0.00 | +0.0 |
| 16 | Jared Jones | PIT | 24 | SP | 64 | 41° | 0.90 | supinator | 101 | 102 | 107 | 110 | SI (115, 0.38, 0.24) | +2.1 | 0.60 | 2 | 456 |  | 103 | +1.8 | +0.06 | +0.5 |
| 17 | Jose Quintana | COL | 37 | SP | 41 | 43° | 0.80 | supinator | 81 | 98 | 104 | 86 | FC (96, 0.40, 0.05) | +2.2 | 0.12 | 1 | 292 |  | 83 | +1.9 | +0.06 | +0.5 |
| 18 | Matthew Boyd | CHC | 35 | SP | 85 | 24° | 0.93 | hybrid | 96 | 99 | 108 | 101 | SI (104, 0.72, 0.38) | +1.1 | 0.42 | 1 | 106 |  | 97 | +0.9 | +0.04 | +0.3 |
| 19 | Tommy Nance | - - - | 35 | RP | 45 | 47° | nan | unknown | 105 | 102 | 96 | 102 | — (nan, nan, nan) | +0.0 | 0.00 | 3 | 442 |  | 105 | +0.0 | +0.00 | +0.0 |
| 20 | JT Brubaker | SFG | 32 | RP | 57 | 45° | 0.89 | supinator | 90 | 100 | 106 | 98 | FC (101, 0.23, 0.04) | +1.5 | 0.06 | 1 | 517 |  | 91 | +1.3 | +0.03 | +0.2 |
| 21 | Tony Santillan | CIN | 29 | RP | 31 | 24° | 0.92 | hybrid | 92 | 100 | 102 | 94 | SI (96, 0.60, 0.11) | +0.6 | 0.06 | 2 | 293 |  | 92 | +0.5 | +0.01 | +0.1 |
| 22 | Mason Black | KCR | 26 | RP | 25 | 26° | 0.99 | lean_supinator | 93 | 98 | 99 | 96 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 247 | Y | 93 | +0.0 | +0.00 | +0.0 |
| 23 | Drew Anderson | DET | 32 | RP | 76 | 41° | 0.86 | supinator | 99 | 101 | 100 | 101 | SI (106, 0.57, 0.35) | +1.0 | 0.35 | 2 | 857 |  | 100 | +0.8 | +0.03 | +0.2 |
| 24 | JP Sears | SDP | 30 | SP | 32 | 30° | 0.98 | pronator | 91 | 98 | 99 | 92 | CU (104, 0.23, 0.03) | +1.8 | 0.06 | 1 | 118 | Y | 93 | +1.6 | +0.05 | +0.4 |
| 25 | Robbie Ray | - - - | 34 | SP | 131 | 46° | 0.96 | pronator | 95 | 97 | 91 | 87 | FC (99, 0.40, 0.05) | +0.6 | 0.03 | 1 | 304 |  | 95 | +0.5 | +0.04 | +0.3 |
| 26 | Elmer Rodríguez | NYY | 22 | SP | 17 | 27° | 0.93 | lean_supinator | 94 | 96 | 81 | 75 | FC (99, 0.23, 0.28) | +0.8 | 0.22 | 1 | 352 |  | 94 | +0.7 | +0.02 | +0.2 |
| 27 | Rhett Lowder | CIN | 24 | SP | 101 | 26° | 0.89 | supinator | 86 | 100 | 104 | 93 | CU (111, 0.35, 0.02) | +3.5 | 0.14 | 2 | 300 |  | 90 | +3.0 | +0.16 | +1.3 |
| 28 | Kirby Yates | - - - | 39 | RP | 35 | 19° | 0.94 | lean_pronator | 88 | 99 | 101 | 88 | SL (108, 0.85, 0.16) | +2.7 | 0.51 | 3 | 132 |  | 91 | +2.3 | +0.04 | +0.3 |
| 29 | Mark Leiter Jr. | ATH | 35 | RP | 33 | 44° | 0.97 | pronator | 92 | 98 | 99 | 94 | SL (98, 0.88, 0.37) | +0.9 | 0.33 | 1 | 771 |  | 93 | +0.8 | +0.01 | +0.1 |
| 30 | Adam Macko | TOR | 25 | RP | 22 | 46° | 0.89 | supinator | 98 | 99 | 96 | 92 | FC (110, 0.38, 0.24) | +1.7 | 0.58 | 2 | 247 |  | 100 | +1.4 | +0.02 | +0.2 |
| 31 | Eric Lauer | - - - | 31 | SP | 98 | 38° | 0.94 | hybrid | 89 | 97 | 103 | 89 | SI (98, 0.65, 0.30) | +1.3 | 0.39 | 1 | 181 | Y | 90 | +1.1 | +0.06 | +0.5 |
| 32 | Michael McGreevy | STL | 25 | SP | 132 | 34° | 0.82 | supinator | 81 | 99 | 111 | 95 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 311 |  | nan | +nan | +nan | +nan |
| 33 | Lucas Giolito | SDP | 31 | SP | 29 | 56° | 0.99 | pronator | 87 | 98 | 91 | 82 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 189 |  | 87 | +0.0 | +0.00 | +0.0 |
| 34 | Simeon Woods Richardson | - - - | 25 | SP | 63 | 50° | 0.96 | pronator | 87 | 99 | 93 | 85 | FC (95, 0.38, 0.05) | +1.0 | 0.05 | 1 | 310 |  | 88 | +0.9 | +0.03 | +0.2 |
| 35 | Camilo Doval | - - - | 28 | RP | 47 | 17° | nan | unknown | 100 | 101 | 99 | 101 | FF (100, 0.70, 0.10) | +0.0 | 0.00 | 1 | 115 |  | 100 | +0.0 | +0.00 | +0.0 |
| 36 | Miles Mikolas | WSN | 37 | RP | 116 | 43° | 0.90 | lean_supinator | 89 | 99 | 108 | 96 | FC (98, 0.25, 0.05) | +1.2 | 0.06 | 1 | 150 |  | 91 | +1.0 | +0.03 | +0.3 |
| 37 | Tatsuya Imai | HOU | 28 | SP | 64 | 24° | 0.97 | pronator | 87 | 97 | 97 | 86 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 309 |  | 87 | +0.0 | +0.00 | +0.0 |
| 38 | John King | MIA | 31 | RP | 48 | 25° | nan | unknown | 94 | 99 | 98 | 93 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 57 |  | 94 | +0.0 | +0.00 | +0.0 |
| 39 | Carmen Mlodzinski | PIT | 27 | RP | 102 | 35° | 0.94 | lean_supinator | 92 | 99 | 105 | 96 | nan (nan, nan, nan) | +nan | 0.00 | 0 | 768 | Y | nan | +nan | +nan | +nan |
| 40 | Matt Svanson | STL | 27 | RP | 43 | 27° | nan | unknown | 96 | 101 | 100 | 96 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 425 |  | 96 | +0.0 | +0.00 | +0.0 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Randy Dobnak | KCR | SP | 20° | supinator | 82 | CU | 116 | 0.33 | 0.02 | +4.8 | 86 | +0.13 |
| 2 | Rhett Lowder | CIN | SP | 26° | supinator | 86 | CU | 111 | 0.35 | 0.02 | +3.5 | 90 | +0.16 |
| 3 | Ethan Roberts | CHC | RP | 37° | unknown | 96 | CU | 120 | 0.25 | 0.01 | +3.3 | 100 | +0.05 |
| 4 | Jake Woodford | - - - | RP | 26° | unknown | 98 | KC | 120 | 0.23 | 0.01 | +3.0 | 101 | +0.04 |
| 5 | Albert Suárez | BAL | RP | 46° | hybrid | 85 | SL | 104 | 0.90 | 0.34 | +2.8 | 87 | +0.05 |
| 6 | Eduardo Rodriguez | ARI | SP | 42° | supinator | 92 | SL | 111 | 0.82 | 0.32 | +2.7 | 94 | +0.19 |
| 7 | Kirby Yates | - - - | RP | 19° | lean_pronator | 88 | SL | 108 | 0.85 | 0.16 | +2.7 | 91 | +0.04 |
| 8 | Zack Littell | - - - | SP | 43° | hybrid | 83 | CU | 102 | 0.33 | 0.02 | +2.6 | 86 | +0.15 |
| 9 | Brennan Bernardino | COL | RP | 16° | supinator | 91 | SL | 110 | 0.80 | 0.14 | +2.6 | 94 | +0.04 |
| 10 | Jalen Beeks | TEX | RP | 47° | hybrid | 89 | SL | 107 | 0.78 | 0.15 | +2.5 | 91 | +0.03 |
| 11 | Brady Singer | CIN | SP | 22° | supinator | 92 | CU | 110 | 0.30 | 0.03 | +2.5 | 95 | +0.14 |
| 12 | Luis Castillo | - - - | SP | 19° | supinator | 97 | CU | 114 | 0.28 | 0.03 | +2.5 | 99 | +0.13 |
| 13 | Will Klein | LAD | RP | 45° | pronator | 95 | SI | 112 | 0.28 | 0.19 | +2.4 | 97 | +0.03 |
| 14 | Julian Garcia | CIN | RP | 56° | supinator | 86 | CU | 103 | 0.50 | 0.02 | +2.4 | 89 | +0.03 |
| 15 | Dennis Santana | - - - | RP | 31° | hybrid | 92 | CU | 108 | 0.20 | 0.04 | +2.3 | 94 | +0.03 |
| 16 | Dean Kremer | - - - | SP | 44° | pronator | 90 | SL | 107 | 0.75 | 0.20 | +2.3 | 93 | +0.06 |
| 17 | Raisel Iglesias | ATL | RP | 29° | supinator | 96 | CU | 112 | 0.20 | 0.02 | +2.3 | 98 | +0.04 |
| 18 | Taylor Clarke | ARI | RP | 45° | unknown | 92 | CU | 108 | 0.38 | 0.04 | +2.2 | 94 | +0.04 |
| 19 | Martín Pérez | ATL | SP | 45° | pronator | 86 | SL | 102 | 0.50 | 0.01 | +2.2 | 88 | +0.12 |
| 20 | Tim Mayza | PHI | RP | 43° | lean_supinator | 97 | CU | 113 | 0.20 | 0.02 | +2.2 | 100 | +0.04 |
| 21 | Shaun Anderson | LAA | RP | 46° | supinator | 86 | CU | 102 | 0.53 | 0.04 | +2.2 | 89 | +0.03 |
| 22 | Jose Quintana | COL | SP | 43° | supinator | 81 | FC | 96 | 0.40 | 0.05 | +2.2 | 83 | +0.06 |
| 23 | Travis Adams | MIN | RP | 43° | supinator | 93 | CU | 108 | 0.40 | 0.04 | +2.1 | 95 | +0.03 |
| 24 | Huascar Brazobán | - - - | RP | 37° | lean_pronator | 96 | SL | 111 | 0.75 | 0.05 | +2.1 | 98 | +0.04 |
| 25 | Jared Jones | PIT | SP | 41° | supinator | 101 | SI | 115 | 0.38 | 0.24 | +2.1 | 103 | +0.06 |

## Named checks

- **Trey Yesavage** (TOR, SP): slot 66°, eff4 0.98, pronator; Stuff+ 108 (own 101), Loc+ 90; reachable 2, best add CU (prec Stf+ 111, share 0.40, P 0.02), gain +0.4, ΣEV 0.01, pool n=16, drop-recipe N → proj Stf+ 108, ΔWAR +0.02
- **Carson Palmquist** (WSN, SP): slot 12°, eff4 0.90, lean_supinator; Stuff+ 107 (own 99), Loc+ 93; reachable 1, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=29, drop-recipe N → proj Stf+ 107, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 11°, eff4 0.82, supinator; Stuff+ 101 (own 100), Loc+ 106; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=36, drop-recipe N → proj Stf+ 101, ΔWAR +0.00