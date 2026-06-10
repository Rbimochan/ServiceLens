# Phase 12 - Model Comparison

## Ranking by ROC-AUC

1. **Gradient Boosting** - ROC-AUC 0.7038, F1 0.3626, recall 0.6394
2. **Random Forest** - ROC-AUC 0.6958, F1 0.3601, recall 0.5832
3. **Logistic Regression** - ROC-AUC 0.6660, F1 0.3254, recall 0.6423

## Tradeoffs

- Logistic Regression is the most interpretable baseline and easiest to explain, but it assumes additive linear effects after encoding.
- Random Forest captures nonlinear interactions and is robust, but its probabilities and global explanations require additional analysis.
- Gradient Boosting captures nonlinear structure efficiently. In this run it produced the strongest ROC-AUC and the highest F1 score.

## Selected Model

**Best model: Gradient Boosting**

The selection uses ROC-AUC as the primary criterion because Phase 12 evaluates minority-class ranking ability across thresholds. F1 and recall remain important deployment metrics and should be tuned in Phase 13.
