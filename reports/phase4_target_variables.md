# Phase 4 - Target Variables

## Purpose

This report documents the target variables available in the processed ServiceLens dataset. It identifies the original CSAT target and engineered CSAT target variants, explains their business meaning, and defines appropriate future modeling use.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Target Variable Summary

| Target Variable | Source | Business Meaning | Modeling Use |
|---|---|---|---|
| `CSAT Score` | Original dataset column | Original customer satisfaction rating recorded from the survey. | Preserve as the original target reference; use `csat_score` for modeling after numeric standardization. |
| `csat_score` | Engineered from `CSAT Score` | Numeric standardized version of the customer satisfaction rating. | Main target for regression-style modeling or direct CSAT score analysis. |
| `low_csat_flag` | Engineered from `CSAT Score` | Binary flag identifying tickets with lower customer satisfaction scores. | Candidate binary classification target for predicting low satisfaction risk. |
| `high_csat_flag` | Engineered from `CSAT Score` | Binary flag identifying tickets with higher customer satisfaction scores. | Candidate binary classification target for predicting high satisfaction outcomes. |

## CSAT Target Definitions

| Variable | Definition | Verified Count / Status |
|---|---|---:|
| `csat_score` | Numeric version of `CSAT Score`. | 85,907 valid values; 0 invalid values |
| `low_csat_flag` | 1 when `csat_score <= 3`, otherwise 0. | 15,071 true values |
| `high_csat_flag` | 1 when `csat_score >= 4`, otherwise 0. | 70,836 true values |

## CSAT Score Distribution

| CSAT Score | Count |
|---:|---:|
| 1 | 11,230 |
| 2 | 1,283 |
| 3 | 2,558 |
| 4 | 11,219 |
| 5 | 59,617 |

## Recommended Modeling Use

- Use `csat_score` when the research task treats satisfaction as an ordered or numeric rating.
- Use `low_csat_flag` when the research task focuses on identifying dissatisfied or at-risk customers.
- Use `high_csat_flag` when the research task focuses on identifying positive satisfaction outcomes.
- Select only one target variable for a given model to avoid target leakage and conflicting objectives.
- Keep `CSAT Score` as the original reference field, but prefer `csat_score` for modeling because it is standardized as numeric.

## Risks and Notes

- The target is imbalanced toward high satisfaction scores, especially score 5.
- `low_csat_flag` and `high_csat_flag` are complementary target variants and should not be used together as predictors.
- Target definitions should be stated clearly in any later modeling or Tableau reporting.
- No model has been trained in this step.
