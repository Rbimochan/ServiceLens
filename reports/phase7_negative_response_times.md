# Phase 7 - Negative Response Times

## Summary

- Negative response-time records: 3,128
- Percentage of dataset: 3.64%
- Minimum response time: -1,437 minutes
- Closest negative response time to zero: -20 minutes
- Existing `is_negative_response_time` true values: 3,128
- Flag mismatches: 0

## Severity Distribution

| Negative duration band | Records | Interpretation |
|---|---:|---|
| Less than -720 minutes | 2,209 | Severe ordering/date issue |
| -720 through less than -120 minutes | 906 | Large ordering issue |
| -120 through less than -60 minutes | 7 | Moderate ordering issue |
| -60 through less than -30 minutes | 5 | Short ordering issue |
| -30 through less than 0 minutes | 1 | Small ordering issue |

All 3,128 negative cases occur on the same calendar date for issue and response timestamps; none are caused by the response date being earlier than the issue date. This points to within-day timestamp ordering problems rather than a prior-date response.

Affected records are already flagged but were not removed or corrected.
