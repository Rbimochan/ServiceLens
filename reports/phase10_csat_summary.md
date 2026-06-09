# Phase 10 - CSAT Summary

`CSAT Score` is complete for all 85,907 records.

| Metric | Value |
|---|---:|
| Mean | 4.2422 |
| Median | 5 |
| Mode | 5 |
| Score 5 share | 69.40% |
| Low CSAT, scores 1–2 | 12,513 (14.57%) |
| High CSAT, scores 4–5 | 70,836 (82.46%) |
| Largest-to-smallest score-class ratio | 46.47:1 |
| Skewness | -1.6708 |

The target is strongly concentrated at score 5. This creates class imbalance and means overall accuracy will be insufficient for later classification evaluation. Stratified splitting and minority-class metrics are required.

Phase 8 low CSAT uses scores 1–2. The existing `low_csat_flag` uses scores 1–3 and must not be treated as the same outcome definition.
