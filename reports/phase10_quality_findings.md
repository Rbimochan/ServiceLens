# Phase 10 - Quality Findings

| Severity | Quality finding | Verified evidence |
|---|---|---|
| Critical | Connected handling time is effectively unavailable | 99.72% missing |
| High | City, product, price, and order timestamp are critically sparse | Approximately 80% missing |
| High | Negative response durations | 3,128 rows (3.64%) |
| High | Target leakage risk | Four representations of CSAT |
| High | Target class imbalance | Score 5 is 69.40%; class ratio 46.47:1 |
| Medium | Customer remarks are sparse | 66.54%-66.62% missing |
| Medium | High-cardinality agent and city fields | 1,371 agents and 1,782 cities |
| Medium | Product-category label error | `Home Appliences` in 1,300 rows |
| Medium | Suspicious timing extremes | 13,423 responses at 0–1 minute; 2,877 over 24 hours |
| Medium | Personnel interpretation risk | Unadjusted agent, supervisor, and manager outcomes |
| Low | Original remarks contain edge whitespace | 13,499 values |
| Low | Datetimes load as strings from CSV | Explicit conversion required |
| Low | Intentional redundant fields | Raw/clean and raw/parsed pairs |

## Verified Integrity Strengths

- No duplicate rows or duplicate ticket IDs.
- No missing CSAT values.
- CSAT, issue hour, date, and binary-flag domains are valid.
- Required datetime fields parse at 100%.
- No future dates were detected.
