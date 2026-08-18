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

## Results so far (2026-08-18)
- Emulator (season-level, n≥50): in-sample R² .84 → grouped-OOS .635 (gap +.21, matches @tomdoyo's
  leakage finding); temporal 24-25→26 .68; unseen-pitchers-in-26 .56. Pitch-level: .62 / .72 / .56.
  Ablating x0/z0/extension/dead-zone does NOT shrink the gap here — leakage is pitcher-pitch persistence
  across seasons, not release position per se.
- Within-pitcher Δ (OOS pred on new shape − old shape vs realized ΔStf+): r=.47 all, .55 on ≥5° slot
  changers, .65 on FF (slope 1.1). This is the simulator-relevant number.
- Corpora in 2024–26: 86 slot-changers ≥5° (36 steeper / 50 flatter); ~141 pitch additions (<2%→≥8%).
