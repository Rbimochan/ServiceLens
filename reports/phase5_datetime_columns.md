# Phase 5 - Datetime Columns

| Column | CSV dtype | Parse result | Timezone status | Notes |
|---|---|---|---|---|
| order_date_time | str | 17,214/17,214 non-null parsed | Naive | Sparse original timestamp |
| Issue_reported at | str | 85,907/85,907 parsed | Naive | Original timestamp |
| issue_responded | str | 85,907/85,907 parsed | Naive | Original timestamp |
| Survey_response_Date | str | 85,907/85,907 parsed | Naive | Original date |
| issue_reported_at_parsed | str | 85,907/85,907 parsed | Naive | Standardized serialized datetime |
| issue_responded_parsed | str | 85,907/85,907 parsed | Naive | Standardized serialized datetime |
| survey_response_date_parsed | str | 85,907/85,907 parsed | Naive | Standardized serialized date |
| issue_day | str | 85,907/85,907 parsed | Naive | Derived serialized date |
| survey_day | str | 85,907/85,907 parsed | Naive | Derived serialized date |

## Verification

- All non-null datetime values parse successfully with pandas.
- No timezone-aware values were detected; all fields are consistently timezone-naive.
- Because CSV does not preserve datetime dtypes, every datetime field loads as `str` and requires explicit conversion after loading.
