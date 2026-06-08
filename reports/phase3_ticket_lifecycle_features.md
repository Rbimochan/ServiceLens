# Phase 3 - Ticket Lifecycle Features

## Purpose

This report documents safe ticket lifecycle features derived only from available timestamp columns in the raw customer support ticket dataset. Features were calculated in memory for assessment only. The raw dataset was not modified, invalid rows were not removed, and no processed dataset was created.

## Source Columns

| Source Column | Use |
|---|---|
| `Issue_reported at` | Base timestamp for issue timing features. |
| `issue_responded` | Response timestamp used to calculate response time. |

No fake resolution time, escalation field, or unavailable lifecycle event was created.

## Feature Definitions

| Feature | Definition | Intended Type | Notes |
|---|---|---|---|
| `response_time_minutes` | Difference between `issue_responded` and `Issue_reported at` in minutes. | Numeric | Can be negative when response timestamp is earlier than issue timestamp. |
| `response_time_bucket` | Categorical bucket created from `response_time_minutes`. | Categorical | Includes a separate `negative` bucket to preserve invalid cases. |
| `issue_hour` | Hour extracted from `Issue_reported at`. | Integer / categorical | Values range from 0 to 23. |
| `issue_day` | Calendar date extracted from `Issue_reported at`. | Date | Useful for later daily volume analysis. |
| `issue_weekday` | Weekday name extracted from `Issue_reported at`. | Categorical | Useful for later weekly pattern analysis. |
| `is_negative_response_time` | Boolean flag where `response_time_minutes < 0`. | Boolean | Keeps invalid timestamp rows visible without deleting them. |

## Response Time Bucket Plan

| Bucket | Rule | Count |
|---|---|---:|
| `negative` | `< 0 minutes` | 3,128 |
| `0 minutes` | `= 0 minutes` | 2,448 |
| `1-5 minutes` | `> 0 and <= 5 minutes` | 38,038 |
| `6-30 minutes` | `> 5 and <= 30 minutes` | 19,750 |
| `31-60 minutes` | `> 30 and <= 60 minutes` | 4,484 |
| `1-4 hours` | `> 60 and <= 240 minutes` | 7,399 |
| `4-24 hours` | `> 240 and <= 1,440 minutes` | 7,783 |
| `more than 24 hours` | `> 1,440 minutes` | 2,877 |

## Feature Validation Summary

| Check | Result |
|---|---:|
| Rows assessed | 85,907 |
| Rows with valid parsed issue and response timestamps | 85,907 |
| Rows with timestamp parse failures | 0 |
| Rows flagged as negative response time | 3,128 |
| Issue hour coverage | 0-23 |
| Distinct issue dates observed | 35 |

## Issue Weekday Summary

| Weekday | Count |
|---|---:|
| Monday | 12,053 |
| Tuesday | 14,282 |
| Wednesday | 13,633 |
| Thursday | 13,803 |
| Friday | 10,564 |
| Saturday | 10,630 |
| Sunday | 10,942 |

## Recommended Treatment

- Create these lifecycle features later in a prepared working dataset, not in the raw dataset.
- Keep `is_negative_response_time` as a quality flag.
- Do not remove negative response-time rows yet.
- Use `response_time_minutes` carefully in later modeling or Tableau work because invalid and extreme values may distort summaries.
- Use `response_time_bucket` for safer reporting when raw response times are skewed.
- Treat `issue_hour`, `issue_day`, and `issue_weekday` as derived timing features for later EDA and dashboarding.

## Risks

- Negative response times indicate timestamp inconsistencies and require a documented cleaning decision later.
- Buckets are practical for initial reporting but may need adjustment after stakeholder or academic review.
- `issue_day` is derived from report time only and should not be interpreted as resolution date.
- No resolution time or escalation feature can be created safely from the available fields without additional source columns.

## Next Step

Combine this lifecycle feature plan with the missing value, duplicate, datatype, and datetime reports before creating any processed dataset.
