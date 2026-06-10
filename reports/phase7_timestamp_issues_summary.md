# Phase 7 - Timestamp Issues Summary

| Severity | Finding | Verified evidence | Recommended action |
|---|---|---|---|
| High | Negative response times | 3,128 rows (3.64%); all correctly flagged | Exclude from valid-duration summaries and investigate source timestamp ordering |
| Medium | Extremely long response times | 2,877 rows exceed 24 hours; 999 exceed 48 hours | Validate against service workflow before modeling or SLA analysis |
| Medium | Extremely short response times | 13,423 rows are 0-1 minute; 2,448 are exactly zero | Confirm whether automated or immediate responses are valid |
| Low | CSV does not preserve datetime dtype | Required fields load as strings | Parse with explicit formats on every load |
| Low | Parser-setting ambiguity | ISO fields can be misread if `dayfirst=True` is applied indiscriminately | Parse raw day-first and derived ISO fields with separate rules |
| None | Conversion failures | 0 failed conversions | No repair required |
| None | Future dates | 0 future values as of June 9, 2026 | No action required |
| None | Raw/derived mismatch | 0 mismatches with format-aware parsing | Derived datetime fields are consistent |

## Recommended Treatment

1. Use explicit formats for the three raw datetime fields.
2. Parse ISO-derived fields separately without applying day-first interpretation.
3. Keep negative rows flagged and exclude them from valid response-time modeling until investigated.
4. Treat 0-1 minute and over-24-hour durations as review categories, not automatically invalid.
5. Document the prediction or reporting cutoff before using survey-derived dates.

No timestamps or durations were modified.
