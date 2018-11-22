import math
import numpy as np
from kneed.data_generator import DataGenerator
from kneed.knee_locator import KneeLocator

x = np.arange(0, 10)
y_convex_inc = np.array([1, 2, 3, 4, 5, 10, 15, 20, 40, 100])
y_convex_dec = np.array(y_convex_inc[::-1])
y_concave_dec = np.array(100 - y_convex_inc)
y_concave_inc = np.array(100 - y_convex_dec)


def test_figure2():
    """From the kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.figure2()
    kl = KneeLocator(x, y, S=1.0, curve='concave')
    assert math.isclose(kl.knee, 0.22, rel_tol=0.05)


def test_NoisyGaussian():
    """From the Kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.noisy_gaussian(mu=50, sigma=10, N=10000)
    kl = KneeLocator(x, y, S=1.0, curve='concave')
    assert math.isclose(kl.knee, 60.5, rel_tol=7.0)


def test_concave_increasing():
    """test a concave increasing function"""
    kn = KneeLocator(x, y_concave_inc, curve='concave')
    assert kn.knee == 2


def test_concave_decreasing():
    """test a concave decreasing function"""
    kn = KneeLocator(x, y_concave_dec, curve='concave', direction='decreasing')
    assert kn.knee == 7


def test_convex_increasing():
    """test a convex increasing function"""
    kn = KneeLocator(x, y_convex_inc, curve='convex')
    assert kn.knee == 7


def test_convex_decreasing():
    """test a convex decreasing function"""
    kn = KneeLocator(x, y_convex_dec, curve='convex', direction='decreasing')
    assert kn.knee == 2


def test_concave_increasing_truncated():
    """test a truncated concave increasing function"""
    kn = KneeLocator(x[:-3] / 10, y_concave_inc[:-3] / 10, curve='concave')
    assert kn.knee == 0.2


def test_concave_decreasing_truncated():
    """test a truncated concave decreasing function"""
    kn = KneeLocator(x[:-3] / 10, y_concave_dec[:-3] / 10,
                     curve='concave', direction='decreasing')
    assert kn.knee == 0.4


def test_convex_increasing_truncated():
    """test a truncated convex increasing function"""
    kn = KneeLocator(x[:-3] / 10, y_convex_inc[:-3] / 10, curve='convex')
    assert kn.knee == 0.4


def test_convex_decreasing_truncated():
    """test a truncated convex decreasing function"""
    kn = KneeLocator(x[:-3] / 10, y_convex_dec[:-3] / 10,
                     curve='convex', direction='decreasing')
    assert kn.knee == 0.2
