# baseball-slot-sim

Slot-conditional arsenal simulator for MLB FA/trade targeting. Design doc (source of truth):
`~/mirror/baseball-slot-sim-design.md`.

## Data
- `data/raw/plb.twbx` — Alex Chamberlain's Pitch Leaderboard v8 (Tableau Public, `chamb117`), downloaded
  2026-08-18. Hyper extract = raw Statcast pitch-level 2024-03-28 → 2026-08-16 (~2.0M pitches, arm_angle,
  trajectory columns). His VAA/HAA/AA/dead-zone formulas are recovered from the .twb and reproduced in
  `src/build_pitch_features.py`.
- `data/raw/statcast_YYYY_MM.parquet` — pybaseball backfill 2020–2023 (`src/backfill_statcast.py`).
- `data/derived/fg_stuff.csv` — FanGraphs Stuff+/Location+/Pitching+ overall + per pitch, 2020–2026
  (`src/pull_fangraphs.py`, keyed by xMLBAMID = Statcast pitcher).

## Pipeline (python3.11)
1. `src/build_pitch_features.py` → `data/derived/pitches.parquet` (VAA, HAA, VRA, HRA, VAA_AA_*, HAA_AA_*,
   AzOE, AxOE, PythagOE, IVB/HB) and `pitcher_season_pitch.parquet/csv` (Statcast typing).
2. `src/pull_fangraphs.py` → `fg_stuff.csv`.
3. `src/build_emulator_table.py` → `emulator_table.parquet` (FG typing: ST/SV→SL, CS→CU; joins Stf+/Loc+/Pit+
   per pitch; adds bauer, move_axis, axis_minus_slot, primary-FB differentials). 99% join.
4. `src/fit_emulator.py [min_n]` — season-level Stuff+ emulator; `src/fit_emulator_pitchlevel.py` — pitch-level.
   Both evaluated per the identity-leakage protocol (in-sample vs grouped-K-fold-by-pitcher vs temporal).

## Results so far (2026-08-18, full 2020–26 span; 4.58M pitches, 15.4k pitcher-season-pitch rows w/ FG target)
- Stuff+ emulator (n≥50): in-sample R² .80 → grouped-OOS-by-pitcher .648 (gap .15; leakage claim reproduced —
  on 2024–26 only the gap was .21). Forward: train ≤2023 → 2024-25 .668; → 2026 .657; unseen-2026 pitchers .56.
  Ablating x0/z0/dead-zone: no change; extension is real signal (−.02 when dropped).
- Within-pitcher Δ (OOS pred on new shape − old shape vs realized ΔStf+, n≥100 both seasons):
  all r=.53 slope .97 (n=6680) | ≥5° slot changers r=.59 slope 1.03 (n=864; steeper .61, flatter .57) | FF .65.
- Corpora: 349 slot-changers ≥5° (131 steeper / 218 flatter; mean ΔStuff+ ≈ 0 both ways → base rate is zero,
  the model's job is separating who pays); 393 pitch additions (<2%→≥8%; 112 SI, 105 FC, 56 SL…; 21 abandoned).
- Precedent (kNN, same hand, own pitcher excluded, functional roles): which-pitch top-1 .52 vs slot-bucket base
  .49 (top-2 .73 vs .78 — needs a real classifier); added-pitch quality r(precedent Stf+, realized)=.53.
  Yesavage 2026: precedent pool n=16, optionality 1.1, only lever a 12-6 curve (comps 111 vs his 108) → the
  "no stuff lever, north-south only" check passes from the data. Palmquist 2026: optionality 0 (now optimal).
- Scripts: build_corpora.py, precedent.py, test_delta.py.

## Update (2026-08-18, later): sup/pro classifier, addition classifier, own run-value Stuff model
- `docs/RESEARCH-supination-pronation.md` — sourced operational definitions (Rosen/FanGraphs: 4S spin-based active spin ≥95% pronator,
  <90% supinator; Pitcher List hybrid 80–89% w/ high raw spin; Tread sweeper tell; SSW deviation; slot-relative axis residual).
- `src/pull_savant_spin.py` → `savant_spin.csv` (Savant spin-direction leaderboard: active spin, measured vs inferred axis, deviation;
  20.5k pitcher-season-pitch rows 2020–26). `src/suppro.py` → `suppro.parquet`: eff4 Y2Y r² .86; class persistence 72%;
  Hancock 96%/27° pronator → 82%/11° supinator reproduces the published story; Yesavage pronator; Palmquist lean supinator.
- `src/fit_addition_classifier.py`: which family gets added, grouped 10-fold, OOF base rate — model top-1 .59 / top-2 .82 vs
  base .56 / .78, log-loss 1.14 vs 1.25 (n=394). Supinator-leaning add FC/SL, pronator-leaning add SI/FS/CH.
- `src/fit_stuff_rv.py`: OWN Stuff model — XGBoost, pitch-level, target = platoon/season-adjusted run value, all pitches pooled,
  no pitch-type label, physical features only. A = FG-like features; B = A + arm angle, HAVAA, VRA/HRA, AzOE/AxOE, measured
  axis, active spin, SSW deviation. Indexed 100/10 per season. TRUE-FORWARD test (train ≤2023, predict next-season RV/100 for
  2024–25 pitcher-seasons, n=753): FG Stuff+ .371 | A .302 | B .363 | FG Pitching+ .398. Physics features ≈ +.06 forward r;
  first pass at parity with FG. B–FG corr .60; Y2Y .75 (FG .78).

## Update (2026-08-18, night): slot lever — negative results recorded
- `src/fit_transfer.py` (transfer_fits.csv): on 3,139 |Δslot|≥3° pitcher-family pairs, grouped-OOS — release height 0.04 ft/°
  (r² .62–.75); measured spin axis rotates ~0.9°/° on FF/SI/CH (r² .53–.70), not on SL/FC; IVB FF +0.18"/°, SI +0.27"/°,
  CH +0.20"/° (r² .30/.53/.26); HB FF −0.10"/° (r² .35); breaking-ball HB, velo, active spin: no slot dependence (r² ≈ 0).
- `src/simulate_slot.py`: rotate a pitcher's own pitches by the slopes and rescore with the own RV model → mean best-case gain
  0.5, and r ≈ 0 vs realized ΔStuff on the 349 changers. `src/test_shape_prediction.py`: slopes/precedent cut fastball IVB
  error to ~0.8–1.0" but nothing beats "no change" on breaking balls; Palmquist's 2026 sinker (4.7" IVB) was a NEW pitch,
  not a transformed one — precedent at 16° for LHP/eff .91 predicts 4.7"/18.1"/Stf+ 98 vs his 4.7"/16.5"/97.
- `src/precedent_at_slot.py`: precedent-arsenal-at-slot lever → r = −.07 vs realized ΔStuff+ on changers; the "unrealized
  pitch" distance (flags Palmquist 2025 SI at 11") has r = .01 with next-season ΔStuff+ over 2,155 pitcher-seasons.
- Verdict: slot changes average ~0 either direction and neither rotation nor precedent-at-slot identifies winners ex ante.
  What is predictable is downstream of the shape (Δ r ≈ .6 given the realized arsenal). The slot lever is therefore a
  repertoire question (addition classifier + precedent quality), not a geometry question.

## Update (2026-08-18, night): Location+ cost, Pitching+ mapping, value map (`src/fit_value_map.py`, `src/pull_fangraphs_std.py`)
- ΔLoc+ next season: all pairs −0.3 | slot changers ≥5° +0.6 (≥8° +1.8; flatter +0.9, steeper +0.1) | adders 0.0. Regression on
  changers: ΔLoc+ = −0.31 + 0.00·|Δslot| − 0.50·(Loc+−100) → no command cost from slot change, only mean reversion (survivorship caveat).
- Pitching+ ≈ −74.8 + 0.850·Stuff+ + 0.897·Location+, R² .945 (n=3749).
- Next-season (IP≥40, n=1783, IP-weighted r): ERA — Stuff+ −.39, Pit+ −.36, SIERA +.34, ERA +.19; xERA — Stuff+ −.53, Pit+ −.47;
  WAR/180 — Pit+ +.41, Stuff+ +.38. Location+ alone ≈ 0 forward. → the projection is a Stuff projection; Loc+ is second-order.
- Value: SP next WAR/180 = −7.46 + 0.098·Pit+ (1 Pit+ ≈ .098 WAR/180); RP = −5.79 + 0.074·Pit+.

## Update (2026-08-18, late): research corroboration + the one slot screen with support
- `docs/RESEARCH-arm-angle-and-stuff-models.md`: independent Savant-leaderboard fits match our transfer slopes (SI +2.8"/10°,
  axis 0.9°/°, no velo/BB% cost); FG Stuff+ construction (axis differential yes; VAA/arm angle no; per-type not re-centered;
  reportedly rewritten as classification by 2025; predictiveness decaying since 2024); Tango's Stuff+→next-ERA r=.37 = our .371.
- Driveline 2026 recipe replicated: ≥3° droppers with below-avg FF IVB and eff4≥.93 → ΔStuff+ +1.4 (n=54) vs −0.7…−1.0 elsewhere;
  same profile without dropping −1.2; raisers no structure. Borderline p, independent corroboration → keep as a drop-direction
  feasibility screen, not a projected gain.

## Update (2026-08-18, late): target cards (`src/build_targets.py` → `docs/targets_2026.md`, `data/derived/target_cards.parquet`)
- Repertoire lever per pitcher-season: reachable families (precedent share ≥.20 in the same-hand, sup/pro-compatible neighborhood),
  gain = 0.14 × (precedent Stf+ − Stuff+)+, P(add) from a binary LightGBM over all pitcher-season × unthrown-family rows
  (grouped-OOF AUC .785, calibrated by decile), EV = P × gain. Slot = feasibility flag only (Driveline drop recipe, pool count).
- Valuation: Pit+ = −74.8 + .85·Stf+ + .90·Loc+; ΔPit+ = .85·gain; ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP; $8M/WAR.
- Backtest (n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after mean reversion → cards are reachability +
  conditional value, not forecasts. Yesavage: +0.5 max, P .02 → no lever. Palmquist/Hancock: nothing reachable → optimized.

## Update (2026-08-18, late): prospective test + HTML board
- `ASOF=2025 python3.11 src/precedent.py 40 && ASOF=2025 python3.11 src/build_targets.py` rebuilds the cards strictly as of end-2025
  (precedent pools and P(add) labels ≤2025). Result: EV top-40 gained +2.7 Stuff+ in 2026 vs −0.1 for stuff-matched controls
  (n=19); raw-gain top-40 +2.2. Hancock #1 by raw gain (mechanism wrong: card said curve; he dropped 8° + added sweeper/cutter);
  Palmquist not findable (rank 309, no reachable add — his gain was a running-FF→real-SI conversion, which the lever doesn't model);
  Dollander #2, Senzatela #7, Sasaki #36 on the list. `docs/targets_2025.md`.
- `src/render_targets_html.py` → `docs/targets_2026.html`: sortable/filterable board with per-row family detail.

## Update (2026-08-18, late): levers that find Palmquist (`src/levers_v2.py`, folded into `build_targets.py`)
- Decomposition of Palmquist's +14: mostly USAGE reallocation (threw his 86 four-seam 42%; his 2025 grades at his 2026 mix ≈ 101)
  plus existing-pitch quality gap vs comps (FF 86 vs comps 101; FC 75 vs 93) plus Coors.
- New levers: (A) mix optimization (≤20 pts of usage toward better pitches; FB ≥30%, cap 45%); (B) existing-pitch gap =
  usage × (comps' Stf+ on same family − own)⁺ over pitches thrown ≥8%; (C) Coors = own-model road-minus-all for ≥25%-at-COL
  seasons (own model: home 96.2 vs road 98.3, ~2 pts suppressed).
- Regression of next-season ΔStuff+ on level + levers (2020–25, n≈2270): existing-pitch gap .31 (t=5.9), addition EV 1.9 (p=.10),
  mix .06 (p=.2), Coors .14 (n.s.). Combined "opportunity" score = weighted sum; r=.31 raw / .10 after mean reversion.
- As-of-2025 (strict): opportunity top-40 gained +3.1 in 2026 vs −0.2 stuff-matched (excess +3.25, n=20; top-80 +1.4).
  Palmquist #29, Dollander #18, Senzatela #20, Hancock #105. Caveat: survivorship among ranked relievers without 2026 samples.
- Additions are now ROLE-level (CU/KC one role, CH/FS one role): no "add a curve when he throws a knuckle-curve" rows.
- Board: `docs/targets_2026.html` (default sort = opportunity; row detail shows all four levers).

## Update (2026-08-18, evening): what "pitch gap" is, and the ACTIONABLE score
- `src/test_gap_decomp.py`: the existing-pitch gap predicts next-season Δ identically whether the pitch is shaped like comps' or not
  (.22 vs .25), and its velo and shape halves predict identically (.233/.234) → it is shrinkage toward a hardware prior
  (per-pitch next Stf+ ≈ .7·own + .25·comps, t=15), not a fixable-shape signal. Persistent (last-year) gap .16/pt, transient .26/pt;
  pitches with gap≥8 two years running still average +2.3 (31% improve ≥5). Dobnak (91.7→88.4→81.4 vs comps ~100) is the
  individual counterexample. Relabeled REGRESS-TO-COMPS; kept in Drift (valuation), excluded from Actionable.
- ACTIONABLE = mix gain (≤20 pts usage toward better pitches; FB≥30%, cap 45%) + best reachable role-unoccupied add at comps'
  Stf+ × 0.14 (no P(add) discount) + drop-recipe bonus 1.4 (floor lowered to 15°). Beck Way #7 (mix +8.5: 128 slider at 15%,
  84 FF at 14%; curve 103 reachable; drop-recipe) → proj 109. As-of-2025 actionable top-40 gained +1.8 in 2026 vs −0.6 matched
  (excess +2.4, n=27; top-80 +2.8). Hancock #38, Palmquist #56 as of 2025.
- Board: default sort Actionable; Drift and Regress shown alongside.

## Update (2026-08-18, evening): cluster-based pitch identity + mix on the Stf+/Pit+ blend
- `levers_v2.py` merges labels that are one physical pitch (CU/KC, CH/FS, FF/SI, FC/SL within 2.5 mph & 4.5") before mix; mix is
  optimized on a 50/50 blend of per-pitch Stuff+ and Pitching+ (owner asked for Pit+; pure Pit+ was noisiest prospectively).
  Prospective (as-of-2025 top-40 excess ΔStuff+/ΔPit+): Stf-mix +2.6/+1.5, Pit-mix +1.1/+2.5 (top-80 ≈0), blend +2.5/+2.5 → blend.
- 2026: Beck Way #1, Iglesias #26 (changeup no longer "cut"), Glasnow #243 (CU+KC merged). As of 2025: Palmquist #93 actionable /
  #25 drift (his gain was pitch quality → drift list), Hancock #51.

## Update (2026-08-18, night): The Carson Palmquist Model (`docs/CARSON-PALMQUIST-MODEL.md`)
- Gate = plus pitch (Stf+≥105) inside an ordinary arsenal (Stuff+ 88–104). Engine A (development): GBM on next-season ΔStuff+
  from structural features; strict 2025→26 test top-10 +3.9 (gated; Palmquist #3, Dollander #2), +7.9 ungated (Palmquist #7).
  Engine B (reconfiguration) = Actionable. Combined z-sum: Palmquist #7 of 165 going into 2026; Way #13 of 176 in 2026.
- ΔPit+ target rejected (Loc+ mean reversion dominates; Bummer #1). Scripts: palmquist_model.py, palmquist_model_variants.py.

## Update (2026-08-18, night): sample-size shrinkage of per-pitch grades
- Poulin (#3 as of 2025) was driven by a 38-pitch sinker graded 106 (→93 in 2026). Now grade* = (n·own + 80·comps)/(n+80)
  before mix, plus-pitch, regress (levers_v2.py, palmquist_model.py). CPM top-10 excess +2.9/+1.9; Palmquist #11 (dev alone #4);
  Way #29. Board v9.

## Update (2026-08-18, night): sup/pro classifier fix (Mason Black)
- Bug: arsenal/SSW "points" could outvote 4S efficiency (Black: eff .99 → lean supinator). Now efficiency is primary (≥.95 pronator,
  <.90 supinator); secondary evidence only breaks ties in .90–.95; hybrid = .80–.90 + high raw spin + no strong supinator evidence.
  Black → pronator; Hancock 2023–26: pronator → pronator → hybrid → supinator (matches Rosen). Class counts: 1179 P / 1570 S / 310 H.
- Chain rerun (precedent neighborhoods use class). CPM as-of-2025 top-10 excess +3.9 Stuff+ / +4.9 Pit+; top-40 +2.8/+2.7.
  Going into 2026: Hancock #1, Dollander #4, Palmquist #12. 2026: Mason Black #4, Way #38.

## Update (2026-08-18, night): rolling backtest + calibration of Dev ΔStf+ (`src/backtest_dev.py`)
- Rolling origins 2021→22 … 2025→26 (train strictly on earlier seasons): r = .22/.27/.44/.29/.27 (pooled .30); ungated top-25 excess
  vs stuff-matched +0.2/+1.6/+5.7/+2.3/+4.5 (positive 5/5, mean +2.9); gated top-10 +0.2/+2.9/+7.5/−1.2/+6.1.
- Calibration by predicted bucket: −5→−3.7, −1→−1.4, +1→+0.6, +3→+1.5, +4–6→+4.8 (44% chance of ≥5 gain), >+6 (n=10)→~0.
  realized ≈ −0.3 + 0.69×pred; sd ≈ 6 in every bucket; max prediction ever +8.3. Board now shows calibrated Dev and P(≥5).
- "Regress" relabeled "Gap vs comps → expected" (expected ≈ 0.2×gap; Blewett's 11.6 gap ≈ +2–3 expected, and he is out of the gate).

## Update (2026-08-18, night): Own ablation, Actionable scaling, archetype toggle
- Own−FG in the dev engine: rolling r .318 vs .305 without, top-25 excess +3.5 vs +3.3 → keep (board shows Own−FG, not raw Own).
- Actionable was accounting, not fitted. Conditional tests: MIX — pitchers who raised best-pitch usage ≥10 pts (n=267) gained +1.5 vs
  −1.2 for non-movers (mean effect ≈ predicted +2.7) but dose-response weak (r .09, slope .28) → ×0.5. ADD — among 360 adders,
  realized vs usage×(pStf−stuff): r .33, slope 1.2 → ×1.0. DROP +1.4 replicated. Actionable = 0.5·mix + add + drop.
- Board: 'Gate' column replaced by a default-on toggle "Palmquist archetype only — a plus pitch (Stf+ ≥105) inside an ordinary arsenal
  (Stuff+ 88–104)". CPM as-of-2025 top-10 +2.4/+3.8, top-25 +2.3/+1.9; Hancock #1, Dollander #2, Palmquist #11; 2026 Black #4, Way #33.

## Update (2026-08-18, night): own model dropped from the product; dev prediction for everyone (`src/build_cpm.py`)
- Owner call: the own run-value Stuff model isn't additive to the product → removed from the development engine's features, from the
  board (Own/Own−FG), and the Coors lever (own-model road-minus-all) dropped from Drift. Calibration unchanged: realized ≈ −0.29 +
  0.67×raw, pooled r .29; calibrated +3–5 → +3.3 (39% ≥5, 27% decline).
- Ungated development prediction now computed and shown for ALL pitchers (dev_all_2026/2025.parquet); CPM stays the gated composite.
  As of 2025 (ungated dev): Hancock #6, Sasaki #13, Palmquist #20, Dollander #22 of 521; Harrison #481 (already 104).
  Gated CPM 2025→26: top-10 excess +3.0 Stuff+ / +2.1 Pit+; top-25 +2.8. Hancock #1, Dollander #3, Palmquist #15 of 201 (gate now
  includes 2025 pitchers without a 2026 season). 2026: Mason Black #6, Way #27.
- The own-model scripts remain in the repo as research (fit_stuff_rv.py, stuff_model.py); they are not used downstream.

## Update (2026-08-18, night): CPM for everyone
- CPM = z(dev) + z(actionable) across ALL pitchers (archetype toggle is a filter, not a scoring gate); LightGBM handles missing
  features natively so every pitcher gets a Dev. 2025→26: CPM-all top-10 excess +4.8 Stuff+ / +3.7 Pit+, top-25 +4.4, top-40 +3.0;
  within gate top-10 +2.9. Hancock #6, Dollander #7, Sasaki #14 (out of gate), Palmquist #32 (gate #16) of 574. 2026: Black #9, Way #60.
