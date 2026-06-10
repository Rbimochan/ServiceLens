# Phase 7 - Datetime Validation Report

## Datetime Parsing

`Issue_reported at`, `issue_responded`, and `Survey_response_Date` each parsed successfully for all 85,907 rows. There were no failed or malformed conversions. Format-aware parsing also confirms complete agreement with their derived parsed columns.

## Date Ranges

Issue reports cover July 28 through August 31, 2023. Responses and surveys cover August 1 through August 31, 2023. All fields are timezone-naive.

## Future Dates

No future dates were detected relative to June 9, 2026.

## Invalid Dates

There are no impossible, malformed, or unparseable dates. Raw and derived datetime representations have no verified mismatches when parsed according to their actual formats.

## Response Times

The recalculated response time matches the stored feature in every row. Across all records, the median is 5 minutes, mean is 136.89 minutes, minimum is -1,437 minutes, and maximum is 5,758 minutes. Among non-negative records, the median is 6 minutes and mean is 176.06 minutes.

## Negative Response Times

There are 3,128 negative response times, representing 3.64% of the dataset. The existing negative-response flag identifies all affected rows. These records are invalid as durations and require source-timestamp investigation.

## Anomalies

Using the documented Phase 7 thresholds, 66,479 rows are normal, 16,300 are suspicious, and 3,128 are invalid. Suspicious records include 13,423 durations of 0-1 minute and 2,877 durations longer than 24 hours.

## Recommendations

- Parse raw datetime fields with their explicit day-first formats.
- Parse derived ISO fields with ISO-aware rules.
- Exclude negative durations from valid response-time modeling until investigated.
- Review extremely short and long durations against operational rules before deciding whether they are valid.
- Preserve original timestamps and existing quality flags for auditability.

No source data was changed, and no timestamp repairs were performed.
