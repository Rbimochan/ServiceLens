# Phase 6 - Invalid Value Detection

| Check | Valid rule | Invalid count | Result |
|---|---|---:|---|
| CSAT Score | Integer from 1 through 5 | 0 | Pass |
| csat_score | Integer from 1 through 5 | 0 | Pass |
| Original/standardized CSAT agreement | Values equal | 0 mismatches | Pass |
| response_time_minutes | Non-negative duration | 3,128 | Issue detected |
| issue_hour | Integer from 0 through 23 | 0 | Pass |
| issue_day | Parseable calendar date | 0 | Pass |
| survey_day | Parseable calendar date | 0 | Pass |
| Quality/missingness flags | Binary 0 or 1 | 0 | Pass |
| low_csat_flag | Binary 0 or 1 and matches `csat_score <= 3` | 0 | Pass |
| high_csat_flag | Binary 0 or 1 and matches `csat_score >= 4` | 0 | Pass |

## Negative Response Times

- Negative rows: 3,128 (3.64% of records)
- Minimum: -1,437 minutes
- Maximum negative value: -20 minutes
- `is_negative_response_time` true count: 3,128
- Flag-to-duration mismatches: 0

Negative response times are impossible operational durations and likely indicate timestamp ordering, date-boundary, or source-data issues. They are correctly isolated by the existing quality flag and should not be silently corrected.

## Missing-Flag Consistency

Six non-text missingness flags match direct null status exactly. For customer remarks, 69 raw values contain sentinel text such as `Na`, `na`, `none`, `None`, or `N/A`. Phase 3 intentionally standardized these values to missing in `customer_remarks_clean` and marked them through `is_customer_remarks_missing`; this is expected behavior, not an invalid binary flag.

No values were fixed in this phase.
