# Sample Test passing with nose and pytest

import math
from kneed import data_generator, knee_locator

def test_figure2():
    DG = data_generator()
    x,y = DG.figure2()
    kneedle = knee_locator(x, y, S=1.0, invert=False)
    assert math.isclose(kneedle.knee, 0.22, rel_tol=1e-02)

def test_NoisyGaussian():
    DG = data_generator()
    x,y = DG.NoisyGaussian(mu=50, sigma=10, N=1000)
    kneedle = knee_locator(x, y, S=1.0, invert=False)
    assert math.isclose(kneedle.knee, 60.5, rel_tol=0.05)
