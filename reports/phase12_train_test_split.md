# Phase 12 - Train/Test Split

The modeling data was split with `test_size=0.20`, `random_state=42`, and stratification by `low_csat_binary`.

| Split | Total | High CSAT (0) | Low CSAT (1) | Low-CSAT Rate |
|---|---:|---:|---:|---:|
| Train | 64,240 | 54,500 | 9,740 | 15.16% |
| Test | 16,061 | 13,626 | 2,435 | 15.16% |

Stratification preserves the class imbalance in both partitions. Balanced class weighting was used during training so the models did not optimize only for the majority high-CSAT class.
