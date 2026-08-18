# Slot-conditional arsenal simulator — design (v1.0 workflow agreed, 2026-08-18)

## WORKFLOW (agreed 8/18 — build against this)
Deliverable per pitcher: PROJECTED POSSIBLE Stuff+ → Location+ (kept, or
projected under the change) → PROJECTED Pitching+ → VALUE (fWAR / $) →
ranked list of undervalued FA/trade targets, each with the lever named.

Stage 0  Data + emulators
  - FG Stf+/Loc+/Pit+ overall & per pitch 2020–25; Savant shape/arm angle/
    spin; ids; transactions; contracts.
  - Stuff+ emulator (per-pitch Stf+ from shape) — grouped-CV per protocol.
  - Pitching+ emulator: Pit+ ≈ f(Stf+, Loc+, per-pitch mix). FG Pitching+ is
    its own model, NOT arithmetic on Stf+/Loc+, so fit the mapping (linear
    on Stf+/Loc+ likely r²≈.9) and report OOS error. This is what turns a
    projected Stuff+ into a projected Pitching+.
  - Value map: Pitching+ → run prevention per IP (fit on comps with similar
    Pit+; use next-season RA9/FIP not same-season) × role IP → fWAR → $ via
    $/WAR. Role (SP/RP) and IP are separate assumptions, stated on the card.

Stage 1  Levers → possible Stuff+
  - Lever A: slot change (module 2/3a). Output: new per-pitch Stf+ at best
    feasible slot.
  - Lever B: pitch addition at current slot (module 3b). Output: added
    pitch's Stf+ and its usage; overall Stuff+ moves because it's the
    usage-weighted average of per-pitch Stf+ (and existing pitches shift
    slightly through differentials — emulator handles that).
  - Joint search with cost per change; feasibility grade; support check.
  - Possible Stuff+ = best config; report actual, possible, gap, lever,
    feasibility, comps.
  - The model MUST be able to return "no lever." Yesavage (66°) is the named
    check: he plays NORTH-SOUTH because of the slot (ride/depth, steep VAA
    on the fastball, splitter/12-6 depth as the natural family) — east-west
    families have no precedent from there and a slot change of the size that
    would unlock them is infeasible → gap ≈ 0 → his Pitching+ path is
    Location+ (and velo). If the model finds him a lever, we're wrong, not
    him.
  - SLOT LEVER IS BIDIRECTIONAL. Pitchers get FLATTER (Palmquist: lower
    release → flatter VAA, axis rotates toward horizontal → run/sweep, east-
    west separation) OR STEEPER (higher release → steeper VAA, axis toward
    vertical → ride/depth, 12-6/splitter/changeup depth, north-south
    separation). The search runs ±10° in both directions and the transfer
    function must be fit on changers in both directions; do not let the
    Palmquist example bias the prior toward "lower is better." Which
    direction pays is a function of the pitcher's spin efficiency, VAA vs
    expectation, and existing arsenal — that's the model's job.
  - VAA IS A FIRST-CLASS VARIABLE (owner requirement). Compute fastball
    VAA (and HAA) per pitch from Statcast (release ht, extension, velo,
    IVB, plate height); normalize to a common plate height (height-adjusted
    VAA, HAVAA) so it isn't just a location artifact; also VAA-vs-expected
    at his release height/velo (the "flat for his height" premium). VAA
    enters: the emulator (fastball value), the transfer function (release
    ht → VAA is the mechanism by which slot changes move Stuff+ on
    fastballs, in both directions), the comps neighborhood for additions
    (steep-VAA pitchers add north-south families; flat-VAA add east-west),
    and the optionality index.

Stage 2  Location+ under the change
  - Default: keep past Location+ for pitch additions (small command cost).
  - Slot changes cost command: fit ΔLoc+ on the slot-changer corpus (and
    ΔLoc+ of added pitches on the addition corpus) and apply it — a lever
    that adds 10 Stf+ and loses 6 Loc+ is a different valuation.
  - Also project Location+ from its own aging/stabilization prior (Loc+
    stabilizes ~400 pitches; young pitchers gain).

Stage 3  Projected Pitching+ → value
  - Pitching+ emulator on (possible Stf+, projected Loc+) → projected Pit+
    with a range; value map → fWAR range → $ vs contract/market → rank on
    (value − price) × feasibility.

Backtests (grouped K-fold by pitcher + temporal; leakage protocol applies)
  - Addition corpus (primary, large n): which pitch, how good, did it stick.
  - Slot-changer corpus: predicted vs realized ΔStf+, and ΔLoc+.
  - End-to-end: for changers/adders, predicted vs realized ΔPit+ and
    next-season run prevention — that's the number a front office believes.
  - Cohort check: high-slot pitchers show fewer/worse additions and near-zero
    gaps (Yesavage cohort).

Card per target: actual Stf+/Loc+/Pit+ · possible Stf+ (lever, config,
comps, feasibility) · projected Loc+ · projected Pit+ range · fWAR/$ range ·
contract/control · market price · the tell.

---


Purpose: find undervalued MLB FA / trade targets for a real front office by
modeling what a pitcher's arsenal WOULD BE at a different arm slot / mix, and
what that's worth in FanGraphs Stuff+ units. Spec example: Carson Palmquist
(COL 21° → WSN 16°; Stf+ 92 → 107; sweeper 107 → 121; FA 86 → 109 at 16%
usage; sinker/sweeper ~35" east-west spread).

## Modules
1. Stuff+ emulator — regress FG per-pitch Stf+ (2020–25 pitcher-seasons) on
   Savant shape: velo, IVB, HB, VAA/HAA, arm angle, release ht/side, ext,
   spin, differentials vs primary FB. Bridge that keeps FG units and lets us
   score hypothetical arsenals. (Eval rules below apply HERE first.)
2. Slot → shape transfer function — physics prior (movement axis rotates with
   slot at <1:1, total Magnus break ~conserved for spin×eff×velo, release
   height ≈ shoulder + arm·sin(slot) → VAA/HAA) blended with natural
   experiments (pitchers with ≥4–5° y/y arm-angle change, IN BOTH
   DIRECTIONS — steeper and flatter modeled separately, then pooled if the
   physics is symmetric).
3. Arsenal search — two levers, searched JOINTLY (Palmquist pulled both:
   slot −5° AND added a sinker AND flipped usage), with a cost per change
   (slot change >> pitch add >> usage shift) so the optimizer prefers cheap
   moves and doesn't double-count.
   3a. Slot change — sweep ±10° in 1° steps; transform existing pitches via
       module 2; score with emulator.
   3b. Pitch addition at CURRENT slot (added 8/18) — for each pitch family
       the pitcher doesn't throw, ask: is there precedent for a pitcher with
       similar arm angle / fastball VAA / release height / spin efficiency /
       supination-pronation index / velo / hand throwing it, and what did it
       grade? Neighborhood = kNN (or conditional model) on those traits;
       candidate shape = comps' shape for that family; value = emulator on
       that shape in his arsenal context; feasibility = precedent count and
       add-success rate in the neighborhood.
       Supination/pronation index (Tread-style, from Statcast): 4-seam active
       spin % and axis tilt vs slot expectation (cut-side residual → supinator,
       run-side → pronator), breaking-ball gyro degree, changeup run/drop vs
       FB. Supinators: cutter/slider/gyro natural, changeup hard (kick-change
       is the workaround); pronators: sinker/changeup natural, sweep hard.
       This is a feature in the neighborhood AND a prior on which families
       are reachable.
   Output per pitcher: latent Stf+ (best config), the config, gap vs actual,
   and ARSENAL OPTIONALITY = breadth of reachable families × expected value
   of best add. Low optionality is the Yesavage knock (very high slot: elite
   now, but few precedents for adding east-west pitches if it stops working)
   — a risk term for extensions/acquisitions, not just an upside term.
4. Feasibility prior — release/axis variance, slot drift history, axis-tilt
   residual (already "wants" the slot), age, height; base rates from changers.
   Also SUPPORT check: counterfactual (slot, x0, z0, shape) must lie inside
   the population's observed region — never extrapolate off-manifold.

Pre-change tells (screens runnable today): axis-tilt residual vs slot; best
pitch's optimal slot ≠ current slot; Coors → road-only shape; sweeper-first
arsenal thrown from a 4-seam slot.

## Evaluation protocol (added 8/18 from @tomdoyo thread on identity leakage)
Claim: stuff models evaluated with naive train/test splits memorize pitchers.
Grouped 10-fold CV by pitcher_id drops a Stuff+ replica's same-season |r| to
xERA by ~22% (in-sample .54–.58 → OOS .42–.45); ablating x0, z0, extension,
ssw_angle, pitch_type_id, is_primary_fb SHRINKS the gap and IMPROVES OOS
(x0 −2.0% gap / +2.2% on 25→26; drop-5: gap .105→.072, OOS .422→.433).
Reading: release-position features act as pitcher fingerprints.

Why it matters MORE for us: our whole product is applying the model at a
release position the pitcher has never thrown from. A model that uses x0/z0
to look pitchers up will hand back a memorized value at the wrong address.

Rules:
- Every fitted component (emulator, transfer fn, feasibility) is evaluated
  with GROUPED K-fold by pitcher_id AND with a temporal holdout by season.
  Report in-sample vs grouped-OOS side by side; the gap is a first-class
  metric, not a footnote.
- Ablation table for the emulator on x0, z0, extension, ssw/axis features,
  pitch_type_id, is_primary_fb. Keep a feature only if grouped-OOS
  performance survives without the gap widening.
- Prefer physically-derived, slot-invariant-in-meaning features (VAA, HAA,
  arm angle, movement relative to slot expectation, movement/velo
  differentials) over raw x0/z0. If release position stays, it enters via
  arm angle + release height only, and counterfactuals must pass the
  support check.
- Extension: physically real (perceived velo) and ~conserved under a slot
  change, so lower counterfactual risk than x0/z0 — but still ablate; treat
  the tweet's numbers as one replica's hypothesis, verify on ours.
- Transfer fn / natural experiments: leave-one-pitcher-out (a changer's
  before+after live in the same fold).
- Palmquist implication: after a slot change the pitcher is a NEW pitcher
  to a memorizing model — some of a 14-pt swing may be fingerprint drift,
  not physics. The grouped-CV emulator lets us decompose "real shape value"
  from "model moved because release moved." Report both.
- Ground-truth eval for the emulator's ranking on unseen pitchers: OOS r to
  run value / xERA, √IP-weighted, IP ≥ 10, same as the thread — so numbers
  are comparable to public replicas.

## Pitch-addition corpus (module 3b validation — the biggest test set we have)
Definition: pitcher throws family F at <2% in year t and ≥5–10% in year t+1
(also in-season: <2% through May, ≥10% after July). Include TRIED-AND-
ABANDONED additions (appeared ≥5% for a stretch, then dropped) — failures
are precedent too; a success-only corpus is selection bias.
Pitch identity by movement CLUSTER, not label: Statcast added ST (sweeper) in
2023 and SV later, so label-based "additions" in 2023 are relabels; FG's
per-pitch Stf+ has no ST column (sweeper lives in SL). Define families by
(velo diff vs FB, HB, IVB, spin axis) within pitcher, map to FG columns for
scoring.
Tasks & metrics (all grouped K-fold by pitcher_id + temporal holdout):
- Which family gets added: multiclass, top-1/top-2 accuracy and calibration
  vs a slot-bucket base-rate baseline. Lift over baseline is the headline.
- How good it is: OOS r between predicted and realized year-t+1 Stf+ of the
  added pitch; and predicted vs realized change in overall Stf+/Pit+.
- Did it stick: P(still ≥5% usage next season) vs predicted feasibility.
- Optionality sanity: pitchers we score low-optionality should show fewer
  and worse additions historically; high-slot cohort as the named check.

## Validation that sells itself
Two backtests: (1) pitch-addition corpus above (large n, primary);
(2) hold out all slot-changers 2021–25; predict their post-change Stf+ from
pre-change data at the new slot; plot predicted vs realized ΔStf+. Palmquist
from 2025 → ~105 at 16° before looking at 2026. Then run the search over all
current MLB/40-man arms; rank by (latent − actual) × feasibility ÷ market
price; card per name (profile, optimal slot, projected arsenal, comps, tell,
contract/control).

## Data
FG leaderboards Stf+/Loc+/Pit+ overall + per pitch, 2020–25, min ~200
pitches (watch model-version drift across seasons; weight per-pitch Stf+ by
pitch count). Savant pitcher-season + pitch-level via pybaseball (arm angle,
active spin, axis, release, movement, ext). Chadwick id crosswalk. MLB stats
API for age/transactions/org tenure. Contract table (Spotrac/Cot's).

## Shelved
Δstuff-residual "optimization gap" model (weaker cousin of module 3).

## Open
- Does FG park-adjust movement (Coors)? If not, road-only for COL.
- Sample size of ≥4–5° changers; physics prior must carry most weight.

## Stage 0 status (2026-08-18) — repo ~/baseball-slot-sim
- Data: Chamberlain Pitch Leaderboard v8 extract (raw Statcast 2024–2026-08-16, 2.0M pitches, arm_angle)
  + his VAA/HAA/VAA-AA/HAA-AA/Dynamic-Dead-Zone (AzOE/AxOE/PythagOE) formulas reproduced. Note his dead
  zone conditions on RELEASE angle (VRA/HRA) — movement over expected given how the ball leaves the hand.
  FG Stuff+/Loc+/Pit+ overall+per-pitch 2020–26 pulled via leaderboard API (xMLBAMID join, 99% match).
  Statcast 2020–23 backfill via pybaseball running.
- Emulator: grouped-OOS R² .63 (in-sample .84 — gap .21 reproduces the leakage claim). Ablating release
  features does NOT close the gap here → leakage is pitcher-pitch persistence across seasons. Within-pitcher
  Δ prediction r=.47 (all), .55 (≥5° slot changers), .65 (FF, slope 1.1) — the simulator-relevant number.
  Emulator compresses extremes (Yesavage FS 137→118 pred; Palmquist SL 121→111).
- Corpora 2024–26: 86 slot-changers ≥5° (both directions), ~141 pitch additions. Backfill should ~3x.
- Sanity: league VAA FF −4.7/SI −5.9/CU −9.6; Yesavage 66°/7.1ft/19.5" IVB; Palmquist SI 14.7→4.7" IVB,
  SW −8.8→−12.6" HB, FF VAA −4.64→−3.98 but HAVAA (VAA_AA_pt) unchanged +0.5 → part of the raw
  flattening is location, not release. Palmquist pitch-weighted slot Δ = −3.8° (Savant headline 21→16).
- UPDATE (later 8/18, full 2020–26): emulator grouped-OOS .648 (gap .15), forward ≤23→24-25 .668.
  Within-pitcher Δ r=.59 on ≥5° slot changers, slope 1.03, both directions (.61 steeper/.57 flatter).
  Corpora 349 changers / 393 additions. Precedent module w/ functional roles + precedent-pool count:
  Yesavage pool n=16, optionality 1.1 (curve only) — no-lever check passes. Next: transfer function
  (module 2) on the 349 changers; addition classifier w/ OOF base rates; ΔLoc+ model; Pit+ emulator.
