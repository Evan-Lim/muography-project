# Student project sheet — Seeing Through Solid Rock

## The project in one sentence
Build and test a Python simulation of absorption muography, then determine the exposure time at which the **expected** chamber signal reaches 5σ under the project's simplified model.

## Baseline parameters

| Parameter | Baseline | Units |
|---|---:|---|
| Detector area | 0.25 | m² |
| Detector position | (0, −40, 3) | m |
| Pyramid base | 230 | m |
| Pyramid height | 139 | m |
| Limestone density | 2.5 | g/cm³ |
| Chamber radius | 10 | m |
| Chamber centre | (0, 0, 70) | m |
| Angular field | ±40 | degrees |
| Angular bin size | 2 | degrees |
| Ray step | 0.25 | m |
| Reference random seed | 0 | — |

Unless a study explicitly changes one of these, keep it fixed.

## Shared code architecture

- `code/muography.py`: supplied physics and geometry.
- `code/project_config.py`: baseline parameters.
- `code/student_analysis.py`: your work. Implement `opacity_map` in notebook 02 and `expected_counts` in notebook 03.
- Notebooks 04–05 import these functions rather than relying on variables left in memory by an earlier notebook.

## Weekly milestones

1. Python setup; reproduce the flux-vs-angle plot.
2. Range/energy and surviving flux; do the 100 m limestone check.
3. Build and inspect the target; verify a single-ray notch.
4. Complete the opacity map and test it against the no-void target and a smaller ray step.
5. Produce expected-count maps and the clean ratio map.
6. Add Poisson noise; produce observed significance maps and the **expected-significance** exposure curve; report the first expected crossing of 5σ.
7. Complete two of Studies A–D and place the figures in the report.
8. Finalise report, slides and reproducible repository.

## Two significance definitions

**Expected significance** compares the expected count with a chamber to the expected count without a chamber. It is deterministic for fixed parameters and defines the smooth exposure curve.

**Observed significance** compares one noisy Poisson count map with the no-chamber expectation. It changes when the random seed changes.

Do not use the maximum noisy pixel to define the official headline exposure time. If you explore the maximum pixel, label it as an exploratory statistic.

## Required outputs

- Working shared analysis module and notebooks.
- Target/density figure.
- Opacity map and validation tests.
- Expected-count map and clean ratio map.
- 1-day and 30-day noisy significance maps.
- Expected-significance exposure curve with 3σ and 5σ reference lines.
- Two parameter studies.
- Week-8 report and presentation.

## Reproducibility rule

Use the reference seed while developing and state the seed used for any noisy figure. A notebook must work from a fresh kernel; do not rely on variables created by running another notebook first.
