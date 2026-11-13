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

