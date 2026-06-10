# Phase 13 - Class Imbalance Handling

The training target contains approximately 15% low-CSAT cases. Three approaches were compared using the tuned architecture.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Unweighted tuned | 0.8487 | 0.5182 | 0.0292 | 0.0552 | 0.7050 |
| Balanced tuned | 0.6572 | 0.2525 | 0.6431 | 0.3626 | 0.7045 |
| Random oversampling | 0.6636 | 0.2541 | 0.6300 | 0.3622 | 0.6969 |

**Best approach by F1: Balanced tuned.**

- Class weighting adjusts loss contribution without duplicating records.
- Random oversampling duplicates minority training records until classes are equal.
- SMOTE was not applied because the feature set contains nominal categories represented by integer codes. Standard SMOTE would interpolate invalid synthetic category values, and `imbalanced-learn` is not installed. SMOTENC could be assessed later with an explicit dependency and nested validation.

All comparisons use the same untouched test set.
