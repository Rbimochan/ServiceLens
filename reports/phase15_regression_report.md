# Phase 15 - Regression Analysis Report

## Dataset and Models

The analysis used 82,779 valid interactions to predict continuous CSAT scores from nine operational and date/time features. Linear Regression provides coefficient-based effect estimates; Random Forest Regression captures nonlinear structure.

## Performance

| Model | R-squared | MAE | RMSE |
|---|---:|---:|---:|
| Linear Regression | 0.0825 | 0.9981 | 1.3329 |
| Random Forest Regression | 0.0600 | 1.0048 | 1.3491 |

**Best predictive model: Linear Regression.**

## Feature Importance

The leading grouped predictors are response_time_minutes, Sub-category, Tenure Bucket, issue_weekday, channel_name. The strongest variable is **response_time_minutes**.

## Effect Sizes

- A one-standard-deviation increase in log response time is associated with -0.2768 linear-model CSAT points.
- The Random Forest response-time sensitivity changes from 4.462 predicted CSAT at 0 minutes to 3.659 at 1,440 minutes, a difference of -0.803.
- Categorical coefficients in the detailed report quantify channel, issue, tenure, shift, and weekday levels relative to explicit references.

## RQ1 Answer

**Which operational factors matter most?**

The strongest predictive factors are response_time_minutes, Sub-category, Tenure Bucket, issue_weekday, channel_name, with response time and detailed issue type expected to dominate when supported by the measured ranking. Importance describes predictive contribution, not causation.

## RQ4 Answer

**What is their relative contribution and effect size?**

Relative contribution is reported through grouped holdout permutation importance and encoded Random Forest importance. Effect magnitude is reported through linear CSAT-point coefficients and the nonlinear response-time sensitivity curve. The complete ranking is documented in `phase15_driver_quantification.md`.

## Limitations

- Regression estimates are observational and do not establish causal effects.
- R-squared quantifies explained holdout variation, not business impact by itself.
- Linear coefficients depend on reference categories and feature specification.
- Random Forest importance can distribute credit across correlated predictors.
- Temporal validation, confidence intervals, and causal controls remain future work.
