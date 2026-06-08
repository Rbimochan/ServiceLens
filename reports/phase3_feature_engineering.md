# Phase 3 - Feature Engineering

## Purpose

This report documents safe engineered features for analysis and later modeling using only verified columns available in the customer support ticket dataset. Feature checks were performed in memory for planning and validation only. The raw dataset was not modified and no processed dataset was created.

## Dataset Location

`data/raw/customer_support_tickets.csv`

## Verified Source Columns Used

| Source Column | Use |
|---|---|
| `Issue_reported at` | Datetime features and response time calculation. |
| `issue_responded` | Response time calculation. |
| `Survey_response_Date` | Survey date features if needed later. |
| `CSAT Score` | Target variants. |
| `Customer Remarks` | Missingness flag and optional cleaned text field. |
| `Order_id` | Missingness flag only; not a baseline predictive feature. |
| `order_date_time` | Missingness flag only unless retained later. |
| `Customer_City` | Missingness flag and cleaned categorical field if retained. |
| `Product_category` | Missingness flag and cleaned categorical field if retained. |
| `Item_price` | Missingness flag and numeric feature only if retained. |
| `connected_handling_time` | Missingness flag only unless retained later. |
| Categorical fields | Cleaned categorical versions for consistent later encoding. |

No fake resolution time, priority, escalation, proposal-only variable, or interaction count was created.

## Datetime Features

| Engineered Feature | Derived From | Definition | Validation Status |
|---|---|---|---|
| `issue_hour` | `Issue_reported at` | Hour of issue report, 0-23. | Source parsed successfully. |
| `issue_day` | `Issue_reported at` | Calendar date of issue report. | Source parsed successfully. |
| `issue_weekday` | `Issue_reported at` | Weekday name of issue report. | Source parsed successfully. |
| `survey_day` | `Survey_response_Date` | Calendar date of survey response, if needed later. | Source parsed successfully. |
| `survey_weekday` | `Survey_response_Date` | Weekday name of survey response, if needed later. | Source parsed successfully. |

## Response Time Features

| Engineered Feature | Derived From | Definition | Notes |
|---|---|---|---|
| `response_time_minutes` | `issue_responded - Issue_reported at` | Response delay in minutes. | Can be negative for invalid timestamp ordering. |
| `response_time_bucket` | `response_time_minutes` | Bucketed response time group. | Should include a `negative` bucket. |
| `is_negative_response_time` | `response_time_minutes` | Boolean flag for response time below 0. | Keep invalid rows flagged; do not delete yet. |

## Missingness Flags for Sparse Fields

| Engineered Feature | Source Column | Missing Count | Purpose |
|---|---|---:|---|
| `is_customer_remarks_missing` | `Customer Remarks` | 57,151 | Preserve whether customer text is absent. |
| `is_order_id_missing` | `Order_id` | 18,232 | Track missing order identifiers. |
| `is_order_date_time_missing` | `order_date_time` | 68,693 | Track sparse order datetime availability. |
| `is_customer_city_missing` | `Customer_City` | 68,828 | Track sparse location availability. |
| `is_product_category_missing` | `Product_category` | 68,711 | Track sparse product category availability. |
| `is_item_price_missing` | `Item_price` | 68,701 | Track sparse price availability. |
| `is_connected_handling_time_missing` | `connected_handling_time` | 85,665 | Track sparse handling time availability. |

## Cleaned Categorical Fields

| Cleaned Field | Source Column | Cleaning Rule | Notes |
|---|---|---|---|
| `channel_name_clean` | `channel_name` | Strip whitespace; standardize empty strings as missing. | Low-cardinality field for later encoding. |
| `category_clean` | `category` | Strip whitespace; standardize empty strings as missing. | Low-cardinality field for later encoding. |
| `sub_category_clean` | `Sub-category` | Strip whitespace; standardize empty strings as missing. | Medium-cardinality field. |
| `customer_city_clean` | `Customer_City` | Strip whitespace; standardize empty strings as missing. | High missingness; use with caution. |
| `product_category_clean` | `Product_category` | Strip whitespace; standardize empty strings as missing. | High missingness; use with caution. |
| `agent_name_clean` | `Agent_name` | Strip whitespace; standardize empty strings as missing. | High-cardinality name field; avoid baseline model use unless justified. |
| `supervisor_clean` | `Supervisor` | Strip whitespace; standardize empty strings as missing. | Medium-cardinality operational field. |
| `manager_clean` | `Manager` | Strip whitespace; standardize empty strings as missing. | Low-cardinality operational field. |
| `tenure_bucket_clean` | `Tenure Bucket` | Strip whitespace; standardize empty strings as missing. | May be ordinal; confirm order before label encoding. |
| `agent_shift_clean` | `Agent Shift` | Strip whitespace; standardize empty strings as missing. | Low-cardinality operational field. |

## CSAT Target Variants

| Engineered Feature | Source Column | Definition | Count / Status |
|---|---|---|---|
| `csat_score` | `CSAT Score` | Numeric version of CSAT score. | 85,907 valid values; 0 invalid values. |
| `low_csat_flag` | `CSAT Score` | 1 when `csat_score <= 3`, else 0. | 15,071 true values. |
| `high_csat_flag` | `CSAT Score` | 1 when `csat_score >= 4`, else 0. | 70,836 true values. |

## CSAT Score Distribution Check

| CSAT Score | Count |
|---:|---:|
| 1 | 11,230 |
| 2 | 1,283 |
| 3 | 2,558 |
| 4 | 11,219 |
| 5 | 59,617 |

## Recommended Feature Set for Later Processing

| Feature Type | Recommended Features |
|---|---|
| Datetime | `issue_hour`, `issue_day`, `issue_weekday`, optional `survey_day`, optional `survey_weekday` |
| Response time | `response_time_minutes`, `response_time_bucket`, `is_negative_response_time` |
| Missingness flags | Sparse-field missingness flags listed above |
| Cleaned categoricals | Cleaned versions of support channel, category, team, tenure, and shift fields |
| Target variants | `csat_score`, `low_csat_flag`, `high_csat_flag` |

## Excluded Unsafe Features

| Feature | Reason |
|---|---|
| Resolution time | No verified resolution timestamp is available. |
| Priority | No verified priority column is available. |
| Escalation flag | No verified escalation column is available. |
| Interaction count | No verified interaction count column is available. |
| Proposal-only business variables | Not present in the verified dataset columns. |

## Risks

- `response_time_minutes` includes negative values and should not be used without the `is_negative_response_time` flag.
- Sparse fields may create biased features if missingness is related to customer or operational processes.
- Cleaned categorical fields still need encoding decisions before modeling.
- `high_csat_flag` and `low_csat_flag` are derived target variants and should not both be used as simultaneous targets in one model.
- CSAT is imbalanced toward high scores, which should be considered in later modeling.

## Next Step

Review this feature plan together with the missing value, duplicate, datatype, datetime, lifecycle, text cleaning, and categorical encoding reports before creating a processed dataset.
