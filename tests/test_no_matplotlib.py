import pytest
from kneed.data_generator import DataGenerator as dg
from kneed.knee_locator import KneeLocator


def test_plot_knee_normalized():
    """Test that error is raised when matplotlib is not installed"""
    with pytest.raises(ModuleNotFoundError):
        x, y = dg.figure2()
        kl = KneeLocator(x, y, S=1.0, curve="concave", interp_method="interp1d")
        kl.plot_knee_normalized()

def test_plot_knee():
    """Test that error is raised when matplotlib is not installed"""
    with pytest.raises(ModuleNotFoundError):
        x, y = dg.figure2()
        kl = KneeLocator(x, y, S=1.0, curve="concave", interp_method="interp1d")
        kl.plot_knee()
