# Phase 7 - Parsing Success

| Column | Parsed | Failed | Success rate | Derived-column agreement |
|---|---:|---:|---:|---:|
| Issue_reported at | 85,907 | 0 | 100.00% | 85,907/85,907 |
| issue_responded | 85,907 | 0 | 100.00% | 85,907/85,907 |
| Survey_response_Date | 85,907 | 0 | 100.00% | 85,907/85,907 |

The raw fields agree with `issue_reported_at_parsed`, `issue_responded_parsed`, and `survey_response_date_parsed` for every row when each representation is parsed according to its actual format.

All parsed timestamps are timezone-naive; no mixed timezone representation was detected.
