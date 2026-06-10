# Phase 5 - Schema Summary

| Column | Actual dtype | Expected type | Role | Missing % | Structure note |
|---|---|---|---|---:|---|
| Unique id | str | Identifier | Identifier | 0.00% | Unique; reference only |
| channel_name | str | Categorical | Predictor | 0.00% | Raw/clean pair |
| category | str | Categorical | Predictor | 0.00% | Raw/clean pair |
| Sub-category | str | Categorical | Predictor | 0.00% | Medium cardinality |
| Customer Remarks | str | Text | Metadata | 66.54% | Sparse raw text |
| Order_id | str | Identifier | Identifier | 21.22% | High cardinality |
| order_date_time | str | Datetime | Metadata | 79.96% | Sparse; parse on load |
| Issue_reported at | str | Datetime | Metadata | 0.00% | Parse on load |
| issue_responded | str | Datetime | Metadata | 0.00% | Parse on load |
| Survey_response_Date | str | Datetime | Metadata | 0.00% | Possible temporal leakage |
| Customer_City | str | Categorical | Predictor | 80.12% | Sparse, high cardinality |
| Product_category | str | Categorical | Predictor | 79.98% | Sparse |
| Item_price | float64 | Numeric | Predictor | 79.97% | Sparse numeric |
| connected_handling_time | float64 | Numeric | Predictor | 99.72% | Nearly unusable |
| Agent_name | str | Categorical | Predictor | 0.00% | High cardinality |
| Supervisor | str | Categorical | Predictor | 0.00% | Medium cardinality |
| Manager | str | Categorical | Predictor | 0.00% | Low cardinality |
| Tenure Bucket | str | Categorical | Predictor | 0.00% | Possible ordinal meaning |
| Agent Shift | str | Categorical | Predictor | 0.00% | Low cardinality |
| CSAT Score | int64 | Numeric | Target | 0.00% | Original target |
| issue_reported_at_parsed | str | Datetime | Derived Feature | 0.00% | Parse on load |
| issue_responded_parsed | str | Datetime | Derived Feature | 0.00% | Parse on load |
| survey_response_date_parsed | str | Datetime | Derived Feature | 0.00% | Possible temporal leakage |
| response_time_minutes | int64 | Numeric | Derived Feature | 0.00% | Negative values flagged |
| response_time_bucket | str | Categorical | Derived Feature | 0.00% | Eight categories |
| issue_hour | int64 | Numeric | Derived Feature | 0.00% | 0-23 timing feature |
| issue_day | str | Datetime | Derived Feature | 0.00% | Parse on load |
| issue_weekday | str | Categorical | Derived Feature | 0.00% | Seven categories |
| survey_day | str | Datetime | Derived Feature | 0.00% | Possible temporal leakage |
| survey_weekday | str | Categorical | Derived Feature | 0.00% | Possible temporal leakage |
| is_negative_response_time | int64 | Categorical | Derived Feature | 0.00% | Binary quality flag |
| is_customer_remarks_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_order_id_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_order_date_time_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_customer_city_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_product_category_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_item_price_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| is_connected_handling_time_missing | int64 | Categorical | Derived Feature | 0.00% | Binary missingness flag |
| customer_remarks_clean | str | Text | Derived Feature | 66.62% | Preferred future NLP text |
| channel_name_clean | str | Categorical | Derived Feature | 0.00% | Preferred cleaned field |
| category_clean | str | Categorical | Derived Feature | 0.00% | Preferred cleaned field |
| sub_category_clean | str | Categorical | Derived Feature | 0.00% | Medium cardinality |
| customer_city_clean | str | Categorical | Derived Feature | 80.12% | Sparse, high cardinality |
| product_category_clean | str | Categorical | Derived Feature | 79.98% | Sparse |
| agent_name_clean | str | Categorical | Derived Feature | 0.00% | High cardinality |
| supervisor_clean | str | Categorical | Derived Feature | 0.00% | Medium cardinality |
| manager_clean | str | Categorical | Derived Feature | 0.00% | Low cardinality |
| tenure_bucket_clean | str | Categorical | Derived Feature | 0.00% | Possible ordinal meaning |
| agent_shift_clean | str | Categorical | Derived Feature | 0.00% | Low cardinality |
| csat_score | int64 | Numeric | Target | 0.00% | Standardized target |
| low_csat_flag | int64 | Categorical | Target | 0.00% | Binary target |
| high_csat_flag | int64 | Categorical | Target | 0.00% | Binary target |

## Summary

- 52 of 52 columns are documented.
- Actual storage: 36 string, 14 integer, 2 float.
- Expected business types: 33 categorical, 9 datetime, 6 numeric, 2 text, 2 identifier.
- Roles: 29 derived features, 12 predictors, 5 metadata, 4 targets, 2 identifiers.
