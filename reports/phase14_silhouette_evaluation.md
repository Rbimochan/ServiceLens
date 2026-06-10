# Phase 14 - Silhouette Evaluation

| Method | Silhouette | Davies-Bouldin | Inertia |
|---|---|---|---|
| K-Means | 0.2740 | 1.5757 | 355,679.76 |
| Bisecting K-Means | 0.2740 | 1.5758 | 355,679.78 |

Higher silhouette scores indicate stronger separation and cohesion. Scores were calculated on the same fixed 10,000-row sample.

**Best method by silhouette: K-Means.**

The absolute scores should be interpreted cautiously because mixed operational data often forms overlapping profiles rather than sharply separated natural groups.
