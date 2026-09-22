# Eight-week plan

Two months, eight hours per week, each student completing the full pipeline independently. The plan below assumes roughly
two sessions per week: one longer block for the work, one shorter block for
reading, writing and the mentor meeting.

The schedule is deliberately front-loaded. Weeks 1–5 build the machinery; weeks
6–8 use it. If you slip, slip in weeks 6–7, never in weeks 1–3.

| Week | Focus | Notebook | Due at the meeting |
|---|---|---|---|
| 1 | Setup, Python, the muon spectrum | 00, start 01 | Working environment; the spectrum plot; primer §1–2 read |
| 2 | Rock penetration, opacity, 1D calculation | 01 | Minimum-energy and surviving-flux plots; the "muons per day" estimate |
| 3 | The target; ray marching; the by-hand notch | 02 | Density-slice picture; opacity-vs-angle scan showing the dip |
| 4 | The opacity map | 02 | A 2D opacity image with the chamber visible; two tests of the code |
| 5 | Counts, and dividing out the pyramid | 03 | Expected-counts map; clean ratio map showing the chamber as an excess above 1.0 |
| 6 | Poisson noise; significance; the exposure curve | 04 | **The headline number**: first 5σ crossing of the expected-significance curve |
| 7 | Two parameter studies; first draft of report | 05 | Draft report with all figures in place |
| 8 | Rewrite, rehearse, present | — | Final report, slide deck, repository that runs top to bottom |

## Checkpoints that matter

Three moments decide whether this project lands.

**End of week 3.** The student must be able to trace a single ray and see the
notch. If ray marching is not working by the end of week 3, switch to the
supplied `opacity_map` from the mentor copy and continue — the project's
research content is in weeks 5–7, not in the geometry, and it is not worth
losing the whole thing to a stubborn loop.

**End of week 5.** The clean ratio map should show the chamber as an excess above 1.0; the exact peak depends on the angular grid and baseline parameters. If it does not, check the units and the target geometry before adding noise.

**End of week 6.** The expected-significance curve and its 5σ crossing exist. The noisy maps are demonstrations of statistical fluctuations, not the definition of the headline number. From here, everything else is
optional; the project has succeeded.

## If the student is ahead

Send them to Study D (angular bin size) and the Malaysian-target extension in
notebook 05. Both are open-ended enough to absorb any amount of extra capacity,
and the Malaysian estimate is genuinely worth showing to other people.

## If the student is behind

Cut, in this order: Study C and D, then the look-elsewhere demonstration, then
one of the two required parameter studies. Do not cut the exposure curve, and do
not cut the week-8 rewrite. A finished small project beats an unfinished large
one, and the student will learn more from polishing than from adding.
