# 2026 target cards (as of end of 2026 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Aaron Nola | PHI | 33 | SP | 130 | 18° | 0.95 | lean_supinator | 104 | 99 | 103 | 107 | SL (109, 0.82, 0.23) | +0.7 | 0.16 | 1 | 116 | Y | 105 | +0.6 | +0.04 | +0.3 |
| 2 | Paul Skenes | PIT | 24 | SP | 134 | 26° | 0.97 | pronator | 99 | 101 | 108 | 106 | CU (109, 0.38, 0.03) | +1.4 | 0.04 | 2 | 343 | Y | 100 | +1.2 | +0.09 | +0.7 |
| 3 | Chase Petty | CIN | 23 | RP | 31 | 31° | 0.99 | pronator | 100 | 101 | 100 | 99 | KC (115, 0.23, 0.01) | +2.2 | 0.03 | 3 | 290 | Y | 102 | +1.9 | +0.03 | +0.2 |
| 4 | JP Sears | SDP | 30 | SP | 32 | 30° | 0.98 | pronator | 91 | 98 | 99 | 92 | CU (105, 0.20, 0.03) | +1.9 | 0.06 | 1 | 118 | Y | 93 | +1.6 | +0.05 | +0.4 |
| 5 | Rhett Lowder | CIN | 24 | SP | 101 | 26° | 0.89 | supinator | 86 | 100 | 104 | 93 | CU (110, 0.33, 0.02) | +3.4 | 0.13 | 2 | 300 |  | 90 | +2.9 | +0.16 | +1.3 |
| 6 | Walbert Ureña | LAA | 22 | SP | 107 | 43° | 0.88 | supinator | 99 | 101 | 103 | 105 | CU (110, 0.25, 0.03) | +1.5 | 0.06 | 2 | 403 |  | 101 | +1.3 | +0.07 | +0.6 |
| 7 | Dennis Santana | - - - | 30 | RP | 42 | 31° | 0.93 | hybrid | 92 | 100 | 96 | 87 | CU (108, 0.20, 0.03) | +2.3 | 0.06 | 1 | 533 | Y | 94 | +2.0 | +0.03 | +0.3 |
| 8 | Randy Dobnak | KCR | 31 | SP | 41 | 20° | 0.87 | supinator | 82 | 99 | 109 | 91 | CU (113, 0.35, 0.02) | +4.3 | 0.21 | 2 | 47 |  | 86 | +3.7 | +0.12 | +1.0 |
| 9 | Mason Black | KCR | 26 | RP | 25 | 26° | 0.99 | pronator | 93 | 98 | 99 | 96 | FS (99, 0.23, 0.03) | +0.9 | 0.03 | 1 | 247 | Y | 94 | +0.7 | +0.01 | +0.1 |
| 10 | Casey Legumina | - - - | 29 | RP | 54 | 16° | 0.95 | pronator | 112 | 101 | 96 | 105 | KC (120, 0.20, 0.01) | +1.2 | 0.01 | 1 | 66 | Y | 113 | +1.0 | +0.02 | +0.2 |
| 11 | Albert Suárez | BAL | 36 | RP | 51 | 46° | 0.91 | hybrid | 85 | 98 | 104 | 91 | SL (104, 0.90, 0.31) | +2.8 | 1.21 | 2 | 317 |  | 87 | +2.3 | +0.05 | +0.4 |
| 12 | Beck Way | KCR | 26 | RP | 23 | 31° | 0.96 | pronator | 99 | 98 | 92 | 91 | CU (102, 0.28, 0.01) | +0.4 | 0.00 | 1 | 529 | Y | 99 | +0.4 | +0.01 | +0.0 |
| 13 | Eric Lauer | - - - | 31 | SP | 98 | 38° | 0.94 | hybrid | 89 | 97 | 103 | 89 | SI (98, 0.65, 0.28) | +1.3 | 0.36 | 1 | 181 | Y | 90 | +1.1 | +0.06 | +0.5 |
| 14 | Kevin Ginkel | ARI | 32 | RP | 52 | 42° | 0.89 | supinator | 94 | 101 | 110 | 103 | CU (110, 0.50, 0.03) | +2.2 | 0.06 | 3 | 256 |  | 97 | +1.9 | +0.04 | +0.3 |
| 15 | Luis Castillo | - - - | 33 | SP | 115 | 19° | 0.87 | supinator | 97 | 100 | 108 | 102 | CU (114, 0.28, 0.03) | +2.5 | 0.09 | 2 | 137 |  | 99 | +2.1 | +0.13 | +1.1 |
| 16 | Jalen Beeks | TEX | 32 | RP | 26 | 47° | 0.92 | hybrid | 89 | 97 | 101 | 91 | SL (107, 0.78, 0.12) | +2.5 | 0.47 | 3 | 303 |  | 91 | +2.1 | +0.03 | +0.3 |
| 17 | Ryan Johnson | LAA | 23 | SP | 60 | 20° | nan | unknown | 92 | 99 | 92 | 85 | CU (102, 0.35, 0.01) | +1.3 | 0.01 | 2 | 143 |  | 94 | +1.1 | +0.04 | +0.3 |
| 18 | Sam Aldegheri | LAA | 24 | SP | 33 | 44° | 0.93 | lean_supinator | 90 | 96 | 96 | 87 | SI (97, 0.57, 0.22) | +1.1 | 0.24 | 1 | 239 |  | 91 | +0.9 | +0.03 | +0.2 |
| 19 | Keaton Winn | SFG | 28 | RP | 43 | 40° | 0.88 | supinator | 98 | 101 | 101 | 100 | CU (111, 0.35, 0.03) | +1.8 | 0.05 | 2 | 513 |  | 99 | +1.6 | +0.03 | +0.2 |
| 20 | Sandy Alcantara | MIA | 30 | SP | 170 | 33° | 0.95 | lean_pronator | 101 | 102 | 103 | 103 | CU (113, 0.38, 0.02) | +1.8 | 0.04 | 1 | 618 | Y | 102 | +1.5 | +0.14 | +1.1 |
| 21 | Raisel Iglesias | ATL | 36 | RP | 45 | 29° | 0.86 | supinator | 96 | 101 | 105 | 100 | CU (112, 0.20, 0.02) | +2.3 | 0.04 | 1 | 472 |  | 98 | +1.9 | +0.04 | +0.3 |
| 22 | Joe Ryan | MIN | 30 | SP | 125 | 23° | 0.97 | pronator | 107 | 101 | 107 | 111 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 153 | Y | 107 | +0.0 | +0.00 | +0.0 |
| 23 | Landen Roupp | SFG | 27 | SP | 129 | 22° | 0.83 | supinator | 99 | 102 | 105 | 104 | SL (108, 0.75, 0.10) | +1.3 | 0.14 | 1 | 183 |  | 100 | +1.1 | +0.08 | +0.6 |
| 24 | Ron Marinaccio | - - - | 30 | RP | 57 | 26° | 0.99 | pronator | 94 | 99 | 94 | 89 | SI (98, 0.47, 0.16) | +0.4 | 0.07 | 1 | 357 | Y | 95 | +0.4 | +0.01 | +0.1 |
| 25 | Dean Kremer | - - - | 30 | SP | 53 | 44° | 0.98 | pronator | 90 | 98 | 95 | 89 | SL (107, 0.75, 0.22) | +2.3 | 0.50 | 1 | 748 |  | 93 | +1.9 | +0.06 | +0.5 |
| 26 | Kirby Yates | - - - | 39 | RP | 35 | 19° | 0.94 | lean_pronator | 88 | 99 | 101 | 88 | SL (108, 0.82, 0.14) | +2.7 | 0.51 | 4 | 132 | Y | 91 | +2.3 | +0.04 | +0.3 |
| 27 | Joel Kuhnel | - - - | 31 | RP | 35 | 39° | 0.70 | supinator | 97 | 100 | 98 | 94 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 204 |  | 97 | +0.0 | +0.00 | +0.0 |
| 28 | Tanner Gordon | COL | 28 | RP | 71 | 45° | 0.98 | pronator | 86 | 99 | 109 | 93 | FC (95, 0.25, 0.05) | +1.3 | 0.06 | 1 | 320 | Y | 87 | +1.1 | +0.03 | +0.3 |
| 29 | Trey Gibson | BAL | 24 | SP | 33 | 33° | 0.96 | pronator | 97 | 100 | 92 | 93 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 635 | Y | 97 | +0.0 | +0.00 | +0.0 |
| 30 | Kumar Rocker | TEX | 26 | SP | 116 | 32° | 0.90 | supinator | 92 | 99 | 96 | 91 | CU (104, 0.33, 0.04) | +1.7 | 0.08 | 1 | 528 |  | 93 | +1.4 | +0.09 | +0.7 |
| 31 | Zach Agnos | COL | 25 | RP | 70 | 38° | 0.93 | lean_supinator | 90 | 99 | 100 | 91 | CU (102, 0.45, 0.01) | +1.7 | 0.02 | 1 | 820 | Y | 92 | +1.4 | +0.04 | +0.3 |
| 32 | Wandy Peralta | SDP | 34 | RP | 62 | 45° | 0.98 | pronator | 101 | 99 | 105 | 106 | CU (108, 0.28, 0.02) | +1.1 | 0.02 | 1 | 326 | Y | 102 | +0.9 | +0.02 | +0.2 |
| 33 | Huascar Brazobán | - - - | 36 | RP | 59 | 37° | 0.93 | lean_pronator | 96 | 99 | 100 | 97 | CU (110, 0.33, 0.02) | +2.0 | 0.14 | 2 | 756 | Y | 98 | +1.7 | +0.04 | +0.3 |
| 34 | Jared Jones | PIT | 24 | SP | 64 | 41° | 0.90 | hybrid | 101 | 102 | 107 | 110 | SI (120, 0.23, 0.13) | +2.7 | 0.35 | 1 | 456 |  | 103 | +2.3 | +0.08 | +0.6 |
| 35 | Edgardo Henriquez | LAD | 24 | RP | 49 | 38° | 0.94 | lean_supinator | 127 | 102 | 80 | 107 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 883 | Y | 127 | +0.0 | +0.00 | +0.0 |
| 36 | Michael Wacha | KCR | 34 | SP | 155 | 54° | 0.99 | pronator | 98 | 100 | 101 | 99 | — (nan, nan, nan) | +nan | 0.00 | 0 | 162 |  | nan | +nan | +nan | +nan |
| 37 | Franco Aleman | CLE | 26 | RP | 18 | 18° | 0.95 | hybrid | 101 | 99 | 92 | 92 | CU (114, 0.23, 0.01) | +1.9 | 0.02 | 2 | 95 | Y | 102 | +1.6 | +0.03 | +0.2 |
| 38 | Craig Yoho | - - - | 26 | RP | 25 | 20° | 0.99 | pronator | 95 | 100 | 97 | 96 | SL (107, 0.70, 0.10) | +1.7 | 0.18 | 1 | 162 | Y | 96 | +1.5 | +0.02 | +0.2 |
| 39 | Germán Márquez | SDP | 31 | SP | 53 | 39° | 0.98 | pronator | 87 | 97 | 99 | 86 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 669 | Y | 87 | +0.0 | +0.00 | +0.0 |
| 40 | Jacob Lopez | ATH | 28 | SP | 88 | 23° | 0.94 | lean_supinator | 97 | 99 | 102 | 98 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 98 | Y | 97 | +0.0 | +0.00 | +0.0 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Randy Dobnak | KCR | SP | 20° | supinator | 82 | CU | 113 | 0.35 | 0.02 | +4.3 | 86 | +0.12 |
| 2 | Rhett Lowder | CIN | SP | 26° | supinator | 86 | CU | 110 | 0.33 | 0.02 | +3.4 | 90 | +0.16 |
| 3 | Ethan Roberts | CHC | RP | 37° | unknown | 96 | CU | 120 | 0.25 | 0.01 | +3.3 | 100 | +0.05 |
| 4 | Jake Woodford | - - - | RP | 26° | unknown | 98 | KC | 120 | 0.23 | 0.00 | +3.0 | 101 | +0.04 |
| 5 | Albert Suárez | BAL | RP | 46° | hybrid | 85 | SL | 104 | 0.90 | 0.31 | +2.8 | 87 | +0.05 |
| 6 | Kirby Yates | - - - | RP | 19° | lean_pronator | 88 | SL | 108 | 0.82 | 0.14 | +2.7 | 91 | +0.04 |
| 7 | Eduardo Rodriguez | ARI | SP | 42° | supinator | 92 | SL | 111 | 0.82 | 0.29 | +2.7 | 94 | +0.19 |
| 8 | Jared Jones | PIT | SP | 41° | hybrid | 101 | SI | 120 | 0.23 | 0.13 | +2.7 | 103 | +0.08 |
| 9 | Zack Littell | - - - | SP | 43° | hybrid | 83 | CU | 102 | 0.33 | 0.02 | +2.6 | 86 | +0.15 |
| 10 | Brennan Bernardino | COL | RP | 16° | supinator | 91 | SL | 110 | 0.80 | 0.13 | +2.6 | 94 | +0.04 |
| 11 | Jalen Beeks | TEX | RP | 47° | hybrid | 89 | SL | 107 | 0.78 | 0.12 | +2.5 | 91 | +0.03 |
| 12 | Brady Singer | CIN | SP | 22° | supinator | 92 | CU | 110 | 0.30 | 0.04 | +2.5 | 95 | +0.14 |
| 13 | Luis Castillo | - - - | SP | 19° | supinator | 97 | CU | 114 | 0.28 | 0.03 | +2.5 | 99 | +0.13 |
| 14 | Martín Pérez | ATL | SP | 45° | pronator | 86 | SL | 104 | 0.53 | 0.01 | +2.5 | 88 | +0.13 |
| 15 | Julian Garcia | CIN | RP | 56° | supinator | 86 | CU | 103 | 0.50 | 0.02 | +2.4 | 89 | +0.03 |
| 16 | Slade Cecconi | CLE | SP | 40° | lean_pronator | 94 | FS | 111 | 0.28 | 0.01 | +2.4 | 96 | +0.12 |
| 17 | Dennis Santana | - - - | RP | 31° | hybrid | 92 | CU | 108 | 0.20 | 0.03 | +2.3 | 94 | +0.03 |
| 18 | Raisel Iglesias | ATL | RP | 29° | supinator | 96 | CU | 112 | 0.20 | 0.02 | +2.3 | 98 | +0.04 |
| 19 | Dean Kremer | - - - | SP | 44° | pronator | 90 | SL | 107 | 0.75 | 0.22 | +2.3 | 93 | +0.06 |
| 20 | Taylor Clarke | ARI | RP | 45° | unknown | 92 | CU | 108 | 0.38 | 0.03 | +2.2 | 94 | +0.04 |
| 21 | Kevin Ginkel | ARI | RP | 42° | supinator | 94 | CU | 110 | 0.50 | 0.03 | +2.2 | 97 | +0.04 |
| 22 | Shaun Anderson | LAA | RP | 46° | supinator | 86 | CU | 102 | 0.53 | 0.03 | +2.2 | 89 | +0.03 |
| 23 | Chase Petty | CIN | RP | 31° | pronator | 100 | KC | 115 | 0.23 | 0.01 | +2.2 | 102 | +0.03 |
| 24 | Jose Quintana | COL | SP | 43° | supinator | 81 | FC | 96 | 0.40 | 0.05 | +2.2 | 83 | +0.06 |
| 25 | Travis Adams | MIN | RP | 43° | supinator | 93 | CU | 108 | 0.40 | 0.04 | +2.1 | 95 | +0.03 |

## Named checks

- **Trey Yesavage** (TOR, SP): slot 66°, eff4 0.98, pronator; Stuff+ 108 (own 101), Loc+ 90; reachable 2, best add CU (prec Stf+ 111, share 0.40, P 0.02), gain +0.4, ΣEV 0.01, pool n=16, drop-recipe N → proj Stf+ 108, ΔWAR +0.02
- **Carson Palmquist** (WSN, SP): slot 12°, eff4 0.90, lean_supinator; Stuff+ 107 (own 99), Loc+ 93; reachable 1, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=29, drop-recipe N → proj Stf+ 107, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 11°, eff4 0.82, supinator; Stuff+ 101 (own 100), Loc+ 106; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=36, drop-recipe N → proj Stf+ 101, ΔWAR +0.00