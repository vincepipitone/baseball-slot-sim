# 2026 target cards (as of end of 2026 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Tyler Glasnow | LAD | 32 | SP | 39 | 57° | 0.76 | supinator | 104 | 101 | 95 | 101 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 246 |  | 104 | +0.0 | +0.00 | +0.0 |
| 2 | Raisel Iglesias | ATL | 36 | RP | 45 | 29° | 0.86 | supinator | 96 | 101 | 105 | 100 | CU (112, 0.20, 0.02) | +2.3 | 0.04 | 1 | 472 |  | 98 | +1.9 | +0.04 | +0.3 |
| 3 | Walbert Ureña | LAA | 22 | SP | 107 | 43° | 0.88 | supinator | 99 | 101 | 103 | 105 | CU (112, 0.25, 0.02) | +1.7 | 0.07 | 2 | 403 |  | 101 | +1.5 | +0.09 | +0.7 |
| 4 | Aaron Nola | PHI | 33 | SP | 130 | 18° | 0.95 | lean_supinator | 104 | 99 | 103 | 107 | SL (107, 0.82, 0.19) | +0.5 | 0.09 | 1 | 116 | Y | 105 | +0.4 | +0.03 | +0.2 |
| 5 | Michael Wacha | KCR | 34 | SP | 155 | 54° | 0.99 | pronator | 98 | 100 | 101 | 99 | — (nan, nan, nan) | +nan | 0.00 | 0 | 162 |  | nan | +nan | +nan | +nan |
| 6 | Garrett Crochet | BOS | 27 | SP | 30 | 32° | 0.87 | supinator | 113 | 100 | 95 | 105 | CU (118, 0.23, 0.01) | +0.6 | 0.01 | 1 | 188 |  | 114 | +0.5 | +0.02 | +0.1 |
| 7 | Beck Way | KCR | 26 | RP | 23 | 31° | 0.96 | pronator | 99 | 98 | 92 | 91 | CU (103, 0.23, 0.01) | +0.5 | 0.00 | 1 | 529 | Y | 99 | +0.4 | +0.01 | +0.1 |
| 8 | Joel Kuhnel | - - - | 31 | RP | 35 | 39° | 0.70 | supinator | 97 | 100 | 98 | 94 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 204 |  | 97 | +0.0 | +0.00 | +0.0 |
| 9 | Paul Skenes | PIT | 24 | SP | 134 | 26° | 0.97 | pronator | 99 | 101 | 108 | 106 | CU (110, 0.23, 0.03) | +1.6 | 0.05 | 2 | 343 | Y | 100 | +1.4 | +0.10 | +0.8 |
| 10 | Nick Mears | KCR | 29 | RP | 19 | 56° | 0.98 | pronator | 100 | 101 | 92 | 91 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 314 |  | 100 | +0.0 | +0.00 | +0.0 |
| 11 | Brandon Sproat | MIL | 25 | SP | 95 | 32° | 0.89 | supinator | 100 | 100 | 94 | 93 | — (nan, nan, nan) | +nan | 0.00 | 0 | 582 |  | nan | +nan | +nan | +nan |
| 12 | Brandon Williamson | CIN | 28 | SP | 28 | 41° | 0.99 | pronator | 98 | 98 | 90 | 91 | — (nan, nan, nan) | +nan | 0.00 | 0 | 169 |  | nan | +nan | +nan | +nan |
| 13 | Michael Soroka | ARI | 28 | SP | 92 | 25° | 0.80 | supinator | 94 | 100 | 106 | 98 | CU (106, 0.42, 0.05) | +1.7 | 0.08 | 1 | 340 |  | 96 | +1.5 | +0.07 | +0.6 |
| 14 | JP Sears | SDP | 30 | SP | 32 | 30° | 0.98 | pronator | 91 | 98 | 99 | 92 | CU (104, 0.23, 0.03) | +1.8 | 0.06 | 1 | 118 | Y | 93 | +1.6 | +0.05 | +0.4 |
| 15 | Sonny Gray | BOS | 36 | SP | 132 | 46° | 0.59 | supinator | 101 | 101 | 98 | 102 | — (nan, nan, nan) | +nan | 0.00 | 0 | 717 |  | nan | +nan | +nan | +nan |
| 16 | Cole Sulser | TBR | 36 | RP | 46 | 45° | 0.97 | pronator | 98 | 102 | 104 | 103 | KC (101, 0.20, 0.00) | +0.5 | 0.00 | 1 | 750 |  | 98 | +0.4 | +0.01 | +0.1 |
| 17 | Joe Ryan | MIN | 30 | SP | 125 | 23° | 0.97 | pronator | 107 | 101 | 107 | 111 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 153 | Y | 107 | +0.0 | +0.00 | +0.0 |
| 18 | Lance McCullers Jr. | - - - | 32 | SP | 44 | 32° | 0.79 | supinator | 97 | 99 | 96 | 96 | — (nan, nan, nan) | +nan | 0.00 | 0 | 601 |  | nan | +nan | +nan | +nan |
| 19 | Emerson Hancock | SEA | 27 | SP | 128 | 11° | 0.82 | supinator | 101 | 100 | 106 | 101 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 36 |  | 101 | +0.0 | +0.00 | +0.0 |
| 20 | Tyler Holton | DET | 30 | RP | 58 | 40° | 0.83 | supinator | 101 | 100 | 97 | 97 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 285 |  | 101 | +0.0 | +0.00 | +0.0 |
| 21 | Kodai Senga | NYM | 33 | RP | 49 | 47° | 0.86 | supinator | 97 | 100 | 93 | 95 | CU (108, 0.42, 0.05) | +1.5 | 0.07 | 2 | 679 |  | 99 | +1.2 | +0.03 | +0.2 |
| 22 | Phil Maton | CHC | 33 | RP | 27 | 27° | nan | unknown | 103 | 100 | 89 | 94 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 243 |  | 103 | +0.0 | +0.00 | +0.0 |
| 23 | Brandon Pfaadt | ARI | 27 | SP | 92 | 29° | 0.75 | supinator | 94 | 101 | 103 | 99 | — (nan, nan, nan) | +nan | 0.00 | 0 | 475 |  | nan | +nan | +nan | +nan |
| 24 | Ryan Yarbrough | NYY | 34 | RP | 45 | 14° | 0.99 | pronator | 100 | 97 | 101 | 97 | CU (103, 0.20, 0.01) | +0.5 | 0.00 | 1 | 30 |  | 100 | +0.4 | +0.01 | +0.1 |
| 25 | Braxton Ashcraft | PIT | 26 | SP | 141 | 37° | 0.91 | lean_supinator | 106 | 102 | 107 | 110 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 734 |  | 106 | +0.0 | +0.00 | +0.0 |
| 26 | JT Brubaker | SFG | 32 | RP | 57 | 45° | 0.89 | supinator | 90 | 100 | 106 | 98 | FC (101, 0.23, 0.04) | +1.5 | 0.06 | 1 | 517 |  | 91 | +1.3 | +0.03 | +0.2 |
| 27 | Mitch Farris | LAA | 25 | RP | 47 | 51° | 0.99 | pronator | 93 | 97 | 87 | 79 | CU (98, 0.25, 0.04) | +0.8 | 0.03 | 2 | 217 |  | 94 | +0.6 | +0.01 | +0.1 |
| 28 | Andrew Morris | MIN | 24 | RP | 58 | 60° | 0.98 | pronator | 107 | 101 | 100 | 104 | CU (109, 0.33, 0.03) | +0.3 | 0.01 | 1 | 152 |  | 107 | +0.3 | +0.01 | +0.0 |
| 29 | Colin Holderman | CLE | 30 | RP | 49 | 23° | 0.81 | supinator | 108 | 101 | 94 | 97 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 278 |  | 108 | +0.0 | +0.00 | +0.0 |
| 30 | Ryan Johnson | LAA | 23 | SP | 60 | 20° | nan | unknown | 92 | 99 | 92 | 85 | CU (102, 0.35, 0.01) | +1.3 | 0.01 | 2 | 143 |  | 94 | +1.1 | +0.04 | +0.3 |
| 31 | Elmer Rodríguez | NYY | 22 | SP | 17 | 27° | 0.93 | lean_supinator | 94 | 96 | 81 | 75 | FC (99, 0.23, 0.28) | +0.8 | 0.22 | 1 | 352 |  | 94 | +0.7 | +0.02 | +0.2 |
| 32 | Mason Black | KCR | 26 | RP | 25 | 26° | 0.99 | lean_supinator | 93 | 98 | 99 | 96 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 247 | Y | 93 | +0.0 | +0.00 | +0.0 |
| 33 | Zack Wheeler | PHI | 36 | SP | 115 | 22° | 0.88 | supinator | 104 | 102 | 106 | 112 | — (nan, nan, nan) | +nan | 0.00 | 0 | 167 |  | nan | +nan | +nan | +nan |
| 34 | Trey Yesavage | TOR | 22 | SP | 93 | 66° | 0.98 | pronator | 108 | 101 | 90 | 97 | CU (111, 0.40, 0.02) | +0.4 | 0.01 | 2 | 16 |  | 108 | +0.4 | +0.02 | +0.1 |
| 35 | Casey Legumina | - - - | 29 | RP | 54 | 16° | 0.95 | pronator | 112 | 101 | 96 | 105 | KC (120, 0.20, 0.01) | +1.2 | 0.01 | 1 | 66 | Y | 113 | +1.0 | +0.02 | +0.2 |
| 36 | Landen Roupp | SFG | 27 | SP | 129 | 22° | 0.83 | supinator | 99 | 102 | 105 | 104 | SL (107, 0.80, 0.09) | +1.2 | 0.11 | 1 | 183 |  | 100 | +1.0 | +0.07 | +0.6 |
| 37 | Randy Dobnak | KCR | 31 | SP | 41 | 20° | 0.87 | supinator | 82 | 99 | 109 | 91 | CU (116, 0.33, 0.02) | +4.8 | 0.20 | 2 | 47 |  | 86 | +4.1 | +0.13 | +1.1 |
| 38 | Evan Sisk | PIT | 29 | RP | 40 | 22° | 0.84 | supinator | 105 | 96 | 83 | 88 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 84 |  | 105 | +0.0 | +0.00 | +0.0 |
| 39 | Eric Lauer | - - - | 31 | SP | 98 | 38° | 0.94 | hybrid | 89 | 97 | 103 | 89 | SI (98, 0.65, 0.30) | +1.3 | 0.39 | 1 | 181 | Y | 90 | +1.1 | +0.06 | +0.5 |
| 40 | Trevor Rogers | BAL | 28 | SP | 125 | 22° | 0.88 | supinator | 102 | 100 | 105 | 103 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 86 |  | 102 | +0.0 | +0.00 | +0.0 |

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