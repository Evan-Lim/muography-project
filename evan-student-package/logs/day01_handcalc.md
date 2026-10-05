# Day 1 — Hand Calculations (Markdown)

## 1. Lorentz factor for a 4 GeV muon

Muon rest mass energy: \(m_\mu c^2 = 105.66\) MeV.

\[
\gamma = \frac{E}{m_\mu c^2} = \frac{4000 \text{ MeV}}{105.66 \text{ MeV}} \approx 37.85
\]

Rounded: \(\gamma \approx 37.9\).

## 2. Time-dilated lifetime

Muon lifetime at rest: \(\tau_\mu \approx 2.2\,\mu s\).

\[
\gamma \tau_\mu \approx 37.9 \times 2.2\,\mu s \approx 83.4\,\mu s
\]

## 3. Distance at speed of light

\[
d = c \gamma \tau_\mu
\]

Using \(c = 3 \times 10^8\) m/s and \(\gamma \tau_\mu = 83.4 \times 10^{-6}\) s:

\[
d \approx 3 \times 10^8 \times 83.4 \times 10^{-6} \approx 25.0 \text{ km}
\]

## 4. Range of a 4 GeV muon

Approximate energy-loss rule: \(R \approx E / 2\) in units of g/cm² when \(E\) is in MeV.

\[
R \approx \frac{4000}{2} = 2000 \text{ g/cm}^2
\]

## 5. Range in rock

Assume rock density \(\rho = 2.65 \text{ g/cm}^3\).

\[
R_{\text{rock}} = \frac{2000}{2.65} \approx 754.7 \text{ cm} \approx 7.5 \text{ m}
\]

## 6. Opacity of 100 m limestone

Take \(\rho_{\text{limestone}} = 2.5 \text{ g/cm}^3\) and thickness \(L = 100 \text{ m} = 10000 \text{ cm}\).

\[
\text{opacity} = \rho_{\text{limestone}} \times L = 2.5 \times 10000 = 25000 \text{ g/cm}^2
\]

## 7. Linear minimum energy

Simple linear estimate: \(E_{\min} \approx 2\rho\) when \(\rho\) is in g/cm² and \(E_{\min}\) is in MeV.

\[
E_{\min} \approx 2 \times 25000 = 50000 \text{ MeV} = 50 \text{ GeV}
\]

## 8. Code minimum energy

Using the project function:

`mg.minimum_energy(25000)`

Your result:

`np.float64(52.58545903782386)`

So the code gives approximately \(52.59\) GeV.

Note: The plan expected roughly \(55.9\) GeV. The difference is likely due to the exact implementation of the radiative term, the constants used in `muography.py`, or the project configuration. The key point is that the code result is higher than the simple linear estimate \(50\) GeV because the full energy-loss equation \(dE/dX = -(a + bE)\) includes the radiative term \(bE\).

## 9. Toy significance

Suppose observed counts \(N_{\text{obs}} = 460\) and background expectation \(N_{\text{bg}} = 400\).

\[
S = \frac{N_{\text{obs}} - N_{\text{bg}}}{\sqrt{N_{\text{bg}}}}
= \frac{460 - 400}{\sqrt{400}}
= \frac{60}{20}
= 3.0
\]

## 10. Double exposure

Double the exposure time, so counts roughly double.

\[
N_{\text{obs}} = 920,\qquad N_{\text{bg}} = 800
\]

\[
S = \frac{920 - 800}{\sqrt{800}}
= \frac{120}{28.284}
\approx 4.24
\]

Check: \(S \propto \sqrt{T}\), so \(3.0 \times \sqrt{2} \approx 4.24\). This matches.

## Summary of hand-calculation results

- \(\gamma(4\text{ GeV}) \approx 37.9\)
- \(\gamma \tau_\mu \approx 83.4\,\mu s\)
- Distance at \(c\): \(\approx 25.0\) km
- Range: \(\approx 2000\) g/cm²
- Range in rock: \(\approx 7.5\) m
- 100 m limestone opacity: \(25000\) g/cm²
- Linear \(E_{\min}\): \(50\) GeV
- Code `mg.minimum_energy(25000)`: \(52.58545903782386\) GeV
- Toy significance: \(S = 3.0\)
- Double exposure: \(S \approx 4.24\)
