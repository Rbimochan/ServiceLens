# Phase 13 - Hyperparameter Tuning

`RandomizedSearchCV` evaluated 12 parameter combinations with 3-fold cross-validation, `random_state=42`, and ROC-AUC scoring.

Phase 12 used `HistGradientBoostingClassifier`. Its `max_iter` parameter is the estimator-count equivalent of `n_estimators`; `min_samples_leaf` is its supported split-regularization control rather than classic `min_samples_split`. Learning rate and tree depth were tuned directly.

## Best Parameters

- `l2_regularization`: `1.0`
- `learning_rate`: `0.08`
- `max_depth`: `5`
- `max_iter`: `300`
- `max_leaf_nodes`: `15`
- `min_samples_leaf`: `10`

- Best cross-validation ROC-AUC: 0.7105

## Holdout Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Phase 12 baseline | 0.6592 | 0.2531 | 0.6394 | 0.3626 | 0.7038 |
| Tuned unweighted | 0.8487 | 0.5182 | 0.0292 | 0.0552 | 0.7050 |
| Tuned balanced | 0.6572 | 0.2525 | 0.6431 | 0.3626 | 0.7045 |

Tuning was performed only on training folds. The unchanged Phase 12 test set was used once for the reported comparison.
