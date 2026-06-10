# Phase 7 - Datetime Parsing

## Dataset

`data/processed/customer_support_tickets_prepared.csv` contains 85,907 rows.

| Column | Verified source format | Non-null values | Parsed values | Failed conversions | Success rate |
|---|---|---:|---:|---:|---:|
| Issue_reported at | `%d-%m-%Y %H:%M` | 85,907 | 85,907 | 0 | 100.00% |
| issue_responded | `%d-%m-%Y %H:%M` | 85,907 | 85,907 | 0 | 100.00% |
| Survey_response_Date | `%d-%b-%y` | 85,907 | 85,907 | 0 | 100.00% |

All values match their documented source format. No source data was modified.

## Parsing Rule

Use explicit formats for raw columns. Derived ISO fields such as `issue_reported_at_parsed` should be parsed as ISO values rather than with `dayfirst=True`, because applying day-first logic to ISO strings can reinterpret ambiguous month/day values.
