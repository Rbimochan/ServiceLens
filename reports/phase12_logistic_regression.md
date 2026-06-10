# Phase 12 - Logistic Regression

## Method

Categorical values were one-hot encoded, numeric values were median-imputed and standardized, and balanced class weights were used. This is the interpretable linear baseline.

## Test Results

| Metric | Score |
|---|---:|
| Accuracy | 0.5962 |
| Precision | 0.2179 |
| Recall | 0.6423 |
| F1 | 0.3254 |
| ROC-AUC | 0.6660 |

Metrics treat low CSAT (`1`) as the positive class. The default probability threshold of 0.50 was used for classification metrics.
