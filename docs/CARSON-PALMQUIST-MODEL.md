# The Carson Palmquist Model — spec and evidence (2026-08-18)

**Archetype gate (the thesis):** owns a plus pitch (any offering Stf+ ≥ 105) inside an ordinary arsenal (overall Stuff+ 88–104).
Palmquist 2025 (sweeper 107 / Stuff+ 93) and Beck Way 2026 (slider 128 / 99) qualify; Yesavage, Glasnow do not.

**Engine A — development (validated):** LightGBM, target next-season ΔStuff+, features: stuff level, age, FB velo, plus-pitch grade
and usage, plus-pitch under-usage, fastball liability vs hardware comps, regress-to-comps, 4S efficiency, sup/pro class, drop-recipe,
Coors share, own-model−FG, precedent pool, Loc+, mix gain, add gain/EV. Strict test train ≤2024 → 2025→26: gated top-10 excess
+3.9 Stuff+ vs matched (Palmquist #3, Dollander #2 of 165); ungated top-10 +7.9 (Palmquist #7, Sasaki #9, Hancock #13, Dollander #3).

**Engine B — reconfiguration (actionable):** label-merged mix on 50/50 Stf+/Pit+ + class-compatible reachable add at precedent grade
+ drop-recipe. Way #1 overall in 2026. Validated on inputs (P(add) AUC .77 calibrated; precedent grade r≈.5), not on outcomes —
intervention-conditional upside cannot be validated on pitchers nobody intervened on.

**Combined (z_dev + z_act within the gate):** Palmquist #7 of 165 going into 2026; Way #13 of 176 today. Test top-10 +2.2 Stuff+.

Caveats: one out-of-sample season; n=10 at the top; specifications were compared while looking at these names (temporal split is
the guardrail; Engine A's number held across variants); org effect / timing not modeled.

## Going into 2026 (as of end-2025) — combined top 12, with what happened
| rank | PlayerName | Team | Age | role | stuff | sp_pitching | pp_stf | pp_use | fb_liability | gain_gap | mix_pit | drop_recipe | col_share | pred | actionable | cpm | d_stuff | d_pit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Chase Dollander | COL | 23.0 | SP | 97.4 | 95.1 | 114.0 | 0.1 | 5.1 | 4.5 | 3.9 | 1 | 0.5 | 5.2 | 7.3 | 4.4 | 12.4 | 8.1 |
| 2 | Anthony Molina | COL | 23.0 | RP | 93.5 | 104.1 | 122.0 | 0.2 | 7.8 | 7.6 | 5.7 | 1 | 0.7 | 3.2 | 8.1 | 3.8 | 6.7 | 5.1 |
| 3 | PJ Poulin | WSN | 28.0 | RP | 96.0 | 86.5 | 107.0 | 0.2 | 2.5 | 5.0 | 8.3 | 1 | 0.0 | 1.4 | 9.5 | 3.6 | -1.6 | 1.8 |
| 4 | Corbin Martin | BAL | 29.0 | RP | 97.5 | 94.8 | 122.6 | 0.2 | 5.2 | 10.9 | 6.3 | 0 | 0.0 | 4.3 | 6.3 | 3.5 | -4.0 | -9.1 |
| 5 | Valente Bellozo | MIA | 25.0 | RP | 92.7 | 90.0 | 116.7 | 0.1 | 4.2 | 5.6 | 7.5 | 0 | 0.0 | 3.1 | 7.5 | 3.4 | -6.8 | -15.5 |
| 6 | Lucas Erceg | KCR | 30.0 | RP | 98.9 | 105.1 | 109.4 | 0.2 | 0.1 | 5.0 | 4.5 | 1 | 0.0 | 2.5 | 7.7 | 3.2 | -0.2 | -5.9 |
| 7 | Carson Palmquist | COL | 24.0 | SP | 93.2 | 84.6 | 106.7 | 0.3 | 4.3 | 9.2 | 3.7 | 1 | 0.5 | 4.5 | 5.0 | 2.9 | 14.1 | 11.8 |
| 8 | Hayden Wesneski | HOU | 27.0 | SP | 95.9 | 104.6 | 125.4 | 0.2 | 3.4 | 3.6 | 7.9 | 0 | 0.0 | 1.7 | 7.9 | 2.9 | -2.9 | -5.4 |
| 9 | Matthew Liberatore | STL | 25.0 | SP | 95.3 | 96.7 | 121.2 | 0.2 | 5.9 | 10.3 | 5.5 | 0 | 0.0 | 3.9 | 5.5 | 2.9 | 2.5 | -0.7 |
| 10 | Jaden Hill | COL | 25.0 | RP | 95.3 | 94.7 | 112.8 | 0.2 | 6.3 | 6.2 | 2.5 | 1 | 0.6 | 5.5 | 3.8 | 2.9 | 3.3 | -4.2 |
| 11 | Angel Chivilli | COL | 22.0 | RP | 94.4 | 97.6 | 110.3 | 0.2 | 0.8 | 3.8 | 1.8 | 1 | 0.6 | 3.8 | 5.4 | 2.8 | 0.1 | -5.5 |
| 12 | Ryan Yarbrough | NYY | 33.0 | RP | 96.4 | 98.8 | 120.1 | 0.2 | 4.1 | 6.7 | 6.8 | 0 | 0.0 | 1.5 | 7.6 | 2.7 | 3.3 | -1.6 |

Palmquist: rank 7 — dev z +2.26, act z +0.67.

## 2026 — combined top 20
| rank | PlayerName | Team | Age | role | IP | stuff | sp_pitching | pp_stf | pp_use | fb_liability | gain_gap | mix_pit | add_act | drop_recipe | pred | actionable | cpm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Walbert Ureña | LAA | 22.0 | SP | 107.2 | 99.3 | 104.8 | 120.2 | 0.2 | 2.6 | 3.7 | 7.7 | 1.7 | 0 | 3.7 | 9.2 | 4.9 |
| 2 | JP Sears | SDP | 30.0 | SP | 32.2 | 91.3 | 91.6 | 110.7 | 0.3 | 4.4 | 10.0 | 4.7 | 1.8 | 1 | 4.1 | 7.6 | 4.3 |
| 3 | Paul Skenes | PIT | 24.0 | SP | 134.2 | 98.6 | 105.7 | 119.6 | 0.2 | 0.5 | 5.4 | 6.3 | 1.6 | 1 | 2.7 | 9.1 | 4.2 |
| 4 | Elmer Rodríguez | NYY | 22.0 | SP | 17.0 | 93.6 | 75.0 | 110.5 | 0.2 | 8.0 | 8.3 | 6.2 | 0.8 | 0 | 3.0 | 6.9 | 3.4 |
| 5 | Mason Black | KCR | 26.0 | RP | 25.2 | 93.2 | 95.7 | 111.4 | 0.2 | 1.0 | 10.6 | 4.2 | 0.0 | 1 | 4.2 | 5.5 | 3.3 |
| 6 | Brandon Sproat | MIL | 25.0 | SP | 95.2 | 100.3 | 93.2 | 135.0 | 0.1 | 2.0 | 4.2 | 7.6 | 0.0 | 0 | 1.6 | 7.6 | 2.9 |
| 7 | Noah Schultz | CHW | 22.0 | SP | 65.1 | 97.3 | 92.3 | 114.3 | 0.2 | 5.0 | 5.5 | 4.8 | 0.0 | 0 | 4.0 | 4.8 | 2.9 |
| 8 | Luis Morales | ATH | 23.0 | RP | 16.0 | 98.3 | 85.4 | 117.2 | 0.3 | 8.5 | 6.4 | 4.9 | 0.2 | 0 | 3.8 | 5.0 | 2.9 |
| 9 | Joel Kuhnel | - - - | 31.0 | RP | 35.1 | 96.9 | 94.2 | 139.3 | 0.1 | 0.0 | 0.0 | 8.1 | 0.0 | 0 | 1.1 | 8.1 | 2.8 |
| 10 | JT Brubaker | SFG | 32.0 | RP | 57.2 | 90.0 | 97.8 | 105.6 | 0.1 | 6.4 | 10.2 | 5.1 | 1.5 | 0 | 2.3 | 6.4 | 2.7 |
| 11 | Trey Gibson | BAL | 24.0 | SP | 33.0 | 96.9 | 93.3 | 109.5 | 0.2 | 0.0 | 3.9 | 5.2 | 0.0 | 1 | 1.9 | 6.5 | 2.5 |
| 12 | Bubba Chandler | PIT | 23.0 | SP | 121.1 | 102.7 | 106.1 | 116.1 | 0.0 | 3.1 | 4.8 | 4.7 | 0.0 | 0 | 3.4 | 4.7 | 2.5 |
| 13 | Beck Way | KCR | 26.0 | RP | 23.1 | 98.9 | 90.6 | 128.0 | 0.1 | 1.6 | 1.6 | 7.9 | 0.5 | 1 | -0.9 | 9.6 | 2.5 |
| 14 | Jared Jones | PIT | 24.0 | SP | 64.0 | 100.7 | 110.1 | 113.8 | 0.1 | 6.1 | 6.6 | 2.5 | 2.1 | 0 | 3.4 | 4.4 | 2.4 |
| 15 | Landen Roupp | SFG | 27.0 | SP | 129.1 | 98.6 | 104.5 | 117.2 | 0.3 | 3.4 | 3.1 | 5.9 | 1.2 | 0 | 1.1 | 7.0 | 2.3 |
| 16 | Yusei Kikuchi | LAA | 35.0 | SP | 31.0 | 97.8 | 102.6 | 106.9 | 0.3 | 5.7 | 11.2 | 4.6 | 0.8 | 0 | 2.2 | 5.3 | 2.1 |
| 17 | Michael Wacha | KCR | 34.0 | SP | 155.2 | 97.7 | 99.0 | 129.9 | 0.2 | 0.0 | 5.1 | 8.3 | 0.0 | 0 | -0.5 | 8.3 | 2.0 |
| 18 | Chris Bassitt | BAL | 37.0 | SP | 61.2 | 96.2 | 95.4 | 113.0 | 0.1 | 3.9 | 0.7 | 7.6 | 0.0 | 0 | -0.1 | 7.6 | 1.9 |
| 19 | Chase Petty | CIN | 23.0 | RP | 31.2 | 99.6 | 99.0 | 108.3 | 0.3 | 4.2 | 3.6 | 3.8 | 0.0 | 1 | 2.1 | 5.1 | 1.9 |
| 20 | Jake Bennett | BOS | 25.0 | SP | 80.2 | 92.0 | 102.6 | 109.9 | 0.0 | 1.7 | 5.0 | 4.0 | 0.0 | 0 | 2.9 | 4.0 | 1.9 |

Way: rank 13 — dev z -0.39, act z +2.84.

Columns: pp_stf/pp_use = plus pitch grade/usage; fb_liability = usage×(comps' FB Stf+ − own)+; gain_gap = regress-to-comps; mix_pit = mix gain
(blend); pred = Engine A predicted ΔStuff+; actionable = Engine B; cpm = z_dev + z_act. Scripts: src/palmquist_model.py, src/palmquist_model_variants.py.
