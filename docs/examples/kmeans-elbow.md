# K-Means Elbow Method

The "elbow method" is a popular technique for choosing the optimal number of clusters in K-means clustering. As `k` increases, the inertia (within-cluster sum of squares) decreases. The elbow point is where adding more clusters yields diminishing returns.

## Example

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from kneed import KneeLocator

# Generate sample data with 4 clusters
X, _ = make_blobs(n_samples=500, centers=4, n_features=2, random_state=42)

# Compute inertia for k=1 to k=10
inertias = []
K = range(1, 11)
for k in K:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)

# Find the elbow
kl = KneeLocator(list(K), inertias, curve="convex", direction="decreasing")
print(f"Optimal k: {kl.elbow}")  # Should be 4
```

## Visualizing

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(K, inertias, "bo-")
plt.vlines(kl.elbow, plt.ylim()[0], plt.ylim()[1], linestyles="--", colors="r", label=f"elbow = {kl.elbow}")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("K-Means Elbow Method")
plt.legend()
plt.show()
```

## Tips

- Use `curve="convex"` and `direction="decreasing"` for inertia curves
- If the elbow isn't clear, try adjusting `S` (lower values detect earlier elbows)
- For noisy inertia values, `interp_method="polynomial"` can help smooth the curve
