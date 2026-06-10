# Phase 6 - Missing Value Analysis

## Dataset

`data/processed/customer_support_tickets_prepared.csv` contains 85,907 rows and 52 columns.

| Column | Missing count | Non-missing count |
|---|---:|---:|
| Unique id | 0 | 85,907 |
| channel_name | 0 | 85,907 |
| category | 0 | 85,907 |
| Sub-category | 0 | 85,907 |
| Customer Remarks | 57,165 | 28,742 |
| Order_id | 18,232 | 67,675 |
| order_date_time | 68,693 | 17,214 |
| Issue_reported at | 0 | 85,907 |
| issue_responded | 0 | 85,907 |
| Survey_response_Date | 0 | 85,907 |
| Customer_City | 68,828 | 17,079 |
| Product_category | 68,711 | 17,196 |
| Item_price | 68,701 | 17,206 |
| connected_handling_time | 85,665 | 242 |
| Agent_name | 0 | 85,907 |
| Supervisor | 0 | 85,907 |
| Manager | 0 | 85,907 |
| Tenure Bucket | 0 | 85,907 |
| Agent Shift | 0 | 85,907 |
| CSAT Score | 0 | 85,907 |
| issue_reported_at_parsed | 0 | 85,907 |
| issue_responded_parsed | 0 | 85,907 |
| survey_response_date_parsed | 0 | 85,907 |
| response_time_minutes | 0 | 85,907 |
| response_time_bucket | 0 | 85,907 |
| issue_hour | 0 | 85,907 |
| issue_day | 0 | 85,907 |
| issue_weekday | 0 | 85,907 |
| survey_day | 0 | 85,907 |
| survey_weekday | 0 | 85,907 |
| is_negative_response_time | 0 | 85,907 |
| is_customer_remarks_missing | 0 | 85,907 |
| is_order_id_missing | 0 | 85,907 |
| is_order_date_time_missing | 0 | 85,907 |
| is_customer_city_missing | 0 | 85,907 |
| is_product_category_missing | 0 | 85,907 |
| is_item_price_missing | 0 | 85,907 |
| is_connected_handling_time_missing | 0 | 85,907 |
| customer_remarks_clean | 57,234 | 28,673 |
| channel_name_clean | 0 | 85,907 |
| category_clean | 0 | 85,907 |
| sub_category_clean | 0 | 85,907 |
| customer_city_clean | 68,828 | 17,079 |
| product_category_clean | 68,711 | 17,196 |
| agent_name_clean | 0 | 85,907 |
| supervisor_clean | 0 | 85,907 |
| manager_clean | 0 | 85,907 |
| tenure_bucket_clean | 0 | 85,907 |
| agent_shift_clean | 0 | 85,907 |
| csat_score | 0 | 85,907 |
| low_csat_flag | 0 | 85,907 |
| high_csat_flag | 0 | 85,907 |

## Summary

- 42 columns have no missing values.
- 10 columns contain missing values.
- No values were imputed or modified.
