# Phase 4 - Variable Roles

## Purpose

This report identifies the role of every variable in the processed ServiceLens dataset. Roles are classified as Target, Predictor, Metadata, Identifier, or Derived Feature. No models were trained in this step.

## Dataset

`data/processed/customer_support_tickets_prepared.csv`

## Role Definitions

| Role | Meaning |
|---|---|
| Target | Customer satisfaction outcome variable or target variant for later analysis/modeling. |
| Predictor | Candidate input variable for later analysis/modeling. |
| Metadata | Context, audit, timing, or descriptive information that supports interpretation but is not a primary model input by default. |
| Identifier | Record or order identifier that should be preserved for traceability but not used as a standard predictor. |
| Derived Feature | Feature created during data preparation from existing verified columns. |

## Variable Role Dictionary

| Column | Role | Rationale |
|---|---|---|
| `Unique id` | Identifier | Unique ticket record identifier used for traceability. |
| `channel_name` | Predictor | Support channel may help explain satisfaction patterns. |
| `category` | Predictor | Main issue category may help explain satisfaction patterns. |
| `Sub-category` | Predictor | Detailed issue category may help explain satisfaction patterns. |
| `Customer Remarks` | Metadata | Original text field preserved for context; cleaned version may be used later with caution. |
| `Order_id` | Identifier | Order identifier is traceability metadata rather than a baseline predictor. |
| `order_date_time` | Metadata | Sparse original order timestamp retained for context. |
| `Issue_reported at` | Metadata | Original raw timestamp preserved for traceability; parsed/derived versions are used for features. |
| `issue_responded` | Metadata | Original raw response timestamp preserved for traceability; parsed/derived versions are used for features. |
| `Survey_response_Date` | Metadata | Original survey date preserved for traceability; parsed/derived versions are used for features. |
| `Customer_City` | Predictor | Customer city may support later analysis if retained despite missingness. |
| `Product_category` | Predictor | Product category may support later analysis if retained despite missingness. |
| `Item_price` | Predictor | Item price may support later analysis if retained despite missingness. |
| `connected_handling_time` | Predictor | Handling duration may support later analysis if retained despite high missingness. |
| `Agent_name` | Predictor | Agent assignment may explain operational patterns, but should be used cautiously. |
| `Supervisor` | Predictor | Supervisor grouping may explain operational patterns. |
| `Manager` | Predictor | Manager grouping may explain operational patterns. |
| `Tenure Bucket` | Predictor | Agent tenure grouping may explain satisfaction patterns. |
| `Agent Shift` | Predictor | Agent shift may explain timing or workload patterns. |
| `CSAT Score` | Target | Original customer satisfaction rating. |
| `issue_reported_at_parsed` | Derived Feature | Parsed version of issue reported timestamp. |
| `issue_responded_parsed` | Derived Feature | Parsed version of issue response timestamp. |
| `survey_response_date_parsed` | Derived Feature | Parsed version of survey response date. |
| `response_time_minutes` | Derived Feature | Derived response delay in minutes. |
| `response_time_bucket` | Derived Feature | Derived categorical response time band. |
| `issue_hour` | Derived Feature | Derived hour of issue report. |
| `issue_day` | Derived Feature | Derived date of issue report. |
| `issue_weekday` | Derived Feature | Derived weekday of issue report. |
| `survey_day` | Derived Feature | Derived date of survey response. |
| `survey_weekday` | Derived Feature | Derived weekday of survey response. |
| `is_negative_response_time` | Derived Feature | Derived quality flag for invalid timestamp ordering. |
| `is_customer_remarks_missing` | Derived Feature | Derived missingness flag. |
| `is_order_id_missing` | Derived Feature | Derived missingness flag. |
| `is_order_date_time_missing` | Derived Feature | Derived missingness flag. |
| `is_customer_city_missing` | Derived Feature | Derived missingness flag. |
| `is_product_category_missing` | Derived Feature | Derived missingness flag. |
| `is_item_price_missing` | Derived Feature | Derived missingness flag. |
| `is_connected_handling_time_missing` | Derived Feature | Derived missingness flag. |
| `customer_remarks_clean` | Derived Feature | Cleaned version of the original customer remarks text. |
| `channel_name_clean` | Derived Feature | Cleaned version of support channel. |
| `category_clean` | Derived Feature | Cleaned version of issue category. |
| `sub_category_clean` | Derived Feature | Cleaned version of issue sub-category. |
| `customer_city_clean` | Derived Feature | Cleaned version of customer city. |
| `product_category_clean` | Derived Feature | Cleaned version of product category. |
| `agent_name_clean` | Derived Feature | Cleaned version of agent name. |
| `supervisor_clean` | Derived Feature | Cleaned version of supervisor. |
| `manager_clean` | Derived Feature | Cleaned version of manager. |
| `tenure_bucket_clean` | Derived Feature | Cleaned version of tenure bucket. |
| `agent_shift_clean` | Derived Feature | Cleaned version of agent shift. |
| `csat_score` | Target | Numeric standardized CSAT target. |
| `low_csat_flag` | Target | Binary lower-satisfaction target variant. |
| `high_csat_flag` | Target | Binary higher-satisfaction target variant. |

## Notes

- Multiple target variants are documented, but only one should be selected for a given future model or analysis task.
- Identifier fields are preserved for traceability and should not be used as baseline predictors.
- Some predictors have high missingness and may later be excluded depending on the modeling or reporting objective.
- Derived features are created from verified available columns only.
