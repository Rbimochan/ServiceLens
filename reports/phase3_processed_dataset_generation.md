# Phase 3 - Processed Dataset Generation

## Purpose

This report documents generation of the first clean prepared dataset for ServiceLens using approved Phase 3 cleaning and feature engineering steps from V1-V8. The raw dataset was preserved unchanged. No rows were silently dropped.

## Input Dataset

`data/raw/customer_support_tickets.csv`

## Processed Dataset Path

`data/processed/customer_support_tickets_prepared.csv`

## Generation Summary

| Metric | Value |
|---|---:|
| Rows read from raw dataset | 85,907 |
| Rows written to processed dataset | 85,907 |
| Rows dropped | 0 |
| Original columns retained | 20 |
| New columns created | 32 |
| Final columns in processed dataset | 52 |

## Columns Retained

The processed dataset retains all original raw columns:

- `Unique id`
- `channel_name`
- `category`
- `Sub-category`
- `Customer Remarks`
- `Order_id`
- `order_date_time`
- `Issue_reported at`
- `issue_responded`
- `Survey_response_Date`
- `Customer_City`
- `Product_category`
- `Item_price`
- `connected_handling_time`
- `Agent_name`
- `Supervisor`
- `Manager`
- `Tenure Bucket`
- `Agent Shift`
- `CSAT Score`

## Columns Created

- `issue_reported_at_parsed`
- `issue_responded_parsed`
- `survey_response_date_parsed`
- `response_time_minutes`
- `response_time_bucket`
- `issue_hour`
- `issue_day`
- `issue_weekday`
- `survey_day`
- `survey_weekday`
- `is_negative_response_time`
- `is_customer_remarks_missing`
- `is_order_id_missing`
- `is_order_date_time_missing`
- `is_customer_city_missing`
- `is_product_category_missing`
- `is_item_price_missing`
- `is_connected_handling_time_missing`
- `customer_remarks_clean`
- `channel_name_clean`
- `category_clean`
- `sub_category_clean`
- `customer_city_clean`
- `product_category_clean`
- `agent_name_clean`
- `supervisor_clean`
- `manager_clean`
- `tenure_bucket_clean`
- `agent_shift_clean`
- `csat_score`
- `low_csat_flag`
- `high_csat_flag`

## Cleaning and Feature Steps Applied

| Area | Action Applied |
|---|---|
| Missing values | Created missingness flags for sparse fields; no imputation applied. |
| Duplicates | No duplicate rows removed because earlier duplicate analysis found no full-row or `Unique id` duplicates. |
| Datatypes | Parsed verified datetime fields into new parsed columns; created numeric `csat_score`. |
| Datetime engineering | Created issue date/hour/weekday and survey date/weekday features. |
| Response time | Created `response_time_minutes`, `response_time_bucket`, and `is_negative_response_time`. |
| Text cleaning | Created `customer_remarks_clean` using basic whitespace stripping and empty-string standardization only. |
| Categorical cleaning | Created cleaned categorical columns with whitespace stripped and empty strings standardized as missing. |
| CSAT target variants | Created `csat_score`, `low_csat_flag`, and `high_csat_flag`. |

## Rows Flagged

| Flag / Issue | Count |
|---|---:|
| Negative response time rows | 3,128 |
| Customer Remarks missing | 57,234 |
| Order_id missing | 18,232 |
| order_date_time missing | 68,693 |
| Customer_City missing | 68,828 |
| Product_category missing | 68,711 |
| Item_price missing | 68,701 |
| connected_handling_time missing | 85,665 |
| Low CSAT flag rows | 15,071 |
| High CSAT flag rows | 70,836 |

## Datetime Parse Status

| Column | Parse Failures |
|---|---:|
| Issue_reported at | 0 |
| issue_responded | 0 |
| Survey_response_Date | 0 |

## Response Time Bucket Counts

| Bucket | Count |
|---|---:|
| negative | 3,128 |
| 0 minutes | 2,448 |
| 1-5 minutes | 38,038 |
| 6-30 minutes | 19,750 |
| 31-60 minutes | 4,484 |
| 1-4 hours | 7,399 |
| 4-24 hours | 7,783 |
| more than 24 hours | 2,877 |

## CSAT Target Variant Counts

| CSAT Feature / Score | Count |
|---|---:|
| CSAT score 1 | 11,230 |
| CSAT score 2 | 1,283 |
| CSAT score 3 | 2,558 |
| CSAT score 4 | 11,219 |
| CSAT score 5 | 59,617 |
| Invalid CSAT values | 0 |
| `low_csat_flag = 1` | 15,071 |
| `high_csat_flag = 1` | 70,836 |

## Known Limitations

- No rows were removed; invalid timestamp ordering is preserved using `is_negative_response_time`.
- Missing values were flagged but not imputed.
- High-missingness columns were retained for traceability, even if they may be excluded later from modeling.
- No fake resolution time, priority, escalation, interaction count, or proposal-only variables were created.
- Frequency encoding, one-hot encoding, and model-specific transformations were not applied in this dataset.
- `response_time_minutes` should be used carefully because it includes negative and extreme values.

## Raw Data Protection

The raw CSV was read as input only and was not overwritten or modified. The prepared dataset was saved separately under `data/processed/`.

## Next Step

Review the prepared dataset schema before using it for EDA, modeling, or Tableau. Any future row removal or feature exclusion should be documented in a separate report.
