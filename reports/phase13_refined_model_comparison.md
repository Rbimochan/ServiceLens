# Phase 13 - Refined Model Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Original Gradient Boosting | 0.6592 | 0.2531 | 0.6394 | 0.3626 | 0.7038 |
| Tuned Gradient Boosting | 0.8487 | 0.5182 | 0.0292 | 0.0552 | 0.7050 |
| Balanced Gradient Boosting | 0.6572 | 0.2525 | 0.6431 | 0.3626 | 0.7045 |
| Threshold Optimized Model | 0.7401 | 0.2905 | 0.4953 | 0.3662 | 0.7045 |

## Ranking by Low-CSAT F1

1. **Threshold Optimized Model** - F1 0.3662, precision 0.2905, recall 0.4953, ROC-AUC 0.7045
2. **Original Gradient Boosting** - F1 0.3626, precision 0.2531, recall 0.6394, ROC-AUC 0.7038
3. **Balanced Gradient Boosting** - F1 0.3626, precision 0.2525, recall 0.6431, ROC-AUC 0.7045
4. **Tuned Gradient Boosting** - F1 0.0552, precision 0.5182, recall 0.0292, ROC-AUC 0.7050

The threshold-optimized candidate uses threshold 0.60 on the best imbalance approach (Balanced tuned). ROC-AUC is unchanged by threshold selection; precision, recall, F1, and accuracy change.

**Recommended model: Threshold Optimized Model.**
