# Phase 15 - Effect Size Analysis

## Linear Response-Time Effect

A one-standard-deviation increase in log-transformed response time is associated with **-0.2768 CSAT points**, holding encoded predictors constant.

## Random Forest Response-Time Effects

| Response Time | Average Predicted CSAT | Change from Immediate Response |
|---:|---:|---:|
| 0 minutes | 4.462 | +0.000 |
| 5 minutes | 4.375 | -0.087 |
| 15 minutes | 4.048 | -0.415 |
| 30 minutes | 4.053 | -0.410 |
| 60 minutes | 4.006 | -0.456 |
| 240 minutes | 3.939 | -0.523 |
| 1,440 minutes | 3.659 | -0.803 |

## Selected Categorical Effects

| Variable Level | Linear Effect vs Reference |
|---|---:|
| Email vs Inbound | -0.2684 CSAT points |
| On Job Training vs 0-30 tenure | -0.1278 CSAT points |
| Morning vs Afternoon shift | -0.0471 CSAT points |

The Email contrast is derived from the fitted reference-coded coefficients because Email is the dropped channel reference. Effects are conditional associations in this specification and must not be interpreted as causal treatment effects.
