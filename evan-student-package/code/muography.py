"""
muography.py
============

Toolkit for the project "Seeing Through Solid Rock: Finding a Hidden Chamber
with Cosmic-Ray Muons".

These are the pieces you are GIVEN. You do not need to modify anything in this
file. Your own work happens in ``student_analysis.py`` and the notebooks.
The small analysis utilities here are fixed so that all students use the same
statistical definitions.

Everything here is deliberately written in a plain, readable style rather than
the fastest possible style.

Units used throughout
---------------------
    energy      GeV
    length      metres (m) for geometry
    density     g/cm^3
    opacity     g/cm^2      (density x path length -- "how much stuff")
    flux        muons per m^2 per second per steradian
    angle       radians internally, degrees in plots

Author: Muon Physics Group, Tsung-Dao Lee Institute, SJTU
"""

import numpy as np

# --------------------------------------------------------------------------
# Physical constants and standard values
# --------------------------------------------------------------------------

RHO_STANDARD_ROCK = 2.65      # g/cm^3, the geologists' "standard rock"
RHO_LIMESTONE = 2.5           # g/cm^3, roughly, for Malaysian karst
RHO_AIR = 0.0012              # g/cm^3, i.e. essentially nothing

A_LOSS = 2.0e-3               # GeV cm^2/g   ionisation energy loss
B_LOSS = 4.0e-6               # cm^2/g       radiative energy loss


# --------------------------------------------------------------------------
# 1. The muon energy spectrum at sea level  (the Gaisser parametrisation)
# --------------------------------------------------------------------------

def gaisser_flux(E, theta):
    """
    Differential muon flux at sea level.

    How many muons arrive per m^2, per second, per steradian, per GeV of
    energy, at energy E and zenith angle theta.

    Parameters
    ----------
    E : float or array
        Muon energy in GeV.
    theta : float or array
        Zenith angle in radians. theta = 0 is straight overhead.

    Returns
    -------
    dI/dE in  muons m^-2 s^-1 sr^-1 GeV^-1

    Notes
    -----
    This is a standard formula from the Particle Data Group, with the
    low-energy correction of Guan et al. (2015). It is a fit to measurements,
    not something derived from first principles. Without the correction the
    original formula badly over-predicts below about 10 GeV; with it, the
    whole range is usable. For us the high-energy end matters most anyway,
    because a muon needs tens of GeV just to get through rock.
    """
    E = np.asarray(E, dtype=float)
    ct = np.cos(np.asarray(theta, dtype=float))
    ct = np.clip(ct, 0.05, 1.0)          # guard against the horizon

    # Low-energy correction: muons below ~10 GeV lose energy in the
    # atmosphere itself, which flattens the spectrum.
    E_eff = E * (1.0 + 3.64 / (E * ct ** 1.29))

    term1 = 1.0 / (1.0 + 1.1 * E * ct / 115.0)
    term2 = 0.054 / (1.0 + 1.1 * E * ct / 850.0)

    # 0.14 E^-2.7 is in cm^-2; the 1e4 converts cm^-2 -> m^-2
    return 1.0e4 * 0.14 * E_eff ** (-2.7) * (term1 + term2)


def integrated_flux(E_min, theta, n_points=400, E_max=1.0e6):
    """
    Total flux of muons with energy ABOVE E_min, arriving at zenith angle theta.

    This is the integral of gaisser_flux from E_min to infinity, done
    numerically. Works on arrays: give it 4000 values of E_min and 4000 values
    of theta and it will return 4000 answers.

    Returns
    -------
    muons m^-2 s^-1 sr^-1
    """
    scalar_input = (np.ndim(E_min) == 0) and (np.ndim(theta) == 0)

    E_min = np.atleast_1d(np.asarray(E_min, dtype=float))
    theta = np.atleast_1d(np.asarray(theta, dtype=float))
    E_min, theta = np.broadcast_arrays(E_min, theta)
    shape = E_min.shape

    E_min_flat = np.maximum(E_min.ravel(), 1.0)
    theta_flat = theta.ravel()

    # One shared logarithmic energy grid, from the smallest threshold upward.
    E_lo = max(E_min_flat.min() * 0.5, 0.5)
    grid = np.logspace(np.log10(E_lo), np.log10(E_max), n_points)

    dI = gaisser_flux(grid[None, :], theta_flat[:, None])   # (rays, energies)

    # Only count the part of the spectrum above each ray's own threshold.
    mask = grid[None, :] >= E_min_flat[:, None]
    integrand = np.where(mask, dI, 0.0)

    result = np.trapezoid(integrand, grid, axis=1).reshape(shape)
    return float(result.reshape(())) if scalar_input else result


# --------------------------------------------------------------------------
# 2. Getting through rock
# --------------------------------------------------------------------------

def minimum_energy(opacity):
    """
    The energy a muon needs in order to survive a given opacity of rock.

    A muon loses energy at a rate  dE/dX = a + b*E  per g/cm^2 travelled.
    The 'a' term is ionisation (it dominates at low energy); the 'b' term is
    radiation (it takes over above a few hundred GeV). Solving that little
    differential equation gives the formula below.

    Parameters
    ----------
    opacity : float or array
        Amount of material along the path, in g/cm^2.

    Returns
    -------
    E_min in GeV.

    Quick sanity check: 1 m of standard rock is 265 g/cm^2, which needs about
    0.53 GeV. 100 m of rock needs about 56 GeV. 500 m needs about 350 GeV.
    """
    X = np.asarray(opacity, dtype=float)
    return (A_LOSS / B_LOSS) * (np.exp(B_LOSS * X) - 1.0)


def transmitted_flux(opacity, theta):
    """
    Flux of muons that survive a given opacity, arriving at zenith angle theta.

    This is just the two functions above, chained together. It is the single
    most important quantity in muography.

    Returns
    -------
    muons m^-2 s^-1 sr^-1
    """
    return integrated_flux(minimum_energy(opacity), theta)


def opacity_from_thickness(thickness_m, density=RHO_STANDARD_ROCK):
    """Convert a thickness in metres into an opacity in g/cm^2."""
    return np.asarray(thickness_m, dtype=float) * 100.0 * density


# --------------------------------------------------------------------------
# 3. The target: a pyramid with a hidden chamber inside it
# --------------------------------------------------------------------------

class Pyramid:
    """
    A square-based pyramid sitting on the ground, with an optional spherical
    void hidden inside it.

    The defaults are roughly the Great Pyramid of Khufu: 230 m along the base,
    139 m tall, built of limestone.

    Coordinates
    -----------
        x, y : horizontal, in metres, with (0, 0) at the centre of the base
        z    : height above the ground, in metres
    """

    def __init__(self,
                 base=230.0,
                 height=139.0,
                 density=RHO_LIMESTONE,
                 void_centre=(0.0, 0.0, 70.0),
                 void_radius=10.0,
                 has_void=True):
        self.base = base
        self.height = height
        self.density = density
        self.void_centre = np.array(void_centre, dtype=float)
        self.void_radius = float(void_radius)
        self.has_void = has_void

    def density_at(self, x, y, z):
        """
        The density (g/cm^3) at any point in space. Works on arrays.

        Outside the pyramid: air (essentially zero).
        Inside the void:     air.
        Everywhere else:     rock.
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        z = np.asarray(z, dtype=float)

        half = 0.5 * self.base
        # The pyramid narrows linearly with height.
        half_at_z = half * (1.0 - np.clip(z, 0.0, self.height) / self.height)

        inside = (z >= 0.0) & (z <= self.height) & \
                 (np.abs(x) <= half_at_z) & (np.abs(y) <= half_at_z)

        rho = np.where(inside, self.density, RHO_AIR)

        if self.has_void:
            cx, cy, cz = self.void_centre
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            rho = np.where(r2 <= self.void_radius ** 2, RHO_AIR, rho)

        return rho

    def without_void(self):
        """A copy of this pyramid with the chamber filled in (solid rock)."""
        twin = Pyramid(self.base, self.height, self.density,
                       self.void_centre, self.void_radius, has_void=False)
        return twin


# --------------------------------------------------------------------------
# 4. Ray tracing  (this is the piece you are given -- see notebook 02)
# --------------------------------------------------------------------------

def trace_one_ray(target, origin, direction, max_length=600.0, step=0.25):
    """
    Send ONE muon path through the target and add up the material it meets.

    We walk along the ray in small steps, ask the target how dense it is at
    each step, and keep a running total. This is called "ray marching".

    Parameters
    ----------
    target : Pyramid
        Anything with a .density_at(x, y, z) method.
    origin : (3,) array
        Where the ray starts, in metres. This is the detector position.
    direction : (3,) array
        Which way the ray points. Does not need to be a unit vector.
    max_length : float
        How far to walk, in metres.
    step : float
        Step size in metres. Smaller = more accurate but slower.

    Returns
    -------
    opacity in g/cm^2
    """
    origin = np.asarray(origin, dtype=float)
    direction = np.asarray(direction, dtype=float)
    direction = direction / np.linalg.norm(direction)

    t = np.arange(0.0, max_length, step)
    points = origin[None, :] + t[:, None] * direction[None, :]

    rho = target.density_at(points[:, 0], points[:, 1], points[:, 2])

    # sum of density * step-length, converted from metres to centimetres
    return float(np.sum(rho) * step * 100.0)


def direction_from_angles(ax, ay):
    """
    Turn two small pointing angles into a direction vector.

    Think of the detector as a camera lying on its back, looking straight up.
    ax tilts the view east-west, ay tilts it north-south. Both in radians.

    Returns an array of shape (..., 3).
    """
    ax = np.asarray(ax, dtype=float)
    ay = np.asarray(ay, dtype=float)
    dx = np.tan(ax)
    dy = np.tan(ay)
    dz = np.ones_like(dx)
    v = np.stack([dx, dy, dz], axis=-1)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def zenith_from_direction(direction):
    """Zenith angle (radians) of a direction vector, measured from straight up."""
    d = np.asarray(direction, dtype=float)
    return np.arccos(np.clip(d[..., 2], -1.0, 1.0))


# --------------------------------------------------------------------------
# 5. Small conveniences
# --------------------------------------------------------------------------

DAY = 86400.0          # seconds in a day


def pixel_solid_angle(angle_step_rad):
    """
    Solid angle covered by one pixel of the image, in steradians.

    For small pixels this is just (angular width) x (angular height).
    """
    return angle_step_rad ** 2


def poisson_counts(expected, rng=None):
    """
    Turn an expected number of muons into a real (whole-number, random) count.

    Nature does not deliver exactly the expected number. It delivers a random
    number drawn from a Poisson distribution whose average is the expected
    number. This one line is the difference between a simulation and a
    daydream.
    """
    if rng is None:
        rng = np.random.default_rng()
    return rng.poisson(np.maximum(expected, 0.0))


def significance(observed, expected_no_void):
    """
    How surprising is the observed count, if there were NO chamber?

    Measured in "sigma" -- the number of standard deviations. Physicists
    conventionally discuss 3 sigma and 5 sigma as increasingly stringent
    thresholds. In this project, 5 sigma is a predefined headline threshold
    for the simplified educational model; it is not by itself a claim about
    a real experiment. For a Poisson count the standard deviation is
    sqrt(expected).
    """
    expected_no_void = np.maximum(np.asarray(expected_no_void, dtype=float), 1e-9)
    return (observed - expected_no_void) / np.sqrt(expected_no_void)


def expected_significance(expected_with_void, expected_no_void):
    """Expected significance for the simplified project model.

    This compares two expectation maps, so it is deterministic for fixed
    inputs. It defines the smooth sensitivity curve used for the headline
    exposure-time estimate. It is deliberately distinct from ``significance``,
    which takes one noisy observation.
    """
    expected_no_void = np.maximum(np.asarray(expected_no_void, dtype=float), 1e-9)
    expected_with_void = np.asarray(expected_with_void, dtype=float)
    return (expected_with_void - expected_no_void) / np.sqrt(expected_no_void)
