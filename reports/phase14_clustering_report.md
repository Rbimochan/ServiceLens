# Phase 14 - Clustering Analysis Report

## Dataset and Preprocessing

The analysis used 82,779 valid interactions and seven source fields. Categorical variables were one-hot encoded. Response time was log-transformed and standardized; CSAT was standardized. Identifiers and names were excluded.

## K Selection

K=2 through K=8 were evaluated using full-data inertia and a reproducible 10,000-row silhouette sample. The selected cluster count is **K=2**.

## Model Comparison

| Method | Silhouette | Davies-Bouldin | Inertia |
|---|---|---|---|
| K-Means | 0.2740 | 1.5757 | 355,679.76 |
| Bisecting K-Means | 0.2740 | 1.5758 | 355,679.78 |

**Selected clustering method: K-Means.**

## Cluster Profiles

| Cluster | Business Profile | Count | Proportion | Avg CSAT | Avg Response Minutes | Median Response Minutes | Dominant Channel | Dominant Category | Dominant Tenure | Dominant Shift |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Efficient Resolution Interactions | 69464 | 83.92% | 4.806 | 135.2 | 5.0 | Inbound | Returns | >90 | Morning |
| 1 | Dissatisfied High-Effort Interactions | 13315 | 16.08% | 1.265 | 389.5 | 27.0 | Inbound | Returns | >90 | Morning |

## RQ3 Answer

**What support interaction profiles emerge?**

The analysis finds 2 overlapping but measurable interaction profiles: Efficient Resolution Interactions, Dissatisfied High-Effort Interactions. The clearest differentiation is based on response effort, satisfaction, and operational issue mix. These profiles can support service-routing and process investigation, but the modest separation metrics mean they should not be treated as fixed customer types without stability testing.

## Limitations

- Clusters depend on encoding, scaling, selected fields, and K.
- CSAT is included as an unsupervised clustering dimension, so satisfaction differences are partly designed into the geometry.
- Silhouette uses a fixed sample for computational practicality.
- Cluster stability across time and resampled datasets has not yet been tested.
- Profiles describe interactions, not permanent customer identities.
