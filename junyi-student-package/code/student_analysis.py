"""Shared analysis for Junyi's MYSSP muography notebooks.

The angular grid, exposure scaling and comparison helpers follow Evan Lim's
MYSSP analysis. The maps use the original [row, column] meshgrid layout.
"""

import numpy as np

import muography as mg
from project_config import DETECTOR_AREA_M2, FIELD_DEG, STEP_DEG, RAY_STEP_M


def opacity_map(target, detector, field_deg=FIELD_DEG, step_deg=STEP_DEG,
                ray_step=RAY_STEP_M, max_length=600.0):
    """Return opacity in g/cm² and two angle grids in degrees."""
    detector = np.asarray(detector, dtype=float)
    if detector.shape != (3,):
        raise ValueError("detector must have x, y and z coordinates")
    if field_deg <= 0 or step_deg <= 0 or ray_step <= 0 or max_length <= 0:
        raise ValueError("field, angular step, ray step and length must be positive")

    # Build the grid around zero so we always include the ray straight up.
    n_half = int(round(field_deg / step_deg))
    angles = np.arange(-n_half, n_half + 1, dtype=float) * step_deg
    ax_deg, ay_deg = np.meshgrid(angles, angles, indexing="xy")
    opacity = np.empty_like(ax_deg)

    # Each row changes ay and each column changes ax.
    for iy, ay in enumerate(np.radians(angles)):
        for ix, ax in enumerate(np.radians(angles)):
            direction = mg.direction_from_angles(ax, ay)
            opacity[iy, ix] = mg.trace_one_ray(
                target, detector, direction, max_length=max_length, step=ray_step
            )
    return opacity, ax_deg, ay_deg


def expected_counts(target, detector, days, area=DETECTOR_AREA_M2,
                    field_deg=FIELD_DEG, step_deg=STEP_DEG,
                    ray_step=RAY_STEP_M, max_length=600.0):
    """Trace the target and return expected counts and angle grids."""
    opacity, ax_deg, ay_deg = opacity_map(
        target, detector, field_deg=field_deg, step_deg=step_deg,
        ray_step=ray_step, max_length=max_length,
    )
    counts = counts_from_opacity(opacity, ax_deg, ay_deg, days, area, step_deg)
    return counts, ax_deg, ay_deg


def counts_from_opacity(opacity, ax_deg, ay_deg, days, area=DETECTOR_AREA_M2,
                        step_deg=STEP_DEG):
    """Convert an existing opacity map to expected counts."""
    if days < 0 or area < 0 or step_deg <= 0:
        raise ValueError("days and area must be non-negative and the step positive")
    direction = mg.direction_from_angles(np.radians(ax_deg), np.radians(ay_deg))
    theta = mg.zenith_from_direction(direction)
    flux = mg.transmitted_flux(opacity, theta)

    # Flux is per square metre, steradian and second, so multiply by all three.
    pixel_sr = mg.pixel_solid_angle(np.radians(step_deg))
    return flux * area * pixel_sr * days * mg.DAY


def ratio_map(counts_void, counts_solid):
    """Divide by the solid reference in the same angular bin."""
    return np.asarray(counts_void) / np.maximum(counts_solid, 1e-12)


def signal_pixel(counts_void, counts_solid):
    """Pick the largest expected excess before drawing any random counts."""
    excess = np.asarray(counts_void) - np.asarray(counts_solid)
    return np.unravel_index(np.argmax(excess), excess.shape)


def first_crossing(days, significance, level):
    """Interpolate the first upward threshold crossing in an ordered scan."""
    days = np.asarray(days, dtype=float)
    significance = np.asarray(significance, dtype=float)
    reached = np.flatnonzero(significance >= level)
    if not reached.size:
        return float("nan")
    i = reached[0]
    if i == 0:
        return float(days[0])
    return float(np.interp(level, significance[i-1:i+1], days[i-1:i+1]))


def solid_angle_factor(ax_deg, ay_deg):
    """Tangent-plane correction evaluated at each angular bin's centre."""
    ax, ay = np.radians(ax_deg), np.radians(ay_deg)
    cos_theta = 1 / np.sqrt(1 + np.tan(ax)**2 + np.tan(ay)**2)
    return cos_theta**3 / (np.cos(ax)**2 * np.cos(ay)**2)
