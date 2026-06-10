# Phase 13 - Threshold Optimization

Thresholds were evaluated on the strongest imbalance-handling candidate, **Balanced tuned**.

| Threshold | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---:|---:|---:|---:|---:|---:|
| 0.20 | 0.2405 | 0.1633 | 0.9725 | 0.2797 | 0.7045 |
| 0.30 | 0.3495 | 0.1790 | 0.9175 | 0.2996 | 0.7045 |
| 0.40 | 0.5252 | 0.2137 | 0.7955 | 0.3369 | 0.7045 |
| 0.50 | 0.6572 | 0.2525 | 0.6431 | 0.3626 | 0.7045 |
| 0.60 | 0.7401 | 0.2905 | 0.4953 | 0.3662 | 0.7045 |
| 0.70 | 0.8252 | 0.3679 | 0.2127 | 0.2696 | 0.7045 |

**Selected business threshold: 0.60.**

This threshold maximizes low-CSAT F1 among the required candidates, using precision as the tie-breaker. Recall remains visible because missed dissatisfied customers carry direct business risk. A production threshold should ultimately be selected using intervention capacity and the relative costs of false positives and false negatives.
