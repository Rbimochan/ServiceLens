# Phase 7 - Response Time Calculation

Response time was recalculated as:

`issue_responded - Issue_reported at`

The recalculated minute value matches `response_time_minutes` for all 85,907 rows.

## All Records

| Statistic | Minutes | Hours |
|---|---:|---:|
| Minimum | -1,437.00 | -23.95 |
| Mean | 136.89 | 2.28 |
| Median | 5.00 | 0.08 |
| 25th percentile | 2.00 | 0.03 |
| 75th percentile | 35.00 | 0.58 |
| 90th percentile | 395.00 | 6.58 |
| 95th percentile | 1,079.00 | 17.98 |
| 99th percentile | 3,007.00 | 50.12 |
| Maximum | 5,758.00 | 95.97 |

## Non-Negative Records

| Statistic | Minutes | Hours |
|---|---:|---:|
| Count | 82,779 | 82,779 |
| Minimum | 0.00 | 0.00 |
| Mean | 176.06 | 2.93 |
| Median | 6.00 | 0.10 |
| 25th percentile | 2.00 | 0.03 |
| 75th percentile | 39.00 | 0.65 |
| 90th percentile | 432.00 | 7.20 |
| 95th percentile | 1,124.00 | 18.73 |
| 99th percentile | 3,047.22 | 50.79 |
| Maximum | 5,758.00 | 95.97 |

Negative records are retained in the all-record summary for auditability and separated in the non-negative summary.
