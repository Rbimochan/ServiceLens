# Phase 7 - Time Anomaly Analysis

## Classification Rules

- Normal: response time greater than 1 minute and no more than 24 hours.
- Suspicious: response time from 0 through 1 minute, or longer than 24 hours.
- Invalid: negative response time.

| Category | Records | Percentage |
|---|---:|---:|
| Normal | 66,479 | 77.38% |
| Suspicious | 16,300 | 18.97% |
| Invalid | 3,128 | 3.64% |
| **Total** | **85,907** | **100.00%** |

## Suspicious Subcategories

| Subcategory | Rule | Records | Percentage |
|---|---|---:|---:|
| Extremely short | 0-1 minute | 13,423 | 15.63% |
| Extremely long | More than 24 hours | 2,877 | 3.35% |
| More than 48 hours | More than 48 hours | 999 | 1.16% |
| Exactly zero | 0 minutes | 2,448 | 2.85% |

## Timestamp Ordering

- Response timestamp earlier than issue timestamp: 3,128 rows.
- Survey calendar date earlier than issue calendar date: 0 rows.
- Survey calendar date earlier than response calendar date: 0 rows.

These categories are diagnostic thresholds for Phase 7, not permanent business rules. No anomaly labels were added to the dataset.
