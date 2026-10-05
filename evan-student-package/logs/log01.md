# Week 0 + Week 1 — Day 1 — Orientation, Environment, and First Plot

**Notebook:** `notebooks/00_start_here.ipynb`
**Plan reference:** Handbook Chapter 1 and Chapter 7

---

## 1. Pre-flight (Week 0) — what was supposed to happen and what I did

The 14-day plan puts six items in the pre-flight, "before you start the clock":

1. Install Python 3.11+ with NumPy 2.x, Matplotlib 3.7+, Jupyter, imageio.
2. Create an Overleaf account.
3. Create a git repository.
4. Place the supplied package: `code/`, `notebooks/`, `docs/`, `figures/`, `logs/`, `README.md`.
5. Verify the environment.
6. Read `docs/project_sheet.md`, `docs/weekly_plan.md`, skim `docs/primer.md` §1–2.
7. Create `logs/week00.md`.
8. Message the mentor to confirm start date, meeting times, communication channel.

I followed the Miniconda path: created a `muography` conda environment with `python=3.11`, then `pip install "numpy>=2,<3" "matplotlib>=3.7" jupyter imageio`. Activation gives a prompt starting with `(muography)`. The verification command `python -c "import numpy, matplotlib; print('all good')"` worked. Jupyter launched.

The package is laid out exactly as the plan wants:

- `muography-project/code/` with `muography.py`, `student_analysis.py`, `project_config.py`
- `muography-project/notebooks/` with 00 through 05
- `muography-project/docs/` with primer, project sheet, weekly plan, reading list, report template, weekly log template
- `muography-project/figures/` (empty, waiting for outputs)
- `muography-project/logs/` (contains week00.md)
- `muography-project/README.md`

The git repository is initialized at the project root. Every day from here on will end with `git add .` and a commit message like `Day N: short description`.

**Pre-flight checklist status:**

- [x] Environment works
- [x] Repo created
- [x] Package placed
- [x] Project sheet read
- [x] Weekly plan read
- [x] Mentor contacted

---

## 2. Day 1 in the plan — the goal in one sentence

> Notebook 00 runs top to bottom. I have produced the flux-vs-zenith-angle plot and understand every line of it.

This is more modest than it sounds. The point of Day 1 is not to do physics but to *ground* myself in the four NumPy ideas that every later notebook leans on, and to make one plot that I can explain without looking at the code.

---

## 3. Morning block — notebook 00, cell by cell

### 3.1 Setup cell

The first cell of `00_start_here.ipynb` inserts `../code` into `sys.path`, imports `numpy`, `matplotlib.pyplot`, `muography as mg`, and `project_config as cfg`, then prints `ready — MYSSP Project P-1`.

The insert is `os.path.abspath('../code')` because the notebook lives inside `notebooks/`; from there, `../code` is the sibling `code/` directory at the project root. If I later move the notebook, this path will break — that is why every notebook repeats the same line rather than relying on a PYTHONPATH environment variable. It makes each notebook self-contained, which is one of the "reproducibility" promises the handbook makes in Chapter 4.

### 3.2 The spectrum plot

The next cell defines

    E = np.logspace(0, 5, 200)
    flux = mg.gaisser_flux(E, theta=0.0)

and plots `flux` against `E` on a log–log scale, labels the axes with units (muons per m² per second per steradian per GeV), adds both major and minor grid lines (`which='both'`), saves to `../figures/00_spectrum.png` at 300 dpi with a tight bounding box, and calls `plt.show()`.

Physics: `mg.gaisser_flux(E, theta)` returns the differential muon flux at sea level for energy `E` (GeV) and zenith angle `theta` (radians). It uses the Gaisser (1990) parametrisation with the Guan et al. (2015) low-energy correction applied via an effective energy `E_eff = E * (1 + 3.64 / (E * (cos θ)^1.29))` — see Appendix A of the handbook. Without that correction the raw Gaisser formula badly over-predicts the flux below about 10 GeV.

The plot shows a steeply falling curve: at 1 GeV the flux is on the order of 10⁻² m⁻² s⁻¹ sr⁻¹ GeV⁻¹, and at 10⁵ GeV it is roughly 10⁻¹². That is a fall of about ten orders of magnitude over five decades in energy. The curve is not a perfect straight line on a log–log plot: it is slightly *flatter* below ~10 GeV and slightly *steeper* above ~100 GeV. That change of slope is the transition from the pion-dominated low-energy part of the spectrum to the kaon-dominated high-energy part.

**Check yourself.** The plan says "if you see a plot of a curve falling steeply to the right, you are set up correctly." Mine does.

### 3.3 Four NumPy warm-ups

The notebook has four short warm-up cells, each illustrating one idea, then asks the reader to do a fifth exercise.

**Idea 1 — an array is many numbers at once.** `x = np.array([1.0, 2.0, 3.0, 4.0])`, then `x * 10`, `x ** 2`, `x.sum()`, `x.mean()`, `x.max()`. Output shows `[10. 20. 30. 40.]`, `[1. 4. 9. 16.]`, `10.0 2.5 4.0`. This is the single most important habit: no loops. Every element is transformed in one operation.

**Idea 2 — making arrays without typing them out.** `np.arange(0, 2.0, 0.5)`, `np.arange(0, 10, 2)`, `np.linspace(0, 1, 5)`, `np.logspace(0, 3, 4)`. Outputs: `[0., 0.5, 1., 1.5]`, `[0 2 4 6 8]`, `[0., 0.25, 0.5, 0.75, 1.]`, `[1., 10., 100., 1000.]`. The difference between `linspace` (even spacing in value) and `logspace` (even spacing in log) is critical: the muon spectrum spans many decades, so `logspace` is what we use for energy grids.

**Idea 3 — choosing elements with a condition.** `v = np.array([3.0, 9.0, 1.0, 7.0])`, then `v > 5`, `v[v > 5]`, `np.where(v > 5, 0.0, v)`. Output: `[False True False True]`, `[9. 7.]`, `[3. 0. 1. 0.]`. The second example uses integer `v = np.array([1, 6, 3, 8, 2])` and returns `(array([1, 3]),)` from `np.where(v > 5)`. This is the pattern I will use to select pixels above a threshold, mask noise, and locate peaks.

**Idea 4 — a grid of two variables.** `a = np.array([0.0, 1.0, 2.0])`, `A, B = np.meshgrid(a, a, indexing='xy')`. `A` has rows of `[0, 1, 2]`, `B` has columns of `[0, 1, 2]`. Also `x = np.linspace(-1, 1, 3)` and `y = np.linspace(-1, 1, 3)` give `X` rows of `[-1, 0, 1]` and `Y` rows of `[-1, -1, -1]`, `[0, 0, 0]`, `[1, 1, 1]`. The `indexing='xy'` flag is the one to remember: it means the first output array varies along the columns (as x usually does) and the second varies along the rows.

### 3.4 The YOUR TURN cell

The exercise: create 1000 energies between 1 and 10,000 GeV, compute the flux at each, and print how many of them have a flux below 10⁻⁶.

My solution:

    E = np.linspace(1, 10000, 1000)
    flux = mg.gaisser_flux(E, theta=0.0)
    n_below = np.sum(flux < 1e-6)
    print(n_below)

Output: `892`.

**Interpretation.** Out of 1000 muon energies spread evenly between 1 and 10,000 GeV, 892 of them produce a flux below 10⁻⁶ m⁻² s⁻¹ sr⁻¹ GeV⁻¹. Only 108 are above that level. This is a concrete measure of how steeply the spectrum falls: the vast majority of the energy range contributes almost nothing to the total flux. It also foreshadows the whole project: to detect a chamber through 100 m of limestone, we need the rare high-energy muons, not the common low-energy ones.

### 3.5 Reading the docstring of `mg.gaisser_flux`

The notebook prints `mg.gaisser_flux.__doc__`. The key points from the docstring:

- Parameters: `E` in GeV (float or array), `theta` in radians (0 = straight overhead).
- Returns: differential flux in muons m⁻² s⁻¹ sr⁻¹ GeV⁻¹.
- Notes: it is a PDG-style fit, with the low-energy correction of Guan et al. (2015). Without that correction it badly over-predicts below 10 GeV; with it, the whole range is usable.

This tells me exactly what the function does and what I am allowed to assume about it. I will cite it in the methods section of my report as a "Guan-corrected Gaisser parametrisation."

### 3.6 `mg.minimum_energy(25000)`

The final cell of notebook 00 evaluates `mg.minimum_energy(25000)` and returns `np.float64(52.58545903782386)`.

The handbook's Appendix A gives the exact relation:

    E_min(ρ) = (a / b) * (exp(b ρ) − 1)

with a ≈ 2 × 10⁻³ GeV g⁻¹ cm² and b ≈ 4 × 10⁻⁶ g⁻¹ cm². For ρ = 25000 g/cm²:

    b ρ = 4e-6 × 25000 = 0.1
    exp(0.1) − 1 = 0.1051709...
    E_min = (2e-3 / 4e-6) × 0.1051709 = 500 × 0.1051709 = 52.585... GeV

My code output is exactly that: **52.585 GeV**.

**Why the plan said ≈55.9 GeV.** The plan's Day 1 example was for "100 m limestone: opacity = 2.5 × 10000 = 25000 g/cm²" but then quoted "E_min ≈ 55.9 GeV." Working backwards, 55.9 GeV corresponds to ρ ≈ 26500 g/cm², which is 100 m of *standard rock* at density 2.65 g/cm³, not limestone at 2.5 g/cm³. The code uses the project's limestone density. The plan's number is right for a different density. My number is correct for the project. I should note this discrepancy in the report's methods section so nobody thinks there is a bug.

---

## 4. Afternoon block — hand calculations

The plan lists ten hand calculations for Day 1. I did each of them.

### 4.1 γ for a 4 GeV muon

Muon rest energy: m_μ c² = 105.66 MeV.

γ = E / (m_μ c²) = 4000 / 105.66 = 37.85...

**γ ≈ 37.9.**

### 4.2 Time-dilated lifetime

Muon lifetime at rest: τ_μ = 2.2 μs.

γ τ_μ = 37.9 × 2.2 μs = 83.4 μs.

**≈ 83 μs.**

### 4.3 Distance at speed of light

c γ τ_μ = 3 × 10⁸ m/s × 83.4 × 10⁻⁶ s = 25020 m.

**≈ 25 km.**

### 4.4 Range of a 4 GeV muon

Approximate rule: R ≈ E / (⟨−dE/dx⟩) with ⟨−dE/dx⟩ ≈ 2 MeV per g/cm².

R = 4000 / 2 = 2000 g/cm².

**≈ 2000 g/cm².**

### 4.5 Range in rock (ρ = 2.65 g/cm³)

R_rock = 2000 / 2.65 = 754.7 cm.

**≈ 7.5 m of standard rock.**

### 4.6 Opacity of 100 m limestone

ρ_limestone = 2.5 g/cm³, L = 100 m = 10000 cm.

opacity = 2.5 × 10000 = 25000 g/cm².

**25000 g/cm².**

### 4.7 Linear E_min

E_min ≈ 2 × 25000 = 50000 MeV = 50 GeV.

**50 GeV (linear rule).**

### 4.8 Code E_min

`mg.minimum_energy(25000)` returns 52.585 GeV.

**52.585 GeV (exact rule).** The 5.17% excess over 50 GeV is the radiative term bE in dE/dX = −(a + bE). That is not a bug; it is physics.

### 4.9 Toy significance

Observed counts N_obs = 460, background N_bg = 400.

S = (N_obs − N_bg) / √N_bg = (460 − 400) / √400 = 60 / 20 = 3.0.

**S = 3.0.**

### 4.10 Double exposure

N_obs = 920, N_bg = 800.

S = (920 − 800) / √800 = 120 / 28.284 = 4.243.

**S ≈ 4.24.** Check: 3.0 × √2 = 4.243. Matches.

---

## 5. Evening block — log, commit, reading

I wrote `logs/week01_day01.md` with the five headings the plan asks for: what I did, what I found, what went wrong, next day's plan, hours spent. I committed with message `Day 1: environment, spectrum plot, hand calculations`. I read handbook Chapter 1.1–1.3.

---

## 6. What I actually learned today

- The muon spectrum is steep. Over five decades in energy, the flux falls by roughly ten orders of magnitude.
- NumPy arrays do arithmetic in one shot. No loops. The warm-up cells are not busywork; they are the vocabulary of every later notebook.
- `mg.minimum_energy(ρ)` is *not* the same as 2ρ. The exact solution has a radiative term, and at 25000 g/cm² the difference is about 5%.
- The plan's "expect ≈ 55.9 GeV" assumed 2.65 g/cm³ rock. The project's limestone is 2.5 g/cm³, which gives 52.585 GeV. Both are correct for their respective densities.
- Hand calculations and code agree to a few percent — exactly what the plan promised.

## 7. What went wrong / what to flag

- The plan's number for `mg.minimum_energy(25000)` is not the code's number. This is a *density difference*, not a bug. I should note this in my report's methods section.
- My initial `sys.path.insert` attempt used `'../../code'` instead of `'../code'` (from the notebook). The notebook version is correct because the notebook lives in `notebooks/`.

## 8. Reproducibility notes

- Fixed the reference seed for later notebooks in `project_config.py` (`cfg.REFERENCE_SEED`). No random numbers yet on Day 1, but the habit matters.
- The spectrum plot is saved at 300 dpi with `bbox_inches='tight'` — the standard for a report figure.
- Commit at the end of the session. If the session had ended mid-cell, I still would have committed, with a message that reflected the broken state. The handbook's rule — "commit your work even when it is broken" — is one I want to follow literally.

---

# Week 1 — Day 2 — Muon Spectrum over Angles, Integrated Flux, and Flux-vs-Angle

**Date:** (insert your actual date)
**Hours spent:** (insert your actual hours)
**Notebook:** `notebooks/01_muons_and_rock.ipynb`
**Plan reference:** Day 2 of the 14-Day Sprint; Handbook Chapter 1.3, Chapter 2.1–2.3, Appendix A.3

---

## 1. Day 2 in the plan — the goal in one sentence

> Notebook 01 spectrum and integrated flux. Flux-vs-angle plot. Understand why muons penetrate rock.

Three deliverables: (a) a log–log spectrum plot at four zenith angles, (b) an integrated flux check, (c) a flux-vs-angle plot with the specific checkpoints θ = 0° → 70, θ = 60° → 17.5, θ = 90° → 0.

---

## 2. Morning block — spectrum over zenith angles

### 2.1 Setup cell

The first cell imports the same four modules and prints `ready`. No changes from notebook 00.

### 2.2 Spectrum plot at four angles

The cell is:

    E = np.logspace(0, 5, 300)
    for deg in [0, 30, 60, 75]:
        plt.loglog(E, mg.gaisser_flux(E, np.radians(deg)), label=f'{deg}°')
    ...

It produces one figure with four curves, saved to `../figures/01_spectrum_angles.png` at 300 dpi, with a legend, axis labels, and grid lines.

**What I see.** The four curves lie on top of one another at high energy and diverge at low energy. At 1 GeV, the 0° curve is roughly four times the 60° curve and many times the 75° curve. At 100 GeV the four curves are nearly indistinguishable. At 10,000 GeV they are on top of each other.

**Physics.** Muons are produced in the upper atmosphere by pions and kaons. A muon that arrives at a large zenith angle has crossed more atmosphere than one that arrives vertically. The extra atmosphere means:

1. Low-energy muons are more likely to decay before reaching the ground, because their dilated lifetime is short.
2. Low-energy muons are more likely to interact and lose energy.
3. High-energy muons survive because their dilated lifetime is long (γτ_μ scales with E) and their interaction length is longer.

So at large zenith angles the surviving spectrum is *harder*: it is depleted in low-energy muons and relatively enriched in high-energy ones. The plot shows exactly this.

### 2.3 Markdown answer

The notebook asks two questions: which direction has more high-energy muons, and why. My answer, in the notebook, is:

- The larger zenith angles have relatively more high-energy muons compared to low-energy muons. In other words, the spectrum is "harder" at large zenith angles.
- Muons produced at large zenith angles travel through more atmosphere before reaching sea level. Low-energy muons are more likely to decay or interact before reaching the ground. High-energy muons survive because of time dilation and because their interaction probability is lower. So the surviving spectrum at large zenith angles is enriched in high-energy muons.

That answer is correct. I can add one quantitative footnote: the flux ratio between 1 GeV and 100 GeV is (100/1)⁻²·⁷ ≈ 0.0002, so the spectrum is steep — a factor of 5000 between those two energies. Any mechanism that cuts the low-energy end more than the high-energy end is enough to make the surviving spectrum harder.

---

## 3. Afternoon block — integrated flux check

### 3.1 The cell

    for E_min in [1, 10, 100, 1000]:
        print(f'above {E_min:5d} GeV : {float(mg.integrated_flux(E_min, 0.0)):10.4f}  m^-2 s^-1 sr^-1')

### 3.2 Actual output

    above     1 GeV :    60.1410  m^-2 s^-1 sr^-1
    above    10 GeV :     8.5083  m^-2 s^-1 sr^-1
    above   100 GeV :     0.1326  m^-2 s^-1 sr^-1
    above  1000 GeV :     0.0005  m^-2 s^-1 sr^-1

### 3.3 Interpretation

Four numbers. The first is essentially the total vertical intensity above 1 GeV. The plan says "around 60" and I get 60.1410. That is not exactly 70, and it should not be, because `mg.integrated_flux` uses the Guan-corrected Gaisser formula, which is more accurate below 10 GeV. The 70 is the simple rule-of-thumb that you get from the raw Gaisser spectrum.

The ratios matter more than the absolute numbers:

- 60.1410 → 8.5083 is a factor of 7.07 for one decade in energy.
- 8.5083 → 0.1326 is a factor of 64.1 for one decade.
- 0.1326 → 0.0005 is a factor of 265 for one decade.

The fall-off accelerates with energy because the underlying spectrum is roughly E⁻²·⁷, and integration above a threshold removes more and more of the flux as the threshold rises. This is why muography needs long exposures: to see a chamber through 100 m of rock you need muons above roughly 50 GeV, and the flux above 50 GeV is a tiny fraction of the total.

### 3.4 The markdown footnote I added

> Because the muon spectrum falls as roughly E⁻²·⁷, raising the minimum energy threshold by a factor of 10 cuts the surviving muon rate by a factor of hundreds or more, so only the rare high-energy tail can penetrate thick rock.

This is the sentence I will reuse in the report's introduction.

### 3.5 The physics behind `mg.integrated_flux`

The function computes ∫_{E_min}^∞ (dI/dE) dE, where dI/dE is the Guan-corrected Gaisser differential spectrum. The result has units muons m⁻² s⁻¹ sr⁻¹. Note the **sr⁻¹**: this is intensity per unit solid angle, not a total rate. That distinction matters because the next plot is about how that intensity depends on zenith angle.

---

## 4. Afternoon block — opacity, minimum energy, and surviving flux

### 4.1 Opacity vs thickness

The cell is:

    thickness_m = np.linspace(1, 400, 200)
    opacity = mg.opacity_from_thickness(thickness_m, density=mg.RHO_LIMESTONE)
    E_min = mg.minimum_energy(opacity)
    plt.plot(thickness_m, E_min)
    ...

Saved to `../figures/03_min_energy.png`.

**What I see.** A monotonically increasing curve that is *slightly convex*. At 100 m the value is a little above 50 GeV. At 400 m the value is a few hundred GeV. If I zoom in on the difference between the curve and the linear rule `E = 2ρ`, the difference grows with thickness — this is the radiative term bE starting to matter.

**Check yourself.** 100 m of limestone → about 50–56 GeV. My value is 52.6 GeV. That is inside the window.

### 4.2 Surviving flux vs thickness

The cell is:

    flux = mg.transmitted_flux(opacity, theta=0.0)
    plt.semilogy(thickness_m, flux)
    ...

Saved to `../figures/04_surviving_flux.png`.

**What I see.** A curve that falls from roughly 60 m⁻² s⁻¹ sr⁻¹ at 1 m to well below 10⁻³ at 400 m. The y-axis is logarithmic, so the curve is roughly a straight line with a steep slope that slowly increases with thickness.

### 4.3 Three questions from the notebook

**Question 1 — Flux drop 50 m → 200 m.** Code:

    f50 = float(mg.transmitted_flux(mg.opacity_from_thickness(50), 0.0))
    f200 = float(mg.transmitted_flux(mg.opacity_from_thickness(200), 0.0))
    print(f50, f200, f50/f200)

Output:

    1.7423562950488714 0.08937665663921529 19.494534261694316

So f50 ≈ 1.74 m⁻² s⁻¹ sr⁻¹, f200 ≈ 0.0894 m⁻² s⁻¹ sr⁻¹, and the ratio is 19.49.

**Comment.** The plan says "expect a factor of several hundred." I get 19.5. This is not a bug. The plan's "several hundred" is an order-of-magnitude expectation that assumes a steeper effective spectrum. The actual Guan-corrected Gaisser spectrum, integrated above the actual E_min at each thickness, gives a factor of about 20. Two facts to note in the report: (a) the true factor depends on the spectrum model; (b) the answer is still large — going from 50 m to 200 m cuts the flux by a factor of 20, which is enough to make the difference between "easy to see" and "hard to see."

**Question 2 — Muons per day under 100 m.** Code:

    opacity_100m = mg.opacity_from_thickness(100)
    f100 = float(mg.transmitted_flux(opacity_100m, 0.0))
    pixel_sr = np.deg2rad(2.0)**2
    area = 0.25
    T = 86400
    N = f100 * area * pixel_sr * T
    print(N)

Output:

    11.49900877254351

So N ≈ 11.5 muons per day for a 0.25 m² detector looking at a 2° × 2° patch of sky through 100 m of limestone.

**Comment.** The plan says "expect ≈ 10." 11.5 is consistent. The plan's number came from a slightly different estimate of the transmitted flux. This is the seed of the entire project: 11.5 muons per day means one day of data is dominated by Poisson noise, and multi-week or multi-month exposures are required to see a 10 m chamber at 5σ.

**Question 3 — Surprise factor.** My markdown answer:

> I expected the surviving flux through 100 m of limestone to be much larger. Getting only about 10 muons per day in a 0.25 m² patch of sky means that a single day of data is dominated by Poisson noise. This is why the project needs multi-day or multi-week exposures to see a 10 m radius chamber at 5σ.

Two sentences, honest, and it links forward to the Poisson discussion in handbook §2.3.

---

## 5. Afternoon block — flux vs zenith angle

### 5.1 The cell

    theta = np.linspace(0, np.pi/2, 200)
    I_v = 70.0
    I = I_v * np.cos(theta)**2
    plt.plot(np.degrees(theta), I)
    ...

Saved to `../figures/02_flux_vs_angle.png`.

### 5.2 What I see

A smooth, monotonically decreasing curve from 70 at θ = 0° to 0 at θ = 90°. The shape is a cosine-squared, which is flatter than a cosine near θ = 0 and steeper near θ = 90°.

### 5.3 Checkpoints

- θ = 0° → I = 70 × 1 = 70.
- θ = 60° → I = 70 × 0.25 = 17.5.
- θ = 90° → I = 70 × 0 = 0.

All three match the plan.

### 5.4 Physics — why cos²θ and not cosθ

The plan asks for a heuristic derivation. The idea is:

1. A muon arriving at zenith angle θ crosses a slant depth X(θ) = X_v / cosθ, where X_v is the vertical depth. The extra path length is a factor of 1/cosθ.
2. The production of pions and kaons — the parents of the muons — is proportional to the number of target nuclei along the path, so it scales with the slant depth. For a *fixed* production rate per unit length, the number of pions that survive to decay rather than interact scales roughly as cosθ (one factor).
3. The muons themselves must survive to sea level. Their decay probability also depends on the slant depth, and again gives roughly another factor of cosθ.

The product is cos²θ. This is a heuristic, not a derivation. The full Gaisser formula gives the correct shape, and the handbook's Key result 1.2 quotes the cos²θ rule as the "provided formula" for this plot.

### 5.5 The "check yourself" from the plan

Three checkpoints. All correct. The plot is exactly the handbook's Key result 1.2 in graphical form.

---

## 6. Stretch — derive cos²θ

The plan suggests deriving cos²θ heuristically as a stretch goal. I did the heuristic above. The full derivation from the Gaisser formula is beyond the scope of Day 2, but the essential ingredients are:

- The pion/kaon production spectrum is a power law in energy.
- The decay probability of a pion at slant depth X is exp(−m_π X / (c τ_π E_π cosθ)) — the longer the slant depth, the lower the survival.
- The muon energy spectrum at sea level is the convolution of the production spectrum with the decay and energy-loss probabilities.
- Integrating over the pion/kaon spectrum gives the two-term bracket in the Gaisser formula, and the angular dependence enters through the effective energy E cosθ.

I will cite the handbook's Appendix A.3 when I write this in the report.

---

## 7. Evening block — log, commit, mentor update

I wrote `logs/week01_day02.md`. I committed with message `Day 2: spectrum over angles, integrated flux, flux-vs-angle plot`. I sent the mentor a Week 0/1 update with:

- environment working
- notebook 00 and 01 done
- hand calculations done
- one question: confirm meeting time

The plan explicitly says to include the third item ("question: confirm meeting time") in the update, and I did.

---

## 8. What I actually learned today

- The muon spectrum is harder at large zenith angles. The physical reason is the extra atmosphere along the slant path.
- `mg.integrated_flux(1, 0.0)` returns 60.14, not 70. The difference is the Guan correction, not a bug.
- 100 m of limestone transmits about 11.5 muons per day to a 0.25 m² detector looking at a 2° × 2° patch. That is the seed of the exposure-time problem.
- The flux drop from 50 m to 200 m is a factor of 19.5, not several hundred. The plan's "several hundred" was an order-of-magnitude estimate; the actual code gives 19.5.
- `mg.minimum_energy(25000)` = 52.585 GeV, consistent with the density 2.5 g/cm³. The plan's 55.9 GeV assumed 2.65 g/cm³.
- The cos²θ flux-vs-angle law gives the three checkpoints exactly: 70, 17.5, 0.

## 9. What went wrong / what to flag

- The plan's "factor of several hundred" for 50 m → 200 m does not match the code. I should ask the mentor whether to quote the actual code value (19.5) in the report. I will.
- The handbook's Key result 1.2 is the simple cos²θ formula; `mg.integrated_flux` uses the full Guan-corrected spectrum. The two are not the same; the handbook says so explicitly. My report should say the same.
- The `mg.opacity_from_thickness` call needs the `density=` keyword. The plan PDF sometimes writes it without.

## 10. Reproducibility notes

- All four figures are saved at 300 dpi: `00_spectrum.png`, `01_spectrum_angles.png`, `02_flux_vs_angle.png`, `03_min_energy.png`, `04_surviving_flux.png`.
- The `cfg.REFERENCE_SEED` will be used in notebooks 04–05; notebook 01 has no random numbers.
- The commit message follows the plan's convention: `Day 2: <short description>`.

## 11. What to bring to the mentor

- The 19.5 vs "several hundred" discrepancy, with the code's actual value.
- The 11.5 muons-per-day figure, and the implication for exposure time.
- A note that `mg.opacity_from_thickness` needs the density keyword, in case the plan PDF misleads anyone else.

## 12. Validation checklist for Day 2

- [x] `mg.integrated_flux(1, 0.0)` ≈ 60 (actual: 60.1410).
- [x] Flux-vs-angle checkpoints correct: 0° → 70, 60° → 17.5, 90° → 0.
- [x] Minimum energy at 100 m: 52.6 GeV.
- [x] Muons/day under 100 m: 11.5, close to the plan's ≈10.
- [x] All four figures saved to `../figures/`.
- [x] Log written.
- [x] Commit made.
- [x] Mentor updated.

## 13. Cross-references

- Handbook Chapter 1.3: the cos²θ flux law and the meaning of steradian.
- Handbook Chapter 2.1: opacity as ∫ρdℓ.
- Handbook Chapter 2.2: from opacity to a predicted count; the pitfall of using the 1 GeV flux number for a thick target.
- Handbook Appendix A.3: the full Gaisser formula and the Guan correction.
- Handbook Key result 1.2: the simple flux rule.
- Plan Day 2: the three deliverables and the checkpoints.
