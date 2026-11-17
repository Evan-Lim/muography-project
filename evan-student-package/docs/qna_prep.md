# Demo-day Q&A preparation

The MYSSP rubric gives 10 minutes of questions and probes methodological
choices, confidence, limitations, generalisability and next steps. These are
the answers we rehearsed. Each answer starts with the short version.

## 1. Why this detector area and this chamber?

Because they are the project's baseline, not a design optimisation. The
0.25 m² area and 10 m radius chamber are fixed in `project_config.py`, so every
student compares the same model. The engineering question is the opposite one:
if you change the area, the exposure scales as \(1/A\); a 1 m² detector would
need 3.3 days instead of 13.3.

## 2. Why quote 5σ? Isn't that a discovery claim?

No. In this project 5σ is a predefined simulation benchmark, not a discovery
criterion. We use it because it is the threshold the project sheet specifies and
because it makes the exposure comparison concrete. A real analysis would need a
global look-elsewhere correction, a full likelihood, and control of detector
systematics before making a discovery claim.

## 3. What is the difference between expected and observed significance?

Expected significance compares two noiseless expectation maps:
\(S_{\exp}=(\mu_{\rm void}-\mu_{\rm rock})/\sqrt{\mu_{\rm rock}}\). It is
deterministic and defines the smooth exposure curve. Observed significance uses
one Poisson count: \(S_{\rm obs}=(N-\mu_0)/\sqrt{\mu_0}\). It changes with the
seed. The official headline uses \(S_{\exp}\) at a fixed pixel; the noisy maps
are demonstrations of fluctuations around it.

## 4. Why fix one pixel? Isn't that cherry-picking?

It is the opposite: fixing the pixel from the noiseless model prevents
cherry-picking. If we chose the brightest pixel in each noisy map, we would
select upward fluctuations and bias the exposure low. The null experiment shows
why: the maximum over 1,681 noise-only pixels is already about 3.4σ on average.

## 5. Why is the 30-day expected significance 7.5σ but the headline 13.4 days?

Because the signal grows as \(\sqrt{T}\). At 30 days \(S=7.50\), so
\(T_5 = 30(5/7.50)^2 = 13.3\) days. The 5σ crossing is earlier than 30 days;
30 days is simply a convenient exposure at which the chamber is already clear.

## 6. Why does the chamber signal scale with radius, not volume?

A muon radiograph integrates density along a line. The signal is the missing
chord through the chamber, approximately \(2r\), not the missing volume
\(\frac{4}{3}\pi r^3\). The fit gives \(S\propto r^{1.32}\) and
\(T_5\propto r^{-2.65}\). That is why a 4 m chamber needs 147 days while a
20 m chamber needs 2 days, not a factor of 125 different.

## 7. Why does the coarse angular bin look better in Study D?

Because the peak-pixel statistic is bin-dependent. Counts per pixel scale with
solid angle \(\Omega\propto(\Delta\theta)^2\), so
\(S_{\rm peak}\propto\Omega/\sqrt{\Omega}\propto\Delta\theta\). The whole-image
significance stays at about 3.5σ; the coarse-bin "gain" is a change in the
statistic, not in the physics. A real detector would also blur neighbouring
directions, which we do not model.

## 8. How do you know the ray tracer is correct?

Three checks: the chamber opacity deficit is 4,935 g/cm² against the geometric
5,000 for a 20 m chord; halving the ray step changes the map by at most 0.24%;
and the no-void control is zero to machine precision away from the chamber.
The central vertical opacity is 21,999 against 21,913 from the exact pyramid
geometry.

## 9. Why is the detector inside the pyramid footprint?

The baseline position is \((0,-40,3)\) m, which is inside the 230 m footprint.
We interpret it as a detector in an accessible niche or passage at the base;
the rock between that niche and the outside is not modelled. This is a stated
limitation, not a hidden assumption. A real campaign would need a surveyed
cavity or an external detector position.

## 10. What is the biggest systematic?

The assumed rock density. A 4% error (2.6 instead of 2.5 g/cm³) produces a fake
maximum of 3.86σ at 30 days and 9.46σ at 180 days, and a fake 2.72σ at the
chamber pixel at 180 days. A void and slightly lighter rock are degenerate in a
line-integrated measurement. Real campaigns need core samples, gravity data, or
a known-solid reference region.

## 11. Why does the exact pixel solid angle change the answer?

The project uses \(\Omega=(\Delta\theta)^2\). A tangent-plane pixel covers less
solid angle as it tilts: the exact factor is 0.866 at the signal pixel and about
0.77 at the field edge. The exact treatment lowers the counts and raises the
5σ exposure from 13.3 to 15.4 days. It is a systematic shift, not a statistical
error, and the report quotes both.

## 12. Why is the whole-image significance only 3.55σ?

Because the whole-image statistic divides the total excess by the square root
of the total background over all 1,681 pixels, including pixels that contain no
chamber. That is more conservative than asking whether one pre-selected pixel is
bright. The per-pixel value is the project's official definition; the
whole-image value is the global context and gives about 60 days for 5σ.

## 13. How does this compare with the 2017 Khufu result?

It is a simplified model of the same physics, not a reproduction. ScanPyramids
used nuclear emulsion, scintillator and gas detectors, and had to control
acceptance, efficiency, backgrounds and a real non-uniform target. Our toy
result shows the same qualitative behaviour: a roughly 10 m void inside a
roughly 100 m rock target needs a long exposure and careful systematics to reach
several sigma.

## 14. What would you do with another month?

Three concrete things: add a detector-response model (efficiency, angular
resolution, point-spread function); run a Monte Carlo over rock density and
efficiency to turn the single-point systematics into a confidence interval;
and replace the single radiograph with a multi-view 3D inversion. A real digital
elevation model of a Malaysian hill would make the stretch target useful.

## 15. Is the result reproducible?

Yes. The shared functions are in `code/student_analysis.py`; the seed is 0; the
notebooks run from fresh kernels; the baseline parameters are in one file; and
`figures/results_summary.json` contains every number used in the paper and
slides. The repository contains the code, notebooks, figures and logs.

## 16. How did the team divide the work?

All three members worked through the full pipeline independently, as the
project requires. Evan led the simulation and report integration; Junyi led the
spectrum/energy-loss validation and the video; Samantha led the parameter
studies and the slide design. Everyone reviewed the other's notebooks and
contributed to the Q&A rehearsal. The weekly logs record the individual work.

