"""Student-owned analysis functions for Seeing Through Solid Rock.

Notebook 02: implement opacity_map.
Notebook 03: implement expected_counts.
These functions live here rather than inside individual notebooks so every
notebook can be restarted and run independently after the student's work is
complete.
"""

import numpy as np
import muography as mg
from project_config import (
    DETECTOR_AREA_M2, FIELD_DEG, STEP_DEG, RAY_STEP_M,
)


def opacity_map(target, detector, field_deg=FIELD_DEG, step_deg=STEP_DEG,
                ray_step=RAY_STEP_M):
    """Return opacity map and angular grids for the chosen viewing field.

    TODO (Notebook 02): build ax/ay grids, trace one ray per direction, and
    return ``opacity, ax_deg, ay_deg`` where the angle grids are in degrees.
    """


    half_field = field_deg / 2.0
    ax_range = np.arange(-half_field, half_field + step_deg, step_deg)
    ay_range = np.arange(-half_field, half_field + step_deg, step_deg)

    ax_deg, ay_deg = np.meshgrid(ax_range,ay_range)

    opacity = np.zeros_like (ax_deg, dtype=float)

    for i in range (opacity.shape[0]):
        for j in range(opacity.shape[1]):
            ax_rad = np.radians (ax_deg[i,j])
            ay_rad = np.radians(ay_deg[i,j])

            direction = mg.direction_from_angles(ax_rad,ay_rad)

            opacity[i,j] = mg.trace_one_ray(target, detector, direction, step=ray_step)

    return opacity, ax_deg, ay_deg
    


def expected_counts(target, detector, days, area=DETECTOR_AREA_M2,
                    field_deg=FIELD_DEG, step_deg=STEP_DEG,
                    ray_step=RAY_STEP_M):
    """Return expected muon counts per angular pixel.

    TODO (Notebook 03): call opacity_map, convert each direction to a zenith
    angle, use mg.transmitted_flux, multiply by detector area, pixel solid
    angle and exposure time, and return counts plus angle grids.
    """
    raise NotImplementedError("Implement expected_counts in notebook 03.")
