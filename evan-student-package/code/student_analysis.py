"""Student-owned analysis functions for Seeing Through Solid Rock.

Notebook 02: implement ``opacity_map``.
Notebook 03: implement ``expected_counts``.

These functions live here rather than inside individual notebooks so every
notebook can be restarted and run independently after the student's work is
complete.  Notebooks 03--05 import them from this module, so a fresh kernel
only needs the setup cell at the top of each notebook.

Author: Evan Lim Hong Yan -- MYSSP Project P-1
"""

import numpy as np

import muography as mg
from project_config import (
    DETECTOR_AREA_M2, FIELD_DEG, STEP_DEG, RAY_STEP_M,
)


# --------------------------------------------------------------------------
# Notebook 02 -- geometry: one ray per angular pixel
# --------------------------------------------------------------------------

def angle_grid(field_deg=FIELD_DEG, step_deg=STEP_DEG):
    """Return the one-dimensional pointing-angle grid, in degrees.

    The grid is symmetric about zero and contains zero when ``step_deg``
    divides ``field_deg``.  Both the horizontal angle ``ax`` (east-west) and
    the vertical angle ``ay`` (north-south) use the same grid, so the image is
    square in angle.
    """
    if field_deg <= 0.0:
        raise ValueError("field_deg must be positive")
    if step_deg <= 0.0:
        raise ValueError("step_deg must be positive")

    n_half = int(round(field_deg / step_deg))
    # Build from an integer index so the grid is exactly symmetric and
    # contains 0.0 without floating-point drift.
    idx = np.arange(-n_half, n_half + 1, dtype=float)
    return idx * float(step_deg)


def opacity_map(target, detector, field_deg=FIELD_DEG, step_deg=STEP_DEG,
                ray_step=RAY_STEP_M, max_length=600.0):
    """Return the opacity map and angular grids for the chosen viewing field.

    One ray is traced for every angular pixel.  The returned array is indexed
    ``[iy, ix]``, so ``opacity[iy, ix]`` belongs to the direction
    ``(ax_deg[ix], ay_deg[iy])``.  This is the natural orientation for
    ``plt.pcolormesh(ax_deg, ay_deg, opacity)`` and for ``origin='lower'``.

    Parameters
    ----------
    target : object
        Anything with a ``density_at(x, y, z)`` method, e.g. ``mg.Pyramid``.
    detector : array_like of shape (3,)
        Detector position in metres.
    field_deg : float
        Half-width of the square angular field, in degrees.
    step_deg : float
        Angular pixel size, in degrees.
    ray_step : float
        Ray-marching step length in metres.
    max_length : float
        Maximum distance a ray is followed, in metres.  The default clears the
        baseline pyramid from any detector position used in this project.

    Returns
    -------
    opacity : numpy.ndarray, shape (n_ay, n_ax)
        Opacity in g/cm^2.
    ax_deg : numpy.ndarray
        Horizontal pointing angles in degrees.
    ay_deg : numpy.ndarray
        Vertical pointing angles in degrees.
    """
    detector = np.asarray(detector, dtype=float)
    if detector.shape != (3,):
        raise ValueError("detector must be a three-element position vector")

    ax_deg = angle_grid(field_deg, step_deg)
    ay_deg = angle_grid(field_deg, step_deg)

    opacity = np.empty((ay_deg.size, ax_deg.size), dtype=float)

    for iy, ay in enumerate(ay_deg):
        for ix, ax in enumerate(ax_deg):
            direction = mg.direction_from_angles(np.radians(ax), np.radians(ay))
            opacity[iy, ix] = mg.trace_one_ray(
                target, detector, direction,
                max_length=max_length, step=ray_step,
            )

    return opacity, ax_deg, ay_deg


# --------------------------------------------------------------------------
# Notebook 03 -- physics: opacity -> expected muon counts
# --------------------------------------------------------------------------

def zenith_angles(ax_deg, ay_deg):
    """Zenith angle in radians for every pixel of an angular map.

    ``direction_from_angles`` builds the unit vector

        d = (tan(ax), tan(ay), 1) / norm,

    so ``cos(theta) = 1 / sqrt(1 + tan(ax)^2 + tan(ay)^2)``.  Doing the
    algebra directly avoids constructing a (n_ay, n_ax, 3) direction array.
    """
    ax = np.radians(np.asarray(ax_deg, dtype=float))
    ay = np.radians(np.asarray(ay_deg, dtype=float))
    tan2 = np.tan(ax)[None, :] ** 2 + np.tan(ay)[:, None] ** 2
    cos_theta = 1.0 / np.sqrt(1.0 + tan2)
    return np.arccos(np.clip(cos_theta, -1.0, 1.0))


def expected_counts(target, detector, days, area=DETECTOR_AREA_M2,
                    field_deg=FIELD_DEG, step_deg=STEP_DEG,
                    ray_step=RAY_STEP_M, max_length=600.0):
    """Return expected muon counts per angular pixel.

    For each pixel the calculation is

        counts = flux(opacity, zenith) * area * pixel solid angle * time.

    The flux is the integrated Gaisser spectrum above the minimum energy
    implied by the opacity, computed by ``mg.transmitted_flux``.  The pixel
    solid angle uses the small-angle approximation
    ``Omega = (step_deg in radians)^2``, which is the convention fixed by
    ``mg.pixel_solid_angle``.  At the signal direction (about 30 degrees from
    vertical) this overestimates the exact tangent-plane solid angle by about
    13%, and at the edge of the +-40 degree field by about 23%.  The effect is
    treated as a systematic in notebook 05 and in the report.

    Returns
    -------
    counts : numpy.ndarray, shape (n_ay, n_ax)
        Expected number of muons in each angular pixel.  This is an
        expectation, not an integer; Poisson sampling is a separate step.
    ax_deg : numpy.ndarray
        Horizontal pointing angles in degrees.
    ay_deg : numpy.ndarray
        Vertical pointing angles in degrees.
    """
    if days < 0.0:
        raise ValueError("days must be non-negative")

    opacity, ax_deg, ay_deg = opacity_map(
        target, detector, field_deg=field_deg, step_deg=step_deg,
        ray_step=ray_step, max_length=max_length,
    )

    counts = counts_from_opacity(
        opacity, ax_deg, ay_deg, days, area=area, step_deg=step_deg,
    )
    return counts, ax_deg, ay_deg


# --------------------------------------------------------------------------
# Small shared helpers used by notebooks 03--05 and the reproducibility script
# --------------------------------------------------------------------------

def ratio_map(expected_with_void, expected_without_void):
    """Pixel-by-pixel ratio ``with_void / without_void``.

    This is Key result 3.1: dividing by the twin target removes the shape of
    the pyramid and leaves the chamber as an excess above 1.0.
    """
    num = np.asarray(expected_with_void, dtype=float)
    den = np.maximum(np.asarray(expected_without_void, dtype=float), 1e-12)
    return num / den


def first_crossing(x, y, level):
    """First x at which the monotonic curve ``y(x)`` reaches ``level``.

    Linear interpolation is performed between the two scan points that
    bracket the crossing.  Returns ``numpy.nan`` if the curve never reaches
    the level.  The inputs are sorted by x first, so a decreasing scan is
    handled as well.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    order = np.argsort(x)
    x = x[order]
    y = y[order]

    above = y >= level
    if not np.any(above):
        return float("nan")
    i = int(np.argmax(above))
    if i == 0:
        return float(x[0])
    x0, x1 = x[i - 1], x[i]
    y0, y1 = y[i - 1], y[i]
    if y1 == y0:
        return float(x1)
    return float(x0 + (level - y0) * (x1 - x0) / (y1 - y0))


def counts_from_opacity(opacity, ax_deg, ay_deg, days, area=DETECTOR_AREA_M2,
                        step_deg=STEP_DEG):
    """Convert an existing opacity map into expected counts.

    This is the same arithmetic as :func:`expected_counts`, but it accepts an
    opacity map that has already been computed.  It is useful for exposure
    scans: the geometry is traced once, and only the linear exposure factor
    changes.  Because the expected count is exactly proportional to time,
    re-using one opacity map is not an approximation.
    """
    opacity = np.asarray(opacity, dtype=float)
    theta = zenith_angles(ax_deg, ay_deg)
    flux = mg.transmitted_flux(opacity, theta)
    pixel_sr = mg.pixel_solid_angle(np.radians(step_deg))
    return flux * float(area) * pixel_sr * float(days) * mg.DAY


def signal_pixel(expected_with_void, expected_without_void):
    """Index of the pixel with the largest expected excess.

    The pixel is chosen once, from the noiseless expectation maps, and then
    held fixed for every exposure time.  Choosing a different pixel in each
    noisy map would introduce a selection bias -- see the project sheet.
    """
    excess = np.asarray(expected_with_void) - np.asarray(expected_without_void)
    return np.unravel_index(int(np.argmax(excess)), excess.shape)

