# Phase 14 - Feature Scaling

- Categorical encoding: one-hot encoding with unknown-category handling
- Numeric transformation: `log1p` applied to non-negative response time to reduce extreme skew
- Numeric scaling: z-score standardization for transformed response time and CSAT
- Final matrix dimensions: 82,779 rows x 84 columns
- Encoded feature count: 84
- Matrix format: sparse during clustering; converted to dense only for Davies-Bouldin evaluation

The transformation prevents raw response-time magnitude from overwhelming categorical distances while retaining the ordering of delays.
