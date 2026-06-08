# Phase 3 - Datetime Engineering

## Purpose

This report parses and validates key datetime fields in the raw customer support ticket dataset and derives a temporary in-memory response time metric for assessment. The raw dataset was not modified, no rows were deleted, and no processed dataset was created.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Datetime Parsing Status

| Column | Expected Format Used | Raw Missing | Parse Success | Parse Failed | Status |
|---|---|---:|---:|---:|---|
| Issue_reported at | `dd-mm-yyyy HH:MM` | 0 | 85,907 | 0 | Parsed successfully |
| issue_responded | `dd-mm-yyyy HH:MM` | 0 | 85,907 | 0 | Parsed successfully |
| Survey_response_Date | `dd-Mon-yy` | 0 | 85,907 | 0 | Parsed successfully |

## Response Time Summary

`response_time_minutes` was calculated in memory as:

`issue_responded - Issue_reported at`

| Metric | Value |
|---|---:|
| Valid response time values | 85,907 |
| Missing or invalid response time values | 0 |
| Negative response times | 3,128 |
| Zero-minute response times | 2,448 |
| Positive response times | 80,331 |
| Minimum response time | -1,437.00 minutes |
| 25th percentile | 2.00 minutes |
| Median | 5.00 minutes |
| Mean | 136.89 minutes |
| 75th percentile | 35.00 minutes |
| Maximum response time | 5,758.00 minutes |

## Invalid / Negative Timestamp Count

| Issue Type | Count | Interpretation |
|---|---:|---|
| Unparseable `Issue_reported at` values | 0 | No parsing failures detected. |
| Unparseable `issue_responded` values | 0 | No parsing failures detected. |
| Unparseable `Survey_response_Date` values | 0 | No parsing failures detected. |
| Negative response times | 3,128 | Response timestamp occurs before issue reported timestamp. These records require review before modeling. |

## Recommended Treatment

- Keep all rows for now; do not delete negative response-time rows at this stage.
- Create `response_time_minutes` later in a prepared working dataset, not in the raw dataset.
- Flag negative response times as invalid or suspicious during cleaning.
- Exclude or separately review negative response-time records before using response time as a modeling or dashboard feature.
- Treat zero-minute response times as valid but review them later for business plausibility.
- Keep parsed datetime fields available for later feature engineering after final cleaning rules are approved.

## Risks

- Negative response times may indicate data entry errors, timezone issues, system timestamp inconsistencies, or event ordering problems.
- Very large response times may influence averages and should be reviewed before summary reporting.
- The mean response time is much higher than the median, suggesting possible skew or outliers that should be examined in later exploratory analysis.
- Datetime-derived features should not be used in models until invalid timestamp handling is finalized.

## Next Step

Proceed to the next Phase 3 data preparation check. Do not delete rows or create a final processed dataset until missing value, duplicate, datatype, and datetime handling decisions are combined into a final cleaning plan.
