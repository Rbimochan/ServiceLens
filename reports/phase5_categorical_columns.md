# Phase 5 - Categorical Columns

## Cardinality Rules

- Low: 2-20 unique values
- Medium: 21-100 unique values
- High: more than 100 unique values

| Column | Unique count | Cardinality |
|---|---:|---|
| channel_name | 3 | Low |
| category | 12 | Low |
| Sub-category | 57 | Medium |
| Customer_City | 1,782 | High |
| Product_category | 9 | Low |
| Agent_name | 1,371 | High |
| Supervisor | 40 | Medium |
| Manager | 6 | Low |
| Tenure Bucket | 5 | Low |
| Agent Shift | 5 | Low |
| response_time_bucket | 8 | Low |
| issue_weekday | 7 | Low |
| survey_weekday | 7 | Low |
| is_negative_response_time | 2 | Low |
| is_customer_remarks_missing | 2 | Low |
| is_order_id_missing | 2 | Low |
| is_order_date_time_missing | 2 | Low |
| is_customer_city_missing | 2 | Low |
| is_product_category_missing | 2 | Low |
| is_item_price_missing | 2 | Low |
| is_connected_handling_time_missing | 2 | Low |
| channel_name_clean | 3 | Low |
| category_clean | 12 | Low |
| sub_category_clean | 57 | Medium |
| customer_city_clean | 1,782 | High |
| product_category_clean | 9 | Low |
| agent_name_clean | 1,371 | High |
| supervisor_clean | 40 | Medium |
| manager_clean | 6 | Low |
| tenure_bucket_clean | 5 | Low |
| agent_shift_clean | 5 | Low |
| low_csat_flag | 2 | Low |
| high_csat_flag | 2 | Low |

## Notes

- High-cardinality categorical fields are city and agent fields, including their cleaned counterparts.
- Identifier, datetime-like, and free-text string columns are documented separately.
- Binary integer flags are included because their business meaning is categorical.
