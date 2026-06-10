# Phase 5 - DataFrame Info Analysis

## Dataset Overview

- Dataset: `data/processed/customer_support_tickets_prepared.csv`
- Rows: 85,907
- Columns: 52
- Deep memory usage: 70,946,060 bytes (67.66 MiB)
- Pandas storage types: 36 string, 14 `int64`, 2 `float64`

## Non-Null Counts

| Column | Pandas dtype | Non-null | Missing | Complete % |
|---|---|---:|---:|---:|
| Unique id | str | 85,907 | 0 | 100.00% |
| channel_name | str | 85,907 | 0 | 100.00% |
| category | str | 85,907 | 0 | 100.00% |
| Sub-category | str | 85,907 | 0 | 100.00% |
| Customer Remarks | str | 28,742 | 57,165 | 33.46% |
| Order_id | str | 67,675 | 18,232 | 78.78% |
| order_date_time | str | 17,214 | 68,693 | 20.04% |
| Issue_reported at | str | 85,907 | 0 | 100.00% |
| issue_responded | str | 85,907 | 0 | 100.00% |
| Survey_response_Date | str | 85,907 | 0 | 100.00% |
| Customer_City | str | 17,079 | 68,828 | 19.88% |
| Product_category | str | 17,196 | 68,711 | 20.02% |
| Item_price | float64 | 17,206 | 68,701 | 20.03% |
| connected_handling_time | float64 | 242 | 85,665 | 0.28% |
| Agent_name | str | 85,907 | 0 | 100.00% |
| Supervisor | str | 85,907 | 0 | 100.00% |
| Manager | str | 85,907 | 0 | 100.00% |
| Tenure Bucket | str | 85,907 | 0 | 100.00% |
| Agent Shift | str | 85,907 | 0 | 100.00% |
| CSAT Score | int64 | 85,907 | 0 | 100.00% |
| issue_reported_at_parsed | str | 85,907 | 0 | 100.00% |
| issue_responded_parsed | str | 85,907 | 0 | 100.00% |
| survey_response_date_parsed | str | 85,907 | 0 | 100.00% |
| response_time_minutes | int64 | 85,907 | 0 | 100.00% |
| response_time_bucket | str | 85,907 | 0 | 100.00% |
| issue_hour | int64 | 85,907 | 0 | 100.00% |
| issue_day | str | 85,907 | 0 | 100.00% |
| issue_weekday | str | 85,907 | 0 | 100.00% |
| survey_day | str | 85,907 | 0 | 100.00% |
| survey_weekday | str | 85,907 | 0 | 100.00% |
| is_negative_response_time | int64 | 85,907 | 0 | 100.00% |
| is_customer_remarks_missing | int64 | 85,907 | 0 | 100.00% |
| is_order_id_missing | int64 | 85,907 | 0 | 100.00% |
| is_order_date_time_missing | int64 | 85,907 | 0 | 100.00% |
| is_customer_city_missing | int64 | 85,907 | 0 | 100.00% |
| is_product_category_missing | int64 | 85,907 | 0 | 100.00% |
| is_item_price_missing | int64 | 85,907 | 0 | 100.00% |
| is_connected_handling_time_missing | int64 | 85,907 | 0 | 100.00% |
| customer_remarks_clean | str | 28,673 | 57,234 | 33.38% |
| channel_name_clean | str | 85,907 | 0 | 100.00% |
| category_clean | str | 85,907 | 0 | 100.00% |
| sub_category_clean | str | 85,907 | 0 | 100.00% |
| customer_city_clean | str | 17,079 | 68,828 | 19.88% |
| product_category_clean | str | 17,196 | 68,711 | 20.02% |
| agent_name_clean | str | 85,907 | 0 | 100.00% |
| supervisor_clean | str | 85,907 | 0 | 100.00% |
| manager_clean | str | 85,907 | 0 | 100.00% |
| tenure_bucket_clean | str | 85,907 | 0 | 100.00% |
| agent_shift_clean | str | 85,907 | 0 | 100.00% |
| csat_score | int64 | 85,907 | 0 | 100.00% |
| low_csat_flag | int64 | 85,907 | 0 | 100.00% |
| high_csat_flag | int64 | 85,907 | 0 | 100.00% |

## Completeness Summary

- 42 columns are fully populated.
- `connected_handling_time` is the sparsest field at 0.28% complete.
- Nine original or cleaned fields have more than 50% missing data.
- This report documents structure only; no distributions or relationships were analyzed.
