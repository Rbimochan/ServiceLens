# Phase 12 - Random Forest

## Method

The model used 250 trees, `min_samples_leaf=5`, balanced class weights, and `random_state=42`. It can learn nonlinear interactions but is less directly interpretable.

## Test Results

| Metric | Score |
|---|---:|
| Accuracy | 0.6858 |
| Precision | 0.2605 |
| Recall | 0.5832 |
| F1 | 0.3601 |
| ROC-AUC | 0.6958 |

Metrics treat low CSAT (`1`) as the positive class. The default probability threshold of 0.50 was used for classification metrics.
