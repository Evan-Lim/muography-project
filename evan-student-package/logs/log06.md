# Week 6 — Noise, significance, and the headline number

**Dates:** Week 6 of the eight-week plan
**Hours spent:** 8
**Notebook:** `notebooks/04_noise_and_exposure.ipynb`

## What I did

Added Poisson sampling with the reference seed 0, made 1-day and 30-day
observed maps, and plotted observed counts divided by the no-void expectation.
Built observed-significance maps and the smooth expected-significance curve at
14 exposure times. Chose the signal pixel once from the noiseless maps and held
it fixed. Ran 500 null experiments on the solid pyramid and 500 void experiments
at 7, 14 and 30 days. Computed the exact pixel solid angle as a systematic check.

## What I found

- Expected significance at the fixed pixel: 1.3696 at 1 day, 7.5016 at 30 days.
- 3σ crossing: 4.82 days. 5σ crossing: 13.37 days by interpolation, 13.33 days
  from the exact sqrt-T scaling. Quote 13.4 days.
- Observed 30-day significance at the fixed pixel is 7.70 (seed 0), close to the
  expected 7.50.
- Observed distributions: 7 days mean 3.75 ± 1.19, 15% cross 5σ; 14 days
  5.12 ± 1.24, 54% cross; 30 days 7.53 ± 1.23, 98% cross.
- Null control: mean maximum 3.44σ, median 3.40σ, 95th percentile 4.12σ; 91.6%
  of null maps have a 3σ pixel, none has a 5σ pixel. Mean number of pixels
  above 3σ is 2.68, close to the naive 2.27.
- Exact pixel solid angle: factor 0.866 at the signal pixel; S(30 d) falls from
  7.50 to 6.98, and T5 rises from 13.3 to 15.4 days.

## What went wrong / what I don't understand

- The first version of the 1-day significance map looked like pure noise, which
  is correct but made me doubt the sign convention. The null fixed-pixel
  histogram has mean zero and standard deviation one, so the convention is
  right.
- I initially wanted to use the maximum noisy pixel as the headline. The null
  runs show why that is a bad idea: the maximum is 3.4σ even with no chamber.
  The official result now uses the fixed pixel and the expected curve.

## Next week I plan to

- Run Studies A–D and the Malaysian extension.
- Add detector-area and density-systematics studies.
- Start the report with all figures in place.
