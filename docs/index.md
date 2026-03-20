# kneed

**Knee-point detection in Python**

`kneed` is a Python library for detecting knee (elbow) points in curves using the [Kneedle algorithm](https://www1.icsi.berkeley.edu/~barath/papers/kneedle-simplex11.pdf). Given a set of `x` and `y` values, it identifies the point of maximum curvature — the "knee" or "elbow" of the curve.

![Summary of curve and direction arguments](https://raw.githubusercontent.com/arvkevi/kneed/main/images/functions_args_summary.png)

## Key Features

- **Knee and elbow detection** for concave and convex curves
- **Increasing and decreasing** function support
- **Automatic shape detection** with [`find_shape()`](user-guide/find-shape.md)
- **Multiple knee detection** via [online mode](user-guide/multi-knee.md)
- **Tunable sensitivity** parameter (`S`) for fine-grained control
- **Multiple interpolation methods** — `interp1d` and `polynomial`
- **Built-in plotting** for quick visualizations

## Quick Example

```python
from kneed import KneeLocator, DataGenerator

x, y = DataGenerator.figure2()
kl = KneeLocator(x, y, curve="concave", direction="increasing")

print(kl.knee)    # 0.222
print(kl.knee_y)  # 1.897
```

## Interactive App

Explore `kneed` parameters interactively with the [Streamlit app](https://share.streamlit.io/arvkevi/ikneed/main/ikneed.py):

![ikneed interactive app](https://raw.githubusercontent.com/arvkevi/kneed/main/images/ikneed.gif)

## Citation

If you use `kneed` in your research, please cite:

> Satopa, V., Albrecht, J., Irwin, D., and Raghavan, B. (2011). "Finding a 'Kneedle' in a Haystack: Detecting Knee Points in System Behavior." *31st International Conference on Distributed Computing Systems Workshops*, pp. 166-171.
