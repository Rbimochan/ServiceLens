# ServiceLens Milestone 1 - Data Understanding Report

## Executive Summary

ServiceLens evaluates customer satisfaction patterns in a Kaggle customer-support dataset. The prepared dataset contains 85,907 tickets and 52 columns, including 20 retained source fields and 32 engineered preparation fields. Milestone 1 established the data dictionary, schema, quality profile, datetime validity, CSAT target behavior, and initial operational patterns.

The dataset is suitable for controlled exploratory analysis and model development after handling three major risks: critical missingness in several fields, 3,128 invalid negative response durations, and severe CSAT class imbalance. Findings are observational and must not be interpreted as causal effects or unadjusted personnel evaluations.

## Dataset Overview

- Source: Kaggle Customer Support Ticket Dataset
- URL: https://www.kaggle.com/datasets/akashbommidi/customer-support-data
- Prepared dimensions: 85,907 rows and 52 columns
- Issue-report coverage: July 28 to August 31, 2023
- Primary target: `CSAT Score`
- Project objective: identify operational factors associated with satisfaction and prepare scalable analytics, modeling, and Tableau reporting.

## Data Dictionary

All 52 columns have documented business meaning, conceptual datatype, variable role, missing percentage, and usage notes. Roles include 12 predictors, 29 derived features, 5 metadata fields, 2 identifiers, and 4 target representations.

The intended baseline uses cleaned channel, category, sub-category, timing, tenure, shift, organizational groupings, valid response-time features, and selected missingness indicators. Identifiers, alternative target forms, sparse fields, high-cardinality identity fields, and text are excluded or restricted.

## Data Structure

The CSV loads as 36 string, 14 integer, and 2 float columns. Conceptually, the schema contains 33 categorical, 9 datetime, 6 numeric, 2 text, and 2 identifier fields. Datetimes load as strings because CSV does not preserve datetime metadata but parse successfully when explicit formats are used.

Intentional structural redundancy exists between raw and cleaned labels, raw and parsed timestamps, and original and engineered target fields. This supports auditability but requires careful feature selection.

## Data Quality

Forty-two columns are complete. The primary quality risks are:

- `connected_handling_time`: 99.72% missing.
- City, product category, item price, and order timestamp: about 80% missing.
- Customer remarks: about 66.5% missing.
- Negative response times: 3,128 rows, or 3.64%.
- Product label `Home Appliences`: 1,300 rows.
- High-cardinality agent and city fields.

There are no exact duplicate rows, duplicate ticket IDs, missing ticket IDs, invalid CSAT values, or invalid binary-flag domains.

## Datetime Validation

The three required raw datetime fields parse at 100%, with no malformed, future, or unparseable values. Their derived parsed fields agree completely under format-aware parsing.

Response time recalculation matches the stored feature in all records. Negative durations are invalid and must be excluded or investigated. Phase 7 additionally classified 16,300 durations as suspicious because they are 0–1 minute or exceed 24 hours.

## CSAT Target

| Measure | Result |
|---|---:|
| Mean | 4.2422 |
| Median | 5 |
| Mode | 5 |
| Low CSAT, scores 1–2 | 14.57% |
| High CSAT, scores 4–5 | 82.46% |
| Score 5 share | 69.40% |
| Largest-to-smallest class ratio | 46.47:1 |

The target is strongly left-skewed and imbalanced. Later classification must use stratification, confusion matrices, minority-class recall/precision/F1, and balanced evaluation. The Phase 8 low-CSAT definition of scores 1–2 differs from the existing 1–3 engineered flag.

## Exploratory Profiling

### Channels

Email is the weakest channel, with average CSAT 3.8991 and low-CSAT rate 23.16%. Outcall is strongest at 4.2699 average CSAT.

### Categories And Sub-Categories

Cancellation is the weakest established category. Technician Visit is the weakest sub-category among groups with at least 100 tickets, followed by Seller Cancelled Order.

### Staffing

On Job Training is the weakest tenure group at 4.1452 average CSAT. Morning is the weakest and largest shift at 4.1895. Agent-level names were not ranked; supervisor and manager findings remain unadjusted and unsuitable as direct personnel judgments.

### Response Time

Average CSAT decreases from 4.4844 at 0–5 minutes to 4.0205 at 16–30 minutes and 3.3952 beyond 24 hours. Low-CSAT rate increases from 8.88% to 36.32%. This is the clearest descriptive operational pattern, but it may be confounded by issue complexity, channel, workload, and category.

## Major Risks

1. Sparse variables can bias analysis or reduce usable sample size.
2. Negative response times can corrupt timing models if not excluded.
3. Alternative CSAT targets can cause direct leakage.
4. Score-5 dominance can produce misleading model accuracy.
5. High-cardinality personnel and location fields can overfit.
6. Survey timing and post-outcome fields may introduce temporal leakage.
7. Observational group differences do not establish causality.

## Recommendations

1. Apply explicit datetime parsing and isolate negative durations.
2. Correct `Home Appliences` through a documented category map.
3. Use a conservative baseline feature set built from complete cleaned fields.
4. Exclude identifiers, alternative targets, and critically sparse fields.
5. Define the target threshold explicitly for every modeling task.
6. Use stratified validation and class-sensitive metrics.
7. Evaluate response-time relationships with controls for channel, category, shift, tenure, and workload.
8. Preserve raw fields and quality flags for auditability.
9. Keep personnel reporting aggregated and contextualized.

## Readiness For Modeling

Milestone 1 is complete from a data-understanding perspective. The dataset is ready to enter a controlled cleaning and modeling workflow once the documented timestamp, missingness, leakage, class-imbalance, and feature-selection rules are implemented.

Recommended next work includes formal exploratory data analysis, classification, clustering, regression or feature-importance analysis, and Tableau dashboard development. No causal conclusions should be made without additional methodology.
