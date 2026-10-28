import numpy as np
from scipy.signal import argrelextrema
from typing import Tuple, Optional, Iterable

VALID_CURVE = ["convex", "concave"]
VALID_DIRECTION = ["increasing", "decreasing"]

try:
    import matplotlib.pyplot as plt
except ImportError:
    _has_matplotlib = False
    _matplotlib_not_found_err = ModuleNotFoundError(
        "This function needs Matplotlib to be executed. Please run command `pip install kneed[plot]` "
    )
else:
    _has_matplotlib = True


class KneeLocator(object):
    """Once instantiated, this class attempts to find the point of maximum
    curvature on a line. The knee is accessible via the ``.knee`` attribute.

    Parameters
    ----------
    x : array-like
        x values, must be the same length as y.
    y : array-like
        y values, must be the same length as x.
    S : float, default 1.0
        Sensitivity. The number of minimum data points below the local
        distance maximum before calling a knee. The original paper suggests
        a default of 1.0.
    curve : str, default "concave"
        If ``"concave"``, the algorithm will detect knees. If ``"convex"``,
        it will detect elbows.
    direction : str, default "increasing"
        One of ``{"increasing", "decreasing"}``.
    interp_method : str, default "interp1d"
        One of ``{"interp1d", "polynomial"}``. ``"interp1d"`` uses ``y`` as
        given; ``"polynomial"`` smooths ``y`` with a polynomial fit.
    online : bool, default False
        If True, kneed will correct old knee points as it traverses the
        curve. If False, it returns the first knee found.
    polynomial_degree : int, default 7
        The degree of the fitting polynomial. Only used when
        ``interp_method="polynomial"``. Passed to ``numpy.polyfit`` as
        the ``deg`` parameter.

    Attributes
    ----------
    x : numpy.ndarray
        x values.
    y : numpy.ndarray
        y values.
    S : float
        Sensitivity, original paper suggests default of 1.0.
    curve : str
        If ``"concave"``, the algorithm detects knees. If ``"convex"``,
        it detects elbows.
    direction : str
        One of ``{"increasing", "decreasing"}``.
    interp_method : str
        One of ``{"interp1d", "polynomial"}``.
    online : bool
        If True, corrects old knee points. If False, returns first knee.
    polynomial_degree : int
        The degree of the fitting polynomial.
    N : int
        The number of ``x`` values in the input data.
    Ds_y : numpy.ndarray
        The y values from the fitted spline.
    x_normalized : numpy.ndarray
        The normalized x values.
    y_normalized : numpy.ndarray
        The normalized y values.
    x_difference : numpy.ndarray
        The x values of the difference curve.
    y_difference : numpy.ndarray
        The y values of the difference curve.
    maxima_indices : numpy.ndarray
        The indices of each of the maxima on the difference curve.
    x_difference_maxima : numpy.ndarray
        The x values from the difference curve where the local maxima
        are located.
    y_difference_maxima : numpy.ndarray
        The y values from the difference curve where the local maxima
        are located.
    minima_indices : numpy.ndarray
        The indices of each of the minima on the difference curve.
    x_difference_minima : numpy.ndarray
        The x values from the difference curve where the local minima
        are located.
    y_difference_minima : numpy.ndarray
        The y values from the difference curve where the local minima
        are located.
    Tmx : numpy.ndarray
        The threshold values on the difference curve for determining the
        knee point.
    knee : float or None
        The x value of the knee point. None if no knee/elbow was detected.
    knee_y : float or None
        The y value of the knee point. None if no knee/elbow was detected.
    norm_knee : float or None
        The normalized x value of the knee point.
    norm_knee_y : float or None
        The normalized y value of the knee point.
    all_knees : list
        All the x values of the identified knee points, in the order they were found.
    all_norm_knees : list
        All the normalized x values of the identified knee points.
    all_knees_y : list
        All the y values of the identified knee points.
    all_norm_knees_y : list
        All the normalized y values of the identified knee points.
    elbow : float or None
        Alias for ``knee``.
    elbow_y : float or None
        Alias for ``knee_y``.
    norm_elbow : float or None
        Alias for ``norm_knee``.
    norm_elbow_y : float or None
        Alias for ``norm_knee_y``.
    all_elbows : set
        Alias for ``all_knees``.
    all_elbows_y : list
        Alias for ``all_knees_y``.
    all_norm_elbows : set
        Alias for ``all_norm_knees``.
    all_norm_elbows_y : list
        Alias for ``all_norm_knees_y``.
    """

    def __init__(
        self,
        x: Iterable[float],
        y: Iterable[float],
        S: float = 1.0,
        curve: str = "concave",
        direction: str = "increasing",
        interp_method: str = "interp1d",
        online: bool = False,
        polynomial_degree: int = 7,
    ):
        # Step 0: Raw Input
        self.x = np.array(x)
        self.y = np.array(y)
        if len(self.x) != len(self.y):
            raise ValueError("x and y must be the same length.")
        self.curve = curve
        self.direction = direction
        self.N = len(self.x)
        self.S = S
        self.all_knees = []
        self.all_norm_knees = []
        self.all_knees_y = []
        self.all_norm_knees_y = []
        self.online = online
        self.polynomial_degree = polynomial_degree

        # I'm implementing Look Before You Leap (LBYL) validation for direction
        # and curve arguments. This is not preferred in Python. The motivation
        # is that the logic inside the conditional once y_difference[j] is less
        # than threshold in find_knee() could have been evaluated improperly if
        # they weren't one of convex, concave, increasing, or decreasing,
        # respectively.
        valid_curve = self.curve in VALID_CURVE
        valid_direction = self.direction in VALID_DIRECTION
        if not all((valid_curve, valid_direction)):
            raise ValueError(
                "Please check that the curve and direction arguments are valid."
            )

        # Step 1: smooth the data. "interp1d" means no smoothing: a linear
        # interpolant evaluated at its own x values returns y unchanged.
        if interp_method == "interp1d":
            self.Ds_y = self.y.astype(float)
        elif interp_method == "polynomial":
            p = np.poly1d(np.polyfit(x, y, self.polynomial_degree))
            self.Ds_y = p(x)
        else:
            raise ValueError(
                "{} is an invalid interp_method parameter, use either 'interp1d' or 'polynomial'".format(
                    interp_method
                )
            )

        # Step 2: normalize values
        self.x_normalized = self.__normalize(self.x)
        self.y_normalized = self.__normalize(self.Ds_y)

        # Step 3: Calculate the Difference curve
        self.y_normalized = self.transform_y(
            self.y_normalized, self.direction, self.curve
        )
        # flipping y by index only mirrors the curve on evenly spaced x;
        # mirror x by value too (paper: x -> x_max - x), keeping ascending order
        if (self.direction, self.curve) in (("decreasing", "concave"), ("increasing", "convex")):
            self.x_normalized = np.flip(1 - self.x_normalized)
        # normalized difference curve
        self.y_difference = self.y_normalized - self.x_normalized
        self.x_difference = self.x_normalized.copy()

        # Step 4: Identify local maxima/minima
        # local maxima
        self.maxima_indices = argrelextrema(self.y_difference, np.greater_equal)[0]
        self.x_difference_maxima = self.x_difference[self.maxima_indices]
        self.y_difference_maxima = self.y_difference[self.maxima_indices]

        # local minima
        self.minima_indices = argrelextrema(self.y_difference, np.less_equal)[0]
        self.x_difference_minima = self.x_difference[self.minima_indices]
        self.y_difference_minima = self.y_difference[self.minima_indices]

        # Step 5: Calculate thresholds
        self.Tmx = self.y_difference_maxima - (
            self.S * np.abs(np.diff(self.x_normalized).mean())
        )

        # Step 6: find knee
        self.knee, self.norm_knee = self.find_knee()

        # Step 7: If we have a knee, extract data about it
        self.knee_y = self.norm_knee_y = None
        if self.knee is not None:
            self.knee_y = self.y[self.x == self.knee][0]
            self.norm_knee_y = self.y_normalized[self.x_normalized == self.norm_knee][0]

    @staticmethod
    def __normalize(a: Iterable[float]) -> Iterable[float]:
        """Normalize an array to [0, 1].

        Parameters
        ----------
        a : array-like
            The array to normalize.

        Returns
        -------
        numpy.ndarray
            The normalized array.
        """
        a = np.asarray(a, dtype=float)
        return (a - min(a)) / (max(a) - min(a))

    @staticmethod
    def transform_y(y: Iterable[float], direction: str, curve: str) -> float:
        """Transform y to concave, increasing based on given direction and curve.

        Parameters
        ----------
        y : array-like
            The y values to transform.
        direction : str
            One of ``{"increasing", "decreasing"}``.
        curve : str
            One of ``{"concave", "convex"}``.

        Returns
        -------
        numpy.ndarray
            The transformed y values.
        """
        # convert elbows to knees
        if direction == "decreasing":
            if curve == "concave":
                y = np.flip(y)
            elif curve == "convex":
                y = y.max() - y
        elif direction == "increasing" and curve == "convex":
            y = np.flip(y.max() - y)

        return y

    def find_knee(
        self,
    ):
        """Identify the knee value and set the instance attributes.

        This method is called automatically when ``KneeLocator`` is
        instantiated.

        Returns
        -------
        tuple
            ``(knee, norm_knee)`` where each is a float or None.
        """
        if not self.maxima_indices.size:
            return None, None

        x = self.x
        x_normalized = self.x_normalized
        y_difference = self.y_difference
        all_knees = self.all_knees
        object_x = x.dtype.hasobject
        unique_x = unique_normalized = None

        def crossings():
            maxima = self.maxima_indices
            minima = self.minima_indices
            stop = len(self.x_difference) - 1
            if object_x or type(self.curve) is not str or type(self.direction) is not str:
                # Keep repeated comparisons observable for object coordinates.
                maxima_set = set(maxima)
                minima_set = set(minima)
                maxima_threshold_index = 0
                detection_active = True
                for i in range(maxima[0], stop):
                    if i in maxima_set:
                        threshold = self.Tmx[maxima_threshold_index]
                        threshold_index = i
                        maxima_threshold_index += 1
                        detection_active = True
                    if i in minima_set:
                        threshold = 0.0
                        detection_active = False
                    if detection_active and y_difference[i + 1] < threshold:
                        yield threshold_index
                return

            if not np.isnan(y_difference).any():
                # Between consecutive maxima the first minimum is the lowest
                # value, so reducing the whole interval preserves crossings.
                indices = maxima[maxima < stop]
                if not indices.size:
                    return
                lows = np.fmin.reduceat(y_difference[1:], indices)
                thresholds = self.Tmx[:indices.size]
                crossed = lows < thresholds
                # A flat extremum cannot cross a threshold at or below its
                # height; higher thresholds still need minima precedence.
                if (thresholds > y_difference[indices]).any():
                    next_minimum = np.searchsorted(minima, indices)
                    crossed &= indices != np.append(minima, stop)[next_minimum]
                yield from indices[crossed]
                return

            # Each maximum stays active until the next maximum or minimum.
            ends = np.minimum(np.append(maxima[1:], stop), stop)
            next_minimum = np.searchsorted(minima, maxima)
            ends = np.minimum(ends, np.append(minima, stop)[next_minimum])
            active = maxima < ends
            indices = maxima[active]
            if not indices.size:
                return
            boundaries = np.empty(2 * indices.size, dtype=maxima.dtype)
            boundaries[::2] = indices
            boundaries[1::2] = ends[active]
            if boundaries[-1] == stop:
                boundaries = boundaries[:-1]
            # Ignore NaNs just as individual less-than comparisons do.
            lows = np.fmin.reduceat(y_difference[1:], boundaries)[::2]
            yield from indices[lows < self.Tmx[active]]

        for threshold_index in crossings():
            if self.curve == "convex":
                if self.direction == "decreasing":
                    knee_index = threshold_index
                    knee = x[knee_index]
                    norm_knee = x_normalized[threshold_index]
                else:
                    knee_index = -(threshold_index + 1)
                    knee = x[knee_index]
                    norm_knee = x_normalized[threshold_index]
            elif self.curve == "concave":
                if self.direction == "decreasing":
                    knee_index = -(threshold_index + 1)
                    knee = x[knee_index]
                    norm_knee = x_normalized[threshold_index]
                else:
                    knee_index = threshold_index
                    knee = x[knee_index]
                    norm_knee = x_normalized[threshold_index]

            if object_x:
                y_at_knee = self.y[x == knee][0]
                y_norm_at_knee = self.y_normalized[x_normalized == norm_knee][0]
            if knee not in all_knees:
                if not object_x:
                    if unique_x is None:
                        unique_x = (x[1:] > x[:-1]).all()
                        unique_normalized = (
                            x_normalized[1:] > x_normalized[:-1]
                        ).all()
                    y_at_knee = (
                        self.y[knee_index] if unique_x else self.y[x == knee][0]
                    )
                    y_norm_at_knee = (
                        self.y_normalized[threshold_index]
                        if unique_normalized
                        else self.y_normalized[x_normalized == norm_knee][0]
                    )
                all_knees.append(knee)
                self.all_norm_knees.append(norm_knee)
                self.all_knees_y.append(y_at_knee)
                self.all_norm_knees_y.append(y_norm_at_knee)

            if self.online is False:
                return knee, norm_knee

        if not all_knees:
            return None, None
        return knee, norm_knee

    def plot_knee_normalized(
        self,
        figsize: Optional[Tuple[int, int]] = None,
        title: str = "Normalized Knee Point",
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
    ):
        """Plot the normalized curve, the difference curve, and the knee.

        Parameters
        ----------
        figsize : tuple of int, optional
            The figure size of the plot, e.g. ``(12, 8)``.
        title : str, default "Normalized Knee Point"
            Title of the visualization.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        """
        if not _has_matplotlib:
            raise _matplotlib_not_found_err

        if figsize is None:
            figsize = (6, 6)

        plt.figure(figsize=figsize)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.plot(self.x_normalized, self.y_normalized, "b", label="normalized curve")
        plt.plot(self.x_difference, self.y_difference, "r", label="difference curve")
        plt.xticks(
            np.arange(self.x_normalized.min(), self.x_normalized.max() + 0.1, 0.1)
        )
        plt.yticks(
            np.arange(self.y_difference.min(), self.y_normalized.max() + 0.1, 0.1)
        )

        plt.vlines(
            self.norm_knee,
            plt.ylim()[0],
            plt.ylim()[1],
            linestyles="--",
            label="knee/elbow",
        )
        plt.legend(loc="best")

    def plot_knee(
        self,
        figsize: Optional[Tuple[int, int]] = None,
        title: str = "Knee Point",
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
    ):
        """Plot the curve and the knee, if it exists.

        Parameters
        ----------
        figsize : tuple of int, optional
            The figure size of the plot, e.g. ``(12, 8)``.
        title : str, default "Knee Point"
            Title of the visualization.
        xlabel : str, optional
            X-axis label.
        ylabel : str, optional
            Y-axis label.
        """
        if not _has_matplotlib:
            raise _matplotlib_not_found_err

        if figsize is None:
            figsize = (6, 6)

        plt.figure(figsize=figsize)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.plot(self.x, self.y, "b", label="data")
        plt.vlines(
            self.knee, plt.ylim()[0], plt.ylim()[1], linestyles="--", label="knee/elbow"
        )
        plt.legend(loc="best")

    # Niceties for users working with elbows rather than knees
    @property
    def elbow(self):
        return self.knee

    @property
    def norm_elbow(self):
        return self.norm_knee

    @property
    def elbow_y(self):
        return self.knee_y

    @property
    def norm_elbow_y(self):
        return self.norm_knee_y

    @property
    def all_elbows(self):
        return self.all_knees

    @property
    def all_norm_elbows(self):
        return self.all_norm_knees

    @property
    def all_elbows_y(self):
        return self.all_knees_y

    @property
    def all_norm_elbows_y(self):
        return self.all_norm_knees_y
