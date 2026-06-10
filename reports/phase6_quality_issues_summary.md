# Phase 6 - Quality Issues Summary

| Severity | Issue | Verified evidence | Recommended cleaning action |
|---|---|---|---|
| Critical | Connected handling time is nearly absent | 85,665 missing; 99.72% | Exclude from primary analysis unless a better source becomes available |
| High | City, product, price, and order timestamp fields are critically sparse | 79.96%-80.12% missing | Exclude from baseline or use only with an explicit missingness methodology |
| High | Negative response times | 3,128 rows; values from -1,437 to -20 minutes | Investigate timestamp logic and exclude or correct only under documented rules |
| High | Multiple CSAT target representations | Four target-related fields | Select one target and exclude the others from predictors |
| Medium | Customer remarks are sparse | 66.54%-66.62% missing | Restrict to optional text analysis and assess response-selection bias |
| Medium | Product-category spelling error | `Home Appliences` occurs in 1,300 rows | Correct to `Home Appliances` through an approved mapping |
| Medium | High-cardinality agent and city labels | 1,371 agent and 1,782 city values | Avoid naive one-hot encoding; evaluate aggregation, leakage, and generalization |
| Medium | Redundant raw/clean and raw/parsed fields | Multiple parallel representations | Select cleaned/parsed fields for analysis and retain originals for audit |
| Low | Original customer remarks contain edge whitespace | 13,499 values | Prefer `customer_remarks_clean`; preserve original for traceability |
| Low | Missing-value sentinel text in original remarks | 69 values standardized during Phase 3 | Continue using cleaned remarks and the existing missing flag |
| Low | Duplicate rows and IDs | 0 duplicate rows and 0 duplicate IDs | No action required; recheck on refresh |

## Verified Clean Areas

- CSAT values are within the 1-5 range.
- Issue hours are within 0-23.
- Derived day fields parse successfully.
- Binary flags contain only 0 and 1 and match their documented definitions.
- No non-null empty or whitespace-only strings were detected.
- No case-only or whitespace-only categorical label duplicates were detected.

No cleaning was performed during Phase 6.
