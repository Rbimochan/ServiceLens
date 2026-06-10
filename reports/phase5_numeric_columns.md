# Phase 5 - Numeric Columns

## Integer Columns

| Column | Actual dtype | Purpose |
|---|---|---|
| CSAT Score | int64 | Original CSAT target |
| response_time_minutes | int64 | Derived response delay |
| issue_hour | int64 | Derived issue-report hour |
| is_negative_response_time | int64 | Encoded binary quality flag |
| is_customer_remarks_missing | int64 | Encoded binary missingness flag |
| is_order_id_missing | int64 | Encoded binary missingness flag |
| is_order_date_time_missing | int64 | Encoded binary missingness flag |
| is_customer_city_missing | int64 | Encoded binary missingness flag |
| is_product_category_missing | int64 | Encoded binary missingness flag |
| is_item_price_missing | int64 | Encoded binary missingness flag |
| is_connected_handling_time_missing | int64 | Encoded binary missingness flag |
| csat_score | int64 | Standardized numeric CSAT target |
| low_csat_flag | int64 | Encoded binary target |
| high_csat_flag | int64 | Encoded binary target |

## Float Columns

| Column | Actual dtype | Purpose |
|---|---|---|
| Item_price | float64 | Item monetary value; nullable |
| connected_handling_time | float64 | Handling duration; nullable |

## Notes

- There are 16 numeric-storage columns: 14 integer and 2 float.
- `response_time_minutes`, `issue_hour`, the quality/missingness flags, `csat_score`, and CSAT flags are derived fields.
- Binary flags are stored numerically but are conceptually categorical indicators.
