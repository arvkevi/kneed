# Getting Started

## Installation

`kneed` requires Python 3.8 or later.

=== "pip"

    ```bash
    pip install kneed              # knee-detection only
    pip install kneed[plot]        # also install matplotlib for visualizations
    ```

=== "conda"

    ```bash
    conda install -c conda-forge kneed
    ```

=== "From source"

    ```bash
    git clone https://github.com/arvkevi/kneed.git && cd kneed
    pip install -e .
    ```

## What is a Knee Point?

A **knee point** (or **elbow point**) is the point of maximum curvature on a curve — the spot where the rate of change shifts most dramatically. It's commonly used in machine learning to determine optimal parameters, such as the number of clusters in K-means or the number of components in PCA.

## Minimal Example

```python
from kneed import KneeLocator, DataGenerator

# Generate sample data (Figure 2 from the Kneedle paper)
x, y = DataGenerator.figure2()

# Find the knee point
kl = KneeLocator(x, y, curve="concave", direction="increasing")

print(kl.knee)    # 0.222 — the x value of the knee
print(kl.knee_y)  # 1.897 — the y value at the knee
```

## Choosing `curve` and `direction`

The two most important parameters are `curve` and `direction`:

| Parameter   | Values                       | Description                                      |
|-------------|------------------------------|--------------------------------------------------|
| `curve`     | `"concave"` or `"convex"`    | Concave curves have knees, convex curves have elbows |
| `direction` | `"increasing"` or `"decreasing"` | The overall trend of the data from left to right |

!!! tip
    Not sure which values to use? Let `kneed` auto-detect them:

    ```python
    from kneed import find_shape

    direction, curve = find_shape(x, y)
    kl = KneeLocator(x, y, curve=curve, direction=direction)
    ```

    See the [find_shape guide](user-guide/find-shape.md) for details.

## Visualizing Results

`kneed` includes two built-in plotting methods (requires `pip install kneed[plot]`):

```python
# Plot the raw data with the knee point marked
kl.plot_knee()
```

![Raw knee point](https://raw.githubusercontent.com/arvkevi/kneed/main/images/figure2.knee.raw.png)

```python
# Plot the normalized curve and difference curve
kl.plot_knee_normalized()
```

![Normalized knee point](https://raw.githubusercontent.com/arvkevi/kneed/main/images/figure2.knee.png)

## Next Steps

- **[Parameters Guide](user-guide/parameters.md)** — learn how to tune sensitivity, interpolation method, and more
- **[Curve Types](user-guide/curve-types.md)** — visual guide to all four curve/direction combinations
- **[Real-World Examples](examples/kmeans-elbow.md)** — K-means elbow method, PCA, and more
- **[API Reference](api.md)** — full class and method documentation
