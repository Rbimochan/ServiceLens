# Phase 4 - Master Data Dictionary

## Purpose

This master data dictionary combines verified Phase 4 documentation for all original and engineered fields in the processed ServiceLens dataset. It includes business meaning, datatype, variable role, missing percentage, and notes for every column.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Summary

- Rows assessed for missing percentages: 85,907
- Columns documented: 52
- Includes original retained fields, engineered preparation features, and CSAT target variables.

## Master Data Dictionary

| Column Name | Business Meaning | Datatype | Variable Role | Missing % | Notes |
|---|---|---|---|---:|---|
| `Unique id` | Unique ticket record identifier assigned to each support interaction. | Identifier | Identifier | 0.00% | Reference identifier; exclude from baseline modeling. |
| `channel_name` | Support channel used by the customer to contact support. | Categorical | Predictor | 0.00% | Low-cardinality support channel predictor. |
| `category` | Main issue category assigned to the customer support ticket. | Categorical | Predictor | 0.00% | Core issue category predictor. |
| `Sub-category` | More detailed issue category within the main support category. | Categorical | Predictor | 0.00% | Medium-cardinality issue detail; encoding choice required later. |
| `Customer Remarks` | Original free-text comment or remark provided by the customer, when available. | Text | Metadata | 66.54% | High missingness; preserve for context and possible future NLP only. |
| `Order_id` | Identifier for the customer order associated with the support ticket, when available. | Identifier | Identifier | 21.22% | Identifier-like field with missingness; exclude from baseline modeling. |
| `order_date_time` | Original date and time associated with the customer order, when available. | Datetime | Metadata | 79.96% | Very high missingness; retained for traceability. |
| `Issue_reported at` | Original timestamp when the customer support issue was reported. | Datetime | Metadata | 0.00% | Raw timestamp; use parsed/derived features for analysis. |
| `issue_responded` | Original timestamp when the support team responded to the issue. | Datetime | Metadata | 0.00% | Raw timestamp; use parsed/derived response-time features. |
| `Survey_response_Date` | Original date when the customer submitted the satisfaction survey response. | Datetime | Metadata | 0.00% | Raw survey date; use carefully to avoid temporal leakage. |
| `Customer_City` | Customer city associated with the support ticket, when available. | Categorical | Predictor | 80.12% | High missingness and high cardinality; use with caution. |
| `Product_category` | Product category linked to the customer order or support issue, when available. | Categorical | Predictor | 79.98% | High missingness; use with caution. |
| `Item_price` | Price of the item associated with the support ticket, when available. | Numeric | Predictor | 79.97% | High missingness; use only after documented treatment. |
| `connected_handling_time` | Recorded support handling duration, when available. | Numeric | Predictor | 99.72% | Almost entirely missing; generally exclude unless justified. |
| `Agent_name` | Name of the support agent associated with the ticket. | Categorical | Predictor | 0.00% | High cardinality; possible overfitting or identity leakage risk. |
| `Supervisor` | Supervisor responsible for the support agent or ticket handling team. | Categorical | Predictor | 0.00% | Operational grouping; can be considered with interpretation caution. |
| `Manager` | Manager responsible for the supervisor, support agent, or operational team. | Categorical | Predictor | 0.00% | Operational grouping; can be considered with interpretation caution. |
| `Tenure Bucket` | Grouping that describes the support agent's experience or tenure range. | Categorical | Predictor | 0.00% | May be ordinal; confirm order before ordinal encoding. |
| `Agent Shift` | Work shift during which the support agent handled or was assigned the ticket. | Categorical | Predictor | 0.00% | Low-cardinality shift predictor. |
| `CSAT Score` | Original customer satisfaction rating recorded from the survey. | Numeric | Target | 0.00% | Original target reference; prefer csat_score for modeling. |
| `issue_reported_at_parsed` | Standardized parsed version of the issue reported timestamp. | Datetime | Derived Feature | 0.00% | Parsed timestamp retained for traceability and derivation. |
| `issue_responded_parsed` | Standardized parsed version of the issue response timestamp. | Datetime | Derived Feature | 0.00% | Parsed timestamp retained for traceability and derivation. |
| `survey_response_date_parsed` | Standardized parsed version of the survey response date. | Datetime | Derived Feature | 0.00% | Parsed survey date retained for traceability. |
| `response_time_minutes` | Time difference in minutes between issue reporting and support response. | Numeric | Derived Feature | 0.00% | Includes negative/extreme values; use with quality flag. |
| `response_time_bucket` | Grouped response time band used to make response timing easier to review. | Categorical | Derived Feature | 0.00% | Safer grouped response-time feature; includes negative bucket. |
| `issue_hour` | Hour of day when the support issue was reported. | Numeric | Derived Feature | 0.00% | Derived timing feature from issue report timestamp. |
| `issue_day` | Calendar date when the support issue was reported. | Datetime | Derived Feature | 0.00% | Derived date feature; consider aggregation use. |
| `issue_weekday` | Day of week when the support issue was reported. | Categorical | Derived Feature | 0.00% | Derived weekday feature for operational timing patterns. |
| `survey_day` | Calendar date when the customer survey response was submitted. | Datetime | Derived Feature | 0.00% | Use cautiously because survey timing follows support interaction. |
| `survey_weekday` | Day of week when the customer survey response was submitted. | Categorical | Derived Feature | 0.00% | Use cautiously because survey timing follows support interaction. |
| `is_negative_response_time` | Flag showing whether the response timestamp appears earlier than the issue reported timestamp. | Categorical | Derived Feature | 0.00% | Audit/quality flag for invalid timestamp ordering. |
| `is_customer_remarks_missing` | Flag showing whether customer remarks are missing for the ticket. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse text field. |
| `is_order_id_missing` | Flag showing whether the order identifier is missing for the ticket. | Categorical | Derived Feature | 0.00% | Missingness flag for order identifier availability. |
| `is_order_date_time_missing` | Flag showing whether the order date/time is missing for the ticket. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse order timestamp. |
| `is_customer_city_missing` | Flag showing whether customer city information is missing. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse city field. |
| `is_product_category_missing` | Flag showing whether product category information is missing. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse product category. |
| `is_item_price_missing` | Flag showing whether item price information is missing. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse price field. |
| `is_connected_handling_time_missing` | Flag showing whether connected handling time information is missing. | Categorical | Derived Feature | 0.00% | Missingness flag for sparse handling-time field. |
| `customer_remarks_clean` | Basic cleaned version of customer remarks after whitespace cleanup and missing-value standardization. | Text | Derived Feature | 66.62% | Best candidate text field for any future approved NLP. |
| `channel_name_clean` | Basic cleaned version of support channel name. | Categorical | Derived Feature | 0.00% | Cleaned channel field preferred for modeling. |
| `category_clean` | Basic cleaned version of the main issue category. | Categorical | Derived Feature | 0.00% | Cleaned category field preferred for modeling. |
| `sub_category_clean` | Basic cleaned version of the detailed issue sub-category. | Categorical | Derived Feature | 0.00% | Cleaned sub-category field; encoding choice required later. |
| `customer_city_clean` | Basic cleaned version of customer city information. | Categorical | Derived Feature | 80.12% | Cleaned city field; high missingness/cardinality caution. |
| `product_category_clean` | Basic cleaned version of product category information. | Categorical | Derived Feature | 79.98% | Cleaned product category; high missingness caution. |
| `agent_name_clean` | Basic cleaned version of support agent name. | Categorical | Derived Feature | 0.00% | Cleaned agent name; avoid baseline unless justified. |
| `supervisor_clean` | Basic cleaned version of supervisor name. | Categorical | Derived Feature | 0.00% | Cleaned supervisor grouping. |
| `manager_clean` | Basic cleaned version of manager name. | Categorical | Derived Feature | 0.00% | Cleaned manager grouping. |
| `tenure_bucket_clean` | Basic cleaned version of the agent tenure grouping. | Categorical | Derived Feature | 0.00% | Cleaned tenure bucket; possible ordinal field. |
| `agent_shift_clean` | Basic cleaned version of the agent shift grouping. | Categorical | Derived Feature | 0.00% | Cleaned shift grouping. |
| `csat_score` | Numeric standardized version of the customer satisfaction score. | Numeric | Target | 0.00% | Primary numeric CSAT target. |
| `low_csat_flag` | Flag identifying tickets with lower customer satisfaction scores. | Categorical | Target | 0.00% | Binary target variant; do not use as predictor. |
| `high_csat_flag` | Flag identifying tickets with higher customer satisfaction scores. | Categorical | Target | 0.00% | Binary target variant; do not use as predictor. |

## Notes

- Missing percentages are calculated from the processed dataset.
- Variable roles are based on Phase 4 variable-role documentation.
- Datatypes are based on Phase 4 datatype documentation.
- Business meanings are based on Phase 4 business-meaning documentation.
- Target variables are documented explicitly and should not be used as predictors.
- Engineered features are included because they are present in the processed dataset.
