import numpy as np

from typing import Iterable, Tuple


class DataGenerator(object):
    """Generate data to work with kneedle."""

    def __init(self,):
        pass

    @staticmethod
    def noisy_gaussian(
        mu: float = 50, sigma: float = 10, N: int = 100
    ) -> Tuple[Iterable[float], Iterable[float]]:
        """Recreate NoisyGaussian from the orignial kneedle paper.
        :param mu: The mean value to build a normal distribution around
        :param sigma: The standard deviation of the distribution.
        :param N: The number of samples to draw from to build the normal distribution.
        :returns: tuple(x, y)
        """
        z = np.random.normal(loc=mu, scale=sigma, size=N)
        x = np.sort(z)
        y = np.array(range(N)) / float(N)
        return x, y

    @staticmethod
    def figure2() -> Tuple[Iterable[float], Iterable[float]]:
        """Recreate the values in figure 2 from the original kneedle paper.
        :returns: tuple(x, y)
        """
        with np.errstate(divide="ignore"):
            x = np.linspace(0.0, 1, 10)
            return x, np.true_divide(-1, x + 0.1) + 5

    @staticmethod
    def decreasing() -> Tuple[Iterable[float], Iterable[float]]:
        """Test function for decreasing data.
        :returns: tuple(x, y)
        """
        x = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        y = [2314, 802, 519, 417, 358, 318, 302, 284, 280]
        return x, y

    @staticmethod
    def convex_increasing() -> Tuple[Iterable[float], Iterable[float]]:
        """Generate a sample increasing convex function
        :returns: tuple(x, y)
        """
        x = np.arange(0, 10)
        y_convex_inc = np.array([1, 2, 3, 4, 5, 10, 15, 20, 40, 100])
        return x, y_convex_inc

    @staticmethod
    def convex_decreasing() -> Tuple[Iterable[float], Iterable[float]]:
        """Generate a sample decreasing convex function
        :returns: tuple(x, y)
        """
        x = np.arange(0, 10)
        y_convex_dec = np.array([100, 40, 20, 15, 10, 5, 4, 3, 2, 1])
        return x, y_convex_dec

    @staticmethod
    def concave_decreasing() -> Tuple[Iterable[float], Iterable[float]]:
        """Generate a sample decreasing concave function
        :returns: tuple(x, y)
        """
        x = np.arange(0, 10)
        y_concave_dec = np.array([99, 98, 97, 96, 95, 90, 85, 80, 60, 0])
        return x, y_concave_dec

    @staticmethod
    def concave_increasing() -> Tuple[Iterable[float], Iterable[float]]:
        """Generate a sample increasing concave function
        :returns: tuple(x, y)
        """
        x = np.arange(0, 10)
        y_concave_inc = np.array([0, 60, 80, 85, 90, 95, 96, 97, 98, 99])
        return x, y_concave_inc

    @staticmethod
    def bumpy() -> Tuple[Iterable[float], Iterable[float]]:
        """Generate a sample function with local minima/maxima
        :returns: tuple(x, y)
        """
        x_bumpy = list(range(90))
        y_bumpy = [
            7305.0,
            6979.0,
            6666.6,
            6463.2,
            6326.5,
            6048.8,
            6032.8,
            5762.0,
            5742.8,
            5398.2,
            5256.8,
            5227.0,
            5001.7,
            4942.0,
            4854.2,
            4734.6,
            4558.7,
            4491.1,
            4411.6,
            4333.0,
            4234.6,
            4139.1,
            4056.8,
            4022.5,
            3868.0,
            3808.3,
            3745.3,
            3692.3,
            3645.6,
            3618.3,
            3574.3,
            3504.3,
            3452.4,
            3401.2,
            3382.4,
            3340.7,
            3301.1,
            3247.6,
            3190.3,
            3180.0,
            3154.2,
            3089.5,
            3045.6,
            2989.0,
            2993.6,
            2941.3,
            2875.6,
            2866.3,
            2834.1,
            2785.1,
            2759.7,
            2763.2,
            2720.1,
            2660.1,
            2690.2,
            2635.7,
            2632.9,
            2574.6,
            2556.0,
            2545.7,
            2513.4,
            2491.6,
            2496.0,
            2466.5,
            2442.7,
            2420.5,
            2381.5,
            2388.1,
            2340.6,
            2335.0,
            2318.9,
            2319.0,
            2308.2,
            2262.2,
            2235.8,
            2259.3,
            2221.0,
            2202.7,
            2184.3,
            2170.1,
            2160.0,
            2127.7,
            2134.7,
            2102.0,
            2101.4,
            2066.4,
            2074.3,
            2063.7,
            2048.1,
            2031.9,
        ]
        return x_bumpy, y_bumpy
