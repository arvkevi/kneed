import numpy as np


class DataGenerator(object):
    """Generate data to work with kneedle."""

    def __init(self,):
        pass

    @staticmethod
    def noisy_gaussian(mu=50, sigma=10, N=100):
        """Recreate NoisyGaussian from the orignial kneedle paper.
        :param mu: The mean value to build a normal distribution around
        :type mu: int
        :param sigma: The standard deviation of the distribution.
        :type sigma: int
        :param N: The number of samples to draw from to build the normal distribution.
        :type N: int
        :returns: tuple(x, y)
        :rtypes: (array, array)
        """
        z = np.random.normal(loc=mu, scale=sigma, size=N)
        x = np.sort(z)
        y = np.array(range(N)) / float(N)
        return x, y

    @staticmethod
    def figure2():
        """Recreate the values in figure 2 from the original kneedle paper.
        :returns: tuple(x, y)
        :rtypes: (array, array)
        """
        with np.errstate(divide='ignore'):
            x = np.linspace(0.0, 1, 10)
            return x, np.true_divide(-1, x + 0.1) + 5

    @staticmethod
    def decreasing():
        """Test function for decreasing data.
        :returns: tuple(x, y)
        :rtypes: (array, array)
        """
        x = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        y = [2314, 802, 519, 417, 358, 318, 302, 284, 280]
        return x, y
