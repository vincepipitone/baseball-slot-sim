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
