import math
import numpy as np
import pytest
from kneed.data_generator import DataGenerator as dg
from kneed.knee_locator import KneeLocator



@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_figure2(interp_method):
    """From the kneedle manuscript"""
    x, y = dg.figure2()
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method=interp_method)
    assert math.isclose(kl.knee, 0.22, rel_tol=0.05)


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_NoisyGaussian(interp_method):
    """From the Kneedle manuscript"""
    x, y = dg.noisy_gaussian(mu=50, sigma=10, N=10000)
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method=interp_method)
    assert math.isclose(kl.knee, 60.5, rel_tol=7.0)


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing(interp_method):
    """test a concave increasing function"""
    x, y = dg.concave_increasing()
    kn = KneeLocator(x, y, curve='concave', interp_method=interp_method)
    assert kn.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing(interp_method):
    """test a concave decreasing function"""
    x, y = dg.concave_decreasing()
    kn = KneeLocator(x, y, curve='concave', direction='decreasing', interp_method=interp_method)
    assert kn.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing(interp_method):
    """test a convex increasing function"""
    x, y = dg.convex_increasing()
    kl = KneeLocator(x, y, curve='convex', interp_method=interp_method)
    assert kl.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing(interp_method):
    """test a convex decreasing function"""
    x, y = dg.convex_decreasing()
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', interp_method=interp_method)
    assert kl.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing_truncated(interp_method):
    """test a truncated concave increasing function"""
    x, y = dg.concave_increasing()
    kl = KneeLocator(x[:-3] / 10, y[:-3] / 10, curve='concave', interp_method=interp_method)
    assert kl.knee == 0.2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing_truncated(interp_method):
    """test a truncated concave decreasing function"""
    x, y = dg.concave_decreasing()
    kl = KneeLocator(x[:-3] / 10, y[:-3] / 10, curve='concave', direction='decreasing', interp_method=interp_method)
    assert kl.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing_truncated(interp_method):
    """test a truncated convex increasing function"""
    x, y = dg.convex_increasing()
    kl = KneeLocator(x[:-3] / 10, y[:-3] / 10, curve='convex', interp_method=interp_method)
    assert kl.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing_truncated(interp_method):
    """test a truncated convex decreasing function"""
    x, y = dg.convex_decreasing()
    kl = KneeLocator(x[:-3] / 10, y[:-3] / 10, curve='convex', direction='decreasing', interp_method=interp_method)
    assert kl.knee == 0.2


@pytest.mark.parametrize("interp_method, expected", [
    ('interp1d', 31),
    ('polynomial', 28)
])
def test_convex_decreasing_bumpy(interp_method, expected):
    """test a bumpy convex decreasing function"""
    x, y = dg.bumpy()
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', interp_method=interp_method)
    assert kl.knee == expected


def test_gamma():
    np.random.seed(23)
    n = 1000
    x = range(1, n + 1)
    y = sorted(np.random.gamma(0.5, 1.0, n), reverse=True)
    kl = KneeLocator(x, y, curve='convex', direction='decreasing')
    assert kl.knee == 43


def test_sensitivity():
    """Test the S parameter -- where S is the number of flat points to identify before calling a knee"""
    np.random.seed(23)
    sensitivity = [1, 3, 5, 10, 100, 200, 400]
    detected_knees = []
    expected_knees = [43, 137, 178, 258, 305, 482, 482]
    n = 1000
    x = range(1, n + 1)
    y = sorted(np.random.gamma(0.5, 1.0, n), reverse=True)
    for s, expected_knee in zip(sensitivity, expected_knees):
        kl = KneeLocator(x, y, curve='convex', direction='decreasing', S=s)
        detected_knees.append(kl.knee)
        assert kl.knee, expected_knee


def test_sine():
    x = np.arange(0, 10, 0.1)
    y_sin = np.sin(x)

    sine_combos =  [
        ('decreasing', 'convex'),
        ('increasing', 'convex'),
        ('increasing', 'concave'),
        ('decreasing', 'concave')
    ]
    expected_knees = [4.5, 4.9, 1.4, 7.7, 8.1, 1.8]
    detected_knees = []
    for direction, curve in sine_combos:
        kl_sine = KneeLocator(x, y_sin, direction=direction, curve=curve, S=1)
        detected_knees.extend(kl_sine.all_knees)
    assert np.isclose(expected_knees, detected_knees).all()
