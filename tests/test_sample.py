import math
import numpy as np
from kneed.data_generator import DataGenerator
from kneed.knee_locator import KneeLocator

x = np.arange(0, 10)
y_convex_inc = np.array([1, 2, 3, 4, 5, 10, 15, 20, 40, 100])
y_convex_dec = y_convex_inc[::-1]
y_concave_dec = 100 - y_convex_inc
y_concave_inc = 100 - y_convex_dec


def test_figure2():
    """From the kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.figure2()
    kl = KneeLocator(x, y, S=1.0, invert=False)
    assert math.isclose(kl.knee, 0.22, rel_tol=1e-02)


def test_NoisyGaussian():
    """From the Kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.noisy_gaussian(mu=50, sigma=10, N=100000)
    kl = KneeLocator(x, y, S=1.0, invert=False)
    assert math.isclose(kl.knee, 60.5, rel_tol=6.0)


def concave_increasing():
    """test a concave increasing function"""
    kn = KneeLocator(x, y_concave_inc, curve='concave')
    assert kn.knee == 2


def concave_decreasing():
    """test a concave decreasing function"""
    kn = KneeLocator(x, y_concave_dec, curve='concave', direction='decreasing')
    assert kn.knee == 7


def convex_increasing():
    """test a convex increasing function"""
    kn = KneeLocator(x, y_convex_inc, curve='convex')
    assert kn.knee == 7


def convex_decreasing():
    """test a convex decreasing function"""
    kn = KneeLocator(x, y_convex_dec, curve='convex', direction='decreasing')
    assert kn.knee == 2
