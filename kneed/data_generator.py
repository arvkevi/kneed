import numpy as np

class DataGenerator(object):

    def __init(self,):
        pass

    def noisy_gaussian(self, mu=50, sigma=10, N=100):
        """
        Recreates NoisyGaussian from the orignial kneedle paper.
        """
        z = np.random.normal(loc=mu, scale=sigma, size=N)
        x = np.sort(z)
        y = np.array(range(N)) / float(N)
        return x, y

    def figure2(self,):
        """
        Recreates the values in figure 2 from the original kneedle paper.
        """
        with np.errstate(divide='ignore'):
            x = np.linspace(0.0, 1, 10)
            return x, np.true_divide(-1, x + 0.1) + 5

    def inverted(self,):
        """
        Test function for inverted data
        """
        x = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
        y = [2314, 802, 519, 417, 358, 318, 302, 284, 280]
        return x, y
