# Troubleshooting

Common issues and how to resolve them.

## `knee` is `None`

If `kl.knee` returns `None`, no knee point was detected. Common causes:

### Wrong `curve` or `direction`

This is the most common issue. If `curve` or `direction` don't match your data, the algorithm won't find a knee.

```python
from kneed import KneeLocator, DataGenerator

x, y = DataGenerator.figure2()

# Wrong direction — returns None
kl = KneeLocator(x, y, curve="concave", direction="decreasing")
print(kl.knee)  # None

# Correct direction
kl = KneeLocator(x, y, curve="concave", direction="increasing")
print(kl.knee)  # 0.222
```

**Fix**: Use [`find_shape()`](find-shape.md) to auto-detect, or plot your data to determine the correct values.

### Data is too flat or linear

If the data has no meaningful curvature (e.g., a straight line), there's no knee to detect.

```python
import numpy as np

x = np.arange(10)
y = x  # Perfectly linear — no knee

kl = KneeLocator(x, y, curve="concave", direction="increasing")
print(kl.knee)  # None
```

### Sensitivity (`S`) is too high

A high `S` value makes the algorithm more conservative. Try lowering it:

```python
# Too conservative
kl = KneeLocator(x, y, curve="convex", direction="decreasing", S=200)
print(kl.knee)  # May be None or late

# More sensitive
kl = KneeLocator(x, y, curve="convex", direction="decreasing", S=1)
print(kl.knee)  # Earlier knee detection
```

See the [S parameter guide](parameters.md#s-sensitivity) for details.

## Wrong Knee Detected

If a knee is detected but it's not where you expect:

### Try online mode

Offline mode returns the **first** knee found, which may not be the most significant:

```python
kl = KneeLocator(x, y, curve="convex", direction="decreasing", online=True)
print(kl.knee)  # Often a better result
```

### Adjust sensitivity

The `S` parameter controls how early or late a knee is detected. Experiment with different values:

```python
for s in [1, 3, 5, 10]:
    kl = KneeLocator(x, y, curve="convex", direction="decreasing", S=s)
    print(f"S={s}: knee={kl.knee}")
```

### Try polynomial interpolation

If your data is noisy, polynomial interpolation can smooth out the curve:

```python
kl = KneeLocator(
    x, y, curve="convex", direction="decreasing",
    interp_method="polynomial", polynomial_degree=7,
)
```

See the [interp_method guide](parameters.md#interp_method) for details.

## Debugging with Internal Data

`KneeLocator` exposes intermediate calculation data that can help you understand what's happening:

```python
kl = KneeLocator(x, y, curve="concave", direction="increasing")

# Plot the normalized difference curve
import matplotlib.pyplot as plt

plt.plot(kl.x_difference, kl.y_difference, label="difference curve")
plt.plot(kl.x_difference_maxima, kl.y_difference_maxima, "ro", label="maxima")
plt.plot(kl.x_difference_minima, kl.y_difference_minima, "go", label="minima")
plt.legend()
plt.title("Difference Curve")
plt.show()
```

Key attributes for debugging:

| Attribute | Description |
|-----------|-------------|
| `x_normalized`, `y_normalized` | Normalized input data |
| `x_difference`, `y_difference` | The difference curve |
| `maxima_indices` | Indices of local maxima on the difference curve |
| `minima_indices` | Indices of local minima on the difference curve |
| `Tmx` | Threshold values for each maximum |

## scipy `interp1d` Deprecation Warning

If you see a deprecation warning about `scipy.interpolate.interp1d`, you can suppress it or switch to polynomial interpolation:

```python
# Option 1: Use polynomial interpolation instead
kl = KneeLocator(x, y, curve="concave", interp_method="polynomial")

# Option 2: Suppress the warning
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="scipy")
kl = KneeLocator(x, y, curve="concave")
```

## Plotting Errors

If you get a `ModuleNotFoundError` when calling `plot_knee()` or `plot_knee_normalized()`, install matplotlib:

```bash
pip install kneed[plot]
```

Matplotlib is an optional dependency and is only required for the plotting methods.
