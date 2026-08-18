# 2025 target cards (as of end of 2025 data) — repertoire lever, precedent-valued

Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). `drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.

Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.

## Top 40 by expected value of reachable additions

| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | José Ureña | - - - | 33 | RP | 55 | 28° | 0.99 | pronator | 87 | 100 | 101 | 92 | CU (113, 0.20, 0.01) | +3.5 | 0.08 | 2 | 386 | Y | 91 | +3.0 | +0.07 | +0.5 |
| 2 | Germán Márquez | COL | 30 | SP | 126 | 40° | 0.96 | pronator | 86 | 98 | 98 | 85 | FS (108, 0.20, 0.01) | +3.2 | 0.03 | 1 | 498 | Y | 89 | +2.7 | +0.19 | +1.5 |
| 3 | Konnor Pilkington | WSN | 27 | RP | 28 | 30° | 0.95 | pronator | 97 | 97 | 84 | 83 | CU (115, 0.23, 0.01) | +2.5 | 0.06 | 2 | 149 | Y | 100 | +2.1 | +0.03 | +0.3 |
| 4 | Erik Miller | SFG | 27 | RP | 30 | 38° | 0.94 | hybrid | 107 | 100 | 88 | 97 | CU (114, 0.33, 0.01) | +1.0 | 0.01 | 1 | 138 | Y | 108 | +0.9 | +0.01 | +0.1 |
| 5 | Pete Fairbanks | TBR | 31 | RP | 60 | 56° | 0.89 | hybrid | 115 | 100 | 99 | 109 | KC (123, 0.20, 0.01) | +1.0 | 0.01 | 2 | 90 |  | 116 | +0.8 | +0.02 | +0.2 |
| 6 | Lyon Richardson | CIN | 25 | RP | 37 | 30° | 0.93 | lean_supinator | 93 | 97 | 95 | 88 | SL (112, 0.90, 0.35) | +2.7 | 0.98 | 2 | 466 | Y | 95 | +2.3 | +0.04 | +0.3 |
| 7 | Brad Lord | WSN | 25 | RP | 130 | 21° | 0.98 | pronator | 91 | 100 | 102 | 92 | CU (111, 0.23, 0.01) | +2.8 | 0.02 | 1 | 137 | Y | 94 | +2.4 | +0.08 | +0.6 |
| 8 | PJ Poulin | WSN | 28 | RP | 24 | 17° | 0.97 | pronator | 96 | 98 | 91 | 87 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 29 | Y | 96 | +0.0 | +0.00 | +0.0 |
| 9 | Yennier Cano | BAL | 31 | RP | 58 | 17° | 0.87 | supinator | 101 | 100 | 96 | 97 | CU (118, 0.20, 0.02) | +2.5 | 0.04 | 1 | 22 |  | 103 | +2.1 | +0.05 | +0.4 |
| 10 | Tanner Gordon | COL | 27 | SP | 75 | 43° | 0.99 | pronator | 89 | 99 | 104 | 91 | CU (96, 0.33, 0.02) | +1.1 | 0.04 | 3 | 352 | Y | 90 | +0.9 | +0.04 | +0.3 |
| 11 | Emerson Hancock | SEA | 26 | SP | 90 | 16° | 0.90 | hybrid | 90 | 99 | 100 | 88 | CU (116, 0.20, 0.01) | +3.6 | 0.03 | 1 | 75 |  | 94 | +3.1 | +0.15 | +1.2 |
| 12 | Lou Trivino III | - - - | 33 | RP | 47 | 36° | 0.94 | lean_supinator | 95 | 99 | 96 | 92 | CU (105, 0.40, 0.01) | +1.3 | 0.01 | 1 | 669 | Y | 97 | +1.1 | +0.02 | +0.2 |
| 13 | Chase Dollander | COL | 23 | SP | 98 | 25° | 0.94 | lean_pronator | 97 | 100 | 98 | 95 | SL (113, 0.93, 0.42) | +2.2 | 0.90 | 1 | 271 | Y | 100 | +1.8 | +0.10 | +0.8 |
| 14 | Aaron Nola | PHI | 32 | SP | 94 | 20° | 0.95 | pronator | 102 | 100 | 108 | 109 | SL (103, 0.75, 0.08) | +0.2 | 0.02 | 1 | 128 | Y | 102 | +0.2 | +0.01 | +0.1 |
| 15 | Angel Chivilli | COL | 22 | RP | 58 | 34° | 0.99 | pronator | 94 | 98 | 101 | 98 | CU (112, 0.25, 0.01) | +2.5 | 0.09 | 2 | 370 | Y | 97 | +2.1 | +0.05 | +0.4 |
| 16 | Anthony Molina | COL | 23 | RP | 34 | 50° | 0.99 | pronator | 94 | 97 | 111 | 104 | FC (100, 0.20, 0.34) | +0.9 | 0.31 | 2 | 459 | Y | 94 | +0.8 | +0.01 | +0.1 |
| 17 | Jorge López | WSN | 32 | RP | 24 | 39° | 0.96 | pronator | 98 | 99 | 96 | 91 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 747 | Y | 98 | +0.0 | +0.00 | +0.0 |
| 18 | Gavin Williams | CLE | 25 | SP | 167 | 34° | 0.96 | pronator | 101 | 100 | 98 | 99 | FS (112, 0.25, 0.01) | +1.5 | 0.01 | 2 | 586 | Y | 102 | +1.3 | +0.12 | +0.9 |
| 19 | Jack Perkins | ATH | 25 | RP | 38 | 31° | 0.96 | pronator | 100 | 101 | 96 | 96 | SI (103, 0.50, 0.42) | +0.4 | 0.17 | 1 | 444 | Y | 101 | +0.3 | +0.01 | +0.0 |
| 20 | JP Sears | - - - | 29 | SP | 135 | 30° | 0.98 | pronator | 98 | 97 | 105 | 102 | CU (105, 0.25, 0.02) | +1.0 | 0.02 | 1 | 85 | Y | 99 | +0.8 | +0.06 | +0.5 |
| 21 | Luis Peralta | COL | 24 | RP | 19 | 28° | 0.98 | pronator | 98 | 98 | 92 | 86 | SL (113, 0.72, 0.11) | +2.1 | 0.28 | 2 | 77 | Y | 100 | +1.8 | +0.03 | +0.2 |
| 22 | Thomas Hatch | - - - | 30 | RP | 34 | 40° | 0.81 | supinator | 90 | 101 | 96 | 91 | CU (106, 0.35, 0.01) | +2.2 | 0.03 | 1 | 492 |  | 92 | +1.8 | +0.03 | +0.2 |
| 23 | Jesús Luzardo | PHI | 27 | SP | 183 | 34° | 0.95 | pronator | 106 | 101 | 109 | 113 | CU (111, 0.23, 0.01) | +0.7 | 0.01 | 1 | 177 | Y | 107 | +0.6 | +0.06 | +0.5 |
| 24 | Tayler Scott | - - - | 33 | RP | 27 | 15° | 0.96 | pronator | 91 | 97 | 103 | 94 | CU (114, 0.28, 0.00) | +3.2 | 0.01 | 1 | 65 |  | 94 | +2.7 | +0.05 | +0.4 |
| 25 | Andrew Heaney | - - - | 34 | SP | 122 | 26° | 0.99 | pronator | 90 | 100 | 104 | 93 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 90 | Y | 90 | +0.0 | +0.00 | +0.0 |
| 26 | Bubba Chandler | PIT | 22 | SP | 31 | 44° | 0.95 | lean_pronator | 105 | 103 | 103 | 111 | SI (116, 0.38, 0.07) | +1.5 | 0.11 | 1 | 601 |  | 107 | +1.3 | +0.04 | +0.3 |
| 27 | Orlando Ribalta | WSN | 27 | RP | 24 | 39° | 0.87 | supinator | 102 | 101 | 94 | 97 | CU (116, 0.42, 0.02) | +1.9 | 0.04 | 2 | 626 |  | 104 | +1.6 | +0.03 | +0.2 |
| 28 | Trevor Williams | WSN | 33 | SP | 82 | 17° | 0.62 | supinator | 90 | 100 | 103 | 94 | CU (111, 0.35, 0.02) | +2.9 | 0.06 | 2 | 71 |  | 93 | +2.4 | +0.11 | +0.9 |
| 29 | Zack Kelly | BOS | 30 | RP | 35 | 38° | 0.94 | lean_supinator | 109 | 100 | 101 | 106 | — (nan, nan, nan) | +0.0 | 0.00 | 1 | 556 | Y | 109 | +0.0 | +0.00 | +0.0 |
| 30 | Wandy Peralta | SDP | 33 | RP | 71 | 48° | 0.95 | pronator | 99 | 100 | 102 | 102 | CU (111, 0.30, 0.01) | +1.7 | 0.02 | 1 | 243 | Y | 100 | +1.5 | +0.04 | +0.3 |
| 31 | Antonio Senzatela | COL | 30 | SP | 130 | 42° | 0.84 | supinator | 85 | 98 | 106 | 93 | FC (101, 0.28, 0.23) | +2.2 | 0.51 | 1 | 373 |  | 88 | +1.9 | +0.13 | +1.1 |
| 32 | Zach Agnos | COL | 24 | RP | 31 | 39° | 0.97 | pronator | 89 | 99 | 96 | 90 | CU (97, 0.30, 0.01) | +1.2 | 0.06 | 2 | 773 | Y | 90 | +1.0 | +0.02 | +0.1 |
| 33 | Nick Pivetta | SDP | 32 | SP | 181 | 57° | 0.95 | pronator | 102 | 102 | 102 | 103 | CH (114, 0.45, 0.02) | +1.7 | 0.04 | 1 | 105 |  | 103 | +1.4 | +0.14 | +1.1 |
| 34 | Lucas Erceg | KCR | 30 | RP | 61 | 42° | 0.98 | pronator | 99 | 101 | 106 | 105 | CU (102, 0.25, 0.02) | +0.5 | 0.01 | 1 | 732 | Y | 99 | +0.4 | +0.01 | +0.1 |
| 35 | Jacob Lopez | ATH | 27 | SP | 92 | 23° | 0.94 | lean_supinator | 98 | 99 | 101 | 100 | — (nan, nan, nan) | +0.0 | 0.00 | 0 | 79 | Y | 98 | +0.0 | +0.00 | +0.0 |
| 36 | Brandon Waddell | NYM | 31 | RP | 31 | 44° | 0.75 | supinator | 96 | 100 | 103 | 101 | CU (108, 0.40, 0.04) | +1.6 | 0.06 | 1 | 195 |  | 98 | +1.4 | +0.02 | +0.2 |
| 37 | Cole Sands | MIN | 27 | RP | 72 | 24° | 0.86 | supinator | 96 | 100 | 105 | 100 | SL (114, 0.75, 0.11) | +2.5 | 0.28 | 1 | 237 |  | 99 | +2.2 | +0.06 | +0.5 |
| 38 | Yerry De los Santos | NYY | 27 | RP | 35 | 28° | 0.99 | pronator | 97 | 99 | 99 | 96 | CU (109, 0.30, 0.01) | +1.7 | 0.03 | 2 | 293 | Y | 99 | +1.4 | +0.02 | +0.2 |
| 39 | Sawyer Gipson-Long | DET | 27 | RP | 31 | 29° | 0.88 | supinator | 95 | 100 | 105 | 99 | CU (101, 0.47, 0.03) | +0.9 | 0.03 | 1 | 431 |  | 96 | +0.8 | +0.01 | +0.1 |
| 40 | Spencer Bivens | SFG | 31 | RP | 81 | 35° | 0.89 | supinator | 97 | 99 | 103 | 99 | CU (104, 0.23, 0.01) | +0.9 | 0.01 | 1 | 260 |  | 98 | +0.8 | +0.03 | +0.2 |

## Top 25 by raw possible gain (best single add, regardless of P(add))

| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Emerson Hancock | SEA | SP | 16° | hybrid | 90 | CU | 116 | 0.20 | 0.01 | +3.6 | 94 | +0.15 |
| 2 | José Ureña | - - - | RP | 28° | pronator | 87 | CU | 113 | 0.20 | 0.01 | +3.5 | 91 | +0.07 |
| 3 | Tayler Scott | - - - | RP | 15° | pronator | 91 | CU | 114 | 0.28 | 0.00 | +3.2 | 94 | +0.05 |
| 4 | Germán Márquez | COL | SP | 40° | pronator | 86 | FS | 108 | 0.20 | 0.01 | +3.2 | 89 | +0.19 |
| 5 | Alexis Díaz | - - - | RP | 16° | hybrid | 94 | CU | 114 | 0.30 | 0.01 | +2.9 | 97 | +0.04 |
| 6 | Trevor Williams | WSN | SP | 17° | supinator | 90 | CU | 111 | 0.35 | 0.02 | +2.9 | 93 | +0.11 |
| 7 | Brad Lord | WSN | RP | 21° | pronator | 91 | CU | 111 | 0.23 | 0.01 | +2.8 | 94 | +0.08 |
| 8 | Lyon Richardson | CIN | RP | 30° | lean_supinator | 93 | SL | 112 | 0.90 | 0.35 | +2.7 | 95 | +0.04 |
| 9 | Andrew Saalfrank | ARI | RP | 47° | supinator | 87 | SL | 106 | 0.85 | 0.10 | +2.6 | 90 | +0.04 |
| 10 | Tanner Houck | BOS | SP | 21° | supinator | 96 | CU | 114 | 0.30 | 0.01 | +2.6 | 98 | +0.07 |
| 11 | Cole Sands | MIN | RP | 24° | supinator | 96 | SL | 114 | 0.75 | 0.11 | +2.5 | 99 | +0.06 |
| 12 | Dane Dunning | - - - | RP | 38° | unknown | 81 | CU | 100 | 0.23 | 0.01 | +2.5 | 84 | +0.04 |
| 13 | Michael Tonkin | MIN | RP | 14° | lean_supinator | 93 | CU | 111 | 0.33 | 0.01 | +2.5 | 96 | +0.04 |
| 14 | Konnor Pilkington | WSN | RP | 30° | pronator | 97 | CU | 115 | 0.23 | 0.01 | +2.5 | 100 | +0.03 |
| 15 | Yennier Cano | BAL | RP | 17° | supinator | 101 | CU | 118 | 0.20 | 0.02 | +2.5 | 103 | +0.05 |
| 16 | Angel Chivilli | COL | RP | 34° | pronator | 94 | CU | 112 | 0.25 | 0.01 | +2.5 | 97 | +0.05 |
| 17 | Brady Singer | CIN | SP | 24° | supinator | 95 | CU | 113 | 0.35 | 0.01 | +2.5 | 98 | +0.19 |
| 18 | Martín Pérez | CHW | SP | 47° | pronator | 86 | SL | 103 | 0.55 | 0.01 | +2.4 | 88 | +0.07 |
| 19 | Félix Bautista | BAL | RP | 69° | unknown | 100 | KC | 117 | 0.23 | 0.00 | +2.4 | 102 | +0.03 |
| 20 | Jalen Beeks | ARI | RP | 49° | hybrid | 92 | SL | 109 | 0.75 | 0.15 | +2.4 | 94 | +0.05 |
| 21 | Victor Mederos | LAA | SP | 23° | unknown | 98 | CU | 115 | 0.20 | 0.01 | +2.4 | 100 | +0.07 |
| 22 | Antonio Senzatela | COL | SP | 42° | supinator | 85 | FC | 101 | 0.28 | 0.23 | +2.2 | 88 | +0.13 |
| 23 | Luke Weaver | NYY | RP | 48° | pronator | 97 | SL | 113 | 0.90 | 0.13 | +2.2 | 99 | +0.05 |
| 24 | Nic Enright | CLE | RP | 55° | pronator | 93 | CH | 109 | 0.28 | 0.02 | +2.2 | 95 | +0.03 |
| 25 | Thomas Hatch | - - - | RP | 40° | supinator | 90 | CU | 106 | 0.35 | 0.01 | +2.2 | 92 | +0.03 |

## Named checks

- **Carson Palmquist** (COL, SP): slot 16°, eff4 0.93, lean_supinator; Stuff+ 93 (own 97), Loc+ 91; reachable 0, best add — (prec Stf+ nan, share nan, P nan), gain +0.0, ΣEV 0.00, pool n=33, drop-recipe Y → proj Stf+ 93, ΔWAR +0.00
- **Emerson Hancock** (SEA, SP): slot 16°, eff4 0.90, hybrid; Stuff+ 90 (own 99), Loc+ 100; reachable 1, best add CU (prec Stf+ 116, share 0.20, P 0.01), gain +3.6, ΣEV 0.03, pool n=75, drop-recipe N → proj Stf+ 94, ΔWAR +0.15