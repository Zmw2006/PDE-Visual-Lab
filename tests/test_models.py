import numpy as np
import pytest

from pde_visual_lab.models import (
    advection, burgers_foot, burgers_initial, burgers_position,
    gaussian, heat, wave,
)


def test_initial_conditions_and_propagation():
    x = np.linspace(-2, 2, 101)
    np.testing.assert_allclose(advection(x, 0, 1.7), gaussian(x))
    np.testing.assert_allclose(advection(x + 1.7, 1, 1.7), gaussian(x))
    np.testing.assert_allclose(wave(x, 0, 1.2), gaussian(x))
    np.testing.assert_allclose(heat(x, 0, 0.4), np.sin(x) + 0.5 * np.sin(2 * x))


def test_burgers_inverse_before_first_crossing():
    for t in (0, 0.3, 0.95):
        for foot in np.linspace(-2.8, 2.8, 13):
            x = float(burgers_position(foot, t))
            assert burgers_foot(x, t) == pytest.approx(foot, abs=1e-12)
            assert float(burgers_initial(foot)) == pytest.approx(-np.sin(foot))


def test_burgers_rejects_nonclassical_time():
    with pytest.raises(ValueError):
        burgers_foot(0, 1.0)
    with pytest.raises(ValueError):
        burgers_foot(0, 1.2)
