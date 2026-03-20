# Using Custom Data

`kneed` works with any paired `x` and `y` data. Here are some common patterns for loading and using your own data.

## From Lists

```python
from kneed import KneeLocator

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 2, 3.5, 4.5, 5, 5.3, 5.5, 5.6, 5.65, 5.7]

kl = KneeLocator(x, y, curve="concave", direction="increasing")
print(f"Knee: x={kl.knee}, y={kl.knee_y}")
```

## From NumPy Arrays

```python
import numpy as np
from kneed import KneeLocator

x = np.linspace(0, 10, 100)
y = np.log1p(x)  # Logarithmic curve

kl = KneeLocator(x, y, curve="concave", direction="increasing")
print(f"Knee: x={round(kl.knee, 3)}")
```

## From a CSV File

```python
import numpy as np
from kneed import KneeLocator

# Load two columns from a CSV
data = np.genfromtxt("my_data.csv", delimiter=",", skip_header=1)
x = data[:, 0]
y = data[:, 1]

kl = KneeLocator(x, y, curve="concave", direction="increasing")
print(f"Knee: x={kl.knee}")
```

## From a Pandas DataFrame

```python
import pandas as pd
from kneed import KneeLocator

df = pd.read_csv("my_data.csv")

kl = KneeLocator(
    df["x_column"].values,
    df["y_column"].values,
    curve="concave",
    direction="increasing",
)
print(f"Knee: x={kl.knee}")
```

## Auto-Detecting Shape

If you're not sure about the curve type, use `find_shape()`:

```python
from kneed import KneeLocator, find_shape

direction, curve = find_shape(x, y)
kl = KneeLocator(x, y, curve=curve, direction=direction)
print(f"Detected: {direction} {curve}, knee at x={kl.knee}")
```

## Important Notes

!!! warning "Requirements for input data"
    - `x` and `y` must be the same length
    - `x` values should be sorted in ascending order
    - Both `x` and `y` are automatically converted to NumPy arrays
    - Lists, tuples, NumPy arrays, and Pandas Series all work as input
