# kneed

## Knee-point detection in Python

[![Downloads](https://pepy.tech/badge/kneed)](https://pepy.tech/project/kneed) [![Downloads](https://pepy.tech/badge/kneed/week)](https://pepy.tech/project/kneed) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arvkevi/kneed/master)  [![Build Status](https://travis-ci.com/arvkevi/kneed.svg?branch=master)](https://travis-ci.com/arvkevi/kneed) [![CodeFactor](https://www.codefactor.io/repository/github/arvkevi/kneed/badge)](https://www.codefactor.io/repository/github/arvkevi/kneed)

This repository is an attempt to implement the kneedle algorithm, published [here](https://www1.icsi.berkeley.edu/~barath/papers/kneedle-simplex11.pdf). Given a set of `x` and `y` values, `kneed` will return the knee point of the function. The knee point is the point of maximum curvature.

![](images/functions_args_summary.png)

## Installation

To install use:

conda:

    $ conda install -c conda-forge kneed                                                         

pip:                                                               

```
$ pip install kneed
```

Or clone the repo:
```
$ git clone https://github.com/arvkevi/kneed.git
$ python setup.py install
```

**Tested with Python 3.5 and 3.6**

## Usage
*This reproduces Figure 2 from the manuscript.*

`x` and `y` must be equal length arrays.  
`DataGenerator` has functions to generate sample datasets.  
```python
from kneed import DataGenerator, KneeLocator

x, y = DataGenerator.figure2()

print([round(i, 3) for i in x])
print([round(i, 3) for i in y])

[0.0, 0.111, 0.222, 0.333, 0.444, 0.556, 0.667, 0.778, 0.889, 1.0]
[-5.0, 0.263, 1.897, 2.692, 3.163, 3.475, 3.696, 3.861, 3.989, 4.091]
```

Instantiating `KneeLocator` with `x`, `y` and the appropriate `curve` and `direction` will find the knee (or elbow) point.  
Here, `kneedle.knee` stores the knee point of the curve.

```python
kneedle = KneeLocator(x, y, S=1.0, curve='concave', direction='increasing')

print(round(kneedle.knee, 3))
0.222

# .elbow can also be used to access point of maximum curvature
print(round(kneedle.elbow, 3))
0.222
```

The `KneeLocator` class also has some plotting functions for quick visualization of the curve (blue), the distance curve (red) and the knee (dashed line, if present)

```Python
kneedle.plot_knee_normalized()
```

![](images/figure2.knee.png)

#### Average Knee from 5000 NoisyGaussians when mu=50 and sigma=10

```python
import numpy as np

knees = []
for i in range(5000):
    x,y = DataGenerator.noisy_gaussian(mu=50, sigma=10, N=1000)
    kneedle = KneeLocator(x, y, curve='concave', direction='increasing')
    knees.append(kneedle.knee)

np.mean(knees)
60.921051806064931
```

#### Polynomial Line Fit
Here is an example of a "bumpy" line where the default `interp1d` spline fitting method does not provide the best estimate for the point of maximum curvature.
This example demonstrates that setting the parameter `interp_method='polynomial'` will choose a more accurate point by smoothing the line.

```python
x = list(range(90))
y = [
    7304.99, 6978.98, 6666.61, 6463.20, 6326.53, 6048.79, 6032.79, 5762.01, 5742.77,
    5398.22, 5256.84, 5226.98, 5001.72, 4941.98, 4854.24, 4734.61, 4558.75, 4491.10,
    4411.61, 4333.01, 4234.63, 4139.10, 4056.80, 4022.49, 3867.96, 3808.27, 3745.27,
    3692.34, 3645.55, 3618.28, 3574.26, 3504.31, 3452.44, 3401.20, 3382.37, 3340.67,
    3301.08, 3247.59, 3190.27, 3179.99, 3154.24, 3089.54, 3045.62, 2988.99, 2993.61,
    2941.35, 2875.60, 2866.33, 2834.12, 2785.15, 2759.65, 2763.20, 2720.14, 2660.14,
    2690.22, 2635.71, 2632.92, 2574.63, 2555.97, 2545.72, 2513.38, 2491.57, 2496.05,
    2466.45, 2442.72, 2420.53, 2381.54, 2388.09, 2340.61, 2335.03, 2318.93, 2319.05,
    2308.23, 2262.23, 2235.78, 2259.27, 2221.05, 2202.69, 2184.29, 2170.07, 2160.05,
    2127.68, 2134.73, 2101.96, 2101.44, 2066.40, 2074.25, 2063.68, 2048.12, 2031.87
]

# the default spline fit, `interp_method='interp1d'`
kneedle = KneeLocator(x, y, S=1.0, curve='convex', direction='decreasing', interp_method='interp1d')
kneedle.plot_knee_normalized()
```
![](images/bumpy_line.png)

```python
# The same data, only using a polynomial fit this time.
kneedle = KneeLocator(x, y, S=1.0, curve='convex', direction='decreasing', interp_method='polynomial')
kneedle.plot_knee_normalized()
```
![](images/bumpy_line.smoothed.png)

## Application

Find the optimal number of clusters (k) to use in k-means clustering.
See the tutorial in the notebooks folder, this can be achieved with the `direction` keyword argument:

```python
KneeLocator(x, y, curve='convex', direction='decreasing')
```

![](images/knee.png)

## Contributing

Contributions are welcome, if you have suggestions or would like to make improvements please submit an issue or pull request.                             

## Citation

Finding a “Kneedle” in a Haystack:
Detecting Knee Points in System Behavior
Ville Satopa
†
, Jeannie Albrecht†
, David Irwin‡
, and Barath Raghavan§
†Williams College, Williamstown, MA
‡University of Massachusetts Amherst, Amherst, MA
§
International Computer Science Institute, Berkeley, CA
