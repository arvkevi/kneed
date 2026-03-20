# Auto-Detection with find_shape

The `find_shape()` function automatically detects the `direction` and `curve` type of your data, removing the guesswork from setting these parameters.

## Usage

```python
from kneed import KneeLocator, DataGenerator, find_shape

x, y = DataGenerator.figure2()

# Auto-detect the curve shape
direction, curve = find_shape(x, y)
print(f"direction={direction}, curve={curve}")
# direction=increasing, curve=concave

# Use the detected values
kl = KneeLocator(x, y, curve=curve, direction=direction)
print(kl.knee)
```

## How It Works

`find_shape()` fits a second-degree polynomial to the data and examines the coefficients:

1. **Direction**: determined by the sign of the linear coefficient — positive means increasing, negative means decreasing.
2. **Curve type**: determined by the sign of the quadratic coefficient — negative means concave, positive means convex.

## Return Value

`find_shape()` returns a tuple of two strings:

```python
(direction, curve)
```

Where:

- `direction` is `"increasing"` or `"decreasing"`
- `curve` is `"concave"` or `"convex"`

## When to Use

`find_shape()` is helpful when:

- You're processing many datasets programmatically and can't manually inspect each one
- You're building a pipeline that needs to auto-detect knee points
- You're not sure whether your data is concave or convex

## Limitations

!!! warning
    `find_shape()` uses a simple polynomial fit and may not correctly identify the shape for:

    - **Very noisy data** — noise can overwhelm the polynomial fit
    - **Multi-modal curves** — curves with multiple peaks/valleys
    - **S-shaped curves** — curves that change from concave to convex

    In these cases, visually inspect your data and set `curve` and `direction` manually.
