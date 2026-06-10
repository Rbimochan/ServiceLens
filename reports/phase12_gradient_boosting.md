# Phase 12 - Gradient Boosting

## Method

A histogram gradient-boosted tree model used ordinal-encoded categoricals marked as categorical features, balanced class weights, 200 boosting iterations, and `random_state=42`.

## Test Results

| Metric | Score |
|---|---:|
| Accuracy | 0.6592 |
| Precision | 0.2531 |
| Recall | 0.6394 |
| F1 | 0.3626 |
| ROC-AUC | 0.7038 |

Metrics treat low CSAT (`1`) as the positive class. The default probability threshold of 0.50 was used for classification metrics.
