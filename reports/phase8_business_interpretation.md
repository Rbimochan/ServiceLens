# Phase 8 - Business Interpretation

## Satisfaction Level

The mean CSAT is 4.2422, while the median and mode are both 5. High CSAT scores 4–5 account for 82.46% of responses. These measures indicate a predominantly satisfied survey population.

## Dissatisfaction Level

Low CSAT scores 1–2 account for 12,513 records, or 14.57%. Score 1 alone represents 13.07%, showing that dissatisfaction is concentrated more heavily in the minimum rating than in score 2.

## Distribution Shape

The distribution is strongly left-skewed, with skewness of -1.6708. Score 5 represents 69.40% of records, so averages can hide the size and operational importance of the dissatisfied minority.

## Classification Challenges

- The 46.47:1 largest-to-smallest class ratio creates strong multiclass imbalance.
- Models may overpredict score 5 without class-sensitive evaluation.
- Binary satisfaction tasks must use an explicit threshold because Phase 8 low CSAT (1–2) differs from the existing 1–3 low flag.
- Later modeling should report minority-class performance and avoid relying only on accuracy.

These are verified baseline interpretations, not causal conclusions.
