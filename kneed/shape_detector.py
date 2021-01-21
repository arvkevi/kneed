import numpy as np


def find_shape(x, y):
    """
    Detect the direction and curve type of the line.

    :return: direction("increasing" or "decreasing") and curve type("concave" or "convex")
    """

    p = np.polyfit(x, y, deg=1)
    x1, x2 = int(len(x) * 0.2), int(len(x) * 0.8)
    q = np.mean(y[x1:x2]) - np.mean(x[x1:x2] * p[0] + p[1])
    if p[0] > 0 and q > 0:
        return 'increasing', 'concave'
    if p[0] > 0 and q <= 0:
        return 'increasing', 'convex'
    if p[0] <= 0 and q > 0:
        return 'decreasing', 'concave'
    else:
        return 'decreasing', 'convex'