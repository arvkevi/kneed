import numpy as np
from scipy import interpolate
from scipy.signal import argrelextrema
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import warnings


class KneeLocator(object):

    def __init__(self, x, y, S=1.0, curve='concave', direction='increasing', interp_method='interp1d'):
        """
        Once instantiated, this class attempts to find the point of maximum
        curvature on a line. The knee is accessible via the `.knee` attribute.
        :param x: x values.
        :type x: list or array.
        :param y: y values.
        :type y: list or array.
        :param S: Sensitivity, original paper suggests default of 1.0
        :type S: float
        :param curve: If 'concave', algorithm will detect knees. If 'convex', it
            will detect elbows.
        :type curve: string
        :param direction: one of {"increasing", "decreasing"}
        :type direction: string
        :param interp_method: one of {"interp1d", "polynomial"}
        :type interp_method: string
        """
        # Step 0: Raw Input
        self.x = np.array(x)
        self.y = np.array(y)
        self.curve = curve
        self.direction = direction
        self.N = len(self.x)
        self.S = S

        # Step 1: fit a smooth line
        if interp_method == "interp1d":
            uspline = interpolate.interp1d(self.x, self.y)
            self.Ds_y = uspline(self.x)
        elif interp_method == "polynomial":
            pn_model = PolynomialFeatures(7)
            xpn = pn_model.fit_transform(self.x.reshape(-1, 1))
            regr_model = LinearRegression()
            regr_model.fit(xpn, self.y)
            self.Ds_y = regr_model.predict(
                pn_model.fit_transform(self.x.reshape(-1, 1)))
        else:
            warnings.warn(
                "{} is an invalid interp_method parameter, use either 'interp1d' or 'polynomial'".format(
                    interp_method)
            )
            return

        # Step 2: normalize values
        self.x_normalized = self.__normalize(self.x)
        self.y_normalized = self.__normalize(self.Ds_y)

        # Step 3: Calculate the Difference curve
        # convert elbows to knees
        if self.curve == 'convex':
            self.x_normalized = self.x_normalized.max() - self.x_normalized
            self.y_normalized = self.y_normalized.max() - self.y_normalized
        # flip decreasing functions to increasing
        if self.direction == 'decreasing':
            self.y_normalized = np.flip(self.y_normalized)
        # normalized difference curve
        self.y_distance = self.y_normalized - self.x_normalized
        self.x_distance = self.x_normalized

        # Step 4: Identify local maxima/minima
        # local maxima
        self.maxima_inidices = argrelextrema(self.y_distance, np.greater)[0]
        self.x_distance_maxima = self.x_distance[self.maxima_inidices]
        self.y_distance_maxima = self.y_distance[self.maxima_inidices]

        # local minima
        self.minima_indices = argrelextrema(self.y_distance, np.less)[0]
        self.x_distance_minima = self.x_distance[self.minima_indices]
        self.y_distance_minima = self.y_distance[self.minima_indices]

        # Step 5: Calculate thresholds
        self.Tmx = self.y_distance_maxima - (self.S * np.abs(np.diff(self.x_normalized).mean()))

        # Step 6: find knee
        self.knee, self.norm_knee, self.knee_x = self.find_knee()

    @staticmethod
    def __normalize(a):
        """normalize an array
        :param a: The array to normalize
        :type a: array
        """
        return (a - min(a)) / (max(a) - min(a))

    def find_knee(self, ):
        """This function finds and returns the knee value, the normalized knee
        value, and the x value where the knee is located.
        :returns: tuple(knee, norm_knee, knee_x)
        :rtype: (float, float, int)
        )
        """
        if not self.maxima_inidices.size:
            warnings.warn("No local maxima found in the distance curve\n"
                          "The line is probably not polynomial, try plotting\n"
                          "the distance curve with plt.plot(knee.x_distance, knee.y_distance)\n"
                          "Also check that you aren't mistakenly setting the curve argument", RuntimeWarning)
            return None, None, None

        mxmx_iter = np.arange(self.maxima_inidices[0], len(self.x_normalized))
        xmx_idx_iter = np.append(self.maxima_inidices, len(self.x_normalized))

        knee_, norm_knee_, knee_x = 0.0, 0.0, None
        for mxmx_i, mxmx in enumerate(xmx_idx_iter):
            # stopping criteria for exhasuting array
            if mxmx_i == len(xmx_idx_iter) - 1:
                break
            # indices between maxima/minima
            idxs = (mxmx_iter > xmx_idx_iter[mxmx_i]) * \
                (mxmx_iter < xmx_idx_iter[mxmx_i + 1])
            between_local_mx = mxmx_iter[np.where(idxs)]

            for j in between_local_mx:
                if j in self.minima_indices:
                    # reached a minima, x indices are unique
                    # only need to check if j is a min
                    if self.y_distance[j + 1] > self.y_distance[j]:
                        self.Tmx[mxmx_i] = 0
                        knee_x = None  # reset x where y_distance crossed Tmx
                    elif self.y_distance[j + 1] <= self.y_distance[j]:
                        warnings.warn("If this is a minima, "
                                      "how would you ever get here:", RuntimeWarning)
                if self.y_distance[j] < self.Tmx[mxmx_i] or self.Tmx[mxmx_i] < 0:
                    # declare a knee
                    if not knee_x:
                        knee_x = j
                    knee_ = self.x[self.maxima_inidices[mxmx_i]]
                    norm_knee_ = self.x_normalized[self.maxima_inidices[mxmx_i]]
        return knee_, norm_knee_, knee_x

    def plot_knee_normalized(self, ):
        """Plot the normalized curve, the distance curve (x_distance, y_normalized) and the
        knee, if it exists.
        """
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 8))
        plt.plot(self.x_normalized, self.y_normalized)
        plt.plot(self.x_distance, self.y_distance, 'r')
        plt.xticks(np.arange(self.x_normalized.min(), self.x_normalized.max() + 0.1, 0.1))
        plt.yticks(np.arange(self.y_distance.min(), self.y_normalized.max() + 0.1, 0.1))

        plt.vlines(self.norm_knee, plt.ylim()[0], plt.ylim()[1])

    def plot_knee(self, ):
        """Plot the curve and the knee, if it exists"""
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 8))
        plt.plot(self.x, self.y)
        plt.vlines(self.knee, plt.ylim()[0], plt.ylim()[1])

    # Niceties for users working with elbows rather than knees

    @property
    def elbow(self):
        return self.knee

    @property
    def norm_elbow(self):
        return self.norm_knee

    @property
    def elbow_x(self):
        return self.knee_x
