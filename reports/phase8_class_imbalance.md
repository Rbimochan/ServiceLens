# Phase 8 - Class Imbalance

## Class Frequencies

| Score | Count | Percentage |
|---:|---:|---:|
| 1 | 11,230 | 13.07% |
| 2 | 1,283 | 1.49% |
| 3 | 2,558 | 2.98% |
| 4 | 11,219 | 13.06% |
| 5 | 59,617 | 69.40% |

## Imbalance Measures

- Largest class: score 5 with 59,617 records.
- Smallest class: score 2 with 1,283 records.
- Largest-to-smallest class ratio: 46.47:1.
- Score 5 alone exceeds all other scores combined.

## Classification Implications

- Overall accuracy could be misleading because a model can favor score 5.
- Minority-class recall, precision, F1, confusion matrices, and balanced metrics will be necessary.
- Stratified splits should preserve class proportions.
- Class weighting or resampling may be considered later, but no balancing was performed in Phase 8.
