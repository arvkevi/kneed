import math
from kneed.data_generator import DataGenerator
from kneed.knee_locator import KneeLocator
import pytest


def test_figure2():
    """From the kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.figure2()
    kl = KneeLocator(x, y, S=1.0, invert=False)
    assert math.isclose(kl.knee, 0.22, rel_tol=1e-02)


def test_NoisyGaussian():
    """From the Kneedle manuscript"""
    DG = DataGenerator()
    x, y = DG.NoisyGaussian(mu=50, sigma=10, N=1000)
    kl = KneeLocator(x, y, S=1.0, invert=False)
    assert math.isclose(kl.knee, 60.5, rel_tol=0.05)
