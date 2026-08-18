# Supination / pronation bias from public Statcast — research note (2026-08-18)

## Operational definitions in use
- **4-seam spin efficiency (Savant spin-based active spin)** — Michael Rosen (FanGraphs, Hancock 2026-04-13; Bergert 2025-08-11):
  ≥95% = pronator class, <90% = supinator. Y2Y r² ≈ .65 → treated as a fixed motor preference. Hancock: 99% at 23° ("low-slot
  pronator jail") → <90% at 13° and became a supinator (added sweeper/cutter). Boyle 86% → 67% when slot 53° → 26°.
- **Hybrid "spin doctor"** — Jack Foley (Pitcher List, 2025-05-16): ~80–89% efficiency but high raw spin; good 4S via total
  spin, plus breaking balls with movement and small velo separation (Leahy 2355 rpm/85%, Bachar 2700/88%).
- **Sweeper tell** — Tread (Zombro via Rosen): a pronator pays −8 to −10 mph to get a breaking ball to 0" HB; a real sweeper
  (≥13" HB) at ≤10 mph off the FB is a supinator tell. Brewster: supinators apply force to the outside of the ball, pronators
  through center/inside; it is a spectrum.
- **Pronator's Triangle** — Delgado Genzor (BP 2024-01-05): running FB + gyro slider + high-rpm sidespin CH; also a
  "backspin bias" subtype (elite ride, floating changeups). **Kick change** = supinator's changeup (Strom/Tread; Martin, Holmes,
  Povich); a pronator throwing it "would mostly throw a worse regular changeup."
- **Seam-shifted wake** — Savant deviation = observed-movement axis − spin-based axis. Driveline 2021: SI +3" run/~4" drop,
  CH ~4" drop, FC +3" glove; sliders/curves ~0 on average. Seam-shift sinkers are a supinator trait (Rosen, Tread, TDA).
- **Expected FB axis by slot** — PRP clock bins (hop 12:00–1:30 RHP, sink 1:30–3:00); Max Bay's expected-movement-given-arm-angle
  residual (Flaherty/Imanaga/Clase "unexpected ride/cut"). No published formula — we use exp_axis = 180 ± (90 − arm_angle).

## Reachable families
| Class | Natural | With design | Avoid |
|---|---|---|---|
| Pronator (eff4 ≥95, run residual) | ride/ride-run 4S, sinker, changeup, splitter, gyro SL/cutter | Tread "sweeper grip for pronators" (velo cost); slot drop changes class | sweeper, big curve, cut-ride 4S, kick change |
| Backspin bias (very high eff, ~12:00, high slot) | elite-ride 4S, splitter, gyro | breaking array | dive changeup |
| Supinator (eff4 <90, cut residual) | cut-ride 4S, cutter, gyro & sweeper, curve, seam-shift SI | kick change / split-change | pronated CH, true ride-run 4S at 100% |
| Hybrid (80–89, high raw spin) | 4S + SI + sweeper + SL + CH/CB | — | — |

Archetypes: Yesavage (63–66°, 99% eff, 20" IVB, splitter, gyro-ish SL) = "extreme pronator … minimal ability to spin
breakers" (Brozdowski). Palmquist (low-slot LHP, SI + 74-mph sweeper): sinker+sweeper is the textbook supinator arsenal but
his 4S eff is 93% and the sweeper is 17 mph off the FB → hybrid/lean-pronator by the vote; classify on the data, not the slot.

## Sources
FanGraphs: Hancock (blogs.fangraphs.com/emerson-hancock-became-less-efficient-and-more-effective/), Bergert (…/in-at-least-one-respect-ryan-bergert-looks-like-an-ace/), kick change (…/what-if-a-pronator-not-a-supinator-threw-a-kick-change/, …/davis-martin-and-matt-bowman-break-down-the-kick-change/), release angles (…/its-release-angles-all-the-way-down/), SSW (…/the-seam-shifted-revolution-is-headed-for-the-mainstream/). Pitcher List: pitcherlist.com/spin-doctors-a-look-at-the-most-versatile-pitcher-archetype/. Tread: x.com/TreadAthletics/status/1825604066963046869. BP: baseballprospectus.com/news/article/87514/luis-castillo-and-the-pronators-triangle/. Driveline: drivelinebaseball.com/2021/03/the-impact-of-seam-shifted-wakes-on-pitch-quality/, …/2021/10/optimizing-breaking-ball-shape-through-data-driven-pitch-design-part-ii/. TDA: tdabaseball.com/post/how-important-is-the-new-statcast-arm-angle-data. PRP: prpbaseball.com/blog/master-your-fastball-shape-epfmk-bfa8h. Bunikiewicz: rbunikiewicz.substack.com/p/what-you-dont-know-about-pronation. Savant: baseballsavant.mlb.com/leaderboard/spin-direction-comparison, mlb.com/glossary/statcast/active-spin. Brozdowski on Yesavage: lancebroz.substack.com (2026 breakdown).
