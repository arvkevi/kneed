# PCA Component Selection

When using Principal Component Analysis (PCA), a common question is: how many components should you keep? The knee point of the cumulative explained variance curve indicates where additional components contribute diminishing information.

## Example

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_digits
import numpy as np
from kneed import KneeLocator

# Load dataset
X, _ = load_digits(return_X_y=True)

# Fit PCA with all components
pca = PCA().fit(X)

# Cumulative explained variance
cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
n_components = range(1, len(cumulative_variance) + 1)

# Find the knee
kl = KneeLocator(
    list(n_components),
    cumulative_variance.tolist(),
    curve="concave",
    direction="increasing",
)
print(f"Optimal components: {kl.knee}")
```

## Visualizing

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(n_components, cumulative_variance, "bo-", markersize=3)
plt.vlines(kl.knee, 0, 1, linestyles="--", colors="r", label=f"knee = {kl.knee}")
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("PCA Component Selection")
plt.legend()
plt.show()
```

## Tips

- Use `curve="concave"` and `direction="increasing"` for cumulative variance curves
- The knee point tells you where you get the most variance for the fewest components
- Adjust `S` to control how aggressively the knee is detected
