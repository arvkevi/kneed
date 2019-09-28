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
        self.all_knees = set()
        self.all_norm_knees = set()

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
        self.x_normalized, self.y_normalized = self.transform_xy(self.x_normalized, self.y_normalized, self.direction, self.curve)
        # normalized difference curve
        self.y_distance = self.y_normalized - self.x_normalized
        self.x_distance = self.x_normalized.copy()

        # Step 4: Identify local maxima/minima
        # local maxima
        self.maxima_indices = argrelextrema(self.y_distance, np.greater)[0]
        self.x_distance_maxima = self.x_distance[self.maxima_indices]
        self.y_distance_maxima = self.y_distance[self.maxima_indices]

        # local minima
        self.minima_indices = argrelextrema(self.y_distance, np.less)[0]
        self.x_distance_minima = self.x_distance[self.minima_indices]
        self.y_distance_minima = self.y_distance[self.minima_indices]

        # Step 5: Calculate thresholds
        self.Tmx = self.y_distance_maxima - (self.S * np.abs(np.diff(self.x_normalized).mean()))

        # Step 6: find knee
        self.find_knee()
        self.knee, self.norm_knee = min(self.all_knees), min(self.all_norm_knees)

    @staticmethod
    def __normalize(a):
        """normalize an array
        :param a: The array to normalize
        :type a: array
        """
        return (a - min(a)) / (max(a) - min(a))

    @staticmethod
    def transform_xy(x, y, direction, curve):
        """transform x and y to concave, increasing based on given direction and curve"""
        # convert elbows to knees
        if curve == 'convex':
            x = x.max() - x
            y = y.max() - y
        # flip decreasing functions to increasing
        if direction == 'decreasing':
            y = np.flip(y, axis=0)

        if curve == 'convex':
            x = np.flip(x, axis=0)
            y = np.flip(y, axis=0)

        return x, y

    def find_knee(self, ):
        """This function finds and sets the knee value and the normalized knee value. """
        if not self.maxima_indices.size:
            warnings.warn("No local maxima found in the distance curve\n"
                          "The line is probably not polynomial, try plotting\n"
                          "the distance curve with plt.plot(knee.x_distance, knee.y_distance)\n"
                          "Also check that you aren't mistakenly setting the curve argument", RuntimeWarning)
            return None, None

        # artificially place a local max at the last item in the x_distance array
        self.maxima_indices = np.append(self.maxima_indices, len(self.x_distance) - 1)
        self.minima_indices = np.append(self.minima_indices, len(self.x_distance) - 1)

        # placeholder for which threshold region i is located in.
        maxima_threshold_index = 0
        minima_threshold_index = 0
        # traverse the distance curve
        for idx, i in enumerate(self.x_distance):
            # reached the end of the curve
            if i == 1.0:
                break
            # values in distance curve are at or after a local maximum
            if idx >= self.maxima_indices[maxima_threshold_index]:
                threshold = self.Tmx[maxima_threshold_index]
                threshold_index = idx
                maxima_threshold_index += 1
            # values in distance curve are at or after a local minimum
            if idx >= self.minima_indices[minima_threshold_index]:
                threshold = 0.0
                minima_threshold_index += 1
            # Do not evaluate values in the distance curve before the first local maximum.
            if idx < self.maxima_indices[0]:
                continue

            # evaluate the threshold
            if self.y_distance[idx] < threshold:
                if self.curve == 'convex':
                    if self.direction == 'decreasing':
                        knee = self.x[threshold_index]
                        self.all_knees.add(knee)
                        norm_knee = self.x_normalized[threshold_index]
                        self.all_norm_knees.add(norm_knee)
                    else:
                        knee = self.x[-(threshold_index + 1)]
                        self.all_knees.add(knee)
                        norm_knee = self.x_normalized[-(threshold_index + 1)]
                        self.all_norm_knees.add(norm_knee)

                elif self.curve == 'concave':
                    if self.direction == 'decreasing':
                        knee = self.x[-(threshold_index + 1)]
                        self.all_knees.add(knee)
                        norm_knee = self.x_normalized[-(threshold_index + 1)]
                        self.all_norm_knees.add(norm_knee)
                    else:
                        knee = self.x[threshold_index]
                        self.all_knees.add(knee)
                        norm_knee = self.x_normalized[threshold_index]
                        self.all_norm_knees.add(norm_knee)

        if self.all_knees == set():
            warnings.warn('No knee/elbow found')

    def plot_knee_normalized(self, ):
        """Plot the normalized curve, the distance curve (x_distance, y_normalized) and the knee, if it exists."""
        import matplotlib.pyplot as plt

        plt.figure(figsize=(6, 6))
        plt.title('Normalized Knee Point')
        plt.plot(self.x_normalized, self.y_normalized, 'b', label='normalized curve')
        plt.plot(self.x_distance, self.y_distance, 'r', label='difference curve')
        plt.xticks(np.arange(self.x_normalized.min(), self.x_normalized.max() + 0.1, 0.1))
        plt.yticks(np.arange(self.y_distance.min(), self.y_normalized.max() + 0.1, 0.1))

        plt.vlines(self.norm_knee, plt.ylim()[0], plt.ylim()[1], linestyles='--', label='knee/elbow')
        plt.legend(loc='best')

    def plot_knee(self, ):
        """Plot the curve and the knee, if it exists"""
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6, 6))
        plt.title('Knee Point')
        plt.plot(self.x, self.y, 'b', label='data')
        plt.vlines(self.knee, plt.ylim()[0], plt.ylim()[1], linestyles='--', label='knee/elbow')
        plt.legend(loc='best')

    # Niceties for users working with elbows rather than knees
    @property
    def elbow(self):
        return self.knee

    @property
    def norm_elbow(self):
        return self.norm_knee

    @property
    def all_elbows(self):
        return self.all_knees

    @property
    def all_norm_elbows(self):
        return self.all_norm_knees
