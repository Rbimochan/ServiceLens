# Phase 12 - Classification Report

## Research Question

**RQ2: Can customer satisfaction be predicted using support interaction data?**

**Answer: YES, with limited-to-moderate predictive ability.**

The models detect predictive signal, but Phase 12 results are baseline estimates rather than evidence of production readiness.

## Dataset and Target

- Modeling rows: 80,301
- Train rows: 64,240
- Test rows: 16,061
- Target: `low_csat_binary`
- `0`: CSAT 4-5
- `1`: CSAT 1-2
- Split: 80/20, stratified, `random_state=42`

## Model Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.5962 | 0.2179 | 0.6423 | 0.3254 | 0.6660 |
| Random Forest | 0.6858 | 0.2605 | 0.5832 | 0.3601 | 0.6958 |
| Gradient Boosting | 0.6592 | 0.2531 | 0.6394 | 0.3626 | 0.7038 |

## Best Model

**Gradient Boosting**

- Accuracy: 0.6592
- Precision: 0.2531
- Recall: 0.6394
- F1: 0.3626
- ROC-AUC: 0.7038

The best model was selected by ROC-AUC. Balanced class weighting prioritizes detection of the minority low-CSAT class, so accuracy alone is not the selection criterion.

## Limitations

- Results come from one reproducible holdout split and require cross-validation in Phase 13.
- Threshold 0.50 was not tuned for operational precision-recall costs.
- Invalid negative response durations and neutral CSAT scores were excluded.
- The available features may not capture issue complexity, customer history, or service-resolution quality.
- Observational patterns do not prove causal relationships.
- Model calibration, feature importance, fairness, drift, and external validation remain untested.

## Phase 13 Direction

Tune hyperparameters and the decision threshold, add cross-validation and confidence intervals, inspect feature importance, test calibration, and confirm that performance is stable across channels and issue categories.
