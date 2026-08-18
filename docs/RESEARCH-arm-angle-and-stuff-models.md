# Arm angle → shape transfer, and Stuff+ model construction — research note (2026-08-18)

## Arm angle facts (documented)
- Statcast arm angle = angle from horizontal of shoulder→ball-at-release (Hawk-Eye pose); 0 sidearm, 90 over the top; 2020+.
  Petriello (mlb.com 2024-09-25): ~75% of pitchers stay within 3° y/y; Estrada 65° vs Skenes 24° at the same release height
  because shoulder height differs a foot. Sports Biomechanics 2026 (n=336): Δrelease-z ↔ Δarm-angle r=.74; release-based proxies
  only partially track true angle.
- Geometry (Savant leaderboard, 2024–25): release_z ≈ 4.35 ft (shoulder, uncorrelated with slot) + 2.30 ft × sin(angle);
  ≈ +0.39" per +1°; y/y r=.97, sd of Δ 3.3°, ~50/395 move ≥5°/yr.
- Spin axis follows slot ~0.9° per 1° on FF/SI/CH/CU with a ~15–18° "behind the ball" offset; sliders gyro-dominated, flat.
  Driveline 2019: FF axis ~191° over-the-top vs ~161° sidearm; "lower slot → east-west for virtually every pitch type."
- Within-pitcher (Savant, 2024→25) per +10°: FF IVB +1.0", HB −2.0"; SI IVB +2.8", HB −1.4"; CH IVB +1.4", HB −1.6"; CU HB
  −1.9" glove; ST IVB −1.7"; SL/gyro ≈ 0; velo ≈ 0; release +3.2". Cross-sectional slopes ~1.5× within-pitcher (selection).
  Slot explains ~10–30% of shape change; grip/wrist/efficiency ride along. → matches our transfer_fits.csv.
- Rosen: VRA is the largest single driver of FF carry (even > release height); within-pitcher R² ~.2. Bay dead zone = expected
  FF shape given (arm angle, extension, ax, az). Driveline 2026 (Sawchik): droppers ≥2° since 2016 netted +2.1 runs; elbow
  varus torque +4.2 N·m per +10°; "who benefits" recipe = below-average IVB + efficiency held ~95%. Command: no systematic
  BB% cost (Savant y/y, n=199; corr(|Δ|,ΔBB%) = −.09), anecdotes both ways (Abbott up → BB up; Leiter down → Loc+ 96→108).
- Efficiency is sticky (Rosen r² .65) and does not move with slot cross-sectionally (+0.8pp/10°); Hancock/Boyle-style
  efficiency collapses are individual and mechanics-driven; Mariners 2026 deliberately cut FF efficiency (Gilbert 97→92,
  Muñoz →80) to "improve other shapes."
- Our replication (src, this repo): among ≥3° droppers, low-IVB + eff4≥.93 fastballs ΔStuff+ +1.4 (n=54) vs −0.7…−1.0
  other cells; same profile without a drop −1.2; raisers no structure. Consistent with Driveline; borderline p.

## Case studies (Savant-derived unless [DOC]; 2026 through Aug 18)
| Pitcher | Slot path | FF | Breaking | Other | Command / result |
|---|---|---|---|---|---|
| Hancock | 27.5→18.5→11.4 (23→26) | IVB 13.7→9.1, active spin 96→82 [DOC] | SL→gyro cutter; sweeper 3→25–33% | SI IVB 8.5→0.4 | 2.74 ERA mid-June 26; K/9 +2.3 |
| Boyle | 53.5→29.2 | IVB 16.4→14.8, HB 4.5→8.2, eff 86→67 [DOC] | SL IVB −1.3→2.2 | added SI | — |
| May | 30→21→34 (down then back to natural) | 15.5/9.7→12.9/11.3→15.0/9.9 [DOC] | sweeper 39→20% | — | BB% 9.8→6.6 [DOC], HR/9 1.59→0.62 |
| Weathers | 41.5→32.8 | +1.8" drop, +0.9" run [DOC] | sweeper +4" [DOC] | new SI 8.4/17.7 | K/9 +1 |
| Cavalli | 43.9→36.1 | 15.1/4.4→14.6/6.0 | new ST 86 mph | CH whiff 42→60% | K/9 +2 |
| Burrows | 47.7→39.6 | 16.9/5.7→16.5/8.7 | SL lost depth, CU less drop | — | worst qualified ERA; re-raised mid-June [DOC] |
| Kikuchi | 41.9→36.5→49.4 | HB 7.9→10.5 [DOC] | — | CH fade up | WHIP 1.43 (25) [DOC] |
| Woo | ~25 flat | 5.0 ft release, VAA ~−4°, 91% active | — | — | +21 FF RV 2025 |
| Gilbert | 52→40→43; eff 97→92 [DOC] | 16.5/8.6→17.1/6.4 | new FC | new CH | K/9 11.9→9.3 |
| Abbott | 47.5→51.0 (up) | HB 9.1→6.7 | ST HB 11.9→14.0 | — | ball rate 33→38%, career-high BB% [DOC] |
| Wheeler | 38→22 over 6 yrs (~3°/yr) | 9.5" run; SI 17.3" | ST 9.9" | — | Driveline +23.7 FB RV |
| Leiter | 50.3→45.5 | Stuff+ 106→118 | — | new SI, kick-change | Loc+ 96→108 [DOC] |
| Palmquist | 20.7→16.1 | dropped FF for SI 4.7/16.5 | ST HB 8.8→12.6 | — | (this repo) |
| Yesavage | 63→66 | 20" IVB, 99% eff | gyro-ish SL | FS | pronator, no E-W precedent |
Others in the agent's full table: Jansen, Sánchez, Ober, Glasnow, Whitlock, McCullers, Kochanowicz, Klein, deGrom, Manaea,
Duran, Valdez, Kirby, Luzardo, Meyer, Elder, Seymour, Skenes, Sale — see data/derived/armangle_bucket_and_yoy_tables_2024_2025.txt.

## FanGraphs Stuff+ / Location+ / Pitching+ (primer, library.fangraphs.com)
- Sarris & Bay; tree-based (XGBoost per third parties) on per-pitch run values. Features: release point, velocity, V/H movement,
  spin rate, AXIS DIFFERENTIAL (observed vs spin-inferred axis = SSW proxy), differentials vs primary fastball (velo, movement —
  said to matter more than raw). VAA not explicit ("captured by release × movement"); arm angle not a feature. Pitch type used.
- Scaling: 100 mean, 10 = 1 SD at the PITCH level. Per-pitch-type Stf+ NOT re-centered: FF 99.2, CH 87.2, CU 105.5, FC 102.1,
  KC 110.3, SI 92.5, SL 110.8, FS 109.6. Pitcher-level SD: Stuff+ 12.2 SP / 17.0 RP; Loc+ 3.3/5.9; Pit+ 4.9/6.6.
- Stabilization: Stuff+ 80 pitches; Loc+ ~400; Pit+ beats preseason projections after ~250 (RP) / 400 (SP) pitches.
- Versions: launched 2023-03-10 (trained 2021–22); retrained 2024; Salorio (2025-03) reports FG's "new Stuff+" is an
  outcome-classification model (event probs → RV). Andrews (FG 2026-01-20): pitcher-level SD 9.7 (2020) → 8.8 (2025) and
  weaker correlation to wOBA/xwOBA since 2024. Criticisms: no explicit VAA/arm angle; team-switcher predictiveness drops (BP).
- Benchmarks: Tango — Stuff+ (2021) → ERA (2022) r=.37 (n=264, ≥40 IP); FIP→ERA .29; ERA→ERA .21. BP Judge — Stuff+ → next
  RA9 .41 same-team / .33 all / .14 switched; reliability Stuff+ .74, Loc+ .62, Pit+ .59. Zimmerman: ERA ≈ 49.19·e^(−.025·Stuff+)
  (3.00 ≈ 108, 4.00 ≈ 96). Our forward test (.371 to next-season RV/100, ≥300 pitches) sits on Tango's number.
- Other models: PitchingBot (XGBoost sub-models by pitch group; includes spin efficiency + axis deviation; 20–80 scale);
  PLV (Pitcher List; wOBA-value trees; 0–10); tjStuff+ (LightGBM on xRV; github tnestico/tjstuff_plus); aStuff+ v2 (Salorio;
  XGBoost on xRV, altitude + est. spin efficiency, train 21–23/test 24 — beats FG on next FIP/ERA in large samples);
  BATcast (Carty 2026-02: arm-angle-expected movement + tunneling); Driveline Stuff+ 2024 revision (SSW + deceptive release).

## Sources
Savant arm-angle/pitch-movement/spin-direction leaderboards; mlb.com/news/how-arm-slot-and-arm-angle-affect-pitches;
pubmed 41782391; blogs.fangraphs.com: its-release-angles-all-the-way-down, aiming-a-pitch-changes-how-it-moves,
emerson-hancock-became-less-efficient-and-more-effective, andres-munoz-is-an-analytical-blind-spot, they-dont-make-pitch-models-
like-they-used-to, dustin-may-is-finally-having-his-day, arm-angle-analysis-the-pros-and-cons-of-a-sidearm-shift,
introducing-the-bat-x-for-pitchers-and-the-batcast-stuff-model; drivelinebaseball.com 2019/09 spin-axis review, 2024/05
revisiting-stuff-plus, 2026/03 pitchers-are-going-low; library.fangraphs.com stuff-location-and-pitching-primer +
pitchingbot-pitch-modeling-primer; tangotiger.com predictiveness-of-the-tools-of-pitching; BP article 82426; RotoGraphs
referencing-pitch-quality-models; adamsalorio.substack.com introducing-astuff-v2; pitcherlist.com what-is-plv, dropping-down-who-
has-lowered-their-arm-slot, emerson-hancock-has-a-new-signature; athlonsports.com arm-angle pieces; lancebroz.substack.com
Hancock/Mariners; twinkietown Duran; thesportingtribune Kikuchi; tdabaseball.com arm-angle post; prpbaseball.com fastball shape.
