# Phase 14 - Bisecting K-Means

Bisecting K-Means used K=2, `n_init=10`, `random_state=42`, and the `biggest_inertia` splitting strategy.

| Cluster | Count | Proportion |
|---:|---:|---:|
| 0 | 13,317 | 16.09% |
| 1 | 69,462 | 83.91% |

- Inertia: 355,679.78
- Sampled silhouette: 0.2740
- Davies-Bouldin index: 1.5758

The same preprocessed matrix and cluster count were used for a direct comparison with standard K-Means.
