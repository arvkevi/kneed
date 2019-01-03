import numpy as np
from scipy import interpolate
from scipy.signal import argrelextrema
import warnings


class KneeLocator(object):

    def __init__(self, x, y, S=1.0, curve='concave', direction='increasing'):
        """
        x = x values
        y = y values
        S = Sensitivity parameter, original paper suggests default of 1.0
        curve = If True, algorithm will detect elbows instead of knees.
        direction = {"increasing", "decreasing"}
        """
        # Step 0: Raw Input
        self.x = x
        self.y = y
        self.curve = curve
        self.direction = direction
        self.N = len(self.x)
        self.S = S

        # Step 1: fit a smooth line
        uspline = interpolate.interp1d(self.x, self.y)
        self.Ds_x = np.linspace(np.min(self.x), np.max(self.x), self.N)
        self.Ds_y = uspline(self.Ds_x)

        # Step 2: normalize values
        self.xsn = self.__normalize(self.Ds_x)
        self.ysn = self.__normalize(self.Ds_y)

        # Step 3: Calculate difference curve
        self.xd = self.xsn
        if self.curve == 'convex' and direction == 'decreasing':
            self.yd = self.ysn + self.xsn
            self.yd = 1 - self.yd
        elif self.curve == 'concave' and direction == 'decreasing':
            self.yd = self.ysn + self.xsn
        elif self.curve == 'concave' and direction == 'increasing':
            self.yd = self.ysn - self.xsn
        if self.curve == 'convex' and direction == 'increasing':
            self.yd = abs(self.ysn - self.xsn)

        # Step 4: Identify local maxima/minima
        # local maxima
        self.xmx_idx = argrelextrema(self.yd, np.greater)[0]
        self.xmx = self.xd[self.xmx_idx]
        self.ymx = self.yd[self.xmx_idx]

        # local minima
        self.xmn_idx = argrelextrema(self.yd, np.less)[0]
        self.xmn = self.xd[self.xmn_idx]
        self.ymn = self.yd[self.xmn_idx]

        # Step 5: Calculate thresholds
        self.Tmx = self.__threshold(self.ymx)

        # Step 6: find knee
        self.knee, self.norm_knee, self.knee_x = self.find_knee()

    def __normalize(self, a):
        return (a - min(a)) / (max(a) - min(a))

    def __threshold(self, ymx_i):
        """
        calculates the difference threshold for a
        given difference local maximum
        """
        return ymx_i - (self.S * np.diff(self.xsn).mean())

    def find_knee(self, ):
        if len(self.xmx_idx) == 0:
            warnings.warn("No local maxima found in the distance curve\n"
                          "The line is probably not polynomial, try plotting\n"
                          "the distance curve with plt.plot(knee.xd, knee.yd)\n"
                          "Also check that you aren't mistakenly setting the curve argument", RuntimeWarning)
            return None, None, None

        mxmx_iter = np.arange(self.xmx_idx[0], len(self.xsn))
        xmx_idx_iter = np.append(self.xmx_idx, len(self.xsn))

        knee_, norm_knee_, knee_x = 0.0, 0.0, None
        for mxmx_i in range(len(xmx_idx_iter)):
            # stopping criteria for exhasuting array
            if mxmx_i == len(xmx_idx_iter) - 1:
                break
            # indices between maxima/minima
            idxs = (mxmx_iter > xmx_idx_iter[mxmx_i]) * \
                (mxmx_iter < xmx_idx_iter[mxmx_i + 1])
            between_local_mx = mxmx_iter[np.where(idxs)]

            for j in between_local_mx:
                if j in self.xmn_idx:
                    # reached a minima, x indices are unique
                    # only need to check if j is a min
                    if self.yd[j + 1] > self.yd[j]:
                        self.Tmx[mxmx_i] = 0
                        knee_x = None  # reset x where yd crossed Tmx
                    elif self.yd[j + 1] <= self.yd[j]:
                        warnings.warn("If this is a minima, "
                                      "how would you ever get here:", RuntimeWarning)
                if self.yd[j] < self.Tmx[mxmx_i] or self.Tmx[mxmx_i] < 0:
                    # declare a knee
                    if not knee_x:
                        knee_x = j
                    knee_ = self.x[self.xmx_idx[mxmx_i]]
                    norm_knee_ = self.xsn[self.xmx_idx[mxmx_i]]
        return knee_, norm_knee_, knee_x

    def plot_knee_normalized(self, ):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 8))
        plt.plot(self.xsn, self.ysn)
        plt.plot(self.xd, self.yd, 'r')
        plt.xticks(np.arange(min(self.xsn), max(self.xsn) + 0.1, 0.1))
        plt.yticks(np.arange(min(self.xd), max(self.ysn) + 0.1, 0.1))

        plt.vlines(self.norm_knee, plt.ylim()[0], plt.ylim()[1])

    def plot_knee(self, ):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 8))
        plt.plot(self.x, self.y)
        plt.vlines(self.knee, plt.ylim()[0], plt.ylim()[1])
