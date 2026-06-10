# Phase 5 - Type Mismatch Detection

| Issue | Affected column(s) | Evidence | Recommendation |
|---|---|---|---|
| Datetime stored as string | order_date_time; Issue_reported at; issue_responded; Survey_response_Date; issue_reported_at_parsed; issue_responded_parsed; survey_response_date_parsed; issue_day; survey_day | All load as `str`; all non-null values parse successfully | Apply `pd.to_datetime` after loading or supply explicit parsing logic |
| Conceptual categorical flags stored as integers | is_negative_response_time; seven missingness flags; low_csat_flag; high_csat_flag | Values are integer encoded with two unique values | Retain for modeling, but treat as categorical indicators in documentation |

## Checks With No Detected Issue

- `Item_price` and `connected_handling_time` load as `float64`.
- `CSAT Score`, `csat_score`, `response_time_minutes`, and `issue_hour` load as `int64`.
- IDs load as strings.
- String inference found no mixed-type columns among non-null values.
- Datetime conversion produced zero failures for non-null values.

No columns were modified or removed.
