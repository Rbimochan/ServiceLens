# Phase 4 - Datatype Documentation

## Purpose

This report documents the datatype category for every variable in the processed ServiceLens dataset. Datatypes are classified as Numeric, Categorical, Datetime, Text, or Identifier.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Datatype Dictionary

| Column | Datatype | Justification |
|---|---|---|
| `Unique id` | Identifier | Unique ticket record identifier; should not be treated as a numeric measurement. |
| `channel_name` | Categorical | Support channel has a small set of repeated category values. |
| `category` | Categorical | Main issue category is a repeated support classification. |
| `Sub-category` | Categorical | Detailed issue category is a repeated support classification. |
| `Customer Remarks` | Text | Free-text customer comment field. |
| `Order_id` | Identifier | Order identifier links tickets to orders and should not be treated as numeric. |
| `order_date_time` | Datetime | Original order timestamp field, stored as raw text but conceptually datetime. |
| `Issue_reported at` | Datetime | Original timestamp when the support issue was reported. |
| `issue_responded` | Datetime | Original timestamp when the support issue was responded to. |
| `Survey_response_Date` | Datetime | Original survey response date. |
| `Customer_City` | Categorical | Customer location field with repeated city values. |
| `Product_category` | Categorical | Product grouping associated with the ticket. |
| `Item_price` | Numeric | Monetary value associated with the item. |
| `connected_handling_time` | Numeric | Handling time measurement when available. |
| `Agent_name` | Categorical | Agent name is a repeated operational category, not a free numeric value. |
| `Supervisor` | Categorical | Supervisor name/group is a repeated operational category. |
| `Manager` | Categorical | Manager name/group is a repeated operational category. |
| `Tenure Bucket` | Categorical | Tenure is grouped into buckets rather than stored as a continuous value. |
| `Agent Shift` | Categorical | Shift assignment is a repeated category. |
| `CSAT Score` | Numeric | Customer satisfaction rating is a scored numeric survey value. |
| `issue_reported_at_parsed` | Datetime | Parsed standardized version of issue reported timestamp. |
| `issue_responded_parsed` | Datetime | Parsed standardized version of issue response timestamp. |
| `survey_response_date_parsed` | Datetime | Parsed standardized version of survey response date. |
| `response_time_minutes` | Numeric | Time difference measured in minutes. |
| `response_time_bucket` | Categorical | Bucketed response time group. |
| `issue_hour` | Numeric | Hour extracted from issue timestamp as an integer value. |
| `issue_day` | Datetime | Calendar date extracted from issue timestamp. |
| `issue_weekday` | Categorical | Weekday name extracted from issue timestamp. |
| `survey_day` | Datetime | Calendar date extracted from survey response date. |
| `survey_weekday` | Categorical | Weekday name extracted from survey response date. |
| `is_negative_response_time` | Categorical | Binary flag indicating invalid timestamp ordering. |
| `is_customer_remarks_missing` | Categorical | Binary missingness flag. |
| `is_order_id_missing` | Categorical | Binary missingness flag. |
| `is_order_date_time_missing` | Categorical | Binary missingness flag. |
| `is_customer_city_missing` | Categorical | Binary missingness flag. |
| `is_product_category_missing` | Categorical | Binary missingness flag. |
| `is_item_price_missing` | Categorical | Binary missingness flag. |
| `is_connected_handling_time_missing` | Categorical | Binary missingness flag. |
| `customer_remarks_clean` | Text | Cleaned free-text customer comment field. |
| `channel_name_clean` | Categorical | Cleaned support channel category. |
| `category_clean` | Categorical | Cleaned main issue category. |
| `sub_category_clean` | Categorical | Cleaned detailed issue sub-category. |
| `customer_city_clean` | Categorical | Cleaned customer city category. |
| `product_category_clean` | Categorical | Cleaned product category. |
| `agent_name_clean` | Categorical | Cleaned agent name category. |
| `supervisor_clean` | Categorical | Cleaned supervisor category. |
| `manager_clean` | Categorical | Cleaned manager category. |
| `tenure_bucket_clean` | Categorical | Cleaned tenure bucket category. |
| `agent_shift_clean` | Categorical | Cleaned shift category. |
| `csat_score` | Numeric | Numeric standardized customer satisfaction score. |
| `low_csat_flag` | Categorical | Binary target flag for lower CSAT outcomes. |
| `high_csat_flag` | Categorical | Binary target flag for higher CSAT outcomes. |

## Notes

- Binary flags are documented as Categorical because they represent class membership or yes/no indicators.
- Raw datetime fields may be stored as text in the CSV, but they are classified by their intended data meaning.
- Identifier fields should not be treated as numeric measurements during later analysis.
