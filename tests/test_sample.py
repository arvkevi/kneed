import math
import numpy as np
import pytest
from kneed.data_generator import DataGenerator
from kneed.knee_locator import KneeLocator

x = np.arange(0, 10)
y_convex_inc = np.array([1, 2, 3, 4, 5, 10, 15, 20, 40, 100])
y_convex_dec = np.array(y_convex_inc[::-1])
y_concave_dec = np.array(100 - y_convex_inc)
y_concave_inc = np.array(100 - y_convex_dec)
x_bumpy = list(range(90))
y_bumpy = [7305., 6979., 6666.6, 6463.2, 6326.5, 6048.8, 6032.8, 5762.,
           5742.8, 5398.2, 5256.8, 5227., 5001.7, 4942., 4854.2, 4734.6,
           4558.7, 4491.1, 4411.6, 4333., 4234.6, 4139.1, 4056.8, 4022.5,
           3868., 3808.3, 3745.3, 3692.3, 3645.6, 3618.3, 3574.3, 3504.3,
           3452.4, 3401.2, 3382.4, 3340.7, 3301.1, 3247.6, 3190.3, 3180.,
           3154.2, 3089.5, 3045.6, 2989., 2993.6, 2941.3, 2875.6, 2866.3,
           2834.1, 2785.1, 2759.7, 2763.2, 2720.1, 2660.1, 2690.2, 2635.7,
           2632.9, 2574.6, 2556., 2545.7, 2513.4, 2491.6, 2496., 2466.5,
           2442.7, 2420.5, 2381.5, 2388.1, 2340.6, 2335., 2318.9, 2319.,
           2308.2, 2262.2, 2235.8, 2259.3, 2221., 2202.7, 2184.3, 2170.1,
           2160., 2127.7, 2134.7, 2102., 2101.4, 2066.4, 2074.3, 2063.7,
           2048.1, 2031.9]


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_figure2(interp_method):
    """From the kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.figure2()
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method=interp_method)
    assert math.isclose(kl.knee, 0.22, rel_tol=0.05)


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_NoisyGaussian(interp_method):
    """From the Kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.noisy_gaussian(mu=50, sigma=10, N=10000)
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method=interp_method)
    assert math.isclose(kl.knee, 60.5, rel_tol=7.0)


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing(interp_method):
    """test a concave increasing function"""
    kn = KneeLocator(x, y_concave_inc, curve='concave', interp_method=interp_method)
    assert kn.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing(interp_method):
    """test a concave decreasing function"""
    kn = KneeLocator(x, y_concave_dec, curve='concave',
                     direction='decreasing', interp_method=interp_method)
    assert kn.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing(interp_method):
    """test a convex increasing function"""
    kn = KneeLocator(x, y_convex_inc, curve='convex', interp_method=interp_method)
    assert kn.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing(interp_method):
    """test a convex decreasing function"""
    kn = KneeLocator(x, y_convex_dec, curve='convex',
                     direction='decreasing', interp_method=interp_method)
    assert kn.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing_truncated(interp_method):
    """test a truncated concave increasing function"""
    kn = KneeLocator(x[:-3] / 10, y_concave_inc[:-3] / 10,
                     curve='concave', interp_method=interp_method)
    assert kn.knee == 0.2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing_truncated(interp_method):
    """test a truncated concave decreasing function"""
    kn = KneeLocator(x[:-3] / 10, y_concave_dec[:-3] / 10,
                     curve='concave', direction='decreasing', interp_method=interp_method)
    assert kn.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing_truncated(interp_method):
    """test a truncated convex increasing function"""
    kn = KneeLocator(x[:-3] / 10, y_convex_inc[:-3] / 10,
                     curve='convex', interp_method=interp_method)
    assert kn.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing_truncated(interp_method):
    """test a truncated convex decreasing function"""
    kn = KneeLocator(x[:-3] / 10, y_convex_dec[:-3] / 10,
                     curve='convex', direction='decreasing', interp_method=interp_method)
    assert kn.knee == 0.2


@pytest.mark.parametrize("interp_method, expected", [
    ('interp1d', 53),
    ('polynomial', 28)
])
def test_convex_decreasing_bumpy(interp_method, expected):
    """test a bumpy convex decreasing function"""
    kn = KneeLocator(x_bumpy, y_bumpy, curve='convex',
                     direction='decreasing', interp_method=interp_method)
    assert kn.knee == expected

def test_gamma():
    n = 6000
    x = range(1, n + 1)
    y = sorted(np.random.gamma(0.5, 1.0, n), reverse=True)
    kn = KneeLocator(x, y, curve='convex', direction='decreasing')
    assert math.isclose(kn.knee, 1000, abs_tol=500.0)


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
        kl_sine = KneeLocator(x, y_sin, S=1, direction=direction, curve=curve)
        detected_knees.extend(kl_sine.all_knees)
    assert np.isclose(expected_knees, detected_knees).all()