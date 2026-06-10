# Phase 11 - Exploratory CSAT Driver Analysis

## Purpose

This analysis ranks observed associations with CSAT for prioritization. It does not claim causal drivers and does not replace multivariable modeling.

## Relative Driver Ranking

| Variable | Eta-squared | Relative Evidence | Reason |
|---|---:|---|---|
| Response-time band | 0.04495 | Higher | Largest measured group separation; clear decline with delay |
| Sub-category | 0.03065 | Higher | Meaningful differences across specific issue types |
| Category | 0.00852 | Medium | Cancellation and product/order groups underperform |
| Channel | 0.00228 | Medium operational priority | Small overall effect, but Email has a clear gap |
| Agent tenure | 0.00233 | Lower | On Job Training is weaker, but group effect is small |
| Shift | 0.00182 | Lower | Morning is weaker, but group effect is small |

## Priority Areas for Phase 12

1. Validate the response-time relationship while controlling for category, sub-category, and channel.
2. Examine high-volume, low-CSAT issue groups such as Installation/demo and delayed or cancellation-related cases.
3. Test whether the Email gap remains after accounting for response time and issue mix.
4. Evaluate On Job Training and Morning-shift differences with appropriate controls.
5. Avoid duplicate response-time units and redundant missingness flags in modeling.

## Limitations

All eta-squared values are modest, and unobserved case complexity may affect every comparison. Small categories can produce unstable averages. These findings should be treated as hypotheses for structured statistical analysis.

