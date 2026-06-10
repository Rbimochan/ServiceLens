# Phase 14 - Davies-Bouldin Evaluation

| Method | Davies-Bouldin | Silhouette | Inertia |
|---|---|---|---|
| K-Means | 1.5757 | 0.2740 | 355,679.76 |
| Bisecting K-Means | 1.5758 | 0.2740 | 355,679.78 |

Lower Davies-Bouldin values indicate more compact, better-separated clusters.

**Best method by Davies-Bouldin index: K-Means.**

This metric was calculated on the complete transformed matrix. It is considered alongside silhouette rather than used as the sole selection criterion.
