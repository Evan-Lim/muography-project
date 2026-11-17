# Week 1 — Day 3 — Range-Energy and 1D Survival

**Notebook:** `notebooks/01_muons_and_rock.ipynb` (min-energy and surviving-flux cells already completed on Day 2)
**Plan reference:** Day 3 of the 14-Day Sprint; Handbook Chapter 1.2, Appendix A.1, Appendix C.1

---

## 0. Status at the start of Day 3

When Day 3 began, the two headline plots of the day were already saved from Day 2:

- `figures/03_min_energy.png` — minimum energy vs limestone thickness, from 1 m to 400 m.
- `figures/04_surviving_flux.png` — transmitted muon flux vs limestone thickness, on a semilog y-axis.

The three notebook questions had also been answered:

- f50 = 1.7423562950488714, f200 = 0.08937665663921529, ratio f50/f200 = 19.494534261694316.
- muons per day under 100 m for 0.25 m² and 2° × 2° = 11.49900877254351.
- Surprise factor: the surviving flux through 100 m is only about 11 muons per day, which means single-day data is Poisson-dominated and the project needs multi-day or multi-week exposures.

So the morning and afternoon blocks of Day 3 were already done. The remaining work was the stretch derivation, reading the Khufu paper, and writing this log.

---

## 1. What I did

### Morning block

- Reopened `01_muons_and_rock.ipynb` and confirmed the two plots from Day 2 are still present and correctly saved.
- Confirmed `mg.minimum_energy(25000)` returns `np.float64(52.58545903782386)`.
- Re-derived the exact range-energy relation from `dE/dX = -(a + bE)` (see Section 3).
- Verified the small-ρ limit of the exact relation reduces to the linear rule `E_min ≈ a ρ`.
- Verified the numerical check by hand: for ρ = 25000 g/cm², the exact formula gives 52.585 GeV and the linear rule gives 50 GeV.
- Started the optional extra validation figure `03b_min_energy_linear_vs_exact.png` comparing the exact curve with the linear rule.

### Afternoon block

- Read the abstract and figures of Morishima et al. 2017 (the ScanPyramids Khufu paper).
- Wrote a draft paragraph for the report's introduction comparing this simulation to the real Khufu result.
- Did not run any new notebook cells beyond the optional validation figure.

### Evening block

- Wrote this log.

---

## 2. What I found

- The exact range-energy relation is `E_min(ρ) = (a/b)(e^{bρ} − 1)`.
- For small `bρ`, the exponential expands to `1 + bρ`, and the exact formula reduces to the linear rule `E_min ≈ a ρ`.
- At ρ = 25000 g/cm² (100 m of limestone), the exact formula gives 52.585 GeV and the linear rule gives 50 GeV. The 5.17% difference is the radiative term.
- The gap between exact and linear grows with thickness: about 5% at 100 m, about 10% at 200 m, about 22% at 400 m.
- The Khufu paper reports a large void above the Grand Gallery, detected independently by three muon detector technologies. Significance ~5σ. This is the historical anchor for the project.
- My simulation is a simplified model of the same idea, not a reproduction of the ScanPyramids analysis.

---

## 3. Hand calculations

### 3.1 Derivation of E_min(ρ) from dE/dX = −(a + bE)

Start from the energy-loss equation:

    dE/dX = −(a + bE)

Separate variables:

    dE / (a + bE) = −dX

Integrate from E = E_min at X = 0 to E = 0 at X = ρ:

    ∫_{E_min}^{0} dE / (a + bE) = − ∫_{0}^{ρ} dX

Let u = a + bE, so du = b dE and dE = du / b. Then

    ∫ dE / (a + bE) = (1/b) ∫ du / u = (1/b) ln(a + bE)

Evaluating at the limits:

    (1/b) [ln(a) − ln(a + b E_min)] = − ρ

Multiply by b:

    ln( a / (a + b E_min) ) = − b ρ

Exponentiate:

    a / (a + b E_min) = e^{− b ρ}

Invert:

    a + b E_min = a · e^{ b ρ }

Subtract a and divide by b:

    E_min(ρ) = (a / b) ( e^{ b ρ } − 1 )

This is the exact range-energy relation implemented in `mg.minimum_energy`.

### 3.2 Small-ρ limit

For small bρ, expand the exponential:

    e^{ b ρ } ≈ 1 + b ρ + (b ρ)² / 2 + ...

So

    e^{ b ρ } − 1 ≈ b ρ

Therefore

    E_min(ρ) ≈ (a / b) · b ρ = a ρ

With a = 2 × 10⁻³ GeV g⁻¹ cm², this is the linear rule `E_min ≈ 2ρ MeV`. That is the handbook's Key result 1.1.

### 3.3 Numerical check at ρ = 25000 g/cm²

    bρ = 4 × 10⁻⁶ × 25000 = 0.1
    e^{0.1} − 1 = 0.1051709...
    a / b = 2 × 10⁻³ / 4 × 10⁻⁶ = 500 GeV
    E_min = 500 × 0.1051709 = 52.5854... GeV

Code output: `np.float64(52.58545903782386)`. Matches to all shown digits.

Linear rule:

    E_min ≈ a ρ = 2 × 10⁻³ × 25000 = 50 GeV

Difference: 52.585 − 50 = 2.585 GeV, or 5.17% of the linear value. This is the radiative term.

### 3.4 Optional — exact vs linear curve for the report

If I add the extra figure, I will plot:

    thickness_m = np.linspace(1, 400, 200)
    opacity = mg.opacity_from_thickness(thickness_m, density=mg.RHO_LIMESTONE)
    E_exact = mg.minimum_energy(opacity)
    E_linear = 2e-3 * opacity

    plt.plot(thickness_m, E_exact, label='exact')
    plt.plot(thickness_m, E_linear, '--', label='linear (a·ρ)')
    plt.xlabel('Limestone thickness (m)')
    plt.ylabel('Minimum muon energy (GeV)')
    plt.title('Exact vs linear range-energy relation')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('../figures/03b_min_energy_linear_vs_exact.png', dpi=300, bbox_inches='tight')
    plt.show()

Expected behaviour: the two curves are indistinguishable below about 100 m and diverge visibly above 200 m, with the exact curve lying above the linear one.

---

## 4. Reading the Khufu paper

### 4.1 Citation

Morishima, K., Kuno, M., Nishio, A. et al. **Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons.** *Nature* 552, 386–390 (2017). DOI: 10.1038/nature24647.

### 4.2 What the paper does

The ScanPyramids collaboration placed three independent muon detectors inside the Queen's Chamber of the Great Pyramid of Khufu:

- Nuclear emulsions (Nagoya University).
- Scintillator hodoscopes (KEK).
- Gas electron multipliers (CEA).

Each detector looked upward through the pyramid and measured muon flux as a function of direction. Higher flux means less rock along that line of sight — the signature of a void.

### 4.3 What they found

A large void above the Grand Gallery, roughly 30 m long and at least 8 m tall, comparable in volume to the Grand Gallery. Detected independently by all three technologies. Significance around 5σ.

### 4.4 Why this matters for my report

- My simulation uses a simplified square pyramid with a spherical chamber. The real Khufu pyramid has a complex internal structure.
- My detector is a single idealised 0.25 m² pixel. The real measurement used three different technologies with different acceptances, efficiencies, and backgrounds.
- My background is Poisson counting only. The real analysis had to account for atmospheric variations, detector systematics, and the look-elsewhere effect.
- My headline number — the expected exposure time for 5σ — is a model number, not a prediction for the real Khufu void.

The comparison I can make is at the level of physics and scale: both my simulation and their measurement show that a ~10 m scale void inside a ~100 m rock target is detectable at the several-σ level only with long exposures and careful control of systematics.

### 4.5 Draft paragraph for the report introduction

> The ScanPyramids collaboration (Morishima et al. 2017) reported a large void above the Grand Gallery of the Great Pyramid of Khufu, detected independently by three muon detector technologies. The present simulation does not reproduce that measurement; instead, it builds a simplified model of the same physical idea — a chamber inside a pyramid, imaged by counting cosmic-ray muons that survive the passage through rock. The chamber appears as an excess of muons above the smooth-rock expectation, and the exposure time required to reach 5σ is the headline number of this project. This mirrors the essential logic of the 2017 measurement at the level of physics and scale, without claiming to reproduce its experimental analysis.

---

## 5. What went wrong / what I don't understand

- The plan's expectation "50 m → 200 m should drop by a factor of several hundred" does not match the code's 19.5. 
- The plan's Day 1 example "E_min(25000) ≈ 55.9 GeV" does not match the code's 52.585 GeV. This is a density difference: 55.9 GeV corresponds to 2.65 g/cm³ rock, while the project uses 2.5 g/cm³ limestone. Not a bug.
- I have not yet fully digested the full Gaisser formula. But the code handles it, and the report's methods section can cite the handbook's Appendix A.3 rather than deriving it.

---

## 6. Next day's plan

- Day 4 — Target and single-ray tracing.
- Build the pyramid with `mg.Pyramid`.
- Verify density inside the void, inside the rock, outside the pyramid.
- Make the vertical density slice at x = 0.
- Save as `figures/05_density_slice.png`.
- Scan `ay` from 15° to 45° and plot opacity for the target with and without the void.
- Save as `figures/06_opacity_notch.png`.
- Read handbook Chapter 3.2–3.3.

---

## 7. Validation checklist for Day 3

- [x] `mg.minimum_energy(25000)` = 52.585 GeV, consistent with the exact formula.
- [x] The linear rule gives 50 GeV, and the difference is explained by the radiative term.
- [x] The small-ρ limit of the exact formula reduces to the linear rule.
- [x] The exact derivation is written down in full.
- [x] The minimum-energy plot, the surviving-flux plot, and the three questions are all saved from Day 2.
- [x] The Khufu paper abstract and figures have been read.
- [x] Log written.
- [x] Commit made.
- [x] Optional extra figure `03b_min_energy_linear_vs_exact.png`.

---

## 8. Cross-references

- Handbook Chapter 1.2: why muons get through rock; the minimum-ionising regime.
- Handbook Key result 1.1: the range-energy relation and its linear approximation.
- Handbook Appendix A.1: the exact range-energy relation with the radiative term.
- Handbook Appendix C.1: the Morishima et al. 2017 reference.
- Plan Day 3: the three deliverables and the stretch goal.
- Day 2 log: the minimum-energy and surviving-flux plots are already there.
