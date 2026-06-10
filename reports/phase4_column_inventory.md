# Phase 4 - Column Inventory

## Purpose

This report identifies all columns in the processed ServiceLens dataset, records their order, and notes which columns are original versus generated. Business meaning is not interpreted in this step.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Column Count

- Total columns: 52
- Original raw columns retained: 20
- Generated preparation columns: 32

## Column Inventory

| Order | Column Name | Column Source |
|---:|---|---|
| 1 | `Unique id` | Original retained column |
| 2 | `channel_name` | Original retained column |
| 3 | `category` | Original retained column |
| 4 | `Sub-category` | Original retained column |
| 5 | `Customer Remarks` | Original retained column |
| 6 | `Order_id` | Original retained column |
| 7 | `order_date_time` | Original retained column |
| 8 | `Issue_reported at` | Original retained column |
| 9 | `issue_responded` | Original retained column |
| 10 | `Survey_response_Date` | Original retained column |
| 11 | `Customer_City` | Original retained column |
| 12 | `Product_category` | Original retained column |
| 13 | `Item_price` | Original retained column |
| 14 | `connected_handling_time` | Original retained column |
| 15 | `Agent_name` | Original retained column |
| 16 | `Supervisor` | Original retained column |
| 17 | `Manager` | Original retained column |
| 18 | `Tenure Bucket` | Original retained column |
| 19 | `Agent Shift` | Original retained column |
| 20 | `CSAT Score` | Original retained column |
| 21 | `issue_reported_at_parsed` | Generated preparation feature |
| 22 | `issue_responded_parsed` | Generated preparation feature |
| 23 | `survey_response_date_parsed` | Generated preparation feature |
| 24 | `response_time_minutes` | Generated preparation feature |
| 25 | `response_time_bucket` | Generated preparation feature |
| 26 | `issue_hour` | Generated preparation feature |
| 27 | `issue_day` | Generated preparation feature |
| 28 | `issue_weekday` | Generated preparation feature |
| 29 | `survey_day` | Generated preparation feature |
| 30 | `survey_weekday` | Generated preparation feature |
| 31 | `is_negative_response_time` | Generated preparation feature |
| 32 | `is_customer_remarks_missing` | Generated preparation feature |
| 33 | `is_order_id_missing` | Generated preparation feature |
| 34 | `is_order_date_time_missing` | Generated preparation feature |
| 35 | `is_customer_city_missing` | Generated preparation feature |
| 36 | `is_product_category_missing` | Generated preparation feature |
| 37 | `is_item_price_missing` | Generated preparation feature |
| 38 | `is_connected_handling_time_missing` | Generated preparation feature |
| 39 | `customer_remarks_clean` | Generated preparation feature |
| 40 | `channel_name_clean` | Generated preparation feature |
| 41 | `category_clean` | Generated preparation feature |
| 42 | `sub_category_clean` | Generated preparation feature |
| 43 | `customer_city_clean` | Generated preparation feature |
| 44 | `product_category_clean` | Generated preparation feature |
| 45 | `agent_name_clean` | Generated preparation feature |
| 46 | `supervisor_clean` | Generated preparation feature |
| 47 | `manager_clean` | Generated preparation feature |
| 48 | `tenure_bucket_clean` | Generated preparation feature |
| 49 | `agent_shift_clean` | Generated preparation feature |
| 50 | `csat_score` | Generated preparation feature |
| 51 | `low_csat_flag` | Generated preparation feature |
| 52 | `high_csat_flag` | Generated preparation feature |

## Notes on Renamed / Generated Features

- The first 20 columns are retained from the raw dataset in their original order.
- The remaining 32 columns were generated during Phase 3 data preparation.
- Generated columns include parsed datetime fields, response-time features, missingness flags, cleaned text/categorical fields, and CSAT target variants.
- This report records column inventory only and does not interpret business meaning.
