# Week 7 — Parameter studies and the Malaysian extension

**Dates:** Week 7 of the eight-week plan
**Hours spent:** 8
**Notebook:** `notebooks/05_parameter_study.ipynb`

## What I did

Ran all four named studies, changing one parameter at a time. For Studies A–C I
used the exact detector-to-chamber-centre ray, which avoids the 2° grid
alignment artefact; Study D uses the full map because the binning is the
variable. Built a conical limestone-hill model with an 8 m cave and ran the same
pipeline on it. Added three extra studies: detector-area scaling, rock-density
systematics, and a peak-pixel versus whole-image comparison. Wrote
`figures/results_summary.json`.

## What I found

- Study A: radius 4 m needs 146.6 days; radius 20 m needs 1.99 days.
  `S ∝ r^1.32`, `T5 ∝ r^-2.65`. The signal follows the chord, not the volume.
- Study B: depth 55–110 m gives T5 from 15.4 to 21.6 days, with a secondary rise
  near the apex. The baseline 70 m is on the broad optimum.
- Study C: distance optimum near `y = -25` m (15.9 days); lateral response is
  flat within ±30 m (17.1–19.8 days).
- Study D: peak-pixel S rises from 3.75 to 18.75 as the bin grows from 1° to 5°;
  whole-image S stays at 3.39–3.61. The coarse-bin gain is a statistic artefact.
- Malaysian hill: 9.1 days for 5σ, because the cave is seen through about 80 m
  of rock instead of 125 m.
- Area scaling: T5 ∝ A^-1.00, exactly.
- Density: a 4% error (2.6 instead of 2.5 g/cm³) fakes 9.46σ maximum at 180
  days; at the chamber pixel it fakes 2.72σ. This is the dominant systematic.
- Peak pixel 7.50σ vs whole image 3.55σ at 30 days; 13.3 vs 59.5 days for 5σ.

## What went wrong / what I don't understand

- Study B and C were jagged when I used the map maximum at 2°: a small change in
  chamber position moves the nearest ray on or off the chamber centre. Switching
  A–C to the exact on-axis ray fixed this and is physically cleaner.
- The lateral placement scan is weakly non-monotonic because the line of sight
  exits through different faces of the pyramid. I report it as a geometric
  effect, not a general rule.
- The 1° binning map is 81×81 and takes about 5 s per map; the notebook is still
  under two minutes because the other maps are coarser.

## Next week I plan to

- Write the final report and slides.
- Run every notebook from a fresh kernel and check reproducibility.
- Finalise the figure list and the code-availability section.
