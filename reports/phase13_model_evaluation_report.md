# Phase 13 - Model Evaluation and Refinement Report

## Evaluation Summary

The exact Phase 12 gradient-boosting baseline was reproduced on the same stratified holdout split. Phase 13 added confusion-matrix analysis, error review, permutation feature importance, randomized tuning, imbalance comparisons, and threshold optimization.

## Driver Importance

Top predictive variables by holdout permutation importance:

1. response_time_minutes (0.11225)
2. Sub-category (0.08273)
3. Tenure Bucket (0.00746)
4. Agent Shift (0.00540)
5. channel_name (0.00395)

These variables help prediction but are not proven causal satisfaction drivers.

## Model Improvement

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Phase 12 baseline | 0.6592 | 0.2531 | 0.6394 | 0.3626 | 0.7038 |
| Recommended model | 0.7401 | 0.2905 | 0.4953 | 0.3662 | 0.7045 |

- F1 change: +0.0035
- Precision change: +0.0374
- Baseline ROC-AUC: 0.7038
- Final ROC-AUC: 0.7045

## Recommended Model

**Threshold Optimized Model**, using the Balanced tuned probability model and decision threshold 0.60.

- Final accuracy: 0.7401
- Final precision: 0.2905
- Final recall: 0.4953
- Final F1: 0.3662
- Final ROC-AUC: 0.7045

## Business Interpretation

The model can prioritize potentially dissatisfied customers better than random ranking, but precision remains limited. False negatives represent missed recovery opportunities; false positives consume intervention capacity. The recommended threshold improves the measured F1 tradeoff among the required candidates, but deployment still requires calibration, repeated cross-validation, cost-based threshold selection, fairness checks, and monitoring.

## Answers

1. **Which variables drive satisfaction predictions?** The ranked variables above, led by response_time_minutes, provide the strongest predictive contribution.
2. **How much did performance improve?** F1 changed by +0.0035 and precision by +0.0374 relative to the exact Phase 12 baseline.
3. **What model should be used?** Use the Threshold Optimized Model as the Phase 14-ready production candidate for further validation, not immediate deployment.
