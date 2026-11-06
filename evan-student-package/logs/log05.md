# Week 5 — From opacity to a first image

**Dates:** Week 5 of the eight-week plan
**Hours spent:** 8
**Notebook:** `notebooks/03_first_image.ipynb`

## What I did

Implemented `expected_counts` in `code/student_analysis.py`. It calls
`opacity_map`, computes the zenith angle for every pixel from the tangent-plane
direction, uses `mg.transmitted_flux` for the integrated Gaisser flux above
`E_min`, and multiplies by detector area, pixel solid angle and exposure time.
Added a `counts_from_opacity` helper so exposure scans can reuse a traced
geometry. Rebuilt the target and no-void twin, produced the 30-day
expected-count map, and divided the two maps pixel by pixel to make the clean
ratio image.

## What I found

- The 30-day expected-count map runs from 191 to 1,197 counts per pixel, a
  factor 6.3. It is a picture of the pyramid, not the chamber.
- The clean ratio is 1.0000 away from the chamber and peaks at 1.4758 at
  `(ax, ay) = (0°, 30°)`.
- At the peak the expected counts are 366.8 with the chamber and 248.5 without:
  an excess of 118.3 muons in 30 days, or 7.50σ expected significance.
- The chamber adds only 0.36% to the total count, which is why the raw map
  hides it.

## What went wrong / what I don't understand

- The detector at `(0, -40, 3)` is inside the pyramid footprint, so a vertical
  ray exits through the sloping face after 87.7 m, not through the apex. I
  initially expected a central opacity near 34,750 g/cm² and got 21,999. The
  geometry is correct; the interpretation is a detector in a base-level niche.
- The 2° grid samples the chamber-centre direction (30.8°) at 30°, so the peak
  ratio is slightly below the ideal chord value. I documented this rather than
  interpolating.

## Next week I plan to

- Add Poisson noise and build observed significance maps.
- Produce the expected-significance exposure curve and the 5σ crossing.
- Demonstrate the look-elsewhere effect on the no-void control.
