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
