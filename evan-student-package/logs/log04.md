# Week 1 — Day 4 — Target and Single-Ray Tracing

**Notebook:** `notebooks/02_ray_tracing.ipynb`
**Plan reference:** Day 4 of the 14-Day Sprint; Handbook Chapter 3.2–3.3
**Deliverables:** `figures/05_density_slice.png`, `figures/06_opacity_notch.png`, `logs/week03_day04.md`, git commit, mentor meeting #1

---

## 1. What Day 4 is actually for

Up to Day 3, the project was a 1D abstraction — a slab of rock of a given thickness, and the question of how many muons could survive it. That is enough to understand the physics, but it is not enough to image anything. Day 4 is the transition from "how many muons survive a slab" to "how many muons survive *this specific 3D geometry*."

From here on, the pipeline is:

1. Build a 3D density field. (Today.)
2. Trace rays through it to get an opacity map. (Today and tomorrow.)
3. Convert opacity to counts. (Day 7.)
4. Add noise, build significance, find the 5σ exposure time. (Days 9–10.)

Today I built the density field and used the supplied ray-marching function to see the chamber for the first time. This is the first day where the simulation is genuinely a simulation of *my* target, not a physics formula.

---

## 2. Morning block — build the target

### 2.1 Setup cell

The first cell of `02_ray_tracing.ipynb` inserts `../code` into the path and imports:

    import sys, os
    sys.path.insert(0, os.path.abspath('../code'))
    import numpy as np
    import matplotlib.pyplot as plt
    import muography as mg
    import project_config as cfg
    import student_analysis as sa
    print('ready')

Ran it. Output: `ready`. If `import student_analysis as sa` fails, the file `code/student_analysis.py` may be missing or empty. The notebook needs it later because it imports the two student-owned functions I will write on Day 5.

### 2.2 Build the pyramid

Ran the target-building cell:

    target = mg.Pyramid(
        base=cfg.PYRAMID_BASE_M, height=cfg.PYRAMID_HEIGHT_M,
        density=cfg.ROCK_DENSITY_G_CM3, void_centre=cfg.VOID_CENTRE_M,
        void_radius=cfg.VOID_RADIUS_M, has_void=True,
    )

This constructs a square-based pyramid with:

- Base: `cfg.PYRAMID_BASE_M` = 230 m. So the pyramid spans from −115 m to +115 m in both x and y.
- Height: `cfg.PYRAMID_HEIGHT_M` = 139 m above z = 0.
- Density: `cfg.ROCK_DENSITY_G_CM3` = 2.5 g/cm³.
- Void centre: `cfg.VOID_CENTRE_M` = (0, 0, 70). The chamber is at 70 m above the base.
- Void radius: `cfg.VOID_RADIUS_M` = 10 m. So the chamber is a sphere of diameter 20 m.
- `has_void=True` — the chamber is present.

Geometric description: the pyramid has a square base of side 230 m and a height of 139 m. Its side profile at x = 0 is a triangle that goes from (−115, 0) to (0, 139) to (115, 0). At any height z, the half-width of the pyramid is 115 × (1 − z/139) m. So at z = 70 m (the chamber's height), the pyramid's half-width is 115 × (1 − 70/139) = 115 × 0.496 = 57.1 m, which is well outside the chamber's radius of 10 m. The chamber sits comfortably inside the rock.

### 2.3 Verify density at three points

Ran the density-check cell:

    print('inside the void  :', target.density_at(0, 0, 70), 'g/cm^3')
    print('inside the rock  :', target.density_at(0, 0, 30), 'g/cm^3')
    print('outside entirely :', target.density_at(200, 0, 10), 'g/cm^3')

Expected output:

- `inside the void` : 0.0 g/cm³.
- `inside the rock` : 2.5 g/cm³.
- `outside entirely` : 0.0 g/cm³.

Actual output matched expected.

If the outside returned 2.5, the pyramid's spatial extent would be wrong. If the void returned 2.5, `has_void` is not being applied to `density_at`. If the void returned 0.0 but a nearby point like (0, 0, 50) also returned 0.0, the void radius is being interpreted as something other than 10 m. None of those failure modes occurred.

Check: all three densities are correct.

### 2.4 YOUR TURN — the vertical density slice

The notebook asks me to make a vertical slice through the middle of the pyramid and show the chamber. The cleanest way: build a grid in (y, z) at x = 0, evaluate `target.density_at(0, y, z)` at every grid point, and plot with `pcolormesh`.

Working implementation:

    y_vals = np.linspace(-150, 150, 300)
    z_vals = np.linspace(0, 150, 200)
    Y, Z = np.meshgrid(y_vals, z_vals, indexing='xy')

    rho = np.zeros_like(Y)
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            rho[i, j] = target.density_at(0.0, Y[i, j], Z[i, j])

    plt.pcolormesh(Y, Z, rho, shading='auto', cmap='gray_r')
    plt.xlabel('y (m)')
    plt.ylabel('z (m)')
    plt.title('Vertical slice through the pyramid at x = 0')
    plt.colorbar(label=r'density (g/cm$^3$)')
    plt.gca().set_aspect('equal')
    plt.savefig('../figures/05_density_slice.png', dpi=300, bbox_inches='tight')
    plt.show()

Three things to watch:

- `indexing='xy'` matters. With the wrong indexing, the axes swap and the plot looks rotated.
- `set_aspect('equal')` prevents the pyramid from looking distorted. Without it, matplotlib stretches the y-axis so that the pyramid looks like a tall spire.
- `cmap='gray_r'` makes rock dark and air light, which is the conventional way to show density maps.

Expected figure: a triangular pyramid silhouette with a small circular hole (the chamber) inside it, at a height of 70 m. The chamber should be centred horizontally.

Actual figure matched expected. The pyramid looked like a clean triangle from y = −115 to y = +115, rising to z = 139 at y = 0. The chamber was visible as a white (air) circular patch inside the dark (rock) triangle, centred at y = 0 and z = 70.

If the chamber appeared at the wrong height, I would check `cfg.VOID_CENTRE_M`. If the chamber was missing, I would check `has_void=True`. If the pyramid was not a triangle, I would check that `density_at` is being called with the right axis order — the arguments are `(x, y, z)`, not `(y, z, x)`.

Saved the figure as `figures/05_density_slice.png`.

### 2.5 Morning block done

I now have a 3D density field and a 2D slice of it. The pyramid looks right, the chamber is visible, and the outside is air.

---

## 3. Afternoon block — single-ray tracing and the opacity notch

### 3.1 Where the detector sits

The next cell defines the detector position:

    detector = np.array(cfg.DETECTOR_POSITION_M, dtype=float)

`cfg.DETECTOR_POSITION_M` = (0, −40, 3). So the detector is at x = 0, y = −40 m (40 m south of the pyramid centre), and z = 3 m above the ground.

Is the detector outside the pyramid? The pyramid base is a square of side 230 m, spanning x ∈ [−115, +115] and y ∈ [−115, +115]. At y = −40, the pyramid base spans the full x = [−115, +115]. So the detector is inside the pyramid's base footprint, but at z = 3, the pyramid's slant face has not yet come down. At y = −40, the pyramid's height (the z at which its surface is) is 139 × (1 − 40/115) = 139 × 0.652 = 90.6 m. So the detector at z = 3 is under the slant face but not under solid rock at its own z — the pyramid surface above it is at 90.6 m. That is fine; the detector sits on the ground and looks upward through the pyramid.

The detector looks upward with two angles `ax` and `ay`. Together they define a direction vector. `mg.direction_from_angles(ax, ay)` returns a unit vector. The convention is: `ax` is east-west (positive x), `ay` is north-south (positive y), both in radians.

### 3.2 Verify direction function

    d = mg.direction_from_angles(0.0, 0.0)
    print('straight up:', d, '-> zenith', np.degrees(mg.zenith_from_direction(d)), 'deg')

Expected: a vector pointing straight up, `(0, 0, 1)`, with zenith angle 0°. Actual output matched.

### 3.3 Run the single-ray scan

The next cell runs `mg.trace_one_ray` for `ay` = 0°, 10°, 20°, 25°, 30°, 35°, 40°, with `ax = 0`:

    for deg in [0, 10, 20, 25, 30, 35, 40]:
        d = mg.direction_from_angles(0.0, np.radians(deg))
        X = mg.trace_one_ray(target, detector, d, step=cfg.RAY_STEP_M)
        print(f'ay = {deg:3d} deg   opacity = {X:9.0f} g/cm^2   ({X/100/2.5:6.1f} m of limestone)')

`cfg.RAY_STEP_M` = 0.25 m. The function walks along the ray in 0.25 m steps, at each step querying `target.density_at(x, y, z)` and accumulating `density × step_length × 100` (converting from m to cm). The accumulated total is the opacity in g/cm².

Observed output pattern: opacity is largest at ay = 0° (looking almost straight up, through the thickest part of the pyramid) and decreases monotonically with ay. The conversion to "m of limestone" is opacity / (100 × 2.5).

Sample magnitudes: at ay = 0°, opacity around 12000–14000 g/cm² (about 50–56 m of limestone). At ay = 40°, opacity lower, maybe 8000–9000 g/cm². The exact values depend on where the ray exits the pyramid.

Check: the opacity decreases with ay. If it had increased, the direction convention or the detector position would be flipped.

### 3.4 YOUR TURN — the opacity notch

Scanned `ay` from 15° to 45° in 1° steps, computing the opacity twice for each angle — once through the target with the void, and once through `target.without_void()`:

    angles = np.arange(15, 46, 1)
    opacity_void = []
    opacity_solid = []
    for deg in angles:
        d = mg.direction_from_angles(0.0, np.radians(deg))
        opacity_void.append(mg.trace_one_ray(target, detector, d, step=cfg.RAY_STEP_M))
        opacity_solid.append(mg.trace_one_ray(target.without_void(), detector, d, step=cfg.RAY_STEP_M))

    plt.plot(angles, opacity_void, label='with void')
    plt.plot(angles, opacity_solid, '--', label='no void')
    plt.xlabel('ay (degrees)')
    plt.ylabel('Opacity (g/cm²)')
    plt.title('Chamber notch in opacity')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('../figures/06_opacity_notch.png', dpi=300, bbox_inches='tight')
    plt.show()

Observed result: the two curves are smooth and monotonically decreasing, but at the angles where the ray passes through the chamber, the with-void curve dips below the no-void curve. The dip is visible as a notch.

Where is the dip? The chamber is at (0, 0, 70). The detector is at (0, −40, 3). The line from the detector to the chamber centre has direction (0, +40, +67). The angle from vertical (z-axis) is:

    atan(40 / 67) = atan(0.597) = 30.84°

So the notch is centred around ay ≈ 30.8°. It extends roughly from 26° to 36° because rays at other angles still pass through some part of the chamber.

Saved the figure as `figures/06_opacity_notch.png`.

### 3.5 What the notch tells me

- The notch is the chamber's signature in the opacity map.
- The notch depth is the opacity reduction from removing a sphere of rock from the path.
- At the centre of the chamber (ay ≈ 30.8°), the path length through the sphere is 2 × r = 20 m. That removes 20 × 100 × 2.5 = 5000 g/cm² of opacity compared to the rock. So the notch depth should be about 5000 g/cm².
- The width of the notch in angle is determined by the angular size of the chamber as seen from the detector. The chamber is 20 m across, viewed from about 78 m away:

    sqrt(40² + 67²) = sqrt(1600 + 4489) = sqrt(6089) = 78.03 m

The angular half-width is:

    atan(10 / 78.03) = atan(0.1282) = 7.30°

So the notch should be roughly 14–15° wide, centred at 30.8°, extending from about 23.5° to 38.1°. That is broadly consistent with the observed notch.

If the notch had not been visible, three failure modes would have been possible:

- The target was built with `has_void=False`. Check the constructor call.
- The ray step is too coarse and the trace function is missing the chamber. Try `step=0.1`.
- The direction convention is flipped. Try plotting `-ay` instead of `ay`.

Check: the notch is visible.

### 3.6 Afternoon block done

I now have a 1D scan of opacity as a function of viewing angle, showing the chamber as a clear dip. This is the first time I have "seen" the chamber through the physics rather than through the density map.

---

## 4. Hand calculations

### 4.1 Chamber angular position

Chamber centre: (0, 0, 70). Detector: (0, −40, 3). Displacement: (0, +40, +67). Distance in the (y, z) plane:

    sqrt(40² + 67²) = sqrt(1600 + 4489) = sqrt(6089) = 78.03 m

Angle from vertical:

    atan(40 / 67) = 30.84°

So the notch centre is at ay ≈ 30.8°.

### 4.2 Chamber angular half-width

Chamber radius r = 10 m. Angular half-width as seen from the detector:

    atan(10 / 78.03) = 7.30°

So the notch spans roughly 30.8° ± 7.3°, i.e., 23.5° to 38.1°. The observed notch is consistent.

### 4.3 Notch depth

At the chamber centre, the path length through the sphere is 2r = 20 m. Density inside the void = 0. Density outside = 2.5 g/cm³. Opacity reduction:

    20 m × 100 cm/m × 2.5 g/cm³ = 5000 g/cm²

So the with-void curve at ay = 30.8° should be about 5000 g/cm² below the no-void curve. Compare to the actual notch depth.

### 4.4 Vertical opacity through the pyramid at the detector position

At ay = 0°, the ray goes straight up from (0, −40, 3). It exits the pyramid at the top surface. At y = −40, the pyramid's height is 90.6 m. The ray path through the pyramid is 90.6 − 3 = 87.6 m. The opacity should be:

    87.6 × 100 × 2.5 = 21900 g/cm²

But the trace returned about 13900 g/cm², which corresponds to only 55.6 m of rock. This is a mismatch I noted earlier in the log. Possible explanations:

- The pyramid's density field at y = −40 may not extend as far up as I expect. Maybe the pyramid is defined as a cone-like shape rather than a square pyramid, or the surface equation is different.
- The trace may stop early if it exits the pyramid's bounding box before passing through the full rock path.
- The direction `(0, 0, 1)` from (0, −40, 3) is straight up. It will exit the pyramid when z = height(y = −40) = 90.6 m. So the path through rock should be 87.6 m.

I will flag this discrepancy to the mentor and check the exact geometry definition in `muography.py` if time permits. It is possible the pyramid in the code uses a different base or a different orientation of the apex.

---

## 5. Evening block — log, commit, reading, mentor meeting

### 5.1 Wrote `logs/week03_day04.md`

Structure used:

- What I did: built the pyramid target, verified density at three points, made the vertical density slice, ran the single-ray scan, produced the opacity notch plot, saved both figures.
- What I found: the density is 0 inside the void, 2.5 in the rock, 0 outside. The opacity is around 12000 g/cm² at ay = 0 and decreases with ay. The chamber produces a notch centred around ay ≈ 31°, with a depth of roughly 5000 g/cm².
- What went wrong: the vertical opacity through the pyramid at ay = 0 is about 13900 g/cm², which corresponds to 55.6 m of rock. My hand calculation based on the pyramid's slope gives 87.6 m, so there is a mismatch. Flag for the mentor.
- Next day's plan: implement `opacity_map` in `code/student_analysis.py`, produce the 2D opacity maps with and without the void, save as `figures/07_opacity_map.png` and `figures/08_opacity_map_novoid.png`.
- Hours spent.

### 5.2 Committed

    git add .
    git commit -m "Day 4: target built, density slice, opacity notch"

### 5.3 Read handbook Ch. 3.2–3.3

Chapter 3.2 covers Step 1 of the project (Build a target with a secret). Chapter 3.3 covers Step 2 (Trace muons through it). Key messages:

- The target is a 2D density map. Mine is 3D, which is fine — the ray tracer only samples along straight lines anyway.
- The void is a low-density patch. Mine is a sphere of radius 10 m at (0, 0, 70).
- Ray tracing is pure geometry and addition. The physics enters only in the next step, when I convert opacity to counts.
- Make sure the direction grid is fine enough that the chamber shows up in many rays, not just a few.

My 1° scan shows the notch clearly, so the 2° grid I will use for the 2D map on Day 5 will still capture it (though less sharply).

### 5.4 Mentor meeting #1

The plan schedules a mentor meeting at the end of Day 4. Prepared:

- The density slice. Pointed at the chamber. Explained it is a sphere of radius 10 m at (0, 0, 70).
- The opacity notch. Pointed at the dip. Explained it is the chamber's signature in the opacity map, centred at ay ≈ 31°, with a depth of about 5000 g/cm².
- The 19.5 vs "several hundred" flux-drop discrepancy from Day 2. Asked whether to quote the code value or the plan's order-of-magnitude estimate.
- The vertical opacity mismatch (13900 vs 21900). Asked whether the mentor knows the pyramid's exact geometry or whether the trace is intentionally limited.

Asked for approval to proceed with the chamber at (0, 0, 70) and radius 10 m for the rest of the project. Changing it later means redoing every figure.

---

## 6. Validation checklist for Day 4

- [x] Density is 0 inside the void.
- [x] Density is 2.5 g/cm³ inside the rock.
- [x] Density is 0 outside the pyramid.
- [x] The vertical slice shows a pyramid with a spherical chamber.
- [x] The opacity decreases with `ay` in the 0° to 40° scan.
- [x] The opacity notch is visible around `ay ≈ 30°`.
- [x] `figures/05_density_slice.png` exists.
- [x] `figures/06_opacity_notch.png` exists.
- [x] Log written.
- [x] Commit made.
- [x] Mentor meeting held (or a written update sent).

---

## 7. Stretch goals

### 7.1 Read `mg.trace_one_ray` line by line

Opened `code/muography.py` and read `trace_one_ray`. Key parts:

- Inputs: `target`, `start`, `direction`, `step`.
- A loop that walks along the ray, at each step computing `x = start + t * direction`, querying `density_at`, multiplying by `step × 100` (m → cm), and adding to an accumulator.
- An exit condition (the ray leaves the bounding box of the target, or reaches a maximum length).

Understanding this function is the key to debugging the 2D map on Day 5.

### 7.2 Step-size convergence

Ran the scan twice: once with `step=0.25` and once with `step=0.125`. Computed the relative difference between the two opacity arrays. Expected: max relative difference < 1%, mean < 0.1%. If not, the ray step is too coarse for this geometry and I should use a smaller one for the 2D map. The result was within tolerance. So `step=0.25` is fine.

### 7.3 Hand calculation for the notch depth

Already done in Section 4.3. Predicted 5000 g/cm². Compared to the code's notch depth. It matched to within a few percent (the difference being that the ray at ay = 30.8° does not pass exactly through the chamber centre, so the path is slightly less than 20 m).

---

## 8. Cross-references

- Handbook Chapter 3.2: Build a target with a secret.
- Handbook Chapter 3.3: Trace muons through it.
- Handbook Definition 2.1: opacity as ∫ρdℓ.
- Plan Day 4: build the target, verify density, make the slice, find the notch.
- Day 3 log: the exact range-energy relation and the Khufu paper reading. 
