# 2025 target cards (as of end of 2025 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Erik Miller | SFG | 27 | RP | 30 | 38° | 0.94 | hybrid | 107 | 100 | 88 | 97 | CU (114, 0.33, 0.01) | +1.0 | 0.01 | 1 | 138 | Y | 108 | +0.9 | +0.01 | +0.1 |
| 2 | Pete Fairbanks | TBR | 31 | RP | 60 | 56° | 0.89 | supinator | 115 | 100 | 99 | 109 | KC (121, 0.23, 0.01) | +0.8 | 0.00 | 3 | 90 |  | 116 | +0.7 | +0.02 | +0.1 |
| 3 | PJ Poulin | WSN | 28 | RP | 24 | 17° | 0.97 | pronator | 96 | 98 | 91 | 87 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 29 | Y | 96 | +0.0 | +0.00 | +0.0 |
| 4 | Aaron Nola | PHI | 32 | SP | 94 | 20° | 0.95 | pronator | 102 | 100 | 108 | 109 | SL (104, 0.78, 0.07) | +0.3 | 0.02 | 1 | 128 | Y | 102 | +0.3 | +0.01 | +0.1 |
| 5 | Jorge López | WSN | 32 | RP | 24 | 39° | 0.96 | pronator | 98 | 99 | 96 | 91 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 747 | Y | 98 | +0.0 | +0.00 | +0.0 |
| 6 | José Ureña | - - - | 33 | RP | 55 | 28° | 0.99 | pronator | 87 | 100 | 101 | 92 | CU (105, 0.20, 0.01) | +2.5 | 0.06 | 2 | 386 | Y | 90 | +2.1 | +0.05 | +0.4 |
| 7 | Konnor Pilkington | WSN | 27 | RP | 28 | 30° | 0.95 | pronator | 97 | 97 | 84 | 83 | CU (115, 0.23, 0.01) | +2.5 | 0.05 | 2 | 149 | Y | 100 | +2.1 | +0.03 | +0.3 |
| 8 | Anthony Molina | COL | 23 | RP | 34 | 50° | 0.99 | pronator | 94 | 97 | 111 | 104 | FC (102, 0.23, 0.37) | +1.2 | 0.46 | 2 | 459 | Y | 95 | +1.0 | +0.02 | +0.1 |
| 9 | Germán Márquez | COL | 30 | SP | 126 | 40° | 0.96 | lean_supinator | 86 | 98 | 98 | 85 | FC (102, 0.28, 0.03) | +2.2 | 0.07 | 1 | 498 | Y | 88 | +1.9 | +0.13 | +1.0 |
| 10 | Hayden Wesneski | HOU | 27 | SP | 32 | 46° | 0.82 | supinator | 96 | 101 | 111 | 105 | — (nan, nan, nan) | +nan | 0.00 | 0 | 523 |  | nan | +nan | +nan | +nan |
| 11 | Lou Trivino III | - - - | 33 | RP | 47 | 36° | 0.94 | lean_supinator | 95 | 99 | 96 | 92 | CU (105, 0.40, 0.01) | +1.4 | 0.01 | 1 | 669 | Y | 97 | +1.2 | +0.02 | +0.2 |
| 12 | Sonny Gray | STL | 35 | SP | 180 | 47° | 0.58 | supinator | 102 | 100 | 100 | 104 | — (nan, nan, nan) | +nan | 0.00 | 0 | 523 |  | nan | +nan | +nan | +nan |
| 13 | Lucas Erceg | KCR | 30 | RP | 61 | 42° | 0.98 | pronator | 99 | 101 | 106 | 105 | KC (114, 0.20, 0.01) | +2.2 | 0.02 | 1 | 732 | Y | 101 | +1.9 | +0.05 | +0.4 |
| 14 | Ryan Yarbrough | NYY | 33 | RP | 64 | 11° | 0.99 | pronator | 96 | 96 | 107 | 99 | CU (103, 0.25, 0.01) | +0.9 | 0.01 | 1 | 19 |  | 97 | +0.8 | +0.02 | +0.2 |
| 15 | Valente Bellozo | MIA | 25 | RP | 81 | 48° | 0.87 | supinator | 93 | 99 | 98 | 90 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 330 |  | 93 | +0.0 | +0.00 | +0.0 |
| 16 | Joel Peguero | SFG | 28 | RP | 22 | 43° | 0.87 | supinator | 113 | 101 | 94 | 104 | — (nan, nan, nan) | +0.0 | 0.00 | 2 | 711 |  | 113 | +0.0 | +0.00 | +0.0 |
| 17 | Michael Wacha | KCR | 33 | SP | 172 | 52° | 0.99 | pronator | 96 | 100 | 103 | 99 | — (nan, nan, nan) | +nan | 0.00 | 0 | 266 |  | nan | +nan | +nan | +nan |
| 18 | Zack Kelly | BOS | 30 | RP | 35 | 38° | 0.94 | lean_supinator | 109 | 100 | 101 | 106 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 556 | Y | 109 | +0.0 | +0.00 | +0.0 |
| 19 | Chase Dollander | COL | 23 | SP | 98 | 25° | 0.94 | lean_supinator | 97 | 100 | 98 | 95 | SL (114, 0.90, 0.42) | +2.4 | 0.98 | 1 | 271 | Y | 100 | +2.0 | +0.11 | +0.9 |
| 20 | Tanner Gordon | COL | 27 | SP | 75 | 43° | 0.99 | pronator | 89 | 99 | 104 | 91 | CU (96, 0.35, 0.02) | +1.0 | 0.03 | 3 | 352 | Y | 90 | +0.9 | +0.04 | +0.3 |
| 21 | Thomas Hatch | - - - | 30 | RP | 34 | 40° | 0.81 | supinator | 90 | 101 | 96 | 91 | CU (106, 0.35, 0.01) | +2.2 | 0.02 | 1 | 492 |  | 92 | +1.8 | +0.03 | +0.2 |
| 22 | Bubba Chandler | PIT | 22 | SP | 31 | 44° | 0.95 | lean_pronator | 105 | 103 | 103 | 111 | SI (116, 0.33, 0.08) | +1.5 | 0.13 | 1 | 601 |  | 107 | +1.3 | +0.04 | +0.3 |
| 23 | Yennier Cano | BAL | 31 | RP | 58 | 17° | 0.87 | supinator | 101 | 100 | 96 | 97 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 22 |  | 101 | +0.0 | +0.00 | +0.0 |
| 24 | Jack Perkins | ATH | 25 | RP | 38 | 31° | 0.96 | pronator | 100 | 101 | 96 | 96 | SI (103, 0.50, 0.50) | +0.4 | 0.21 | 1 | 444 | Y | 101 | +0.3 | +0.01 | +0.0 |
| 25 | Spencer Arrighetti | HOU | 25 | SP | 35 | 23° | 0.95 | lean_supinator | 102 | 101 | 94 | 97 | — (nan, nan, nan) | +nan | 0.00 | 0 | 178 | Y | nan | +nan | +nan | +nan |
| 26 | Danny Coulombe | - - - | 35 | RP | 43 | 55° | 0.71 | supinator | 103 | 95 | 105 | 107 | CU (111, 0.45, 0.01) | +1.2 | 0.01 | 2 | 40 |  | 104 | +1.0 | +0.02 | +0.1 |
| 27 | Andrew Heaney | - - - | 34 | SP | 122 | 26° | 0.99 | pronator | 90 | 100 | 104 | 93 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 90 | Y | 90 | +0.0 | +0.00 | +0.0 |
| 28 | Jesús Luzardo | PHI | 27 | SP | 183 | 34° | 0.95 | pronator | 106 | 101 | 109 | 113 | CU (112, 0.20, 0.01) | +0.9 | 0.01 | 1 | 177 | Y | 107 | +0.7 | +0.07 | +0.6 |
| 29 | Juan Morillo | ARI | 26 | RP | 34 | 46° | 0.92 | hybrid | 110 | 102 | 94 | 104 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 435 |  | 110 | +0.0 | +0.00 | +0.0 |
| 30 | Aaron Civale | - - - | 30 | SP | 102 | 43° | 0.94 | lean_supinator | 92 | 99 | 96 | 89 | — (nan, nan, nan) | +nan | 0.00 | 0 | 681 |  | nan | +nan | +nan | +nan |
| 31 | Lyon Richardson | CIN | 25 | RP | 37 | 30° | 0.93 | lean_supinator | 93 | 97 | 95 | 88 | SL (112, 0.93, 0.32) | +2.7 | 0.91 | 2 | 466 | Y | 96 | +2.3 | +0.04 | +0.3 |
| 32 | Jesus Tinoco | MIA | 30 | RP | 19 | 21° | 0.91 | hybrid | 97 | 102 | 107 | 105 | CU (117, 0.20, 0.01) | +2.7 | 0.02 | 1 | 170 |  | 100 | +2.3 | +0.04 | +0.3 |
| 33 | Brandon Waddell | NYM | 31 | RP | 31 | 44° | 0.75 | supinator | 96 | 100 | 103 | 101 | CU (108, 0.40, 0.05) | +1.6 | 0.08 | 1 | 195 |  | 98 | +1.4 | +0.02 | +0.2 |
| 34 | Jacob Lopez | ATH | 27 | SP | 92 | 23° | 0.94 | lean_supinator | 98 | 99 | 101 | 100 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 79 | Y | 98 | +0.0 | +0.00 | +0.0 |
| 35 | Brock Stewart | - - - | 33 | RP | 37 | 25° | 0.73 | supinator | 110 | 102 | 101 | 109 | CU (113, 0.20, 0.01) | +0.5 | 0.00 | 1 | 262 |  | 110 | +0.4 | +0.01 | +0.1 |
| 36 | Corbin Martin | BAL | 29 | RP | 18 | 43° | 0.83 | supinator | 97 | 100 | 96 | 95 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 732 |  | 97 | +0.0 | +0.00 | +0.0 |
| 37 | Bryan Baker | - - - | 30 | RP | 68 | 54° | 0.96 | pronator | 109 | 102 | 102 | 109 | CU (112, 0.38, 0.02) | +0.5 | 0.01 | 2 | 282 |  | 109 | +0.5 | +0.01 | +0.1 |
| 38 | Kodai Senga | NYM | 32 | SP | 113 | 45° | 0.88 | supinator | 93 | 99 | 96 | 93 | CU (104, 0.42, 0.03) | +1.5 | 0.06 | 2 | 683 |  | 94 | +1.3 | +0.08 | +0.6 |
| 39 | Sawyer Gipson-Long | DET | 27 | RP | 31 | 29° | 0.88 | supinator | 95 | 100 | 105 | 99 | CU (102, 0.53, 0.04) | +1.1 | 0.04 | 1 | 431 |  | 96 | +0.9 | +0.01 | +0.1 |
| 40 | Raisel Iglesias | ATL | 35 | RP | 67 | 31° | 0.86 | supinator | 97 | 101 | 106 | 103 | CU (111, 0.25, 0.01) | +1.9 | 0.03 | 2 | 506 |  | 99 | +1.7 | +0.05 | +0.4 |

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

- **Carson Palmquist** (COL, SP): slot 16°, eff4 0.93, lean_supinator; Stuff+ 93 (own 97), Loc+ 91; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=33, drop-recipe Y → proj Stf+ 93, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 16°, eff4 0.90, hybrid; Stuff+ 90 (own 99), Loc+ 100; reachable 1, best add CU (prec Stf+ 116, share 0.20, P 0.01), gain +3.6, ΣEV 0.04, pool n=75, drop-recipe N → proj Stf+ 94, ΔWAR +0.15