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

