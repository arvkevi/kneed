# kneed
 Knee-point detection in Python

[![Downloads](https://pepy.tech/badge/kneed)](https://pepy.tech/project/kneed) [![Downloads](https://pepy.tech/badge/kneed/week)](https://pepy.tech/project/kneed) ![Dependents](https://badgen.net/github/dependents-repo/arvkevi/kneed/?icon=github) [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/arvkevi/ikneed/main/ikneed.py) [![codecov](https://codecov.io/gh/arvkevi/kneed/branch/main/graph/badge.svg)](https://codecov.io/gh/arvkevi/kneed)[![DOI](https://zenodo.org/badge/113799037.svg)](https://zenodo.org/badge/latestdoi/113799037)


This repository is an attempt to implement the kneedle algorithm, published [here](https://www1.icsi.berkeley.edu/~barath/papers/kneedle-simplex11.pdf). Given a set of `x` and `y` values, `kneed` will return the knee point of the function. The knee point is the point of maximum curvature.

![](https://raw.githubusercontent.com/arvkevi/kneed/main/images/functions_args_summary.png)

## Table of contents
- [Installation](#installation)
- [Usage](#usage)
  - [Input Data](#input-data)
  - [Find Knee](#find-knee)
  - [Visualize](#visualize)
- [Documentation](#documentation)
- [Interactive](#interactive)
- [Contributing](#contributing)
- [Citation](#citation)

## Installation  
`kneed` has been tested with Python 3.7, 3.8, 3.9, and 3.10.

**anaconda**
```bash
$ conda install -c conda-forge kneed
```

**pip**
```bash
$ pip install kneed # To install only knee-detection algorithm
$ pip install kneed[plot] # To also install plotting functions for quick visualizations
```

**Clone from GitHub**
```bash
$ git clone https://github.com/arvkevi/kneed.git && cd kneed
$ pip install -e .
```

## Usage
These steps introduce how to use `kneed` by reproducing Figure 2 from the manuscript.

### Input Data
The `DataGenerator` class is only included as a utility to generate sample datasets. 
>  Note: `x` and `y` must be equal length arrays.
```python
from kneed import DataGenerator, KneeLocator

x, y = DataGenerator.figure2()

print([round(i, 3) for i in x])
print([round(i, 3) for i in y])

[0.0, 0.111, 0.222, 0.333, 0.444, 0.556, 0.667, 0.778, 0.889, 1.0]
[-5.0, 0.263, 1.897, 2.692, 3.163, 3.475, 3.696, 3.861, 3.989, 4.091]
```

### Find Knee  
The knee (or elbow) point is calculated simply by instantiating the `KneeLocator` class with `x`, `y` and the appropriate `curve` and `direction`.  
Here, `kneedle.knee` and/or `kneedle.elbow` store the point of maximum curvature.

```python
kneedle = KneeLocator(x, y, S=1.0, curve="concave", direction="increasing")

print(round(kneedle.knee, 3))
0.222

print(round(kneedle.elbow, 3))
0.222
```

The knee point returned is a value along the `x` axis. The `y` value at the knee can be identified:

```python
print(round(kneedle.knee_y, 3))
1.897
```

### Visualize
The `KneeLocator` class also has two plotting functions for quick visualizations.
**Note that all (x, y) are transformed for the normalized plots**
```python
# Normalized data, normalized knee, and normalized distance curve.
kneedle.plot_knee_normalized()
```

![](https://raw.githubusercontent.com/arvkevi/kneed/main/images/figure2.knee.png)

```python
# Raw data and knee.
kneedle.plot_knee()
```

![](https://raw.githubusercontent.com/arvkevi/kneed/main/images/figure2.knee.raw.png)

## Documentation
Documentation of the parameters and a full API reference can be found [here](https://kneed.readthedocs.io/).

## Interactive
An interactive streamlit app was developed to help users explore the effect of tuning the parameters.
There are two sites where you can test out kneed by copy-pasting your own data:
1. https://share.streamlit.io/arvkevi/ikneed/main/ikneed.py
2. https://ikneed.herokuapp.com/

You can also run your own version -- head over to the [source code for ikneed](https://github.com/arvkevi/ikneed).

![ikneed](images/ikneed.gif)

## Contributing

Contributions are welcome, please refer to [CONTRIBUTING](https://github.com/arvkevi/kneed/blob/main/CONTRIBUTING.md) 
to learn more about how to contribute.                            

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
