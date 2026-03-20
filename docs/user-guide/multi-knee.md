# Multi-Knee Detection

By default, `KneeLocator` returns the **first** knee point found (offline mode). To detect **all** knee points in a curve, use online mode.

## Online vs. Offline Mode

### Offline Mode (default)

With `online=False` (the default), `KneeLocator` stops at the first knee detected:

```python
import numpy as np
from kneed import KneeLocator

np.random.seed(23)
x = range(1, 1001)
y = sorted(np.random.gamma(0.5, 1.0, 1000), reverse=True)

kl = KneeLocator(x, y, curve="convex", direction="decreasing", online=False)
print(kl.knee)  # Returns the first knee found
```

### Online Mode

With `online=True`, the algorithm scans the entire curve, collecting all knee points and "correcting" previous detections as it goes. The final `kl.knee` value is the last (most significant) knee found:

```python
kl = KneeLocator(x, y, curve="convex", direction="decreasing", online=True)
print(kl.knee)  # Returns the last (corrected) knee found
```

## Accessing All Knees

When using online mode, all detected knee points are available via the `all_knees` attributes:

```python
kl = KneeLocator(x, y, curve="convex", direction="decreasing", online=True)

# x values of all detected knees
print(kl.all_knees)        # set of x values
print(kl.all_knees_y)      # list of corresponding y values

# Normalized values
print(kl.all_norm_knees)   # set of normalized x values
print(kl.all_norm_knees_y) # list of normalized y values
```

!!! note
    The `all_knees` attribute is a `set`, so knee values are unique but unordered. The `all_knees_y` attribute is a `list` that preserves the order of detection.

## Elbow Aliases

If you prefer "elbow" terminology, equivalent properties are available:

```python
kl.all_elbows        # same as kl.all_knees
kl.all_elbows_y      # same as kl.all_knees_y
kl.all_norm_elbows   # same as kl.all_norm_knees
kl.all_norm_elbows_y # same as kl.all_norm_knees_y
```

## Example: Bumpy Curve

Curves with multiple local maxima in the difference curve produce multiple knee points:

```python
from kneed import DataGenerator, KneeLocator

x, y = DataGenerator.bumpy()
kl = KneeLocator(x, y, curve="concave", direction="increasing", online=True)

print(f"Primary knee: {kl.knee}")
print(f"All knees: {sorted(kl.all_knees)}")
print(f"Number of knees found: {len(kl.all_knees)}")
```

## When to Use Online Mode

| Scenario | Mode |
|----------|------|
| Need just the first/most obvious knee | Offline (`online=False`) |
| Want to find the most significant knee | Online (`online=True`) |
| Need all knee points in a bumpy curve | Online (`online=True`), read `all_knees` |
| Performance-sensitive applications | Offline (stops early) |
