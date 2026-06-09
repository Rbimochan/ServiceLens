# Phase 10 - Datetime Summary

## Parsing And Ranges

| Field | Parsing success | Range |
|---|---:|---|
| Issue_reported at | 100.00% | July 28 to August 31, 2023 |
| issue_responded | 100.00% | August 1–31, 2023 |
| Survey_response_Date | 100.00% | August 1–31, 2023 |

- Failed conversions: 0
- Future dates relative to June 9, 2026: 0
- Raw/derived datetime mismatches with format-aware parsing: 0
- Timezone representation: consistently naive

## Response-Time Findings

- Recalculated and stored response minutes match for every row.
- Negative response times: 3,128 rows (3.64%).
- Negative range: -1,437 to -20 minutes.
- Normal Phase 7 timing category: 66,479 rows.
- Suspicious timing category: 16,300 rows.
- Invalid negative category: 3,128 rows.

Raw day-first fields and ISO-derived fields require separate explicit parsing rules. Negative durations must be excluded from valid response-time modeling until investigated.
